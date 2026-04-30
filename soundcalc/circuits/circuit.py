from __future__ import annotations

from abc import ABC, abstractmethod

from soundcalc.common.fields import FieldParams
from soundcalc.lookups.logup import LogUp
from soundcalc.pcs.pcs import PCS


class Circuit(ABC):
    """
    Abstract base class for a circuit within a zkVM.

    A circuit is proved with a specific proof system (e.g. DEEP-ALI, Jagged, SWIRL).

    Each circuit has its own parameters and security analysis.
    Subclasses implement the specific proof system logic.
    """

    # These attributes must be set by each subclass __init__
    name: str
    pcs: PCS
    field: FieldParams
    # The name of the proof system (e.g. "DEEP-ALI", "Jagged", "SWIRL").
    proof_system_name: str

    # Set to True when the circuit does not yet expose a full proof-size estimate.
    # When True, reports render "TODO" for proof size.
    proof_size_todo: bool = False

    def get_name(self) -> str:
        """Returns the name of the circuit."""
        return self.name

    def get_lookups(self) -> list[LogUp]:
        """Returns the list of lookups for this circuit."""
        return []

    def get_proof_size_bits(self) -> int:
        """Returns an estimate for the proof size, given in bits."""
        return self.pcs.get_proof_size_bits()

    def get_expected_proof_size_bits(self) -> int:
        """Returns an estimate for the *expected* proof size, given in bits."""
        return self.pcs.get_expected_proof_size_bits()

    @abstractmethod
    def get_security_levels(self) -> dict[str, dict[str, float]]:
        """
        Returns a dictionary that maps each regime (i.e., a way of doing security analysis)
        to a dictionary that contains the round-by-round soundness levels.

        It maps from a label that describes the regime (e.g., UDR, JBR in case of FRI) to a
        regime-specific dictionary. Any such regime-specific dictionary is as follows:

        It maps from a label that explains which round it is for to an integer.
        If this integer is, say, k, then it means the error for this round is at
        most 2^{-k}.
        """
        ...

    @abstractmethod
    def get_parameter_summary(self) -> str:
        """Returns a description of the parameters of the circuit."""
        ...

    @abstractmethod
    def get_report_parameter_lines(self) -> list[str]:
        """Returns markdown-formatted parameter lines for reports."""
        ...
