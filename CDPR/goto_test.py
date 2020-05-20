from core import CDPR #relative import of core
import time

cdpr = CDPR()

cdpr.goto((1,2,3), 12)
time.sleep(10)
cdpr.goto((2,2,2), 10)
cdpr.goto((1,1,1), 10)

cdpr.shutdown()