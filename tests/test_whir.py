import pytest

from soundcalc.common.fields import FieldParams
from soundcalc.pcs.whir import WHIR, WHIRConfig

# Goldilocks prime: 2^64 - 2^32 + 1
GOLDILOCKS_P = 2**64 - 2**32 + 1


def _field_goldilocks_cubic() -> FieldParams:
    return FieldParams(
        name="Goldilocks^3",
        p=GOLDILOCKS_P,
        field_extension_degree=3,
        F=GOLDILOCKS_P**3,
        two_adicity=32,
    )


def _base_config(*, num_iterations=3, folding_factor=2, gap_to_radius=None) -> WHIRConfig:
    return WHIRConfig(
        hash_size_bits=256,
        log_inv_rate=4,
        num_iterations=num_iterations,
        folding_factor=folding_factor,
        field=_field_goldilocks_cubic(),
        log_degree=10,
        batch_size=1,
        power_batching=True,
        grinding_bits_batching=0,
        constraint_degree=3,
        grinding_bits_folding=[[0] * folding_factor for _ in range(num_iterations)],
        num_queries=[1] * num_iterations,
        grinding_bits_queries=[0] * num_iterations,
        num_ood_samples=[1] * (num_iterations - 1),
        grinding_bits_ood=[0] * (num_iterations - 1),
        gap_to_radius=gap_to_radius,
    )


def test_gap_to_radius_sequence_len_ok():
    cfg = _base_config(
        num_iterations=4,
        folding_factor=2,
        gap_to_radius=[0.01, 0.01, 0.01, 0.01],
    )
    WHIR(cfg)  # should not raise


def test_gap_to_radius_sequence_len_bad_raises_assertion():
    cfg = _base_config(
        num_iterations=4,
        folding_factor=2,
        gap_to_radius=[0.01, 0.01, 0.01],  # too short
    )
    with pytest.raises(
        AssertionError,
        match=r"gap_to_radius must have length == num_iterations",
    ):
        WHIR(cfg)
