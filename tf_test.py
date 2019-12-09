import numpy as np
import tensorflow as tf

# model = tf.keras.models.load_model('frankenbot/model.h5')
def load_model():
    return tf.keras.models.load_model('frankenbot/saved_model')

model = load_model()

player_data = {
    'pos_x': 0.322,
    'pos_y': 0.313,
    'pos_z': 0.0084,
}

input_data = np.array([
    player_data['pos_x'],
    player_data['pos_y'],
    player_data['pos_z'],
    0.70,  # @TODO boost quantity
    3000, # self.game_info.ball_location.x,
    -4500, # self.game_info.ball_location.y,
    500, # self.game_info.ball_location.z,
    100,  # @TODO velocity x
    100,  # @TODO velocity y
    5,  # @TODO velocity z
    1.0,  # @TODO map
    1.0,  # @TODO team - top priority!
])
input_data = np.float64(input_data)
print(input_data.shape[0])
print(input_data)
# model_input = np.ndarray((1, 3), buffer=np.array(np.int64([1, 2, 3])))
model_input = np.ndarray((1, input_data.shape[0]), buffer=input_data)
print(model_input.shape)

def predict(model, model_input):
    return model.predict(model_input, batch_size=1).flatten()

output = predict(model, model_input)
print(output)

time = timeit.timeit()