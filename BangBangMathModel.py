#BangBang Math Model Script
#Script splits linear trajectory into an acceleration step and deccel step
#with optimized cycle time based on user defined max accel/deccel
#See Matt Skopin for questions

import numpy as np
#delcare global vars
# declare global vars
R = 0.5         # spool radius [inches]
L_plat = 5      # length of platform [inches]
W_plat = 3.75   # width of platform [inches]
Anchor_loc = np.array([[-23.5, 20, 8.75], [23.5, 20, 8.75],
                       [23.5, 20, -8.75], [-23.5, 20, -8.75]])  # anchor locations [inches]
#User input values (for testing)
init_pos = np.array([-19.6, 4, 0])      # initial position of platform
end_pos = np.array([19.6, 4, 0])    # end position of platform
accel_max = 30                     # maximum accelration of cable link [rpm/s]
def BB_movement():
    # Locations where cord meets platform [inches]
    cpm00 = init_pos[0] - L_plat / 2
    cpm02 = init_pos[2] + W_plat / 2
    cpm10 = init_pos[0] + L_plat / 2
    cpm12 = init_pos[2] + W_plat / 2
    cpm20 = init_pos[0] + L_plat / 2
    cpm22 = init_pos[2] - W_plat / 2
    cpm30 = init_pos[0] - L_plat / 2
    cpm32 = init_pos[2] - W_plat / 2
    cord_platform_mate = np.array([[cpm00, init_pos[1], cpm02],
                                   [cpm10, init_pos[1], cpm12],
                                   [cpm20, init_pos[1], cpm22],
                                   [cpm30, init_pos[1], cpm32]])
    delta_pos = np.subtract(end_pos, init_pos)                      # delta vector
    init_cord_len = np.subtract(cord_platform_mate, Anchor_loc)     # cord meets platform - anchor location
    end_cord_len = np.add(init_cord_len, delta_pos)                 # init_cord_len + delta_pos
    init_cord_len_scalar = np.array([[np.linalg.norm(init_cord_len[0])], [np.linalg.norm(init_cord_len[1])],
                            [np.linalg.norm(init_cord_len[2])], [np.linalg.norm(init_cord_len[3])]])
    end_cord_len_scalar = np.array([[np.linalg.norm(end_cord_len[0])], [np.linalg.norm(end_cord_len[1])],
                            [np.linalg.norm(end_cord_len[2])], [np.linalg.norm(end_cord_len[3])]])
    #optimization step: test cycle time at accel_max for each cord, largest becomes global cycle time
    cycle_time_comp = np.sqrt(abs(np.subtract(end_cord_len_scalar, init_cord_len_scalar)) * 60 * (4/ (2 * 3.14 * R * accel_max)))
    cycle_time = np.amax(cycle_time_comp)
    #Generate target positions(steps), angular velocities (rpm), and anuglar accelerations (rpm/s)
    motor_speed = 2 * abs(((np.subtract(end_cord_len_scalar, init_cord_len_scalar)*60) / (cycle_time * 2 * 3.14 * R))) #the constant 2 is added here to offset lost time due to BB
    rel_pos_un = 2000*.5*(np.subtract(end_cord_len_scalar, init_cord_len_scalar) / (2 * 3.14 * R)) #the constant .5 is added here so two pro-pos CAN messesges make one full move
    rel_pos_s = np.multiply(rel_pos_un, np.array([[1], [-1], [1], [-1]]))   # signed for different motor orientations
    rel_pos_int = np.round(rel_pos_s)
    motor_speed_int = np.round(motor_speed)
    motor_accel = np.subtract(end_cord_len_scalar, init_cord_len_scalar)* 60 * (4/ (2 * 3.14 * R * cycle_time**2))
    motor_deccel = -1 * motor_accel
    #from here, each print represents values sent to the appropriate register on the drives over CAN
    #CAN messege 1, for accel leg of trajectory
    print(rel_pos_int)
    print(motor_speed_int)
    print(motor_accel)
    #CAN messege 2, for deccel leg of trajectory, into destination buffer
    print(rel_pos_int)
    print(motor_speed_int)
    print(motor_deccel)
    print(cycle_time)
BB_movement()