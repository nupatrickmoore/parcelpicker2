from core import CDPR #relative import of core
import time
import logging

#logging.basicConfig(level=logging.DEBUG)

print("Initialising")
cdpr = CDPR()
#quick test accel var
accel = 150
accel2 = 30

print("Moving")
cdpr.goto((-20, 12, 0), accel, relative=False)
print("Moving")
cdpr.goto((-20, 4, 0), accel, relative=False)
print("Moving")
cdpr.goto((-20, 12, 0), accel, relative=False)
print("Moving")
cdpr.goto((0, 4, 0), accel, relative=False)

print("Done")

cdpr.shutdown()
print("Shutdown")