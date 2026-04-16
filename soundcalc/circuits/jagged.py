from __future__ import annotations

from dataclasses import dataclass
from math import log2, ceil

from soundcalc.circuits.circuit import Circuit
from soundcalc.common.fields import FieldParams
from soundcalc.common.utils import get_bits_of_security_from_error
from soundcalc.lookups.logup import LogUp
from soundcalc.pcs.pcs import PCS
from soundcalc.pcs.fri import FRI
from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime
from soundcalc.proxgaps.unique_decoding import UniqueDecodingRegime


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
    trace_length: int

    # The maximum width of the trace.
    trace_width: int

class JaggedPCS(PCS):
    """
    Jagged Polynomial Commitment Scheme.
    """

    label = "Jagged"

    def __init__(self, config: JaggedConfig):
        self.dense_pcs = config.dense_pcs
        self.trace_length = config.trace_length
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
        return self.dense_pcs.get_proof_size_bits() + self._reduction_proof_size_bits()

    def get_expected_proof_size_bits(self) -> int:
        """Returns estimated *expected* proof size in bits."""
        return self.dense_pcs.get_expected_proof_size_bits() + self._reduction_proof_size_bits()

    def get_rate(self) -> float:
        return self.dense_pcs.get_rate()

    def get_dimension(self) -> int:
        return self.dense_pcs.get_dimension()

    def get_trace_length(self) -> int:
        return self.trace_length

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
            "trace_length": self.trace_length,
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

    def get_report_parameter_lines(self) -> list[str]:
        return self.dense_pcs.get_report_parameter_lines()


@dataclass(frozen=True)
class JaggedCircuitConfig:
    """Configuration for a JaggedCircuit."""
    name: str
    dense_pcs: FRI
    field: FieldParams
    trace_length: int
    trace_width: int
    num_constraints: int
    AIR_max_degree: int
    lookups: list[LogUp] | None = None


class JaggedCircuit(Circuit):
    """
    Circuit using the Jagged proof system over FRI.

    Jagged adds a sumcheck-based reduction layer on top of a dense FRI PCS,
    plus a multilinear zerocheck for constraint satisfaction.
    Used by SP1.
    """

    def __init__(self, config: JaggedCircuitConfig):
        self.name = config.name
        self.field = config.field
        self.protocol_label = "Jagged + FRI"
        self._jagged_pcs = JaggedPCS(JaggedConfig(
            dense_pcs=config.dense_pcs,
            trace_length=config.trace_length,
            trace_width=config.trace_width,
        ))
        self.pcs = self._jagged_pcs
        self.num_constraints = config.num_constraints
        self.AIR_max_degree = config.AIR_max_degree
        self._lookups = config.lookups or []

    def get_lookups(self) -> list[LogUp]:
        """Returns the list of lookups for this circuit."""
        return self._lookups

    def get_security_levels(self) -> dict[str, dict[str, float]]:
        regime = UniqueDecodingRegime(self.field)
        pcs_levels = self.pcs.get_pcs_security_levels(regime)

        # Multilinear zerocheck error
        log_height = ceil(log2(self.pcs.get_trace_length()))
        zerocheck_error = (self.num_constraints + (self.AIR_max_degree + 2) * log_height) / self.field.F
        all_levels = pcs_levels | {"zerocheck": get_bits_of_security_from_error(zerocheck_error)}

        # Add lookup security levels
        for lookup in self._lookups:
            all_levels[lookup.get_name()] = lookup.get_soundness_bits()

        all_levels["total"] = min(all_levels.values())
        return {regime.identifier(): all_levels}

    def get_parameter_summary(self) -> str:
        """Returns a description of the parameters of the circuit."""
        pcs_summary = self.pcs.get_parameter_summary()
        lines = pcs_summary.split("\n")

        # Find the closing ``` (last one) and insert params before it
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip() == "```":
                extra_lines = []
                for lookup in self._lookups:
                    extra_lines.append(f"  lookup (logup)                     : {lookup.get_name()}")
                if extra_lines:
                    lines = lines[:i] + extra_lines + lines[i:]
                break

        return "\n".join(lines)

    def get_report_parameter_lines(self) -> list[str]:
        """Returns markdown-formatted parameter lines for reports."""
        dense = self._jagged_pcs.dense_pcs
        batching = "Powers" if dense.power_batching else "Affine"
        lines = [
            "- Proof system: Jagged",
            "- Inner PCS: FRI",
            f"- Hash size (bits): {dense.hash_size_bits}",
            f"- Number of queries: {dense.num_queries}",
            f"- Grinding query phase (bits): {dense.grinding_query_phase}",
        ]
        if dense.grinding_commit_phase > 0:
            lines.append(f"- Grinding commit phase (bits): {dense.grinding_commit_phase}")
        lines.extend([
            f"- Field: {dense.field.to_string()}",
            f"- Rate (ρ): {dense.rho}",
            f"- Dense trace length: $2^{{{dense.h}}}$",
            f"- Trace length: {self._jagged_pcs.trace_length}",
            f"- Trace width: {self._jagged_pcs.trace_width}",
            f"- FRI rounds: {dense.FRI_rounds_n}",
            f"- FRI folding factors: {dense.FRI_folding_factors}",
            f"- FRI early stop degree: {dense.FRI_early_stop_degree}",
            f"- Dense batch size: {dense.batch_size}",
            f"- Batching: {batching}",
        ])
        for lookup in self._lookups:
            lines.append(f"- Lookup (logup): {lookup.get_name()}")
        return lines
