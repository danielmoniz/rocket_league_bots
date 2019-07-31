import pytest
import numpy as np

import src.pathing as pathing
from src.util.vec import Vec3

class TestGetFortranArray:
    def test_should_return_a_2d_numpy_array(self):
        vectors = [
            Vec3(1, 4, 0),
            Vec3(1, 6, -5),
            Vec3(-4, 1, 7),
        ]
        result = pathing.get_fortran_array(vectors)

        assert type(result) == np.ndarray
        assert result.size == 9
        for thing in result:
            print(thing, type(thing))
            assert type(thing) == np.ndarray

class TestGetShootingVectors:
    scale = 100
    def test_should_return_five_coordinates(self):
        vec1, vec2, vec3, vec4 = (Vec3(1), Vec3(2), Vec3(3), Vec3(4))
        result = pathing.get_shooting_vectors(vec1, vec2, vec3, vec4, self.scale)
        assert len(result) == 5

    def test_should_return_first_vector_equal_to_car_location(self):
        pass

    def test_should_direct_car_forward_when_close_and_facing(self):
        car_location = Vec3(0, 0, 0)
        car_direction = Vec3(1, 0, 0)
        ball_location = Vec3(4, 0, 0)
        goal_location = Vec3(100, 0, 0)
        ball_to_goal = (goal_location - ball_location).normalized()
        vectors = pathing.get_shooting_vectors(
            car_location,
            car_direction,
            ball_location,
            ball_to_goal,
            self.scale,
        )
        print(car_location, vectors[0])
        print(vectors)
        for i in range(1, 4):
            assert vectors[i].x > car_location.x
            assert vectors[i].x < ball_location.x
            assert vectors[i].y == 0
            assert vectors[i].z == 0

        assert vectors[4] == ball_location
        # assert vectors[4].x < ball_location.x
        # assert vectors[4].y == 0
        # assert vectors[4].z == 0
