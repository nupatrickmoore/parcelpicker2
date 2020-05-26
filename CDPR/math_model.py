import numpy as np

spool_radius = 0.5
plat_l = 0 #5
plat_w = 0 #3.75
anchor_pos = np.array([[-23.5, 20, 8.75], [23.5, 20, 8.75],
                    [23.5, 20, -8.75], [-23.5, 20, -8.75]])

def oneshot_movement(init_pos, end_pos, cycle_time):
    '''
    Returns relative motor positions and velocities for a basic linear cdpr movement
    '''

    #convert positions to arrays, may not be needed but wanted to be safe -Ian
    init_pos = np.asarray(init_pos)
    end_pos = np.asarray(end_pos)
    
    # Locations where cord meets platform [inches]
    cpm00 = init_pos[0] - plat_l / 2
    cpm02 = init_pos[2] + plat_w / 2
    cpm10 = init_pos[0] + plat_l / 2
    cpm12 = init_pos[2] + plat_w / 2
    cpm20 = init_pos[0] + plat_l / 2
    cpm22 = init_pos[2] - plat_w / 2
    cpm30 = init_pos[0] - plat_l / 2
    cpm32 = init_pos[2] - plat_w / 2
    cord_platform_mate = np.array([[cpm00, init_pos[1], cpm02],
                                   [cpm10, init_pos[1], cpm12],
                                   [cpm20, init_pos[1], cpm22],
                                   [cpm30, init_pos[1], cpm32]])

    delta_pos = np.subtract(end_pos, init_pos)                      # delta vector
    init_cord_len = np.subtract(cord_platform_mate, anchor_pos)     # cord meets platform - anchor location
    end_cord_len = np.add(init_cord_len, delta_pos)                 # init_cord_len + delta_pos
    # take magnitude of initial cord lengths
    init_cord_len_scalar = np.array([[np.linalg.norm(init_cord_len[0])], [np.linalg.norm(init_cord_len[1])],
                            [np.linalg.norm(init_cord_len[2])], [np.linalg.norm(init_cord_len[3])]])
    # take magnitude of end cord lengths
    end_cord_len_scalar = np.array([[np.linalg.norm(end_cord_len[0])], [np.linalg.norm(end_cord_len[1])],
                          [np.linalg.norm(end_cord_len[2])], [np.linalg.norm(end_cord_len[3])]])
    # calculate motor speed
    motor_speed = abs(((np.subtract(end_cord_len_scalar, init_cord_len_scalar)*60) / (cycle_time * 2 * 3.14 * spool_radius)))
    # calculate relative position
    rel_pos_un = 2000*(np.subtract(end_cord_len_scalar, init_cord_len_scalar) / (2 * 3.14 * spool_radius))
    rel_pos_s = np.multiply(rel_pos_un, np.array([[1], [-1], [1], [-1]]))   # signed for different motor orientations
    # round outputs
    rel_pos_int = np.round(rel_pos_s)
    motor_speed_int = np.round(motor_speed)

    return (rel_pos_int, motor_speed_int)

def BB_movement(init_pos, end_pos, accel_max):
    '''
    Returns relative motor positions, velocities  and accelerations for a smoother cdpr movement
    '''

    #convert positions to arrays, may not be needed but wanted to be safe -Ian
    init_pos = np.asarray(init_pos)
    end_pos = np.asarray(end_pos)

    # Locations where cord meets platform [inches]
    cpm00 = init_pos[0] - plat_l / 2
    cpm02 = init_pos[2] + plat_w / 2
    cpm10 = init_pos[0] + plat_l / 2
    cpm12 = init_pos[2] + plat_w / 2
    cpm20 = init_pos[0] + plat_l / 2
    cpm22 = init_pos[2] - plat_w / 2
    cpm30 = init_pos[0] - plat_l / 2
    cpm32 = init_pos[2] - plat_w / 2
    cord_platform_mate = np.array([[cpm00, init_pos[1], cpm02],
                                   [cpm10, init_pos[1], cpm12],
                                   [cpm20, init_pos[1], cpm22],
                                   [cpm30, init_pos[1], cpm32]])
    delta_pos = np.subtract(end_pos, init_pos)                      # delta vector
    init_cord_len = np.subtract(cord_platform_mate, anchor_pos)     # cord meets platform - anchor location
    end_cord_len = np.add(init_cord_len, delta_pos)                 # init_cord_len + delta_pos
    init_cord_len_scalar = np.array([[np.linalg.norm(init_cord_len[0])], [np.linalg.norm(init_cord_len[1])],
                            [np.linalg.norm(init_cord_len[2])], [np.linalg.norm(init_cord_len[3])]])
    end_cord_len_scalar = np.array([[np.linalg.norm(end_cord_len[0])], [np.linalg.norm(end_cord_len[1])],
                            [np.linalg.norm(end_cord_len[2])], [np.linalg.norm(end_cord_len[3])]])
    #optimization step: test cycle time at accel_max for each cord, largest becomes global cycle time
    cycle_time_comp = np.sqrt(abs(np.subtract(end_cord_len_scalar, init_cord_len_scalar)) * 60 * (4/ (2 * 3.14 * spool_radius * accel_max)))
    cycle_time = np.amax(cycle_time_comp)
    #Generate target positions(steps), angular velocities (rpm), and angular accelerations (rpm/s)
    motor_speed = 2 * abs(((np.subtract(end_cord_len_scalar, init_cord_len_scalar)*60) / (cycle_time * 2 * 3.14 * spool_radius))) #the constant 2 is added here to offset lost time due to BB
    rel_pos_un = 2000*.5*(np.subtract(end_cord_len_scalar, init_cord_len_scalar) / (2 * 3.14 * spool_radius)) #the constant .5 is added here so two pro-pos CAN messesges make one full move
    rel_pos_s = np.multiply(rel_pos_un, np.array([[1], [-1], [1], [-1]]))   # signed for different motor orientations
    rel_pos_int = np.round(rel_pos_s)
    motor_speed_int = np.round(motor_speed)
    motor_accel = np.subtract(end_cord_len_scalar, init_cord_len_scalar)* 60 * (4/ (2 * 3.14 * spool_radius * cycle_time**2))
    motor_deccel = -1 * motor_accel
    #from here, each print represents values sent to the appropriate register on the drives over CAN
    return (rel_pos_int, motor_speed_int, motor_accel, motor_deccel, cycle_time)



if __name__ == '__main__':#will only run if the file is specificall ran, not imported
    #rel_pos_int, motor_speed_int = oneshot_movement((1, 1, 1), (2, 2, 2), 1.5)
    #print(rel_pos_int, motor_speed_int)
    rel_pos_int, motor_speed_int, motor_accel, motor_deccel, cycle_time = BB_movement((-19.6, 4, 0), (19.6, 4, 0), 30)
    print(rel_pos_int, motor_speed_int, motor_accel, motor_deccel, cycle_time)

    

