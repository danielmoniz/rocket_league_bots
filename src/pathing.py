import numpy as np
import bezier

from util.vec import Vec3

def compute_shooting_curve(player):
    car_location = Vec3(player.car.physics.location)
    car_direction = Vec3(player.car.physics.direction)
    ball_location = player.game_info['ball_location']
    ball_to_goal = (Vec3(player.opposite_goal.location) - ball_location).normalized
    coordinates = [
        car_location,
        car_location + car_direction,
        ball_location - (ball_to_goal * 10),
        ball_location - ball_to_goal,
        ball_location,
    ]
    return compute_curve(coordinates)


def compute_curve(vectors, degree=10):
    massaged_vectors = get_fortran_array(vectors)
    return bezier.Curve(massaged_vectors, degree=degree)


def get_fortran_array(vectors):
    def vector_to_tuple(vector):
        return tuple(map(lambda x: float(x), vector))
    return np.asfortranarray([vector_to_tuple(x) for x in vectors])
