from __future__ import annotations

from .zkevm import zkEVMConfig, zkEVMParams
from ..common.fields import *


class PicoPreset:
    @staticmethod
    def default() -> "PicoPreset":
        """
        Populate a zkEVMConfig instance with Pico parameters.

        Pico's STARK backend is built on top of Plonky3's `TwoAdicFriPcs` polynomial commitment scheme.
        All chip traces (preprocessed, main, permutation and quotient) are committed to the same PCS,
        and their columns are opened jointly in a single batched FRI opening.

        Reference: https://github.com/brevis-network/pico/blob/f84173e7d7200201a582cf38ad9b7c4bff63fdf4/vm/src/machine/prover.rs#L581-L589

        We currently focus only on Pico's RISC-V proving phase. The recursion proving phase is not considered for now.
        """
        field = KOALABEAR_4

        # RISC-V phase uses a fixed blowup factor = 2.
        # Reference: https://github.com/brevis-network/pico/blob/f84173e7d7200201a582cf38ad9b7c4bff63fdf4/vm/src/configs/stark_config/kb_poseidon2.rs#L60-L80
        blowup_factor = 2
        rho = 1 / blowup_factor
        grinding_query_phase=16

        # All chip traces in the RISC-V prover are constrained by the shape configuration.
        # Reference: https://github.com/brevis-network/pico/blob/f84173e7d7200201a582cf38ad9b7c4bff63fdf4/vm/src/instances/compiler/shapes/riscv_shape.rs#L909-L923
        trace_length = 1 << 22

        # Reference: https://github.com/brevis-network/pico/blob/98550581dc43e3eec286cb0a8f061e88fb970f2a/vm/src/machine/prover.rs#L461-L472
        # These numbers are from a common CPU chunk.
        # Other Pico chunks may have different trace widths and polynomial counts.
        num_columns = 1278
        num_polys = 1435

        # Reference: https://github.com/brevis-network/pico/blob/f84173e7d7200201a582cf38ad9b7c4bff63fdf4/vm/src/configs/stark_config/kb_poseidon2.rs#L60-L80
        num_queries = 84

        #   Each chip exposes `log_quotient_degree`:
        #   At proof time we do:
        #       log_quotient_degrees = [chip.get_log_quotient_degree() for chip in chips]
        #       quotient_degrees     = [1 << d for d in log_quotient_degrees]
        #       max_q_deg            = max(quotient_degrees)
        #       air_max_degree_upper_bound = max_q_deg + 1    # upper bound on AIR constraint degree
        # Reference: https://github.com/brevis-network/pico/blob/f84173e7d7200201a582cf38ad9b7c4bff63fdf4/vm/src/machine/utils.rs#L357-L377
        AIR_max_degree = 3

        # Reference: https://github.com/brevis-network/Plonky3/blob/411a80deafb89335b5571f9925d584d7f51317e9/fri/src/two_adic_pcs.rs#L78-L82
        FRI_folding_factor = 2

        # Reference: https://github.com/brevis-network/Plonky3/blob/411a80deafb89335b5571f9925d584d7f51317e9/fri/src/verifier.rs#L54
        # In Plonky3, `log_max_height = proof.commit_phase_commits.len() + config.log_blowup`.
        # This means FRI folds until the domain height is 2^{log_blowup}, when the polynomial is constant.
        FRI_early_stop_degree = 1

        # Pico chips only use the local row and the next row in any constraint.
        max_combo = 2

        # Reference: https://github.com/brevis-network/pico/blob/main/vm/src/configs/stark_config/kb_poseidon2.rs
        # Poseidon2 hash output: 8 KoalaBear field elements (31 bits each) = 248 bits
        hash_size_bits = 248

        cfg = zkEVMConfig(
            name="Pico",
            hash_size_bits=hash_size_bits,
            rho=rho,
            trace_length=trace_length,
            field=field,
            num_columns=num_columns,
            num_polys=num_polys,
            power_batching=True,
            num_queries=num_queries,
            AIR_max_degree=AIR_max_degree,
            FRI_folding_factor=FRI_folding_factor,
            FRI_early_stop_degree=FRI_early_stop_degree,
            max_combo=max_combo,
            # POW
            grinding_query_phase=grinding_query_phase,
        )
        return zkEVMParams(cfg)
