from __future__ import annotations

import math

KIB = (1024 * 8) # Kilobytes


def get_rho_plus(H: int, D: float, max_combo: int) -> float:
    """Compute rho+. See page 16 of Ha22"""
    # XXX Should this be (H + 2) / D? This part is cryptic in [Ha22]
    # TODO Figure out
    return (H + max_combo) / D

def get_bits_of_security_from_error(error: float) -> int:
    """
    Returns the maximum k such that error <= 2^{-k}
    """
    return int(math.floor(-math.log2(error)))


def get_size_of_merkle_proof_bits(num_leafs: int, tuple_size: int, element_size_bits: int, hash_size_bits: int) -> int:
    """
    Compute the size of a Merkle path in bits.

    We assume a Merkle tree that represents num_leafs tuples of elements
    where each element has size element_size_bits and one tuple contains tuple_size
    many elements. Each leaf of the tree contains one such tuple.

    Note: the result counts both the leaf itself and the Merkle path.
    """
    assert num_leafs > 0
    leaf_size = tuple_size * element_size_bits
    sibling = min(tuple_size * element_size_bits, hash_size_bits)
    tree_depth = math.ceil(math.log2(num_leafs))
    co_path = (tree_depth - 1) * hash_size_bits
    return leaf_size + sibling + co_path

def get_size_of_merkle_multi_proof_bits_expected(num_leafs: int, num_openings: int, tuple_size: int, element_size_bits: int,  hash_size_bits: int) -> int:
    """
    Compute the *expected* size of a Merkle multi-proof in bits.

    We assume a Merkle tree that represents num_leafs leaves.

    Note: the result counts both the leafs and the Merkle path.

    For derivation see: https://xn--2-umb.com/25/merkle-multi-proof/#expected-value-1
    """
    assert num_leafs > 0

    leafs_size = num_openings * tuple_size * element_size_bits

    tree_depth = math.ceil(math.log2(num_leafs))

    num_hashes = 0
    for d in range(1, tree_depth +1):
        prob_sibling_in_proof = ((1 - 2**(-d))**num_openings - (1 - 2**(1-d))**num_openings)
        num_hashes += math.ceil(2**d * prob_sibling_in_proof)
    return leafs_size + num_hashes * hash_size_bits


def get_size_of_merkle_multi_proof_bits(num_leafs: int, num_openings: int, tuple_size: int, element_size_bits: int,  hash_size_bits: int, expected: bool) -> int:
    """
    Compute the *worst case* or *expected* size of a Merkle multi-proof in bits.
    """
    if expected:
        return get_size_of_merkle_multi_proof_bits_expected(num_leafs, num_openings, tuple_size, element_size_bits, hash_size_bits)
    else:
        return num_openings * get_size_of_merkle_proof_bits(num_leafs, tuple_size, element_size_bits, hash_size_bits)