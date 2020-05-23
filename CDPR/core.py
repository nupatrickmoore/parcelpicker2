import c5e
import math_model
import logging
import canopen
import time

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
            self.motors.append(motor)
        self.network.sync.start(0.1) 

        #TODO home

    def __del__(self):
        #shuts down when destroyed
        self.shutdown()

    def shutdown(self):
        logging.info("Shutting Down")
        for motor in self.motors:
            motor.shutdown()
        self.network.sync.stop()
        self.network.disconnect()
        #TODO test, (possibly home?)
        
    def goto(self, position, cycle_time, relative=False, blocking=True):

        #TODO determine init_position

        if relative:
            end_pos = init_pos + position
        else:
            end_pos = position

        rel_pos_int, motor_speed_int = math_model.oneshot_movement(init_pos, end_pos, cycle_time)

        for idx, motor in enumerate(self.motors):
            motor.goto(rel_pos_int[idx], relative=True, blocking=False, speed=motor_speed_int[idx])

        while(not self.is_at_target() and blocking):
            time.sleep(0.001) #idle checking at 1khz
        #TODO

    def is_at_target(self):
        for motor in self.motors:
            if not motor.is_at_target():
                return False
        return True #TODO

    def home(self):
        pass #TODO

    def is_homed(self):
        return False #TODO

    def grab(self):
        pass #TODO

    def release(self):
        pass #TODO