# CDPR 3D Motion Model python Vers.
# OUTPUT: Motor speeds and positions INPUT: origin coord (in), destination coord(in), and cycle time in seconds
# See Matt Skopin for details

import numpy as np              #allows for use of arrays.
from tabulate import tabulate   #allows for slick tables.
import ast                      #for evaluating user input as a list and not a string.

#intialize important vectors and factors
p1 = np.array([[0,2,0]]) #starting point, overwritten by input. in inches
p2 = np.array([[0,4,0]]) #destination point, overwritten by input. in inches
x = np.array([[0,0,0]])  #vector difference between p1 and p2, (p2-p1). in inches
tc = 1       #"cycle time", time inteval over which move will occur, overwritten by input. in seconds
r = .50      #Spool radius, doesn't change. in inches.
V = np.zeros((4, 1))#4 motor speeds, output by script. in rpm
b = np.array([[-23.5,20,8.75],[23.5,20,8.75],[23.5,20,-8.75],[-23.5,20,-8.75]]) #anchor locations, never change. in inches.
a = np.zeros((4, 3))#Locations where cord meets platorm, determined by following, in inches.
plat_L = 5   #platform Length, doesn't change. in inches
plat_W = 3.75#platofrm wideth, doesn't change. in inches
Li = np.zeros((4, 3))#initial cord vectors, b to a.
Lf = np.zeros((4, 3))#final cord vectors.
Li_abs = np.zeros((4, 1))
Lf_abs = np.zeros((4, 1))
count = -1
OUT1 = np.zeros((2, 7))
OUT2 = np.zeros((2, 7))
OUT3 = np.zeros((2, 7))
OUT4 = np.zeros((2, 7))
DSYN = np.zeros((14, 14))
V = np.zeros((4, 3))
I = np.zeros((4, 3))

#prompt for input
p1 = input("input initial position ")
p1 = np.array(ast.literal_eval(p1))
while True:
    p2 = input("input destination positions, or [[100,100,100]] to stop ")
    p2 = np.array(ast.literal_eval(p2))
    pTest = np.subtract(np.array([[100,100,100]]), p2)
    if pTest.all() == False:
        break
    tc = input("input desired cycle time ")
    tc = ast.literal_eval(tc)
    #begin calcs
    x = np.subtract(p2, p1)
    a[0][0] = (p1[0][0] - .5*plat_L)
    a[0][1] = (p1[0][1])
    a[0][2] = (p1[0][2] + .5*plat_W)
    a[1][0] = (p1[0][0] + .5*plat_L)
    a[1][1] = (p1[0][1])
    a[1][2] = (p1[0][2] + .5*plat_W)
    a[2][0] = (p1[0][0] + .5*plat_L)
    a[2][1] = (p1[0][1])
    a[2][2] = (p1[0][2] - .5*plat_W)
    a[3][0] = (p1[0][0] - .5*plat_L)
    a[3][1] = (p1[0][1])
    a[3][2] = (p1[0][2] - .5*plat_W)
    p1 = p2
    Li = np.subtract(a, b)
    Lf = np.add(Li, x)
    for N in range(0,4):
        Li_abs[N][0] = (Li[N][0]**2 + Li[N][1]**2 + Li[N][2]**2)**.5
        Lf_abs[N][0] = (Lf[N][0]**2 + Lf[N][1]**2 + Lf[N][2]**2)**.5
    V = abs(((np.subtract(Lf_abs, Li_abs)*60)/ (tc * 2 * 3.14 * r)))
    for N in range(0,4): #motors won't take floats, and a zero rpm will cause a lot of desync. Always rounds to 1.
        if V[N][0] < 1:
            V[N][0] = 1
    I = 2000*((np.subtract(Lf_abs, Li_abs)/ (2 * 3.14 * r)))
    I = np.multiply(I,np.array([[1],[-1],[1],[-1]]))  #accounting for different motor orientations.
    count = count + 1
    OUT1[0][count] = round(I[0][0]) #everything in column 0 is a relative position
    OUT1[1][count] = round(V[0][0]) #everything in column 1 is a velocity
    DSYN[count][0] = tc - 60*(abs((I[0][0]/2000))/ round(V[0][0])) #DSYN tracks desync in seconds, stored on a per motor, per motion basis.
    OUT2[0][count] = round(I[1][0])
    OUT2[1][count] = round(V[1][0])
    DSYN[count][1] = tc - 60*((abs(I[1][0]/2000))/ round(V[1][0]))
    OUT3[0][count] = round(I[2][0])
    OUT3[1][count] = round(V[2][0])
    DSYN[count][2] = tc - 60*(abs((I[2][0]/2000))/ round(V[2][0]))
    OUT4[0][count] = round(I[3][0])
    OUT4[1][count] = round(V[3][0])
    DSYN[count][3] = tc - 60*(abs((I[3][0]/2000))/ round(V[3][0]))
#remove excess zeroes from arrays
OUT1 = OUT1[OUT1 != 0]
OUT2 = OUT2[OUT2 != 0]
OUT3 = OUT3[OUT3 != 0]
OUT4 = OUT4[OUT4 != 0]
#print tables with speeds and postions
table = [OUT1,OUT2,OUT3,OUT4]
print(tabulate(table))