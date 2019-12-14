import math

import numpy as np
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket


from src.util.orientation import Orientation
from src.util.vec import Vec3
from src.util.debug import draw_debug
from src.util.angle import find_correction
from src import pathing
from src.util import angle


class FrankenBot(BaseAgent):
    def initialize_agent(self):
        # This runs once before the bot starts up
        self.controller_state = SimpleControllerState()
        self.packet = None
        self.game_info = {
            'field_info': self.get_field_info(),
        }
        # Values are from: https://github.com/RLBot/RLBot/wiki/Useful-Game-Values
        self.goal_width = 892.755 * 2
        self.goal_height = 642.775  # actual height: 624
        self.field = {
            'width': 4096 * 2,
            'length': 5120 * 2,
            'height': 2044,
        }
        self.max_speed = 2300

        import tensorflow as tf
        tf.get_logger().setLevel('ERROR')
        self.predictor = tf.keras.models.load_model('frankenbot/saved_model')

    def normalize_x(self, old_x):
        return (old_x + self.field['width'] / 2) / self.field['width']

    def normalize_y(self, old_y):
        return (old_y + self.field['length'] / 2) / self.field['length']

    def normalize_z(self, old_z):
        return (old_z) / self.field['height']

    def normalize_velocity(self, old_value):
        return old_value / (self.max_speed * 2) + 0.5

    def normalize_steering(self, value):
        return value * 2 - 1

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        # get/set game information (eg. ball location)
        self.set_game_info(packet)

        # set controller state using planned actions of bot
        # throttle
        # steer
        # boost
        # handbrake
        # ...(more to come)

        # get full dictionary of game state data (player, teammates, opponents, ball)
        # part 1: get player game state
        # rot_x	rot_y	rot_z	vel_x	vel_y	vel_z	ang_vel_x	ang_vel_y	ang_vel_z	active	boost
        player_data = {
            'pos_x': self.normalize_x(self.game_info['car_location'].x),
            'pos_y': self.normalize_y(self.game_info['car_location'].y),
            'pos_z': self.normalize_z(self.game_info['car_location'].z),
            'vel_x': self.normalize_velocity(self.car.physics.velocity.x),
            'vel_y': self.normalize_velocity(self.car.physics.velocity.y),
            'vel_z': self.normalize_velocity(self.car.physics.velocity.z),
        }

        ball_data = {
            'pos_x': self.normalize_x(self.game_info['ball_location'].x),
            'pos_y': self.normalize_y(self.game_info['ball_location'].y),
            'pos_z': self.normalize_z(self.game_info['ball_location'].z),
        }

        orient = self.game_info['car_orientation']
        # print(orient.forward, orient.right, orient.up)
        # print(orient.yaw, orient.pitch, orient.roll)
        # NOTE: Negative y is toward Blue's goal!
        # normalize all data
        # run through model
        # turn outputs into dictionary

        input_data = np.array([
            player_data['pos_x'],
            player_data['pos_y'],
            player_data['pos_z'],
            0,  # @TODO boost quantity
            ball_data['pos_x'],
            ball_data['pos_y'],
            ball_data['pos_z'],
            player_data['vel_x'],
            player_data['vel_y'],
            player_data['vel_z'],
            1,  # @TODO map
            1,  # @TODO team - top priority!
        ])
        model_input = np.ndarray((1, input_data.shape[0]), buffer=input_data)
        print(model_input)
        output = self.predictor.predict(model_input)
        output = output.flatten()
        controls = {
            'throttle': output[0],
            'steer': self.normalize_steering(output[1]),
            'boost': output[2] > 0.5,
        }

        # set controls to match output dictionary
        self.controller_state.throttle = controls['throttle']
        self.controller_state.steer = controls['steer']
        # self.controller_state.handbrake = controls['handbrake']
        self.controller_state.boost = controls['boost']

        # output debug information
        # action_display = f"{mode}: {get_turn_debug_text(controls['steer'])}{strategy_debug}"
        # draw_debug(
        #     self,
        #     self.renderer,
        #     self.game_info['car'],
        #     action_display,
        #     planned_curve=planned_curve,
        # )

        # return controller state
        return self.controller_state

    def set_game_info(self, packet):
        self.packet = packet
        self.car = packet.game_cars[self.index]
        self.opposing_goal = self.game_info['field_info'].goals[1 - self.car.team]
        car_orientation = Orientation(self.car.physics.rotation)
        ball_location = Vec3(packet.game_ball.physics.location)
        car_location = Vec3(self.car.physics.location)

        self.game_info.update({
            'car': self.car,
            'car_location': car_location,
            'car_orientation': car_orientation,
            'car_direction': car_orientation.forward,
            'ball_location': ball_location,
            'ball_to_goal': (Vec3(self.opposing_goal.location) - ball_location).normalized(),
            'distance_from_ball': (car_location - ball_location).length(),
        })


def get_turn(angle):
    # Positive radians in the unit circle is a turn to the left.
    turn = 1.0 if angle < 0 else -1.0
    if abs(angle) < math.pi / 24:
        return turn / math.pi
    return turn


def get_turn_debug_text(left_right):
    if left_right == 0:
        return "no turn"
    if left_right < 0:
        return "turn left"
    return "turn right"
