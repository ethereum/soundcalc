"""This file is a mess"""

from __future__ import annotations

import math
from typing import Dict, Any, List, Tuple

from soundcalc.common.utils import KIB
from soundcalc.zkvms.fri_based_vm import FRIBasedVM
from soundcalc.zkvms.whir_based_vm import WHIRBasedVM


def _field_label(field) -> str:
    if hasattr(field, "to_string"):
        return field.to_string()
    return "Unknown"


def _fri_parameter_lines(zkvm_obj: FRIBasedVM) -> list[str]:
    batching = "Powers" if zkvm_obj.power_batching else "Affine"
    return [
        f"- Polynomial commitment scheme: FRI",
        f"- Hash size (bits): {zkvm_obj.hash_size_bits}",
        f"- Number of queries: {zkvm_obj.num_queries}",
        f"- Grinding (bits): {zkvm_obj.grinding_query_phase}",
        f"- Field: {_field_label(zkvm_obj.field)}",
        f"- Rate (ρ): {zkvm_obj.rho}",
        f"- Trace length (H): $2^{{{zkvm_obj.h}}}$",
        f"- FRI folding factor: {zkvm_obj.FRI_folding_factor}",
        f"- FRI early stop degree: {zkvm_obj.FRI_early_stop_degree}",
        f"- Batching: {batching}",
    ]


def _whir_parameter_lines(zkvm_obj: WHIRBasedVM) -> list[str]:
    batching = "Powers" if zkvm_obj.power_batching else "Affine"
    return [
        f"- Polynomial commitment scheme: WHIR",
        f"- Hash size (bits): {zkvm_obj.hash_size_bits}",
        f"- Field: {_field_label(zkvm_obj.field)}",
        f"- Iterations (M): {zkvm_obj.num_iterations}",
        f"- Folding factor (k): {zkvm_obj.folding_factor}",
        f"- Constraint degree: {zkvm_obj.constraint_degree}",
        f"- Batch size: {zkvm_obj.batch_size}",
        f"- Batching: {batching}",
        f"- Queries per iteration: {zkvm_obj.num_queries}",
        f"- OOD samples per iteration: {zkvm_obj.num_ood_samples}",
        f"- Total grinding overhead log2: {zkvm_obj.log_grinding_overhead}",
    ]


def _generic_parameter_lines(zkvm_obj) -> list[str]:
    lines: list[str] = []
    lines.append(f"- Polynomial commitment scheme: Unknown")
    if hasattr(zkvm_obj, "hash_size_bits"):
        lines.append(f"- Hash size (bits): {zkvm_obj.hash_size_bits}")
    if hasattr(zkvm_obj, "field"):
        lines.append(f"- Field: {_field_label(zkvm_obj.field)}")
    return lines


def _describe_vm(zkvm_obj):
    if isinstance(zkvm_obj, FRIBasedVM):
        return "", _fri_parameter_lines(zkvm_obj)
    if isinstance(zkvm_obj, WHIRBasedVM):
        return "", _whir_parameter_lines(zkvm_obj)
    return "", _generic_parameter_lines(zkvm_obj)



def build_markdown_report(sections) -> str:

    lines: list[str] = []
    lines.append("# 📊 soundcalc report")
    lines.append("")
    lines.append("How to read this report:")
    lines.append("- Choose a zkEVM")
    lines.append("- Table rows correspond to security regimes")
    lines.append("- Table columns correspond to proof system components")
    lines.append("- Cells show bits of security per component")
    lines.append("- Proof size estimate is only indicative")
    lines.append("")

    # ToC
    lines.append("# Supported zkEVMs")
    for zkevm in sections:
        anchor = zkevm.lower().replace(" ", "-")
        lines.append(f"- [{zkevm}](#{anchor})")
    lines.append("")

    for zkevm in sections:
        anchor = zkevm.lower().replace(" ", "-")

        (zkvm_obj, results) = sections[zkevm]
        commitment_label, parameter_lines = _describe_vm(zkvm_obj)

        lines.append(f"## {zkevm}")
        lines.append("")

        display_results: dict[str, Any] = {
            name: data.copy() if isinstance(data, dict) else data
            for name, data in results.items()
        }

        # Add parameter information
        lines.append(f"**Parameters:**")
        if parameter_lines:
            lines.extend(parameter_lines)
        else:
            lines.append("- No parameter summary available.")
        lines.append("")

        # Proof size
        proof_size_kib = zkvm_obj.get_proof_size_bits() // KIB
        lines.append(f"**Proof Size Estimate:** {proof_size_kib} KiB, where 1 KiB = 1024 bytes")
        lines.append("")

        # Show results

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

        lines.append(md_table)


    return "\n".join(lines)
