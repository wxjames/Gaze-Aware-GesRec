import numpy as np
import os

def initialize():
    global camera_view_ori, camera_view, gaze, time_count, iter, results, name, gesture_name
    global T1, N, delta_T, first_timestamp, iter1, time, throw_frame, Inference_data, T0, temp1, temp2, aver, std, Tap_data
    global interaction, count_interaction, interaction_data, post_processing

    camera_view_ori = None
    camera_view = None
    gaze = None
    time_count = 0
    iter = 29
    results = None
    name = {0: 'Excavator', 1: 'Truck'}
    gesture_name = {0: {0: 'Load Up', 1: 'Load Down', 2: 'Swing Right', 3: 'Swing Left', 4: 'Stop', 5: 'Stop Engine',
                        6: 'Dipper In', 7: 'Dipper Out', 8: 'Open Bucket', 9: 'Close Bucket'},
                    1: {2: 'Move Right', 3: 'Move Left', 10: 'Pull Forward', 11: 'Proceed Backwards',
                        12: 'Raise the Truck Bed, Load, etc.', 13: 'Lower the Truck Bed, Load, etc.'}}

    T1 = 0
    N = 10
    time = 1
    delta_T = time / N
    first_timestamp = 0
    iter1 = 1
    throw_frame = 0
    T0 = 3
    temp1 = np.array([])
    temp2 = np.array([])
    aver = np.load(os.path.join('utils', 'aver.npy'))
    std = np.load(os.path.join('utils', 'std.npy'))
    Tap_data = np.array([])

    interaction = -1
    count_interaction = {'Truck': np.zeros(10), 'Excavator': np.zeros(10)}
    interaction_data = np.array([])
    post_processing = {0: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
                       1: [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]}
