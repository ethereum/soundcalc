"""
CLI console output for soundcalc.

Prints security summaries to stdout.
"""

from __future__ import annotations

import json

from soundcalc.common.utils import KIB
from soundcalc.circuits.circuit import Circuit
from soundcalc.zkvms.zkvm import zkVM


def _print_summary_for_circuit(circuit: Circuit) -> None:
    """
    Print a summary of security results for a single circuit.
    """
    proof_size_kib = circuit.get_proof_size_bits() // KIB
    print(f"proof size estimate (worst case): {proof_size_kib} KiB, where 1 KiB = 1024 bytes")
    print("")
    proof_size_expected_kib = circuit.get_expected_proof_size_bits() // KIB
    print(f"proof size estimate (expected): {proof_size_expected_kib} KiB, where 1 KiB = 1024 bytes")
    print("")
    print(f"parameters: \n {circuit.get_parameter_summary()}")
    print("")
    security_levels = circuit.get_security_levels()
    print(f"security levels (rbr): \n {json.dumps(security_levels, indent=4)}")


def _print_summary_for_zkvm(zkvm: zkVM) -> None:
    """
    Print a summary of security results for a zkVM and all its circuits.
    """
    circuits = zkvm.get_circuits()

    print("")
    print("#############################################")
    print(f"#  zkVM: {zkvm.get_name()}")
    print("#############################################")

    if len(circuits) == 1:
        # Single circuit - print directly
        print("")
        _print_summary_for_circuit(circuits[0])
    else:
        # Multiple circuits - print each as a subsection
        for circuit in circuits:
            print("")
            print(f"--- Circuit: {circuit.get_name()} ---")
            print("")
            _print_summary_for_circuit(circuit)

    print("")
    print("")
    print("")


def print_summaries(zkvms: list[zkVM]) -> None:
    """
    Print CLI summaries for all zkVMs.
    """
    for zkvm in zkvms:
        _print_summary_for_zkvm(zkvm)
