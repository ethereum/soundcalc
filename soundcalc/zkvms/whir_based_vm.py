
from dataclasses import dataclass

from soundcalc.common.fields import FieldParams, field_element_size_bits
from soundcalc.common.utils import get_size_of_merkle_path_bits
from soundcalc.zkvms.zkvm import zkVM

@dataclass(frozen=True)
class WHIRBasedVMConfig:
    """
    A configuration of a FRI-based zkVM
    """

    # Name of the proof system
    name: str

    # The output length of the hash function that is used in bits
    # Note: this concerns the hash function used for Merkle trees
    hash_size_bits: int

    # Parameters are inspired by Giacomo's script here for inspiration
    # https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/whir.rs

    # log2(1/rate), e.g., 2 if rate is 1/4
    # note that this is the rate of the initial code
    log_inv_rate: int

    # this is the number of WHIR iterations
    # note that a WHIR iteration consists of multiple rounds
    # this is denoted by M in the paper
    num_iterations: int

    # this is what is called k_0,...,k_{M-1} in the paper
    # as in Giacomo's script, we assume that this is the same for all
    # see https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/whir.rs#L72
    # in each iteration, we go from dimension 2^m_i to dimension 2^(m_i - k)
    folding_factor: int

    # the field that is used
    field: FieldParams

    # the log2 of the degree that we test
    # in the WHIR paper, this is denoted by m
    log_degree: int

    # how many functions do we test in one go
    # TODO (BW): need to check how batching is done in WHIR
    # This is not written in the WHIR paper IIUC, but here it is done:
    # https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/whir.rs#L144
    # batch_size: int

    # degree of constraints being proven on the committed words
    # This is d in Construction 5.1 in WHIR. Note that d = max{d*,3},
    # and d* =  1 + deg_Z(hat{w}0) + max_i deg_Xi(hat{w}0)
    constraint_degree: int

    # TODO (BW): grinding?
    # TODO: number of queries (different for each round)

    # the number of queries for each round (length M)
    num_queries: list[int]

    # the number of OOD samples for each round (length M-1)
    num_ood_samples: list[int]



class WHIRBasedVM(zkVM):
    """
    Models a zkVM that is based on WHIR.
    """
    def __init__(self, config: WHIRBasedVMConfig):
        """
        Given a config, compute all the parameters relevant for the zkVM.
        """
        self.name = config.name

        self.hash_size_bits = config.hash_size_bits
        self.folding_factor = config.folding_factor
        self.num_iterations = config.num_iterations
        self.field = config.field
        self.constraint_degree = config.constraint_degree
        self.num_queries = config.num_queries
        self.num_ood_samples = config.num_ood_samples

        # determine all rates (in contrast to FRI, these change over the iterations)
        # this also involves determining all log degrees
        assert(config.log_inv_rate > 0 and config.folding_factor >= 1)

        # the log degrees that we have are (m0, m1 = m0 - k, m2 = m0 - 2k, ..., m(M) = m0 - (M)k)
        assert (self.num_iterations * self.folding_factor <= config.log_degree)
        self.log_degrees = [config.log_degree - i * self.folding_factor for i in range(self.num_iterations + 1)]

        # the eval domain sizes shrink by a factor of two, so the rates decrease by a factor of
        self.log_inv_rates = [config.log_inv_rate + i * (self.folding_factor - 1) for i in range(self.num_iterations + 1)]

        # ensure that we did not mess up with the number of rounds
        assert(len(self.num_ood_samples) == self.num_iterations - 1)
        assert(len(self.log_degrees)     == self.num_iterations + 1)
        assert(len(self.log_inv_rates)   == self.num_iterations + 1)
        assert(len(self.num_queries)     == self.num_iterations)


    def get_name(self) -> str:
        return self.name

    def get_parameter_summary(self) -> str:
        lines = []
        lines.append("")
        lines.append("```")

        # Collect scalar parameters
        params = {
            "name": self.name,
            "hash_size_bits": self.hash_size_bits,
            "folding_factor": self.folding_factor,
            "num_iterations": self.num_iterations,
            "constraint_degree": self.constraint_degree,
            "field": self.field.to_string(),
        }

        key_width = max(len(k) for k in params)

        for k, v in params.items():
            lines.append(f"  {k:<{key_width}} : {v}")

        lines.append("")
        lines.append("  Per-round parameters:")
        lines.append(f"    log_degrees     : {self.log_degrees}")
        lines.append(f"    log_inv_rates   : {self.log_inv_rates}")
        lines.append(f"    num_queries     : {self.num_queries}")
        lines.append(f"    num_ood_samples : {self.num_ood_samples}")

        lines.append("```")
        return "\n".join(lines)

    def get_proof_size_bits(self) -> int:

        # We estimate the proof size by looking at the WHIR paper, counting sizes of prover messages.
        # Note that verifier messages do not count into proof size, as they are obtained from Fiat-Shamir.
        # Here, messages are either field elements, polynomials, functions, or function evaluations.
        #
        # Field elements are included directly in the proof;
        # Polynomials are sent by the vector of their coefficients;
        # Functions are sent in the form of a Merkle root;
        # Function evaluations are sent in the form of a Merkle path;

        field_size_bits = field_element_size_bits(self.field)

        # Prover sends the initial function (Merkle root)
        proof_size = self.hash_size_bits

        # Initial sum check: Prover sends k0 polynomials of degree d
        proof_size += self.folding_factor * self.constraint_degree * field_size_bits

        # Main loop, runs for i = 1 to i = M - 1
        for i in range(1, self.num_iterations):
            # In each iteration: send a function, then do OOD samples, then do sum check rounds

            # Send function
            proof_size += self.hash_size_bits

            # Send evaluations for the OOD samples
            proof_size += self.num_ood_samples[i-1] * field_size_bits

            # Sum check rounds
            proof_size += self.folding_factor * self.constraint_degree * field_size_bits

        # Prover sends the final polynomial. This is a multi-linear polynomial in
        # m_M variables, i.e., it has 2^{m_M} coefficients.
        assert self.log_degrees
        proof_size += self.log_degrees[-1] * field_size_bits

        # Decision phase: we query each function f_0,...,f_{M-1} that the prover sent
        # at t_i groups of points. Each group is a set of "folding siblings", also
        # called a "Block" in the literature. As in the WHIR paper, we assume that
        # an entire block is stored in the Merkle leaf. That is, we simply count
        # t_i Merkle leafs.
        assert(len(self.num_queries)     == self.num_iterations)
        for i in range(self.num_iterations):
            domain_size = 2 ** (self.log_degrees[i] + self.log_inv_rates[i])
            block_size = 2 ** self.folding_factor
            num_leafs = domain_size / block_size
            merkle_path_size = get_size_of_merkle_path_bits(num_leafs=num_leafs, tuple_size=block_size, element_size_bits=field_size_bits, hash_size_bits=self.hash_size_bits)
            proof_size += self.num_queries[i] * merkle_path_size


        return proof_size

    def get_security_levels(self) -> dict[str, dict[str, int]]:

        # TODO: add an error from the batching step

        # TODO: for initial sum check: k0 errors

        # TODO: for each iteration: OOD errors, shift errors, fold errors

        # TODO: final error from final

        return {} # TODO: implement