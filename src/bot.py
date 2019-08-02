import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from src.util.orientation import Orientation
from src.util.vec import Vec3
from src.util.debug import draw_debug
from src.util.angle import find_correction
from src.strategy import drive_at_ball, shoot_with_power
from src import pathing
from src.pathing import get_vector_on_curve


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

        # determine heuristics
        mode = self.get_mode()

        # pick strategy
        # strategy = drive_at_ball.enact(self)
        strategy = shoot_with_power.enact(self)

        # convert strategy to quantities. Specifically, set:
        turn = get_turn(strategy['turn_angle'])
        planned_curve = strategy['planned_curve']

        # set controller state using planned actions of bot
            # throttle
            # steer
            # boost
            # ...(more to come)

        controls = self.convert_curve_to_controls(planned_curve)

        self.controller_state.throttle = controls['throttle']
        self.controller_state.steer = controls['steer']
        self.controller_state.handbrake = controls['handbrake']
        self.controller_state.boost = controls['boost']

        # output debug information
        action_display = f"{mode}: {get_debug(turn)}"
        draw_debug(
            self,
            self.renderer,
            self.game_info['car'],
            action_display,
            planned_curve=planned_curve,
        )

        # return controller state
        return self.controller_state

    def convert_curve_to_controls(self, curve):
        ## needed info:
        # current car location (loc0)
        car_location = self.game_info['car_location']
        # current car direction (dir0)
        car_direction = self.game_info['car_direction']
        # intended vector shortly into the planned curve (loc1)
        next_vector = get_vector_on_curve(0.4, curve)
        # intended direction at same location (dir1)
        delta_vector = get_vector_on_curve(0.41, curve)
        # print(next_vector, delta_vector, delta_vector - next_vector)
        next_direction = (delta_vector - next_vector).normalized()
        # distance between loc0 and loc1 (dist)
        distance = (next_vector - car_location).length()
        # angle between dir0 and dir1 (angle)
        angle = find_correction(car_direction, next_direction)

        ## logic:
            # if dist < some_amount and angle >= 90 deg:
                # activate handbrake
                # do NOT activate boost
            # if dist < some_amount and angle < 90 deg:
                # activate boost (if allowed/possible)
            # if dist < some_amount and facing > 45 deg:
                # slow down for turn
        throttle = 1.0
        angle_threshold = math.pi / 8
        if distance < 5000 and abs(angle) >= angle_threshold:
            print("Major turn! Use handbrake!")
            return {
                'steer': get_turn(angle),
                'throttle': throttle,
                'boost': self.filter_boost(False),
                'handbrake': True,
            }
        if abs(angle) < angle_threshold:
            return {
                'steer': get_turn(angle),
                'throttle': throttle,
                'boost': self.filter_boost(True),
                'handbrake': False,
            }

        return {
            'steer': get_turn(angle),
            'throttle': throttle,
            'boost': self.filter_boost(False),
            'handbrake': False,
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
        self.opposing_goal = self.game_info['field_info'].goals[1 - self.car.team]
        car_orientation = Orientation(self.car.physics.rotation)
        ball_location = Vec3(packet.game_ball.physics.location)

        self.game_info.update({
            'ball_location': ball_location,
            'car': self.car,
            'car_location': Vec3(self.car.physics.location),
            'car_orientation': car_orientation,
            'car_direction': car_orientation.forward,
            'ball_to_goal': (Vec3(self.opposing_goal.location) - ball_location).normalized()
        })

    def filter_boost(self, boost):
        # For now, never boost
        return False


def get_turn(angle):
    # Positive radians in the unit circle is a turn to the left.
    turn = 1.0 if angle < 0 else -1.0
    if abs(angle) < math.pi / 24:
        return turn / math.pi
    return turn


def get_debug(left_right):
    if left_right == 0:
        return "no turn"
    if left_right < 0: return "turn left"
    return "turn right"
