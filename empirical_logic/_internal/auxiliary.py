"""
auxiliary.py

Auxiliary functions that are used to implement the Empirical Logic operators
"""

from dataclasses import dataclass
from typing import Optional, Union, List
from empirical_logic.core.constants import e_TRUE, e_FALSE
from empirical_logic.core.exceptions import (InputError,
                                             ValidityError,
                                             ModulationParameterError)
from empirical_logic.core.parameters import blackboard
from empirical_logic.operators.validity_modulation import e_MODULATE

Numeric = Union[int, float]
ModulatedValidity = List[Numeric]  # [validity, modulation parameter]
Validity = Union[Numeric, ModulatedValidity]


@dataclass(frozen=True)
class _Validity:
    """
    Internal representation of a validity value.

    Attributes:
        val: The validity value in [-1, 1]
        mod: Optional modulation parameter in [-1, 1]
    """
    val: float
    mod: Optional[float] = None

    def __iter__(self):
        is_mod = self.mod is not None
        yield self.val
        yield self.mod
        yield is_mod

    @property
    def is_modulated(self) -> bool:
        """Return True if a modulation parameter is present."""
        return self.mod is not None


def _flatten(validities):
    """
    Flatten a sequence of validity inputs.

    This generator ensures that nested iterables (e.g. tuples or lists
    returned by other operators) are expanded into a flat sequence of
    scalar validity values.

    This is necessary because some operators may return multiple values
    (e.g. tuples), while downstream operators expect a flat list of
    validity inputs.

    Args:
        validities:
            Iterable of validity inputs, which may include nested
            lists or tuples.

    Yields:
        Individual validity values (numeric or modulated validity),
        with all nested structures flattened.
    """
    for v in validities:
        # If the element is a list or tuple, expand it into individual elements
        if isinstance(v, (list, tuple)):
            yield from v
        else:
            # Otherwise, yield the element as-is
            yield v


def _parse_validity(v: Validity, func_name: str) -> _Validity:
    """
    Parse and check a validity input.

    Accepts either:
    - a numeric value in [-1, 1]
    - a list [val, mod] with both values in [-1, 1]

    Returns:
        _Validity object (internal representation)
    """

    if isinstance(v, list):  # modulated validity

        if len(v) != 2:
            raise InputError(
                f"ERROR in {func_name}: Incorrect syntax \"[val, mod]\": {v}"
            )

        val, mod = v

        if not (e_FALSE <= val <= e_TRUE):
            raise ValidityError(
                f"ERROR in {func_name}: validity value must be in [-1, 1], got {v}"
            )

        if not (-1 <= mod <= 1):
            raise ModulationParameterError(
                f"ERROR in {func_name}: modulation parameter must be in [-1, 1], got {v}"
            )

        return _Validity(float(val), float(mod))

    # --- scalar validity ---

    if not (e_FALSE <= v <= e_TRUE):
        raise ValidityError(
            f"ERROR in {func_name}: validity value must be in [-1, 1], got {v}"
        )

    return _Validity(float(v))


def _prepare_validities(
    validities: tuple,
    func_name: str,
    normalize: bool = True
) -> list:
    """
    Parse, optionally modulate and normalize validity inputs.

    Args:
        validities: input arguments
        func_name: name of calling function
        normalize: whether to normalize to [0, 1]

    Returns:
        List of processed validity values
    """

    # Snapshot of the "global" parameter e_M residing on the "blackboard"
    e_M = blackboard.e_M
    result = []

    for v in _flatten(validities):
        # Parse and check validity "v"
        v_obj = _parse_validity(v, func_name)

        if v_obj.is_modulated:
            # "v" is an expression of the form "[val, mod]",
            # which demands the "modulation" of "val" with parameter "mod".
            val = e_MODULATE(v_obj.val, v_obj.mod)
        else:
            if e_M != 0:
                # Global modulation parameter "e_M" is set on the "blackboard".
                val = e_MODULATE(v_obj.val, e_M)
            else:
                val = v_obj.val

        if normalize:
            # Normalize the validity input to the interval [0, 1]
            val = _normalize_validity(val)

        result.append(val)

    return result


def _normalize_validity(v: Numeric) -> Numeric:
    """
    Normalize the validity argument.

    That is, perform a mapping from interval [-1, 1]
    to the "normalized" interval [0, 1].

    Args:
        v:: [Validity]
            Validity taken from interval [-1, 1].

    Returns:
        Equivalent validity taken from interval [0, 1].
    """

    # Check the value of the validity argument
    assert e_FALSE <= v <= e_TRUE, (
        f"ERROR in _normalize_validity: "
        f"The value of the validity argument must be within interval [-1, 1], got {v}"
    )

    # Return the "normalized" validity value.
    return 0.5 * v + 0.5


def _restore_validity(v: Numeric) -> Numeric:
    """
    Restore the validity argument.

    That is, perform a mapping from interval [0, 1]
    to the "restored" interval [-1, 1].

    Args:
        v:: [Validity]
            Validity taken from interval [0, 1].

    Returns:
        Equivalent validity taken from interval [-1, 1].
    """

    # Check the value of the validity argument
    assert 0 <= v <= 1, (
        f"ERROR in _restore_validity: "
        f"The value of the validity argument must be within interval [0, 1], got {v}"
        )

    # Return the "restored" validity value.
    return 2 * v - 1
