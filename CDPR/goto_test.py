from core import CDPR #relative import of core
import time
import logging

logging.basicConfig(level=logging.INFO)

cdpr = CDPR()

print("Moving...")
cdpr.goto((3,3,3), 30)
time.sleep(10)
cdpr.goto((-3,-3,-3), 30)
print("Done!")

#cdpr.shutdown() #should do automatically with end of program