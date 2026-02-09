from __future__ import annotations

from pathlib import Path

import toml

from soundcalc.common.fields import FieldParams, parse_field
from soundcalc.lookups.logup import LogUp, LogUpConfig, LogUpType
from soundcalc.pcs.fri import FRI, FRIConfig
from soundcalc.pcs.pcs import PCS
from soundcalc.pcs.jagged import JaggedPCS, JaggedConfig
from soundcalc.pcs.whir import WHIR, WHIRConfig
from soundcalc.zkvms.circuit import Circuit, CircuitConfig


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
            alphabet_size_H=lookup_section.get("alphabet_size_H"),
            grinding_bits_lookup=lookup_section.get("grinding_bits_lookup", 0),
            cross_table_lookup=lookup_section.get("cross_table_lookup", False),
            multilinear_fingerprint=lookup_section.get("multilinear_fingerprint", False),
            reduction_error=lookup_section.get("reduction_error", 0.0),
        )
        lookups.append(LogUp(lookup_config))
    return lookups


class zkVM:
    """
    A class modeling a zkVM, which contains one or more circuits.
    """

    def __init__(self, name: str, circuits: list[Circuit]):
        self._name = name
        self._circuits = circuits

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
        Uses the protocol_family field to determine which loader to use.
        """
        with open(toml_path, "r") as f:
            config = toml.load(f)

        protocol_family = config["zkevm"]["protocol_family"]
        if protocol_family == "FRI_STARK":
            return cls._load_fri_from_toml(config)
        elif protocol_family == "WHIR":
            return cls._load_whir_from_toml(config)
        elif protocol_family == "JAGGED":
            return cls._load_jagged_from_toml(config)
        else:
            raise ValueError(f"Unknown protocol_family: {protocol_family}")

    @classmethod
    def _load_fri_from_toml(cls, config: dict) -> "zkVM":
        """
        Load a FRI-based VM from a parsed TOML config dict.
        """
        field = parse_field(config["zkevm"]["field"])
        circuits = []

        for section in config.get("circuits", []):
            pcs = FRI(FRIConfig(
                hash_size_bits=config["zkevm"]["hash_size_bits"],
                rho=section["rho"],
                gap_to_radius=section.get("gap_to_radius"),
                trace_length=section["trace_length"],
                field=field,
                batch_size=section["batch_size"],
                power_batching=section["power_batching"],
                multilinear_batching=section.get("multilinear_batching", 0),
                num_queries=section["num_queries"],
                FRI_folding_factors=section.get("fri_folding_factors"),
                FRI_early_stop_degree=section.get("fri_early_stop_degree"),
                grinding_query_phase=section.get("grinding_query_phase", 0),
                grinding_commit_phase=section.get("grinding_commit_phase", 0),
            ))
            lookups = _parse_lookups_from_toml(section, field)
            circuit = Circuit(CircuitConfig(
                name=section["name"],
                pcs=pcs,
                field=field,
                gap_to_radius=section.get("gap_to_radius"),
                num_constraints=section["num_constraints"],
                AIR_max_degree=section["air_max_degree"],
                max_combo=section["opening_points"],
                lookups=lookups if lookups else None,
                grinding_deep=section.get("grinding_deep", 0),
                multilinear_zerocheck = section.get("multilinear_zerocheck", False),
                udr_only = section.get("udr_only", False),
            ))
            circuits.append(circuit)

        return cls(config["zkevm"]["name"], circuits=circuits)

    @classmethod
    def _load_whir_from_toml(cls, config: dict) -> "zkVM":
        """
        Load a WHIR-based VM from a parsed TOML config dict.
        """
        field = parse_field(config["zkevm"]["field"])
        circuits = []

        for section in config.get("circuits", []):
            pcs = WHIR(WHIRConfig(
                hash_size_bits=config["zkevm"]["hash_size_bits"],
                log_inv_rate=section["log_inv_rate"],
                num_iterations=section["num_iterations"],
                folding_factor=section["folding_factor"],
                field=field,
                gap_to_radius=section.get("gap_to_radius"),
                log_degree=section["log_degree"],
                batch_size=section["batch_size"],
                power_batching=section["power_batching"],
                grinding_bits_batching=section["grinding_bits_batching"],
                constraint_degree=section["constraint_degree"],
                grinding_bits_folding=section["grinding_bits_folding"],
                num_queries=section["num_queries"],
                grinding_bits_queries=section["grinding_bits_queries"],
                num_ood_samples=section["num_ood_samples"],
                grinding_bits_ood=section["grinding_bits_ood"],
            ))
            lookups = _parse_lookups_from_toml(section, field)
            circuit = Circuit(CircuitConfig(
                name=section["name"],
                pcs=pcs,
                field=field,
                gap_to_radius=section.get("gap_to_radius"),
                multilinear_zerocheck = section.get("multilinear_zerocheck", False),
                udr_only = section.get("udr_only", False),
                lookups=lookups if lookups else None,
            ))
            circuits.append(circuit)

        return cls(config["zkevm"]["name"], circuits=circuits)
    
    @classmethod
    def _load_jagged_from_toml(cls, config: dict) -> "zkVM":
        """
        Load a Jagged PCS-based VM from a parsed TOML config dict.
        """
        field = parse_field(config["zkevm"]["field"])
        circuits = []

        for section in config.get("circuits", []):
            dense_pcs = FRI(FRIConfig(
                hash_size_bits=config["zkevm"]["hash_size_bits"],
                rho=section["rho"],
                gap_to_radius=section.get("gap_to_radius"),
                trace_length=section["dense_length"],
                field=field,
                batch_size=section["dense_batch"],
                power_batching=section["power_batching"],
                multilinear_batching=section.get("multilinear_batching", 0),
                num_queries=section["num_queries"],
                FRI_folding_factors=section.get("fri_folding_factors"),
                FRI_early_stop_degree=section.get("fri_early_stop_degree"),
                grinding_query_phase=section.get("grinding_query_phase", 0),
            ))
            pcs = JaggedPCS(JaggedConfig(
                dense_pcs = dense_pcs,
                trace_height = section["trace_length"], 
                trace_width = section["trace_columns"],
            ))
            lookups = _parse_lookups_from_toml(section, field)
            circuit = Circuit(CircuitConfig(
                name=section["name"],
                pcs=pcs,
                field=field,
                gap_to_radius=section.get("gap_to_radius"),
                num_constraints=section["num_constraints"],
                AIR_max_degree=section["air_max_degree"],
                max_combo=section["opening_points"],
                multilinear_zerocheck = section.get("multilinear_zerocheck", False),
                udr_only = section.get("udr_only", False),
                lookups=lookups if lookups else None,
            ))
            circuits.append(circuit)

        return cls(config["zkevm"]["name"], circuits=circuits)
