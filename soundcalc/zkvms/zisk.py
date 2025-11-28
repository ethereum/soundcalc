from __future__ import annotations

from soundcalc.zkvms.fri_based_vm import FRIBasedVM, FRIBasedVMConfig

from ..common.fields import *


class ZiskPreset:
    @staticmethod
    def default() -> "ZiskPreset":
        """
        Populate a zkEVMConfig instance with zkVM parameters.

        For ZisK, we populate the trace parameters from its constraint description:
            https://github.com/0xPolygonHermez/zisk/blob/main/pil/zisk.pil
        """

        # We generate a STARK proof of different traces with different parameters.
        # Therefore, in what follows, we put the parameters for our worst-case trace
        # in terms of columns and batch size.

        # The blowup factor is dinamically chosen by this tool:
        #       https://github.com/0xPolygonHermez/pil2-proofman-js/blob/main/src/pil2-stark/pil_info/imPolsCalculation/imPolynomials.js#L96
        # by chosing the one (greater or equal than 2) that yields the lowest number of columns.
        # Here we just fix it to 2 for simplicity.
        blowup_factor = 2
        rho = 1 / blowup_factor

        trace_length = 1 << 16
        num_columns = 3024
        batch_size = 4065

        num_queries = 128

        AIR_max_degree = 3

        FRI_folding_factor = 2**4
        FRI_early_stop_degree = 2**5

        max_combo = 2

        cfg = FRIBasedVMConfig(
            name="ZisK",
            hash_size_bits=256,
            rho=rho,
            trace_length=trace_length,
            field=GOLDILOCKS_3,
            num_columns=num_columns,
            batch_size=batch_size,
            power_batching=True,
            num_queries=num_queries,
            AIR_max_degree=AIR_max_degree,
            FRI_folding_factor=FRI_folding_factor,
            FRI_early_stop_degree=FRI_early_stop_degree,
            max_combo=max_combo,
            grinding_query_phase=0,
        )
        return FRIBasedVM(cfg)
