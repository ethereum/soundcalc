import math
from dataclasses import replace

import pytest

from soundcalc.circuits.swirl.calculator import (
    calculate_n_logup_bound,
    calculate_swirl_soundness,
)
from soundcalc.circuits.swirl.proof_size import get_swirl_proof_size_breakdown_bits
from soundcalc.zkvms import openvm2


def test_openvm2_uses_backend_logup_depth_bounds():
    assert calculate_n_logup_bound(4, 100, 1000, 24, 2013265921) == 27
    assert calculate_n_logup_bound(4, 50, 100, 20, 2013265921) == 27
    assert calculate_n_logup_bound(2, 50, 100, 19, 2013265921) == 29


def test_openvm2_security_uses_soundness_bounds_not_smaller_actual_specs():
    circuit = {circuit.get_name(): circuit for circuit in openvm2.load().get_circuits()}["app"]

    bounded_levels = _raw_security_levels(circuit)
    actual_levels = _security_levels_with_actual_specs(circuit)

    assert bounded_levels["stacked_reduction"] < actual_levels["stacked_reduction"]
    assert circuit.get_security_levels()["UDR"]["stacked_reduction"] == math.floor(
        bounded_levels["stacked_reduction"]
    )


def test_openvm2_proof_size_uses_all_optional_airs_present_bounds():
    circuit = {circuit.get_name(): circuit for circuit in openvm2.load().get_circuits()}["app"]

    bounded_breakdown = circuit.get_proof_size_breakdown_bits()
    actual_breakdown = get_swirl_proof_size_breakdown_bits(
        replace(
            circuit._proof_size_config(),
            num_airs=circuit.num_airs,
            max_log_trace_height=circuit.max_log_trace_height,
            num_trace_columns=circuit.num_trace_columns,
            max_interactions_per_air=circuit.max_interactions_per_air,
        )
    )

    assert bounded_breakdown.total_bits() > actual_breakdown.total_bits()
    assert bounded_breakdown.batch_constraint_bits > actual_breakdown.batch_constraint_bits


def test_openvm2_swirl_proof_size_backend_codec_breakdown():
    expected = {
        "app": (214426344, (10952, 194624, 7730208, 271392, 206219168)),
        "leaf": (127050968, (9336, 194624, 548768, 270624, 126027616)),
        "internal_for_leaf": (19604440, (9336, 194624, 541088, 70944, 18788448)),
        "internal_recursive": (19604440, (9336, 194624, 541088, 70944, 18788448)),
        "hook": (10895992, (6040, 194624, 541728, 15904, 10137696)),
        "root": (2217400, (5976, 194624, 542368, 7968, 1466464)),
    }

    for circuit in openvm2.load().get_circuits():
        total_bits, components = expected[circuit.get_name()]
        breakdown = circuit.get_proof_size_breakdown_bits()

        assert not circuit.proof_size_todo
        assert circuit.get_proof_size_bits() == total_bits
        assert breakdown.total_bits() == total_bits
        assert (
            breakdown.preamble_bits,
            breakdown.gkr_bits,
            breakdown.batch_constraint_bits,
            breakdown.stacking_bits,
            breakdown.whir_bits,
        ) == components


def _raw_security_levels(circuit):
    return calculate_swirl_soundness(
        params=circuit.params,
        field=circuit.field,
        whir=circuit.pcs,
        max_num_constraints_per_air=circuit.soundness_max_num_constraints_per_air,
        num_airs=circuit.soundness_num_airs,
        max_log_trace_height=circuit.soundness_max_log_trace_height,
        num_trace_columns=circuit.soundness_num_trace_columns,
        max_interactions_per_air=circuit.soundness_max_interactions_per_air,
    )


def _security_levels_with_actual_specs(circuit):
    return calculate_swirl_soundness(
        params=circuit.params,
        field=circuit.field,
        whir=circuit.pcs,
        max_num_constraints_per_air=circuit.max_num_constraints_per_air,
        num_airs=circuit.num_airs,
        max_log_trace_height=circuit.max_log_trace_height,
        num_trace_columns=circuit.num_trace_columns,
        max_interactions_per_air=circuit.max_interactions_per_air,
    )


def test_openvm2_raw_total_is_computed_minimum():
    for circuit in openvm2.load().get_circuits():
        levels = _raw_security_levels(circuit)
        assert levels["total"] == min(v for k, v in levels.items() if k != "total")


def test_swirl_rejects_pcs_parameter_drift():
    circuit = openvm2.load().get_circuits()[0]
    circuit.pcs.num_queries = [1] * len(circuit.pcs.num_queries)

    with pytest.raises(ValueError, match="num_queries"):
        _raw_security_levels(circuit)


def test_openvm2_reported_security_uses_integer_bits():
    expected = {
        "app": ("UDR", {"total": 100, "whir": 100, "logup": 102}),
        "leaf": ("UDR", {"total": 100, "whir": 100, "zerocheck_sumcheck": 117}),
        "internal_for_leaf": ("JBR", {"total": 100, "whir": 100, "logup": 100}),
        "internal_recursive": ("JBR", {"total": 100, "whir": 100, "logup": 100}),
        "hook": ("JBR", {"total": 100, "whir": 100, "logup": 101}),
        "root": ("JBR", {"total": 100, "whir": 100, "whir_ood_rbr": 100}),
    }

    for circuit in openvm2.load().get_circuits():
        regime, expected_levels = expected[circuit.get_name()]
        levels = circuit.get_security_levels()[regime]
        assert all(isinstance(value, int) for value in levels.values())
        for key, value in expected_levels.items():
            assert levels[key] == value
