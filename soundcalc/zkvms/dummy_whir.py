from __future__ import annotations

from soundcalc.zkvms.whir_based_vm import WHIRBasedCircuit, WHIRBasedVM, WHIRBasedVMConfig


from ..common.fields import *


class DummyWHIRPreset:
    @staticmethod
    def default() -> WHIRBasedVM:
        """
        A dummy zkVM using WHIR for testing WHIR
        """
        return WHIRBasedVM(
            name="DummyWHIR",
            circuits=[DummyWHIRPreset._main_circuit()]
        )

    @staticmethod
    def _main_circuit() -> WHIRBasedCircuit:

        name = "main"
        hash_size_bits = 256
        log_inv_rate = 1 # rate 1/2
        num_iterations = 5
        folding_factor = 4
        field = GOLDILOCKS_2
        log_degree = 23
        batch_size = 100
        power_batching = True
        constraint_degree = 1
        num_queries = [80,35,22,12,9]
        num_ood_samples = [2,2,2,2]

        # grinding
        grinding_bits_batching = 10
        grinding_bits_folding = [[10,10,10,10], [10,10,10,10], [10,10,10,10], [10,10,10,10], [10,10,10,10]]
        grinding_bits_queries = [0,0,0,12,20]
        grinding_bits_ood = [0,0,0,0]


        cfg = WHIRBasedVMConfig(
            name=name,
            hash_size_bits=hash_size_bits,
            log_inv_rate=log_inv_rate,
            num_iterations=num_iterations,
            folding_factor=folding_factor,
            field=field,
            log_degree=log_degree,
            batch_size=batch_size,
            power_batching=power_batching,
            grinding_bits_batching=grinding_bits_batching,
            grinding_bits_folding=grinding_bits_folding,
            constraint_degree=constraint_degree,
            num_queries=num_queries,
            grinding_bits_queries=grinding_bits_queries,
            num_ood_samples=num_ood_samples,
            grinding_bits_ood=grinding_bits_ood
        )
        return WHIRBasedCircuit(cfg)
