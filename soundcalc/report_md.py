"""
Markdown report generation for soundcalc.

This file is a mess.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from soundcalc.circuits.circuit import Circuit
from soundcalc.common.utils import KIB
from soundcalc.zkvms.zkvm import zkVM


REPORTS_DIR = "reports"
SUMMARY_REPORT_NAME = "summary.md"

# zkVMs excluded from the summary overview (test/dummy entries)
_SUMMARY_EXCLUDE = {"DummyWHIR", "DummySTIR"}

# Minimum requirements for a zkVM to appear in the summary overview
# See https://blog.ethereum.org/2025/12/18/zkevm-security-foundations#three-milestones
_SUMMARY_MIN_SECURITY_BITS = 100
_SUMMARY_MAX_EXPECTED_PROOF_SIZE_KIB = 600


@dataclass
class zkVMSummary:
    """Summary data for a single zkVM used in comparison reports."""
    name: str
    version: str | None
    field: str
    # Combined "<proof system> + <PCS>" label, e.g. "DEEP-ALI + FRI".
    proof_system: str
    num_circuits: int
    security_bits: float
    security_regime: str
    # None when the final circuit's proof-size estimate is a TODO (see
    # Circuit.proof_size_todo).
    final_proof_size_kib: int | None
    final_expected_proof_size_kib: int | None


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
    if final_circuit.proof_size_todo:
        final_proof_size_kib = None
    else:
        final_proof_size_kib = final_circuit.get_proof_size_bits() // KIB

    security = _best_security_across_circuits(circuits)
    offending_circuit = security["circuit"]

    return {
        "final_circuit_name": final_circuit.get_name(),
        "final_proof_size_kib": final_proof_size_kib,
        "best_regime": security["regime"],
        "min_security_bits": security["security_bits"],
        "offending_circuit": offending_circuit.get_name() if offending_circuit else None,
    }


def _field_label(field) -> str:
    if hasattr(field, "to_string"):
        return field.to_string()
    return "Unknown"


def _format_security_value(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.1f}"
    return str(value)


def _best_security_across_circuits(circuits: list[Circuit]) -> dict[str, Any]:
    """
    Find the regime with the highest minimum security across circuits,
    together with the weakest circuit in that regime.

    Only regimes reported by every circuit are compared; if there is no such
    regime, each circuit is credited with its own best regime, the weakest
    circuit wins, and the result is labeled "mixed".
    """
    regime_totals_by_circuit: list[tuple[Circuit, dict[str, int]]] = []
    for circuit in circuits:
        totals = {
            regime_name: levels["total"]
            for regime_name, levels in circuit.get_security_levels().items()
            if isinstance(levels, dict) and "total" in levels
        }
        regime_totals_by_circuit.append((circuit, totals))

    if not regime_totals_by_circuit:
        return {"security_bits": 0, "regime": "N/A", "circuit": None}

    common_regimes = set(regime_totals_by_circuit[0][1])
    for _, totals in regime_totals_by_circuit[1:]:
        common_regimes &= set(totals)

    if not common_regimes:
        circuit, min_bits = min(
            (
                (circuit, max(totals.values()))
                for circuit, totals in regime_totals_by_circuit
                if totals
            ),
            key=lambda item: item[1],
        )
        return {"security_bits": min_bits, "regime": "mixed", "circuit": circuit}

    best_regime = None
    best_min_bits = -1
    offending_circuit = None
    for regime_name in sorted(common_regimes):
        circuit, min_bits = min(
            (
                (circuit, totals[regime_name])
                for circuit, totals in regime_totals_by_circuit
            ),
            key=lambda item: item[1],
        )
        if min_bits > best_min_bits:
            best_min_bits = min_bits
            best_regime = regime_name
            offending_circuit = circuit

    return {
        "security_bits": best_min_bits,
        "regime": best_regime,
        "circuit": offending_circuit,
    }


def _proof_system_label(circuit: Circuit) -> str:
    """Get the combined "<proof system> + <PCS>" label for a circuit."""
    return f"{circuit.proof_system_name} + {circuit.pcs.label}"


def _zkvm_proof_system_label(circuits: list[Circuit]) -> str:
    labels = []
    for circuit in circuits:
        label = _proof_system_label(circuit)
        if label not in labels:
            labels.append(label)
    if len(labels) == 1:
        return labels[0]
    return "Mixed(" + ", ".join(labels) + ")"


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
            version=zkvm.version,
            field="Unknown",
            proof_system="Unknown",
            num_circuits=0,
            security_bits=0,
            security_regime="N/A",
            final_proof_size_kib=0,
            final_expected_proof_size_kib=0,
        )

    field = _field_label(circuits[0].field)
    proof_system = _zkvm_proof_system_label(circuits)

    security = _best_security_across_circuits(circuits)
    best_bits = security["security_bits"]
    best_regime = security["regime"]

    if circuits[-1].proof_size_todo:
        final_proof_kib = None
        final_expected_proof_kib = None
    else:
        final_proof_kib = int(circuits[-1].get_proof_size_bits() // KIB)
        final_expected_proof_kib = int(circuits[-1].get_expected_proof_size_bits() // KIB)

    return zkVMSummary(
        name=zkvm.get_name(),
        version=zkvm.version,
        field=field,
        proof_system=proof_system,
        num_circuits=len(circuits),
        security_bits=best_bits,
        security_regime=best_regime,
        final_proof_size_kib=final_proof_kib,
        final_expected_proof_size_kib=final_expected_proof_kib,
    )


def _is_shown_in_summary(s: zkVMSummary) -> bool:
    """
    Decide whether a zkVM appears in the summary overview.

    Hides test/dummy entries, zkVMs below the minimum security, and zkVMs
    whose expected proof size is too large. zkVMs with an unknown (TODO)
    proof size are kept.
    """
    if s.name in _SUMMARY_EXCLUDE:
        return False
    if s.security_bits < _SUMMARY_MIN_SECURITY_BITS:
        return False
    if (
        s.final_expected_proof_size_kib is not None
        and s.final_expected_proof_size_kib >= _SUMMARY_MAX_EXPECTED_PROOF_SIZE_KIB
    ):
        return False
    return True


def _get_parameter_lines(circuit: Circuit) -> list[str]:
    """Get parameter lines for a circuit."""
    return circuit.get_report_parameter_lines()


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
                row_values.append(_format_security_value(row_data.get(col, "—")))
        else:
            # Non-dict value sits under the 'total' column when present.
            for col in columns[1:]:
                if col == "total":
                    row_values.append(_format_security_value(row_data))
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

    version_suffix = f" (v{zkvm.version})" if zkvm.version else ""
    lines.append(f"# 📊 {zkvm_name}{version_suffix}")
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
            final_proof_size_kib = overview['final_proof_size_kib']
            final_proof_size_str = "**TODO**" if final_proof_size_kib is None else f"**{int(final_proof_size_kib)} KiB**"
            lines.append(f"| Final bits of security | **{_format_security_value(overview['min_security_bits'])} bits** | {offending_circuit_link} | Regime: {overview['best_regime']} |")
            lines.append(f"| Final proof size (worst case) | {final_proof_size_str} | {final_circuit_link} | |")
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
            if circuit.proof_size_todo:
                lines.append("**Proof Size:** TODO")
            else:
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
            if circuit.proof_size_todo:
                lines.append("**Proof Size:** TODO")
            else:
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
        "- Security shows the best bits of security across the reported regimes",
        f"- Only zkVMs with at least {_SUMMARY_MIN_SECURITY_BITS} bits of security "
        f"and an expected proof size below {_SUMMARY_MAX_EXPECTED_PROOF_SIZE_KIB} KiB are shown",
        "",
        "## Overview",
        "",
        "| zkVM | Version | Security | Expected Proof Size | Worst-Case Proof Size | Proof system | Field | Circuits |",
        "|------|---------|----------|---------------------|-----------------------|--------------|-------|----------|",
    ]

    summaries = sorted(
        filter(_is_shown_in_summary, (_collect_zkvm_summary(z) for z in zkvms)),
        key=lambda s: s.name.lower(),
    )

    for s in summaries:
        report_filename = f"{s.name.lower().replace(' ', '_')}.md"
        version_str = s.version if s.version else "—"
        if s.final_proof_size_kib is None:
            expected_str = "TODO"
            worst_str = "TODO"
        else:
            expected_str = f"{s.final_expected_proof_size_kib} KiB"
            worst_str = f"{s.final_proof_size_kib} KiB"
        lines.append(
            f"| [{s.name}]({report_filename}) "
            f"| {version_str} "
            f"| **{_format_security_value(s.security_bits)}** bits ({s.security_regime}) "
            f"| {expected_str} "
            f"| {worst_str} "
            f"| {s.proof_system} | {s.field} | {s.num_circuits} |"
        )

    lines.extend([
        "",
        "## Notes",
        "",
        "- **Security**: Best bits of security across the reported regimes",
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
