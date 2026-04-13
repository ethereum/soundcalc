from __future__ import annotations

from pathlib import Path

import toml

from soundcalc.common.fields import parse_field
from soundcalc.custom.swirl import (
    SWIRLCircuit,
    SWIRLCircuitConfig,
    SWIRLLogUpSecurityParameters,
    SWIRLWhirProximityMode,
    build_swirl_system_params,
)
from soundcalc.pcs.whir import WHIR, WHIRConfig
from soundcalc.zkvms.zkvm import zkVM


def load() -> zkVM:
    with open(Path(__file__).parent / "openvm2.toml", "r") as f:
        config = toml.load(f)

    field = parse_field(config["zkevm"]["field"])
    hash_size_bits = config["zkevm"]["hash_size_bits"]
    logup = SWIRLLogUpSecurityParameters(
        max_interaction_count=config["swirl"]["logup_max_interaction_count"],
        log_max_message_length=config["swirl"]["logup_log_max_message_length"],
        pow_bits=config["swirl"]["logup_pow_bits"],
    )

    circuits = []
    for section in config.get("circuits", []):
        if section["whir_proximity"] == "unique":
            proximity = SWIRLWhirProximityMode(kind="unique")
        else:
            proximity = SWIRLWhirProximityMode(kind="list", m=section["whir_m"])

        params = build_swirl_system_params(
            l_skip=section["l_skip"],
            n_stack=section["n_stack"],
            w_stack=section["w_stack"],
            log_blowup=section["log_blowup"],
            folding_pow_bits=section["whir_folding_pow_bits"],
            mu_pow_bits=section["whir_mu_pow_bits"],
            proximity=proximity,
            logup=logup,
        )
        whir = WHIR(WHIRConfig(
            hash_size_bits=hash_size_bits,
            log_inv_rate=params.log_blowup,
            num_iterations=len(params.whir.rounds),
            folding_factor=params.whir.k,
            field=field,
            log_degree=params.log_stacked_height(),
            batch_size=params.w_stack,
            power_batching=True,
            grinding_batching_phase=params.whir.mu_pow_bits,
            constraint_degree=section["constraint_degree"],
            grinding_bits_folding=[
                [params.whir.folding_pow_bits] * params.whir.k
                for _ in params.whir.rounds
            ],
            num_queries=[round_config.num_queries for round_config in params.whir.rounds],
            grinding_bits_queries=[params.whir.query_phase_pow_bits] * len(params.whir.rounds),
            num_ood_samples=[1] * max(len(params.whir.rounds) - 1, 0),
            grinding_bits_ood=[0] * max(len(params.whir.rounds) - 1, 0),
        ))
        circuits.append(SWIRLCircuit(SWIRLCircuitConfig(
            name=section["name"],
            pcs=whir,
            field=field,
            params=params,
            max_num_constraints_per_air=section["max_constraints_per_air"],
            num_airs=section["num_airs"],
            max_log_trace_height=section["max_log_trace_height"],
            num_trace_columns=section["num_trace_columns"],
            max_interactions_per_air=section["max_interactions_per_air"],
        )))

    return zkVM(config["zkevm"]["name"], circuits=circuits, version=config["zkevm"].get("version"))
