from core import CDPR #relative import of core
import time
import logging

#logging.basicConfig(level=logging.DEBUG)

print("Initialising")
cdpr = CDPR()
#quick test accel var
accel = 30
accel2 = 30

cdpr.release_ser()
print("Moving")
cdpr.goto((-10, 12, 0), accel, relative=False)
print("Moving")
cdpr.goto((-10, 4, 0), accel, relative=False)
print("Grabbing")
cdpr.grab_ser()
print("Moving")
cdpr.goto((-10, 12, 0), accel, relative=False)
print("Moving")
cdpr.goto((13, 12, -5), accel, relative=False)
print("Moving")
cdpr.goto((13, 5, -5), accel, relative=False)
print("Releasing")
cdpr.release_ser()
print("Moving")
cdpr.goto((13, 12, -5), accel, relative=False)
print("Moving")
cdpr.goto((5, 12, 5), accel, relative=False)
print("Moving")
cdpr.goto((5, 5, 5), accel, relative=False)
print("Grabbing")
cdpr.grab_ser()
print("Moving")
cdpr.goto((5, 12, 5), accel, relative=False)
print("Moving")
cdpr.goto((-10, 12, 0), accel, relative=False)
print("Moving")
cdpr.goto((-10, 4, 0), accel, relative=False)
print("Releasing")
cdpr.release_ser()
print("Moving")
cdpr.goto((-10, 12, 0), accel, relative=False)
print("Moving")
cdpr.goto((0, 4, 0), accel, relative=False)
print("Done")
cdpr.grab_ser()


cdpr.shutdown()
print("Shutdown")