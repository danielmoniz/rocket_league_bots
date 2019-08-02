import math

from src import pathing
from src.util.vec import Vec3
from src.util.angle import find_correction

def enact(player):
    # near future: assume ball is on ground
    # PLAN
    # if very close to the ball (facing any direction), dodge in its direction
    # if not facing the ball:
        # ...can bezier curves handle this?
    # if facing the ball, and current line to the ball points into the opposing net:
        # boost and thrust toward the ball's location

    car_location = Vec3(player.car.physics.location)
    distance_from_ball = (car_location - player.game_info['ball_location']).length()

    very_short_range = 400
    short_range = 1000

    if distance_from_ball < very_short_range: # should probably just dodge into the ball
        # @TODO Dodge into a specific part of the ball
        print('Very short range')
    elif distance_from_ball < short_range:
        print('Short range.')
    else: # define maximum scale for the shooting curve
        print('Medium or greater range.')

    # calculate curve required to strike the ball at correct angle (Bezier curve)
        # points: current car position, point behind ball, ball location
    curve = pathing.compute_shooting_curve(player)
    next_coord = curve.evaluate(0.05).tolist()
    next_vector = pathing.convert_coordinate_to_vector(next_coord)

    pre_ball_coord = curve.evaluate(0.9).tolist()
    pre_ball_vector = pathing.convert_coordinate_to_vector(pre_ball_coord)

    planned_angle = next_vector - car_location
    car_direction = player.game_info['car_orientation'].forward
    turn_angle = find_correction(car_direction, planned_angle)

    # plan: use function that accepts current/future position/velocity
        # and returns a controller-based action object

    # optional: segment into smaller pieces (Bezier spline)

    return {
        'turn_angle': turn_angle, # @TODO Remove this
        'style': 'hurry',
        'planned_curve': curve,
    }
