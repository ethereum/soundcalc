"""Soundness calculator for the SWIRL proof system.

The SWIRL proof system consists of the following components:
1. LogUp GKR - Fractional sumcheck for interaction constraints
2. ZeroCheck - Batched constraint verification across AIRs
3. Stacked Reduction - Reduces trace evaluations to stacked polynomial evaluations
4. WHIR - Polynomial commitment opening via FRI-like folding

Each component contributes to the overall soundness error, and the total security
is the minimum across all components.

References:
- SWIRL paper: https://openvm.dev/swirl.pdf
- Canonical OpenVM2 soundness calculator:
  https://github.com/openvm-org/stark-backend/blob/develop-v2/crates/stark-backend/src/soundness.rs
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from soundcalc.common.fields import FieldParams
from soundcalc.common.utils import apply_grinding
from soundcalc.pcs.whir import WHIR
from soundcalc.proxgaps.johnson_bound import JohnsonBoundRegime
from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime
from soundcalc.proxgaps.unique_decoding import UniqueDecodingRegime


SWIRL_WHIR_K = 4
SWIRL_QUERY_PHASE_POW_BITS = 20
SWIRL_MAX_CONSTRAINT_DEGREE = 4


@dataclass(frozen=True)
class SWIRLWhirRoundConfig:
    num_queries: int


@dataclass(frozen=True)
class SWIRLWhirConfig:
    k: int
    rounds: list[SWIRLWhirRoundConfig]
    mu_pow_bits: int
    query_phase_pow_bits: int
    folding_pow_bits: int
    explicit_regime: str
    explicit_m: int | None = None

    def choose_regime_for_this_circuit(self, field: FieldParams) -> ProximityGapsRegime:
        """Use the toml config to pick regime for this circuit"""
        if self.explicit_regime == "unique":
            return UniqueDecodingRegime(field)
        if self.explicit_regime == "list":
            if self.explicit_m is None:
                raise ValueError("list-decoding mode requires multiplicity m")
            return JohnsonBoundRegime(field, explicit_m=self.explicit_m)
        raise ValueError(f"Unknown SWIRL explicit_regime: {self.explicit_regime}")


@dataclass(frozen=True)
class SWIRLLogUpSecurityParameters:
    """SWIRL's interaction LogUp bound expressed through the shared error-to-bits path.

    LogUp soundness from α/β sampling.

    - α: Random evaluation point to test whether Σ p(y)/q(y) = 0. If interactions
      are unbalanced, the sum is a non-zero rational function with a bounded number
      of roots. By Schwartz-Zippel, a random α detects this with high probability.
    - β: Random challenge for compressing interaction messages into field elements.
      Degeneracy would allow distinct message tuples to collide.

    Security = |F_ext| - log₂(2 × max_interaction_count) - log_max_message_length + pow_bits

    Reference: Section 4 of docs/Soundness_of_Interactions_via_LogUp.pdf
    """

    max_interaction_count: int
    log_max_message_length: int
    pow_bits: int

    def max_message_length(self) -> int:
        return 1 << self.log_max_message_length

    def get_soundness_error(self, challenge_field_size: int, list_size: float = 1.0) -> float:
        return (
            2.0
            * self.max_interaction_count
            * self.max_message_length()
            / (challenge_field_size * list_size)
        )

    def get_soundness_bits(self, challenge_field_size: int, list_size: float = 1.0) -> float:
        grounded_error = apply_grinding(
            self.get_soundness_error(challenge_field_size, list_size),
            self.pow_bits,
        )
        return -math.log2(grounded_error)


@dataclass(frozen=True)
class SWIRLSystemParams:
    l_skip: int
    n_stack: int
    w_stack: int
    log_blowup: int
    whir: SWIRLWhirConfig
    logup: SWIRLLogUpSecurityParameters
    max_constraint_degree: int

    def log_stacked_height(self) -> int:
        return self.l_skip + self.n_stack


def _challenge_field_bits(field: FieldParams) -> float:
    return field.field_extension_degree * math.log2(field.p)


def calculate_gkr_batching_soundness(challenge_field_bits: float) -> float:
    """GKR batching soundness from μ and λ challenges per layer.

    Each layer samples:
    - μ: Reduces four evaluation claims to two via linear interpolation (degree 1)
    - λ: Batches numerator and denominator claims (degree 1)

    Per-round security = ``|F_ext| - log₂(degree) = |F_ext| - log₂(1) = |F_ext|``.
    """
    # Each μ/λ challenge is a degree-1 polynomial test (linear interpolation)
    return challenge_field_bits


def calculate_constraint_batching_soundness(
    challenge_field_bits: float,
    max_num_constraints_per_air: int,
    num_airs: int,
    log2_list_size: float,
) -> float:
    """Constraint batching soundness via Schwartz-Zippel.

    Two batching levels:

    - λ: Within each AIR, batching n constraints. Error ≤ ``n / |F_ext|``.
    - μ: Across AIRs, batching 3k sum claims (ZeroCheck + LogUp numerator + LogUp
      denominator per AIR). Error ≤ ``3k / |F_ext|``.
    """
    lambda_batching_bits = challenge_field_bits - math.log2(max_num_constraints_per_air)
    # Each AIR contributes 3 sum claims to the batch sumcheck:
    # 1. ZeroCheck (constraint satisfaction)
    # 2. LogUp numerator (p̂(ξ) input layer)
    # 3. LogUp denominator (q̂(ξ) input layer)
    mu_batching_bits = challenge_field_bits - math.log2(3.0 * num_airs)

    return log2_list_size + min(lambda_batching_bits, mu_batching_bits)


def calculate_stacked_reduction_soundness(
    challenge_field_bits: float,
    num_trace_columns: int,
    l_skip: int,
    n_stack: int,
    log2_list_size: float,
) -> float:
    """Stacked reduction soundness.

    Reduces trace evaluations at point r to stacked polynomial evaluations at
    point u.

    Note: Trace heights do not appear directly; polynomial degrees are determined
    by the stacking structure (``l_skip``, ``n_stack``), not individual trace
    heights.

    Error sources:

    1. **λ batching**: 2 claims per column (``T(r)`` and ``T_rot(r)``).
       Error = ``2n / |F_ext|``.
    2. **Univariate round**: Degree ``2×(2^l_skip - 1)``.
       Per-round error = ``degree / |F_ext|``.
    3. **Multilinear rounds**: ``n_stack`` rounds, each with degree 2.
       Per-round error = ``2 / |F_ext|``.
    """
    batching_bits = challenge_field_bits - math.log2(2.0 * num_trace_columns)

    univariate_degree = 2 * ((1 << l_skip) - 1)
    univariate_bits = challenge_field_bits - math.log2(univariate_degree)

    # Degree 2 per round => log2(2) = 1.
    multilinear_bits = challenge_field_bits - 1.0

    return log2_list_size + min(batching_bits, univariate_bits, multilinear_bits)


def calculate_zerocheck_sumcheck_soundness(
    challenge_field_bits: float,
    max_constraint_degree: int,
    l_skip: int,
    max_log_trace_height: int,
    log2_list_size: float,
) -> float:
    """ZeroCheck sumcheck soundness (per-round).

    Two phases with different per-round degrees:

    1. Univariate round over coset domain (size ``2^l_skip``):
       - Degree: ``(max_constraint_degree + 1) × (2^l_skip - 1)``

    2. Multilinear rounds (``n_max = max_log_trace_height - l_skip``):
       - Per-round degree: ``max_constraint_degree + 1``

    3. Polynomial identity testing at r: After sumcheck completes, trace
       polynomials are evaluated at random r. If the prover's trace differs from
       the committed trace, this is caught by Schwartz-Zippel. Trace polynomials
       have ``deg_Z ≤ 2^l_skip - 1`` and ``deg_{X_i} ≤ 1``.
       Error ≤ ``(2^l_skip - 1 + n_max) / |F_ext|``.
    """
    univariate_degree = (max_constraint_degree + 1) * ((1 << l_skip) - 1)
    multilinear_degree = max_constraint_degree + 1

    worst_degree = max(univariate_degree, multilinear_degree)
    sumcheck_bits = challenge_field_bits - math.log2(worst_degree)

    # Polynomial identity testing: trace polynomial has deg_Z ≤ 2^l_skip - 1,
    # deg_{X_i} ≤ 1. n_max = max_log_trace_height - l_skip multilinear variables.
    n_max = max(max_log_trace_height - l_skip, 0)
    poly_degree_sum = ((1 << l_skip) - 1) + n_max
    poly_identity_bits = challenge_field_bits - math.log2(poly_degree_sum)

    return log2_list_size + min(sumcheck_bits, poly_identity_bits)


def build_swirl_system_params(
    *,
    l_skip: int,
    n_stack: int,
    w_stack: int,
    log_blowup: int,
    folding_pow_bits: int,
    mu_pow_bits: int,
    explicit_regime: str,
    explicit_m: int | None,
    num_queries: list[int],
    logup: SWIRLLogUpSecurityParameters,
) -> SWIRLSystemParams:
    rounds = [SWIRLWhirRoundConfig(num_queries=n) for n in num_queries]

    return SWIRLSystemParams(
        l_skip=l_skip,
        n_stack=n_stack,
        w_stack=w_stack,
        log_blowup=log_blowup,
        whir=SWIRLWhirConfig(
            k=SWIRL_WHIR_K,
            rounds=rounds,
            mu_pow_bits=mu_pow_bits,
            query_phase_pow_bits=SWIRL_QUERY_PHASE_POW_BITS,
            folding_pow_bits=folding_pow_bits,
            explicit_regime=explicit_regime,
            explicit_m=explicit_m,
        ),
        logup=logup,
        max_constraint_degree=SWIRL_MAX_CONSTRAINT_DEGREE,
    )


def calculate_swirl_soundness(
    *,
    params: SWIRLSystemParams,
    field: FieldParams,
    whir: WHIR,
    max_num_constraints_per_air: int,
    num_airs: int,
    max_log_trace_height: int,
    num_trace_columns: int,
    max_interactions_per_air: int,
) -> dict[str, float]:
    """Calculates soundness for the given system parameters.

    Args:
        params: System parameters including WHIR config and LogUp parameters.
        field: Field parameters. The challenge field bits are derived as
            ``field_extension_degree * log2(p)`` (e.g. BabyBear4 ≈ 124 bits).
        whir: The WHIR PCS instance used for polynomial commitments.
        max_num_constraints_per_air: Maximum constraints in any single AIR.
        num_airs: Number of AIRs being batched.
        max_log_trace_height: Maximum log₂(trace height) across all AIRs.
        num_trace_columns: Total columns batched in stacked reduction.
        max_interactions_per_air: Maximum number of interactions in any single AIR
            (used by LogUp-related checks).

    The maximum constraint degree and number of stacked columns are taken from
    ``params`` / ``whir`` respectively.
    """
    challenge_field_bits = _challenge_field_bits(field)
    regime = params.whir.choose_regime_for_this_circuit(field)

    # Delegate all WHIR soundness analysis to the WHIR module
    pcs_security_levels = whir.get_pcs_security_levels(regime)

    # List size of the initial WHIR code, used by SWIRL-side bounds below.
    initial_list_size = regime.get_max_list_size(whir.get_rate(), whir.get_dimension())
    log2_list_size = math.log2(initial_list_size)

    # Get security for the LogUp argument
    logup_bits = params.logup.get_soundness_bits(
        field.F,
        initial_list_size,
    )

    # GKR sumcheck soundness (per-round).
    #
    # The GKR protocol has a triangular sumcheck structure where round j has j
    # sub-rounds. Each sub-round uses degree-3 interpolation, giving per-round
    # error = 3 / |F_ext|.
    #
    # Security is determined by the worst round: |F_ext| - log₂(3)
    gkr_sumcheck_bits = challenge_field_bits - math.log2(3.0)

    gkr_batching_bits = calculate_gkr_batching_soundness(challenge_field_bits)

    zerocheck_bits = calculate_zerocheck_sumcheck_soundness(
        challenge_field_bits,
        params.max_constraint_degree,
        params.l_skip,
        max_log_trace_height,
        log2_list_size,
    )

    constraint_batching_bits = calculate_constraint_batching_soundness(
        challenge_field_bits,
        max_num_constraints_per_air,
        num_airs,
        log2_list_size,
    )

    stacked_reduction_bits = calculate_stacked_reduction_soundness(
        challenge_field_bits,
        num_trace_columns,
        params.l_skip,
        params.n_stack,
        log2_list_size,
    )

    swirl_levels: dict[str, float] = {
        "logup": logup_bits,
        "gkr_sumcheck": gkr_sumcheck_bits,
        "gkr_batching": gkr_batching_bits,
        "zerocheck_sumcheck": zerocheck_bits,
        "constraint_batching": constraint_batching_bits,
        "stacked_reduction": stacked_reduction_bits,
    }
    levels: dict[str, float] = pcs_security_levels | swirl_levels
    levels["total"] = min(levels.values())
    return levels
