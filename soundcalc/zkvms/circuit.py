from __future__ import annotations

from dataclasses import dataclass

from soundcalc.common.fields import FieldParams
from soundcalc.common.utils import get_bits_of_security_from_error
from soundcalc.pcs.pcs import PCS
from soundcalc.proxgaps.johnson_bound import JohnsonBoundRegime
from soundcalc.proxgaps.unique_decoding import UniqueDecodingRegime


@dataclass
class CircuitConfig:
    """Configuration for a Circuit."""
    name: str
    pcs: PCS
    field: FieldParams
    gap_to_radius: float | None = None
    # Total columns of AIR table (used in DEEP-ALI soundness)
    num_columns: int | None = None
    # Maximum constraint degree
    AIR_max_degree: int | None = None
    # Maximum number of entries from a single column referenced in a single constraint
    max_combo: int | None = None


class Circuit:
    """
    A class modeling a single circuit within a zkVM.
    Each circuit has its own parameters and security analysis.
    """

    def __init__(self, config: CircuitConfig):
        self.name = config.name
        self.pcs = config.pcs
        self.field = config.field
        self.gap_to_radius = config.gap_to_radius
        # Store optional DEEP-ALI params
        self.num_columns = config.num_columns
        self.AIR_max_degree = config.AIR_max_degree
        self.max_combo = config.max_combo

    def get_name(self) -> str:
        """Returns the name of the circuit."""
        return self.name

    def get_parameter_summary(self) -> str:
        """Returns a description of the parameters of the circuit."""
        pcs_summary = self.pcs.get_parameter_summary()
        if self._has_deep_ali_params():
            # Insert DEEP-ALI params into the summary
            lines = pcs_summary.split("\n")
            # Find the closing ``` and insert before it
            for i, line in enumerate(lines):
                if line.strip() == "```" and i > 0:
                    deep_ali_lines = [
                        f"  num_columns                        : {self.num_columns}",
                        f"  AIR_max_degree                     : {self.AIR_max_degree}",
                        f"  max_combo                          : {self.max_combo}",
                    ]
                    lines = lines[:i] + deep_ali_lines + lines[i:]
                    break
            return "\n".join(lines)
        return pcs_summary

    def get_proof_size_bits(self) -> int:
        """
        Returns an estimate for the proof size, given in bits.
        """
        return self.pcs.get_proof_size_bits()

    def get_expected_proof_size_bits(self) -> int:
        """
        Returns an estimate for the *expected* proof size, given in bits.
        """
        return self.pcs.get_expected_proof_size_bits()

    def get_security_levels(self) -> dict[str, dict[str, int]]:
        """
        Returns a dictionary that maps each regime (i.e., a way of doing security analysis)
        to a dictionary that contains the round-by-round soundness levels.

        It maps from a label that describes the regime (e.g., UDR, JBR in case of FRI) to a
        regime-specific dictionary. Any such regime-specific dictionary is as follows:

        It maps from a label that explains which round it is for to an integer.
        If this integer is, say, k, then it means the error for this round is at
        most 2^{-k}.
        """
        regimes = [
            UniqueDecodingRegime(self.field),
            JohnsonBoundRegime(self.field, gap_to_radius=self.gap_to_radius),
        ]

        result = {}
        for regime in regimes:
            id = regime.identifier()
            pcs_levels = self.pcs.get_pcs_security_levels(regime)

            # Add DEEP-ALI errors if circuit params are provided
            if self._has_deep_ali_params():
                rate = self.pcs.get_rate()
                dimension = self.pcs.get_dimension()
                list_size = regime.get_max_list_size(rate, dimension)
                deep_ali_levels = self._get_DEEP_ALI_errors(list_size)
                all_levels = pcs_levels | deep_ali_levels
            else:
                all_levels = pcs_levels

            all_levels["total"] = min(all_levels.values())
            result[id] = all_levels

        return result

    def _has_deep_ali_params(self) -> bool:
        """Should we report DEEP-ALI soundness?"""
        # A dirty heuristic for now
        return self.num_columns is not None

    def _get_DEEP_ALI_errors(self, L_plus: float) -> dict[str, int]:
        """
        Compute common proof system error components that are shared across regimes.
        Some of them depend on the list size L_plus

        Returns a dictionary containing levels for ALI and DEEP
        """
        # TODO Check that it holds for all regimes

        # XXX These proof system errors are actually quite RISC0 specific.
        # See Section 3.4 from the RISC0 technical report.
        # We might want to generalize this further for other zkEVMs.
        # For example, Miden also computes similar values for DEEP-ALI in:
        # https://github.com/facebook/winterfell/blob/2f78ee9bf667a561bdfcdfa68668d0f9b18b8315/air/src/proof/security.rs#L188-L210
        field_size = self.field.F
        trace_length = self.pcs.get_dimension()
        D = trace_length / self.pcs.get_rate()

        e_ALI = L_plus * self.num_columns / field_size
        e_DEEP = (
            L_plus
            * (self.AIR_max_degree * (trace_length + self.max_combo - 1) + (trace_length - 1))
            / (field_size - trace_length - D)
        )

        levels = {}
        levels["ALI"] = get_bits_of_security_from_error(e_ALI)
        levels["DEEP"] = get_bits_of_security_from_error(e_DEEP)

        return levels
