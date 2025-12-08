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

    def get_error_powers(self, rate: float, dimension: int, num_functions: int) -> float:
        return self.get_error_linear(rate, dimension) * (num_functions - 1)

    def get_error_linear(self, rate: float, dimension: int) -> float:
        # Using Theorem 1.4 (which points to Theorem 1.2) from BCIKS20
        n = dimension / rate
        return n / self.field.F
