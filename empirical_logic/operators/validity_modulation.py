"""
validaty_modulation.py

contains the function e_MODULATE that implements the meaning of
the modulated validity expression "[v, m]"
"""

from empirical_logic._internal.math_utils import _sigmoid_up, _sigmoid_down
from empirical_logic.core.constants import e_TRUE, e_FALSE
from empirical_logic.core.exceptions import ValidityError, ModulationParameterError
from typing import List, Union

Numeric = Union[int, float]
ModulatedValidity = List[Numeric]  # [validity, modulation factor]
Validity = Union[Numeric, ModulatedValidity]


def e_MODULATE(v: Numeric, m: Numeric) -> Numeric:
    """
    Modulate the validity argument.
    That is, implement the meaning of the validity expression [v, m] with m ∈ [−1, 1], as follows:

    (1) m = 0                           => [v, m] = v (leave the validity of argument v unchanged)
    (2) m ∈ [−1, 1] and v ∈ {-1, 0, 1}  => [v, m] = v (leave the validity of argument v unchanged)
    (3) m > 0       and v ∈ (0, 1)      => [v, m] > v (increase the positive tendency of argument v)
    (4) m > 0       and v ∈ (-1, 0)     => [v, m] ≤ v (increase the negative tendency of argument v)
    (5) m < 0       and v ∈ (0, 1)      => [v, m] < v (decrease the positive tendency of argument v)
    (6) m < 0       and v ∈ (-1, 0)     => [v, m] ≥ v (decrease the negative tendency of argument v)

    Args:
        v:: [Numeric]
            Validity taken from interval [-1, 1].

        m:: [Numeric]
            Modulation parameter taken from interval [-1, 1].

    Returns:
        The modulated validity argument.
    """

    # Check the value of the validity argument
    if not (e_FALSE <= v <= e_TRUE):
        raise ValidityError(
            f"ERROR in e_MODULATE: "
            f"The value of the validity argument must be within interval [-1, 1], got {v}"
        )

    # Check the modulation parameter
    if not (-1 <= m <= 1):
        raise ModulationParameterError(
            f"ERROR in e_MODULATE: "
            f"The modulation parameter must be within interval [-1, 1], got {m}"
        )

    if m >= 0:
        return (1 - abs(m)) * v + abs(m) * _sigmoid_up(v)
    else:
        return (1 - abs(m)) * v + abs(m) * _sigmoid_down(v)
