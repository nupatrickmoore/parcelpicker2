#Quintic Math Model Script
#defines movement as 5th order funtion, creating smooth movement optimized
#for cycle time constrained by a maximum allowed acceleration
#See Matt Skopin for questions.
#to be used with Patrick Moore's simplfied Python Math model, modfied to take arguments,
#called local here as Movement function.

import numpy as np
# declare global vars
R = 0.5         # spool radius [inches]
L_plat = 5      # length of platform [inches]
W_plat = 3.75   # width of platform [inches]
Anchor_loc = np.array([[-23.5, 20, 8.75], [23.5, 20, 8.75],
                       [23.5, 20, -8.75], [-23.5, 20, -8.75]])  # anchor locations [inches]
#intitialize movment funtion
init_pos = np.array([0, 1, 0])      # initial position of platform
end_pos = np.array([10, 20, -7])       # end position of platform
cycle_time = 2                    # desired cycle time of movement
# input values (for testing)
accel_max = 5  # maximum accelration of cable link [inches/s^2]
path_start = np.array([[0,0,0]]) #starting position of trajectory [inches]
path_end = np.array([[1,1,1]])   #end position of trajectory [inches]
num_lin_interpol = 10   # number linear interpolations to be made from quintic trajacoties
                       # Each interpolation represents one set of steps/rpm insructions sent to drives
def movement(init_pos, end_pos, cycle_time):
    # Locations where cord meets platform [inches]
    cpm00 = init_pos[0][0] - L_plat / 2
    cpm02 = init_pos[0][2] + W_plat / 2
    cpm10 = init_pos[0][0] + L_plat / 2
    cpm12 = init_pos[0][2] + W_plat / 2
    cpm20 = init_pos[0][0] + L_plat / 2
    cpm22 = init_pos[0][2] - W_plat / 2
    cpm30 = init_pos[0][0] - L_plat / 2
    cpm32 = init_pos[0][2] - W_plat / 2
    cord_platform_mate = np.array([[cpm00, init_pos[0][1], cpm02],
                                   [cpm10, init_pos[0][1], cpm12],
                                   [cpm20, init_pos[0][1], cpm22],
                                   [cpm30, init_pos[0][1], cpm32]])
    delta_pos = np.subtract(end_pos, init_pos)                      # delta vector
    init_cord_len = np.subtract(cord_platform_mate, Anchor_loc)     # cord meets platform - anchor location
    end_cord_len = np.add(init_cord_len, delta_pos)                 # init_cord_len + delta_pos
    init_cord_len_scalar = np.array([[np.linalg.norm(init_cord_len[0])], [np.linalg.norm(init_cord_len[1])],
                            [np.linalg.norm(init_cord_len[2])], [np.linalg.norm(init_cord_len[3])]])
    end_cord_len_scalar = np.array([[np.linalg.norm(end_cord_len[0])], [np.linalg.norm(end_cord_len[1])],
                          [np.linalg.norm(end_cord_len[2])], [np.linalg.norm(end_cord_len[3])]])
    motor_speed = abs(((np.subtract(end_cord_len_scalar, init_cord_len_scalar)*60) / (cycle_time * 2 * 3.14 * R)))
    rel_pos_un = 2000*(np.subtract(end_cord_len_scalar, init_cord_len_scalar) / (2 * 3.14 * R))
    rel_pos_s = np.multiply(rel_pos_un, np.array([[1], [-1], [1], [-1]]))   # signed for different motor orientations
    rel_pos_int = np.round(rel_pos_s)
    motor_speed_int = np.round(motor_speed)
    print(rel_pos_int)
    print(motor_speed_int)
    return

def quintic(accel_max, path_start, path_end, num_lin_interpol):
    path_distance = np.linalg.norm(np.subtract(path_end, path_start)) #SCALAR length of vector connecting path_start to path_end
    path_cycle_time = np.sqrt((10 * path_distance) / (np.sqrt(3) * accel_max)) #optimized path cycle time based on max acceleration
    path_heading = np.subtract(path_end, path_start)
    def pos_eq(real_time): #position equation, which will be interpolated by Movement function
                           #real_time is the time at which each iterpolation occurs, elapsed from trajectory start
        quin_pos = path_start + path_heading * (10*((real_time/(path_cycle_time))**3))-(15*((real_time/(path_cycle_time))**4))+(6*((real_time/(path_cycle_time))**5))
        return quin_pos

    #define formula for start/end positions for each interpolation
    interpol_count = 0 #index value for coming For Loop, goes from 1 to lin_interpol_num
    for interpol_count in range(0, num_lin_interpol):
        interpol_start = pos_eq((interpol_count * path_cycle_time) / num_lin_interpol)
        interpol_end = pos_eq(((interpol_count + 1) * path_cycle_time) / num_lin_interpol)
        movement(interpol_start, interpol_end, path_cycle_time / num_lin_interpol)
    return
quintic(accel_max, path_start, path_end, num_lin_interpol)