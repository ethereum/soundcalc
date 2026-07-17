from __future__ import annotations

import math
from dataclasses import dataclass

from soundcalc.circuits.circuit import Circuit
from soundcalc.circuits.swirl.calculator import SWIRLSystemParams, calculate_swirl_soundness
from soundcalc.circuits.swirl.proof_size import (
    SWIRLProofSizeBreakdown,
    SWIRLProofSizeConfig,
    get_swirl_proof_size_bits,
    get_swirl_proof_size_breakdown_bits,
)
from soundcalc.common.fields import FieldParams
from soundcalc.pcs.whir import WHIR


@dataclass(frozen=True)
class SWIRLCircuitConfig:
    name: str
    pcs: WHIR
    field: FieldParams
    params: SWIRLSystemParams
    max_num_constraints_per_air: int
    num_airs: int
    max_log_trace_height: int
    num_trace_columns: int
    max_interactions_per_air: int
    soundness_max_num_constraints_per_air: int
    soundness_num_airs: int
    soundness_max_log_trace_height: int
    soundness_num_trace_columns: int
    soundness_max_interactions_per_air: int
    proof_size_num_airs: int
    proof_size_max_log_trace_height: int
    proof_size_num_trace_columns: int
    proof_size_max_interactions_per_air: int
    proof_size_num_public_values: int = 0


class SWIRLCircuit(Circuit):
    def __init__(self, config: SWIRLCircuitConfig):
        self.name = config.name
        self.pcs = config.pcs
        self.field = config.field
        self.proof_system_name = "SWIRL"
        self.params = config.params
        self.max_num_constraints_per_air = config.max_num_constraints_per_air
        self.num_airs = config.num_airs
        self.max_log_trace_height = config.max_log_trace_height
        self.num_trace_columns = config.num_trace_columns
        self.max_interactions_per_air = config.max_interactions_per_air
        self.soundness_max_num_constraints_per_air = config.soundness_max_num_constraints_per_air
        self.soundness_num_airs = config.soundness_num_airs
        self.soundness_max_log_trace_height = config.soundness_max_log_trace_height
        self.soundness_num_trace_columns = config.soundness_num_trace_columns
        self.soundness_max_interactions_per_air = config.soundness_max_interactions_per_air
        self.proof_size_num_airs = config.proof_size_num_airs
        self.proof_size_max_log_trace_height = config.proof_size_max_log_trace_height
        self.proof_size_num_trace_columns = config.proof_size_num_trace_columns
        self.proof_size_max_interactions_per_air = (
            config.proof_size_max_interactions_per_air
        )
        self.proof_size_num_public_values = config.proof_size_num_public_values

    def get_security_levels(self) -> dict[str, dict[str, int]]:
        levels = calculate_swirl_soundness(
            params=self.params,
            field=self.field,
            whir=self.pcs,
            max_num_constraints_per_air=self.soundness_max_num_constraints_per_air,
            num_airs=self.soundness_num_airs,
            max_log_trace_height=self.soundness_max_log_trace_height,
            num_trace_columns=self.soundness_num_trace_columns,
            max_interactions_per_air=self.soundness_max_interactions_per_air,
        )
        report_levels = {
            k: math.floor(v)
            for k, v in levels.items()
            if k != "total"
        }
        report_levels["total"] = min(report_levels.values())
        return {self._regime_label(): report_levels}

    def _regime_label(self) -> str:
        return "UDR" if self.params.whir.explicit_regime == "unique" else "JBR"

    def _uses_soundness_bounds(self) -> bool:
        return (
            self.soundness_max_num_constraints_per_air,
            self.soundness_num_airs,
            self.soundness_max_log_trace_height,
            self.soundness_num_trace_columns,
            self.soundness_max_interactions_per_air,
        ) != (
            self.max_num_constraints_per_air,
            self.num_airs,
            self.max_log_trace_height,
            self.num_trace_columns,
            self.max_interactions_per_air,
        )

    def _uses_proof_size_bounds(self) -> bool:
        return (
            self.proof_size_num_airs,
            self.proof_size_max_log_trace_height,
            self.proof_size_num_trace_columns,
            self.proof_size_max_interactions_per_air,
        ) != (
            self.num_airs,
            self.max_log_trace_height,
            self.num_trace_columns,
            self.max_interactions_per_air,
        )

    def _proof_size_config(self) -> SWIRLProofSizeConfig:
        return SWIRLProofSizeConfig(
            params=self.params,
            field=self.field,
            whir=self.pcs,
            hash_size_bits=self.pcs.hash_size_bits,
            num_airs=self.proof_size_num_airs,
            max_log_trace_height=self.proof_size_max_log_trace_height,
            num_trace_columns=self.proof_size_num_trace_columns,
            max_interactions_per_air=self.proof_size_max_interactions_per_air,
            num_public_values=self.proof_size_num_public_values,
        )

    def get_proof_size_bits(self) -> int:
        return get_swirl_proof_size_bits(self._proof_size_config())

    def get_expected_proof_size_bits(self) -> int:
        return self.get_proof_size_bits()

    def get_proof_size_breakdown_bits(self) -> SWIRLProofSizeBreakdown:
        return get_swirl_proof_size_breakdown_bits(self._proof_size_config())

    def get_parameter_summary(self) -> str:
        lines = [
            "",
            "```",
            f"  proof_system_name          : {self.proof_system_name}",
            f"  pcs                        : {self.pcs.label}",
            f"  field                      : {self.field.to_string()}",
            f"  l_skip                     : {self.params.l_skip}",
            f"  n_stack                    : {self.params.n_stack}",
            f"  w_stack                    : {self.params.w_stack}",
            f"  log_blowup                 : {self.params.log_blowup}",
            f"  max_constraint_degree      : {self.params.max_constraint_degree}",
            f"  whir_queries               : {[round_config.num_queries for round_config in self.params.whir.rounds]}",
            f"  whir_folding_pow_bits      : {self.params.whir.folding_pow_bits}",
            f"  whir_query_phase_pow_bits  : {self.params.whir.query_phase_pow_bits}",
            f"  whir_mu_pow_bits           : {self.params.whir.mu_pow_bits}",
        ]
        lines.extend([
            f"  max_constraints_per_air    : {self.max_num_constraints_per_air}",
            f"  num_airs                   : {self.num_airs}",
            f"  max_log_trace_height       : {self.max_log_trace_height}",
            f"  num_trace_columns          : {self.num_trace_columns}",
            f"  max_interactions_per_air   : {self.max_interactions_per_air}",
        ])
        if self._uses_soundness_bounds():
            lines.extend([
                f"  soundness_max_constraints_per_air : {self.soundness_max_num_constraints_per_air}",
                f"  soundness_num_airs                : {self.soundness_num_airs}",
                f"  soundness_max_log_trace_height    : {self.soundness_max_log_trace_height}",
                f"  soundness_num_trace_columns       : {self.soundness_num_trace_columns}",
                f"  soundness_max_interactions_per_air: {self.soundness_max_interactions_per_air}",
            ])
        if self._uses_proof_size_bounds():
            lines.extend([
                f"  proof_size_num_airs                : {self.proof_size_num_airs}",
                f"  proof_size_max_log_trace_height    : {self.proof_size_max_log_trace_height}",
                f"  proof_size_num_trace_columns       : {self.proof_size_num_trace_columns}",
                f"  proof_size_max_interactions_per_air: {self.proof_size_max_interactions_per_air}",
            ])
        lines.extend([
            f"  proof_size_num_public_values       : {self.proof_size_num_public_values}",
        ])
        lines.append("```")
        return "\n".join(lines)

    def get_report_parameter_lines(self) -> list[str]:
        lines = [
            f"- Proof system: {self.proof_system_name}",
            f"- PCS: {self.pcs.label}",
            f"- Field: {self.field.to_string()}",
            f"- Regime: {self._regime_label()}",
        ]
        if self.params.whir.explicit_m is not None:
            lines.append(f"- `m`: {self.params.whir.explicit_m}")
        lines.extend([
            f"- `l_skip`: {self.params.l_skip}",
            f"- `n_stack`: {self.params.n_stack}",
            f"- `w_stack`: {self.params.w_stack}",
            f"- Log blowup: {self.params.log_blowup}",
            f"- WHIR queries per round: {[round_config.num_queries for round_config in self.params.whir.rounds]}",
            f"- WHIR folding PoW (bits): {self.params.whir.folding_pow_bits}",
            f"- WHIR query-phase PoW (bits): {self.params.whir.query_phase_pow_bits}",
            f"- WHIR μ PoW (bits): {self.params.whir.mu_pow_bits}",
            f"- Max constraints per AIR: {self.max_num_constraints_per_air}",
            f"- Number of AIRs: {self.num_airs}",
            f"- Max log trace height: {self.max_log_trace_height}",
            f"- Number of trace columns: {self.num_trace_columns}",
            f"- Max interactions per AIR: {self.max_interactions_per_air}",
        ])
        if self._uses_soundness_bounds():
            lines.extend([
                f"- Soundness max constraints per AIR: {self.soundness_max_num_constraints_per_air}",
                f"- Soundness number of AIRs bound: {self.soundness_num_airs}",
                f"- Soundness max log trace height bound: {self.soundness_max_log_trace_height}",
                f"- Soundness trace columns bound: {self.soundness_num_trace_columns}",
                f"- Soundness max interactions per AIR bound: {self.soundness_max_interactions_per_air}",
            ])
        if self._uses_proof_size_bounds():
            lines.extend([
                f"- Proof-size number of AIRs bound: {self.proof_size_num_airs}",
                f"- Proof-size max log trace height bound: {self.proof_size_max_log_trace_height}",
                f"- Proof-size trace columns bound: {self.proof_size_num_trace_columns}",
                f"- Proof-size max interactions per AIR bound: {self.proof_size_max_interactions_per_air}",
            ])
        lines.extend([
            f"- Proof-size public values bound: {self.proof_size_num_public_values}",
        ])
        return lines
