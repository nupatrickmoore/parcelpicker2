

class Driver():

    #TODO units
    #TODO position buffer? internal buffer limmited 
    #TODO what power states matter

    #TODO constants
    HALT_SLOW_RAMP = 1
    HALT_QUICK_RAMP = 2

    def __init__(self, can_id):
        '''
        Initialise controller and put into switched on state
        '''
        self.max_speed = 10
        self.max_accel = 10
        self.max_jerk = 10

        pass #TODO

    def goto(self, pos, relative = False,  
             speed = self.max_speed, accel = self.max_accel, jerk = self.max_jerk):
        '''
        Set target position immediatly with optional speed, acceleration and jerk
        '''
        self.max_speed = speed
        self.max_accel = accel
        self.max_jerk = jerk

        pass #TODO


    def halt(self, mode = self.HALT_QUICK_RAMP):
        '''
        Stops the motor (6040h Bit 8, 605D)
        '''
        pass #TODO

    def get_torque(self):
        '''
        Get the current actual torque on the motor
        '''
        return #TODO

    def get_velocity(self):
        '''
        Get the current actual velocity of the motor
        '''
        return #TODO

    def get_position(self):
        '''
        Get the actual position of the motor (closed loop)
        '''
        return #TODO

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
        #TODO send command to change max speed
        self._max_speed = value

    @property
    def max_accel(self):
        return self._max_accel

    @max_accel.setter
    def max_accel(self, value):
        if value == self.max_accel:
            return
        #TODO send command to change max acceleration
        self._max_accel = value

            @property
    def max_jerk(self):
        return self._max_jerk

    @max_jerk.setter
    def max_jerk(self, value):
        if value == self.max_jerk:
            return
        #TODO send command to change max jerk
        self._max_jerk = value