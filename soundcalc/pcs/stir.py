
import math
from typing import Optional
from dataclasses import dataclass

from soundcalc.common.fields import FieldParams
from soundcalc.common.utils import (
    apply_grinding,
    get_bits_of_security_from_error,
    get_size_of_merkle_multi_proof_bits,
)
from soundcalc.pcs.pcs import PCS
from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime


def get_STIR_proof_size_bits(
    hash_size_bits: int,
    base_field_bits: int,
    ext_field_bits: int,
    batch_size: int,
    folding_factors: list[int],
    log_degrees: list[int],
    log_inv_rates: list[int],
    num_queries: list[int],
    num_ood_samples: list[int],
    expected: bool,
) -> int:
    """
    Estimate the proof size of STIR in bits by counting prover messages
    (STIR paper, Construction 5.2). Verifier messages are obtained via Fiat-Shamir
    and do not count.

    - `folding_factors` has length M: f_i is folded by 2^{folding_factors[i]}.
    - `log_degrees` has length M+1: log_degrees[i] is the log-degree of f_i, and
      log_degrees[M] is the log-degree of the final polynomial p that is sent in the clear.
    - `log_inv_rates` has length M+1 and gives the log inverse rate of each code.
    - `num_queries` has length M: t_i queries into f_i for i = 0..M-1.
    - `num_ood_samples` has length M-1: s_i out-of-domain samples for f_i, i = 1..M-1.
    """
    num_iterations = len(num_queries)
    assert len(folding_factors) == num_iterations
    assert len(log_degrees) == num_iterations + 1
    assert len(log_inv_rates) == num_iterations + 1
    assert len(num_ood_samples) == num_iterations - 1

    proof_size = 0

    # Prover sends the initial function f_0 (Merkle root).
    # Note: batching does not add roots, we assume all batched functions live in one tree.
    proof_size += hash_size_bits

    # Main loop, i = 1..M-1: prover sends f_i (Merkle root) and the OOD answers f_i(r_out).
    # OOD points are extension field elements, hence so are the answers.
    for i in range(1, num_iterations):
        proof_size += hash_size_bits
        proof_size += num_ood_samples[i - 1] * ext_field_bits

    # Final round: prover sends the polynomial p of degree < 2^{m_M} in the clear.
    proof_size += (2 ** log_degrees[-1]) * ext_field_bits

    # Query phase: for every f_i (i = 0..M-1) the verifier reads t_i folding blocks.
    # As in the paper, an entire block of 2^{k_i} siblings is stored in one Merkle leaf.
    for i in range(num_iterations):
        block_size = 2 ** folding_factors[i]
        domain_size = 2 ** (log_degrees[i] + log_inv_rates[i])
        num_leafs = domain_size // block_size

        # f_0 is the (base field) witness; f_i for i > 0 contain the extension field
        # folding challenges, and so are over the extension field.
        if i == 0:
            element_bits = base_field_bits
            tuple_size = block_size * batch_size
        else:
            element_bits = ext_field_bits
            tuple_size = block_size

        proof_size += get_size_of_merkle_multi_proof_bits(
            num_leafs, num_queries[i], tuple_size, element_bits, hash_size_bits, expected
        )

    return proof_size


@dataclass(frozen=True)
class STIRConfig:
    """
    Configuration for STIR (Arnon, Chiesa, Fenzi, Yogev 2024, https://eprint.iacr.org/2024/390).

    Parameters follow the reference script
    https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/stir.rs
    """

    # The output length of the hash function used, in bits.
    hash_size_bits: int

    # log_2(1/rho) of the initial code RS[F, L_0, 2^{log_degree}].
    #
    # As in WHIR, the rate decreases with every iteration: the degree is divided by 2^{k_i} while
    # the domain only halves, so log_inv_rate grows by (k_i - 1) in iteration i.
    log_inv_rate: int

    # The number of STIR iterations, M. Each iteration folds by 2^{k_i} and shifts to a new domain.
    # The final round sends a polynomial of degree < 2^{log_degree - sum_i k_i} in the clear.
    num_iterations: int

    # Log of the folding factor of each iteration, k_0, ..., k_{M-1} (length M).
    # In iteration i, STIR folds 2^{k_i} evaluations at once (the paper's `k` is 2^{k_i} here).
    folding_factors: list[int]

    # The field that is used.
    field: FieldParams

    # log_2 of the degree bound of the initial polynomial (the code dimension).
    log_degree: int

    # The number of polynomials that are batched before running STIR.
    batch_size: int

    # Power batching (coefficients gamma^i) vs. linear batching (independent coefficients).
    power_batching: bool

    # Grinding bits applied to the batching step.
    grinding_batching_phase: int

    # Grinding bits applied to the initial folding step (iteration 0).
    grinding_bits_folding: int

    # Number of queries t_i into f_i, for i = 0..M-1. Length M.
    num_queries: list[int]

    # Grinding bits for the query / shift step of each iteration. Length M.
    # Entry i reduces the shift error of iteration i+1 (which uses t_i queries), and
    # the last entry reduces the final error.
    grinding_bits_queries: list[int]

    # Number of out-of-domain samples s_i for f_i, for i = 1..M-1. Length M-1.
    num_ood_samples: list[int]

    # Grinding bits for the OOD step of each iteration. Length M-1.
    grinding_bits_ood: list[int]

    # Optional override for the bound *gap*.
    gap_to_radius: Optional[float] = None


class STIR(PCS):
    """
    STIR Polynomial Commitment Scheme.

    Soundness follows the round-by-round analysis of the STIR paper (Lemma 5.4 / Section 5.2),
    with proximity-gap error terms err*(C, k, delta) supplied by the regime.
    """

    label = "STIR"

    def __init__(self, config: STIRConfig):
        self.hash_size_bits = config.hash_size_bits
        self.folding_factors = config.folding_factors
        self.num_iterations = config.num_iterations
        self.field = config.field
        self.batch_size = config.batch_size
        self.power_batching = config.power_batching
        self.grinding_batching_phase = config.grinding_batching_phase
        self.grinding_bits_folding = config.grinding_bits_folding
        self.num_queries = config.num_queries
        self.grinding_bits_queries = config.grinding_bits_queries
        self.num_ood_samples = config.num_ood_samples
        self.grinding_bits_ood = config.grinding_bits_ood
        self.gap_to_radius = config.gap_to_radius
        self.log_degree = config.log_degree

        assert self.batch_size >= 1, "Batch size must be at least 1"
        assert config.log_inv_rate > 0, "Log inverse rate must be > 0 (rate < 1.0)"
        assert config.num_iterations >= 1, "Must have at least 1 iteration"
        assert len(self.folding_factors) == self.num_iterations, (
            f"Expected {self.num_iterations} folding factors, got {len(self.folding_factors)}"
        )
        assert all(k >= 1 for k in self.folding_factors), "Folding factors must be >= 1"

        # Degrees: m_{i+1} = m_i - k_i for i = 0..M-1. The final polynomial has log-degree m_M.
        final_reduction = sum(self.folding_factors)
        assert final_reduction <= config.log_degree, (
            f"Configuration invalid: reducing log-degree {config.log_degree} by "
            f"{final_reduction} (sum of folding factors {self.folding_factors}) "
            "results in a negative log-degree."
        )
        self.log_degrees = [config.log_degree]
        for k in self.folding_factors:
            self.log_degrees.append(self.log_degrees[-1] - k)

        # Rates: the domain halves each iteration (|L_{i+1}| = |L_i| / 2) while the degree is
        # divided by 2^{k_i}, so log_inv_rate grows by k_i - 1 in iteration i.
        self.log_inv_rates = [config.log_inv_rate]
        for k in self.folding_factors:
            self.log_inv_rates.append(self.log_inv_rates[-1] + k - 1)

        # The domain L_i has size 2^{m_i + mu_i}; folding by 2^{k_i} means the relevant
        # smooth subgroup has size 2^{m_i + mu_i - k_i}. All of these must fit the field's 2-adicity.
        required_two_adicity = max(
            self.log_degrees[i] + self.log_inv_rates[i] - self.folding_factors[i]
            for i in range(self.num_iterations)
        )
        assert required_two_adicity <= self.field.two_adicity, (
            f"Field {self.field.name} 2-adicity ({self.field.two_adicity}) is too low.\n"
            f"  - Initial Domain Size: 2^{self.log_degrees[0] + self.log_inv_rates[0]}\n"
            f"  - Folding Factors: {self.folding_factors}\n"
            f"  - Required 2-adicity: {required_two_adicity} (max over i of Domain_i / 2^k_i)"
        )

        # Array length consistency checks
        assert len(self.num_queries) == self.num_iterations, (
            f"Expected {self.num_iterations} query counts, got {len(self.num_queries)}"
        )
        assert len(self.num_ood_samples) == self.num_iterations - 1, (
            f"Expected {self.num_iterations - 1} OOD sample counts, got {len(self.num_ood_samples)}"
        )
        assert len(self.grinding_bits_queries) == self.num_iterations
        assert len(self.grinding_bits_ood) == self.num_iterations - 1

        assert self.grinding_batching_phase >= 0
        assert self.grinding_bits_folding >= 0
        assert all(g >= 0 for g in self.grinding_bits_queries)
        assert all(g >= 0 for g in self.grinding_bits_ood)

        # Every quotient round i = 1..M-1 divides by |G_i| = t_{i-1} + s_i points, so the scheme
        # needs |G_i| < d_i: otherwise the quotient has no positive degree bound and the error
        # terms below are meaningless.
        for i in range(1, self.num_iterations):
            n_g = self.num_queries[i - 1] + self.num_ood_samples[i - 1]
            assert n_g < 2 ** self.log_degrees[i], (
                f"Invalid STIR schedule: |G_{i}| = {n_g} must be below d_{i} = 2^{self.log_degrees[i]}"
            )

        self.log_grinding_overhead = self._get_log_grinding_overhead()

    def get_pcs_security_levels(self, regime: ProximityGapsRegime) -> dict[str, int]:
        """
        Returns PCS-specific security levels for a given regime, one entry per
        round of the round-by-round soundness analysis (STIR paper, Lemma 5.4).
        """
        levels: dict[str, int] = {}

        # Add batching error if applicable
        if self.batch_size > 1:
            epsilon_batch = self._get_batching_error(regime)
            levels["batching"] = get_bits_of_security_from_error(epsilon_batch)

        # Initial folding of f_0 (the only round whose fold error stands alone).
        epsilon_fold = apply_grinding(self._epsilon_fold(0, regime), self.grinding_bits_folding)
        levels["fold(i=0)"] = get_bits_of_security_from_error(epsilon_fold)

        # Main loop, i = 1..M-1: OOD error and shift error (the latter includes the
        # degree correction and the folding of f_i).
        for iteration in range(1, self.num_iterations):
            epsilon_ood = self._epsilon_out(iteration, regime)
            levels[f"OOD(i={iteration})"] = get_bits_of_security_from_error(epsilon_ood)

            epsilon_shift = self._epsilon_shift(iteration, regime)
            levels[f"shift(i={iteration})"] = get_bits_of_security_from_error(epsilon_shift)

        epsilon_final = self._epsilon_final(regime)
        levels["fin"] = get_bits_of_security_from_error(epsilon_final)

        return levels

    def _get_code(self, iteration: int, folded: bool) -> tuple[float, int]:
        """
        Returns (rate, dimension) of the code of iteration i:
        - folded=False: C_i = RS[F, L_i, 2^{m_i}], the code f_i is checked against.
        - folded=True:  RS[F, L_i^{(2^{k_i})}, 2^{m_i - k_i}], the code of Fold(f_i, r). It has the same
          rate as C_i since both degree and domain shrink by 2^{k_i}.
        """
        assert 0 <= iteration < self.num_iterations, f"Iteration {iteration} out of bounds"
        log_dimension = self.log_degrees[iteration]
        if folded:
            log_dimension -= self.folding_factors[iteration]
        assert log_dimension >= 0
        rate = 2 ** (-self.log_inv_rates[iteration])
        return (rate, 2**log_dimension)

    def _get_delta(self, iteration: int, regime: ProximityGapsRegime) -> float:
        """
        Returns delta_i: the largest proximity parameter that the regime supports for both
        C_i and its folded code (the theorem requires delta_i to be below the regime's
        bound for both).
        """
        deltas = [
            regime.get_proximity_parameter(*self._get_code(iteration, folded))
            for folded in (False, True)
        ]
        return min(deltas)

    def _get_list_size(self, iteration: int, regime: ProximityGapsRegime) -> float:
        """Returns ell_i such that C_i is (delta_i, ell_i)-list decodable."""
        return regime.get_max_list_size(*self._get_code(iteration, folded=False))

    def _epsilon_fold(self, iteration: int, regime: ProximityGapsRegime) -> float:
        """
        Error of folding f_i by 2^{k_i} with a single random challenge r:
        err*(RS[F, L_i^{(2^{k_i})}, 2^{m_i-k_i}], 2^{k_i}, delta_i).

        Folding uses the powers 1, r, ..., r^{2^{k_i} - 1}, so we use the regime's powers error
        for 2^{k_i} functions over the folded code. No grinding is applied here; the caller does it.
        """
        (rate, dimension) = self._get_code(iteration, folded=True)
        return regime.get_error_powers(rate, dimension, 2 ** self.folding_factors[iteration])

    def _epsilon_out(self, iteration: int, regime: ProximityGapsRegime) -> float:
        """
        Out-of-domain error for f_i, i = 1..M-1:
            (ell_i^2 / 2) * (2^{m_i} / (|F| - 2^{m_i} / rho_i))^{s_i}
        where s_i = num_ood_samples[i-1].
        """
        assert 1 <= iteration < self.num_iterations
        list_size = self._get_list_size(iteration, regime)
        mi = self.log_degrees[iteration]
        s = self.num_ood_samples[iteration - 1]
        domain_size = 2 ** (mi + self.log_inv_rates[iteration])
        epsilon = (list_size**2 / 2) * ((2**mi) / (self.field.F - domain_size)) ** s
        return apply_grinding(epsilon, self.grinding_bits_ood[iteration - 1])

    def _epsilon_shift(self, iteration: int, regime: ProximityGapsRegime) -> float:
        """
        Shift error of iteration i = 1..M-1, three terms:
          1. (1 - delta_{i-1})^{t_{i-1}}: the t_{i-1} queries into f_{i-1} miss the disagreement.
          2. err*(C_i, t_{i-1} + s_{i-1}, delta_i): degree correction / quotient combining
             of the t_{i-1} in-domain and s_{i-1} out-of-domain answers with powers of a challenge.
          3. err*(folded C_i, 2^{k_i}, delta_i): folding f_i for the next iteration.
        """
        assert 1 <= iteration < self.num_iterations
        t = self.num_queries[iteration - 1]
        s = self.num_ood_samples[iteration - 1]

        epsilon = 0.0

        delta_prev = self._get_delta(iteration - 1, regime)
        assert 0 < delta_prev < 1.0, f"Invalid delta {delta_prev} for shift error"
        epsilon += (1.0 - delta_prev) ** t

        (rate, dimension) = self._get_code(iteration, folded=False)
        epsilon += regime.get_error_powers(rate, dimension, t + s)

        epsilon += self._epsilon_fold(iteration, regime)

        return apply_grinding(epsilon, self.grinding_bits_queries[iteration - 1])

    def _epsilon_final(self, regime: ProximityGapsRegime) -> float:
        """Final error (1 - delta_{M-1})^{t_{M-1}}."""
        t_final = self.num_queries[-1]
        delta = self._get_delta(self.num_iterations - 1, regime)
        assert 0 < delta < 1.0, f"Invalid delta {delta} for final round"
        epsilon = (1.0 - delta) ** t_final
        return apply_grinding(epsilon, self.grinding_bits_queries[-1])

    def _get_log_grinding_overhead(self) -> float:
        """log2 of the total prover grinding overhead, sum of 2^bits over all grinding steps."""
        grinding_sum = 0
        grinding_sum += 2**self.grinding_batching_phase
        grinding_sum += 2**self.grinding_bits_folding
        grinding_sum += sum(2**g for g in self.grinding_bits_queries)
        grinding_sum += sum(2**g for g in self.grinding_bits_ood)
        return round(math.log2(grinding_sum), 2)

    def _get_proof_size_bits(self, expected: bool) -> int:
        return get_STIR_proof_size_bits(
            hash_size_bits=self.hash_size_bits,
            base_field_bits=self.field.base_field_element_size_bits(),
            ext_field_bits=self.field.extension_field_element_size_bits(),
            batch_size=self.batch_size,
            folding_factors=self.folding_factors,
            log_degrees=self.log_degrees,
            log_inv_rates=self.log_inv_rates,
            num_queries=self.num_queries,
            num_ood_samples=self.num_ood_samples,
            expected=expected,
        )

    def get_rate(self) -> float:
        return 2 ** (-self.log_inv_rates[0])

    def get_dimension(self) -> int:
        return 2 ** self.log_degrees[0]

    def get_trace_length(self) -> int:
        return 2 ** self.log_degrees[0]

    def get_parameter_summary(self) -> str:
        lines: list[str] = []
        lines.append("")
        lines.append("```")

        params = {
            "hash_size_bits": self.hash_size_bits,
            "batch_size": self.batch_size,
            "gap_to_radius": self.gap_to_radius,
            "power_batching": self.power_batching,
            "grinding_batching_phase": self.grinding_batching_phase,
            "grinding_bits_folding": self.grinding_bits_folding,
            "num_iterations": self.num_iterations,
            "field": self.field.to_string(),
        }
        key_width = max(len(k) for k in params)
        for k, v in params.items():
            lines.append(f"  {k:<{key_width}} : {v}")

        lines.append("")
        lines.append("  Per-round parameters:")
        lines.append(f"    log_degree            : {self.log_degree}")
        lines.append(f"    folding_factors       : {self.folding_factors}")
        lines.append(f"    log_degrees           : {self.log_degrees}")
        lines.append(f"    log_inv_rates         : {self.log_inv_rates}")
        lines.append(f"    num_queries           : {self.num_queries}")
        lines.append(f"    grinding_bits_queries : {self.grinding_bits_queries}")
        lines.append(f"    num_ood_samples       : {self.num_ood_samples}")
        lines.append(f"    grinding_bits_ood     : {self.grinding_bits_ood}")
        lines.append("")
        lines.append(
            f"  Total grinding overhead (sum of 2^grinding_bits) = 2^({self.log_grinding_overhead})"
        )

        lines.append("```")
        return "\n".join(lines)

    def get_report_parameter_lines(self) -> list[str]:
        batching = "Powers" if self.power_batching else "Affine"
        return [
            f"- Hash size (bits): {self.hash_size_bits}",
            f"- Field: {self.field.to_string()}",
            f"- Iterations (M): {self.num_iterations}",
            f"- Folding factors (k_i): {self.folding_factors}",
            f"- Initial rate (ρ): $2^{{-{self.log_inv_rates[0]}}}$",
            f"- Initial log-degree: {self.log_degree}",
            f"- Batch size: {self.batch_size}",
            f"- Batching: {batching}",
            f"- Queries per iteration: {self.num_queries}",
            f"- OOD samples per iteration: {self.num_ood_samples}",
            f"- Total grinding overhead log2: {self.log_grinding_overhead}",
        ]
