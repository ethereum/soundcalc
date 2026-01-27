from __future__ import annotations

from dataclasses import dataclass

from soundcalc.common.utils import get_bits_of_security_from_error
from soundcalc.proxgaps.johnson_bound import JohnsonBoundRegime
from soundcalc.proxgaps.unique_decoding import UniqueDecodingRegime

@dataclass
class LogUpConfig:
    """Minimal configuration for LogUp."""
    name: str
    pcs: PCS
    field: FieldParams
    # Total columns used for logUP$num_$
    num_arg_columns: int | None = None
    # Trace length
    trace_length: int | None = None
     # Optimization parameter
    ell: int = 1
    #Johnson Bound Regime
    gap_to_radius: float | None = None


class LogUp:
    def __init__(self, config: LogUpConfig):
        self.config = config

    def get_security_levels(self) -> dict[str, dict[str, int]]:
        """Calculates soundness for UDR and JBR regimes."""
        regimes = [
            UniqueDecodingRegime(self.config.field),
            JohnsonBoundRegime(self.config.field, gap_to_radius=self.config.gap_to_radius),
        ]

        result = {}

        # Pre-calculate common error: \ell(H-1)/(F-H)
       	field_size = self.config.field.F
       	M = self.config.num_arg_columns
       	H = self.config.trace_length
        ell= self.config.ell
        logup_error =   ell * (H - 1) / (field_size - H)
        logup_bits = get_bits_of_security_from_error(logup_error)

        for regime in regimes:
            id = regime.identifier()
            levels = self.config.pcs.get_pcs_security_levels(regime)
            levels["logup"] = logup_bits
            levels["total"] = min(levels.values())
            result[id] = levels

        return result

    def get_name(self) -> str:
        return self.config.name
