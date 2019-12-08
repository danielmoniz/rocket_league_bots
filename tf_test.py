import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model('frankenbot/model.h5')

player_data = {
    'pos_x': 300,
    'pos_y': -2000,
    'pos_z': 200,
}

input_data = np.array([
    player_data['pos_x'],
    player_data['pos_y'],
    player_data['pos_z'],
    0,  # @TODO boost quantity
    3000, # self.game_info.ball_location.x,
    -4500, # self.game_info.ball_location.y,
    500, # self.game_info.ball_location.z,
    100,  # @TODO velocity x
    100,  # @TODO velocity y
    5,  # @TODO velocity z
    1,  # @TODO map
    1,  # @TODO team - top priority!
])
input_data = np.int64(input_data)
print(input_data.shape[0])
# model_input = np.ndarray((1, 3), buffer=np.array(np.int64([1, 2, 3])))
model_input = np.ndarray((1, input_data.shape[0]), buffer=input_data)
print(model_input.shape)
output = model.predict(model_input, batch_size=1).flatten()
print(output)