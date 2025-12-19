"""
Preset finite fields to be used by the zkEVM configs
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class FieldParams:
    name: str
    # Base field characteristic (e.g., p = 2^{31} - 2^{27} + 1)
    p: int
    # Extension field degree (e.g., ext_size = 2 for Fp²)
    field_extension_degree: int
    # Extension field size |F| = p^{ext_size}
    F: float
    # Two-adicity of the multiplicative group (largest s such that 2^s divides p-1)
    #
    # This determines the maximum possible FFT domain size.
    two_adicity: int

    def to_string(self) -> str:
        """
        Returns a human-readable string representing the field,
        """
        return self.name

    def base_field_element_size_bits(self) -> int:
        """
        Returns the size of a base field element in bits.
        """
        return math.ceil(math.log2(self.p))

    def extension_field_element_size_bits(self) -> int:
        """
        Returns the size of an extension field element in bits.
        """
        return self.base_field_element_size_bits() * self.field_extension_degree


def _F(p: int, ext_size: int) -> float:
    # Keep as float to match existing zkEVMConfig expectations
    return math.pow(p, ext_size)


# Base fields
GOLDILOCKS_P = (1 << 64) - (1 << 32) + 1
# Goldilocks 2-adicity: 2^64 - 2^32 = 2^32 * (2^32 - 1). 32 is the max power of 2.
GOLDILOCKS_TWO_ADICITY = 32

BABYBEAR_P = (1 << 31) - (1 << 27) + 1
# BabyBear 2-adicity: 2^31 - 2^27 = 2^27 * (2^4 - 1). 27 is the max power of 2.
BABYBEAR_TWO_ADICITY = 27

KOALABEAR_P = (1 << 31) - (1 << 24) + 1
# KoalaBear 2-adicity: 2^31 - 2^24 = 2^24 * (2^7 - 1). 24 is the max power of 2.
KOALABEAR_TWO_ADICITY = 24

M31_P = (1 << 31) - 1
# M31 has Needs an extension field to have any 2-adicity > 1

# BN254 scalar field
BN254_P = 21888242871839275222246405745257275088548364400416034343698204186575808495617
# BN254 2-adicity: 2^28 * (some odd number).
BN254_TWO_ADICITY = 28

# Preset extension fields
GOLDILOCKS_2 = FieldParams(
    name="Goldilocks²",
    p=GOLDILOCKS_P,
    field_extension_degree=2,
    F=_F(GOLDILOCKS_P, 2),
    two_adicity=GOLDILOCKS_TWO_ADICITY,
)

GOLDILOCKS_3 = FieldParams(
    name="Goldilocks³",
    p=GOLDILOCKS_P,
    field_extension_degree=3,
    F=_F(GOLDILOCKS_P, 3),
    two_adicity=GOLDILOCKS_TWO_ADICITY,
)

BABYBEAR_4 = FieldParams(
    name="BabyBear⁴",
    p=BABYBEAR_P,
    field_extension_degree=4,
    F=_F(BABYBEAR_P, 4),
    two_adicity=BABYBEAR_TWO_ADICITY,
)

BABYBEAR_5 = FieldParams(
    name="BabyBear⁵",
    p=BABYBEAR_P,
    field_extension_degree=5,
    F=_F(BABYBEAR_P, 5),
    two_adicity=BABYBEAR_TWO_ADICITY,
)

KOALABEAR_4 = FieldParams(
    name="KoalaBear⁴",
    p=KOALABEAR_P,
    field_extension_degree=4,
    F=_F(KOALABEAR_P, 4),
    two_adicity=KOALABEAR_TWO_ADICITY,
)

M31_6 = FieldParams(
    name="M31⁶",
    p=M31_P,
    field_extension_degree=6,
    F=_F(M31_P, 6),
    two_adicity=32,
)

BN254_1 = FieldParams(
    name="BN254",
    p=BN254_P,
    field_extension_degree=1,
    F=_F(BN254_P, 1),
    two_adicity=BN254_TWO_ADICITY,
)

# Map field strings (as used in TOML configs) to FieldParams
FIELD_MAP = {
    "Goldilocks^2": GOLDILOCKS_2,
    "Goldilocks^3": GOLDILOCKS_3,
    "BabyBear^4": BABYBEAR_4,
    "BabyBear^5": BABYBEAR_5,
    "KoalaBear^4": KOALABEAR_4,
    "M31^6": M31_6,
    "BN254": BN254_1,
}


def parse_field(field_str: str) -> FieldParams:
    """
    Parse a field string from a TOML config into a FieldParams object.
    """
    field = FIELD_MAP.get(field_str)
    if field is None:
        raise ValueError(f"Unknown field: {field_str}")
    return field
