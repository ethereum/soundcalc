from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Mapping, Any

from math import log2
import toml

from soundcalc.common.utils import get_bits_of_security_from_error
from soundcalc.proxgaps.johnson_bound import JohnsonBoundRegime
from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime
from soundcalc.proxgaps.unique_decoding import UniqueDecodingRegime
from soundcalc.zkvms.zkvm import Circuit, zkVM
from ..common.fields import FieldParams, parse_field
from ..common.fri import get_FRI_proof_size_bits, get_num_FRI_folding_rounds


def get_best_attack_security(field_size: float, rho: float, num_queries: int, grinding_query_phase: int) -> int:
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
    query_phase_error_without_grinding = rho ** num_queries
    # Add bits of security from grinding (see section 6.3 in ethSTARK)
    query_phase_error_with_grinding = query_phase_error_without_grinding * 2 ** (-grinding_query_phase)

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
        * (params.AIR_max_degree * (params.trace_length + params.max_combo - 1) + (params.trace_length - 1))
        / (params.field_size - params.trace_length - params.D)
    )

    levels = {}
    levels["ALI"] = get_bits_of_security_from_error(e_ALI)
    levels["DEEP"] = get_bits_of_security_from_error(e_DEEP)

    return levels

@dataclass(frozen=True)
class FRIBasedCircuitConfig:
    """
    A configuration of a FRI-based zkVM
    """

    # Name of the proof system
    name: str

    # The output length of the hash function that is used in bits
    # Note: this concerns the hash function used for Merkle trees
    hash_size_bits: int

    # The code rate ρ
    rho: float
    # Domain size before low-degree extension (i.e. trace length)
    trace_length: int
    # Preset field parameters (contains p, ext_size, F)
    field: FieldParams
    # Total columns of AIR table
    num_columns: int
    # Number of functions appearing in the batched-FRI
    # This can be greater than `num_columns`: some zkEVMs have to use "segment polynomials" (aka "composition polynomials")
    batch_size: int
    # Boolean flag to indicate if batched-FRI is implemented using coefficients
    # r^0, r^1, ... r^{batch_size-1} (power_batching = True) or
    # 1, r_1, r_2, ... r_{batch_size - 1} (power_batching = False)
    power_batching: bool
    # Number of FRI queries
    num_queries: int
    # Maximum constraint degree
    AIR_max_degree: int

    # FRI folding factor: one factor per FRI round
    FRI_folding_factors: list[int]
    # Many zkEVMs don't FRI fold until the final poly is of degree 1. They instead stop earlier.
    # This is the degree they stop at (and it influences the number of FRI folding rounds).
    FRI_early_stop_degree: int

    # Maximum number of entries from a single column referenced in a single constraint
    max_combo: int

    # Proof of Work grinding compute during FRI query phase (expressed in bits of security)
    grinding_query_phase: int


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
            "field": self.field.to_string(),
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
            domain_size=int(self.D),
            folding_factors=self.FRI_folding_factors,
            rate=self.rho
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
            grinding_query_phase=self.grinding_query_phase
        )

        return result

    def get_security_levels_for_regime(self, regime: ProximityGapsRegime) -> dict[str, int]:
        """
        Same as get_security_levels, but for a specific regime.
        """

        bits = {}

        # Compute FRI errors for batching
        bits["batching"] = get_bits_of_security_from_error(self.get_batching_error(regime))

        # Compute FRI error for folding / commit phase
        FRI_rounds = self.FRI_rounds_n
        for i in range(FRI_rounds):
            bits[f"commit round {i+1}"] = get_bits_of_security_from_error(self.get_commit_phase_error(i, regime))

        # Compute FRI error for query phase
        bits["query phase"] = get_bits_of_security_from_error(self.get_query_phase_error(regime))

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

        epsilon = regime.get_error_powers(rate, dimension, self.FRI_folding_factors[round])

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
    """
    A zkVM that contains one or more FRI-based circuits.
    """

    def __init__(self, name: str, circuits: list[FRIBasedCircuit]):
        self._name = name
        self._circuits = circuits

    @classmethod
    def load_from_toml(cls, toml_path: Path) -> "FRIBasedVM":
        """
        Load a FRI-based VM from a TOML configuration file.
        """
        with open(toml_path, "r") as f:
            config = toml.load(f)

        field = parse_field(config["zkevm"]["field"])
        circuits = []

        for section in config.get("circuits", []):
            cfg = FRIBasedCircuitConfig(
                name=section["name"],
                hash_size_bits=config["zkevm"]["hash_size_bits"],
                rho=section["rho"],
                trace_length=section["trace_length"],
                field=field,
                num_columns=section["num_columns"],
                batch_size=section["batch_size"],
                power_batching=section["power_batching"],
                num_queries=section["num_queries"],
                AIR_max_degree=section["air_max_degree"],
                FRI_folding_factors=section.get("fri_folding_factors"),
                FRI_early_stop_degree=section.get("fri_early_stop_degree"),
                max_combo=section["opening_points"],
                grinding_query_phase=section.get("grinding_query_phase", 0),
            )
            circuits.append(FRIBasedCircuit(cfg))

        return cls(config["zkevm"]["name"], circuits=circuits)

    def get_name(self) -> str:
        return self._name

    def get_circuits(self) -> list[FRIBasedCircuit]:
        return self._circuits
