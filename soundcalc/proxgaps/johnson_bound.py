import math
from typing import Optional

from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime

class JohnsonBoundRegime(ProximityGapsRegime):
    """
    Johnson Bound Regime (JBR).
    """
    def identifier(self) -> str:
        if self.explicit_m is not None:
            return f"JBR(m={self.explicit_m})"
        return "JBR"


    def __init__(
        self,
        field,
        gap_to_radius: Optional[float] = None,
        explicit_m: Optional[int] = None,
    ):
        super().__init__(field)

        assert not (gap_to_radius is not None and explicit_m is not None), (
            "gap_to_radius and explicit_m are mutually exclusive"
        )

        # Optional override for the Johnson-bound gap. If set, the proximity
        # parameter becomes: 1 - sqrt(rate) - gap_to_radius.
        # Primarily used by FRI-based systems that want fixed params.
        self.gap_to_radius = gap_to_radius
        # Optional override for the Johnson-bound multiplicity m. If set,
        # the proximity parameter and list size are derived directly from m
        # (rather than computing m from the gap). Used by protocols like
        # SWIRL that commit to a specific m.
        if explicit_m:
            self.explicit_m = max(explicit_m, 1)
        else:
            self.explicit_m = None

    def get_proximity_parameter(self, rate: float, dimension: int) -> float:
        # The proximity parameter defines how close we are to the Johnson Bound 1-sqrt(rate).
        sqrt_rate = math.sqrt(rate)

        if self.explicit_m:
            # Explicit-m override: pp = 1 - sqrt(rate) - sqrt(rate)/(2*m).
            gap = sqrt_rate / (2 * self.explicit_m)
        elif self.gap_to_radius:
            # gap_to_radius override (primarily for FRI-based systems that want fixed params).
            gap = self.gap_to_radius
        else:
            # No help was provided from the config, so let's use a heuristic:
            # For large fields, use a tighter gap (closer to Johnson bound) for better
            # query-phase security. For smaller fields, use a more conservative gap.
            if self.field.F > 2**150:
                gap = sqrt_rate / 100
            else:
                gap = max(rate / 20, sqrt_rate / 100)

        assert(gap)
        return 1 - sqrt_rate - gap

    def get_max_list_size(self, rate: float, dimension: int) -> float:
        sqrt_rate = math.sqrt(rate)

        # With explicit m, the list size is (m + 0.5) / sqrt(rate).
        if self.explicit_m:
            return (self.explicit_m + 0.5) / sqrt_rate

        # Reed-Solomon codes are (1 - sqrt(rate) - gap, (2*gap*sqrt(rate))⁻¹)-list decodable.
        pp = self.get_proximity_parameter(rate, dimension)

        gap = 1 - sqrt_rate - pp
        assert gap > 0

        return 1.0 / (2 * gap * sqrt_rate)

    def get_m(self, rate: float, dimension: int) -> int:
        """
        Set m according to Theorem 4.2 of BCHKS25
        """
        if self.explicit_m:
            return self.explicit_m

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

    def get_error_multilinear(self, rate: float, dimension: int, num_functions: int) -> float:
        return self.get_error_linear(rate, dimension) * math.ceil(math.log2(num_functions))
