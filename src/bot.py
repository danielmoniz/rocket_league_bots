import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.orientation import Orientation
from util.vec import Vec3
from util.debug import draw_debug


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
        strategy = self.drive_at_ball()

        # convert strategy to quantities. Specifically, set:
            # throttle
            # steer
            # boost
            # ...(more to come)
        turn = get_turn(strategy['turn_angle'])
        throttle = strategy['throttle']
        target = strategy['target_location']

        # set controller state
            # throttle
            # steer
            # boost
        self.controller_state.throttle = throttle
        self.controller_state.steer = turn

        # output debug information
        action_display = f"{mode}: {get_debug(turn)}"
        draw_debug(self, self.renderer, self.game_info['car'], target, action_display)

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
            'target_location': self.game_info['ball_location'],
        }

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
