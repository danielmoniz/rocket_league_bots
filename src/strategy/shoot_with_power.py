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

    # calculate curve required to strike the ball at correct angle (Bezier curve)
        # points: current car position, point behind ball, ball location
    curve = pathing.compute_shooting_curve(player)
    next_coord = curve.evaluate(0.1).tolist()
    next_vector = Vec3(
        next_coord[0][0],
        next_coord[1][0],
        next_coord[2][0],
    )
    third_coord = curve.evaluate(0.11).tolist()
    third_vector = Vec3(
        third_coord[0][0],
        third_coord[1][0],
        third_coord[2][0],
    )
    planned_angle = third_vector - next_vector
    turn_angle = find_correction(player.car.physics.velocity, planned_angle)
    # plan: use function that accepts current/future position/velocity
        # and returns a controller-based action object

    # optional: segment into smaller pieces (Bezier spline)

    return {
        'turn_angle': turn_angle,
        'throttle': 1.0,
        'target_location': next_vector,
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