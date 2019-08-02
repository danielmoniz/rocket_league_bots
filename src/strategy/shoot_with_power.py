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

    curve = pathing.compute_shooting_curve(player)

    if distance_from_ball < very_short_range:# and in a decent line
        # @TODO Dodge into a specific part of the ball
        print('Very short range')
    elif distance_from_ball < short_range:
        print('Short range.')
    else: # define maximum scale for the shooting curve
        print('Medium or greater range.')

    # calculate curve required to strike the ball at correct angle (Bezier curve)
        # points: current car position, point behind ball, ball location

    return {
        'style': 'hurry',
        'planned_curve': curve,
    }
