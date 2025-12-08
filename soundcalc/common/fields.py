"""
Preset finite fields to be used by the zkEVM configs
"""

from __future__ import annotations

import math
from typing import Annotated, Any, ClassVar

from pydantic import BaseModel, BeforeValidator, ConfigDict, computed_field


class FieldParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    """Human-readable field name (e.g., "Goldilocks²")"""

    p: int
    """Base field characteristic (e.g., p = 2^{31} - 2^{27} + 1)"""

    field_extension_degree: int
    """Extension field degree (e.g., ext_size = 2 for Fp²)"""

    two_adicity: int
    """
    Two-adicity of the multiplicative group (largest s such that 2^s divides p-1)

    This determines the maximum possible FFT domain size.
    """

    # Registry of known fields (populated below)
    _registry: ClassVar[dict[str, FieldParams]] = {}

    @computed_field  # type: ignore[prop-decorator]
    @property
    def F(self) -> float:
        """Extension field size |F| = p^{ext_size}"""
        return math.pow(self.p, self.field_extension_degree)

    def __str__(self) -> str:
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

    @classmethod
    def register(cls, key: str, field: FieldParams) -> FieldParams:
        """Register a field in the global registry."""
        cls._registry[key] = field
        return field

    @classmethod
    def from_name(cls, name: str) -> FieldParams:
        """Look up a field by its config name (e.g., 'Goldilocks^2')."""
        if name not in cls._registry:
            raise ValueError(f"Unknown field: {name}. Valid: {list(cls._registry)}")
        return cls._registry[name]


_GOLDILOCKS = (p := (1 << 64) - (1 << 32) + 1, 32)
"""
Goldilocks prime: p = 2^64 - 2^32 + 1
Two-adicity: p - 1 = 2^32 * (2^32 - 1), so 32 is the max power of 2
"""

_BABYBEAR = (p := (1 << 31) - (1 << 27) + 1, 27)
"""
BabyBear prime: p = 2^31 - 2^27 + 1
Two-adicity: p - 1 = 2^27 * (2^4 - 1), so 27 is the max power of 2
"""


def _field(name: str, base: tuple[int, int], ext: int, key: str) -> FieldParams:
    """Helper to create and register a field."""
    return FieldParams.register(
        key,
        FieldParams(
            name=name, p=base[0], field_extension_degree=ext, two_adicity=base[1]
        ),
    )


GOLDILOCKS_2 = _field("Goldilocks²", _GOLDILOCKS, 2, "Goldilocks^2")
GOLDILOCKS_3 = _field("Goldilocks³", _GOLDILOCKS, 3, "Goldilocks^3")
BABYBEAR_4 = _field("BabyBear⁴", _BABYBEAR, 4, "BabyBear^4")
BABYBEAR_5 = _field("BabyBear⁵", _BABYBEAR, 5, "BabyBear^5")


def _validate_field(v: Any) -> FieldParams:
    """Pydantic validator: parse field string or pass through FieldParams."""
    if isinstance(v, FieldParams):
        return v
    if isinstance(v, str):
        return FieldParams.from_name(v)
    raise TypeError(f"Expected str or FieldParams, got {type(v).__name__}")


Field = Annotated[FieldParams, BeforeValidator(_validate_field)]
"""Type annotation for automatic field parsing in Pydantic models."""
