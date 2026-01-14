import pytest

from soundcalc.common.fields import BABYBEAR_4
from soundcalc.pcs.pcs import PCS
from soundcalc.zkvms.circuit import Circuit, CircuitConfig


class DummyPCS(PCS):
    def __init__(self, *, dimension: int, rate: float):
        self._dimension = dimension
        self._rate = rate

    def get_pcs_security_levels(self, regime) -> dict[str, int]:
        # Not needed for this test.
        return {}

    def get_proof_size_bits(self) -> int:
        return 0

    def get_expected_proof_size_bits(self) -> int:
        return 0

    def get_rate(self) -> float:
        return self._rate

    def get_dimension(self) -> int:
        return self._dimension

    def get_parameter_summary(self) -> str:
        return "dummy"


def test_deep_ali_eq11_raises_when_max_combo_too_large():
    # trace_length = 64 => trace_length/2 = 32
    pcs = DummyPCS(dimension=64, rate=1 / 2)

    circuit = Circuit(
        CircuitConfig(
            name="test",
            pcs=pcs,
            field=BABYBEAR_4,
            num_columns=1,
            AIR_max_degree=2,
            max_combo=33,  # violates: 33 > 32
        )
    )

    with pytest.raises(AssertionError, match="max_combo"):
        circuit._get_DEEP_ALI_errors(L_plus=1.0)


def test_deep_ali_eq11_allows_max_combo_at_bound():
    pcs = DummyPCS(dimension=64, rate=1 / 2)

    circuit = Circuit(
        CircuitConfig(
            name="test",
            pcs=pcs,
            field=BABYBEAR_4,
            num_columns=1,
            AIR_max_degree=2,
            max_combo=32,  # ok: 32 <= 32
        )
    )

    levels = circuit._get_DEEP_ALI_errors(L_plus=1.0)
    assert "ALI" in levels
    assert "DEEP" in levels
