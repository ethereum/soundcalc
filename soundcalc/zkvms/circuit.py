from __future__ import annotations

from dataclasses import dataclass
from math import ceil, log2
from soundcalc.common.fields import FieldParams
from soundcalc.common.utils import apply_grinding, get_bits_of_security_from_error
from soundcalc.lookups.logup import LogUp
from soundcalc.pcs.pcs import PCS
from soundcalc.proxgaps.johnson_bound import JohnsonBoundRegime
from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime
from soundcalc.proxgaps.unique_decoding import UniqueDecodingRegime


@dataclass
class CircuitConfig:
    """Configuration for a Circuit."""
    name: str
    pcs: PCS
    field: FieldParams
    gap_to_radius: float | None = None
    # Total constraints of AIR table (used in DEEP-ALI soundness)
    num_constraints: int | None = None
    # Maximum constraint degree
    AIR_max_degree: int | None = None
    # Maximum number of entries from a single column referenced in a single constraint
    max_combo: int | None = None
    # Optional list of LogUp instances for lookup soundness
    lookups: list[LogUp] | None = None
    # Whether or not the zerocheck is done with a multilinear sumcheck
    multilinear_zerocheck: bool = False
    # Whether or not to only analyze unique decoding regime. 
    udr_only: bool = False
    # Proof of Work grinding during DEEP (expressed in bits of security)
    grinding_deep: int = 0


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
        self.num_constraints = config.num_constraints
        self.AIR_max_degree = config.AIR_max_degree
        self.max_combo = config.max_combo
        self.multilinear_zerocheck = config.multilinear_zerocheck
        self.udr_only = config.udr_only
        # TODO: add zerocheck error outside of unique decoding regime
        if self.multilinear_zerocheck:
            assert self.udr_only
        # Store optional lookups
        self._lookups = config.lookups or []
        self.grinding_deep = config.grinding_deep

    def get_name(self) -> str:
        """Returns the name of the circuit."""
        return self.name

    def get_lookups(self) -> list[LogUp]:
        """Returns the list of lookups for this circuit."""
        return self._lookups

    def get_parameter_summary(self) -> str:
        """Returns a description of the parameters of the circuit."""
        pcs_summary = self.pcs.get_parameter_summary()
        lines = pcs_summary.split("\n")

        # Find the closing ``` (last one) and insert params before it
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip() == "```":
                extra_lines = []

                # Add DEEP-ALI params if present
                if self._has_deep_ali_params():
                    extra_lines.extend([
                        f"  num_constraints                    : {self.num_constraints}",
                        f"  AIR_max_degree                     : {self.AIR_max_degree}",
                        f"  max_combo                          : {self.max_combo}",
                    ])

                # Add lookup params
                for lookup in self._lookups:
                    extra_lines.append(f"  lookup (logup)                     : {lookup.get_name()}")

                # Add grinding_deep if non-zero
                if self.grinding_deep > 0:
                    extra_lines.append(f"  grinding_deep                  : {self.grinding_deep}")

                if extra_lines:
                    lines = lines[:i] + extra_lines + lines[i:]
                break

        return "\n".join(lines)

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
        ]
        if self.udr_only == False:
            regimes.append(JohnsonBoundRegime(self.field, gap_to_radius=self.gap_to_radius))
        
        result = {}
        for regime in regimes:
            id = regime.identifier()
            pcs_levels = self.pcs.get_pcs_security_levels(regime)

            # Add DEEP-ALI errors if circuit params are provided
            if self._has_deep_ali_params():
                rate = self.pcs.get_rate()
                dimension = self.pcs.get_dimension()
                list_size = regime.get_max_list_size(rate, dimension)
                deep_ali_levels = self._get_DEEP_ALI_errors(list_size,regime)
                all_levels = pcs_levels | deep_ali_levels
            # A dirty heuristic for now, add zerocheck error only for unique decoding regime.
            elif self.multilinear_zerocheck and self.udr_only: 
                zerocheck_levels = {}
                log_height = ceil(log2(self.pcs.get_trace_height()))
                zerocheck_error = (self.num_constraints + (self.AIR_max_degree + 2) * log_height) / self.field.F
                zerocheck_levels["zerocheck"] = get_bits_of_security_from_error(zerocheck_error)
                all_levels = pcs_levels | zerocheck_levels
            else:
                all_levels = pcs_levels

            # Add lookup security levels
            for lookup in self._lookups:
                all_levels[lookup.get_name()] = lookup.get_soundness_bits()

            all_levels["total"] = min(all_levels.values())
            result[id] = all_levels

        return result

    def _has_deep_ali_params(self) -> bool:
        """Should we report DEEP-ALI soundness?"""
        # A dirty heuristic for now
        return self.num_constraints is not None and self.multilinear_zerocheck == False

    def _get_DEEP_ALI_errors(self, L_plus: float, regime: ProximityGapsRegime) -> dict[str, int]:
        """
        Compute common proof system error components that are shared across regimes.
        Some of them depend on the list size L_plus

        Returns a dictionary containing levels for ALI and DEEP
        """

        # Theorem 8 of https://eprint.iacr.org/2022/1216.pdf
        # Note: These bounds are regime independent
        # TODO: If linear batching is used, the num_constraints term in e_ALI should be removed
        # TODO: L_plus computation depends on how the FRI batching is performed.
        #       For instance, if I want to prove the evaluation of f(X) at both z and g·z, then I can
        #       either run a LDT over functions g1(X) = (f(X) - f(z)) / (X - z) and g2(X) = (f(X) - f(g·z)) / (X - g·z)
        #       or I can run a LDT over a single function h(X) = (f(X) - U(X)) / ((X - z)(X - g·z))
        #       where U(X) is the unique degree < 2 interpolant through points (z, f(z)) and (g·z, f(g·z)).
        #       Here it is assumed that the second approach is used.
        field_size = self.field.F
        trace_length = self.pcs.get_dimension()
        rate = self.pcs.get_rate()
        D = trace_length / rate
        theta = regime.get_proximity_parameter(rate, trace_length)
        # Multi-point quotients (a.k.a. combo batching) are only sound when the evaluation domain
        # has enough "slack" relative to the proximity window:
        #   k + m_max < (1 - θ) · n
        # We enforce this here because our DEEP-ALI bound uses multi-point quotients with parameter
        # m_max; the paper states/derives this condition in its FRI multi-point-queries analysis
        # Ref: https://eprint.iacr.org/archive/2022/1216/20241217:162441, Section 4.1.3 (multi-point queries).
        assert trace_length + self.max_combo < (1.0 - theta) * D, (
            "Violates multi-point condition: k + m_max < (1-θ)·n. "
            f"k={trace_length}, m_max={self.max_combo}, θ={theta}, n={D}, (1-θ)·n={(1.0 - theta) * D}."
        )

        e_ALI = L_plus * self.num_constraints / field_size
        e_DEEP = (
            L_plus
            * (self.AIR_max_degree * (trace_length + self.max_combo - 1) + (trace_length - 1))
            / (field_size - trace_length - D)
        )

        # take into account any DEEP grinding
        e_DEEP = apply_grinding(e_DEEP, self.grinding_deep)

        levels = {}
        levels["ALI"] = get_bits_of_security_from_error(e_ALI)
        levels["DEEP"] = get_bits_of_security_from_error(e_DEEP)

        return levels
