

from soundcalc.common.fields import FieldParams
from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime

import math

class JohnsonBoundRegime(ProximityGapsRegime):
    """
    Johnson Bound Regime (JBR).
    """
    def identifier(self) -> str:
        return "JBR"

    def get_proximity_parameter(self, rate: float, dimension: int) -> float:
        # The proximity parameter defines how close we are to the Johnson Bound 1-sqrt(rate).
        n = dimension / rate
        return 1 - math.sqrt(rate) - (1 / n)

    def get_max_list_size(self, rate: float, dimension: int) -> int:
        # Reed-Solomon codes are (1 - sqrt(rate) - pp, (2*pp*sqrt(rate))⁻¹)-list decodable.
        sqrt_rate = math.sqrt(rate)
        pp = self.get_proximity_parameter(rate, dimension)
        assert pp < 1 - sqrt_rate

        return 1.0 / (2 * pp * sqrt_rate)

    def get_m(self, rate: float, dimension: int) -> int:
        """
        Set m according to Theorem 4.2 of BCHKS25
        """
        sqrt_rate = math.sqrt(rate)
        pp = self.get_proximity_parameter(rate, dimension)
        assert pp < 1 - sqrt_rate

        # Theorem 4.2 of BCHKS25 says:
        #    m = max{ ceil( sqrt(rate) / (1 - sqrt(rate) - pp) ), 3 }
        denominator = 1 - sqrt_rate - pp
        m = math.ceil(sqrt_rate / denominator)
        return max(m, 3)

    def get_error_powers(self, rate: float, dimension: int, field: FieldParams, num_functions: int) -> float:
        return self.get_error_linear(rate, dimension, field) * (num_functions - 1)

    def get_error_linear(self, rate: float, dimension: int, field: FieldParams) -> float:
        sqrt_rate = math.sqrt(rate)

        pp = self.get_proximity_parameter(rate, dimension)
        m = self.get_m(rate, dimension)
        m_shifted = m + 0.5
        n = dimension / rate

        # Using Theorem 4.2 from BCHKS25,
        # compute the first fraction
        numerator = (2 * m_shifted**5 + 3 * m_shifted * (pp * rate)) * n
        denominator = 3 * rate * sqrt_rate
        first_fraction = numerator / denominator

        # Now the second one
        second_fraction = m_shifted / sqrt_rate

        return (first_fraction + second_fraction) / field.F
