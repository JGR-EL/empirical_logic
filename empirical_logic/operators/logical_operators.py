"""
logical_operators.py

Empirical logic operators that are used to establish logical connections.
"""
from empirical_logic._internal.auxiliary import (
    _restore_validity,
    _parse_validity,
    _prepare_validities
)
from empirical_logic._internal.norms import (
    _generalized_mean_c,
    _generalized_mean_d
)
from empirical_logic.core.exceptions import InputError

from typing import List, Union

Numeric = Union[int, float]
ModulatedValidity = List[Numeric]  # [validity, modulation factor]
Validity = Union[Numeric, ModulatedValidity]


def e_NOT(*validities: Validity):
    """
    Negate the validity argument(s) such that a single validity value v becomes -v
    and a modulated validity [v, m] becomes [-v, m].

     Args: *validities:: [Validity]: One or more validity values.

     Returns: The negated validity values.
     """

    negated = []

    for v in validities:
        # Parse and check validity "v"
        v_obj = _parse_validity(v, "e_NOT")

        if v_obj.is_modulated:
            # "v" is an expression of the form "[val, mod]",
            # which demands the negation of "val".
            negated.append([-v_obj.val, v_obj.mod])
        else:
            # "v" is a numeric type, which demands to return it as "-v"
            negated.append(-v_obj.val)

    return negated[0] if len(negated) == 1 else tuple(negated)


def e_AND(*validities: Validity, alias_name: str = None) -> Numeric:
    """ Perform a conjunctive logical connection of the arguments.

    Args:

        *validities:: [Validity]: Two or more validity values.

        alias_name: [str]: Optional alias function name

    Returns:
        The conjunctive logical connection of the arguments.
    """

    func_name = alias_name or "e_AND"

    if len(validities) < 2:
        raise InputError(
            f"ERROR in {func_name}: expecting at least two arguments, got {len(validities)}"
        )

    normalized = _prepare_validities(validities, func_name, normalize=True)

    # Apply the "generalized mean" c-norm and
    # restore the result to the validity interval [-1, 1]
    return _restore_validity(_generalized_mean_c(*normalized))



def e_OR(*validities: Validity, alias_name: str = None) -> Numeric:
    """ Perform a disjunctive logical connection of the arguments.

    Args:

        *validities:: [Validity]: Two or more validity values.

        alias_name: [str]: Optional alias function name

    Returns:
        The disjunctive logical connection of the arguments.
    """

    func_name = alias_name or "e_OR"

    if len(validities) < 2:
        raise InputError(
            f"ERROR in {func_name}: expecting at least two arguments, got {len(validities)}"
        )

    normalized = _prepare_validities(validities, func_name, normalize=True)

    # Apply the "generalized mean" d-norm and
    # restore the result to the validity interval [-1, 1]
    return _restore_validity(_generalized_mean_d(*normalized))


def e_XOR(*validities: Validity, alias_name: str = None) -> Numeric:
    """ Perform an exclusive disjunctive logical connection of the arguments.

    Args:

        *validities:: [Validity]: Two or more validity values.

        alias_name: [str]: Optional alias function name

    Returns:
        The exclusive disjunctive logical connection of the arguments.
    """

    func_name = alias_name or "e_XOR"

    if len(validities) < 2:
        raise InputError(
            f"ERROR in {func_name}: expecting at least two arguments, got {len(validities)}"
        )

    normalized = _prepare_validities(validities, func_name, normalize=True)

    # Determine the index of the maximum validity value
    max_value = max(normalized)
    i = normalized.index(max_value)

    # Negate all validity values except the maximum.
    # Then apply the "generalized mean" c-norm and
    # restore the result to the validity interval [-1, 1]
    others = [1 - x for j, x in enumerate(normalized) if j != i]

    return _restore_validity(
        _generalized_mean_c(
            normalized[i],
            *others
        )
    )


def e_IF_POSSIBLE_ALL_OF(*validities: Validity) -> Numeric:
    """ Alias to operator e_AND """
    return e_AND(*validities, alias_name = "e_IF_POSSIBLE_ALL_OF")


def e_SEVERAL_OF(*validities: Validity) -> Numeric:
    """ Alias to operator e_OR """
    return e_OR(*validities, alias_name = "e_SEVERAL_OF")


def e_ONLY_ONE_OF(*validities: Validity) -> Numeric:
    """ Alias to operator e_XOR """
    return e_XOR(*validities, alias_name = "e_ONLY_ONE_OF")


def e_NECESSARILY_ALL_OF(*validities: Validity) -> Numeric:
    """ Determine the minimal validity value.

    Args:

        *validities:: [Validity]

            Two or more validity values.

    Returns:
        The minimal validity value.
    """

    if len(validities) < 2:
        raise InputError(
            f"ERROR in e_NECESSARILY_ALL_OF: expecting at least two arguments, got {len(validities)}"
        )

    values = _prepare_validities(validities, "e_NECESSARILY_ALL_OF", normalize=False)

    return min(values)


def e_AT_LEAST_ONE_OF(*validities: Validity) -> Numeric:
    """ Determine the maximal validity value.

    Args:

        *validities:: [Validity]

            Two or more validity values.

    Returns:
        The maximal validity value.
    """

    if len(validities) < 2:
        raise InputError(
            f"ERROR in e_AT_LEAST_ONE_OF: expecting at least two arguments, got {len(validities)}"
        )

    values = _prepare_validities(validities, "e_AT_LEAST_ONE_OF", normalize=False)

    return max(values)
