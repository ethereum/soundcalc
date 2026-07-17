from __future__ import annotations

import math
from dataclasses import dataclass

from soundcalc.circuits.swirl.calculator import (
    SWIRLSystemParams,
    calculate_n_logup_bound,
)
from soundcalc.common.fields import FieldParams
from soundcalc.pcs.whir import WHIR


USIZE_BITS = 32
U8_BITS = 8
# OpenVM backend proof construction: common main is one commitment, and the
# VM has one cached trace commitment and no preprocessed trace commitment.
OPENVM_NUM_COMMITS = 2
OPENVM_NUM_CACHED_COMMITMENTS = 1


@dataclass(frozen=True)
class SWIRLProofSizeConfig:
    params: SWIRLSystemParams
    field: FieldParams
    whir: WHIR
    hash_size_bits: int
    num_airs: int
    max_log_trace_height: int
    num_trace_columns: int
    max_interactions_per_air: int
    num_public_values: int = 0


@dataclass(frozen=True)
class SWIRLProofSizeBreakdown:
    preamble_bits: int
    gkr_bits: int
    batch_constraint_bits: int
    stacking_bits: int
    whir_bits: int

    def total_bits(self) -> int:
        return (
            self.preamble_bits
            + self.gkr_bits
            + self.batch_constraint_bits
            + self.stacking_bits
            + self.whir_bits
        )


def _base_field_codec_bits(field: FieldParams) -> int:
    return 8 * math.ceil(field.base_field_element_size_bits() / 8)


def _extension_field_codec_bits(field: FieldParams) -> int:
    return _base_field_codec_bits(field) * field.field_extension_degree


def _vec_bits(length: int, element_bits: int) -> int:
    return USIZE_BITS + length * element_bits


def _round0_univariate_len(l_skip: int, degree: int) -> int:
    return degree * ((1 << l_skip) - 1) + 1


def _num_opening_parts(config: SWIRLProofSizeConfig) -> int:
    return config.num_airs + OPENVM_NUM_COMMITS - 1


def _num_column_openings(config: SWIRLProofSizeConfig) -> int:
    return 2 * config.num_trace_columns


def _validate(config: SWIRLProofSizeConfig) -> None:
    num_opening_parts = _num_opening_parts(config)
    num_column_openings = _num_column_openings(config)

    if config.num_airs < 1:
        raise ValueError("SWIRL proof-size config must have at least one AIR")
    if num_opening_parts < config.num_airs:
        raise ValueError("SWIRL proof-size opening parts must cover every present AIR")
    if num_column_openings < config.num_trace_columns:
        raise ValueError("SWIRL proof-size column openings cannot be smaller than trace columns")
    if config.params.w_stack < 1:
        raise ValueError("SWIRL proof-size w_stack must be positive")
    if config.params.log_stacked_height() != config.whir.log_degree:
        raise ValueError("SWIRL proof-size WHIR log degree does not match system params")
    if config.whir.batch_size != config.params.w_stack:
        raise ValueError("SWIRL proof-size WHIR batch size does not match w_stack")


def get_swirl_proof_size_breakdown_bits(
    config: SWIRLProofSizeConfig,
) -> SWIRLProofSizeBreakdown:
    """Return the OpenVM backend codec size for a SWIRL proof.

    The structure follows `stark-backend/src/proof.rs`. This counts encoded bytes,
    not field-capacity bits: BabyBear base elements are encoded as 32-bit words.
    """
    _validate(config)

    base_bits = _base_field_codec_bits(config.field)
    ext_bits = _extension_field_codec_bits(config.field)
    digest_bits = config.hash_size_bits

    preamble_bits = _preamble_bits(config, base_bits, digest_bits)
    gkr_bits = _gkr_bits(config, base_bits, ext_bits)
    batch_constraint_bits = _batch_constraint_bits(config, ext_bits)
    stacking_bits = _stacking_bits(config, ext_bits)
    whir_bits = _whir_bits(config, base_bits, ext_bits, digest_bits)

    return SWIRLProofSizeBreakdown(
        preamble_bits=preamble_bits,
        gkr_bits=gkr_bits,
        batch_constraint_bits=batch_constraint_bits,
        stacking_bits=stacking_bits,
        whir_bits=whir_bits,
    )


def get_swirl_proof_size_bits(config: SWIRLProofSizeConfig) -> int:
    return get_swirl_proof_size_breakdown_bits(config).total_bits()


def _preamble_bits(
    config: SWIRLProofSizeConfig,
    base_bits: int,
    digest_bits: int,
) -> int:
    bits = 0
    bits += USIZE_BITS  # CODEC_VERSION u32
    bits += digest_bits  # common_main_commit

    bits += USIZE_BITS  # num_airs
    bits += math.ceil(config.num_airs / 8) * U8_BITS  # trace_vdata bitmap

    # Present TraceVData entries: log_height and cached_commitments Vec.
    bits += config.num_airs * (USIZE_BITS + USIZE_BITS)
    bits += OPENVM_NUM_CACHED_COMMITMENTS * digest_bits

    # public_values: outer Vec length plus one base-field Vec per AIR.
    bits += USIZE_BITS
    bits += config.num_airs * USIZE_BITS
    bits += config.num_public_values * base_bits
    return bits


def _gkr_bits(
    config: SWIRLProofSizeConfig,
    base_bits: int,
    ext_bits: int,
) -> int:
    bits = 0
    bits += base_bits  # logup_pow_witness
    bits += ext_bits  # q0_claim

    total_interactions_nonzero = (
        config.num_airs > 0 and config.max_interactions_per_air > 0
    )
    if not total_interactions_nonzero:
        return bits + _vec_bits(0, 4 * ext_bits)

    n_logup = calculate_n_logup_bound(
        config.params.l_skip,
        config.num_airs,
        config.max_interactions_per_air,
        config.max_log_trace_height,
        config.field.p,
    )
    num_gkr_rounds = config.params.l_skip + n_logup

    bits += _vec_bits(num_gkr_rounds, 4 * ext_bits)
    num_sumcheck_arrays = num_gkr_rounds * (num_gkr_rounds - 1) // 2
    bits += num_sumcheck_arrays * 3 * ext_bits
    return bits


def _batch_constraint_bits(
    config: SWIRLProofSizeConfig,
    ext_bits: int,
) -> int:
    n_max = max(0, config.max_log_trace_height - config.params.l_skip)
    univariate_len = _round0_univariate_len(
        config.params.l_skip,
        config.params.max_constraint_degree + 1,
    )
    sumcheck_row_len = config.params.max_constraint_degree + 1

    bits = 0
    bits += _vec_bits(config.num_airs, ext_bits)  # numerator_term_per_air
    bits += config.num_airs * ext_bits  # denominator_term_per_air, implicit length
    bits += _vec_bits(univariate_len, ext_bits)

    bits += USIZE_BITS  # n_max
    if n_max > 0:
        bits += USIZE_BITS  # common nested row length
        bits += n_max * sumcheck_row_len * ext_bits

    bits += config.num_airs * USIZE_BITS  # per-AIR part count
    bits += _num_opening_parts(config) * USIZE_BITS
    bits += _num_column_openings(config) * ext_bits
    return bits


def _stacking_bits(
    config: SWIRLProofSizeConfig,
    ext_bits: int,
) -> int:
    univariate_len = _round0_univariate_len(config.params.l_skip, 2)

    bits = 0
    bits += _vec_bits(univariate_len, ext_bits)
    bits += USIZE_BITS  # sumcheck_round_polys length
    bits += config.params.n_stack * 2 * ext_bits
    bits += USIZE_BITS  # stacking_openings outer length
    bits += OPENVM_NUM_COMMITS * USIZE_BITS
    bits += config.params.w_stack * ext_bits
    return bits


def _whir_bits(
    config: SWIRLProofSizeConfig,
    base_bits: int,
    ext_bits: int,
    digest_bits: int,
) -> int:
    params = config.params
    whir = params.whir
    num_whir_rounds = len(whir.rounds)
    if num_whir_rounds < 1:
        raise ValueError("SWIRL proof-size config must have at least one WHIR round")

    k = whir.k
    block_size = 1 << k
    log_stacked_height = params.log_stacked_height()
    log_final_poly_len = log_stacked_height - num_whir_rounds * k
    if log_final_poly_len < 0:
        raise ValueError("SWIRL proof-size WHIR rounds over-fold the stacked polynomial")

    num_whir_sumcheck_rounds = num_whir_rounds * k
    bits = 0
    bits += base_bits  # mu_pow_witness
    bits += _vec_bits(num_whir_sumcheck_rounds, 2 * ext_bits)
    bits += _vec_bits(num_whir_rounds - 1, digest_bits)  # codeword_commits
    bits += (num_whir_rounds - 1) * ext_bits  # ood_values, implicit length
    bits += num_whir_sumcheck_rounds * base_bits  # folding_pow_witnesses
    bits += num_whir_rounds * base_bits  # query_phase_pow_witnesses

    initial_queries = whir.rounds[0].num_queries
    bits += USIZE_BITS  # num_commits
    bits += USIZE_BITS  # initial_num_whir_queries
    if initial_queries > 0:
        initial_merkle_depth = log_stacked_height + params.log_blowup - k
        if initial_merkle_depth < 0:
            raise ValueError("SWIRL proof-size initial WHIR Merkle depth is negative")
        bits += USIZE_BITS  # initial merkle depth
        bits += OPENVM_NUM_COMMITS * USIZE_BITS  # per-commit widths
        bits += initial_queries * block_size * params.w_stack * base_bits
        bits += OPENVM_NUM_COMMITS * initial_queries * initial_merkle_depth * digest_bits

    for round_idx in range(1, num_whir_rounds):
        num_queries = whir.rounds[round_idx].num_queries
        bits += USIZE_BITS
        bits += num_queries * block_size * ext_bits

    bits += USIZE_BITS  # first non-initial Merkle depth
    for round_idx in range(1, num_whir_rounds):
        num_queries = whir.rounds[round_idx].num_queries
        merkle_depth = log_stacked_height + params.log_blowup - k - round_idx
        if merkle_depth < 0:
            raise ValueError("SWIRL proof-size non-initial WHIR Merkle depth is negative")
        bits += num_queries * merkle_depth * digest_bits

    bits += _vec_bits(1 << log_final_poly_len, ext_bits)
    return bits
