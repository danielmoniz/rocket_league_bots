import math

from src import pathing
from src.util.vec import Vec3

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

    scale = max_scale = 100
    very_short_range = 400
    short_range_factor = 10

    if distance_from_ball < very_short_range: # should probably just dodge into the ball
        scale = distance_from_ball / short_range_factor # temporary - same as below
        curve = pathing.compute_shooting_curve(player, scale=scale)
    elif distance_from_ball < short_range_factor * max_scale:
        scale = distance_from_ball / short_range_factor
        curve = pathing.compute_shooting_curve(player, scale=scale)
    else: # define maximum scale for the shooting curve
        curve = pathing.compute_shooting_curve(player, scale=100)

    # calculate curve required to strike the ball at correct angle (Bezier curve)
        # points: current car position, point behind ball, ball location
    curve = pathing.compute_shooting_curve(player, scale=100)
    next_coord = curve.evaluate(0.2).tolist()
    next_vector = pathing.convert_coordinate_to_vector(next_coord)

    pre_ball_coord = curve.evaluate(0.9).tolist()
    pre_ball_vector = pathing.convert_coordinate_to_vector(pre_ball_coord)

    planned_angle = next_vector - car_location
    car_direction = player.game_info['car_orientation'].forward
    turn_angle = find_correction(car_direction, planned_angle)


    print('#-------------------------#')
    print("Starting location:")
    print(car_location.round())

    print('Next vector:')
    print(next_vector.round())

    print('Pre-ball vector:')
    print(pre_ball_vector.round())

    print("Ball location:")
    print(player.game_info['ball_location'].round())

    print("Goal location:")
    print(Vec3(player.opposing_goal.location).round())

    # plan: use function that accepts current/future position/velocity
        # and returns a controller-based action object

    # optional: segment into smaller pieces (Bezier spline)

    return {
        'turn_angle': turn_angle,
        'throttle': 0.3,
        'target_location': next_vector,
        'style': 'hurry',
    }


# @TODO Move this somewhere reusable
import math
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