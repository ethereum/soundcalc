import math
import pytest

from soundcalc.common.fields import BABYBEAR_4
from soundcalc.pcs.pcs import PCS
from soundcalc.zkvms.circuit import Circuit, CircuitConfig
from soundcalc.proxgaps.johnson_bound import JohnsonBoundRegime
from soundcalc.proxgaps.unique_decoding import UniqueDecodingRegime


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


def _multipoint_rhs(*, pcs: PCS, regime) -> float:
    """
    Compute RHS = (1 - θ)·n for the multi-point condition:
        k + m_max < (1 - θ)·n
    """
    k = pcs.get_dimension()
    rate = pcs.get_rate()
    n = k / rate
    theta = regime.get_proximity_parameter(rate, k)
    return (1.0 - theta) * n


def _max_combo_at_bound(*, pcs: PCS, regime) -> int:
    """
    Largest integer m such that k + m < (1 - θ)·n.
    """
    k = pcs.get_dimension()
    rhs = _multipoint_rhs(pcs=pcs, regime=regime)

    # strict inequality: m < rhs - k
    eps = 1e-12
    return max(0, math.floor(rhs - k - eps))


@pytest.mark.parametrize("regime_cls", [UniqueDecodingRegime, JohnsonBoundRegime])
def test_deep_ali_multipoint_raises_when_max_combo_too_large(regime_cls):
    pcs = DummyPCS(dimension=64, rate=1 / 2)
    regime = regime_cls(BABYBEAR_4)

    m_ok = _max_combo_at_bound(pcs=pcs, regime=regime)
    m_bad = m_ok + 1

    circuit = Circuit(
        CircuitConfig(
            name="test",
            pcs=pcs,
            field=BABYBEAR_4,
            num_constraints=1,
            AIR_max_degree=2,
            max_combo=m_bad,
        )
    )

    with pytest.raises(AssertionError, match="multi-point condition"):
        circuit._get_DEEP_ALI_errors(L_plus=1.0, regime=regime)


@pytest.mark.parametrize("regime_cls", [UniqueDecodingRegime, JohnsonBoundRegime])
def test_deep_ali_multipoint_allows_max_combo_at_bound(regime_cls):
    pcs = DummyPCS(dimension=64, rate=1 / 2)
    regime = regime_cls(BABYBEAR_4)

    m_ok = _max_combo_at_bound(pcs=pcs, regime=regime)

    circuit = Circuit(
        CircuitConfig(
            name="test",
            pcs=pcs,
            field=BABYBEAR_4,
            num_constraints=1,
            AIR_max_degree=2,
            max_combo=m_ok,
        )
    )

    levels = circuit._get_DEEP_ALI_errors(L_plus=1.0, regime=regime)
    assert "ALI" in levels
    assert "DEEP" in levels
