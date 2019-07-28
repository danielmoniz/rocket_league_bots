import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from src.util.orientation import Orientation
from src.util.vec import Vec3
from src.util.debug import draw_debug
from src.strategy import drive_at_ball, shoot_with_power


class SuperBot(BaseAgent):
    def initialize_agent(self):
        # This runs once before the bot starts up
        self.controller_state = SimpleControllerState()
        self.packet = None
        self.game_info = {
            'field_info': self.get_field_info(),
        }
        self.goal_width = 1600 # is actually somewhat wider than this
        self.goal_height = 500 # actual height: 624


    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        # get/set game information (eg. ball location)
        self.set_game_info(packet)
        self.opposing_goal = self.game_info['field_info'].goals[1 - self.car.team]

        # determine heuristics
        mode = self.get_mode()

        # pick strategy
        # strategy = drive_at_ball.enact(self)
        strategy = shoot_with_power.enact(self)

        # convert strategy to quantities. Specifically, set:
        turn = get_turn(strategy['turn_angle'])
        throttle = strategy['throttle']
        target = strategy['target_location']

        # set controller state
            # throttle
            # steer
            # boost
            # ...(more to come)
        self.controller_state.throttle = throttle
        self.controller_state.steer = turn

        # output debug information
        action_display = f"{mode}: {get_debug(turn)}"
        draw_debug(self, self.renderer, self.game_info['car'], target, action_display)

        # return controller state
        return self.controller_state

    def get_mode(self):
        if self.game_info['car_location'].y > 0 and self.car.team == 1:
            return 'defend'
        if self.game_info['car_location'].y < 0 and self.car.team == 0:
            return 'defend'
        return 'attack'

    def set_game_info(self, packet):
        self.packet = packet
        self.car = packet.game_cars[self.index]

        self.game_info.update({
            'ball_location': Vec3(packet.game_ball.physics.location),
            'car': self.car,
            'car_location': Vec3(self.car.physics.location),
            'car_orientation': Orientation(self.car.physics.rotation),
        })


def get_turn(angle):
    # Positive radians in the unit circle is a turn to the left.
    if angle == 0:
        return 0
    return -1.0 if angle > 0 else 1.0


def get_debug(left_right):
    if left_right == 0:
        return "no turn"
    if left_right < 0: return "turn left"
    return "turn right"
