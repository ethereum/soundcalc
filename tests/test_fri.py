# tests/test_fri.py
from soundcalc.pcs.fri import get_FRI_proof_size_bits

def test_get_FRI_proof_size_bits():
    hash_size_bits = 1
    field_size_bits = 1
    batch_size = 3
    num_queries = 10
    rate = 1/2
    domain_size = 64 * 2
    folding_factors = [2, 2]

    expected = 0
    expected += 3 * hash_size_bits

    size_per_query = 0
    size_per_query += 7 * hash_size_bits + 3 * field_size_bits
    size_per_query += 6 * hash_size_bits + 2 * field_size_bits
    size_per_query += 5 * hash_size_bits + 2 * field_size_bits

    expected += 16 * field_size_bits
    expected += num_queries * size_per_query

    result = get_FRI_proof_size_bits(
        hash_size_bits,
        field_size_bits,
        batch_size,
        num_queries,
        domain_size,
        folding_factors,
        rate,
        False
    )

    assert result == expected
