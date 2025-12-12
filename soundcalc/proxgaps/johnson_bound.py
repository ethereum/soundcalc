from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime

import math
from typing import Optional

class JohnsonBoundRegime(ProximityGapsRegime):
    """
    Johnson Bound Regime (JBR).
    """

    def __init__(self, field, proximity_gap: Optional[float] = None):
        super().__init__(field)
        # Optional override for the Johnson-bound gap. If set, the proximity
        # parameter becomes: 1 - sqrt(rate) - proximity_gap.
        self.proximity_gap = proximity_gap


    def identifier(self) -> str:
        return "JBR"

    def get_proximity_parameter(self, rate: float, dimension: int) -> float:
        # The proximity parameter defines how close we are to the Johnson Bound 1-sqrt(rate).
        sqrt_rate = math.sqrt(rate)

        # Config override (primarily for FRI-based systems that want fixed params).
        if self.proximity_gap is not None:
            gap = self.proximity_gap
            return 1 - sqrt_rate - gap

        # For large fields, use a tighter gap (closer to Johnson bound) for better
        # query-phase security. For smaller fields, use a more conservative gap.
        if self.field.F > 2**150:
            gap = sqrt_rate / 100
        else:
            gap = max(rate / 20, sqrt_rate / 100)

        return 1 - sqrt_rate - gap

    def get_max_list_size(self, rate: float, dimension: int) -> int:
        # Reed-Solomon codes are (1 - sqrt(rate) - gap, (2*gap*sqrt(rate))⁻¹)-list decodable.
        sqrt_rate = math.sqrt(rate)
        pp = self.get_proximity_parameter(rate, dimension)

        gap = 1 - sqrt_rate - pp
        assert gap > 0

        return 1.0 / (2 * gap * sqrt_rate)

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

    def get_error_powers(self, rate: float, dimension: int, num_functions: int) -> float:
        return self.get_error_linear(rate, dimension) * (num_functions - 1)

    def get_error_linear(self, rate: float, dimension: int) -> float:
        """ Use Theorem 4.2 from BCHKS25 to compute the error"""

        sqrt_rate = math.sqrt(rate)

        pp = self.get_proximity_parameter(rate, dimension)
        m = self.get_m(rate, dimension)
        m_shifted = m + 0.5
        n = dimension / rate

        # Compute the first fraction
        numerator = (2 * m_shifted**5 + 3 * m_shifted * (pp * rate)) * n
        denominator = 3 * rate * sqrt_rate
        first_fraction = numerator / denominator

        # Now the second one
        second_fraction = m_shifted / sqrt_rate

        return (first_fraction + second_fraction) / self.field.F
