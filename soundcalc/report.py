"""
Markdown report generation for soundcalc.

This file is a mess.
"""

from __future__ import annotations

import math
from typing import Dict, Any, List, Tuple

from soundcalc.common.utils import KIB
from soundcalc.zkvms.fri_based_vm import FRIBasedCircuit, FRIBasedVM
from soundcalc.zkvms.whir_based_vm import WHIRBasedCircuit, WHIRBasedVM
from soundcalc.zkvms.zkvm import Circuit, zkVM


def _field_label(field) -> str:
    if hasattr(field, "to_string"):
        return field.to_string()
    return "Unknown"


def _fri_parameter_lines(circuit: FRIBasedCircuit) -> list[str]:
    batching = "Powers" if circuit.power_batching else "Affine"
    return [
        f"- Polynomial commitment scheme: FRI",
        f"- Hash size (bits): {circuit.hash_size_bits}",
        f"- Number of queries: {circuit.num_queries}",
        f"- Grinding (bits): {circuit.grinding_query_phase}",
        f"- Field: {_field_label(circuit.field)}",
        f"- Rate (ρ): {circuit.rho}",
        f"- Trace length (H): $2^{{{circuit.h}}}$",
        f"- FRI rounds: {circuit.FRI_rounds_n}",
        f"- FRI folding factors: {circuit.FRI_folding_factors}",
        f"- FRI early stop degree: {circuit.FRI_early_stop_degree}",
        f"- Number of columns: {circuit.num_columns}",
        f"- Batch size: {circuit.batch_size}",
        f"- Batching: {batching}",
    ]


def _whir_parameter_lines(circuit: WHIRBasedCircuit) -> list[str]:
    batching = "Powers" if circuit.power_batching else "Affine"
    return [
        f"- Polynomial commitment scheme: WHIR",
        f"- Hash size (bits): {circuit.hash_size_bits}",
        f"- Field: {_field_label(circuit.field)}",
        f"- Iterations (M): {circuit.num_iterations}",
        f"- Folding factor (k): {circuit.folding_factor}",
        f"- Constraint degree: {circuit.constraint_degree}",
        f"- Batch size: {circuit.batch_size}",
        f"- Batching: {batching}",
        f"- Queries per iteration: {circuit.num_queries}",
        f"- OOD samples per iteration: {circuit.num_ood_samples}",
        f"- Total grinding overhead log2: {circuit.log_grinding_overhead}",
    ]


def _generic_parameter_lines(circuit) -> list[str]:
    lines: list[str] = []
    lines.append(f"- Polynomial commitment scheme: Unknown")
    if hasattr(circuit, "hash_size_bits"):
        lines.append(f"- Hash size (bits): {circuit.hash_size_bits}")
    if hasattr(circuit, "field"):
        lines.append(f"- Field: {_field_label(circuit.field)}")
    return lines


def _get_parameter_lines(circuit: Circuit) -> list[str]:
    """Get parameter lines for a circuit."""
    if isinstance(circuit, FRIBasedCircuit):
        return _fri_parameter_lines(circuit)
    if isinstance(circuit, WHIRBasedCircuit):
        return _whir_parameter_lines(circuit)
    return _generic_parameter_lines(circuit)


def _build_security_table(results: dict[str, Any]) -> str:
    """Build a markdown security table from security results."""
    display_results: dict[str, Any] = {
        name: data.copy() if isinstance(data, dict) else data
        for name, data in results.items()
    }

    # --- Get all column headers ---
    columns = set()
    for v in display_results.values():
        if isinstance(v, dict):
            columns.update(v.keys())

    ordered_columns: list[str] = ["regime"]
    if "total" in columns:
        ordered_columns.append("total")
    ordered_columns.extend(sorted(col for col in columns if col != "total"))
    columns = ordered_columns

    fri_commit_columns = [
        col for col in columns if col.startswith("FRI commit round ")
    ]

    def should_collapse_commit_columns() -> bool:
        if len(fri_commit_columns) <= 1:
            return False

        def row_has_single_value(row: dict[str, Any]) -> bool:
            values = [row.get(col) for col in fri_commit_columns if col in row]
            values = [value for value in values if value is not None]
            if not values:
                return True
            first_value = values[0]
            return all(value == first_value for value in values)

        for row_data in display_results.values():
            if isinstance(row_data, dict) and not row_has_single_value(row_data):
                return False
        return True

    if should_collapse_commit_columns():
        first_commit_idx = columns.index(fri_commit_columns[0])
        for col in fri_commit_columns:
            columns.remove(col)

        merged_label = f"FRI commit rounds (×{len(fri_commit_columns)})"
        columns.insert(first_commit_idx, merged_label)

        for row_name, row_data in display_results.items():
            if not isinstance(row_data, dict):
                continue
            merged_value = None
            for col in fri_commit_columns:
                if col in row_data:
                    merged_value = row_data[col]
                    break
            if merged_value is not None:
                row_data[merged_label] = merged_value
            for col in fri_commit_columns:
                row_data.pop(col, None)

    # --- Build Markdown header ---
    md_table = "| " + " | ".join(columns) + " |\n"
    md_table += "| " + " | ".join(["---"] * len(columns)) + " |\n"

    # --- Build each row ---
    for row_name, row_data in display_results.items():
        row_values = [row_name]
        if isinstance(row_data, dict):
            for col in columns[1:]:
                row_values.append(str(row_data.get(col, "—")))
        else:
            # Non-dict value sits under the 'total' column when present.
            for col in columns[1:]:
                if col == "total":
                    row_values.append(str(row_data))
                else:
                    row_values.append("—")
        md_table += "| " + " | ".join(row_values) + " |\n"

    return md_table


def build_zkvm_report(zkvm: zkVM, multi_circuit: bool = False) -> str:
    """
    Build a markdown report for a single zkVM.

    Args:
        zkvm: The zkVM to generate a report for
        multi_circuit: If True, inline all circuits separately with their names.
                      If False, only report on the first circuit.
    """
    lines: list[str] = []
    zkvm_name = zkvm.get_name()

    lines.append(f"# 📊 {zkvm_name}")
    lines.append("")
    lines.append("How to read this report:")
    lines.append("- Table rows correspond to security regimes")
    lines.append("- Table columns correspond to proof system components")
    lines.append("- Cells show bits of security per component")
    lines.append("- Proof size estimate is only indicative")
    lines.append("")

    circuits = zkvm.get_circuits()

    if multi_circuit and len(circuits) > 1:
        # Multi-circuit mode: inline all circuits
        lines.append("## Circuits")
        lines.append("")
        for circuit in circuits:
            lines.append(f"- [{circuit.get_name()}](#{circuit.get_name().lower().replace(' ', '-')})")
        lines.append("")

        for circuit in circuits:
            lines.append(f"## {circuit.get_name()}")
            lines.append("")

            # Parameters
            lines.append("**Parameters:**")
            lines.extend(_get_parameter_lines(circuit))
            lines.append("")

            # Proof size
            proof_size_kib = circuit.get_proof_size_bits() // KIB
            lines.append(f"**Proof Size Estimate:** {proof_size_kib} KiB, where 1 KiB = 1024 bytes")
            lines.append("")

            # Security table
            security_levels = circuit.get_security_levels()
            lines.append(_build_security_table(security_levels))
            lines.append("")
    else:
        # Single circuit mode
        circuit = circuits[0] if circuits else None
        if circuit:
            # Parameters
            lines.append("**Parameters:**")
            lines.extend(_get_parameter_lines(circuit))
            lines.append("")

            # Proof size
            proof_size_kib = circuit.get_proof_size_bits() // KIB
            lines.append(f"**Proof Size Estimate:** {proof_size_kib} KiB, where 1 KiB = 1024 bytes")
            lines.append("")

            # Security table
            security_levels = circuit.get_security_levels()
            lines.append(_build_security_table(security_levels))
        else:
            lines.append("No circuits available.")

    return "\n".join(lines)
