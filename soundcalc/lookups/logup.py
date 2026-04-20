from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import math
from typing import Optional

from soundcalc.common.fields import FieldParams
from soundcalc.common.utils import get_bits_of_security_from_error
import soundcalc.lookups.gkr as gkr

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

    # H_T is the size of the set/alphabet used to interpolate T.
    H_T: int
    # H_L is the size of the set/alphabet used to interpolate L.
    H_L: int
    # S: Number of columns of T and L (S=1 for single column case)
    num_columns_S: int = 1
    # M: Number of lookups performed on T
    num_lookups_M: int = 1
    # Proof of Work grinding (expressed in bits of security)
    grinding_bits_lookup: int = 0
    # If unspecified, defaults to true for multivariate lookups and false for
    # univariate lookups.
    # If multilinear_fingerprint = true, column aggregation is modeled as
    # multivariate and contributes a factor log2(S). Otherwise it contributes S.
    multilinear_fingerprint: Optional[bool] = None
    # Optional auxiliary soundness contribution for the multivariate case.
    reduction_error: float = 0.0

    def __post_init__(self):
        if self.multilinear_fingerprint is None:
            self.multilinear_fingerprint = self.logup_type == LogUpType.MULTIVARIATE

class LogUp:
    def __init__(self, config: LogUpConfig):
        self.config = config

    def _get_column_aggregation_factor(self, S: int) -> float:
        """
        Returns R, the soundness multiplier induced by column aggregation.

        For univariate aggregation R = S.
        For multivariate aggregation R = log2(S), with the single-column case
        normalized to R = 1.
        """
        if self.config.multilinear_fingerprint:
            return max(math.log2(S), 1.0)
        return float(S)

    def _calculate_soundness_error(self) -> float:
        """
        Calculates lookup soundness using the unified lookup model:
            K * H * R / F
        where H = H_L + H_T and R is the column aggregation factor.

        For multivariate lookups, we additionally account for the GKR
        soundness term and any configured reduction error.
        """
        F = self.config.field.F
        H = self.config.H_L + self.config.H_T
        S = self.config.num_columns_S
        K = self.config.num_lookups_M
        R = self._get_column_aggregation_factor(S)
        total_error = (K * H * R) / F

        if self.config.logup_type == LogUpType.MULTIVARIATE:
            total_error += gkr.get_gkr_soundness_error(self.config.field, H, K)
            total_error += self.config.reduction_error

        return total_error

    def get_soundness_bits(self) -> int:
        """Returns LogUp soundness in bits of security."""
        total_error = self._calculate_soundness_error()
        # Add grinding
        total_error *= 2 ** (-self.config.grinding_bits_lookup)
        return get_bits_of_security_from_error(total_error)

    def get_name(self) -> str:
        return self.config.name
