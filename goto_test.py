from core import CDPR #relative import of core
import time
import logging

#logging.basicConfig(level=logging.DEBUG)

print("Initialising")
cdpr = CDPR()
#quick test accel var
accel = 30
accel2 = 30

cdpr.dock()
cdpr.undock()
cdpr.goto((0, 4, 0), accel, relative=False)

cdpr.shutdown()
print("Shutdown")