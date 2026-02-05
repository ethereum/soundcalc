
import math
from typing import Optional
from dataclasses import dataclass

from soundcalc.common.fields import FieldParams
from soundcalc.common.utils import (
    apply_grinding,
    get_bits_of_security_from_error,
    get_size_of_merkle_multi_proof_bits,
    get_size_of_merkle_proof_bits,
)
from soundcalc.pcs.pcs import PCS
from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime


@dataclass(frozen=True)
class WHIRConfig:
    """
    Configuration for WHIR PCS.
    """

    # The output length of the hash function that is used in bits
    # Note: this concerns the hash function used for Merkle trees
    hash_size_bits: int

    # Parameters are inspired by Giacomo's script here for inspiration
    # https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/whir.rs

    # The base-2 logarithm of the inverse rate of the initial code.
    #
    # In the paper, the rate is denoted by ρ. This parameter represents:
    #
    # \begin{equation}
    #    \text{log_inv_rate} = \log_2(\frac{1}{ρ})
    # \end{equation}
    #
    # ### Mathematical Definition
    #
    # Per **Definition 4.2** (Reed-Solomon codes):
    # - Let $2^m$ be the degree of the polynomial (size of message).
    # - Let $|L|$ be the size of the evaluation domain (size of codeword).
    #
    # The rate is defined as ρ := $2^m / |L|$.
    #
    # Therefore, this parameter calculates the expansion factor in bits:
    # \begin{equation}
    #   \text{log_inv_rate} = \log_2(|L|) - m
    # \end{equation}
    #
    # ### Examples
    #
    # - If ρ = 1/2: $\log_2(2) = 1$
    # - If ρ = 1/4: $\log_2(4) = 2$
    # - If ρ = 1/16: $\log_2(16) = 4$
    #
    # **NOTE**: The rate in WHIR decreases (becomes smaller) with every iteration.
    #
    # This parameter sets only the initial rate ρ.
    log_inv_rate: int

    # The total number of WHIR iterations, denoted by $M$ in the paper.
    #
    # This parameter dictates how many reduction steps are performed to reduce
    # the polynomial from $m$ variables down to a constant size.
    #
    # **NOTE**: One WHIR iteration corresponds to multiple sumcheck rounds.
    #
    # A single WHIR iteration reduces the number of variable $m$ by $k$.
    # To do this, it runs a sumcheck protocol as a sub-routine.
    #
    # Therefore, one iteration consists of:
    #
    # 1. Sumcheck phase ($k$ rounds):
    #    The Prover and Verifier interact $k$ distinct times.
    #    In each inner round, exactly one variable is eliminated.
    #
    # 2. Sampling phase:
    #    The Verifier requests one or multiple Out-of-Domain (OOD) evaluations.
    #
    # 3. Folding phase:
    #    The Prover computes and sends the new, smaller function.
    #
    # See Construction 5.1 for the flow of the main loop.
    num_iterations: int

    # The logarithmic reduction factor for each WHIR iteration.
    #
    # In the paper, this corresponds to the sequence $k_0, ..., k_{M-1}$
    #
    # This parameter dictates how aggressively the polynomial is compressed in every iteration.
    #
    # ### Mathematical Definition
    #
    # If the folding factor is $k$:
    #
    # 1. Polynomial Degree Reduction:
    #    The number of variables decreases by $k$.
    #    \begin{equation}
    #       m_{new} = m_{old} - k
    #    \end{equation}
    #
    # 2. Evaluation Domain Reduction:
    #    The domain size reduces by a factor of 2.
    #    \begin{equation}
    #       |L_{new}| = |L_{old}| / 2
    #    \end{equation}
    #
    # ### Impact on Rate
    #
    # Because the degree shrinks faster ($2^k$) than the domain ($2^1$),
    # the rate of the code decreases with every step.
    # \begin{equation}
    #   \rho_{new} = 2^{1-k} ⋅ \rho_{old}
    # \end{equation}
    #
    # ### Rust Calculator Note
    #
    # This corresponds to `folding_factors` in the Rust implementation.
    #
    # See `WhirParameters::fixed_domain_shift` in the reference script:
    # https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/whir.rs#L72
    #
    # While the paper allows for variable $k_i$, this calculator (like the
    # Rust script) currently assumes a constant $k$ for all iterations.
    folding_factor: int

    # The field that is used
    field: FieldParams

    # The initial number of variables of the multilinear polynomial.
    #
    # In the paper, this is denoted as $m$ (or $m_0$).
    #
    # This parameter effectively defines the size of the witness/message being proven.
    #
    # ### Mathematical Definition
    #
    # Per Definition 4.2 (Reed-Solomon codes), there is an equivalence
    # between the univariate degree $d$ and the number of variables $m$:
    #
    # \begin{equation}
    #    d = 2^m ⇒ m = \log_2(d)
    # \end{equation}
    #
    # Thus, the code is defined as evaluations of polynomials with degree strictly less than $2^m$.
    #
    # ### Evolution
    #
    # This parameter sets the initial $m$. As the protocol proceeds through
    # iterations of folding, this value decreases:
    #
    # \begin{equation}
    #    m_{next} = m_{current} - k
    # \end{equation}
    #
    # The protocol ends when $m$ is reduced to a small constant.
    log_degree: int

    # The number of polynomials verified simultaneously.
    #
    # In the paper, this is denoted as $t$ in **Construction 5.5** (Section 5.2).
    #
    # This parameter enables the protocol to verify multiple instances with a single proof
    # by taking a random linear combination.
    #
    # ### Mathematical Definition
    #
    # Instead of verifying $t$ functions individually, the protocol verifies:
    # \begin{equation}
    #    f_{batch} = \sum_{i=0}^{t-1} c_i ⋅ f_i
    # \end{equation}
    #
    # ### Coefficient Selection
    #
    # The generation of coefficients $c_i$ depends on the `power_batching` parameter:
    # - Power Batching: $c_i = γ^i$ (as in Construction 5.5).
    # - Linear Batching: $c_i = r_i$ (fully independent random values).
    #
    # ### Rust Calculator Note
    #
    # See `WhirParameters` in the reference script:
    # https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/whir.rs#L144
    batch_size: int

    # A flag determining the strategy for generating batching coefficients.
    #
    # This controls how coefficients $c_i$ are selected when computing the linear
    # combination $f_{batch} = \sum c_i ⋅ f_i$.
    #
    # ### Strategies
    #
    # - True (Power Batching):
    #   Coefficients are powers of a single random challenge $\gamma$.
    #   \begin{equation}
    #      c_i = \gamma^i
    #   \end{equation}
    #   This matches **Construction 5.5** in the paper.
    #
    # - False (Linear Batching):
    #   Coefficients are independent random values $r_i$.
    #   \begin{equation}
    #      c_i = r_i
    #   \end{equation}
    #   This provides stronger soundness at the cost of consuming more randomness.
    power_batching: bool

    # The number of grinding (Proof-of-Work) bits applied to the batching step.
    #
    # ### Definition
    #
    # Grinding forces the Prover to expend computational work to generate a specific
    # prefix for the hash of the transcript.
    #
    # This reduces the soundness error probability by a factor of $2^{\text{bits}}$.
    #
    # This parameter reduces the specific error introduced by the batching linear combination.
    grinding_bits_batching: int

    # The degree of the polynomial constraints being verified.
    #
    # In the paper, this is denoted as $d$ in Construction 5.1.
    #
    # ### Mathematical Definition
    #
    # \begin{equation}
    #    d = \max(d^*, 3)
    # \end{equation}
    #
    # Where $d^*$ is derived from the weight polynomial $\hat{w}$:
    # \begin{equation}
    #    d^* = 1 + \deg_Z(\hat{w}) + \max_i \deg_{X_i}(\hat{w})
    # \end{equation}
    #
    # This parameter impacts the proof size (sumcheck polynomials have degree $d$)
    # and the soundness error term $\frac{d ⋅ ℓ}{|F|}$.
    constraint_degree: int

    # A 2D array of grinding bits for the folding steps.
    #
    # This applies Proof-of-Work to reduce the error of the Sumcheck folding rounds.
    #
    # ### Structure
    #
    # - Outer Dimension: Iterations ($i$ from $0$ to $M-1$).
    # - Inner Dimension: Sumcheck Rounds ($s$ from $1$ to $k$).
    #
    # ### Impact on Soundness
    #
    # This directly reduces the error term $ϵ^{fold}_{i,s}$ defined in
    # Theorem 5.2 (round-by-round soundness), where:
    # - $0 ≤ i < M$
    # - $1 ≤ s ≤ k$
    grinding_bits_folding: list[list[int]]

    # The number of verification queries performed per iteration.
    #
    # In the paper, this corresponds to the sequence $t_0, ..., t_{M-1}$
    # defined in Construction 5.1.
    #
    # This list has length $M$ (one count for each iteration).
    #
    # ### Impact
    #
    # - Soundness: More queries reduce the probability that the Verifier misses an
    #   inconsistency ($≈(1-δ)^t$).
    # - Proof Size: Each query requires a Merkle path, increasing proof size.
    num_queries: list[int]

    # A list of grinding bits applied to the query phases.
    #
    # This list has length $M$ (matching `num_queries`).
    #
    # ### Impact on soundness
    #
    # This reduces the error terms associated with:
    # 1. The Shift checks ($ϵ^{shift}_i$).
    # 2. The Final check ($ϵ^{fin}$).
    #
    # This allows trading off fewer queries (smaller proof) for more prover computation time.
    grinding_bits_queries: list[int]

    # The number of Out-of-Domain (OOD) samples requested per iteration.
    #
    # In the paper, this corresponds to the sample $z_{i,0}$ in Construction 5.1.
    #
    # This list has length $M-1$.
    #
    # ### Mechanism
    #
    # The verifier samples random points $z$ outside the evaluation domain to force
    # consistency between the folded functions $f_i$ and their multilinear extensions.
    num_ood_samples: list[int]

    # A list of grinding bits applied to the OOD sampling phases.
    #
    # This list has length $M-1$ (matching `num_ood_samples`).
    #
    # ### Impact on Soundness
    #
    # This reduces the error term $ϵ^{out}_i$ in Theorem 5.2.
    #
    # It mitigates the risk of collision where distinct polynomials might
    # agree on the sampled OOD point.
    grinding_bits_ood: list[int]

    # Optional override for the bound *gap*.
    # (This is useful to pin fixed parameters in TOML configs.)
    gap_to_radius: Optional[float] = None

class WHIR(PCS):
    """
    WHIR Polynomial Commitment Scheme.
    """

    def __init__(self, config: WHIRConfig):
        """
        Given a config, compute all the parameters relevant for the PCS.
        """
        # Inherit parameters from the given config
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
        self.gap_to_radius = config.gap_to_radius

        # Parameter validity checks

        # Paper Construction 5.1: d = max(d*, 3).
        #
        # A constraint degree < 3 is degenerate in the WHIR protocol structure.
        assert self.constraint_degree >= 3, (
            f"Constraint degree must be >= 3 per Construction 5.1, got {self.constraint_degree}"
        )

        assert self.batch_size >= 1, "Batch size must be at least 1"

        # determine all rates (in contrast to FRI, these change over the iterations)
        # this also involves determining all log degrees
        assert config.log_inv_rate > 0, "Log inverse rate must be > 0 (rate < 1.0)"
        assert config.folding_factor >= 1, (
            "Folding factor must be >= 1 to reduce degree"
        )
        assert config.num_iterations >= 1, "Must have at least 1 iteration"

        # Calculate the log_degree (m) for every iteration 0..M
        #
        # This corresponds to the sequence $m_0, ..., m_M$ in the paper.
        #
        # Formula: m_i = m_0 - i * k
        self.log_degree = config.log_degree

        # Ensure the final polynomial does not end up with a negative number of variables.
        #
        # This implies m_0 >= M * k
        final_reduction = self.num_iterations * self.folding_factor
        assert final_reduction <= config.log_degree, (
            f"Configuration invalid: Reducing {config.log_degree} variables by "
            f"{final_reduction} ({self.num_iterations} iters * {self.folding_factor} fold) "
            "results in a negative number of variables."
        )

        self.log_degrees = [
            config.log_degree - i * self.folding_factor
            for i in range(self.num_iterations + 1)
        ]

        # Calculate `log_inv_rate` (expansion factor) for every iteration.
        #
        # Implements a fixed domain shift: Domain halves (rate * 2), Degree / 2^k (rate / 2^k).
        # - Net change to inv_rate: * 2^(k-1).
        # - Log change: + (k - 1).
        self.log_inv_rates = [
            config.log_inv_rate + i * (self.folding_factor - 1)
            for i in range(self.num_iterations + 1)
        ]

        # Domain validity check

        # Calculate the initial domain size in bits: |L| = 2^{m + log_inv_rate}
        #
        # This includes the initial variable count plus the rate expansion.
        initial_domain_log_size = self.log_degrees[0] + self.log_inv_rates[0]

        # We use Interleaved Reed-Solomon codes (Lemma 4.4).
        #
        # We effectively decompose the polynomial into 2^k smaller polynomials
        # (where k = folding_factor).
        #
        # The FFTs are performed on the smaller domain of size |L| / 2^k.
        # Therefore, the field's 2-adicity only needs to support this smaller domain.
        #
        # Requirement: log2(|L|) - k <= two_adicity
        required_two_adicity = initial_domain_log_size - self.folding_factor

        assert required_two_adicity <= self.field.two_adicity, (
            f"Field {self.field.name} 2-adicity ({self.field.two_adicity}) is too low.\n"
            f"  - Logical Domain Size: 2^{initial_domain_log_size}\n"
            f"  - Folding Factor: {self.folding_factor}\n"
            f"  - Required 2-adicity: {required_two_adicity} (Domain / 2^k)"
        )

        # Array length consistency checks

        # The Main Loop (Construction 5.1) runs for i = 1 to M-1.
        #
        # OOD samples happen inside this loop.
        assert len(self.num_ood_samples) == self.num_iterations - 1, (
            f"Expected {self.num_iterations - 1} OOD sample configs, got {len(self.num_ood_samples)}"
        )

        assert len(self.log_degrees) == self.num_iterations + 1
        assert len(self.log_inv_rates) == self.num_iterations + 1
        # Queries happen in every iteration (0 to M-1).
        assert len(self.num_queries) == self.num_iterations, (
            f"Expected {self.num_iterations} query counts, got {len(self.num_queries)}"
        )

        # ensure that grinding parameters have correct length
        assert len(self.grinding_bits_ood) == self.num_iterations - 1
        assert len(self.grinding_bits_queries) == self.num_iterations
        assert len(self.grinding_bits_folding) == self.num_iterations

        assert self.grinding_bits_batching >= 0, "Batching grinding bits must be >= 0"
        assert all(g >= 0 for g in self.grinding_bits_queries), (
            "Query grinding bits must be >= 0"
        )
        assert all(g >= 0 for g in self.grinding_bits_ood), (
            "OOD grinding bits must be >= 0"
        )

        for i, grinding_bits_folding_iter in enumerate(self.grinding_bits_folding):
            # Each iteration has a sumcheck phase with exactly 'folding_factor' rounds.
            assert len(grinding_bits_folding_iter) == self.folding_factor, (
                f"Iteration {i}: Expected {self.folding_factor} folding grinding entries, "
                f"got {len(grinding_bits_folding_iter)}"
            )
            assert all(g >= 0 for g in grinding_bits_folding_iter), (
                f"Folding grinding bits in iter {i} must be >= 0"
            )

        # determine the total grinding overhead (sum of 2^grinding_bits)
        self.log_grinding_overhead = self._get_log_grinding_overhead()

    def get_pcs_security_levels(self, regime: ProximityGapsRegime) -> dict[str, int]:
        """
        Returns PCS-specific security levels for a given regime.
        """
        levels: dict[str, int] = {}

        # add an error from the batching step
        if self.batch_size > 1:
            epsilon_batch = self._get_batching_error(regime)
            levels["batching"] = get_bits_of_security_from_error(epsilon_batch)

        # Initial Iteration (i=0)
        #
        # Construction 5.1: "1. Initial sumcheck... For l = 1...k0"
        # This iteration only contains folding (sumcheck), no OOD/Shift.
        for round_s in range(1, self.folding_factor + 1):
            epsilon = self._epsilon_fold(iteration=0, round=round_s, regime=regime)
            levels[f"fold(i=0,s={round_s})"] = get_bits_of_security_from_error(epsilon)

        # Main Loop (i=1 to M-1)
        #
        # Construction 5.1: "2. Main loop: For i = 1...M-1"
        # For each iteration i = 1, ... M - 1: OOD errors, shift errors, fold errors
        for iteration in range(1, self.num_iterations):
            # out of domain samples
            epsilon_ood = self._epsilon_out(iteration, regime)
            levels[f"OOD(i={iteration})"] = get_bits_of_security_from_error(epsilon_ood)

            # shift queries
            epsilon_shift = self._epsilon_shift(iteration, regime)
            levels[f"Shift(i={iteration})"] = get_bits_of_security_from_error(
                epsilon_shift
            )

            # sum check (one error for each round)
            for round in range(1, self.folding_factor + 1):
                epsilon = self._epsilon_fold(iteration, round, regime)
                levels[f"fold(i={iteration},s={round})"] = (
                    get_bits_of_security_from_error(epsilon)
                )

        # final error
        # Construction 5.1: "3. Check final polynomial..."
        epsilon_final = self._epsilon_final(regime)
        levels["fin"] = get_bits_of_security_from_error(epsilon_final)

        return levels

    def _get_code_for_iteration_and_round(
        self, iteration: int, round: int
    ) -> tuple[float, int]:
        """
        Returns the code for the given iteration and round. That is, this returns a pair (rate, dimension)
        of the code C_{RS}^{i,s} (in notation of Theorem 5.2 in WHIR paper).
        Here, 0<= i <= M-1 is the iteration and 0 <= s <= k is the round.
        """

        # Bound checks
        assert 0 <= iteration < self.num_iterations, (
            f"Iteration {iteration} out of bounds"
        )
        assert 0 <= round <= self.folding_factor, f"Round {round} out of bounds"

        # The code is C_{RS}^{i,s} = RS[F, L_i^{(2^s)}, m_i - s]
        # So the dimension is 2^{m_i - s}
        log_dimension = self.log_degrees[iteration] - round
        assert log_dimension >= 0, "Log dimension cannot be negative"
        dimension = 2**log_dimension

        # We know what the rate of C_{RS}^{i,0} = RS[F, L_i, m_i] is.
        # Namely, it is 2**(-self.log_inv_rates[i]).
        # The rate of C_{RS}^{i,s} is:
        # 2^{m_i-s} / |L_i^{(2^s)}| =(2^{m_i} / |L_i|) * (2^{-s}/2^{-s}) = 2^{m_i} / |L_i|.
        # So this code has the same rate.
        rate = 2 ** (-self.log_inv_rates[iteration])
        return (rate, dimension)

    def _get_delta_for_iteration(
        self, iteration: int, regime: ProximityGapsRegime
    ) -> float:
        """
        Returns delta_i, in the notation of the paper, where i = iteration.

        This is determined so that it is small enough for the proximity gaps regime on
        all codes C_{RS}^{i,s}, s <= k.
        """

        # we iterate over all codes, i.e., over all rounds s
        # and for each code, we determine the max delta that is supported,
        # and then take the smallest of them, so that the condition is satisfied.

        assert 0 <= iteration < self.num_iterations, "Iteration out of bounds"

        delta = 1.0

        # The range must be 0 <= s <= k (inclusive).
        for round in range(0, self.folding_factor + 1):
            (rate, dimension) = self._get_code_for_iteration_and_round(iteration, round)
            delta_round = regime.get_proximity_parameter(rate, dimension)
            delta = min(delta, delta_round)

        return delta

    def _get_list_size_for_iteration_and_round(
        self, iteration: int, round: int, regime: ProximityGapsRegime
    ) -> float:
        """
        Returns ell_{i,s}, so that code C_{RS}^{i,s} is (ell_{i,s},delta_i)-list decodable.
        This uses the proximity gaps regime to determine the list size.

        Here, delta_i = get_delta_for_iteration(iteration,regime), i = iteration, s = round.
        """

        assert 0 <= iteration < self.num_iterations, "Iteration out of bounds"
        assert 0 <= round <= self.folding_factor, "Round out of bounds"

        # Get Code Parameters
        #
        # We need the Rate and Dimension of C_{RS}^{i,s}
        (rate, dimension) = self._get_code_for_iteration_and_round(iteration, round)

        # Determine List Size
        #
        # We ask the regime for the maximum list size possible for this specific code.
        list_size = regime.get_max_list_size(rate, dimension)

        return list_size

    def _get_batching_error(self, regime: ProximityGapsRegime) -> float:
        """
        Returns the error due to the batching step. This depends on whether batching is done
        with powers or with random coefficients.

        This follows https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/whir.rs#L144
        """

        (rate, dimension) = self._get_code_for_iteration_and_round(0, 0)

        # Calculate Base Error
        #
        # The error depends on how we combine the polynomials.
        if self.power_batching:
            # Power Batching: sum c^i * f_i
            # Error is typically proportional to (batch_size - 1) * list_size / |F|
            epsilon = regime.get_error_powers(rate, dimension, self.batch_size)
        else:
            # Linear Batching: sum r_i * f_i (where r_i are independent)
            # Error is typically list_size / |F| (independent of batch_size)
            epsilon = regime.get_error_linear(rate, dimension)

        # Apply Grinding
        #
        # Reducing error by expending computational work (2^-bits).
        epsilon = apply_grinding(epsilon, self.grinding_bits_batching)
        return epsilon

    def _epsilon_fold(
        self, iteration: int, round: int, regime: ProximityGapsRegime
    ) -> float:
        """
        Returns the error of a folding round. This is epsilon^fold_{i,s} in the notation
        of the paper (Theorem 5.2 in WHIR paper), where i is the iteration and s <= k is the round.
        """

        # Explicitly check that s is within the valid range [1, k].
        assert 1 <= round <= self.folding_factor, (
            f"Folding round {round} out of bounds (must be 1..{self.folding_factor})"
        )

        # the error has two terms
        epsilon = 0

        # first term is d * ell_{i,s-1} / F
        list_size = self._get_list_size_for_iteration_and_round(
            iteration, round - 1, regime
        )
        epsilon += self.constraint_degree * list_size / self.field.F

        # second term is the proximity gaps error err(C_{RS}^{i,s}, 2, delta_i)
        # the WHIR theorem assumes that powers is a prox generator,
        # so we use the error for powers here.
        num_functions = 2
        (rate, dimension) = self._get_code_for_iteration_and_round(iteration, round)
        epsilon += regime.get_error_powers(rate, dimension, num_functions)

        # Apply Grinding
        # Reducing error by expending computational work.
        #
        # Note: round is 1-based, but the grinding array is 0-based.
        epsilon = apply_grinding(epsilon, self.grinding_bits_folding[iteration][round - 1])

        return epsilon

    def _epsilon_out(self, iteration: int, regime: ProximityGapsRegime) -> float:
        """
        Returns the error epsilon^out_i from the paper (Theorem 5.2 in WHIR paper), where i is the iteration.

        Follows https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/errors.rs#L146, as WHIR paper
        does not cover the case of having more than one OOD sample.
        """

        # OOD samples occur in iterations 1 to M-1.
        assert 1 <= iteration < self.num_iterations, (
            f"OOD Error applies to iterations 1..{self.num_iterations - 1}, got {iteration}"
        )

        # term is ell_{i,0}^2 * 2^{m_i} / (2F) for one OOD sample.
        # for w many OOD samples, the 2^{m_i} / (2F) part is raised to the power w
        list_size = self._get_list_size_for_iteration_and_round(iteration, 0, regime)
        mi = self.log_degrees[iteration]
        w = self.num_ood_samples[iteration - 1]
        epsilon = list_size * list_size * ((2**mi) / (2 * self.field.F)) ** w

        # grinding
        epsilon = apply_grinding(epsilon, self.grinding_bits_ood[iteration - 1])

        return epsilon

    def _epsilon_shift(self, iteration: int, regime: ProximityGapsRegime) -> float:
        """
        Returns the error epsilon^shift_i from the paper (Theorem 5.2 in WHIR paper), where i is the iteration.
        """

        # Bound check
        assert 1 <= iteration < self.num_iterations, "Shift Error applies to Main Loop"

        # the error has two terms, both depend on number of queries t_{M-1}
        epsilon = 0
        t = self.num_queries[iteration - 1]

        # first term is (1-delta_{M-1})^{t_{M-1}}
        delta = self._get_delta_for_iteration(iteration - 1, regime)
        epsilon += (1.0 - delta) ** t

        # second term is ell_{i,0} * (t_{i-1}+1)/F
        list_size = self._get_list_size_for_iteration_and_round(iteration, 0, regime)
        epsilon += list_size * (t + 1) / self.field.F

        # grinding
        epsilon = apply_grinding(epsilon, self.grinding_bits_queries[iteration - 1])

        return epsilon

    def _epsilon_final(self, regime: ProximityGapsRegime) -> float:
        """
        Returns the error epsilon^fin from the paper (Theorem 5.2 in WHIR paper).
        """

        t_final = self.num_queries[-1]
        grinding_bits = self.grinding_bits_queries[-1]

        # the error is (1-delta_{M-1})^{t_{M-1}}
        delta = self._get_delta_for_iteration(self.num_iterations - 1, regime)

        # Sanity Check: If delta is 1.0, the code has no redundancy, and security is 0.
        # (Technically error=0, but this implies a broken config).
        assert 0 < delta < 1.0, f"Invalid delta {delta} for final round"

        epsilon = (1.0 - delta) ** t_final

        # grinding
        epsilon = apply_grinding(epsilon, grinding_bits)
        return epsilon

    def _get_log_grinding_overhead(self) -> float:
        """
        Determine the total grinding overhead to the prover time, which is the sum of all individual grinding
        overheads. The grinding overhead for c bits of grinding is 2^c.
        """
        grinding_sum = 0

        # grinding for batching, queries, OOD
        grinding_sum += 2**self.grinding_bits_batching
        grinding_sum += sum([2**g for g in self.grinding_bits_queries])
        grinding_sum += sum([2**g for g in self.grinding_bits_ood])

        # grinding for folding
        for iteration_g in self.grinding_bits_folding:
            grinding_sum += sum([2**g for g in iteration_g])

        # Calculate the effective bits of security added to the Prover time.
        #
        # Sanity check:
        # - Since we have at least 1 iteration and batching, grinding_sum >= 2.0, so log2 is safe.
        assert grinding_sum > 0, "Impossible: Total work cannot be zero"

        return round(math.log2(grinding_sum), 2)

    def _get_proof_size_bits(self, expected: bool) -> int:
        # We estimate the proof size by looking at the WHIR paper, counting sizes of prover messages.
        # Note that verifier messages do not count into proof size, as they are obtained from Fiat-Shamir.
        # Here, messages are either field elements, polynomials, functions, or function evaluations.
        #
        # Field elements are included directly in the proof;
        # Polynomials are sent by the vector of their coefficients;
        # Functions are sent in the form of a Merkle root;
        # Function evaluations are sent in the form of a Merkle path;

        # Let us distinguish between base and extension field elements.
        # - The base field is used for the initial trace (f_0).
        # - The extension field is used for:
        #    - all subsequent folded functions (f_1...f_M),
        #    - sumcheck polynomials,
        #    - OOD answers.
        base_field_bits = self.field.base_field_element_size_bits()
        ext_field_bits = self.field.extension_field_element_size_bits()

        # We start with a fresh proof size
        proof_size = 0

        # Initial commitment
        #
        # Prover sends the initial function (Merkle root)
        proof_size += self.hash_size_bits

        # Initial Sumcheck (Iteration 0)
        #
        # The Prover sends 'folding_factor' (k) univariate polynomials.
        #
        # NOTATION (WHIR Paper, Construction 5.1):
        # The paper defines the polynomial h(X) as belonging to F^{<d*}[X].
        # Let 'd' (`constraint_degree`) represent this bound d*.
        #
        # 1. Actual degree: Strictly less than d => max degree is (d - 1).
        # 2. Naive coefficients: A polynomial of degree (d - 1) needs d coefficients.
        #
        # OPTIMIZATION (Section 3.1 of Gruen 2024: https://eprint.iacr.org/2024/108.pdf):
        #
        # In the sumcheck protocol, the Verifier already knows the sum for the current round:
        #
        #     claim = h(0) + h(1)
        #
        # This linear constraint fixes one degree of freedom. The Prover sends only
        # (d-1) evaluations (e.g., at points 0, 2, ..., d-1), and the Verifier derives
        # the missing value h(1) locally via:
        #
        #     h(1) = claim - h(0)
        #
        # Therefore, we transmit exactly (d-1) elements instead of d.
        proof_size += (
            self.folding_factor * (self.constraint_degree - 1) * ext_field_bits
        )

        # Main loop, runs for i = 1 to i = M - 1
        for i in range(1, self.num_iterations):
            # In each iteration:
            # - Send a function,
            # - Do OOD samples,
            # - Do sumcheck rounds.

            # Send function commitment (f_i)
            proof_size += self.hash_size_bits

            # Send evaluations for the OOD samples
            #
            # Prover sends y = f_i(z). Since z is an extension field element, y is too.
            proof_size += self.num_ood_samples[i - 1] * ext_field_bits

            # Sumcheck rounds
            #
            # The Prover sends 'folding_factor' (k) univariate polynomials per iteration.
            #
            # See above for NOTATION and OPTIMIZATION used here
            proof_size += (
                self.folding_factor * (self.constraint_degree - 1) * ext_field_bits
            )

        # Prover sends the final polynomial.
        #
        # This is a multi-linear polynomial in m_M variables, i.e., it has 2^{m_M} coefficients.
        assert self.log_degrees
        proof_size += (2 ** self.log_degrees[-1]) * ext_field_bits

        # Decision phase: we query each function f_0,...,f_{M-1} that the prover sent
        # at t_i groups of points. Each group is a set of "folding siblings", also
        # called a "Block" in the literature. As in the WHIR paper, we assume that
        # an entire block is stored in the Merkle leaf. That is, we simply count
        # t_i Merkle leafs.

        # We query t_i paths for every iteration i from 0 to M-1.
        assert len(self.num_queries) == self.num_iterations
        for i in range(self.num_iterations):
            domain_size = 2 ** (self.log_degrees[i] + self.log_inv_rates[i])
            block_size = 2**self.folding_factor
            num_leafs = domain_size / block_size

            # The element size depends on the iteration:
            # - Iteration 0: The witness f_0 is over the base field.
            # - Iteration >0: The folded functions f_i contain alpha (extension challenge),
            #   so they are over the Extension Field.
            if i == 0:
                current_element_bits = base_field_bits
            else:
                current_element_bits = ext_field_bits

            # Compute the size of one query (path + leaf data)
            #
            # A leaf in WHIR contains an entire folding block (size 2^k).
            #
            # For iteration 0, the leaf also contains evaluations for all batch_size polynomials, so the tuple size is
            # block_size * batch_size.
            if i == 0:
                tuple_size = block_size * self.batch_size
            else:
                tuple_size = block_size

            merkle_multi_proof_size = get_size_of_merkle_multi_proof_bits(num_leafs, self.num_queries[i], tuple_size, current_element_bits, self.hash_size_bits, expected)
            proof_size += merkle_multi_proof_size

        return proof_size

    def get_proof_size_bits(self) -> int:
        """Returns estimated proof size in bits."""
        return self._get_proof_size_bits(expected=False)

    def get_expected_proof_size_bits(self) -> int:
        """Returns estimated *expected* proof size in bits."""
        return self._get_proof_size_bits(expected=True)

    def get_rate(self) -> float:
        return 2 ** (-self.log_inv_rates[0])

    def get_dimension(self) -> int:
        return 2 ** self.log_degrees[0]

    def get_parameter_summary(self) -> str:
        lines: list[str] = []
        lines.append("")
        lines.append("```")

        # Collect scalar parameters
        params = {
            "hash_size_bits": self.hash_size_bits,
            "folding_factor": self.folding_factor,
            "batch_size": self.batch_size,
            "gap_to_radius": self.gap_to_radius,
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
        lines.append(f"    log_degree            : {self.log_degree}")
        lines.append(f"    log_degrees           : {self.log_degrees}")
        lines.append(f"    log_inv_rates         : {self.log_inv_rates}")
        lines.append(f"    num_queries           : {self.num_queries}")
        lines.append(f"    grinding_bits_queries : {self.grinding_bits_queries}")
        lines.append(f"    num_ood_samples       : {self.num_ood_samples}")
        lines.append(f"    grinding_bits_ood     : {self.grinding_bits_ood}")
        lines.append(f"    grinding_bits_folding : {self.grinding_bits_folding}")
        lines.append("")
        lines.append(
            f"  Total grinding overhead (sum of 2^grinding_bits) = 2^({self.log_grinding_overhead})"
        )

        lines.append("```")
        return "\n".join(lines)
