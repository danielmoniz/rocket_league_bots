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
    def test_should_return_five_coordinates(self):
        scale = 100
        vec1, vec2, vec3, vec4 = (Vec3(1), Vec3(2), Vec3(3), Vec3(4))
        result = pathing.get_shooting_vectors(vec1, vec2, vec3, vec4, scale)
        assert len(result) == 5
