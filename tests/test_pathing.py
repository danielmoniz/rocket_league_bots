import pytest
import numpy as np

import src.pathing as pathing
from util.vec import Vec3

class TestGetFortranArray:
    def test_it_should_return_a_2d_numpy_array(self):
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
