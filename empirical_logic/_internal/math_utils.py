"""
math_utils.py

Utility functions that are used to implement the e_MODULATE operator
"""

import math
from typing import Union
Numeric = Union[int, float]


def _sigmoid_up(v: Numeric) -> Numeric:
    if v < -1:
        return -1.0
    elif -1 <= v < 0:
        return -math.sqrt(-v * (2 + v))
    elif 0 <= v <= 1:
        return math.sqrt(v * (2 - v))
    else:  # v > 1
        return 1.0


def _sigmoid_down(v: Numeric) -> Numeric:
    if v < -1:
        return -1.0
    elif -1 <= v < 0:
        return -1 + math.sqrt(-v**2 + 1)
    elif 0 <= v <= 1:
        return 1 - math.sqrt(-v**2 + 1)
    else:  # v > 1
        return 1.0
