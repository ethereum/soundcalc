from __future__ import annotations

from dataclasses import dataclass

from soundcalc.circuits.circuit import Circuit
from soundcalc.circuits.swirl.calculator import SWIRLSystemParams, calculate_swirl_soundness
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


class SWIRLCircuit(Circuit):
    def __init__(self, config: SWIRLCircuitConfig):
        self.name = config.name
        self.pcs = config.pcs
        self.field = config.field
        self.protocol_label = "SWIRL + WHIR"
        self.params = config.params
        self.max_num_constraints_per_air = config.max_num_constraints_per_air
        self.num_airs = config.num_airs
        self.max_log_trace_height = config.max_log_trace_height
        self.num_trace_columns = config.num_trace_columns
        self.max_interactions_per_air = config.max_interactions_per_air

    def get_security_levels(self) -> dict[str, dict[str, float]]:
        levels = calculate_swirl_soundness(
            params=self.params,
            field=self.field,
            whir=self.pcs,
            max_num_constraints_per_air=self.max_num_constraints_per_air,
            num_airs=self.num_airs,
            max_log_trace_height=self.max_log_trace_height,
            num_trace_columns=self.num_trace_columns,
            max_interactions_per_air=self.max_interactions_per_air,
        )
        return {self._regime_label(): {k: round(v, 1) for k, v in levels.items()}}

    def _regime_label(self) -> str:
        return "UDR" if self.params.whir.explicit_regime == "unique" else "JBR"

    def get_parameter_summary(self) -> str:
        lines = [
            "",
            "```",
            "  protocol_family            : SWIRL",
            "  pcs                        : WHIR",
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
            f"  max_constraints_per_air    : {self.max_num_constraints_per_air}",
            f"  num_airs                   : {self.num_airs}",
            f"  max_log_trace_height       : {self.max_log_trace_height}",
            f"  num_trace_columns          : {self.num_trace_columns}",
            f"  max_interactions_per_air   : {self.max_interactions_per_air}",
            "```",
        ]
        return "\n".join(lines)

    def get_report_parameter_lines(self) -> list[str]:
        lines = [
            "- Proof system: SWIRL",
            "- Inner PCS: WHIR",
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
        return lines
