import pickle
import keras
import numpy as np
import os

model_gesture = keras.models.load_model(os.path.join('models', 'resnet_attention.hdf5'))
post_processing = {0: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1], 1: [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]}

window_size = 3
output = []

for j in range(1, 33):
    dir = str(j)
    Tap_name = os.path.join('framework_validation_data', 'test' + dir + '-Tap')
    interaction_name = os.path.join('framework_validation_data', 'test' + dir + '-interaction')
    with open(Tap_name, "rb") as fp:
        Tap_data = pickle.load(fp)
    with open(interaction_name, "rb") as fp:   # Unpickling
        interaction = pickle.load(fp)

    # Resizing the Tap data
    Tap_data = np.resize(Tap_data, (-1,21))

    result = []
    for i in range(len(Tap_data)-window_size*10):
        if i % 10 == 0 and interaction[i] >= 0:
            basic_unit = Tap_data[i:i + 10 * window_size]
            transformed_basic_unit = basic_unit.tolist()
            y_pred = model_gesture.predict([transformed_basic_unit])
            y_pred[0] = np.multiply(y_pred[0], post_processing[interaction[i]])
            maxindex = np.argmax(y_pred, axis=1)
            if y_pred[0][maxindex[0]] > 0.7 and maxindex[0] != 14:
                if len(result) == 0 or interaction[i] != result[-1][0] or maxindex[0] != result[-1][1]:
                    result.append([interaction[i], maxindex[0]])
    output.append(result)

output_dir = os.path.join('results', 'result_resnet_attention')
with open(output_dir, "wb") as fp:  # Pickling
    pickle.dump(output, fp)