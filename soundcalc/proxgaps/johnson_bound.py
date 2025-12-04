

from soundcalc.common.fields import FieldParams
from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime

import math

class JohnsonBoundRegime(ProximityGapsRegime):
    """
    Johnson Bound Regime (JBR).
    """
    def identifier(self) -> str:
        return "JBR"

    def get_gamma(self, rate: float, dimension: int) -> float:
        # According to Theorem 4.2 of BCHKS25,
        # gamma defines how close we are to 1-sqrt(rho).
        # TODO: We are doing 1/n, but this is arbitrary. Think about it more carefully
        return 1 - math.sqrt(rate) - (1 / dimension)

    def get_max_delta(self, rate: float, dimension: int, _field: FieldParams) -> float:
        # In BCHKS25, what other papers denote as delta, is denoted as gamma.
        # So just return gamma here.
        return self.get_gamma(rate, dimension)

    def get_max_list_size(self, rate: float, dimension: int, field: FieldParams, delta: float) -> int:
        assert delta <= self.get_max_delta(rate, dimension, field)

        # following https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/errors.rs#L43
        # By the JB, RS codes are (1 - √ρ - η, (2*η*√ρ)^-1)-list decodable.
        eta = self.get_eta(rate, dimension)
        return 1.0 / (2 * eta * math.sqrt(rate))

    def get_m(self, rate: float, dimension: int) -> int:
        """
        Set m according to Theorem 4.2 of BCHKS25
        """
        sqrt_rho = math.sqrt(rate)

        gamma = self.get_gamma(rate, dimension)

        # Theorem 4.2 of BCHKS25 says:
        #    m = max{ ceil( sqrt(rho) / (1 - sqrt(rho) - gamma) ), 3 }
        denominator = 1 - sqrt_rho - gamma
        assert(denominator > 0)
        m = math.ceil(sqrt_rho / denominator)
        return max(m, 3)

    def get_eta(self, rate: float, dimension: int) -> float:
        m = self.get_m(rate, dimension)

        # ASN Is this a good value for eta?
        eta = math.sqrt(rate) / (2 * m)

        return eta

    def get_error_powers(self, rate: float, dimension: int, field: FieldParams, num_functions: int) -> float:
        return self.get_error_linear(rate, dimension, field) * (num_functions - 1)

    def get_error_linear(self, rate: float, dimension: int, field: FieldParams) -> float:
        sqrt_rho = math.sqrt(rate)

        gamma = self.get_gamma(rate, dimension)
        m = self.get_m(rate, dimension)

        # Using Theorem 4.2 from BCHKS25,
        # compute the first fraction
        numerator = (2 * (m + 0.5) ** 5 + 3 * (m + 0.5) * (rate * gamma)) * dimension
        denominator = 3 * rate * sqrt_rho
        denominator *= field.F
        first_fraction = numerator / denominator

        # Now the second one
        second_fraction = (m + 0.5) / (sqrt_rho * field.F)

        return first_fraction + second_fraction
