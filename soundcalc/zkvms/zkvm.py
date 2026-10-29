from __future__ import annotations

from pathlib import Path

import toml

from soundcalc.circuits.circuit import Circuit
from soundcalc.circuits.deep_ali import DeepAliCircuit, DeepAliConfig
from soundcalc.circuits.jagged import JaggedCircuit, JaggedCircuitConfig
from soundcalc.circuits.swirl import (
    SWIRLCircuit,
    SWIRLCircuitConfig,
    SWIRLLogUpSecurityParameters,
    build_swirl_system_params,
)
from soundcalc.common.fields import FieldParams, parse_field
from soundcalc.lookups.logup import LogUp, LogUpConfig, LogUpType
from soundcalc.pcs.fri import FRI, FRIConfig
from soundcalc.pcs.stir import STIR, STIRConfig
from soundcalc.pcs.whir import WHIR, WHIRConfig


def _parse_lookups_from_toml(section: dict, field: FieldParams) -> list[LogUp]:
    """Parse lookups from a circuit section in the TOML config."""
    lookups = []
    for lookup_section in section.get("lookups", []):
        logup_type_str = lookup_section.get("logup_type", "univariate")
        logup_type = LogUpType(logup_type_str)
        lookup_config = LogUpConfig(
            name=lookup_section["name"],
            field=field,
            logup_type=logup_type,
            rows_L=lookup_section["rows_L"],
            rows_T=lookup_section["rows_T"],
            num_columns_S=lookup_section.get("num_columns_S", 1),
            num_lookups_M=lookup_section.get("num_lookups_M", 1),
            grinding_bits_lookup=lookup_section.get("grinding_bits_lookup", 0),
            multilinear_fingerprint=lookup_section.get("multilinear_fingerprint"),
            reduction_error=lookup_section.get("reduction_error", 0.0),
        )
        lookups.append(LogUp(lookup_config))
    return lookups


class zkVM:
    """
    A class modeling a zkVM, which contains one or more circuits.
    """

    def __init__(self, name: str, circuits: list[Circuit], version: str | None = None):
        self._name = name
        self._circuits = circuits
        self.version = version

    def get_name(self) -> str:
        """Returns the name of the zkVM."""
        return self._name

    def get_circuits(self) -> list[Circuit]:
        """Returns the list of circuits in this zkVM."""
        return self._circuits

    @classmethod
    def load_from_toml(cls, toml_path: Path) -> "zkVM":
        """
        Load a VM from a TOML configuration file.

        Each circuit section is built according to its protocol_family, so a
        single VM can combine circuits from different families.
        """
        with open(toml_path, "r") as f:
            config = toml.load(f)

        circuits = [
            cls._build_circuit_from_section(config, section)
            for section in config.get("circuits", [])
        ]
        return cls(config["zkevm"]["name"], circuits=circuits,
                   version=config["zkevm"].get("version"))

    @staticmethod
    def _hash_size_bits(config: dict, section: dict) -> int:
        return section.get("hash_size_bits", config["zkevm"]["hash_size_bits"])

    @staticmethod
    def _field(config: dict, section: dict) -> FieldParams:
        return parse_field(section.get("field", config["zkevm"]["field"]))

    @classmethod
    def _build_fri_circuit_from_section(cls, config: dict, section: dict) -> DeepAliCircuit:
        field = cls._field(config, section)
        pcs = FRI(FRIConfig(
            hash_size_bits=cls._hash_size_bits(config, section),
            rho=section["rho"],
            gap_to_radius=section.get("gap_to_radius"),
            trace_length=section["trace_length"],
            field=field,
            batch_size=section["batch_size"],
            power_batching=section["power_batching"],
            multilinear_batching=section.get("multilinear_batching", False),
            num_queries=section["num_queries"],
            FRI_folding_factors=section.get("fri_folding_factors"),
            FRI_early_stop_degree=section.get("fri_early_stop_degree"),
            grinding_query_phase=section.get("grinding_query_phase", 0),
            grinding_commit_phase=section.get("grinding_commit_phase", 0),
            grinding_batching_phase=section.get("grinding_batching_phase", 0),
            initial_tree_widths=section.get("initial_tree_widths"),
            num_evals=section.get("num_evals", 0),
        ))
        lookups = _parse_lookups_from_toml(section, field)
        return DeepAliCircuit(DeepAliConfig(
            name=section["name"],
            pcs=pcs,
            field=field,
            gap_to_radius=section.get("gap_to_radius"),
            num_constraints=section["num_constraints"],
            AIR_max_degree=section["air_max_degree"],
            max_combo=section["opening_points"],
            lookups=lookups if lookups else None,
            grinding_deep=section.get("grinding_deep", 0),
            explicit_regime=section.get("explicit_regime"),
        ))

    @classmethod
    def _build_whir_circuit_from_section(cls, config: dict, section: dict) -> DeepAliCircuit:
        field = cls._field(config, section)
        pcs = WHIR(WHIRConfig(
            hash_size_bits=cls._hash_size_bits(config, section),
            log_inv_rate=section["log_inv_rate"],
            num_iterations=section["num_iterations"],
            folding_factors=section["folding_factors"],
            field=field,
            log_degree=section["log_degree"],
            batch_size=section["batch_size"],
            power_batching=section["power_batching"],
            grinding_batching_phase=section["grinding_batching_phase"],
            constraint_degree=section["constraint_degree"],
            grinding_bits_folding=section["grinding_bits_folding"],
            num_queries=section["num_queries"],
            grinding_bits_queries=section["grinding_bits_queries"],
            num_ood_samples=section["num_ood_samples"],
            grinding_bits_ood=section["grinding_bits_ood"],
        ))
        lookups = _parse_lookups_from_toml(section, field)
        return DeepAliCircuit(DeepAliConfig(
            name=section["name"],
            pcs=pcs,
            field=field,
            gap_to_radius=section.get("gap_to_radius"),
            num_constraints=section["num_constraints"],
            AIR_max_degree=section["air_max_degree"],
            max_combo=section["opening_points"],
            lookups=lookups if lookups else None,
            explicit_regime=section.get("explicit_regime"),
        ))

    @classmethod
    def _build_stir_circuit_from_section(cls, config: dict, section: dict) -> DeepAliCircuit:
        field = cls._field(config, section)
        pcs = STIR(STIRConfig(
            hash_size_bits=cls._hash_size_bits(config, section),
            log_inv_rate=section["log_inv_rate"],
            num_iterations=section["num_iterations"],
            folding_factors=section["folding_factors"],
            field=field,
            log_degree=section["log_degree"],
            batch_size=section["batch_size"],
            power_batching=section["power_batching"],
            grinding_batching_phase=section["grinding_batching_phase"],
            grinding_bits_folding=section["grinding_bits_folding"],
            num_queries=section["num_queries"],
            grinding_bits_queries=section["grinding_bits_queries"],
            num_ood_samples=section["num_ood_samples"],
            grinding_bits_ood=section["grinding_bits_ood"],
            gap_to_radius=section.get("gap_to_radius"),
            initial_tree_widths=section.get("initial_tree_widths"),
            num_evals=section.get("num_evals", 0),
        ))
        lookups = _parse_lookups_from_toml(section, field)
        return DeepAliCircuit(DeepAliConfig(
            name=section["name"],
            pcs=pcs,
            field=field,
            gap_to_radius=section.get("gap_to_radius"),
            num_constraints=section["num_constraints"],
            AIR_max_degree=section["air_max_degree"],
            max_combo=section["opening_points"],
            lookups=lookups if lookups else None,
            explicit_regime=section.get("explicit_regime"),
        ))

    @classmethod
    def _build_jagged_circuit_from_section(cls, config: dict, section: dict) -> JaggedCircuit:
        field = cls._field(config, section)
        explicit_regime = section.get("explicit_regime")
        explicit_m = section.get("explicit_m") if explicit_regime == "list" else None
        # The dense PCS under the jagged reduction: FRI (Basefold) by default,
        # WHIR when the config asks for it.
        dense_pcs_kind = section.get("dense_pcs", "fri").lower()
        if dense_pcs_kind == "fri":
            dense_pcs = FRI(FRIConfig(
                hash_size_bits=cls._hash_size_bits(config, section),
                rho=section["rho"],
                gap_to_radius=section.get("gap_to_radius"),
                trace_length=section["dense_length"],
                field=field,
                batch_size=section["dense_batch"],
                power_batching=section["power_batching"],
                multilinear_batching=section.get("multilinear_batching", False),
                num_queries=section["num_queries"],
                FRI_folding_factors=section.get("fri_folding_factors"),
                FRI_early_stop_degree=section.get("fri_early_stop_degree"),
                grinding_batching_phase=section.get("grinding_batching_phase", 0),
                grinding_query_phase=section.get("grinding_query_phase", 0),
            ))
        elif dense_pcs_kind == "whir":
            # WHIR batches with one challenge (powers) or independent
            # coefficients; it has no multilinear batching, so a config that
            # asks for one would be modelled as something else.  Refuse it
            # rather than let the key be read as accepted.
            if section.get("multilinear_batching", False):
                raise ValueError(
                    f"circuit {section['name']!r}: multilinear_batching is not a WHIR "
                    "batching law; set power_batching instead"
                )
            dense_pcs = WHIR(WHIRConfig(
                hash_size_bits=cls._hash_size_bits(config, section),
                log_inv_rate=section["log_inv_rate"],
                log_inv_rates=section.get("whir_log_inv_rates"),
                num_iterations=section["num_iterations"],
                folding_factors=section["folding_factors"],
                field=field,
                log_degree=section["log_degree"],
                batch_size=section["dense_batch"],
                power_batching=section["power_batching"],
                grinding_batching_phase=section.get("grinding_batching_phase", 0),
                constraint_degree=section["constraint_degree"],
                grinding_bits_folding=section["grinding_bits_folding"],
                num_queries=section["num_queries"],
                grinding_bits_queries=section["grinding_bits_queries"],
                num_ood_samples=section["num_ood_samples"],
                grinding_bits_ood=section["grinding_bits_ood"],
            ))
        else:
            raise ValueError(
                f"Unknown dense_pcs {dense_pcs_kind!r} for a JAGGED circuit (expected 'fri' or 'whir')"
            )
        lookups = _parse_lookups_from_toml(section, field)
        return JaggedCircuit(JaggedCircuitConfig(
            name=section["name"],
            dense_pcs=dense_pcs,
            field=field,
            trace_length=section["trace_length"],
            trace_width=section["trace_columns"],
            num_constraints=section["num_constraints"],
            AIR_max_degree=section["air_max_degree"],
            lookups=lookups if lookups else None,
            explicit_regime=explicit_regime,
            explicit_m=explicit_m,
        ))

    @classmethod
    def _build_swirl_circuit_from_section(cls, config: dict, section: dict) -> SWIRLCircuit:
        field = cls._field(config, section)
        swirl_config = config["swirl"]

        explicit_regime = section["explicit_regime"]
        explicit_m = section.get("explicit_m") if explicit_regime == "list" else None
        logup = SWIRLLogUpSecurityParameters(
            max_interaction_count=swirl_config["logup_max_interaction_count"],
            log_max_message_length=swirl_config["logup_log_max_message_length"],
            pow_bits=section.get("logup_pow_bits", swirl_config["logup_pow_bits"]),
        )

        params = build_swirl_system_params(
            l_skip=section["l_skip"],
            n_stack=section["n_stack"],
            w_stack=section["w_stack"],
            log_blowup=section["log_blowup"],
            folding_pow_bits=section["whir_folding_pow_bits"],
            mu_pow_bits=section["whir_mu_pow_bits"],
            explicit_regime=explicit_regime,
            explicit_m=explicit_m,
            num_queries=section["whir_num_queries"],
            logup=logup,
            max_constraint_degree=section["constraint_degree"],
        )
        whir = WHIR(WHIRConfig(
            hash_size_bits=cls._hash_size_bits(config, section),
            log_inv_rate=params.log_blowup,
            num_iterations=len(params.whir.rounds),
            folding_factors=[params.whir.k] * len(params.whir.rounds),
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
        return SWIRLCircuit(SWIRLCircuitConfig(
            name=section["name"],
            pcs=whir,
            field=field,
            params=params,
            max_num_constraints_per_air=section["max_constraints_per_air"],
            num_airs=section["num_airs"],
            max_log_trace_height=section["max_log_trace_height"],
            num_trace_columns=section["num_trace_columns"],
            max_interactions_per_air=section["max_interactions_per_air"],
            soundness_max_num_constraints_per_air=section.get(
                "soundness_max_constraints_per_air",
                section["max_constraints_per_air"],
            ),
            soundness_num_airs=section.get("soundness_num_airs", section["num_airs"]),
            soundness_max_log_trace_height=section.get(
                "soundness_max_log_trace_height",
                section["max_log_trace_height"],
            ),
            soundness_num_trace_columns=section.get(
                "soundness_num_trace_columns",
                section["num_trace_columns"],
            ),
            soundness_max_interactions_per_air=section.get(
                "soundness_max_interactions_per_air",
                section["max_interactions_per_air"],
            ),
            proof_size_num_airs=section.get(
                "proof_size_num_airs",
                section.get("soundness_num_airs", section["num_airs"]),
            ),
            proof_size_max_log_trace_height=section.get(
                "proof_size_max_log_trace_height",
                section.get(
                    "soundness_max_log_trace_height",
                    section["max_log_trace_height"],
                ),
            ),
            proof_size_num_trace_columns=section.get(
                "proof_size_num_trace_columns",
                section.get("soundness_num_trace_columns", section["num_trace_columns"]),
            ),
            proof_size_max_interactions_per_air=section.get(
                "proof_size_max_interactions_per_air",
                section.get(
                    "soundness_max_interactions_per_air",
                    section["max_interactions_per_air"],
                ),
            ),
            proof_size_num_public_values=section.get("proof_size_num_public_values", 0),
        ))

    @classmethod
    def _build_circuit_from_section(cls, config: dict, section: dict) -> Circuit:
        protocol_family = section["protocol_family"]
        if protocol_family == "FRI_STARK":
            return cls._build_fri_circuit_from_section(config, section)
        if protocol_family == "WHIR":
            return cls._build_whir_circuit_from_section(config, section)
        if protocol_family == "STIR":
            return cls._build_stir_circuit_from_section(config, section)
        if protocol_family == "JAGGED":
            return cls._build_jagged_circuit_from_section(config, section)
        if protocol_family == "SWIRL":
            return cls._build_swirl_circuit_from_section(config, section)
        raise ValueError(f"Unknown circuit protocol_family: {protocol_family}")
