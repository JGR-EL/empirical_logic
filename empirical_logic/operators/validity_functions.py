"""
validity_functions.py

Standardized validity functions for "bound categories". Bound categories are bound to
a scalable reference magnitude (e.g. sizes, ages, degree of capacity utilization, …)

e_THRESHOLD:
    strictly monotonically increasing and continuously differentiable sigmoid
    function (swan neck curve) that describes the validity of a category
    restricted downwards on the scale of the reference magnitude (e.g., "high
    machine utilization").

e_THRESHOLD_INVERSE: inverse function of e_THRESHOLD.

e_LIMITATION:
    strictly monotonically decreasing and continuously differentiable sigmoid
    function that describes the validity of a category restricted above
    on the scale of the reference quantity (e.g., "low machine utilization").

e_LIMITATION_INVERSE: inverse function of e_LIMITATION.

e_INTERVAL:
    a validity interval of a category (e.g., "average machine utilization")
    that is limited both upwards and downwards on the scale of the reference
    magnitude. It is continuously differentiable and initially increases in
    a strictly monotonical manner, before decreasing again in a strictly
    monotonical manner after reaching the maximum.

e_INTERVAL_INVERSE: inverse function of e_INTERVAL.

e_ESTIMATION:
    a strictly increasing and, after reaching an estimated value, strictly
    decreasing bell-shaped curve. It describes a category bound to a reference
    magnitude whose range of validity values constitutes an interval with the
    midpoint given by the estimated value (e.g. average machine capacity
    utilization).

e_ESTIMATION_INVERSE: inverse function of e_ESTIMATION.

"""

import math
from empirical_logic.core.constants import v_MIN, v_MAX
from empirical_logic.core.exceptions import InputError
from typing import Union

Numeric = Union[int, float]

def e_THRESHOLD(x: Numeric, t: Numeric, f: Numeric) -> Numeric:
    """
    Calculate the validity value of a bound category that is restricted
    downwards on the scale of the reference magnitude.

    Args:

        x:: [Numeric]:  the reference magnitude which binds the category.
        t:: [Numeric]:  validity threshold above which belonging to the
                        category can be determined.
        f:: [Numeric]:  fuzziness of the category.

    Returns:
        The validity value of the category at reference magnitude value x.
    """
    if f <= 0:
        raise InputError(
            f"ERROR in e_THRESHOLD: "
            f"The fuzziness parameter f = {f} must be a positive number."
        )

    return math.tanh((x - t) / f)


def e_THRESHOLD_INVERSE(
    v: Numeric,
    x_MIN: Numeric,
    x_MAX: Numeric,
    t: Numeric,
    f: Numeric
) -> Numeric:
    """
    For a given validity value of a bound category described by an e_THRESHOLD
    validity function, calculate the corresponding value of the reference magnitude.

    Args:

        v:: [Numeric]:      validity value from the validity interval [-1, 1].
        x_MIN:: [Numeric]:  minimal permissible value of the reference magnitude.
        x_MAX:: [Numeric]:  maximal permissible value of the reference magnitude.
        t:: [Numeric]:      validity threshold above which belonging to the
                            category can be determined.
        f:: [Numeric]:      fuzziness of the category.

    Returns:
         The validity value of the category at reference magnitude value x.
    """
    if f <= 0:
        raise InputError(
            f"ERROR in e_THRESHOLD_INVERSE: "
            f"The fuzziness parameter f = {f} must be a positive number."
        )

    if x_MAX <= x_MIN:
        raise InputError(
            f"ERROR in e_THRESHOLD_INVERSE: "
            f"The minimal permissible value x_MIN = {x_MIN} of the reference magnitude "
            f"must not exceed the maximal permissible value x_MAX = {x_MAX}."
        )

    # Limitation for arctanh (|x| < 1 required)
    if abs(v) > v_MAX:
        x = math.copysign(v_MAX, v)
    else:
        x = float(v)

    y = t + f * math.atanh(x)

    # Clipping on [x_MIN, x_MAX]
    if y > x_MAX:
        return x_MAX
    elif y < x_MIN:
        return x_MIN
    else:
        return y


def e_LIMITATION(x: Numeric, l: Numeric, f: Numeric) -> Numeric:
    """
    Calculate the validity value of a bound category that is restricted
    downwards on the scale of the reference magnitude.

    Args:

        x:: [Numeric]:  the reference magnitude which binds the category.
        l:: [Numeric]:  validity limit above which belonging to the category
                        can no longer be determined.
        f:: [Numeric]:  fuzziness of the category.

    Returns:
        The validity value of the category at reference magnitude value x.
    """
    if f <= 0:
        raise InputError(
            f"ERROR in e_LIMITATION: "
            f"The fuzziness parameter f = {f} must be a positive number."
        )

    return -math.tanh((x - l) / f)


def e_LIMITATION_INVERSE(
    v: Numeric,
    x_MIN: Numeric,
    x_MAX: Numeric,
    l: Numeric,
    f: Numeric
) -> Numeric:
    """
    For a given validity value of a bound category described by an e_LIMITATION
    validity function, calculate the corresponding value of the reference magnitude.

    Args:

        v:: [Numeric]:      validity value from the validity interval [-1, 1].
        x_MIN:: [Numeric]:  minimal permissible value of the reference magnitude.
        x_MAX:: [Numeric]:  maximal permissible value of the reference magnitude.
        l:: [Numeric]:      validity limit above which belonging to the category
                            can no longer be determined.
        f:: [Numeric]:     fuzziness of the category.

    Returns:
         The validity value of the category at reference magnitude value x.
    """
    if f <= 0:
        raise InputError(
            f"ERROR in e_LIMITATION_INVERSE: "
            f"The fuzziness parameter f = {f} must be a positive number."
        )

    if x_MAX <= x_MIN:
        raise InputError(
            f"ERROR in e_LIMITATION_INVERSE: "
            f"The minimal permissible value x_MIN = {x_MIN} of the reference magnitude "
            f"must not exceed the maximal permissible value x_MAX = {x_MAX}."
        )

    # Limitation for arctanh (|x| < 1 required)
    if abs(v) > v_MAX:
        x = math.copysign(v_MAX, v)
    else:
        x = float(v)

    y = l - f * math.atanh(x)

    # Clipping on [x_MIN, x_MAX]
    if y > x_MAX:
        return x_MAX
    elif y < x_MIN:
        return x_MIN
    else:
        return y


def e_INTERVAL(x: Numeric, t: Numeric, l: Numeric, f: Numeric) -> Numeric:
    """
    Calculate the validity value of a bound category that is restricted
    upwards and downwards on the scale of the reference magnitude.

    Args:

        x:: [Numeric]:  the reference magnitude which binds the category.
        t:: [Numeric]:  validity threshold above which belonging to the
                        category can be determined.
        l:: [Numeric]:  validity limit above which belonging to the category
                        can no longer be determined.
        f:: [Numeric]:  fuzziness of the category.

    Returns:
        The validity value of the category at reference magnitude value x.
    """
    if t > l:
        raise InputError(
            f"ERROR in e_INTERVAL: "
            f"The threshold parameter t = {t} must not exceed the "
            f"limitation parameter l = {l}"
        )

    if f <= 0:
        raise InputError(
            f"ERROR in e_INTERVAL: "
            f"The fuzziness parameter f = {f} must be a positive number."
        )

    return min(e_THRESHOLD(x, t, f), e_LIMITATION(x, l, f))


def e_INTERVAL_INVERSE(
    v: Numeric,
    z: Numeric,
    x_MIN: Numeric,
    x_MAX: Numeric,
    t: Numeric,
    l: Numeric,
    f: Numeric
) -> Numeric:
    """
    For a given validity value of a bound category described by an e_interval
    validity function, calculate the corresponding value of the reference magnitude.

    Args:

        v:: [Numeric]:      validity value from the validity interval [-1, 1].
        z:: [Numeric]:      Last determined value of the reference magnitude,
                            which is taken as a criterion to decide on the
                            applicable inversion section.
        x_MIN:: [Numeric]:  minimal permissible value of the reference magnitude.
        x_MAX:: [Numeric]:  maximal permissible value of the reference magnitude.
        t:: [Numeric]:      validity threshold above which belonging to the
                            category can be determined.
        l:: [Numeric]:      validity limit above which belonging to the category
                            can no longer be determined.
        f:: [Numeric]:      fuzziness of the category.

    Returns:
         The validity value of the category at reference magnitude value x.
    """
    if f <= 0:
        raise InputError(
            f"ERROR in e_INTERVAL_INVERSE: "
            f"The fuzziness parameter f = {f} must be a positive number."
        )

    if x_MAX <= x_MIN:
        raise InputError(
            f"ERROR in e_INTERVAL_INVERSE: "
            f"The minimal permissible value x_MIN = {x_MIN} of the reference magnitude "
            f"must not exceed the maximal permissible value x_MAX = {x_MAX}."
        )

    # Limitation for arctanh (|x| < 1 required)
    if abs(v) > v_MAX:
        x = math.copysign(v_MAX, v)
    else:
        x = float(v)

    # Calculate the inverse function
    x_MIDDLE = (t + l) / 2

    if z > x_MIDDLE:
        return e_LIMITATION_INVERSE(x, x_MIDDLE, x_MAX, l, f)
    else:
        return e_THRESHOLD_INVERSE(x, x_MIN, x_MIDDLE, t, f)


def e_ESTIMATION(x: Numeric, a: Numeric, f: Numeric) -> Numeric:
    """
    Calculate the validity value of a bound category that estimates
    a reference magnitude.

    Args:

        x:: [Numeric]:  the reference magnitude which binds the category.
        a:: [Numeric]:  Estimated value of the reference magnitude.
        f:: [Numeric]:  fuzziness of the category.

    Returns:
        The validity value of the category at reference magnitude value x.
    """
    if f <= 0:
        raise InputError(
            f"ERROR in e_ESTIMATION: "
            f"The fuzziness parameter f = {f} must be a positive number."
        )

    return 2 * math.exp(-4 * math.log(2) * (x - a) ** 2 / (f ** 2)) - 1


def e_ESTIMATION_INVERSE(
    v: Numeric,
    z: Numeric,
    x_MIN: Numeric,
    x_MAX: Numeric,
    a: Numeric,
    f: Numeric
) -> Numeric:
    """
    For a given validity value of a bound category described by an e_ESTIMATION
    validity function, calculate the corresponding value of the reference magnitude.

    Args:

        v:: [Numeric]:      validity value from the validity interval [-1, 1].
        z:: [Numeric]:      Last determined value of the reference magnitude,
                            which is taken as a criterion to decide on the
                            applicable inversion section.
        x_MIN:: [Numeric]:  minimal permissible value of the reference magnitude.
        x_MAX:: [Numeric]:  maximal permissible value of the reference magnitude.
        a:: [Numeric]:      Estimated value of the reference magnitude.
        f:: [Numeric]:      fuzziness of the category.

    Returns:
         The validity value of the category at reference magnitude value x.
    """
    if f <= 0:
        raise InputError(
            f"ERROR in e_ESTIMATION_INVERSE: "
            f"The fuzziness parameter f = {f} must be a positive number."
        )

    if x_MAX <= x_MIN:
        raise InputError(
            f"ERROR in e_ESTIMATION_INVERSE: "
            f"The minimal permissible value x_MIN = {x_MIN} of the reference magnitude "
            f"must not exceed the maximal permissible value x_MAX = {x_MAX}."
        )

    # Lower limit (argument must not be < v_MIN)
    if v < v_MIN:
        x = v_MIN
    else:
        x = float(v)

    # Calculate the inverse function
    inner = -math.log((x + 1) * 0.5) / math.log(2)

    if z > a:
        y = a + 0.5 * f * math.sqrt(inner)
    else:
        y = a - 0.5 * f * math.sqrt(inner)

    # Clipping on [x_MIN, x_MAX]
    if y > x_MAX:
        return x_MAX
    elif y < x_MIN:
        return x_MIN
    else:
        return y