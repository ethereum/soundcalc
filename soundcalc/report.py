"""
Markdown report generation for soundcalc.

This file is a mess.
"""

from __future__ import annotations

import math
from typing import Dict, Any, List, Tuple

from soundcalc.common.utils import KIB
from soundcalc.pcs.fri import FRI
from soundcalc.pcs.whir import WHIR
from soundcalc.zkvms.circuit import Circuit
from soundcalc.zkvms.zkvm import zkVM


def _compute_overview_stats(circuits: list[Circuit]) -> dict[str, Any]:
    """
    Compute overview statistics for a list of circuits.

    Returns a dict containing:
    - final_circuit_name: Name of the final circuit
    - final_proof_size_kib: Proof size of the final circuit in KiB
    - best_regime: The regime with highest minimum security (UDR or JBR)
    - min_security_bits: The minimum bits of security across all circuits
    - offending_circuit: Name of the circuit with lowest security
    """
    if not circuits:
        return {}

    final_circuit = circuits[-1]
    final_proof_size_kib = final_circuit.get_proof_size_bits() // KIB

    # Track minimum security per regime
    regime_mins: dict[str, tuple[int, str]] = {}  # regime -> (min_bits, circuit_name)

    for circuit in circuits:
        security_levels = circuit.get_security_levels()
        for regime_name, levels in security_levels.items():
            if isinstance(levels, dict) and "total" in levels:
                total_bits = levels["total"]
                if regime_name not in regime_mins or total_bits < regime_mins[regime_name][0]:
                    regime_mins[regime_name] = (total_bits, circuit.get_name())

    # Find the regime with the highest minimum security
    best_regime = None
    best_min_bits = -1
    offending_circuit = None

    for regime_name, (min_bits, circuit_name) in regime_mins.items():
        if min_bits > best_min_bits:
            best_min_bits = min_bits
            best_regime = regime_name
            offending_circuit = circuit_name

    return {
        "final_circuit_name": final_circuit.get_name(),
        "final_proof_size_kib": final_proof_size_kib,
        "best_regime": best_regime,
        "min_security_bits": best_min_bits,
        "offending_circuit": offending_circuit,
    }


def _field_label(field) -> str:
    if hasattr(field, "to_string"):
        return field.to_string()
    return "Unknown"


def _fri_parameter_lines(circuit: Circuit) -> list[str]:
    pcs = circuit.pcs
    batching = "Powers" if pcs.power_batching else "Affine"
    return [
        f"- Polynomial commitment scheme: FRI",
        f"- Hash size (bits): {pcs.hash_size_bits}",
        f"- Number of queries: {pcs.num_queries}",
        f"- Grinding (bits): {pcs.grinding_query_phase}",
        f"- Field: {_field_label(pcs.field)}",
        f"- Rate (ρ): {pcs.rho}",
        f"- Trace length (H): $2^{{{pcs.h}}}$",
        f"- FRI rounds: {pcs.FRI_rounds_n}",
        f"- FRI folding factors: {pcs.FRI_folding_factors}",
        f"- FRI early stop degree: {pcs.FRI_early_stop_degree}",
        f"- Number of columns: {circuit.num_columns}",
        f"- Batch size: {pcs.batch_size}",
        f"- Batching: {batching}",
    ]


def _whir_parameter_lines(circuit: Circuit) -> list[str]:
    pcs = circuit.pcs
    batching = "Powers" if pcs.power_batching else "Affine"
    return [
        f"- Polynomial commitment scheme: WHIR",
        f"- Hash size (bits): {pcs.hash_size_bits}",
        f"- Field: {_field_label(pcs.field)}",
        f"- Iterations (M): {pcs.num_iterations}",
        f"- Folding factor (k): {pcs.folding_factor}",
        f"- Constraint degree: {pcs.constraint_degree}",
        f"- Batch size: {pcs.batch_size}",
        f"- Batching: {batching}",
        f"- Queries per iteration: {pcs.num_queries}",
        f"- OOD samples per iteration: {pcs.num_ood_samples}",
        f"- Total grinding overhead log2: {pcs.log_grinding_overhead}",
    ]


def _generic_parameter_lines(circuit: Circuit) -> list[str]:
    lines: list[str] = []
    lines.append(f"- Polynomial commitment scheme: Unknown")
    pcs = circuit.pcs
    if hasattr(pcs, "hash_size_bits"):
        lines.append(f"- Hash size (bits): {pcs.hash_size_bits}")
    if hasattr(pcs, "field"):
        lines.append(f"- Field: {_field_label(pcs.field)}")
    return lines


def _get_parameter_lines(circuit: Circuit) -> list[str]:
    """Get parameter lines for a circuit."""
    if isinstance(circuit.pcs, FRI):
        return _fri_parameter_lines(circuit)
    if isinstance(circuit.pcs, WHIR):
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
        # Multi-circuit mode: add overview and inline all circuits
        overview = _compute_overview_stats(circuits)

        if overview:
            lines.append("## zkEVM Overview")
            lines.append("")
            lines.append(f"| Metric | Value |")
            lines.append(f"| --- | --- |")
            lines.append(f"| Final proof size | **{overview['final_proof_size_kib']:.1f} KiB** (circuit: {overview['final_circuit_name']}) |")
            lines.append(f"| Final bits of security | **{overview['min_security_bits']}** ({overview['best_regime']}, circuit: {overview['offending_circuit']}) |")
            lines.append("")

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
            lines.append(f"**Proof Size Estimate (Worst Case):** {proof_size_kib} KiB, where 1 KiB = 1024 bytes")
            lines.append("")
            proof_size_expected_kib = circuit.get_expected_proof_size_bits() // KIB
            lines.append(f"**Proof Size Estimate (Expected):** {proof_size_expected_kib} KiB, where 1 KiB = 1024 bytes")
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
