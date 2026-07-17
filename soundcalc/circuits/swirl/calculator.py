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
from soundcalc.pcs.whir import WHIR


SWIRL_WHIR_K = 4
SWIRL_QUERY_PHASE_POW_BITS = 20


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

    def validate_regime(self) -> None:
        if self.explicit_regime == "unique":
            return
        if self.explicit_regime == "list" and self.explicit_m is not None:
            return
        raise ValueError(f"Unknown SWIRL explicit_regime: {self.explicit_regime}")


@dataclass(frozen=True)
class SWIRLProximityGapSecurity:
    log2_err: float
    log2_list_size: float


@dataclass(frozen=True)
class SWIRLLogUpSecurityParameters:
    """SWIRL's interaction LogUp bound expressed through the shared error-to-bits path.

    LogUp soundness from α/β sampling.

    - α: Random evaluation point to test whether Σ p(y)/q(y) = 0. If interactions
      are unbalanced, the sum is a non-zero rational function with a bounded number
      of roots. By Schwartz-Zippel, a random α detects this with high probability.
    - β: Random challenge for compressing interaction messages into field elements.
      Degeneracy would allow distinct message tuples to collide.

    Security = |F_ext| - log₂(2 × max_interaction_count) - log_max_message_length
        - log₂(L_PCS) + effective_pow_bits

    Reference: Section 4 of docs/Soundness_of_Interactions_via_LogUp.pdf
    """

    max_interaction_count: int
    log_max_message_length: int
    pow_bits: int

    def max_message_length(self) -> int:
        return 1 << self.log_max_message_length

    def get_soundness_error(self, challenge_field_size: float, list_size: float = 1.0) -> float:
        return (
            2.0
            * self.max_interaction_count
            * self.max_message_length()
            * list_size
            / challenge_field_size
        )

    def get_soundness_bits(
        self,
        challenge_field_bits: float,
        base_field_order: float,
        log2_list_size: float,
    ) -> float:
        return (
            challenge_field_bits
            - math.log2(2.0 * self.max_interaction_count)
            - self.log_max_message_length
            - log2_list_size
            + _effective_pow_bits(self.pow_bits, base_field_order)
        )


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


def _validate_whir_matches_params(
    params: SWIRLSystemParams,
    field: FieldParams,
    whir: WHIR,
) -> None:
    num_rounds = len(params.whir.rounds)
    expected_queries = [round_config.num_queries for round_config in params.whir.rounds]
    expected_folding_pow = [
        [params.whir.folding_pow_bits] * params.whir.k
        for _ in params.whir.rounds
    ]

    checks = [
        ("field", whir.field, field),
        ("log_inv_rate", whir.log_inv_rates[0], params.log_blowup),
        ("num_iterations", whir.num_iterations, num_rounds),
        ("folding_factors", whir.folding_factors, [params.whir.k] * num_rounds),
        ("log_degree", whir.log_degree, params.log_stacked_height()),
        ("batch_size", whir.batch_size, params.w_stack),
        ("power_batching", whir.power_batching, True),
        ("grinding_batching_phase", whir.grinding_batching_phase, params.whir.mu_pow_bits),
        ("constraint_degree", whir.constraint_degree, params.max_constraint_degree),
        ("grinding_bits_folding", whir.grinding_bits_folding, expected_folding_pow),
        ("num_queries", whir.num_queries, expected_queries),
        (
            "grinding_bits_queries",
            whir.grinding_bits_queries,
            [params.whir.query_phase_pow_bits] * num_rounds,
        ),
        ("num_ood_samples", whir.num_ood_samples, [1] * max(num_rounds - 1, 0)),
        ("grinding_bits_ood", whir.grinding_bits_ood, [0] * max(num_rounds - 1, 0)),
    ]

    for name, actual, expected in checks:
        if actual != expected:
            raise ValueError(
                f"SWIRL WHIR PCS mismatch for {name}: expected {expected!r}, got {actual!r}"
            )


def _log2_add(log2_x: float, log2_y: float) -> float:
    """Numerically stable log2(2^x + 2^y)."""
    if math.isinf(log2_x) and log2_x > 0:
        return log2_x
    if math.isinf(log2_y) and log2_y > 0:
        return log2_y
    if math.isnan(log2_x) or math.isnan(log2_y):
        return math.nan

    hi, lo = (log2_x, log2_y) if log2_x >= log2_y else (log2_y, log2_x)
    return hi + math.log2(1.0 + 2.0 ** (lo - hi))


def _combine_security_bits(bits_a: float, bits_b: float) -> float:
    """Combine additive errors 2^-a + 2^-b into security bits."""
    if math.isinf(bits_a) and bits_a > 0:
        return bits_b
    if math.isinf(bits_b) and bits_b > 0:
        return bits_a
    if math.isnan(bits_a) or math.isnan(bits_b):
        return math.nan
    return -_log2_add(-bits_a, -bits_b)


def _sample_bits_residue_probs(
    num_sampled_bits: float,
    base_field_order: float,
) -> tuple[float, float, float]:
    two_pow_n = 2.0 ** num_sampled_bits
    c = math.floor(base_field_order / two_pow_n)
    r = base_field_order - c * two_pow_n
    return ((c + 1.0) / base_field_order, c / base_field_order, r)


def _effective_pow_bits(pow_bits: int, base_field_order: float) -> float:
    if pow_bits == 0:
        return 0.0
    p_hi, _, _ = _sample_bits_residue_probs(float(pow_bits), base_field_order)
    return -math.log2(p_hi)


def _max_agreement(explicit_regime: str, explicit_m: int | None, log_inv_rate: int) -> float:
    rho = 2.0 ** (-log_inv_rate)
    if explicit_regime == "unique":
        max_agreement = (1.0 + rho) / 2.0
    elif explicit_regime == "list":
        if explicit_m is None:
            raise ValueError("list-decoding mode requires multiplicity m")
        m = max(explicit_m, 1)
        max_agreement = math.sqrt(rho) * (1.0 + 1.0 / (2.0 * m))
    else:
        raise ValueError(f"Unknown SWIRL explicit_regime: {explicit_regime}")
    return min(max_agreement, 1.0)


def _bchks25_log2_a_from_log2_degrees(
    log2_d_x: float,
    log2_d_y: float,
    log2_d_z: float,
    log2_agreement_term: float,
) -> float:
    log2_term_poly = 1.0 + log2_d_x + 2.0 * log2_d_y + log2_d_z
    log2_term_gamma = log2_d_y + log2_agreement_term
    return _log2_add(log2_term_poly, log2_term_gamma)


def _bchks25_reference_log2_degrees(
    log_degree: int,
    log_inv_rate: int,
    m: int,
) -> tuple[float, float, float]:
    m_bar = max(m, 1) + 0.5
    log2_m_bar = math.log2(m_bar)
    log2_n = log_degree + log_inv_rate
    log2_rho = -float(log_inv_rate)

    log2_d_x = log2_m_bar + log2_n + 0.5 * log2_rho
    log2_d_y = log2_m_bar - 0.5 * log2_rho
    log2_d_z = 2.0 * log2_m_bar - math.log2(3.0) - log2_rho
    log2_d_z = max(log2_d_y, log2_d_z)
    return log2_d_x, log2_d_y, log2_d_z


def _log2_a_bound_bchks25(log_degree: int, log_inv_rate: int, m: int) -> tuple[float, float]:
    m_eff = max(m, 1)
    rho = 2.0 ** (-log_inv_rate)
    if rho <= 0.0 or not math.isfinite(rho):
        return math.inf, math.inf
    if m_eff == 1 and rho >= 4.0 / 9.0:
        return math.inf, math.inf

    sqrt_rho = math.sqrt(rho)
    eta = sqrt_rho / (2.0 * m_eff)
    gamma = 1.0 - sqrt_rho - eta
    if eta <= 0.0 or gamma <= 0.0 or gamma >= 1.0 - sqrt_rho:
        return math.inf, math.inf

    log2_n = log_degree + log_inv_rate
    log2_d_x, log2_d_y, log2_d_z = _bchks25_reference_log2_degrees(
        log_degree,
        log_inv_rate,
        m_eff,
    )
    log2_gamma_n_plus_1 = _log2_add(math.log2(gamma) + log2_n, 0.0)
    log2_a_real = _bchks25_log2_a_from_log2_degrees(
        log2_d_x,
        log2_d_y,
        log2_d_z,
        log2_gamma_n_plus_1,
    )
    if not math.isfinite(log2_a_real):
        return math.inf, math.inf

    log2_a_real = max(log2_a_real, 0.0)
    a_bound = math.ceil(2.0 ** log2_a_real)
    return math.log2(max(a_bound, 1)), log2_d_y


def _whir_proximity_gap_security(
    explicit_regime: str,
    explicit_m: int | None,
    challenge_field_bits: float,
    log_degree: int,
    log_inv_rate: int,
    batch_size: int,
) -> SWIRLProximityGapSecurity:
    assert batch_size > 1, "batch_size must be > 1 for err*"
    if explicit_regime == "unique":
        return SWIRLProximityGapSecurity(
            log2_err=challenge_field_bits
            - math.log2(batch_size - 1)
            - log_degree
            - log_inv_rate,
            log2_list_size=0.0,
        )
    if explicit_regime == "list":
        if explicit_m is None:
            raise ValueError("list-decoding mode requires multiplicity m")
        log2_a, log2_list_size = _log2_a_bound_bchks25(
            log_degree,
            log_inv_rate,
            explicit_m,
        )
        return SWIRLProximityGapSecurity(
            log2_err=challenge_field_bits - math.log2(batch_size - 1) - log2_a,
            log2_list_size=log2_list_size,
        )
    raise ValueError(f"Unknown SWIRL explicit_regime: {explicit_regime}")


def _whir_query_security_biased(
    explicit_regime: str,
    explicit_m: int | None,
    num_queries: int,
    log_inv_rate: int,
    log_query_domain: int,
    base_field_order: float,
) -> float:
    alpha = _max_agreement(explicit_regime, explicit_m, log_inv_rate)
    _, _, heavy_residues = _sample_bits_residue_probs(float(log_query_domain), base_field_order)
    domain_size = 2.0 ** log_query_domain
    heavy_used = min(alpha * domain_size, heavy_residues)
    mass = alpha * (1.0 - heavy_residues / base_field_order) + heavy_used / base_field_order
    mass = min(max(mass, 2.0 ** -1074), 1.0)
    return -num_queries * math.log2(mass)


def _whir_sumcheck_security(
    base_field_order: float,
    challenge_field_bits: float,
    folding_pow_bits: int,
    log2_list_size: float,
) -> float:
    sumcheck_degree = 3.0
    return (
        challenge_field_bits
        - math.log2(sumcheck_degree)
        - log2_list_size
        + _effective_pow_bits(folding_pow_bits, base_field_order)
    )


def _whir_ood_security(
    log2_list_size: float,
    challenge_field_bits: float,
    log_degree_at_round_start: int,
) -> float:
    return challenge_field_bits - log_degree_at_round_start + 1.0 - 2.0 * log2_list_size


def _whir_gamma_batching_security(
    challenge_field_bits: float,
    batch_size: int,
    log2_list_size: float,
) -> float:
    assert batch_size > 0, "batch_size must be > 0 for gamma batching"
    return challenge_field_bits - math.log2(batch_size) - log2_list_size


def _calculate_whir_soundness(
    params: SWIRLSystemParams,
    base_field_order: float,
    challenge_field_bits: float,
    num_stacked_columns: int,
) -> dict[str, float]:
    params.whir.validate_regime()
    whir = params.whir
    k_whir = whir.k
    log_stacked_height = params.log_stacked_height()
    num_whir_rounds = len(whir.rounds)

    min_query_bits = math.inf
    min_prox_gaps_bits = math.inf
    min_sumcheck_bits = math.inf
    min_ood_bits = math.inf
    min_gamma_batching_bits = math.inf
    min_fold_rbr_bits = math.inf
    min_shift_rbr_bits = math.inf

    assert num_stacked_columns >= 2, "WHIR requires at least 2 stacked columns for mu batching"
    mu_security = _whir_proximity_gap_security(
        whir.explicit_regime,
        whir.explicit_m,
        challenge_field_bits,
        log_stacked_height,
        params.log_blowup,
        num_stacked_columns,
    )
    mu_batching_bits = mu_security.log2_err + _effective_pow_bits(
        whir.mu_pow_bits,
        base_field_order,
    )
    min_rbr_bits = mu_batching_bits

    log_inv_rate = params.log_blowup
    current_log_degree = log_stacked_height

    for round_index, round_config in enumerate(whir.rounds):
        is_final_round = round_index == num_whir_rounds - 1
        next_rate = log_inv_rate + (k_whir - 1)
        log2_list_size: float | None = None

        for _ in range(k_whir):
            current_log_degree -= 1

            prox_gaps = _whir_proximity_gap_security(
                whir.explicit_regime,
                whir.explicit_m,
                challenge_field_bits,
                current_log_degree,
                log_inv_rate,
                2,
            )
            if log2_list_size is None:
                log2_list_size = prox_gaps.log2_list_size

            prox_gaps_bits = prox_gaps.log2_err + _effective_pow_bits(
                whir.folding_pow_bits,
                base_field_order,
            )
            min_prox_gaps_bits = min(min_prox_gaps_bits, prox_gaps_bits)

            sumcheck_bits = _whir_sumcheck_security(
                base_field_order,
                challenge_field_bits,
                whir.folding_pow_bits,
                log2_list_size,
            )
            min_sumcheck_bits = min(min_sumcheck_bits, sumcheck_bits)

            fold_rbr_bits = _combine_security_bits(sumcheck_bits, prox_gaps_bits)
            min_fold_rbr_bits = min(min_fold_rbr_bits, fold_rbr_bits)
            min_rbr_bits = min(min_rbr_bits, fold_rbr_bits)

        log_query_domain = current_log_degree + log_inv_rate
        query_bits = _whir_query_security_biased(
            whir.explicit_regime,
            whir.explicit_m,
            round_config.num_queries,
            log_inv_rate,
            log_query_domain,
            base_field_order,
        ) + _effective_pow_bits(whir.query_phase_pow_bits, base_field_order)
        min_query_bits = min(min_query_bits, query_bits)

        next_prox_gaps = _whir_proximity_gap_security(
            whir.explicit_regime,
            whir.explicit_m,
            challenge_field_bits,
            current_log_degree,
            next_rate,
            2,
        )
        next_log2_list_size = next_prox_gaps.log2_list_size

        num_ood_samples = 1
        gamma_batching_bits = _whir_gamma_batching_security(
            challenge_field_bits,
            round_config.num_queries + num_ood_samples,
            next_log2_list_size,
        )
        min_gamma_batching_bits = min(min_gamma_batching_bits, gamma_batching_bits)

        shift_rbr_bits = _combine_security_bits(query_bits, gamma_batching_bits)
        min_shift_rbr_bits = min(min_shift_rbr_bits, shift_rbr_bits)
        min_rbr_bits = min(min_rbr_bits, shift_rbr_bits)

        if not is_final_round:
            ood_bits = _whir_ood_security(
                next_log2_list_size,
                challenge_field_bits,
                current_log_degree,
            )
            min_ood_bits = min(min_ood_bits, ood_bits)
            min_rbr_bits = min(min_rbr_bits, ood_bits)

        log_inv_rate = next_rate

    levels = {
        "whir": min_rbr_bits,
        "whir_mu_batching": mu_batching_bits,
        "whir_fold_rbr": min_fold_rbr_bits,
        "whir_proximity_gaps": min_prox_gaps_bits,
        "whir_sumcheck": min_sumcheck_bits,
        "whir_shift_rbr": min_shift_rbr_bits,
        "whir_query": min_query_bits,
        "whir_gamma_batching": min_gamma_batching_bits,
    }
    if math.isfinite(min_ood_bits):
        levels["whir_ood_rbr"] = min_ood_bits
    return levels


def calculate_gkr_batching_soundness(
    challenge_field_bits: float,
) -> float:
    """GKR batching soundness from μ and λ challenges per layer.

    Each layer samples:
    - μ: Reduces four evaluation claims to two via linear interpolation (degree 1)
    - λ: Batches numerator and denominator claims (degree 1)

    Per-round security = ``|F_ext| - log₂(degree) = |F_ext| - log₂(1) = |F_ext|``.
    """
    # Each μ/λ challenge is a degree-1 polynomial test (linear interpolation)
    degree = 1
    # This function is essentially a NOP
    return challenge_field_bits - math.log2(degree)


def calculate_gkr_sumcheck_soundness(
    challenge_field_bits: float,
    l_skip: int,
    n_logup: int,
) -> float:
    """GKR sumcheck soundness (per-round).

    The GKR protocol has a triangular sumcheck structure where round j has j
    sub-rounds. Each sub-round uses degree-3 interpolation, giving per-round
    error = ``3 / |F_ext|``.

    Security is determined by the worst round: ``|F_ext| - log₂(3)``.
    """
    assert l_skip + n_logup >= 1, "GKR requires at least 1 round"
    # Each sub-round has degree 3; security = |F_ext| - log2(degree)
    degree_per_subround = 3
    return challenge_field_bits - math.log2(degree_per_subround)


def calculate_constraint_batching_soundness(
    challenge_field_bits: float,
    max_num_constraints_per_air: int,
    num_airs: int,
    l_skip: int,
    max_log_trace_height: int,
    n_logup: int,
    log2_list_size: float,
) -> float:
    """Fused batch-constraint boundary soundness via Schwartz-Zippel.

    Matches the OpenVM backend's fused boundary and batch-sumcheck batching
    terms, including the PCS list-size union bound.
    """
    assert max_num_constraints_per_air > 0, (
        "batch-constraint soundness requires at least one constraint"
    )
    assert num_airs > 0, "batch-constraint soundness requires at least one nonempty AIR"

    n_trace = max(max_log_trace_height - l_skip, 0)
    n_extra = max(n_trace - n_logup, 0)
    skip_degree = (1 << l_skip) - 1

    fused_boundary_degree = (
        max(n_extra, 3) + skip_degree + (max_num_constraints_per_air - 1)
    )
    batch_sumcheck_batching_degree = 3 * num_airs - 1

    fused_boundary_bits = challenge_field_bits - math.log2(fused_boundary_degree)
    batch_sumcheck_batching_bits = challenge_field_bits - math.log2(
        batch_sumcheck_batching_degree
    )
    return min(fused_boundary_bits, batch_sumcheck_batching_bits) - log2_list_size


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

    return min(batching_bits, univariate_bits, multilinear_bits) - log2_list_size


def calculate_zerocheck_sumcheck_soundness(
    challenge_field_bits: float,
    max_constraint_degree: int,
    l_skip: int,
    log2_list_size: float,
) -> float:
    """ZeroCheck sumcheck soundness (per-round).

    Two phases with different per-round degrees:

    1. Univariate round over coset domain (size ``2^l_skip``):
       - Degree: ``(max_constraint_degree + 1) × (2^l_skip - 1)``

    2. Multilinear rounds (``n_max = max_log_trace_height - l_skip``):
       - Per-round degree: ``max_constraint_degree + 1``

    The fused input-layer boundary is accounted for separately in
    ``calculate_constraint_batching_soundness``.
    """
    univariate_degree = (max_constraint_degree + 1) * ((1 << l_skip) - 1)
    multilinear_degree = max_constraint_degree + 1

    worst_degree = max(univariate_degree, multilinear_degree)
    return challenge_field_bits - math.log2(worst_degree) - log2_list_size


def calculate_n_logup_bound(
    l_skip: int,
    num_airs: int,
    max_interactions_per_air: int,
    max_log_trace_height: int,
    max_interaction_count: int,
) -> int:
    field_bound = math.ceil(math.log2(max_interaction_count)) - l_skip
    param_bound = (
        math.ceil(math.log2(num_airs))
        + math.ceil(math.log2(max_interactions_per_air))
        + max_log_trace_height
        - l_skip
    )
    return max(min(field_bound, param_bound), 0)


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
    max_constraint_degree: int,
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
        max_constraint_degree=max_constraint_degree,
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
    base_field_order = float(field.p)
    _validate_whir_matches_params(params, field, whir)

    initial_prox_gap = _whir_proximity_gap_security(
        params.whir.explicit_regime,
        params.whir.explicit_m,
        challenge_field_bits,
        params.log_stacked_height(),
        params.log_blowup,
        params.w_stack,
    )
    log2_list_size = initial_prox_gap.log2_list_size

    logup_bits = params.logup.get_soundness_bits(
        challenge_field_bits,
        base_field_order,
        log2_list_size,
    )

    n_logup = calculate_n_logup_bound(
        params.l_skip,
        num_airs,
        max_interactions_per_air,
        max_log_trace_height,
        params.logup.max_interaction_count,
    )

    gkr_sumcheck_bits = calculate_gkr_sumcheck_soundness(
        challenge_field_bits,
        params.l_skip,
        n_logup,
    )

    gkr_batching_bits = calculate_gkr_batching_soundness(challenge_field_bits)

    zerocheck_bits = calculate_zerocheck_sumcheck_soundness(
        challenge_field_bits,
        params.max_constraint_degree,
        params.l_skip,
        log2_list_size,
    )

    constraint_batching_bits = calculate_constraint_batching_soundness(
        challenge_field_bits,
        max_num_constraints_per_air,
        num_airs,
        params.l_skip,
        max_log_trace_height,
        n_logup,
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
    whir_levels = _calculate_whir_soundness(
        params,
        base_field_order,
        challenge_field_bits,
        params.w_stack,
    )
    levels: dict[str, float] = whir_levels | swirl_levels
    levels["total"] = min(levels.values())
    return levels
