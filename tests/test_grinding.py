# tests/test_grinding.py
"""Tests for grinding parameters: grinding_commit_phase and grinding_deep."""

import pytest

from soundcalc.common.fields import GOLDILOCKS_3
from soundcalc.pcs.fri import FRI, FRIConfig
from soundcalc.proxgaps.johnson_bound import JohnsonBoundRegime
from soundcalc.proxgaps.unique_decoding import UniqueDecodingRegime
from soundcalc.zkvms.circuit import Circuit, CircuitConfig


def _make_fri_config(grinding_commit_phase: int = 0, grinding_query_phase: int = 0) -> FRIConfig:
    """Create a minimal FRI config for testing.

    Domain size D = trace_length / rho = 1024 / 0.5 = 2048
    After folding by [4, 4, 4]: 2048 / 4 / 4 / 4 = 32
    So FRI_early_stop_degree = 32
    """
    return FRIConfig(
        hash_size_bits=256,
        rho=0.5,
        trace_length=1024,
        field=GOLDILOCKS_3,
        batch_size=10,
        power_batching=True,
        num_queries=50,
        FRI_folding_factors=[4, 4, 4],
        FRI_early_stop_degree=32,
        grinding_query_phase=grinding_query_phase,
        grinding_commit_phase=grinding_commit_phase,
    )


@pytest.mark.parametrize("regime_cls", [UniqueDecodingRegime, JohnsonBoundRegime])
def test_grinding_commit_phase_increases_security(regime_cls):
    """Test that grinding_commit_phase increases commit round security bits."""
    fri_no_grind = FRI(_make_fri_config(grinding_commit_phase=0))
    fri_with_grind = FRI(_make_fri_config(grinding_commit_phase=10))

    regime = regime_cls(GOLDILOCKS_3)

    levels_no_grind = fri_no_grind.get_pcs_security_levels(regime)
    levels_with_grind = fri_with_grind.get_pcs_security_levels(regime)

    # Commit rounds should have increased security
    for key in levels_no_grind:
        if key.startswith("commit round"):
            assert levels_with_grind[key] == levels_no_grind[key] + 10, (
                f"{key}: expected {levels_no_grind[key] + 10}, got {levels_with_grind[key]}"
            )

    # Batching and query phase should be unchanged
    assert levels_with_grind["batching"] == levels_no_grind["batching"]
    assert levels_with_grind["query phase"] == levels_no_grind["query phase"]


@pytest.mark.parametrize("regime_cls", [UniqueDecodingRegime, JohnsonBoundRegime])
def test_grinding_deep_increases_security(regime_cls):
    """Test that grinding_deep increases DEEP security bits."""
    pcs = FRI(_make_fri_config())
    regime = regime_cls(GOLDILOCKS_3)

    circuit_no_grind = Circuit(CircuitConfig(
        name="test",
        pcs=pcs,
        field=GOLDILOCKS_3,
        num_constraints=100,
        AIR_max_degree=3,
        max_combo=3,
        grinding_deep=0,
    ))

    circuit_with_grind = Circuit(CircuitConfig(
        name="test",
        pcs=pcs,
        field=GOLDILOCKS_3,
        num_constraints=100,
        AIR_max_degree=3,
        max_combo=3,
        grinding_deep=10,
    ))

    list_size = regime.get_max_list_size(pcs.get_rate(), pcs.get_dimension())

    levels_no_grind = circuit_no_grind._get_DEEP_ALI_errors(list_size, regime)
    levels_with_grind = circuit_with_grind._get_DEEP_ALI_errors(list_size, regime)

    # DEEP should have increased security by 10 bits
    assert levels_with_grind["DEEP"] == levels_no_grind["DEEP"] + 10, (
        f"DEEP: expected {levels_no_grind['DEEP'] + 10}, got {levels_with_grind['DEEP']}"
    )

    # ALI should be unchanged
    assert levels_with_grind["ALI"] == levels_no_grind["ALI"]


def test_grinding_commit_phase_default_zero():
    """Test that grinding_commit_phase defaults to 0."""
    config = FRIConfig(
        hash_size_bits=256,
        rho=0.5,
        trace_length=1024,
        field=GOLDILOCKS_3,
        batch_size=10,
        power_batching=True,
        num_queries=50,
        FRI_folding_factors=[4, 4, 4],
        FRI_early_stop_degree=8,
        grinding_query_phase=0,
    )
    assert config.grinding_commit_phase == 0


def test_grinding_deep_default_zero():
    """Test that grinding_deep defaults to 0."""
    pcs = FRI(_make_fri_config())
    config = CircuitConfig(
        name="test",
        pcs=pcs,
        field=GOLDILOCKS_3,
    )
    assert config.grinding_deep == 0

    circuit = Circuit(config)
    assert circuit.grinding_deep == 0
