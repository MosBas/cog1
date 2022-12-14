"""Some unit tests for the receiver stats calculations"""

import numpy as np
from ..receiver import Receiver

def test_process_vector():
    """Make sure we compute std and mean correctly"""
    receiver = Receiver(None, 0, None, False)
    output = None
    for _ in range(100):
        vector = np.array([1])
        output = receiver.process_vector(vector)
    (_, _, mean, std) = output.split(',')
    assert mean == '1.0'
    assert std == '0.0'
