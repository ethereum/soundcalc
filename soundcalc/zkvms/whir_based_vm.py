
from dataclasses import dataclass

from soundcalc.common.fields import FieldParams, field_element_size_bits
from soundcalc.common.utils import get_bits_of_security_from_error, get_size_of_merkle_path_bits
from soundcalc.proxgaps.johnson_bound import JohnsonBoundRegime
from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime
from soundcalc.proxgaps.unique_decoding import UniqueDecodingRegime
from soundcalc.zkvms.zkvm import Circuit, zkVM
from typing import Tuple
import math

@dataclass(frozen=True)
class WHIRBasedVMConfig:
    """
    A configuration of a WHIR-based zkVM
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

    # how many functions do we check in one go, i.e., this is the batch size
    # for reference: https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/whir.rs#L144
    batch_size: int

    # Boolean flag to indicate if batching is implemented using coefficients
    # r^0, r^1, ... r^{batch_size-1} (power_batching = True) or
    # 1, r_1, r_2, ... r_{batch_size - 1} (power_batching = False)
    power_batching: bool

    # Number of bits of grinding for the batching round
    grinding_bits_batching: int

    # degree of constraints being proven on the committed words
    # This is d in Construction 5.1 in WHIR. Note that d = max{d*,3},
    # and d* =  1 + deg_Z(hat{w}0) + max_i deg_Xi(hat{w}0)
    constraint_degree: int

    # number of bits of grinding for reducing the folding errors (length M x k)
    # this impacts epsilon^fold_{i,s}, 0 <= i <= M-1, 0 <= s <= k
    grinding_bits_folding: list[list[int]]

    # the number of queries for each round (length M)
    # this is t_0, ... , t_{M-1} from the WHIR paper
    num_queries: list[int]

    # number of bits of grinding for the query rounds (length M)
    # this changes the errors eps_shift and eps_fin
    grinding_bits_queries: list[int]

    # the number of OOD samples for each round (length M-1)
    num_ood_samples: list[int]

    # number of bits of grinding for each OOD round (length M-1)
    grinding_bits_ood: list[int]




class WHIRBasedCircuit(Circuit):
    """
    Models a single circuit that is based on WHIR.
    """
    def __init__(self, config: WHIRBasedVMConfig):
        """
        Given a config, compute all the parameters relevant for the zkVM.
        """
        self.name = config.name

        # inherit parameters from the given config
        self.hash_size_bits = config.hash_size_bits
        self.folding_factor = config.folding_factor
        self.num_iterations = config.num_iterations
        self.field = config.field
        self.batch_size = config.batch_size
        self.power_batching = config.power_batching
        self.grinding_bits_batching = config.grinding_bits_batching
        self.constraint_degree = config.constraint_degree
        self.grinding_bits_folding = config.grinding_bits_folding
        self.num_queries = config.num_queries
        self.grinding_bits_queries = config.grinding_bits_queries
        self.num_ood_samples = config.num_ood_samples
        self.grinding_bits_ood = config.grinding_bits_ood

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

        # ensure that grinding parameters have correct length
        assert(len(self.grinding_bits_ood)     == self.num_iterations - 1)
        assert(len(self.grinding_bits_queries) == self.num_iterations)
        assert(len(self.grinding_bits_folding) == self.num_iterations)
        for grinding_bits_folding_for_iteration in self.grinding_bits_folding:
            assert(len(grinding_bits_folding_for_iteration) == self.folding_factor)

        # determine the total grinding overhead (sum of 2^grinding_bits)
        self.log_grinding_overhead = self.get_log_grinding_overhead()

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
            "batch_size": self.batch_size,
            "power_batching": self.power_batching,
            "grinding_bits_batching": self.grinding_bits_batching,
            "num_iterations": self.num_iterations,
            "constraint_degree": self.constraint_degree,
            "field": self.field.to_string(),
        }

        key_width = max(len(k) for k in params)

        for k, v in params.items():
            lines.append(f"  {k:<{key_width}} : {v}")

        lines.append("")
        lines.append("  Per-round parameters:")
        lines.append(f"    log_degrees           : {self.log_degrees}")
        lines.append(f"    log_inv_rates         : {self.log_inv_rates}")
        lines.append(f"    num_queries           : {self.num_queries}")
        lines.append(f"    grinding_bits_queries : {self.grinding_bits_queries}")
        lines.append(f"    num_ood_samples       : {self.num_ood_samples}")
        lines.append(f"    grinding_bits_ood     : {self.grinding_bits_ood}")
        lines.append(f"    grinding_bits_folding : {self.grinding_bits_folding}")
        lines.append("")
        lines.append(f"  Total grinding overhead (sum of 2^grinding_bits) = 2^({self.log_grinding_overhead})")


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
        proof_size += (2 ** self.log_degrees[-1]) * field_size_bits

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

        regimes = [UniqueDecodingRegime(), JohnsonBoundRegime()]

        result = {}
        for regime in regimes:
            id = regime.identifier()
            result[id] = self.get_security_levels_for_regime(regime)

        return result

    def get_security_levels_for_regime(self, regime: ProximityGapsRegime) -> dict[str, int]:
        """
        Same as get_security_levels, but for a specific regime.
        """
        levels = {}

        # add an error from the batching step
        if self.batch_size > 1:
            epsilon_batch = self.get_batching_error(regime)
            levels[f"batching"] = get_bits_of_security_from_error(epsilon_batch)

        # initial iteration (just sum check / fold errors)
        iteration = 0
        for round in range(1, self.folding_factor + 1):
            epsilon = self.epsilon_fold(iteration, round, regime)
            levels[f"fold(i={iteration},s={round})"] = get_bits_of_security_from_error(epsilon)

        # for each iteration i = 1, ... M - 1: OOD errors, shift errors, fold errors
        for iteration in range(1, self.num_iterations):
            # out of domain samples
            epsilon_ood = self.epsilon_out(iteration, regime)
            levels[f"OOD(i={iteration})"] = get_bits_of_security_from_error(epsilon_ood)
            # shift queries
            epsilon_shift = self.epsilon_shift(iteration, regime)
            levels[f"Shift(i={iteration})"] = get_bits_of_security_from_error(epsilon_shift)
            # sum check (one error for each round)
            for round in range(1, self.folding_factor + 1):
                epsilon = self.epsilon_fold(iteration, round, regime)
                levels[f"fold(i={iteration},s={round})"] = get_bits_of_security_from_error(epsilon)

        # final error
        epsilon_final = self.epsilon_final(regime)
        levels["fin"] = get_bits_of_security_from_error(epsilon_final)

        # add a "total" level
        levels["total"] = min(list(levels.values()))

        return levels

    def get_code_for_iteration_and_round(self, iteration: int, round: int) -> tuple[float, int]:
        """
        Returns the code for the given iteration and round. That is, this returns a pair (rate, dimension)
        of the code C_{RS}^{i,s} (in notation of Theorem 5.2 in WHIR paper).
        Here, 0<= i <= M-1 is the iteration and 0 <= s <= k is the round.
        """


        assert iteration <= self.num_iterations - 1 and iteration >= 0
        assert round <= self.folding_factor and round >= 0

        # The code is C_{RS}^{i,s} = RS[F, L_i^{(2^s)}, m_i - s]
        # So the dimension is 2^{m_i - s}
        log_dimension = self.log_degrees[iteration] - round
        dimension = 2 ** log_dimension

        # We know what the rate of C_{RS}^{i,0} = RS[F, L_i, m_i] is.
        # Namely, it is 2**(-self.log_inv_rates[i]).
        # The rate of C_{RS}^{i,s} is:
        # 2^{m_i-s} / |L_i^{(2^s)}| =(2^{m_i} / |L_i|) * (2^{-s}/2^{-s}) = 2^{m_i} / |L_i|.
        # So this code has the same rate.
        rate = 2**(-self.log_inv_rates[iteration])
        return (rate, dimension)

    def get_delta_for_iteration(self, iteration: int, regime: ProximityGapsRegime) -> float:
        """
        Returns delta_i, in the notation of the paper, where i = iteration.

        This is determined so that it is small enough for the proximity gaps regime on
        all codes C_{RS}^{i,s}, s <= k.
        """

        # we iterate over all codes, i.e., over all rounds s
        # and for each code, we determine the max delta that is supported,
        # and then take the smallest of them, so that the condition is satisfied.

        delta = 1.0

        for round in range(1, self.folding_factor + 1):
            (rate, dimension) = self.get_code_for_iteration_and_round(iteration, round)
            delta_round = regime.get_proximity_parameter(rate, dimension)
            delta = min(delta, delta_round)

        return delta


    def get_list_size_for_iteration_and_round(self, iteration: int, round: int, regime: ProximityGapsRegime) -> float:
        """
        Returns ell_{i,s}, so that code C_{RS}^{i,s} is (ell_{i,s},delta_i)-list decodable.
        This uses the proximity gaps regime to determine the list size.

        Here, delta_i = get_delta_for_iteration(iteration,regime), i = iteration, s = round.
        """

        assert iteration <= self.num_iterations - 1 and iteration >= 0
        assert round <= self.folding_factor and round >= 0

        # first figure out the delta for this iteration
        delta = self.get_delta_for_iteration(iteration, regime)

        # now compute the list size from it. This requires the code parameters for C_{RS}^{i,s}.
        (rate, dimension) = self.get_code_for_iteration_and_round(iteration, round)
        list_size = regime.get_max_list_size(rate, dimension)

        return list_size

    def get_batching_error(self, regime: ProximityGapsRegime) -> float:
        """
        Returns the error due to the batching step. This depends on whether batching is done
        with powers or with random coefficients.

        This follows https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/whir.rs#L144
        """

        rate = 2 ** (-self.log_inv_rates[0])
        dimension = 2 ** self.log_degrees[0]

        if self.power_batching:
            epsilon = regime.get_error_powers(rate, dimension, self.field, self.batch_size)
        else:
            epsilon = regime.get_error_linear(rate, dimension, self.field)

        # grinding
        epsilon *= 2 ** (-self.grinding_bits_batching)
        return epsilon

    def epsilon_fold(self, iteration: int, round: int, regime: ProximityGapsRegime) -> float:
        """
        Returns the error of a folding round. This is epsilon^fold_{i,s} in the notation
        of the paper (Theorem 5.2 in WHIR paper), where i is the iteration and s <= k is the round.
        """

        # the error has two terms
        epsilon = 0

        # first term is d * ell_{i,s-1} / F
        list_size = self.get_list_size_for_iteration_and_round(iteration, round - 1, regime)
        epsilon += self.constraint_degree * list_size / self.field.F

        # second term is the proximity gaps error err(C_{RS}^{i,s}, 2, delta_i)
        # the WHIR theorem assumes that powers is a prox generator,
        # so we use the error for powers here.
        num_functions = 2
        (rate, dimension) = self.get_code_for_iteration_and_round(iteration, round)
        epsilon += regime.get_error_powers(rate, dimension, self.field, num_functions)

        # grinding
        epsilon *= 2 ** (-self.grinding_bits_folding[iteration][round - 1])

        return epsilon

    def epsilon_out(self, iteration: int, regime: ProximityGapsRegime) -> float:
        """
        Returns the error epsilon^out_i from the paper (Theorem 5.2 in WHIR paper), where i is the iteration.

        Follows https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/errors.rs#L146, as WHIR paper
        does not cover the case of having more than one OOD sample.
        """

        # term is ell_{i,0}^2 * 2^{m_i} / (2F) for one OOD sample.
        # for w many OOD samples, the 2^{m_i} / (2F) part is raised to the power w
        list_size = self.get_list_size_for_iteration_and_round(iteration, 0, regime)
        mi = self.log_degrees[iteration]
        w = self.num_ood_samples[iteration - 1]
        epsilon = list_size * list_size * ((2**mi) / (2 * self.field.F)) ** w

        # grinding
        epsilon *= 2 ** (-self.grinding_bits_ood[iteration - 1])

        return epsilon

    def epsilon_shift(self, iteration: int, regime: ProximityGapsRegime) -> float:
        """
        Returns the error epsilon^shift_i from the paper (Theorem 5.2 in WHIR paper), where i is the iteration.
        """

        assert iteration <= self.num_iterations - 1 and iteration >= 1

        # the error has two terms, both depend on number of queries t_{M-1}
        epsilon = 0
        t = self.num_queries[iteration - 1]

        # first term is (1-delta_{M-1})^{t_{M-1}}
        delta = self.get_delta_for_iteration(iteration - 1, regime)
        epsilon += (1.0 - delta) ** t

        # second term is ell_{i,0} * (t_{i-1}+1)/F
        list_size = self.get_list_size_for_iteration_and_round(iteration, 0, regime)
        epsilon += list_size * (t + 1) / self.field.F

        # grinding
        epsilon *= 2 ** (-self.grinding_bits_queries[iteration - 1])

        return epsilon

    def epsilon_final(self, regime: ProximityGapsRegime) -> float:
        """
        Returns the error epsilon^fin from the paper (Theorem 5.2 in WHIR paper).
        """

        # the error is (1-delta_{M-1})^{t_{M-1}}
        delta = self.get_delta_for_iteration(self.num_iterations - 1, regime)
        epsilon = (1.0 - delta) ** self.num_queries[self.num_iterations - 1]

        # grinding
        epsilon *= 2 ** (-self.grinding_bits_queries[-1])
        return epsilon

    def get_log_grinding_overhead(self) -> float:
        """
        Determine the total grinding overhead to the prover time, which is the sum of all individual grinding
        overheads. The grinding overhead for c bits of grinding is 2^c.
        """
        grinding_sum = 0

        # grinding for batching, queries, OOD
        grinding_sum += 2 ** self.grinding_bits_batching
        grinding_sum += sum([2 ** g for g in self.grinding_bits_queries])
        grinding_sum += sum([2 ** g for g in self.grinding_bits_ood])

        # grinding for folding
        for iteration_g in self.grinding_bits_folding:
            grinding_sum += sum([2 ** g for g in iteration_g])

        return round(math.log2(grinding_sum), 2)


class WHIRBasedVM(zkVM):
    """
    A zkVM that contains one or more WHIR-based circuits.
    """

    def __init__(self, name: str, circuits: list[WHIRBasedCircuit]):
        self._name = name
        self._circuits = circuits

    def get_name(self) -> str:
        return self._name

    def get_circuits(self) -> list[WHIRBasedCircuit]:
        return self._circuits
