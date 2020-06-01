from core import CDPR #relative import of core
import time
import logging

#logging.basicConfig(level=logging.DEBUG)

print("Initialising")
cdpr = CDPR()

print("Moving")
cdpr.goto((5, 5, 3), 30)
print("Done")

cdpr.shutdown()
print("Shutdown")