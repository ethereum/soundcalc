"""
JSON configuration schemas for zkVM loading.

This module contains Pydantic models for deserializing JSON config files.

These are thin schemas - the actual domain logic lives in the VM modules.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

from soundcalc.common.fields import Field

# =============================================================================
# Base Configuration
# =============================================================================


class _Frozen(BaseModel):
    """Base class for all frozen config models."""

    model_config = ConfigDict(frozen=True)


# =============================================================================
# FRI Schemas
# =============================================================================


class FRICircuit(_Frozen):
    """Schema for a single FRI circuit."""

    name: str
    rho: float
    trace_length: int
    air_max_degree: int
    num_columns: int
    opening_points: int
    batch_size: int
    power_batching: bool
    num_queries: int
    fri_folding_factors: list[int]
    fri_early_stop_degree: int
    grinding_query_phase: int = 0


class FRIConfig(_Frozen):
    """Top-level schema for FRI-based VM JSON files."""

    class Header(_Frozen):
        name: str
        protocol_family: Literal["FRI_STARK"]
        field: Field
        hash_size_bits: int = 256

    zkevm: Header
    circuits: list[FRICircuit]

    @classmethod
    def load(cls, path: Path) -> "FRIConfig":
        return cls.model_validate_json(path.read_text())


# =============================================================================
# WHIR Schemas
# =============================================================================


class WHIRCircuit(_Frozen):
    """Schema for a single WHIR circuit."""

    name: str
    log_inv_rate: int
    num_iterations: int
    folding_factor: int
    log_degree: int
    batch_size: int
    power_batching: bool
    constraint_degree: int
    num_queries: list[int]
    num_ood_samples: list[int]
    grinding_bits_batching: int
    grinding_bits_folding: list[list[int]]
    grinding_bits_queries: list[int]
    grinding_bits_ood: list[int]


class WHIRConfig(_Frozen):
    """Top-level schema for WHIR-based VM JSON files."""

    class Header(_Frozen):
        name: str
        protocol_family: Literal["WHIR"]
        field: Field
        hash_size_bits: int = 256

    zkevm: Header
    circuits: list[WHIRCircuit]

    @classmethod
    def load(cls, path: Path) -> "WHIRConfig":
        return cls.model_validate_json(path.read_text())
