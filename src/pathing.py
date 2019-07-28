import numpy as np
import bezier

from src.util.vec import Vec3

def compute_shooting_curve(player, scale=100):
    car_location = Vec3(player.car.physics.location)
    car_direction = player.game_info['car_orientation'].forward
    ball_location = player.game_info['ball_location']
    ball_to_goal = (Vec3(player.opposing_goal.location) - ball_location).normalized()

    coordinates = get_shooting_vectors(
        car_location, car_direction, ball_location, ball_to_goal, scale=scale)

    # TEST
    new_array = [[round(a.x, 2), round(a.y, 2)] for a in coordinates] # a.z is left out intentionally for graphing
    transposed = zip(*new_array)
    print('[')
    for row in transposed:
        print(f"    [{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}],")
    print(']')
    print('.' * 30)

    return compute_curve(coordinates)


def get_shooting_vectors(car_location, car_direction, ball_location, ball_to_goal, scale):
    return [
        car_location,
        car_location + (car_direction * 4 * scale),
        ball_location - (ball_to_goal * 5 * scale),
        ball_location - (ball_to_goal * 2 * scale),
        ball_location,
    ]


def compute_curve(vectors, degree=10):
    transposed = list(zip(*vectors))
    massaged_vectors = get_fortran_array(transposed)
    return bezier.Curve(massaged_vectors, degree=degree)


def get_fortran_array(vectors):
    def vector_to_tuple(vector):
        return tuple(map(lambda x: float(x), vector))
    return np.asfortranarray([vector_to_tuple(x) for x in vectors])


def convert_coordinate_to_vector(coord):
    return Vec3(
        coord[0][0],
        coord[1][0],
        max(coord[2][0], 25),
    )
