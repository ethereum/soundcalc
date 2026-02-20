"""
Markdown report generation for soundcalc.

This file is a mess.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from soundcalc.common.utils import KIB
from soundcalc.pcs.fri import FRI
from soundcalc.pcs.whir import WHIR
from soundcalc.zkvms.circuit import Circuit
from soundcalc.zkvms.zkvm import zkVM


REPORTS_DIR = "reports"
SUMMARY_REPORT_NAME = "summary.md"

# zkVMs excluded from the summary overview (test/dummy entries)
_SUMMARY_EXCLUDE = {"DummyWHIR"}


@dataclass
class zkVMSummary:
    """Summary data for a single zkVM used in comparison reports."""
    name: str
    field: str
    pcs: str
    num_circuits: int
    weakest_circuit_name: str
    security_bits: int
    security_regime: str
    final_proof_size_kib: int


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


def _pcs_label(circuit: Circuit) -> str:
    """Get the PCS type label for a circuit."""
    if isinstance(circuit.pcs, FRI):
        return "FRI"
    elif isinstance(circuit.pcs, WHIR):
        return "WHIR"
    return "Unknown"


def _collect_zkvm_summary(zkvm: zkVM) -> zkVMSummary:
    """
    Collect summary metrics for a single zkVM.

    Returns a zkVMSummary containing aggregated security and proof size data.
    Security is the best (highest) minimum across regimes, matching
    the "Final bits of security" shown in individual zkVM reports.
    """
    circuits = zkvm.get_circuits()
    if not circuits:
        return zkVMSummary(
            name=zkvm.get_name(),
            field="Unknown",
            pcs="Unknown",
            num_circuits=0,
            weakest_circuit_name="N/A",
            security_bits=0,
            security_regime="N/A",
            final_proof_size_kib=0,
        )

    field = _field_label(circuits[0].field)
    pcs = _pcs_label(circuits[0])

    # Track minimum security per regime across all circuits
    regime_mins: dict[str, tuple[int, str]] = {}  # regime -> (min_bits, circuit_name)
    for circuit in circuits:
        levels = circuit.get_security_levels()
        for regime_name, regime_data in levels.items():
            if isinstance(regime_data, dict) and "total" in regime_data:
                total_bits = regime_data["total"]
                if regime_name not in regime_mins or total_bits < regime_mins[regime_name][0]:
                    regime_mins[regime_name] = (total_bits, circuit.get_name())

    # Find the best regime (highest minimum security)
    best_regime = "N/A"
    best_bits = 0
    weakest_name = circuits[0].get_name()
    for regime_name, (min_bits, circuit_name) in regime_mins.items():
        if min_bits > best_bits:
            best_bits = min_bits
            best_regime = regime_name
            weakest_name = circuit_name

    final_proof_kib = circuits[-1].get_proof_size_bits() // KIB

    return zkVMSummary(
        name=zkvm.get_name(),
        field=field,
        pcs=pcs,
        num_circuits=len(circuits),
        weakest_circuit_name=weakest_name,
        security_bits=best_bits,
        security_regime=best_regime,
        final_proof_size_kib=int(final_proof_kib),
    )


def _fri_parameter_lines(circuit: Circuit) -> list[str]:
    pcs = circuit.pcs
    batching = "Powers" if pcs.power_batching else "Affine"
    lines = [
        f"- Polynomial commitment scheme: FRI",
        f"- Hash size (bits): {pcs.hash_size_bits}",
        f"- Number of queries: {pcs.num_queries}",
        f"- Grinding query phase (bits): {pcs.grinding_query_phase}",
    ]
    if pcs.grinding_commit_phase > 0:
        lines.append(f"- Grinding commit phase (bits): {pcs.grinding_commit_phase}")
    if circuit.grinding_deep > 0:
        lines.append(f"- Grinding DEEP (bits): {circuit.grinding_deep}")
    lines.extend([
        f"- Field: {_field_label(pcs.field)}",
        f"- Rate (ρ): {pcs.rho}",
        f"- Trace length (H): $2^{{{pcs.h}}}$",
        f"- FRI rounds: {pcs.FRI_rounds_n}",
        f"- FRI folding factors: {pcs.FRI_folding_factors}",
        f"- FRI early stop degree: {pcs.FRI_early_stop_degree}",
        f"- Number of constraints: {circuit.num_constraints}",
        f"- Batch size: {pcs.batch_size}",
        f"- Batching: {batching}",
    ])
    return lines


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


def _lookup_parameter_lines(circuit: Circuit) -> list[str]:
    """Get parameter lines for lookups in a circuit."""
    lines: list[str] = []
    for lookup in circuit.get_lookups():
        lines.append(f"- Lookup (logup): {lookup.get_name()}")
    return lines


def _get_parameter_lines(circuit: Circuit) -> list[str]:
    """Get parameter lines for a circuit."""
    if isinstance(circuit.pcs, FRI):
        lines = _fri_parameter_lines(circuit)
    elif isinstance(circuit.pcs, WHIR):
        lines = _whir_parameter_lines(circuit)
    else:
        lines = _generic_parameter_lines(circuit)
    lines.extend(_lookup_parameter_lines(circuit))
    return lines


def _build_security_table(results: dict[str, Any], lookup_names: list[str] | None = None) -> str:
    """Build a markdown security table from security results."""
    display_results: dict[str, Any] = {
        name: data.copy() if isinstance(data, dict) else data
        for name, data in results.items()
    }
    lookup_names = lookup_names or []

    # --- Get all column headers ---
    columns = set()
    for v in display_results.values():
        if isinstance(v, dict):
            columns.update(v.keys())

    # Order: regime, total, lookups (in order), then rest sorted
    ordered_columns: list[str] = ["regime"]
    if "total" in columns:
        ordered_columns.append("total")
    for name in lookup_names:
        if name in columns:
            ordered_columns.append(name)
    excluded = {"total"} | set(lookup_names)
    ordered_columns.extend(sorted(col for col in columns if col not in excluded))
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


def _build_zkvm_report(zkvm: zkVM, multi_circuit: bool = False) -> str:
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
    lines.append("- Proof size estimates are indicative (1 KiB = 1024 bytes)")
    lines.append("")

    circuits = zkvm.get_circuits()

    if multi_circuit and len(circuits) > 1:
        # Multi-circuit mode: add overview and inline all circuits
        overview = _compute_overview_stats(circuits)

        if overview:
            lines.append("## zkVM Overview")
            lines.append("")
            final_circuit = overview['final_circuit_name']
            final_circuit_link = f"[{final_circuit}](#{final_circuit.lower().replace(' ', '-')})"
            offending_circuit = overview['offending_circuit']
            offending_circuit_link = f"[{offending_circuit}](#{offending_circuit.lower().replace(' ', '-')})"
            lines.append(f"| Metric | Value | Relevant circuit | Notes |")
            lines.append(f"| --- | --- | --- | --- |")
            lines.append(f"| Final proof size (worst case) | **{int(overview['final_proof_size_kib'])} KiB** | {final_circuit_link} | |")
            lines.append(f"| Final bits of security | **{overview['min_security_bits']} bits** | {offending_circuit_link} | Regime: {overview['best_regime']} |")
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
            expected_kib = int(circuit.get_expected_proof_size_bits() // KIB)
            worst_kib = int(circuit.get_proof_size_bits() // KIB)
            lines.append(f"**Proof Size:** {expected_kib} KiB (expected) / {worst_kib} KiB (worst case)")
            lines.append("")

            # Security table
            security_levels = circuit.get_security_levels()
            lookup_names = [lookup.get_name() for lookup in circuit.get_lookups()]
            lines.append(_build_security_table(security_levels, lookup_names))
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
            expected_kib = int(circuit.get_expected_proof_size_bits() // KIB)
            worst_kib = int(circuit.get_proof_size_bits() // KIB)
            lines.append(f"**Proof Size:** {expected_kib} KiB (expected) / {worst_kib} KiB (worst case)")
            lines.append("")

            # Security table
            security_levels = circuit.get_security_levels()
            lookup_names = [lookup.get_name() for lookup in circuit.get_lookups()]
            lines.append(_build_security_table(security_levels, lookup_names))
        else:
            lines.append("No circuits available.")

    return "\n".join(lines)


def _build_summary_report(zkvms: list[zkVM]) -> str:
    """
    Build a unified comparison report for multiple zkVMs.

    Args:
        zkvms: List of zkVMs to compare

    Returns:
        Markdown-formatted comparison table with security and proof size metrics.
    """
    lines = [
        "# 📊 zkVM Soundness Summary",
        "",
        "How to read this report:",
        "- Click on zkVM names to view detailed individual reports",
        "- Security shows the best bits of security across regimes (UDR/JBR)",
        "",
        "## Overview",
        "",
        "| zkVM | Security | Proof Size | PCS | Field | Circuits | Weakest Circuit |",
        "|------|----------|------------|-----|-------|----------|-----------------|",
    ]

    summaries = sorted(
        [_collect_zkvm_summary(z) for z in zkvms if z.get_name() not in _SUMMARY_EXCLUDE],
        key=lambda s: s.name.lower(),
    )

    for s in summaries:
        report_filename = f"{s.name.lower().replace(' ', '_')}.md"
        lines.append(
            f"| [{s.name}]({report_filename}) "
            f"| **{s.security_bits}** bits ({s.security_regime}) "
            f"| {s.final_proof_size_kib} KiB "
            f"| {s.pcs} | {s.field} | {s.num_circuits} | {s.weakest_circuit_name} |"
        )

    lines.extend([
        "",
        "## Notes",
        "",
        "- **Security**: Best bits of security across UDR (Unique Decoding) and JBR (Johnson Bound) regimes",
        "- **Weakest Circuit**: Circuit determining the overall security level",
        "- **Proof Size**: Final proof size in KiB (1 KiB = 1024 bytes)",
        "",
    ])

    return "\n".join(lines)


def generate_and_save_reports(zkvms: list[zkVM]) -> None:
    """
    Generate markdown reports for each zkVM and save to reports/ directory.
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)

    for zkvm in zkvms:
        zkvm_name = zkvm.get_name()
        # ZisK gets multi-circuit mode (all circuits inlined)
        multi_circuit = len(zkvm.get_circuits()) > 1

        md = _build_zkvm_report(zkvm, multi_circuit=multi_circuit)
        filename = f"{zkvm_name.lower().replace(' ', '_')}.md"
        md_path = os.path.join(REPORTS_DIR, filename)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md)

        print(f"wrote :: {md_path}")

    # Generate unified summary report
    summary_md = _build_summary_report(zkvms)
    summary_path = os.path.join(REPORTS_DIR, SUMMARY_REPORT_NAME)
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary_md)
    print(f"wrote :: {summary_path}")
