from __future__ import annotations

from abc import ABC, abstractmethod

from soundcalc.proxgaps.proxgaps_regime import ProximityGapsRegime


class PCS(ABC):
    """
    Abstract base class for Polynomial Commitment Schemes.
    """

    @abstractmethod
    def get_pcs_security_levels(self, regime: ProximityGapsRegime) -> dict[str, int]:
        """
        Returns PCS-specific security levels for a given regime.

        Keys are descriptive labels (e.g., "batching", "commit round 1", "query phase").
        Values are bits of security.
        """
        ...

    @abstractmethod
    def get_proof_size_bits(self) -> int:
        """Returns estimated proof size in bits."""
        ...

    @abstractmethod
    def get_expected_proof_size_bits(self) -> int:
        """Returns estimated *expected* proof size in bits."""
        ...

    @abstractmethod
    def get_rate(self) -> float:
        """Returns the code rate (rho)."""
        ...

    @abstractmethod
    def get_dimension(self) -> int:
        """Returns the code dimension (trace_length for FRI)."""
        ...

    @abstractmethod
    def get_parameter_summary(self) -> str:
        """Returns a description of the parameters of the PCS."""
        ...
