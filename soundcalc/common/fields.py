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

    def to_string(self) -> str:
        """
        Returns a human-readable string representing the field,
        """
        return self.name


def _F(p: int, ext_size: int) -> float:
    # Keep as float to match existing zkEVMConfig expectations
    return math.pow(p, ext_size)


# Base fields
GOLDILOCKS_P = (1 << 64) - (1 << 32) + 1
BABYBEAR_P = (1 << 31) - (1 << 27) + 1
KOALABEAR_P = (1 << 31) - (1 << 24) + 1


# Preset extension fields
GOLDILOCKS_2 = FieldParams(
    name="Goldilocks²",
    p=GOLDILOCKS_P,
    field_extension_degree=2,
    F=_F(GOLDILOCKS_P, 2),
)

GOLDILOCKS_3 = FieldParams(
    name="Goldilocks³",
    p=GOLDILOCKS_P,
    field_extension_degree=3,
    F=_F(GOLDILOCKS_P, 3),
)

BABYBEAR_4 = FieldParams(
    name="BabyBear⁴",
    p=BABYBEAR_P,
    field_extension_degree=4,
    F=_F(BABYBEAR_P, 4),
)

BABYBEAR_5 = FieldParams(
    name="BabyBear⁵",
    p=BABYBEAR_P,
    field_extension_degree=5,
    F=_F(BABYBEAR_P, 5),
)

KOALABEAR_4 = FieldParams(
    name="KoalaBear⁴",
    p=KOALABEAR_P,
    field_extension_degree=4,
    F=_F(KOALABEAR_P, 4),
)


def field_element_size_bits(field: FieldParams) -> int:
    """
    Returns the size of a field element in bits.
    """
    return math.ceil(math.log2(field.p)) * field.field_extension_degree


# Map field strings (as used in TOML configs) to FieldParams
FIELD_MAP = {
    "Goldilocks^2": GOLDILOCKS_2,
    "Goldilocks^3": GOLDILOCKS_3,
    "BabyBear^4": BABYBEAR_4,
    "BabyBear^5": BABYBEAR_5,
    "KoalaBear^4": KOALABEAR_4,
}


def parse_field(field_str: str) -> FieldParams:
    """
    Parse a field string from a TOML config into a FieldParams object.
    """
    field = FIELD_MAP.get(field_str)
    if field is None:
        raise ValueError(f"Unknown field: {field_str}")
    return field
