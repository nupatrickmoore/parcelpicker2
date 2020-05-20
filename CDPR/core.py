import c5e
import mathmodel.math_model
import logging

class CDPR():

    def __init__(self):
        #initialise can network
        pass #TODO

    def shutdown(self):
        logging.info("Shutting Down")
        #TODO tell drives to shutdown, possibly homes
        
    def goto(self, position, speed, relative=False, wait=True):
        x, y, z = position
        pass #TODO

    def is_at_target(self):
        return True #TODO

    def home(self):
        pass #TODO

    def grab(self):
        pass #TODO

    def release(self):
        pass #TODO