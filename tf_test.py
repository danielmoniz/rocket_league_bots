import timeit

import numpy as np
import tensorflow as tf


def load_model():
    return tf.keras.models.load_model('frankenbot/saved_model')


def get_model_input(input_map):
    data = np.array(list(input_map.values()))
    input_data = np.float64(data)
    return np.ndarray((1, input_data.shape[0]), buffer=input_data)


def predict(model, model_input):
    return model.predict(model_input, batch_size=1).flatten()


def print_test(input_map, output):
    print("Input/output:")
    print(input_map)
    print(output)
    print('-' * 10)


model = load_model()


def compute(input_map):
    model_input = get_model_input(input_map)
    output = predict(model, model_input)
    print_test(input_map, output)


input_map = {
    'pos_x': 0.1,
    'pos_y': 0.5,
    'pos_z': 0.1,
    'boost_quantity': 0,
    'ball_pos_x': 0.5,
    'ball_pos_y': 0.5,
    'ball_pos_z': 0.01,
    'vel_x': 0,
    'vel_y': 0,
    'vel_z': 0,
    'map': 1,
    'team': 1,
}
compute(input_map)

# time = timeit.timeit()
