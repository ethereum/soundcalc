"""
Preset finite fields to be used by the zkEVM configs
"""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class FieldParams:
    name: str
    # Base field characteristic (e.g., p = 2^{31} - 2^{27} + 1)
    p: int
    # Extension field degree (e.g., ext_size = 2 for Fp²)
    field_extension_degree: int
    # Extension field size |F| = p^{ext_size}
    F: float


def _F(p: int, ext_size: int) -> float:
    # Keep as float to match existing zkEVMConfig expectations
    return math.pow(p, ext_size)


# Base fields
GOLDILOCKS_P = (1 << 64) - (1 << 32) + 1
BABYBEAR_P = (1 << 31) - (1 << 27) + 1
KOALABEAR_P = (1 << 31) - (1 << 24) + 1  # Based on Plonky3: https://github.com/Plonky3/Plonky3/blob/main/koala-bear/src/koala_bear.rs

# Preset extension fields
GOLDILOCKS_2 = FieldParams(
    name="Goldilocks^2",
    p=GOLDILOCKS_P,
    field_extension_degree=2,
    F=_F(GOLDILOCKS_P, 2),
)

GOLDILOCKS_3 = FieldParams(
    name="Goldilocks^3",
    p=GOLDILOCKS_P,
    field_extension_degree=3,
    F=_F(GOLDILOCKS_P, 3),
)

BABYBEAR_4 = FieldParams(
    name="BabyBear^4",
    p=BABYBEAR_P,
    field_extension_degree=4,
    F=_F(BABYBEAR_P, 4),
)

BABYBEAR_5 = FieldParams(
    name="BabyBear^5",
    p=BABYBEAR_P,
    field_extension_degree=5,
    F=_F(BABYBEAR_P, 5),
)

KOALABEAR_4 = FieldParams(
    name="KoalaBear^4",
    p=KOALABEAR_P,
    field_extension_degree=4,
    F=_F(KOALABEAR_P, 4),
)



def field_element_size_bits(field: FieldParams) -> int:
    """
    Returns the size of a field element in bits.
    """
    return math.ceil(math.log2(field.p)) * field.field_extension_degree