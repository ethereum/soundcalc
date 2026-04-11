from __future__ import annotations

import math
from dataclasses import dataclass

from soundcalc.common.fields import FieldParams
from soundcalc.common.utils import apply_grinding
from soundcalc.pcs.whir import WHIR
from soundcalc.proxgaps.johnson_bound import JohnsonBoundRegime
from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime


SWIRL_SECURITY_BITS_TARGET = 100
SWIRL_WHIR_K = 4
SWIRL_WHIR_MAX_LOG_FINAL_POLY_LEN = 10
SWIRL_QUERY_PHASE_POW_BITS = 20
SWIRL_MAX_CONSTRAINT_DEGREE = 4


@dataclass(frozen=True)
class SWIRLWhirRoundConfig:
    num_queries: int


@dataclass(frozen=True)
class SWIRLWhirProximityMode:
    kind: str
    m: int | None = None

    def build_regime(self, field: FieldParams) -> ProximityGapsRegime:
        if self.kind == "unique":
            return SWIRLUniqueDecodingRegime(field)
        if self.kind == "list":
            if self.m is None:
                raise ValueError("list-decoding mode requires multiplicity m")
            return SWIRLListDecodingRegime(field, self.m)
        raise ValueError(f"Unknown SWIRL proximity mode: {self.kind}")

    def whir_query_security_bits(self, num_queries: int, log_inv_rate: int) -> float:
        rho = 2.0 ** (-log_inv_rate)
        if self.kind == "unique":
            max_agreement = (1.0 + rho) / 2.0
        elif self.kind == "list":
            if self.m is None:
                raise ValueError("list-decoding mode requires multiplicity m")
            max_agreement = math.sqrt(rho * (1.0 + 1.0 / self.m)) + 1e-6
        else:
            raise ValueError(f"Unknown SWIRL proximity mode: {self.kind}")

        max_agreement = max(max_agreement, math.ldexp(1.0, -1022))
        return -(num_queries * math.log2(max_agreement))


@dataclass(frozen=True)
class SWIRLWhirConfig:
    k: int
    rounds: list[SWIRLWhirRoundConfig]
    mu_pow_bits: int
    query_phase_pow_bits: int
    folding_pow_bits: int
    proximity: SWIRLWhirProximityMode


@dataclass(frozen=True)
class SWIRLLogUpSecurityParameters:
    """
    SWIRL's interaction LogUp bound expressed through the shared error-to-bits path.
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


@dataclass(frozen=True)
class SWIRLWhirDetails:
    mu_batching_bits: float
    fold_rbr_bits: float
    proximity_gaps_bits: float
    sumcheck_bits: float
    ood_rbr_bits: float
    shift_rbr_bits: float
    query_bits: float
    gamma_batching_bits: float


@dataclass(frozen=True)
class SWIRLSoundnessResult:
    logup_bits: float
    gkr_sumcheck_bits: float
    gkr_batching_bits: float
    zerocheck_sumcheck_bits: float
    constraint_batching_bits: float
    stacked_reduction_bits: float
    whir_bits: float
    whir_details: SWIRLWhirDetails
    total_bits: float


class SWIRLUniqueDecodingRegime(ProximityGapsRegime):
    """
    SWIRL's unique-decoding WHIR bound uses `n / |F|` for the proximity-gap term.

    This differs from soundcalc's generic UDR MCA bound, so it stays isolated here.
    """

    def identifier(self) -> str:
        return "SWIRL-UDR"

    def get_proximity_parameter(self, rate: float, dimension: int) -> float:
        return (1.0 - rate) / 2.0

    def get_max_list_size(self, rate: float, dimension: int) -> int:
        return 1

    def get_error_powers(self, rate: float, dimension: int, batch_size: int) -> float:
        if batch_size <= 1:
            return 0.0
        return self.get_error_linear(rate, dimension) * (batch_size - 1)

    def get_error_linear(self, rate: float, dimension: int) -> float:
        code_length = dimension / rate
        return code_length / self.field.F

    def get_error_multilinear(self, rate: float, dimension: int, batch_size: int) -> float:
        if batch_size <= 1:
            return 0.0
        return self.get_error_linear(rate, dimension) * math.ceil(math.log2(batch_size))


class SWIRLListDecodingRegime(JohnsonBoundRegime):
    """
    SWIRL uses the default BCHKS25 closed-form `a`-bound with an explicit multiplicity `m`.

    The shared Johnson-bound implementation already contains the default `a`-bound algebra.
    We only override the parts where SWIRL fixes `m` directly and uses `D_Y` as the list-size
    proxy for subsequent soundness terms.
    """

    def __init__(self, field: FieldParams, m: int):
        super().__init__(field)
        self.explicit_m = max(m, 1)

    def identifier(self) -> str:
        return f"SWIRL-LDR(m={self.explicit_m})"

    def get_proximity_parameter(self, rate: float, dimension: int) -> float:
        sqrt_rate = math.sqrt(rate)
        return 1.0 - sqrt_rate - (sqrt_rate / (2.0 * self.explicit_m))

    def get_m(self, rate: float, dimension: int) -> int:
        return self.explicit_m

    def get_max_list_size(self, rate: float, dimension: int) -> float:
        sqrt_rate = math.sqrt(rate)
        return (self.explicit_m + 0.5) / sqrt_rate


def _challenge_field_bits(field: FieldParams) -> float:
    return field.field_extension_degree * math.log2(field.p)


def _log2_add(log2_x: float, log2_y: float) -> float:
    hi, lo = (log2_x, log2_y) if log2_x >= log2_y else (log2_y, log2_x)
    return hi + math.log2(1.0 + (2.0 ** (lo - hi)))


def _combine_security_bits(bits_a: float, bits_b: float) -> float:
    return -_log2_add(-bits_a, -bits_b)


def _n_logup_bound(
    l_skip: int,
    num_airs: int,
    max_interactions_per_air: int,
    max_log_height: int,
    max_interaction_count: int,
) -> int:
    field_bound = math.ceil(math.log2(max_interaction_count)) - l_skip
    param_bound = (
        math.ceil(math.log2(num_airs))
        + math.ceil(math.log2(max_interactions_per_air))
        + max_log_height
        - l_skip
    )
    return min(field_bound, param_bound)


def _whir_sumcheck_security(challenge_field_bits: float, sub_round: int, folding_pow_bits: int) -> float:
    sumcheck_degree = 2.0 if sub_round == 0 else 3.0
    return challenge_field_bits - math.log2(sumcheck_degree) + folding_pow_bits


def _whir_gamma_batching_security(
    challenge_field_bits: float,
    batch_size: int,
    list_size: float,
) -> float:
    return challenge_field_bits - math.log2(batch_size) - math.log2(list_size)


def _whir_ood_security(
    challenge_field_bits: float,
    log_degree_at_round_start: int,
    list_size: float,
) -> float:
    return challenge_field_bits - log_degree_at_round_start + 1.0 - 2.0 * math.log2(list_size)


def build_swirl_system_params(
    *,
    l_skip: int,
    n_stack: int,
    w_stack: int,
    log_blowup: int,
    folding_pow_bits: int,
    mu_pow_bits: int,
    proximity: SWIRLWhirProximityMode,
    logup: SWIRLLogUpSecurityParameters,
    security_bits_target: int = SWIRL_SECURITY_BITS_TARGET,
) -> SWIRLSystemParams:
    protocol_security_level = security_bits_target - SWIRL_QUERY_PHASE_POW_BITS
    log_stacked_height = l_skip + n_stack
    num_rounds = math.ceil(
        max(log_stacked_height - SWIRL_WHIR_MAX_LOG_FINAL_POLY_LEN, 0) / SWIRL_WHIR_K
    )

    rounds: list[SWIRLWhirRoundConfig] = []
    log_inv_rate = log_blowup
    for _round in range(num_rounds):
        per_query_bits = proximity.whir_query_security_bits(1, log_inv_rate)
        num_queries = math.ceil(protocol_security_level / per_query_bits)
        rounds.append(SWIRLWhirRoundConfig(num_queries=num_queries))
        log_inv_rate += SWIRL_WHIR_K - 1

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
            proximity=proximity,
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
) -> SWIRLSoundnessResult:
    challenge_field_bits = _challenge_field_bits(field)
    n_logup = _n_logup_bound(
        params.l_skip,
        num_airs,
        max_interactions_per_air,
        max_log_trace_height,
        params.logup.max_interaction_count,
    )

    regime = params.whir.proximity.build_regime(field)
    mu_batching_bits = -math.log2(whir._get_batching_error(regime))
    initial_list_size = whir._get_list_size_for_iteration_and_round(0, 0, regime)
    log2_list_size = math.log2(initial_list_size)

    logup_bits = params.logup.get_soundness_bits(
        field.F,
        initial_list_size,
    )

    gkr_sumcheck_bits = challenge_field_bits - math.log2(3.0)
    gkr_batching_bits = challenge_field_bits

    univariate_degree = (params.max_constraint_degree + 1) * ((1 << params.l_skip) - 1)
    multilinear_degree = params.max_constraint_degree + 1
    zerocheck_sumcheck_bits = challenge_field_bits - math.log2(max(univariate_degree, multilinear_degree))

    n_max = max_log_trace_height - params.l_skip
    poly_degree_sum = ((1 << params.l_skip) - 1) + n_max
    poly_identity_bits = challenge_field_bits - math.log2(poly_degree_sum)
    zerocheck_bits = log2_list_size + min(zerocheck_sumcheck_bits, poly_identity_bits)

    lambda_batching_bits = challenge_field_bits - math.log2(max_num_constraints_per_air)
    mu_constraint_bits = challenge_field_bits - math.log2(3.0 * num_airs)
    constraint_batching_bits = log2_list_size + min(lambda_batching_bits, mu_constraint_bits)

    stacked_batching_bits = challenge_field_bits - math.log2(2.0 * num_trace_columns)
    stacked_univariate_bits = challenge_field_bits - math.log2(2.0 * ((1 << params.l_skip) - 1))
    stacked_multilinear_bits = challenge_field_bits - 1.0
    stacked_reduction_bits = log2_list_size + min(
        stacked_batching_bits,
        stacked_univariate_bits,
        stacked_multilinear_bits,
    )

    min_query_bits = math.inf
    min_proximity_gaps_bits = math.inf
    min_sumcheck_bits = math.inf
    min_ood_bits = math.inf
    min_gamma_batching_bits = math.inf
    min_fold_rbr_bits = math.inf
    min_shift_rbr_bits = math.inf
    min_whir_bits = mu_batching_bits

    for round_index, round_config in enumerate(params.whir.rounds):
        for sub_round in range(params.whir.k):
            fold_bits = -math.log2(whir._epsilon_fold(round_index, sub_round + 1, regime))
            min_fold_rbr_bits = min(min_fold_rbr_bits, fold_bits)
            min_whir_bits = min(min_whir_bits, fold_bits)

            rate, dimension = whir._get_code_for_iteration_and_round(round_index, sub_round + 1)
            proximity_error = regime.get_error_powers(rate, dimension, 2)
            proximity_bits = -math.log2(proximity_error) + params.whir.folding_pow_bits
            min_proximity_gaps_bits = min(min_proximity_gaps_bits, proximity_bits)

            sumcheck_bits = _whir_sumcheck_security(
                challenge_field_bits,
                sub_round,
                params.whir.folding_pow_bits,
            )
            min_sumcheck_bits = min(min_sumcheck_bits, sumcheck_bits)

        query_bits = (
            params.whir.proximity.whir_query_security_bits(
                round_config.num_queries,
                whir.log_inv_rates[round_index],
            )
            + params.whir.query_phase_pow_bits
        )
        min_query_bits = min(min_query_bits, query_bits)

        next_list_size = whir._get_list_size_for_iteration_and_round(
            round_index,
            params.whir.k,
            regime,
        )
        gamma_batching_bits = _whir_gamma_batching_security(
            challenge_field_bits,
            round_config.num_queries + 1,
            next_list_size,
        )
        min_gamma_batching_bits = min(min_gamma_batching_bits, gamma_batching_bits)

        shift_rbr_bits = _combine_security_bits(query_bits, gamma_batching_bits)
        min_shift_rbr_bits = min(min_shift_rbr_bits, shift_rbr_bits)
        min_whir_bits = min(min_whir_bits, shift_rbr_bits)

        if round_index < whir.num_iterations - 1:
            ood_bits = _whir_ood_security(
                challenge_field_bits,
                whir.log_degrees[round_index + 1],
                next_list_size,
            )
            min_ood_bits = min(min_ood_bits, ood_bits)
            min_whir_bits = min(min_whir_bits, ood_bits)

    whir_details = SWIRLWhirDetails(
        mu_batching_bits=mu_batching_bits,
        fold_rbr_bits=min_fold_rbr_bits,
        proximity_gaps_bits=min_proximity_gaps_bits,
        sumcheck_bits=min_sumcheck_bits,
        ood_rbr_bits=min_ood_bits,
        shift_rbr_bits=min_shift_rbr_bits,
        query_bits=min_query_bits,
        gamma_batching_bits=min_gamma_batching_bits,
    )

    total_bits = min(
        logup_bits,
        gkr_sumcheck_bits,
        gkr_batching_bits,
        zerocheck_bits,
        constraint_batching_bits,
        stacked_reduction_bits,
        min_whir_bits,
    )

    return SWIRLSoundnessResult(
        logup_bits=logup_bits,
        gkr_sumcheck_bits=gkr_sumcheck_bits,
        gkr_batching_bits=gkr_batching_bits,
        zerocheck_sumcheck_bits=zerocheck_bits,
        constraint_batching_bits=constraint_batching_bits,
        stacked_reduction_bits=stacked_reduction_bits,
        whir_bits=min_whir_bits,
        whir_details=whir_details,
        total_bits=total_bits,
    )
