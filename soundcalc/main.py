from __future__ import annotations
import json

from soundcalc.common.utils import KIB
from soundcalc.zkvms.dummy_whir import DummyWHIRPreset
from soundcalc.zkvms.risc0 import Risc0Preset
from soundcalc.zkvms.miden import MidenPreset
from soundcalc.zkvms.zisk import ZiskPreset
from soundcalc.report import build_markdown_report
from soundcalc.zkvms.zkvm import Circuit, zkVM



def generate_and_save_md_report(sections) -> None:
    """
    Generate markdown report and save it to disk.
    """
    md = build_markdown_report(sections)
    md_path = "results.md"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"wrote :: {md_path}")


def print_summary_for_circuit(circuit: Circuit) -> None:
    """
    Print a summary of security results for a single circuit.
    """
    proof_size_kib = circuit.get_proof_size_bits() // KIB
    print(f"proof size estimate: {proof_size_kib} KiB, where 1 KiB = 1024 bytes")
    print("")
    print(f"parameters: \n {circuit.get_parameter_summary()}")
    print("")
    security_levels = circuit.get_security_levels()
    print(f"security levels (rbr): \n {json.dumps(security_levels, indent=4)}")


def print_summary_for_zkvm(zkvm: zkVM) -> None:
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
        print_summary_for_circuit(circuits[0])
    else:
        # Multiple circuits - print each as a subsection
        for circuit in circuits:
            print("")
            print(f"--- Circuit: {circuit.get_name()} ---")
            print("")
            print_summary_for_circuit(circuit)

    print("")
    print("")
    print("")


def main() -> None:
    """
    Main entry point for soundcalc

    Analyze multiple zkVMs across different security regimes,
    generate reports, and save results to disk.
    """

    sections: dict[str, tuple[zkVM, dict[str, dict]]] = {}

    # We consider the following zkVMs
    zkvms = [
        ZiskPreset.default(),
        MidenPreset.default(),
        Risc0Preset.default(),
        DummyWHIRPreset.default(),
    ]

    # Analyze each zkVM
    for zkvm in zkvms:
        print_summary_for_zkvm(zkvm)
        # For now, store first circuit's security levels for markdown report
        # TODO: Update markdown report to handle multiple circuits
        circuits = zkvm.get_circuits()
        security_levels = circuits[0].get_security_levels()
        sections[zkvm.get_name()] = (zkvm, security_levels)

    # Generate and save markdown report
    generate_and_save_md_report(sections)

if __name__ == "__main__":
    main()
