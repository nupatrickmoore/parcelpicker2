import queue, threading
import logging
import time
import canopen
import sys
from enum import Enum

#TODO state change delay while checking

#c5e file constants
class State(Enum):
    ERROR = -1
    NOT_READY_TO_SWITCH = 0
    SWITCH_DISSABLED = 1
    READY_TO_SWITCH = 2
    SWITCHED_ON = 3
    OPERATION_ENABLED = 4
    QUICK_STOP = 5
    FAULT_REACTION = 6
    FAULT = 7

class Driver():
    #TODO error on movent if not operational state, and report current state (statusword tranlator)
    SDO_DELAY_RATE = 0.02

    def __init__(self, can_network: canopen.Network, can_id, use_buffer=False, max_speed=50, max_accel=500, max_deccel=500, max_jerk=0):
        '''
        Initialise controller and put into switched on state
        '''
        self.can_network = can_network
        self.can_id = can_id
        
        # Add node to network TODO: scan for and add node (Pat what is this?)
        self.node = canopen.RemoteNode(can_id, 'C5-E-1-09.eds')
        can_network.add_node(self.node)
        try:
            self.node.tpdo.read() # checks if configured properly
            self.node.rpdo.read()
        except:
            sys.exit(f"Drive {self.can_id} failed to configure. Turn on or restart the device")
        time.sleep(self.SDO_DELAY_RATE)

        self._state = 0
        self._max_jerk = 0
        self._max_accel = 0
        self._max_deccel = 0
        self._max_speed = 0
        self.max_speed = max_speed
        self.max_accel = max_accel
        self.max_deccel = max_deccel
        self.max_jerk = max_jerk

        # Enable controlword bit 4 release when at target
        self.node.sdo[0x60F2].raw = 0b10001

        #enable PWM on pin 1
        self.node.sdo[0x2038][0x05].raw = 50 # set PWM frequency to 50hz (default for RC servo)

        self.node.sdo[0x3250][0x08].raw = 0b1 # enables routing
        self.node.sdo[0x3252][0x02].raw = 0x1001 #assigns PWM to output 1 controlled by bit 1 of 60FE
        self.node.sdo[0x60FE][0x01].raw |= 0b10 #enable PWM

        #setup the trajectory queue and its worker thread
        if use_buffer:
            self.trajectory_queue = queue.Queue() #https://docs.python.org/3/library/queue.html#queue-objects
            threading.Thread(target=self._trajectory_handler, daemon=True).start()
        logging.info("Initialized c5e with id: %d"%can_id)

    def goto(self, pos, relative = False, blocking=True, 
             speed = None, acceleration = None, deceleration = None, jerk = None):
        '''
        Set target position immediately with optional speed, acceleration and jerk
        '''

        if self.get_state() is not State.OPERATION_ENABLED:
            raise Exception(f"Cannot move in {self.get_state()} state")

        self.node.sdo[0x607A].raw = pos     # target position is stored in 0x607A
        #print(pos) #DEBUG
        if speed is not None: self.max_speed = speed
        if acceleration is not None: self.max_accel = acceleration
        if deceleration is not None: self.max_deccel = deceleration
        if jerk is not None: self.max_jerk = jerk
        time.sleep(self.SDO_DELAY_RATE)

        #create controlword with optional parameters
        '''
        immediate =      0b0100000
        relative =       0b1000000
        halt =         0b100000000
        pass_pos =    0b1000000000
        '''
        controlword = 0b0111111 # bit 4 = 1 new travel command problem
        if relative: controlword |= 0b1000000 #adds bit 6 if relative 
        self.node.sdo[0x6040].raw = controlword 
        time.sleep(self.SDO_DELAY_RATE)

        while(not self.is_at_target() and blocking):
            time.sleep(self.SDO_DELAY_RATE) #idle checking at 1khz

    def is_at_target(self):
        '''
        Return wether or not the motor is at its target
        '''

        #return 10th bit of 6040h
        return bool(0b10000000000 & self.node.sdo[0x6041].raw)

    def halt(self, halt):
        '''
        Stops the motor (6040h Bit 8, 605D)
        '''
        if halt == 1:
            self.node.sdo[0x6040].raw |= 0b100000000    #set bit 8 to 1
            #print("halted") #DEBUG
        else:
            self.node.sdo[0x6040].raw &= ~0b100000000   #set bit 8 to 0
            #print("unhalted") #DEBUG

    def shutdown(self):
        '''
        Shuts down the drive, into low power state
        '''
        self.node.sdo[0x6040].raw = 0b00110
        time.sleep(self.SDO_DELAY_RATE)
        logging.info("Shutdown drive %d"%self.can_id)

    def enable(self):
        '''
        Puts drive into operational state
        '''
        self.node.sdo[0x6040].raw = 0b110    # ready to switch state
        time.sleep(self.SDO_DELAY_RATE)
        self.node.sdo[0x6060].raw = 0b1      # Set mode of operation to profile position
        time.sleep(self.SDO_DELAY_RATE)
        self.node.sdo[0x6040].raw = 0b111    # switched on
        time.sleep(self.SDO_DELAY_RATE)
        self.node.sdo[0x6040].raw = 0b1111   # operation enabled
        time.sleep(self.SDO_DELAY_RATE)
        logging.info("Enabled drive %d"%self.can_id)
    
    def get_state(self):
        state = self.node.sdo[0x6041].raw
        if (state & 0b01001111) == 0b0: #take the bitmask and see if it then matches a mode
            return State.NOT_READY_TO_SWITCH
        elif (state & 0b01001111) == 0b01000000:
            return State.SWITCH_DISSABLED
        elif (state & 0b01101111) == 0b0100001:
            return State.READY_TO_SWITCH
        elif (state & 0b01101111) == 0b0100011:
            return State.SWITCHED_ON
        elif (state & 0b01101111) == 0b0100111:
            return State.OPERATION_ENABLED
        elif (state & 0b01101111) == 0b0000111:
            return State.QUICK_STOP
        elif (state & 0b01001111) == 0b0001111:
            return State.FAULT_REACTION
        elif (state & 0b01001111) == 0b0001000:
            return State.FAULT
        else:
            return State.ERROR
        #TODO test

    def get_torque(self):
        '''
        Get the current actual torque on the motor
        '''
        #print(self.node.sdo[0x6077].raw) #DEBUG
        return self.node.sdo[0x6077].raw   # operation enabled

        #TODO reports, but only 0's, might be lack of load

    def get_velocity(self):
        '''
        Get the current actual velocity of the motor
        '''
        return self.node.sdo[0x606C].raw

    def get_position(self):
        '''
        Get the actual position of the motor (closed loop)
        '''
        return self.node.sdo[0x6064].raw

    def set_output(self, duty): #for use with EE functionality
        '''
        Sets the PWM duty cycle of pin 1 (0,2-100)
        '''
        self.node.sdo[0x2038][0x06].raw = duty 
        #TODO test



##################################
## Buffered Trajectory 
##################################

    def append_trajectory(self, pos, relative = False,  
                      speed = None, accel = None, jerk = None):
        '''
        Appends a target movement to the buffer
        '''
        self.trajectory_queue.put_nowait((pos, relative, speed, accel, jerk))

    def clear_trajectories(self):
        with self.trajectory_queue.mutex:
            self.trajectory_queue.queue.clear()
        #TODO clear internal buffer or handle some other way

    def _trajectory_handler(self):
        while True:
            '''
            #TODO
            if not self.trajectory_queue.empty() and (6041h, Bit 12) == 0:
                trajectory = self.trajectory_queue.get()
                #send the trajectory to the internal buffer, each trajectory is separate if separate_trajectories
                self.trajectory_queue.task_done()
                #personal note: look into whether a yeild is necessary 
            '''
            pass

##################################
## Properties 
##################################
    
    #Speed property   
    @property
    def max_speed(self):
        return self._max_speed
    @max_speed.setter
    def max_speed(self, value):
        if value == self.max_speed:
            return
        self.node.sdo[0x6081].raw = value
        self._max_speed = value

    #Acceleration property   
    @property
    def max_accel(self):
        return self._max_accel
    @max_accel.setter
    def max_accel(self, value):
        if value == self.max_accel:
            return
        #change acceleration and deacelleration 
        self.node.sdo[0x6083].raw = value
        self._max_accel = value

    #Deceleration property   
    @property
    def max_deccel(self):
        return self._max_deccel
    @max_deccel.setter
    def max_deccel(self, value):
        if value == self.max_deccel:
            return
        #change acceleration and deacelleration 
        self.node.sdo[0x6084].raw = value
        self._max_deccel = value

    #Jerk property   
    @property
    def max_jerk(self):
        return self._max_jerk
    @max_jerk.setter
    def max_jerk(self, value):
        if value == self.max_jerk:
            return
        # enable jerk limmiting if max jerk is defined
        if value != 0 and self._max_jerk == 0:
            self.node.sdo[0x6086].raw = 3       
        elif value == 0:
            self.node.sdo[0x6086].raw = 0       
        # set profile jerk for all 4 occurrences
        for i in range(4):
            self.node.sdo[0x60A4][i].raw = value 
        self._max_jerk = value 
        #TODO test
