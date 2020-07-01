import c5e
from math_model import BB_movement, SVA_movement
import logging
import canopen
import time
import numpy as np
import serial
#TODO limmit/monitor torque?

class CDPR():

    can_ids = [1,2,3,4]
    motors = []

    def __init__(self):
        #initialise can network
        self.ser = serial.Serial('COM8', 9800, timeout=1)  # open serial port for EE controller
        self._state = 0
        self.network = canopen.Network()     # define network
        self.network.connect(channel='PCAN_USBBUS1', bustype='pcan', bitrate=1000000)  # establish communication
        self.network.check()
        #create driver objects
        for id in self.can_ids:
            motor = c5e.Driver(self.network, id)
            motor.enable()
            self.motors.append(motor)
        self.network.sync.start(0.1)

        self._position = (0, 4, 0) #TODO home
        self._SVA_pos = 0          #TODO SVA home

    def __del__(self):
        #shuts down when destroyed
        #self.shutdown() #TODO determine a fix if feature is wanted
        pass

    def shutdown(self):
        logging.info("Shutting Down")
        for motor in self.motors:
            motor.shutdown()
        time.sleep(1)   #TODO wait for shutdown
        self.network.sync.stop()
        self.network.disconnect()
        self.ser.close()
        #TODO (possibly home?), not error if already shut down
        
    def goto(self, position, accel_max, relative=True, blocking=True):

        #if self._state == 1:
            #raise Exception("goto called in SVA mode. Must undock to execute goto")
        #determine movement to make, absolute or relative
        init_pos = self._position
        if relative:
            end_pos = np.add(init_pos, position)
        else:
            end_pos = position
        self._position = end_pos
        
        rel_pos_int, motor_speed_int, motor_accel, motor_deccel, cycle_time = BB_movement(init_pos, end_pos, accel_max)
        logging.info("Moving with cycle time of: %.2f"%cycle_time)


        for idx, motor in enumerate(self.motors):
            motor.goto(rel_pos_int[idx], relative=True, blocking=False, speed=motor_speed_int[idx], acceleration=motor_accel[idx], deceleration=motor_deccel[idx])

        #time.sleep(0.5) #DEBUG
        #for motor in self.motors: #DEBUG
            #print(motor.get_position()) #DEBUG

        while(not self.is_at_target() and blocking):
            time.sleep(0.001) #idle checking at 1khz

    def SVA_move(self, position, accel_max, blocking=True):
        #if self._state == 0:
            #raise Exception("SVA_move called outside of SVA mode. Must dock to execute SVA_move")
        init_pos = self._SVA_pos
        end_pos = position
        self._SVA_pos = end_pos

        rel_pos_int, motor_speed_int, motor_accel, motor_deccel, cycle_time = SVA_movement(init_pos, end_pos, accel_max)
        logging.info("Moving with cycle time of: %.2f" % cycle_time)

        for idx, motor in enumerate(self.motors):
            motor.goto(rel_pos_int[idx], relative=True, blocking=False, speed=motor_speed_int,
                       acceleration=motor_accel, deceleration=motor_deccel)

        while (not self.is_at_target() and blocking):
            time.sleep(0.001)  # idle checking at 1khz

    def is_at_target(self):
        for motor in self.motors:
            if not motor.is_at_target():
                return False
        return True

    def home(self):
        pass #TODO

    def is_homed(self):
        return False #TODO

    def grab(self):
        self.motors[0].set_output(2, True)
        #TODO test

    def release(self):
        self.motors[0].set_output(2, False)
        #TODO test

    def grab_ser(self):
        self.ser.write(b'L')
        time.sleep(4)

    def release_ser(self):
        self.ser.write(b'H')
        time.sleep(4)

    def stop(self): #method of invoking halt from Goto_test
        for motor in self.motors:
            motor.halt(halt=1)

    def unstop(self): #method of invoking halt from Goto_test
        for motor in self.motors:
            motor.halt(halt=0)

    def torq_report(self): #reports each motor torque
        for motor in self.motors:
            print(motor.get_torque())

    def dock(self):
        if self._state == 1:
            raise Exception("dock called when in SVA mode, already docked into SCA mode")
        self.goto((-7, 20, 0), 50, relative=False)
        self.goto((-18, 20, 0), 50, relative=False)
        self.goto((-18, 19, 0), 50, relative=False)
        self._state = 1

    def undock(self):
        print("state is")
        print(self._state)
        if self._state == 0:
            raise Exception("undock called when not in SVA mode, already undocked")
        self.SVA_move(0, 50)
        self._state = 0
        self.goto((-18, 20, 0), 50, relative=False)
        self.goto((-7, 20, 0), 50, relative=False)