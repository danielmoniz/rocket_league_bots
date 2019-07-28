from src.util.vec import Vec3

def enact(player):
    # Find the direction of our car using the Orientation class
    car_to_ball = player.game_info['ball_location'] - player.game_info['car_location']
    car_direction = player.game_info['car_orientation'].forward
    steer_correction_radians = find_correction(car_direction, car_to_ball)
    return {
        'turn_angle': steer_correction_radians,
        'throttle': 1.0,
        'target_location': player.game_info['ball_location'],
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