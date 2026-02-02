from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import math

from soundcalc.common.fields import FieldParams
from soundcalc.common.utils import get_bits_of_security_from_error

class LogUpType(Enum):
    UNIVARIATE = "univariate"
    MULTIVARIATE = "multivariate"

@dataclass
class LogUpConfig:
    """
    Configuration for LogUp

    Please see the math companion for more information on how we work with lookup soundness.
    """
    name: str
    field: FieldParams
    logup_type: LogUpType

    # T: Rows of "big" table T
    rows_T: int
    # L: Rows of "small" table L
    # L is the table is looked-up inside T
    rows_L: int
    # S: Number of columns of T and L (S=1 for single column case)
    num_columns_S: int = 1
    # M: Number of lookups performed on T
    num_lookups_M: int = 1
    # H: Alphabet size
    alphabet_size_H: int | None = None
    # Proof of Work grinding (expressed in bits of security)
    grinding_lookup: int = 0

    # Reduction error for the Multivariate case (case i or ii)
    reduction_error: float = 0.0

class LogUp:
    def __init__(self, config: LogUpConfig):
        self.config = config

    def _calculate_univariate_error(self, F: int, T: int, L: int, S: int, M: int) -> float:
        """
        Calculates univariate LogUp soundness error.

        Single/Multi-column: (L + T) * S / F
        Aggregation: M * (L + T) * S / F
        """
        return (M * (L + T) * S) / F

    def _calculate_multivariate_error(self, F: int, T: int, L: int, S: int, M: int) -> float:
        """
        Calculates multivariate LogUp soundness error.

        H is max{TS, LS} or padded height.
        Single/Multi column (treated as tensors): 2H / F
        Aggregation: M * 2H / F
        """
        H = self.config.alphabet_size_H or max(L * S, T * S)

        epsilon_sum = (M * 2 * H) / F

        # Add reduction error (from multivariate-to-univariate or logup-sound)
        return epsilon_sum + self.config.reduction_error

    def _calculate_soundness_error(self) -> float:
        """
        Calculates epsilon_sum as seen in math companion: "Lookup soundness calculation" section
        """
        F = self.config.field.F
        T = self.config.rows_T
        L = self.config.rows_L
        S = self.config.num_columns_S
        M = self.config.num_lookups_M

        if self.config.logup_type == LogUpType.UNIVARIATE:
            return self._calculate_univariate_error(F, T, L, S, M)
        else:
            assert self.config.logup_type == LogUpType.MULTIVARIATE
            return self._calculate_multivariate_error(F, T, L, S, M)

    def get_soundness_bits(self) -> int:
        """Returns LogUp soundness in bits of security."""
        total_error = self._calculate_soundness_error()
        #Add grinding
        total_error *= 2 ** (-self.config.grinding_lookup)
        return get_bits_of_security_from_error(total_error)

    def get_name(self) -> str:
        return self.config.name
