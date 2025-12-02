

from soundcalc.common.fields import FieldParams
from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime

import math

class JohnsonBoundRegime(ProximityGapsRegime):
    """
    Johnson Bound Regime (JBR).
    """
    def identifier(self) -> str:
        return "JBR"

    def get_max_delta(self, rate: float, dimension: int, field: FieldParams) -> float:

        eta = self.get_eta(rate)

        # And proximity parameter theta = 1 - sqrt(rho) - eta
        #                               = 1 - sqrt(rho) * (1 + 1/ (2m) )
        # as required by Theorem 2 of Ha22.
        alpha = math.sqrt(rate) + eta
        theta = 1 - alpha
        return theta

    def get_max_list_size(self, rate: float, dimension: int, field: FieldParams, delta: float) -> int:
        assert delta <= self.get_max_delta(rate, dimension, field)

        # following https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/errors.rs#L43
        # By the JB, RS codes are (1 - √ρ - η, (2*η*√ρ)^-1)-list decodable.
        eta = self.get_eta(rate)
        return 1.0 / (2 * eta * math.sqrt(rate))

    def get_m(self) -> int:
        # ASN This is hardcoded to 16, whereas winterfell brute forces it:
        # https://github.com/facebook/winterfell/blob/main/air/src/proof/security.rs#L290-L306
        return 16

    def get_eta(self, rate) -> float:
        m = self.get_m()

        # ASN Is this a good value for eta?
        eta = math.sqrt(rate) / (2 * m)

        return eta

    def get_error_powers(self, rate: float, dimension: int, field: FieldParams, num_functions: int) -> float:
        return self.get_error_linear(rate, dimension, field) * (num_functions - 1)

    def get_error_linear(self, rate: float, dimension: int, field: FieldParams) -> float:
        # Using Theorem 4.2 from BCHKS25, and taking a slightly bigger bound by assuming ɣ·n <= n-1
        # This assumption simplifies the bound by removing the factor (m + 1/2)/sqrt(ρ) and the dependence on ɣ.
        m = self.get_m()
        numerator = (2 * (m + 0.5) ** 5 + 3 * (m + 0.5) * rate) * dimension
        denominator = 3 * rate * math.sqrt(rate)
        denominator *= field.F

        return numerator / denominator
