from __future__ import annotations
import json
import os

from soundcalc.common.utils import KIB
from soundcalc.zkvms import risc0, miden, zisk, dummy_whir, pico
from soundcalc.report import build_zkvm_report, build_summary_report
from soundcalc.zkvms.circuit import Circuit
from soundcalc.zkvms.zkvm import zkVM


REPORTS_DIR = "reports"


def generate_and_save_reports(zkvms: list[zkVM]) -> None:
    """
    Generate markdown reports for each zkVM and save to reports/ directory.
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)

    for zkvm in zkvms:
        zkvm_name = zkvm.get_name()
        # ZisK gets multi-circuit mode (all circuits inlined)
        multi_circuit = (zkvm_name == "ZisK" or zkvm_name == "Pico")

        md = build_zkvm_report(zkvm, multi_circuit=multi_circuit)
        filename = f"{zkvm_name.lower().replace(' ', '_')}.md"
        md_path = os.path.join(REPORTS_DIR, filename)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md)

        print(f"wrote :: {md_path}")

    # Generate unified summary report
    summary_md = build_summary_report(zkvms)
    summary_path = os.path.join(REPORTS_DIR, "report.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary_md)
    print(f"wrote :: {summary_path}")


def print_summary_for_circuit(circuit: Circuit) -> None:
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

def main(print_only: list[str] | None = None) -> None:
    """
    Main entry point for soundcalc

    Analyze multiple zkVMs across different security regimes,
    generate reports, and save results to disk.
    """

    # We consider the following zkVMs
    all_zkvms = [
        zisk.load(),
        miden.load(),
        risc0.load(),
        dummy_whir.load(),
        pico.load(),
    ]

    if print_only:
        filter_names = [p.lower() for p in print_only]
        zkvms = [z for z in all_zkvms if z.get_name().lower() in filter_names]
    else:
        zkvms = all_zkvms

    # Print summary for each zkVM
    for zkvm in zkvms:
        print_summary_for_zkvm(zkvm)

    # Generate and save markdown reports (one per zkVM)
    generate_and_save_reports(zkvms)

if __name__ == "__main__":
    main()
