# empirical_logic/__init__.py
__version__ = "1.0.0"

from .core.constants import e_TRUE, e_FALSE, e_UNKNOWN
from .core.parameters import Blackboard, blackboard
from.core.exceptions import EmpiricalLogicError

from .operators.validation_operators import (
    e_VALIDATE,
    e_INVALIDATE,
    e_DECIDE,
    e_WEIGHT,
)

from .operators.logical_operators import (
    e_NOT,
    e_AND,
    e_OR,
    e_XOR,
    e_ONLY_ONE_OF,
    e_AT_LEAST_ONE_OF,
    e_NECESSARILY_ALL_OF,
    e_IF_POSSIBLE_ALL_OF,
    e_SEVERAL_OF,
)

from .operators.validity_functions import (
    e_THRESHOLD,
    e_THRESHOLD_INVERSE,
    e_LIMITATION,
    e_LIMITATION_INVERSE,
    e_INTERVAL,
    e_INTERVAL_INVERSE,
    e_ESTIMATION,
    e_ESTIMATION_INVERSE,
)

from .operators.validity_modulation import e_MODULATE

__all__ = [
    "e_TRUE",
    "e_FALSE",
    "e_UNKNOWN",

    "e_VALIDATE",
    "e_INVALIDATE",
    "e_DECIDE",
    "e_WEIGHT",

    "e_NOT",
    "e_AND",
    "e_OR",
    "e_XOR",
    "e_IF_POSSIBLE_ALL_OF",
    "e_SEVERAL_OF",
    "e_ONLY_ONE_OF",
    "e_NECESSARILY_ALL_OF",
    "e_AT_LEAST_ONE_OF",

    "e_THRESHOLD",
    "e_THRESHOLD_INVERSE",
    "e_LIMITATION",
    "e_LIMITATION_INVERSE",
    "e_INTERVAL",
    "e_INTERVAL_INVERSE",
    "e_ESTIMATION",
    "e_ESTIMATION_INVERSE",

    "e_MODULATE",

    "Blackboard",
    "blackboard",

    "EmpiricalLogicError",
]
