import queue, threading
import logging
import time
import canopen

#TODO constants
#TODO blocking and is_at_target
#TODO state change delay while checking
HALT_SLOW_RAMP = 1
HALT_QUICK_RAMP = 2

class Driver():
    #TODO why all the sleeps?
    #TODO if goto do we clear buffer? how might we want to manipulate buffer? 

    def __init__(self, can_network: canopen.Network, can_id, use_buffer=False, max_speed=50, max_accel=500, max_jerk=0):
        '''
        Initialise controller and put into switched on state
        '''
        self.can_network = can_network
        self.can_id = can_id
        
        # Add node to network TODO: scan for and add node
        self.node = canopen.RemoteNode(can_id, 'C5-E-1-09.eds')
        can_network.add_node(self.node)
        can_network.sync.start(0.1) #TODO can this be called by every driver?
        self.node.tpdo.read() # checks if configured properly
        self.node.rpdo.read()
        time.sleep(0.1)

        self._max_jerk = 0
        self._max_accel = 0
        self._max_speed = 0
        self.max_speed = max_speed
        self.max_accel = max_accel
        self.max_jerk = max_jerk

        #setup the trajectory queue and its worker thread
        if use_buffer:
            self.trajectory_queue = queue.Queue() #https://docs.python.org/3/library/queue.html#queue-objects
            threading.Thread(target=self._trajectory_handler, daemon=True).start()
        
        logging.info("Initialized c5e with id: %d"%can_id)

    def goto(self, pos, relative = False, blocking=True, 
             speed = None, accel = None, jerk = None):
        '''
        Set target position immediately with optional speed, acceleration and jerk
        '''
        self.node.sdo[0x607A].raw = pos     # target position is stored in 0x607A
        if speed is not None: self.max_speed = speed
        if accel is not None: self.max_accel = accel
        if jerk is not None: self.max_jerk = jerk
        time.sleep(0.1)

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
        time.sleep(0.1)

        while(not self.is_at_target() and blocking):
            time.sleep(0.001) #idle checking at 1khz

        #TODO test

    def is_at_target(self):
        '''
        Return wether or not the motor is at its target
        '''
        #return 10th bit of 6040h
        return bool(0b10000000000 & self.node.sdo[0x6041].raw) #TODO test

    def halt(self, halt):
        '''
        Stops the motor (6040h Bit 8, 605D)
        '''
        if halt: 
            self.node.sdo[0x6040].raw |= 0b100000000 #set bit 8 to 1
        else:
            self.node.sdo[0x6040].raw &= ~0b100000000 #set bit 8 to 0
        #TODO test 

    def shutdown(self):
        '''
        Shuts down the drive, into low power state
        '''
        self.node.sdo[0x6040].raw = 0b00110
        logging.info("Shutdown drive %d"%self.can_id)
        #TODO test

    def enable(self):
        '''
        Puts drive into operational state
        '''
        self.node.sdo[0x6040].raw = 0b110    # ready to switch state
        time.sleep(0.1)
        self.node.sdo[0x6060].raw = 0b1      # Set mode of operation to profile position
        time.sleep(0.1)
        self.node.sdo[0x6040].raw = 0b111    # switched on
        time.sleep(0.1)
        self.node.sdo[0x6040].raw = 0b1111   # operation enabled
        time.sleep(0.1)
        logging.info("Enabled drive %d"%self.can_id)
        #TODO test

    def get_torque(self):
        '''
        Get the current actual torque on the motor
        '''
        return self.node.sdo[0x6077].raw   # operation enabled
        #TODO test

    def get_velocity(self):
        '''
        Get the current actual velocity of the motor
        '''
        return self.node.sdo[0x606B].raw 
        #TODO test

    def get_position(self):
        '''
        Get the actual position of the motor (closed loop)
        '''
        return self.node.sdo[0x6064].raw
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

    @property
    def max_speed(self):
        return self._max_speed
    @max_speed.setter
    def max_speed(self, value):
        if value == self.max_speed:
            return
        self.node.sdo[0x6081].raw = value
        self._max_speed = value
        #TODO test

    @property
    def max_accel(self):
        return self._max_accel
    @max_accel.setter
    def max_accel(self, value):
        if value == self.max_accel:
            return
        #change acceleration and deacelleration 
        self.node.sdo[0x6083].raw = value
        self.node.sdo[0x6084].raw = value
        self._max_accel = value
        #TODO test
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