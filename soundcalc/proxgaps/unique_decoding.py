from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime
import math

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
        # Using Corollary 1.4 (which points to Theorem 1.3) from BCHKS25
        gamma = (1 - rate) / 2
        n = dimension / rate
        return (gamma * n + 1) / self.field.F
    
    def get_error_multilinear(self, rate: float, dimension: int, num_functions: int) -> float:
        return self.get_error_linear(rate, dimension) * math.ceil(math.log2(num_functions))
