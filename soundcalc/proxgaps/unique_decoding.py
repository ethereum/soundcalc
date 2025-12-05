

from soundcalc.common.fields import FieldParams
from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime


class UniqueDecodingRegime(ProximityGapsRegime):
    """
    Unique decoding Regime (UDR).
    """
    def identifier(self) -> str:
        return "UDR"

    def get_proximity_parameter(self, rate: float, dimension: int) -> float:
        return (1 - rate) / 2

    def get_max_list_size(self, rate: float, dimension: int) -> int:
        return 1

    def get_error_powers(self, rate: float, dimension: int, field: FieldParams, num_functions: int) -> float:
        return self.get_error_linear(rate, dimension, field) * (num_functions - 1)

    def get_error_linear(self, rate: float, dimension: int, field: FieldParams) -> float:
        # Using Theorem 4.1 from BCIKS20
        n = dimension / rate
        return n / field.F