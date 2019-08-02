from src.util.vec import Vec3
from src.util.angle import find_correction

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
