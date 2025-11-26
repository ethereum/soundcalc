from __future__ import annotations


from ..common.utils import get_bits_of_security_from_error

from dataclasses import dataclass

@dataclass(frozen=True)
class FRIParameters:
    """
    Models the parameters that the FRI protocol has.
    Note that this is different from FRI-based zkVM parameters,
    as such a VM may have additional parameters.
    """
    hash_size_bits: int
    field_size_bits: int
    rho: float
    D: int
    F: float
    power_batching: bool
    num_functions: int
    num_queries: int
    witness_size: int
    field_extension_degree: int
    early_stop_degree: int
    FRI_rounds_n: int
    folding_factor: int
    grinding_query_phase: int
    trace_length: int
    max_combo: int

def best_attack_security(params: FRIParameters) -> int:
    """
    Security level based on the best known attack.

    Currently, this is based on the toy problem also known as "ethSTARK conjecture".
    It uses the simplest and probably the most optimistic soundness analysis.

    Note: this is just for historical reference, the toy problem security has no real meaning.

    This is Regime 1 from the RISC0 Python calculator
    """

    # FRI errors under the toy problem regime
    # see "Toy problem security" in §5.9.1 of the ethSTARK paper
    commit_phase_error = 1 / params.F
    query_phase_error_without_grinding = params.rho ** params.num_queries
    # Add bits of security from grinding (see section 6.3 in ethSTARK)
    query_phase_error_with_grinding = query_phase_error_without_grinding * 2 ** (-params.grinding_query_phase)

    final_error = commit_phase_error + query_phase_error_with_grinding
    final_level = get_bits_of_security_from_error(final_error)

    return final_level
