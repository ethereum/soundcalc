from __future__ import annotations

from abc import ABC, abstractmethod

from soundcalc.common.utils import apply_grinding
from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime


class PCS(ABC):
    """
    Abstract base class for Polynomial Commitment Schemes.
    """

    # Human-readable label for this PCS type (e.g. "FRI", "WHIR").
    # Subclasses must set this.
    label: str

    # Batching parameters used by `_get_batching_error`.
    # Subclasses must set these in `__init__` (except `multilinear_batching`,
    # which only FRI supports; the other schemes keep the default).
    batch_size: int
    power_batching: bool
    multilinear_batching: bool = False
    grinding_batching_phase: int

    @abstractmethod
    def get_report_parameter_lines(self) -> list[str]:
        """Returns markdown-formatted parameter lines for reports."""
        ...

    @abstractmethod
    def get_pcs_security_levels(self, regime: ProximityGapsRegime) -> dict[str, int]:
        """
        Returns PCS-specific security levels for a given regime.

        Keys are descriptive labels (e.g., "batching", "commit round 1", "query phase").
        Values are bits of security.
        """
        ...

    def _get_batching_error(self, regime: ProximityGapsRegime) -> float:
        """
        Returns the error due to the batching step. This depends on whether batching is done
        with powers, with multilinear weights, or with random coefficients.

        The batched functions live in the initial code of the PCS, given by
        `get_rate()` and `get_dimension()`.

        This follows https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/whir.rs#L144
        """
        rate = self.get_rate()
        dimension = self.get_dimension()

        # Calculate Base Error
        #
        # The error depends on how we combine the polynomials.
        if self.power_batching:
            # Power Batching: sum c^i * f_i
            # Error is typically proportional to (batch_size - 1) * list_size / |F|
            epsilon = regime.get_error_powers(rate, dimension, self.batch_size)
        elif self.multilinear_batching:
            # Multilinear Batching: sum eq(r, i) * f_i
            epsilon = regime.get_error_multilinear(rate, dimension, self.batch_size)
        else:
            # Linear Batching: sum r_i * f_i (where r_i are independent)
            # Error is typically list_size / |F| (independent of batch_size)
            epsilon = regime.get_error_linear(rate, dimension)

        # Apply Grinding
        #
        # Reducing error by expending computational work (2^-bits).
        return apply_grinding(epsilon, self.grinding_batching_phase)

    @abstractmethod
    def _get_proof_size_bits(self, expected: bool) -> int:
        """
        Returns the estimated proof size in bits.

        With `expected=False` this is the worst case (every query opens a full Merkle path).
        With `expected=True` it accounts for Merkle path sharing between queries.
        """
        ...

    def get_proof_size_bits(self) -> int:
        """Returns estimated proof size in bits."""
        return self._get_proof_size_bits(expected=False)

    def get_expected_proof_size_bits(self) -> int:
        """Returns estimated *expected* proof size in bits."""
        return self._get_proof_size_bits(expected=True)

    @abstractmethod
    def get_rate(self) -> float:
        """Returns the code rate (rho)."""
        ...

    @abstractmethod
    def get_dimension(self) -> int:
        """Returns the code dimension (trace_length for FRI)."""
        ...

    @abstractmethod
    def get_trace_length(self) -> int:
        """Returns the length of the trace."""
        ...

    @abstractmethod
    def get_parameter_summary(self) -> str:
        """Returns a description of the parameters of the PCS."""
        ...
