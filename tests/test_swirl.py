import math
from dataclasses import replace

import pytest

from soundcalc.circuits.swirl import SWIRLCircuit
from soundcalc.circuits.swirl.calculator import (
    calculate_n_logup_bound,
    calculate_swirl_soundness,
)
from soundcalc.circuits.swirl.proof_size import get_swirl_proof_size_breakdown_bits
from soundcalc.zkvms import openvm2, pico, zkdtvm_v080
from soundcalc.zkvms.zkvm import zkVM


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


def _swirl_circuits_without_shape_inputs():
    circuits = [
        circuit
        for zkvm in (openvm2.load(), zkdtvm_v080.load())
        for circuit in zkvm.get_circuits()
        if isinstance(circuit, SWIRLCircuit)
    ]
    assert "root_shrink" in {circuit.get_name() for circuit in circuits}
    return circuits


def test_swirl_proof_shape_inputs_default_to_the_bounds_and_the_openvm_layout():
    for circuit in _swirl_circuits_without_shape_inputs():
        config = circuit._proof_size_config()
        if config.max_interactions_per_air > 0:
            num_gkr_rounds = circuit.params.l_skip + calculate_n_logup_bound(
                circuit.params.l_skip,
                config.num_airs,
                config.max_interactions_per_air,
                config.max_log_trace_height,
                circuit.field.p,
            )
        else:
            num_gkr_rounds = 0
        explicit = replace(
            config,
            num_gkr_rounds=num_gkr_rounds,
            num_column_openings=2 * config.num_trace_columns,
            num_opening_parts=config.num_airs + 1,
            num_cached_commitments=1,
            num_commitments=2,
        )
        assert (
            get_swirl_proof_size_breakdown_bits(explicit)
            == circuit.get_proof_size_breakdown_bits()
        ), circuit.get_name()


def _fixed_shape_section(**overrides):
    """A fixed-shape circuit (Pico v3.1.1's whitelist-mode compress layer) with
    the shape of its one proof given exactly; an override of None unsets a key."""
    section = dict(
        protocol_family="SWIRL", name="fixed", l_skip=4, n_stack=16, w_stack=25,
        log_blowup=4, whir_folding_pow_bits=16, whir_mu_pow_bits=18,
        whir_num_queries=[65, 34, 24], explicit_regime="list", explicit_m=2,
        constraint_degree=4, max_constraints_per_air=170, num_airs=21,
        max_log_trace_height=16, num_trace_columns=1409, max_interactions_per_air=34,
        proof_size_num_public_values=119, proof_size_num_gkr_rounds=22,
        proof_size_num_column_openings=1554, proof_size_num_opening_parts=42,
        proof_size_num_cached_commitments=0, proof_size_num_commitments=2,
    )
    section.update(overrides)
    return {key: value for key, value in section.items() if value is not None}


def _load_section(section):
    config = {
        "zkevm": {"name": "fixed", "field": "KoalaBear^5", "hash_size_bits": 256},
        "swirl": {
            "logup_max_interaction_count": 2130706433,
            "logup_log_max_message_length": 7,
            "logup_pow_bits": 18,
        },
    }
    return zkVM._build_circuit_from_section(config, section)


def _breakdown_bytes(breakdown):
    return (
        breakdown.preamble_bits // 8,
        breakdown.gkr_bits // 8,
        breakdown.batch_constraint_bits // 8,
        breakdown.stacking_bits // 8,
        breakdown.whir_bits // 8,
    )


def test_swirl_proof_shape_inputs_price_a_fixed_shape_proof_exactly():
    # Pico's encoder wrote this proof in 299,179 bytes.
    circuit = _load_section(_fixed_shape_section())
    assert _breakdown_bytes(circuit.get_proof_size_breakdown_bits()) == (
        775, 15648, 34908, 1780, 246068,
    )
    assert circuit.get_proof_size_bits() == 299179 * 8


@pytest.mark.parametrize(
    "key, value, deltas",
    [
        # One more layer: its 4 claims and its sumcheck, 22 rounds of 3
        # coefficients (layer i of the GKR proof has i rounds).
        ("proof_size_num_gkr_rounds", 23, {"gkr_bits": (4 + 22 * 3) * 160}),
        ("proof_size_num_column_openings", 1555, {"batch_constraint_bits": 160}),
        ("proof_size_num_opening_parts", 43, {"batch_constraint_bits": 32}),
        ("proof_size_num_cached_commitments", 1, {"preamble_bits": 256}),
        # Its width in stacking and WHIR, and its Merkle paths: 65 initial
        # queries at depth 20 + 4 - 4.
        ("proof_size_num_commitments", 3, {"stacking_bits": 32, "whir_bits": 32 + 65 * 20 * 256}),
    ],
)
def test_swirl_proof_shape_inputs_each_price_their_own_part(key, value, deltas):
    base = _load_section(_fixed_shape_section()).get_proof_size_breakdown_bits()
    changed = _load_section(_fixed_shape_section(**{key: value})).get_proof_size_breakdown_bits()
    parts = ("preamble_bits", "gkr_bits", "batch_constraint_bits", "stacking_bits", "whir_bits")
    for part in parts:
        assert getattr(changed, part) - getattr(base, part) == deltas.get(part, 0), part


def test_swirl_gkr_rounds_default_to_zero_without_interactions():
    unset = _load_section(
        _fixed_shape_section(max_interactions_per_air=0, proof_size_num_gkr_rounds=None)
    )
    zero = _load_section(
        _fixed_shape_section(max_interactions_per_air=0, proof_size_num_gkr_rounds=0)
    )
    assert unset.get_proof_size_breakdown_bits() == zero.get_proof_size_breakdown_bits()
    # The LogUp PoW witness, the q0 claim and an empty layer list.
    assert unset.get_proof_size_breakdown_bits().gkr_bits == 32 + 160 + 32


@pytest.mark.parametrize(
    "overrides, message",
    [
        (
            {"proof_size_num_column_openings": 1408},
            "column openings cannot be smaller than trace columns",
        ),
        (
            {"proof_size_num_column_openings": 2819},
            "column openings cannot exceed two per trace column",
        ),
        ({"proof_size_num_opening_parts": 20}, "opening parts must cover every present AIR"),
        (
            {"proof_size_num_commitments": 0, "proof_size_num_opening_parts": None},
            "must have at least one commitment",
        ),
        ({"proof_size_num_cached_commitments": -1}, "cached commitments cannot be negative"),
        (
            {"proof_size_num_cached_commitments": 2},
            "cached commitments must leave one commitment for common main",
        ),
        ({"proof_size_num_gkr_rounds": -1}, "GKR rounds cannot be negative"),
        # The bound is l_skip + 23 = 27.
        ({"proof_size_num_gkr_rounds": 28}, "GKR rounds cannot exceed the n_logup bound"),
    ],
)
def test_swirl_proof_shape_inputs_are_validated(overrides, message):
    circuit = _load_section(_fixed_shape_section(**overrides))
    with pytest.raises(ValueError, match=message):
        circuit.get_proof_size_bits()


def test_pico_final_proof_is_its_compress_proof_at_its_encoded_size():
    circuits = pico.load().get_circuits()
    final = circuits[-1]
    assert final.get_name() == "compress"
    assert final.get_proof_size_bits() == 299179 * 8
    for circuit in circuits:
        (levels,) = circuit.get_security_levels().values()
        assert levels["total"] >= 128
