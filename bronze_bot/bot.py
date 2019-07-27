import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.orientation import Orientation
from util.vec import Vec3
from util.debug import draw_debug


class PythonExample(BaseAgent):

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.controller_state = SimpleControllerState()
        self.game_info = {}

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        # get/process game information (eg. ball location)
        self.set_game_info(packet)

        # determine heuristics
        mode = self.get_mode()

        # pick strategy
        strategy = self.drive_at_ball()

        # convert strategy to quantities. Specifically, set:
            # throttle
            # steer
            # ...(more to come)
        turn = get_turn(strategy['turn_angle'])
        throttle = strategy['throttle']

        # set controller state
            # throttle
            # steer
        self.controller_state.throttle = throttle
        self.controller_state.steer = turn

        # output debug information
        action_display = get_debug(turn)
        draw_debug(self.renderer, self.game_info['car'], packet.game_ball, action_display)

        # return controller state
        return self.controller_state

    def drive_at_ball(self):
        # Find the direction of our car using the Orientation class
        car_to_ball = self.game_info['ball_location'] - self.game_info['car_location']
        car_direction = self.game_info['car_orientation'].forward
        steer_correction_radians = find_correction(car_direction, car_to_ball)
        return {
            'turn_angle': steer_correction_radians,
            'throttle': 1.0,
        }

    def get_mode(self):
        return 'attack'

    def set_game_info(self, packet):
        ball_location = Vec3(packet.game_ball.physics.location)
        my_car = packet.game_cars[self.index]
        car_location = Vec3(my_car.physics.location)
        car_orientation = Orientation(my_car.physics.rotation)

        self.game_info = {
            'ball_location': ball_location,
            'car': my_car,
            'car_location': car_location,
            'car_orientation': car_orientation,
        }


def get_turn(angle):
    # Positive radians in the unit circle is a turn to the left.
    if angle == 0:
        return 0
    return -1.0 if angle > 0 else 1.0


def get_debug(left_right):
    if left_right == 0:
        return "no turn"
    return "turn_left" if left_right > 0 else "turn right"


def find_correction(current: Vec3, ideal: Vec3) -> float:
    # Finds the angle from current to ideal vector in the xy-plane. Angle will be between -pi and +pi.

    # The in-game axes are left handed, so use -x
    current_in_radians = math.atan2(current.y, -current.x)
    ideal_in_radians = math.atan2(ideal.y, -ideal.x)

    diff = ideal_in_radians - current_in_radians

    # Make sure that diff is between -pi and +pi.
    if abs(diff) > math.pi:
        if diff < 0:
            diff += 2 * math.pi
        else:
            diff -= 2 * math.pi

    return diff
