import math
from typing import Callable, Optional, Sequence, Union

from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime

GapSchedule = Union[
    float,
    Sequence[float],
    Callable[[float, int, int], float],  # (rate, dimension, iteration) -> gap
]


def _is_plain_number(x) -> bool:
    # Accept what the old code effectively supported (float/int),
    # and explicitly reject bool (bool is a subclass of int).
    return isinstance(x, (int, float)) and not isinstance(x, bool)


class JohnsonBoundRegime(ProximityGapsRegime):
    """
    Johnson Bound Regime (JBR).
    """

    def identifier(self) -> str:
        return "JBR"

    def __init__(self, field, gap_to_radius: Optional[GapSchedule] = None):
        super().__init__(field)
        # Optional override for the Johnson-bound gap. If set, the proximity
        # parameter becomes: 1 - sqrt(rate) - gap_to_radius (or schedule output).
        self.gap_to_radius = gap_to_radius

        # If set, this instance is bound to a specific WHIR iteration.
        self._iteration: Optional[int] = None

    def for_iteration(self, iteration: int) -> "JohnsonBoundRegime":
        """
        Return a regime instance bound to a specific WHIR iteration.
        WHIR can call this once per iteration and then use the bound instance
        for all regime calls in that iteration.
        """
        reg = JohnsonBoundRegime(self.field, self.gap_to_radius)
        reg._iteration = iteration
        return reg

    def _resolve_gap(self, rate: float, dimension: int) -> float:
        """
        Resolve the gap-to-Johnson (eta).

        Supported self.gap_to_radius:
          - None: default heuristic (existing behavior)
          - float/int: constant gap (existing behavior)
          - Sequence[float]: per-iteration gaps (requires bound iteration via for_iteration)
          - Callable: schedule(rate, dimension, iteration) -> gap (requires bound iteration)

        IMPORTANT: preserve old semantics—do not coerce with float(...).
        """
        g = self.gap_to_radius

        if g is None:
            # Default heuristic (existing behavior)
            sqrt_rate = math.sqrt(rate)
            if self.field.F > 2**150:
                return sqrt_rate / 100
            return max(rate / 20, sqrt_rate / 100)

        # Constant numeric gap
        if _is_plain_number(g):
            return g

        # Per-iteration list/tuple
        if isinstance(g, (list, tuple)):
            if self._iteration is None:
                raise ValueError(
                    "gap_to_radius is per-iteration; bind via regime.for_iteration(i)"
                )
            i = self._iteration
            if i < 0 or i >= len(g):
                raise IndexError(
                    f"iteration={i} out of bounds for gap_to_radius length {len(g)}"
                )
            gi = g[i]
            if not _is_plain_number(gi):
                raise TypeError(
                    f"gap_to_radius[{i}] must be a float/int (not bool), got {type(gi)}"
                )
            return gi

        # Callable schedule
        if callable(g):
            if self._iteration is None:
                raise ValueError(
                    "gap_to_radius schedule needs iteration; bind via regime.for_iteration(i)"
                )
            gi = g(rate, dimension, self._iteration)
            if not _is_plain_number(gi):
                raise TypeError(
                    f"gap schedule must return a float/int (not bool), got {type(gi)}"
                )
            return gi

        raise TypeError(f"Unsupported gap_to_radius type: {type(g)}")

    def get_proximity_parameter(self, rate: float, dimension: int) -> float:
        # The proximity parameter defines how close we are to the Johnson Bound 1-sqrt(rate).
        sqrt_rate = math.sqrt(rate)
        gap = self._resolve_gap(rate, dimension)
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
        """Use Theorem 4.2 from BCHKS25 to compute the error"""

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
