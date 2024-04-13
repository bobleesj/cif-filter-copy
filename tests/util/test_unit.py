import numpy as np
import unit


def test_round_to_three_decimal():
    assert 3.142 == unit.round_to_three_decimal(np.pi)
