import numpy as np

# declare global vars
R = 0.5         # spool radius [inches]
L_plat = 5      # length of platform [inches]
W_plat = 3.75   # width of platform [inches]
Anchor_loc = np.array([[-23.5, 20, 8.75], [23.5, 20, 8.75],
                       [23.5, 20, -8.75], [-23.5, 20, -8.75]])  # anchor locations [inches]

def movement():
    # local variables
    init_pos = np.array([1, 1, 1])      # initial position of platform
    end_pos = np.array([2, 2, 2])       # end position of platform
    cycle_time = 1.5                    # desired cycle time of movement
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
    # take magnitude of initial cord lengths
    init_cord_len_scalar = np.array([[np.linalg.norm(init_cord_len[0])], [np.linalg.norm(init_cord_len[1])],
                            [np.linalg.norm(init_cord_len[2])], [np.linalg.norm(init_cord_len[3])]])
    # take magnitude of end cord lengths
    end_cord_len_scalar = np.array([[np.linalg.norm(end_cord_len[0])], [np.linalg.norm(end_cord_len[1])],
                          [np.linalg.norm(end_cord_len[2])], [np.linalg.norm(end_cord_len[3])]])
    # calculate motor speed
    motor_speed = abs(((np.subtract(end_cord_len_scalar, init_cord_len_scalar)*60) / (cycle_time * 2 * 3.14 * R)))
    # calculate relative position
    rel_pos_un = 2000*(np.subtract(end_cord_len_scalar, init_cord_len_scalar) / (2 * 3.14 * R))
    rel_pos_s = np.multiply(rel_pos_un, np.array([[1], [-1], [1], [-1]]))   # signed for different motor orientations
    # round outputs
    rel_pos_int = np.round(rel_pos_s)
    motor_speed_int = np.round(motor_speed)
movement()
