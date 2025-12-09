"""
A few FRI-related utilities used across regimes.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from soundcalc.common.utils import get_size_of_merkle_path_bits_fri

if TYPE_CHECKING:
    from ..zkvms.zkvm import FRIBasedVM

def get_johnson_parameter_m() -> float:
    """
    Return m from https://eprint.iacr.org/2022/1216.pdf
    """
    # ASN This is hardcoded to 16, whereas winterfell brute forces it:
    #    https://github.com/facebook/winterfell/blob/main/air/src/proof/security.rs#L290-L306
    return 16.0

def get_num_FRI_folding_rounds(
    witness_size: int,
    field_extension_degree: int,
    folding_factors: list[int],
    fri_early_stop_degree: int,
) -> int:
    """
    Compute the number of FRI folding rounds.
    Stolen from:
      https://github.com/risc0/risc0/blob/release-2.0/risc0/zkp/src/prove/soundness.rs#L125
    """
    n = witness_size
    rounds = 0

    for i in range(len(folding_factors)):
        n //= folding_factors[i]
        rounds += 1

    # Make sure that the early stop degree is correctly set
    assert n == fri_early_stop_degree, f"After {rounds} rounds, n={n} != fri_early_stop_degree={fri_early_stop_degree}"
    return rounds

def get_FRI_query_phase_error(theta: float, num_queries: int, grinding_bits: int) -> float:
    """
    Compute the FRI query phase soundness error.
    See the last term of Equation 7 in Theorem 2 of Ha22.

    It includes `grinding_query_phase_bits` bits of grinding.

    Note: This function is used by all regimes except the toy problem regime (TPR).
    """
    FRI_query_phase_error = (1 - theta) ** num_queries

    # Add bits of security from grinding (see section 6.3 in ethSTARK)
    FRI_query_phase_error *= 2 ** (-grinding_bits)

    return FRI_query_phase_error


def get_FRI_proof_size_bits(
        hash_size_bits: int,
        base_field_size_bits: int,
        extension_field_size_bits: int,
        num_columns: list[int],
        num_queries: int,
        domain_size: int,
        folding_factors: list[int],
        merkle_tree_arity: int,
        last_level_verification: int
) -> int:

    """
    Compute the proof size of a (BCS-transformed) FRI interaction in bits.
    """

    # TODO: the following things are not yet considered.
    #   - is there really a Merkle root (and paths) for the final round? Or just the codeword itself?

    # The FRI proof contains two parts: Merkle roots, and one "openings" per query,
    # where an "opening" is a Merkle path for each folding layer.
    #
    # We use the same loop as in `get_num_FRI_folding_rounds`, and count the size that
    # this layer contributes, which includes the root and all Merkle paths.

    size_bits = 0

    # Initial Round: one root and one path per query
    # We assume that for the initial functions, there is only one Merkle root, and
    # each leaf i for that root contains symbols i for all initial functions.
    n = int(domain_size)
    num_leafs = n
    for c in num_columns:
        size_bits += hash_size_bits + num_queries * get_size_of_merkle_path_bits_fri(num_leafs, c * base_field_size_bits, hash_size_bits, merkle_tree_arity, last_level_verification)
    
    # Now we have folded these batch_size initial functions into one
    # Next, we start with the folding rounds.

    # We assume that "siblings" for the following layers are grouped together
    # in one leaf. This is natural as they always need to be opened together.

    rounds = len(folding_factors)
    for i in range(rounds):

        # in our current domain, we group together all siblings (sometimes denoted Block(z) in the literature)
        num_leafs = n // int(folding_factors[i])
        tuple_size = folding_factors[i] * extension_field_size_bits

        # one root and one path per query
        size_bits += hash_size_bits + num_queries * get_size_of_merkle_path_bits_fri(num_leafs, tuple_size, hash_size_bits, merkle_tree_arity, last_level_verification)

        # next domain size is given by applying folding
        n = n // int(folding_factors[i])

    # for the final round, we send the function in the clear.
    # note that we don't need to send the full function, but can just send
    # the polynomial that describes it
    size_bits += n * extension_field_size_bits

    return size_bits