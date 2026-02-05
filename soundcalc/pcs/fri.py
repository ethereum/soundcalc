from __future__ import annotations

from dataclasses import dataclass
from math import log2
from typing import Optional

from soundcalc.common.fields import FieldParams
from soundcalc.common.utils import apply_grinding, get_bits_of_security_from_error, get_size_of_merkle_multi_proof_bits, get_size_of_merkle_proof_bits
from soundcalc.pcs.pcs import PCS
from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime


def get_FRI_proof_size_bits(
        hash_size_bits: int,
        field_size_bits: int,
        batch_size: int,
        num_queries: int,
        domain_size: int,
        folding_factors: list[int],
        rate: int,
        expected: bool
) -> int:
    """
    Compute the proof size or expected proof size of a (BCS-transformed) FRI interaction in bits.
    """

    # TODO: the following things are not yet considered.
    #   - is there really a Merkle root (and paths) for the final round? Or just the codeword itself?

    # The FRI proof contains two parts: Merkle roots, and one "openings" per query,
    # where an "opening" is a Merkle path for each folding layer.
    #
    # We use the same loop as in `get_num_FRI_folding_rounds`, and count the size that
    # this layer contributes, which includes the root and all Merkle paths.

    size_bits = 0

    # Initial Round: one root and opening the queries
    # We assume that for the initial functions, there is only one Merkle root, and
    # each leaf i for that root contains symbols i for all initial functions.
    n = int(domain_size)
    num_leafs = n
    tuple_size = batch_size
    size_bits += hash_size_bits # root
    size_bits += get_size_of_merkle_multi_proof_bits(num_leafs, num_queries, tuple_size, field_size_bits, hash_size_bits, expected) # queries

    # Now we have folded these batch_size initial functions into one
    # Next, we start with the folding rounds.

    # We assume that "siblings" for the following layers are grouped together
    # in one leaf. This is natural as they always need to be opened together.

    rounds = len(folding_factors)
    for i in range(rounds):

        # in our current domain, we group together all siblings (sometimes denoted Block(z) in the literature)
        num_leafs = n // int(folding_factors[i])
        tuple_size = folding_factors[i]

        # one root and one path per query
        size_bits += hash_size_bits # root
        size_bits += get_size_of_merkle_multi_proof_bits(num_leafs, num_queries, tuple_size, field_size_bits, hash_size_bits, expected) # queries

        # next domain size is given by applying folding
        n = n // int(folding_factors[i])

    # for the final round, we send the function in the clear.
    # note that we don't need to send the full function, but can just send
    # the polynomial that describes it
    size_bits += rate * n * field_size_bits

    return size_bits


@dataclass(frozen=True)
class FRIConfig:
    """
    Configuration for FRI PCS.
    """

    # The output length of the hash function that is used in bits
    # Note: this concerns the hash function used for Merkle trees
    hash_size_bits: int

    # The code rate ρ
    rho: float
    # Domain size before low-degree extension (i.e. trace length)
    trace_length: int
    # Preset field parameters (contains p, ext_size, F)
    field: FieldParams
    # Number of functions appearing in the batched-FRI
    # This can be greater than `num_columns`: some zkEVMs have to use "segment polynomials" (aka "composition polynomials")
    batch_size: int
    # Boolean flag to indicate if batched-FRI is implemented using coefficients
    # r^0, r^1, ... r^{batch_size-1} (power_batching = True) or
    # 1, r_1, r_2, ... r_{batch_size - 1} (power_batching = False)
    power_batching: bool
    # Number of FRI queries
    num_queries: int

    # FRI folding factor: one factor per FRI round
    FRI_folding_factors: list[int]
    # Many zkEVMs don't FRI fold until the final poly is of degree 1. They instead stop earlier.
    # This is the degree they stop at (and it influences the number of FRI folding rounds).
    FRI_early_stop_degree: int

    # Proof of Work grinding compute during FRI query phase (expressed in bits of security)
    grinding_query_phase: int

    # Proof of Work grinding compute during FRI commit phase (expressed in bits of security)
    # (Protocols apply this level of grinding to every round of the commit phase due to RBR security)
    grinding_commit_phase: int = 0

    # Optional override for the bound *gap*.
    # (This is useful to pin fixed parameters in TOML configs.)
    gap_to_radius: Optional[float] = None

class FRI(PCS):
    """
    FRI Polynomial Commitment Scheme.
    """

    def __init__(self, config: FRIConfig):
        self.hash_size_bits = config.hash_size_bits
        self.rho = config.rho
        self.trace_length = config.trace_length
        self.batch_size = config.batch_size
        self.power_batching = config.power_batching
        self.num_queries = config.num_queries
        self.FRI_folding_factors = config.FRI_folding_factors
        self.FRI_early_stop_degree = config.FRI_early_stop_degree
        self.grinding_query_phase = config.grinding_query_phase
        self.grinding_commit_phase = config.grinding_commit_phase
        self.gap_to_radius = config.gap_to_radius

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
        self.FRI_rounds_n = self._get_num_folding_rounds()

    def get_pcs_security_levels(self, regime: ProximityGapsRegime) -> dict[str, int]:
        """
        Returns PCS-specific security levels for a given regime.
        """
        bits = {}

        # Compute FRI errors for batching
        bits["batching"] = get_bits_of_security_from_error(self._get_batching_error(regime))

        # Compute FRI error for folding / commit phase
        FRI_rounds = self.FRI_rounds_n
        for i in range(FRI_rounds):
            bits[f"commit round {i+1}"] = get_bits_of_security_from_error(self._get_commit_phase_error(i, regime))

        # Compute FRI error for query phase
        bits["query phase"] = get_bits_of_security_from_error(self._get_query_phase_error(regime))

        return bits

    def _get_batching_error(self, regime: ProximityGapsRegime) -> float:
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

    def _get_commit_phase_error(self, round: int, regime: ProximityGapsRegime) -> float:
        """
        Returns the error from a round of the commit phase.
        """
        rate = self.rho

        acc_folding_factor = 1
        for i in range(round + 1):
            acc_folding_factor *= self.FRI_folding_factors[i]

        dimension = self.trace_length / acc_folding_factor

        epsilon = regime.get_error_powers(rate, dimension, self.FRI_folding_factors[round])

        # add grinding for commit phase
        epsilon = apply_grinding(epsilon, self.grinding_commit_phase)

        return epsilon

    def _get_query_phase_error(self, regime: ProximityGapsRegime) -> float:
        """
        Returns the error from the FRI query phase, including grinding.
        """
        rate = self.rho
        dimension = self.trace_length

        # error is (1-pp)^number of queries
        pp = regime.get_proximity_parameter(rate, dimension)
        epsilon = (1 - pp) ** self.num_queries

        # add grinding
        epsilon = apply_grinding(epsilon, self.grinding_query_phase)

        return epsilon

    def _get_num_folding_rounds(self) -> int:
        """
        Compute the number of FRI folding rounds.
        Stolen from:
          https://github.com/risc0/risc0/blob/release-2.0/risc0/zkp/src/prove/soundness.rs#L125
        """
        n = int(self.D)
        rounds = 0

        for i in range(len(self.FRI_folding_factors)):
            n //= self.FRI_folding_factors[i]
            rounds += 1

        # Make sure that the early stop degree is correctly set
        assert n == self.FRI_early_stop_degree, (
            f"After {rounds} rounds, n={n} != FRI_early_stop_degree={self.FRI_early_stop_degree}"
        )
        return rounds

    def get_proof_size_bits(self) -> int:
        """
        Returns an estimate for the proof size, given in bits.
        """
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
            rate=self.rho,
            expected=False
        )

    def get_expected_proof_size_bits(self) -> int:
        """Returns estimated *expected* proof size in bits."""
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
            rate=self.rho,
            expected=True
        )

    def get_rate(self) -> float:
        return self.rho

    def get_dimension(self) -> int:
        return self.trace_length

    def get_parameter_summary(self) -> str:
        """
        Returns a description of the parameters of the PCS.
        """
        lines = []
        lines.append("")
        lines.append("```")

        params = {
            "hash_size_bits": self.hash_size_bits,
            "rho": self.rho,
            "k = -log2(rho)": self.k,
            "trace_length": self.trace_length,
            "h = log2(trace_length)": self.h,
            "domain_size D = trace_length / rho": self.D,
            "batch_size": self.batch_size,
            "power_batching": self.power_batching,
            "num_queries": self.num_queries,
            "gap_to_radius": self.gap_to_radius,
            "FRI_folding_factors": self.FRI_folding_factors,
            "FRI_early_stop_degree": self.FRI_early_stop_degree,
            "FRI_rounds_n": self.FRI_rounds_n,
            "grinding_query_phase": self.grinding_query_phase,
            "grinding_commit_phase": self.grinding_commit_phase,
            "field": self.field.to_string(),
            "field_extension_degree": self.field_extension_degree,
        }

        key_width = max(len(k) for k in params.keys())
        for k, v in params.items():
            lines.append(f"  {k:<{key_width}} : {v}")

        lines.append("```")
        return "\n".join(lines)
