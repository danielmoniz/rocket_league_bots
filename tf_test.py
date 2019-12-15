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
    print("Input:")
    print(input_map)
    print("Output (throttle, steer, boost_active):")
    print(output)
    print('-' * 10)


model = load_model()


def compute(input_map):
    model_input = get_model_input(input_map)
    output = predict(model, model_input)
    print_test(input_map, output)
    return output


def get_default_input_map(specifics):
    default_map = {
        'pos_x': 0.5,
        'pos_y': 0.5,
        'pos_z': 0.01,
        'boost_quantity': 1,
        'ball_pos_x': 0.5,
        'ball_pos_y': 0.5,
        'ball_pos_z': 0.01,
        'vel_x': 0,
        'vel_y': 0,
        'vel_z': 0,
        'map': 1,
        'team': 1,
    }
    return {**default_map, **specifics}


def test_attack_ball():
    input_map = get_default_input_map({
        'pos_y': 0.1,
    })
    print("We expect: throttle high, steering neutral, boost active")
    throttle, steering, boost = compute(input_map)
    assert throttle >= 0.9
    assert 0.45 <= steering <= 0.55
    assert boost > 0.1


def test_turn_right_for_ball():
    input_map = get_default_input_map({
        'pos_x': 0.1,
        'pos_y': 0.1,
        'vel_y': 0.3,
    })
    print("We expect: throttle medium, steering right, boost optional")
    throttle, steering, boost = compute(input_map)
    assert throttle >= 0.4
    assert steering >= 0.7

# time = timeit.timeit()
