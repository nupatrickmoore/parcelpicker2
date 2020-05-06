import core #relative import of core
import time

cdpr = core.CDPR()

cdpr.goto((0,0,0), 10)
time.sleep(5)
cdpr.goto((0,10,0), 10)
time.sleep(5)

cdpr.shutdown()