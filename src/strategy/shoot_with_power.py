import math

from src import pathing
from src.util.vec import Vec3
from src.util import angle

def enact(player):
    distance_from_ball = player.game_info['distance_from_ball']

    very_short_range = 400
    short_range = 1000

    car_direction = player.game_info['car_orientation'].forward
    ball_to_goal = player.game_info['ball_to_goal']

    curve = pathing.compute_shooting_curve(
        player.game_info['car_location'],
        car_direction,
        player.game_info['ball_location'],
        ball_to_goal,
    )

    car_to_ball = (player.game_info['ball_location'] - player.game_info['car_location'])
    position_angle_threshold = math.radians(20)
    facing_angle_threshold = math.radians(20)

    at_short_range = distance_from_ball < short_range
    if at_short_range: print("At very short range.")

    # print(f"Car to ball: {car_to_ball.normalized()}")
    # print(f"Ball to goal: {ball_to_goal.normalized()}")
    # print(angle.find_correction(car_to_ball, ball_to_goal))
    in_line_position = abs(angle.find_correction(car_to_ball, ball_to_goal)) < position_angle_threshold
    if in_line_position: print("In line position.")

    # print(angle.find_correction(car_direction, car_to_ball))
    in_line_direction = abs(angle.find_correction(car_direction, car_to_ball)) < facing_angle_threshold
    if in_line_direction: print("In line direction.")

    debug = ''
    if at_short_range and in_line_position and in_line_direction:
        print("Attack! (charge the ball)")
        debug = "Charge!"

    # if distance_from_ball < very_short_range:# and in a decent line
    #     # @TODO Dodge into a specific part of the ball
    #     print('Very short range')
    # elif distance_from_ball < short_range:
    #     print('Short range.')
    # else: # define maximum scale for the shooting curve
    #     print('Medium or greater range.')

    # calculate curve required to strike the ball at correct angle (Bezier curve)
        # points: current car position, point behind ball, ball location

    return {
        'style': 'hurry',
        'planned_curve': curve,
        'debug': debug,
    }
