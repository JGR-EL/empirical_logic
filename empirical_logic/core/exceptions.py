"""
Custom exception hierarchy for empirical logic related errors.

Hierarchy:

Exception
└─ EmpiricalLogicError
     ├─ InputError
     ├─ ValidityError
     ├─ ModulationParameterError
     └─ WeightParameterError
"""


class EmpiricalLogicError(Exception):
    """
    Base class for all empirical logic related errors.
    """

    def __init__(self, message: str = "An empirical logic error occurred."):
        super().__init__(message)


class InputError(EmpiricalLogicError):
    """
    Raised when an error occurs due to invalid or malformed input.
    """

    def __init__(self, message: str = "Invalid input provided."):
        super().__init__(message)


class ValidityError(EmpiricalLogicError):
    """
    Raised when a validity condition is violated.
    """

    def __init__(self, message: str = "A validity constraint was violated."):
        super().__init__(message)


class ModulationParameterError(EmpiricalLogicError):
    """
    Raised when a modulation parameter is invalid.
    """

    def __init__(self, message: str = "Invalid modulation parameter."):
        super().__init__(message)


class WeightParameterError(EmpiricalLogicError):
    """
    Raised when a weight parameter is invalid.
    """

    def __init__(self, message: str = "Invalid weight parameter."):
        super().__init__(message)
