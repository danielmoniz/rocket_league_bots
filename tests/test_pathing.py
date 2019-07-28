import pytest

import src.pathing as pathing

def test_pathing_functions_exist():
    assert pathing.compute_curve is not None