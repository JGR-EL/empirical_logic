"""
norms.py

t- and s-norms; c- and d-norms that are used to implement the Empirical Logic operators
"""

from empirical_logic.core.parameters import blackboard
from empirical_logic.core.constants import e_TRUE, e_FALSE
from empirical_logic.operators.validity_modulation import e_MODULATE
from typing import List, Union


Numeric = Union[int, float]
ModulatedValidity = List[Numeric]  # [validity, modulation factor]
Validity = Union[Numeric, ModulatedValidity]


def _einstein_sum_d(x: Numeric, y: Numeric) -> Numeric:
    """ Calculate the d-norm "Einstein sum".

    Args:
        x:: [Numeric]

            validity value normalized to the interval [0, 1].

        y:: [Numeric]

            validity value normalized to the interval [0, 1].

    Returns:
        The result of calculating the "Einstein sum" (x + y / x * y + 1).
    """

    # Check the values of the numeric arguments
    assert 0 <= x <= 1 and 0 <= y <= 1, (
        f"ERROR in _einstein_sum_d: "
        f"The values of the numeric arguments must be within interval [0, 1], got {x, y}"
    )

    # Calculate the "Einstein sum".
    return (x + y) / (x * y + 1)


def _einstein_product_c(x: Numeric, y: Numeric) -> Numeric:
    """ Calculate the c-norm "Einstein product".

    Args:
        x:: [Numeric]

            validity value normalized to the interval [0, 1].

        y:: [Numeric]

            validity value normalized to the interval [0, 1].

    Returns:
        The result of calculating the "Einstein sum" (x + y / x * y + 1).
    """

    # Check the values of the numeric arguments
    assert 0 <= x <= 1 and 0 <= y <= 1, (
        f"ERROR in _einstein_sum_d: "
        f"The values of the numeric arguments must be within interval [0, 1], got {x, y}"
    )

    # Return the "Einstein product".
    return x * y / (2 + (x * y - x - y))


def _generalized_mean_c(*input_values: Numeric) -> float:
    """ Calculate the c-norm "generalized mean".

    Args:
        *input_values:: [Numeric]

            validity values normalized to the interval [0, 1].

    Returns:
        The result of calculating the c-norm "generalized mean".
    """

    e_P = -0.5
    l = input_values
    n = len(l)

    # Check the values of the numeric arguments

    assert n > 0, (
        f"ERROR in _generalized_mean_d: Input must not be empty"
    )

    assert 0 <= min(input_values) <= 1 and 0 <= max(input_values) <= 1, (
        f"ERROR in _generalized_mean_c: "
        f"The values of the numeric arguments must be within interval [0, 1], got {input_values}"
    )

    # Calculate generalized mean (c-norm)
    if min(l) < 1e-10:
        r = 0.0
    else:
        r = (sum(x**e_P for x in l) / n) ** (1 / e_P)

    return r


def _generalized_mean_d(*input_values: Numeric) -> float:
    """ Calculate the d-norm "generalized mean".

    Args:
        *input_values:: [Numeric]

            validity values normalized to the interval [0, 1].

    Returns:
        The result of calculating the d-norm "generalized mean".
    """

    e_P = -0.5
    l = input_values
    n = len(l)

    # Check the values of the numeric arguments

    assert n > 0, (
        f"ERROR in _generalized_mean_d: Input must not be empty"
    )

    assert 0 <= min(input_values) <= 1 and 0 <= max(input_values) <= 1, (
        f"ERROR in _generalized_mean_d: "
        f"The values of the numeric arguments must be within interval [0, 1], got {input_values}"
    )

    # Calculate generalized mean (d-norm)
    if max(l) > 0.9999999999:
        r = 1.0
    else:
        r = 1 - (sum((1 - x) ** e_P for x in l) / n) ** (1 / e_P)

    return r
