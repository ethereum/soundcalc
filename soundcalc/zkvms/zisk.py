from __future__ import annotations

from soundcalc.zkvms.fri_based_vm import FRIBasedCircuit, FRIBasedVM, FRIBasedVMConfig

from ..common.fields import *


class ZiskPreset:
    @staticmethod
    def default() -> FRIBasedVM:
        """
        Create a ZisK VM with multiple circuits.

        For ZisK, we populate the trace parameters from its constraint description:
            https://github.com/0xPolygonHermez/zisk/blob/main/pil/zisk.pil

        The rest of the parameters are adapted from the "eSTARK: Extending STARKs with Arguments" paper:
           https://eprint.iacr.org/2023/474
        """
        return FRIBasedVM(
            name="ZisK",
            circuits=[
                ZiskPreset._main_circuit(),
                ZiskPreset._secondary_circuit(),
            ]
        )

    @staticmethod
    def _main_circuit() -> FRIBasedCircuit:
        """
        Main ZisK circuit - the largest trace.
        """
        field = GOLDILOCKS_3

        # The blowup factor is dinamically chosen by this tool:
        #       https://github.com/0xPolygonHermez/pil2-proofman-js/blob/main/src/pil2-stark/pil_info/imPolsCalculation/imPolynomials.js#L96
        # by chosing the one (greater or equal than 2) that yields the lowest number of columns.
        # Here we just fix it to 2 for simplicity.
        blowup_factor = 2
        rho = 1 / blowup_factor

        trace_length = 1 << 22
        num_columns = 66
        batch_size = num_columns + 2  # +2 for the composition polynomials

        num_queries = 128 // int(math.log2(blowup_factor))

        AIR_max_degree = blowup_factor + 1

        # D = trace_length / rho = 2^23
        # Product of factors should equal D / early_stop = 2^23 / 2^5 = 2^18
        # [16, 16, 16, 8, 8] = 2^4 * 2^4 * 2^4 * 2^3 * 2^3 = 2^18 ✓
        FRI_folding_factors = [2**4, 2**4, 2**4, 2**3, 2**3]
        FRI_early_stop_degree = 2**5

        max_combo = 3

        hash_size_bits = 256  # TODO: check if that is actually true

        cfg = FRIBasedVMConfig(
            name="main",
            hash_size_bits=hash_size_bits,
            rho=rho,
            trace_length=trace_length,
            field=field,
            num_columns=num_columns,
            batch_size=batch_size,
            power_batching=True,
            num_queries=num_queries,
            AIR_max_degree=AIR_max_degree,
            FRI_folding_factors=FRI_folding_factors,
            FRI_early_stop_degree=FRI_early_stop_degree,
            max_combo=max_combo,
            grinding_query_phase=0,
        )
        return FRIBasedCircuit(cfg)

    @staticmethod
    def _secondary_circuit() -> FRIBasedCircuit:
        """
        Secondary ZisK circuit - smaller trace (placeholder values).
        """
        field = GOLDILOCKS_3

        blowup_factor = 2
        rho = 1 / blowup_factor

        trace_length = 1 << 21  # Smaller trace
        num_columns = 50  # Fewer columns
        batch_size = num_columns + 2

        num_queries = 128 // int(math.log2(blowup_factor))

        AIR_max_degree = blowup_factor + 1

        # D = trace_length / rho = 2^22
        # Product of factors should equal D / early_stop = 2^22 / 2^5 = 2^17
        # [16, 16, 16, 8] = 2^4 * 2^4 * 2^4 * 2^3 = 2^15... need adjustment
        # [16, 16, 8, 8, 8] = 2^4 * 2^4 * 2^3 * 2^3 * 2^3 = 2^17 ✓
        FRI_folding_factors = [2**4, 2**4, 2**3, 2**3, 2**3]
        FRI_early_stop_degree = 2**5

        max_combo = 3

        hash_size_bits = 256

        cfg = FRIBasedVMConfig(
            name="secondary",
            hash_size_bits=hash_size_bits,
            rho=rho,
            trace_length=trace_length,
            field=field,
            num_columns=num_columns,
            batch_size=batch_size,
            power_batching=True,
            num_queries=num_queries,
            AIR_max_degree=AIR_max_degree,
            FRI_folding_factors=FRI_folding_factors,
            FRI_early_stop_degree=FRI_early_stop_degree,
            max_combo=max_combo,
            grinding_query_phase=0,
        )
        return FRIBasedCircuit(cfg)
