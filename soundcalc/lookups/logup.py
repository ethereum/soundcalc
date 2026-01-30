from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import math

from soundcalc.common.fields import FieldParams
from soundcalc.common.utils import get_bits_of_security_from_error
from soundcalc.pcs.pcs import PCS
from soundcalc.proxgaps.johnson_bound import JohnsonBoundRegime
from soundcalc.proxgaps.unique_decoding import UniqueDecodingRegime

class LogUpType(Enum):
    UNIVARIATE = "univariate"
    MULTIVARIATE = "multivariate"

@dataclass
class LogUpConfig:
    """Configuration for LogUp based on Ethereum Foundation soundness specs."""
    name: str
    pcs: PCS
    field: FieldParams
<<<<<<< HEAD:soundcalc/lookups/logup.py
    # Total columns used for logUP$num_$
    num_arg_columns: int | None = None
    # Trace length
    trace_length: int | None = None
     # Optimization parameter
    ell: int = 1
    #Johnson Bound Regime
=======
    logup_type: LogUpType
    
    # L: Rows of lookup table L (includes dummy padding)
    rows_L: int 
    # T: Rows of fixed table T (includes dummy padding)
    rows_T: int
    # S: Number of columns (S=1 for single column case)
    num_columns_S: int = 1
    # M: Number of lookups performed (Aggregation factor)
    num_lookups_M: int = 1
    # H: Alphabet size 
    alphabet_size_H: int | None = None
    
    # Reduction error for Multivariate (case i or ii)
    reduction_error: float = 0.0
>>>>>>> 3b29563 (refactor: implement univariate and multivariate logup soundness errors):soundcalc/zkvms/lookups.py
    gap_to_radius: float | None = None

class LogUp:
    def __init__(self, config: LogUpConfig):
        self.config = config

    def _calculate_sum_error(self) -> float:
        """
        Calculates epsilon_sum based on the logic in the provided document.
        """
        F = self.config.field.F
        L = self.config.rows_L
        T = self.config.rows_T
        S = self.config.num_columns_S
        M = self.config.num_lookups_M
        
        if self.config.logup_type == LogUpType.UNIVARIATE:
            # Univariate Soundness Error:
            # Single/Multi-column: (L + T) * S / F
            # Aggregation: M * (L + T) * S / F
            epsilon_sum = (M * (L + T) * S) / F
            return epsilon_sum

        elif self.config.logup_type == LogUpType.MULTIVARIATE:
            # Multivariate Soundness Error:
            # H is max{TS, LS} or padded height
            H = self.config.alphabet_size_H or max(L * S, T * S)
            
            # Single/Multi column (treated as tensors): 2H / F
            # Aggregation: K * 2H / F (where K is num_lookups_M)
            epsilon_sum = (M * 2 * H) / F
            
            # Add reduction error (from multivariate-to-univariate or logup-sound)
            return epsilon_sum + self.config.reduction_error

        return 1.0 # Should not reach here

    def get_security_levels(self) -> dict[str, dict[str, int]]:
        """Calculates soundness for UDR and JBR regimes."""
        regimes = [
            UniqueDecodingRegime(self.config.field),
            JohnsonBoundRegime(self.config.field, gap_to_radius=self.config.gap_to_radius),
        ]

        result = {}
        
        # Calculate total error epsilon_sum
        total_error = self._calculate_sum_error()
        logup_bits = get_bits_of_security_from_error(total_error)

        for regime in regimes:
            rid = regime.identifier()
            # Get PCS security (FRI/KZG/etc)
            levels = self.config.pcs.get_pcs_security_levels(regime)
            
            # logup soundness
            levels["logup_sum"] = logup_bits
            
            # Total security is limited by the weakest link
            levels["total"] = min(levels.values())
            result[rid] = levels

        return result

    def get_name(self) -> str:
        return self.config.name
