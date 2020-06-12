import c5e
from math_model import BB_movement
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
        #TODO test, (possibly home?), not error if already shut down
        
    def goto(self, position, accel_max, relative=True, blocking=True):

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
        ser = serial.Serial('COM4', 9800, timeout=1)  # open serial port for EE controller
        ser.write(b'L')
        ser.close()
        #TODO Test

    def release_ser(self):
        ser = serial.Serial('COM4', 9800, timeout=1)  # open serial port for EE controller
        ser.write(b'H')
        ser.close()
        #TODO Test

    def stop(self): #method of invoking halt from Goto_test
        for motor in self.motors:
            motor.halt(halt=1)

    def unstop(self): #method of invoking halt from Goto_test
        for motor in self.motors:
            motor.halt(halt=0)

    def torq_report(self): #reports each motor torque
        for motor in self.motors:
            print(motor.get_torque())