from __future__ import annotations

from math import log2
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from soundcalc.common.fields import FieldParams
from soundcalc.common.fri import get_FRI_proof_size_bits, get_num_FRI_folding_rounds
from soundcalc.common.utils import get_bits_of_security_from_error
from soundcalc.proxgaps.johnson_bound import JohnsonBoundRegime
from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime
from soundcalc.proxgaps.unique_decoding import UniqueDecodingRegime
from soundcalc.schemas import FRIConfig
from soundcalc.zkvms.zkvm import Circuit, zkVM


def get_best_attack_security(
    field_size: float, rho: float, num_queries: int, grinding_query_phase: int
) -> int:
    """
    Security level based on the best known attack.

    Currently, this is based on the toy problem also known as "ethSTARK conjecture".
    It uses the simplest and probably the most optimistic soundness analysis.

    Note: this is just for historical reference, the toy problem security has no real meaning.

    This is Regime 1 from the RISC0 Python calculator
    """

    # FRI errors under the toy problem regime
    # see "Toy problem security" in §5.9.1 of the ethSTARK paper
    commit_phase_error = 1 / field_size
    query_phase_error_without_grinding = rho**num_queries
    # Add bits of security from grinding (see section 6.3 in ethSTARK)
    query_phase_error_with_grinding = query_phase_error_without_grinding * 2 ** (
        -grinding_query_phase
    )

    final_error = commit_phase_error + query_phase_error_with_grinding
    final_level = get_bits_of_security_from_error(final_error)

    return final_level


def get_DEEP_ALI_errors(L_plus: float, params: "FRIBasedCircuit"):
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
    e_ALI = L_plus * params.num_columns / params.field_size
    e_DEEP = (
        L_plus
        * (
            params.AIR_max_degree * (params.trace_length + params.max_combo - 1)
            + (params.trace_length - 1)
        )
        / (params.field_size - params.trace_length - params.D)
    )

    levels = {}
    levels["ALI"] = get_bits_of_security_from_error(e_ALI)
    levels["DEEP"] = get_bits_of_security_from_error(e_DEEP)

    return levels


class FRIBasedCircuitConfig(BaseModel):
    """A configuration of a FRI-based zkVM."""

    model_config = ConfigDict(frozen=True)

    name: str
    """Name of the proof system."""

    hash_size_bits: int
    """
    The output length of the hash function that is used in bits.
    Note: this concerns the hash function used for Merkle trees.
    """

    rho: float
    """The code rate ρ."""

    trace_length: int
    """Domain size before low-degree extension (i.e. trace length)."""

    field: FieldParams
    """Preset field parameters (contains p, ext_size, F)."""

    num_columns: int
    """Total columns of AIR table."""

    batch_size: int
    """
    Number of functions appearing in the batched-FRI.
    This can be greater than `num_columns`: some zkEVMs have to use
    "segment polynomials" (aka "composition polynomials").
    """

    power_batching: bool
    """
    Boolean flag to indicate if batched-FRI is implemented using coefficients
    r^0, r^1, ... r^{batch_size-1} (power_batching = True) or
    1, r_1, r_2, ... r_{batch_size - 1} (power_batching = False).
    """

    num_queries: int
    """Number of FRI queries."""

    AIR_max_degree: int
    """Maximum constraint degree."""

    FRI_folding_factors: list[int]
    """FRI folding factor: one factor per FRI round."""

    FRI_early_stop_degree: int
    """
    Many zkEVMs don't FRI fold until the final poly is of degree 1. They instead stop earlier.
    This is the degree they stop at (and it influences the number of FRI folding rounds).
    """

    max_combo: int
    """Maximum number of entries from a single column referenced in a single constraint."""

    grinding_query_phase: int
    """Proof of Work grinding compute during FRI query phase (expressed in bits of security)."""


class FRIBasedCircuit(Circuit):
    """
    Models a single circuit that is based on FRI.
    """

    def __init__(self, config: FRIBasedCircuitConfig):
        """
        Given a config, compute all the parameters relevant for the zkVM.
        """
        # Copy the parameters over (also see docs just above)
        self.name = config.name
        self.hash_size_bits = config.hash_size_bits
        self.rho = config.rho
        self.trace_length = config.trace_length
        self.num_columns = config.num_columns
        self.batch_size = config.batch_size
        self.power_batching = config.power_batching
        self.num_queries = config.num_queries
        self.max_combo = config.max_combo
        self.FRI_folding_factors = config.FRI_folding_factors
        self.FRI_early_stop_degree = config.FRI_early_stop_degree
        self.grinding_query_phase = config.grinding_query_phase
        self.AIR_max_degree = config.AIR_max_degree

        # Number of columns should be less or equal to the final number of polynomials in batched-FRI
        assert self.num_columns <= self.batch_size

        # Now, also compute some auxiliary parameters

        # Negative log of rate
        self.k = int(round(-log2(self.rho)))
        # Log of trace length
        self.h = int(round(log2(self.trace_length)))
        # Domain size, after low-degree extension
        self.D = self.trace_length / self.rho

        # Extract field parameters from the preset field
        # Extension field degree (e.g., ext_size = 2 for Fp²)
        self.field_extension_degree = config.field.field_extension_degree
        # Extension field size |F| = p^{ext_size}
        self.field = config.field
        self.field_size = config.field.F

        # Compute number of FRI folding rounds
        self.FRI_rounds_n = get_num_FRI_folding_rounds(
            witness_size=int(self.D),
            field_extension_degree=int(self.field_extension_degree),
            folding_factors=self.FRI_folding_factors,
            fri_early_stop_degree=int(self.FRI_early_stop_degree),
        )

    def get_name(self) -> str:
        return self.name

    def get_parameter_summary(self) -> str:
        """
        Returns a description of the parameters of the zkVM.
        The description is given as a string; formatted so that it looks good
        in both console output and in markdown reports.
        """

        # We put everything inside a markdown code block so it looks
        # identical in plain terminal output.
        lines = []
        lines.append("")
        lines.append("```")

        # Key–value table
        params = {
            "name": self.name,
            "hash_size_bits": self.hash_size_bits,
            "rho": self.rho,
            "k = -log2(rho)": self.k,
            "trace_length": self.trace_length,
            "h = log2(trace_length)": self.h,
            "domain_size D = trace_length / rho": self.D,
            "num_columns": self.num_columns,
            "batch_size": self.batch_size,
            "power_batching": self.power_batching,
            "num_queries": self.num_queries,
            "max_combo": self.max_combo,
            "FRI_folding_factors": self.FRI_folding_factors,
            "FRI_early_stop_degree": self.FRI_early_stop_degree,
            "FRI_rounds_n": self.FRI_rounds_n,
            "grinding_query_phase": self.grinding_query_phase,
            "AIR_max_degree": self.AIR_max_degree,
            "field": str(self.field),
            "field_extension_degree": self.field_extension_degree,
        }

        # Determine alignment width
        key_width = max(len(k) for k in params.keys())

        # Format lines with aligned columns
        for k, v in params.items():
            lines.append(f"  {k:<{key_width}} : {v}")

        lines.append("```")
        return "\n".join(lines)

    def get_proof_size_bits(self) -> int:
        """
        Returns an estimate for the proof size, given in bits.
        """

        # Compute the proof size
        # XXX (BW): note that it is not clear that this is the
        # proof size for every zkEVM we can think of
        # XXX (BW): we should probably also add something for the OOD samples and plookup, lookup etc.

        return get_FRI_proof_size_bits(
            hash_size_bits=self.hash_size_bits,
            field_size_bits=self.field.extension_field_element_size_bits(),
            batch_size=self.batch_size,
            num_queries=self.num_queries,
            witness_size=int(self.D),
            field_extension_degree=int(self.field_extension_degree),
            early_stop_degree=int(self.FRI_early_stop_degree),
            folding_factors=self.FRI_folding_factors,
        )

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

        # we consider the following regimes, and for each regime do the analysis
        regimes = [UniqueDecodingRegime(self.field), JohnsonBoundRegime(self.field)]

        result = {}
        for regime in regimes:
            # Get parameters
            id = regime.identifier()
            rate = self.rho
            dimension = self.trace_length

            # Compute security levels
            fri_levels = self.get_security_levels_for_regime(regime)
            list_size = regime.get_max_list_size(rate, dimension)
            proof_system_levels = get_DEEP_ALI_errors(list_size, self)

            # Note down security levels
            total = min(list(fri_levels.values()) + list(proof_system_levels.values()))
            result[id] = fri_levels | proof_system_levels | {"total": total}

        result["best attack"] = get_best_attack_security(
            field_size=self.field_size,
            rho=self.rho,
            num_queries=self.num_queries,
            grinding_query_phase=self.grinding_query_phase,
        )

        return result

    def get_security_levels_for_regime(
        self, regime: ProximityGapsRegime
    ) -> dict[str, int]:
        """
        Same as get_security_levels, but for a specific regime.
        """

        bits = {}

        # Compute FRI errors for batching
        bits["batching"] = get_bits_of_security_from_error(
            self.get_batching_error(regime)
        )

        # Compute FRI error for folding / commit phase
        FRI_rounds = self.FRI_rounds_n
        for i in range(FRI_rounds):
            bits[f"commit round {i + 1}"] = get_bits_of_security_from_error(
                self.get_commit_phase_error(i, regime)
            )

        # Compute FRI error for query phase
        bits["query phase"] = get_bits_of_security_from_error(
            self.get_query_phase_error(regime)
        )

        return bits

    def get_batching_error(self, regime: ProximityGapsRegime) -> float:
        """
        Returns the error due to the batching step. This depends on whether batching is done
        with powers or with random coefficients.
        """

        rate = self.rho
        dimension = self.trace_length

        if self.power_batching:
            epsilon = regime.get_error_powers(rate, dimension, self.batch_size)
        else:
            epsilon = regime.get_error_linear(rate, dimension)

        return epsilon

    def get_commit_phase_error(self, round: int, regime: ProximityGapsRegime) -> float:
        """
        Returns the error from a round of the commit phase.
        """

        rate = self.rho

        acc_folding_factor = 1
        for i in range(round + 1):
            acc_folding_factor *= self.FRI_folding_factors[i]

        dimension = self.trace_length / acc_folding_factor

        epsilon = regime.get_error_powers(
            rate, dimension, self.FRI_folding_factors[round]
        )

        return epsilon

    def get_query_phase_error(self, regime: ProximityGapsRegime) -> float:
        """
        Returns the error from the FRI query phase, including grinding.
        """

        rate = self.rho
        dimension = self.trace_length

        # error is (1-pp)^number of queries
        pp = regime.get_proximity_parameter(rate, dimension)
        epsilon = (1 - pp) ** self.num_queries

        # add grinding
        epsilon *= 2 ** (-self.grinding_query_phase)

        return epsilon


class FRIBasedVM(zkVM):
    """A zkVM that contains one or more FRI-based circuits."""

    def __init__(self, name: str, circuits: list[FRIBasedCircuit]):
        self._name = name
        self._circuits = circuits

    @classmethod
    def load(cls, path: Path) -> "FRIBasedVM":
        """Load a FRI-based VM from a JSON configuration file."""
        data = FRIConfig.load(path)
        circuits = [
            FRIBasedCircuit(
                FRIBasedCircuitConfig(
                    name=c.name,
                    hash_size_bits=data.zkevm.hash_size_bits,
                    rho=c.rho,
                    trace_length=c.trace_length,
                    field=data.zkevm.field,
                    num_columns=c.num_columns,
                    batch_size=c.batch_size,
                    power_batching=c.power_batching,
                    num_queries=c.num_queries,
                    AIR_max_degree=c.air_max_degree,
                    FRI_folding_factors=c.fri_folding_factors,
                    FRI_early_stop_degree=c.fri_early_stop_degree,
                    max_combo=c.opening_points,
                    grinding_query_phase=c.grinding_query_phase,
                )
            )
            for c in data.circuits
        ]
        return cls(data.zkevm.name, circuits=circuits)

    def get_name(self) -> str:
        return self._name

    def get_circuits(self) -> list[FRIBasedCircuit]:
        return self._circuits
