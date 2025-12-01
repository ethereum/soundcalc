

from soundcalc.common.fields import FieldParams
from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime


class UniqueDecodingRegime(ProximityGapsRegime):
    """
    Unique decoding Regime (UDR).
    """
    def identifier(self) -> str:
        return "UDR"

    def get_max_delta(self, rate: float, dimension: int, field: FieldParams) -> float:
        return (1 - rate) / 2

    def get_max_list_size(self, rate: float, dimension: int, field: FieldParams, delta: float) -> int:
        assert delta <= self.get_max_delta(rate, dimension, field)
        return 1

    def get_error_powers(self, rate: float, dimension: int, field: FieldParams, num_functions: int) -> float:
        return self.get_error_linear(rate, dimension, field) * (num_functions - 1)

    def get_error_linear(self, rate: float, dimension: int, field: FieldParams) -> float:
        return dimension / field.F
