from __future__ import annotations

import math

from soundcalc.common.fields import FieldParams


def get_gkr_soundness_error(field: FieldParams, alphabet_size: int, num_lookups_M: int) -> float:
    """
    Computes soundness error for the GKR protocol as:
        (1/2) * (n + m) * (3 * (n + m) + 1) / |F|
    where:
        |F| is the field size,
        2^n is the alphabet size,
        m = log2(M), and M is the number of lookups.
    """
    if alphabet_size <= 0:
        raise ValueError("alphabet_size must be positive")
    if num_lookups_M <= 0:
        raise ValueError("num_lookups_M must be positive")

    n = math.log2(alphabet_size)
    m = math.log2(num_lookups_M)
    nm = n + m
    return 0.5 * nm * (3 * nm + 1) / field.F
