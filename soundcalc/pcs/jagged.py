from __future__ import annotations

from dataclasses import dataclass
from math import log2, ceil
from typing import Optional

from soundcalc.common.fields import FieldParams
from soundcalc.common.utils import get_bits_of_security_from_error, get_size_of_merkle_multi_proof_bits, get_size_of_merkle_proof_bits
from soundcalc.pcs.pcs import PCS
from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime
from soundcalc.pcs.fri import FRI


def sumcheck_size_bits(
    degree: int,
    num_variables: int, 
    field_size_bits: int
) -> int:
    return (num_variables * (degree + 2) + 2) * field_size_bits

@dataclass(frozen=True)
class JaggedConfig:
    """
    Configuration for Jagged PCS with FRI (Basefold) as its inner dense PCS.
    """
    # The configuration for the dense PCS
    dense_pcs: FRI

    # The maximum height of the trace.
    trace_height: int

    # The maximum width of the trace.
    trace_width: int

class JaggedPCS(PCS):
    """
    Jagged Polynomial Commitment Scheme.
    """

    def __init__(self, config: JaggedConfig):
        self.dense_pcs = config.dense_pcs
        self.trace_height = config.trace_height
        self.trace_width = config.trace_width

    def get_pcs_security_levels(self, regime: ProximityGapsRegime) -> dict[str, int]:
        """
        Returns PCS-specific security levels for a given regime.
        """
        bits = self.dense_pcs.get_pcs_security_levels(regime)
        bits["reduce to dense PCS"] = get_bits_of_security_from_error(self._get_reduction_error())
        return bits

    def _get_reduction_error(self) -> float:
        """
        Returns the error from the zerocheck evaluation claims to the dense PCS.
        """
        log_trace = ceil(log2(self.dense_pcs.trace_length)) + ceil(log2(self.dense_pcs.batch_size))
        epsilon_RLC = ceil(log2(self.trace_width)) / self.dense_pcs.field.F
        epsilon_jagged_sumcheck = (2 * log_trace) / self.dense_pcs.field.F
        epsilon_jagged_evaluation_sumcheck = (2 * (2 * log_trace + 2)) / self.dense_pcs.field.F
        return epsilon_RLC + epsilon_jagged_sumcheck + epsilon_jagged_evaluation_sumcheck

    def _reduction_proof_size_bits(self) -> int:
        log_trace = ceil(log2(self.dense_pcs.trace_length)) + ceil(log2(self.dense_pcs.batch_size))
        field_bits = self.dense_pcs.field.extension_field_element_size_bits()

        jagged_sumcheck_size = sumcheck_size_bits(
            degree = 2, 
            num_variables = log_trace, 
            field_size_bits = field_bits
        )

        jagged_evaluation_sumcheck_size = sumcheck_size_bits(
            degree = 2,
            num_variables = 2 * log_trace + 2,
            field_size_bits = field_bits        
        )

        return jagged_sumcheck_size + jagged_evaluation_sumcheck_size


    def get_proof_size_bits(self) -> int:
        """
        Returns an estimate for the proof size, given in bits.
        """
        # XXX (BW): note that it is not clear that this is the
        # proof size for every zkEVM we can think of
        # XXX (BW): we should probably also add something for the OOD samples and plookup, lookup etc.
        return self.dense_pcs.get_proof_size_bits() + self._reduction_proof_size_bits()

    def get_expected_proof_size_bits(self) -> int:
        """Returns estimated *expected* proof size in bits."""
        # XXX (BW): note that it is not clear that this is the
        # proof size for every zkEVM we can think of
        # XXX (BW): we should probably also add something for the OOD samples and plookup, lookup etc.
        return self.dense_pcs.get_expected_proof_size_bits() + self._reduction_proof_size_bits()

    def get_rate(self) -> float:
        return self.dense_pcs.get_rate()

    def get_dimension(self) -> int:
        return self.dense_pcs.get_dimension()

    def get_trace_height(self) -> int:
        return self.trace_height
    
    def get_parameter_summary(self) -> str:
        """
        Returns a description of the parameters of the PCS.
        """
        lines = []
        lines.append("")
        lines.append("```")

        params = {
            "hash_size_bits": self.dense_pcs.hash_size_bits,
            "rho": self.dense_pcs.rho,
            "k = -log2(rho)": self.dense_pcs.k,
            "dense_length": self.dense_pcs.trace_length,
            "trace_height": self.trace_height,
            "h = log2(dense_length)": self.dense_pcs.h,
            "domain_size D = dense_length / rho": self.dense_pcs.D,
            "dense_batch_size": self.dense_pcs.batch_size,
            "trace_width": self.trace_width,
            "power_batching": self.dense_pcs.power_batching,
            "multilinear_batching": self.dense_pcs.multilinear_batching,
            "num_queries": self.dense_pcs.num_queries,
            "gap_to_radius": self.dense_pcs.gap_to_radius,
            "FRI_folding_factors": self.dense_pcs.FRI_folding_factors,
            "FRI_early_stop_degree": self.dense_pcs.FRI_early_stop_degree,
            "FRI_rounds_n": self.dense_pcs.FRI_rounds_n,
            "grinding_query_phase": self.dense_pcs.grinding_query_phase,
            "grinding_commit_phase": self.dense_pcs.grinding_commit_phase,
            "field": self.dense_pcs.field.to_string(),
            "field_extension_degree": self.dense_pcs.field_extension_degree,
        }

        key_width = max(len(k) for k in params.keys())
        for k, v in params.items():
            lines.append(f"  {k:<{key_width}} : {v}")

        lines.append("```")
        return "\n".join(lines)
