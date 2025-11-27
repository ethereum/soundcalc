from soundcalc.common.fields import FieldParams


class ProximityGapsRegime:
    """
    A class representing a regime for proximity gaps or (mutual) correlated agreement.
    We only consider Reed-Solomon codes here, of dimension k, size n, and rate k/n.
    """

    def identifier(self) -> str:
        """
        Returns the name of the regime.
        """
        raise NotImplementedError

    def get_max_delta(self, rate: float, dimension: int, field: FieldParams) -> float:
        """
        Returns the maximum delta for this regime, based on the rate
        and the dimension of the code.
        """
        raise NotImplementedError

    def get_max_list_size(self, rate: float, dimension: int, field: FieldParams, delta: float) -> int:
        """
        Returns an upper bound on the list size for this regime, and for a given delta
        E.g., unique decoding regime may return 1.
        """
        raise NotImplementedError

    def get_error_powers(self, rate: float, dimension: int, field: FieldParams, num_functions: int) -> float:
        """
        Returns an upper bound on the MCA error when applying a random linear combination.
        The coefficients are assumed to be powers here.

        Note: the errors for correlated agreement in the following two cases differ,
        which is related to the batching method:

        Case 1: we batch with randomness r^0, r^1, ..., r^{num_functions-1}
        This is what is called batching over parameterized curves in BCIKS20.
        Here, the error depends on num_functions (called l in BCIKS20), and we find
        the error in Theorem 6.2.

        Case 2: we batch with randomness r_0 = 1, r_1, r_2, r_{num_functions-1}
        This is what is called batching over affine spaces in BCIKS20.
        Here, the error does not depend on num_functions (called l in BCIKS20), and we find
        the error in Theorem 1.6.

        Then easiest way to see the difference is to compare Theorems 1.5 and 1.6.
        """
        raise NotImplementedError

    def get_error_linear(self, rate: float, dimension: int, field: FieldParams) -> float:
        """
        Returns an upper bound on the MCA error when applying a random linear combination.
        The coefficients are assumed to be independent here.

        See the comment above about the difference between powers and linear.
        """
        raise NotImplementedError
