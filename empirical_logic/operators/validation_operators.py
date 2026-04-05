"""
validation_operators.py

Empirical Logic operators, which perform the validity assessment of category memberships.
"""

from empirical_logic._internal.norms import (
    _einstein_sum_d,
    _einstein_product_c
)
from empirical_logic._internal.auxiliary import (
    _normalize_validity,
    _restore_validity,
    _parse_validity
)
from empirical_logic.core.exceptions import (
    InputError,
    ValidityError,
    WeightParameterError
)
from empirical_logic.core.constants import e_UNKNOWN, e_TRUE, e_FALSE
from empirical_logic.core.parameters import blackboard
from empirical_logic.operators.validity_modulation import e_MODULATE
from typing import Any, List, Union

Numeric = Union[int, float]
ModulatedValidity = List[Numeric]  # [validity, modulation parameter]
Validity = Union[Numeric, ModulatedValidity]


def _apply_validation_operator(
    premise: Validity,
    hypotheses: list,
    func_name: str,
    combine_func,
    invert_premise: bool = False
) -> Any:
    """
    Internal helper for e_VALIDATE and e_INVALIDATE.

    Args:
        premise: validity input
        hypotheses: list of validity inputs
        func_name: name of the calling function
        combine_func: norm function (_einstein_sum_d or _einstein_product_c)
        invert_premise: whether to use (1 - premise)

    Returns:
        Conclusion(s)
    """

    # Snapshot of the "global" parameters "e_M1" and "e_M2" residing on the "blackboard"
    e_M1 = blackboard.e_M1
    e_M2 = blackboard.e_M2

    n = len(hypotheses)

    if n == 0:
        raise InputError(
            f"ERROR in {func_name}: expecting at least one hypothesis, got {n}"
        )

    # --- Process premise of e_VALIDATE or e_INVALIDATE---

    p = _parse_validity(premise, func_name)

    if p.val <= e_UNKNOWN:
        # Premise below activation threshold, return hypotheses unchanged
        return hypotheses[0] if n == 1 else tuple(hypotheses)

    # Premise has reached the activation threshold:
    # Determine a "reduced premise" and normalize it to the interval [0, 1].
    # "Reducing" the premise is necessary in order to ensure the continuity
    # of e_VALIDATE or e_INVALIDATE at the activation threshold.

    if p.is_modulated:
        # validity with a modulation parameter
        reduced = _normalize_validity(e_MODULATE(p.val, p.mod)) - 0.5
    else:
        # validity without a modulation parameter
        if e_M1 != 0:
            # Global modulation parameter "e_M1" is set on the "blackboard".
            reduced = _normalize_validity(e_MODULATE(p.val, e_M1)) - 0.5
        else:
            reduced = _normalize_validity(p.val) - 0.5

    # --- Process hypotheses of e_VALIDATE or e_INVALIDATE---

    normalized = []
    for h in hypotheses:
        h_obj = _parse_validity(h, func_name)

        if h_obj.is_modulated:
            # hypothesis with a modulation parameter
            normalized.append(_normalize_validity(e_MODULATE(h_obj.val, h_obj.mod)))
        else:
            # hypothesis without a modulation parameter
            if e_M2 != 0:
                # Global modulation parameter "e_M2" is set on the "blackboard".
                normalized.append(_normalize_validity(e_MODULATE(h_obj.val, e_M2)))
            else:
                normalized.append(_normalize_validity(h_obj.val))

    # --- Apply suitable operator: ---
    # d-norm (Einstein sum) for e_VALIDATE
    # c-norm (Einstein product) for e_INVALIDATE

    results = []

    for nh in normalized:
        p_val = 1 - reduced if invert_premise else reduced
        results.append(_restore_validity(combine_func(p_val, nh)))

    return results[0] if len(results) == 1 else tuple(results)


def e_VALIDATE(premise: Validity, *current_hypotheses: Validity) -> Any:
    """ Confirm (validate) one or more hypotheses.

    Args:
        premise:: [Validity]
            Premise validity that must be within interval [0, 1]
            to "fire" (i.e., validate the hypotheses).

        current_hypotheses:: [Validity]
            Current validity values of one or more hypotheses.

    Returns:
        Updated validity value(s) of the hypotheses.
    """

    return _apply_validation_operator(
        premise,
        list(current_hypotheses),
        "e_VALIDATE",
        _einstein_sum_d,
        invert_premise=False
    )


def e_INVALIDATE(premise: Validity, *current_hypotheses: Validity) -> Any:
    """ Refute (invalidate) one or more hypotheses.

       Args:
           premise:: [Validity]
               Premise validity that must be within interval [0, 1]
               in order to "fire" (i.e. "invalidate" the hypotheses).

           current_hypotheses:: [Validity]
               Current validity values of one or more hypotheses.

       Returns:
           Updated validity value(s) of the hypotheses.
       """

    return _apply_validation_operator(
        premise,
        list(current_hypotheses),
        "e_INVALIDATE",
        _einstein_product_c,
        invert_premise=True
    )


def e_DECIDE(validation: Numeric, invalidation: Numeric) -> Numeric:
    """
    Decide (balance) the resulting validity value of a hypothesis that is
    obtained by applying e_VALIDATE with pro-indications and independently
    applying e_INVALIDATE with contra-indications of the same hypothesis.

    (Note that before each of these operations, the validity of the hypothesis
    must be initialized with the validity value e_UNKNOWN = 0).

    Args:
        validation:: [Numeric]
            The resulting validity of confirming (validating) the unknown
            validity of a hypothesis with pro-indications.

        invalidation:: [Numeric]
            The resulting validity of refuting (invalidating) the unknown
            validity of a hypothesis with contra-indications.

    Returns:
        The result of balancing the arguments with "validation + invalidation".
    """

    # --- Check the arguments ---
    if not (e_UNKNOWN <= validation <= e_TRUE):
        raise ValidityError(
            f"ERROR in e_DECIDE: "
            f"First argument must be within interval [0, 1], got {validation}"
        )
    if not (e_FALSE <= invalidation <= e_UNKNOWN):
        raise ValidityError(
            f"ERROR in e_DECIDE: "
            f"Second argument must be within interval [-1, 0], got {invalidation}"
        )

    # --- Return the calculated result ---
    return validation + invalidation


def e_WEIGHT(v: Validity, w: Numeric) -> Any:
    """
    Weight the validity v of an indication (pro- or contra-indication)
    of some hypothesis.

    Args:
        v:: [Validity]
            Validity of some indication.

        w:: [Numeric]
            Weight parameter taken from interval [0, 1].

    Returns:
        The result of weighting the validity value.
    """

    # --- Check the weight parameter ---
    if not (0 <= w <= 1):
        raise WeightParameterError(
            f"ERROR in e_WEIGHT: "
            f"The weight parameter must be within interval [0, 1], got {w}"
        )

    # --- Parse validity input ---
    v_obj = _parse_validity(v, "e_WEIGHT")

    val, mod, is_mod = v_obj.val, v_obj.mod, v_obj.is_modulated

    # --- Apply weighting ---
    if is_mod: # validity argument with modulation parameter
        # Preserve modulation parameter
        return [val * w, mod]
    else: # validity argument without modulation parameter
        return val * w
