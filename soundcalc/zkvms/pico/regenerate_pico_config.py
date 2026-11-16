#!/usr/bin/env python3
"""Regenerates pico.toml from Pico's soundness manifest.

Pico writes `mle-core/tests/soundness_manifest.json` from a keygen of its production circuits
(`cargo run --release -p pico-vm --example mle_soundness_manifest`); its CI checks the file
against the code. This script reads it at the commit `PICO_COMMIT`, checks that the circuits
there are tag v3.1.1's, scores the configuration with soundcalc against the manifest, and only
then writes pico.toml. Regenerate the reports afterwards with `python3 -m soundcalc`.

Usage, from the repository root:
    python3 soundcalc/zkvms/pico/regenerate_pico_config.py [--pico-dir PATH]

`--pico-dir` reads both manifests from a local Pico checkout (`git show`) instead of GitHub.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

PICO_REPO = "brevis-network/pico"
# The commit the configuration is generated from: v3.1.1's circuits, with the manifest's
# proof-shape records.
PICO_COMMIT = "150f90c2b6eb2e2f2e556834f4928d99903c91f8"
# Tag v3.1.1.
PICO_V311 = "2acc7c1828fb4ec1bed5963511bb370870c5b608"
MANIFEST = "mle-core/tests/soundness_manifest.json"
OUT = Path(__file__).parent / "pico.toml"

# The circuits in soundcalc's order: the last one is the final proof.
ORDER = ["riscv", "convert", "combine", "deferred", "embed", "compress"]
ROLES = {
    "riscv": "proves one chunk of the RISC-V execution",
    "convert": "verifies one RISCV proof",
    "combine": (
        "verifies one or two CONVERT or COMBINE proofs and joins their execution, down to one root"
    ),
    "deferred": (
        "verifies the root proof of a program whose proof the guest verifies"
        " (a COMBINE-family circuit)"
    ),
    "embed": (
        "re-proves the COMPRESS proof under a BN254 Poseidon2 transcript,"
        " for the on-chain path (WRAP, Groth16)"
    ),
    "compress": "re-proves the complete root at code rate 1/16 with list decoding: the final proof",
}
# Terms on which Pico's calculator is more conservative, by exactly this many bits.
ANALYSIS_GAPS = {
    "gkr_sumcheck": math.log2(4 / 3),  # 4 events per sub-round instead of 3
    "gkr_batching": 1.0,  # 2 events per round instead of 1
}
# Terms on which Pico's calculator takes the worst case its keys admit, and soundcalc the
# whitelist's shapes, so soundcalc scores them at least as high.
SHAPE_TERMS = {
    # Pico takes the GKR depth at 0; every whitelist-mode proof's GKR is at least as deep as its
    # tallest trace, which soundcalc's n_logup bound is too, so no extra rounds are charged.
    "constraint_batching",
    # The columns of the widest shape instead of all the key's columns.
    "stacked_reduction",
    # The widest shape's stacked width instead of the preset's.
    "whir_mu_batching",
}
# soundcalc's level names -> the manifest's component names.
COMPONENTS = {
    "logup": ("soundness", "logup_bits"),
    "gkr_sumcheck": ("soundness", "gkr_sumcheck_bits"),
    "gkr_batching": ("soundness", "gkr_batching_bits"),
    "zerocheck_sumcheck": ("soundness", "zerocheck_sumcheck_bits"),
    "constraint_batching": ("soundness", "constraint_batching_bits"),
    "stacked_reduction": ("soundness", "stacked_reduction_bits"),
    "whir": ("soundness", "whir_bits"),
    "total": ("soundness", "total_bits"),
    "whir_mu_batching": ("whir_details", "mu_batching_bits"),
    "whir_fold_rbr": ("whir_details", "fold_rbr_bits"),
    "whir_proximity_gaps": ("whir_details", "proximity_gaps_bits"),
    "whir_sumcheck": ("whir_details", "sumcheck_bits"),
    "whir_ood_rbr": ("whir_details", "ood_rbr_bits"),
    "whir_shift_rbr": ("whir_details", "shift_rbr_bits"),
    "whir_query": ("whir_details", "query_bits"),
    "whir_gamma_batching": ("whir_details", "gamma_batching_bits"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def fetch(commit: str, pico_dir: str | None) -> dict:
    if pico_dir:
        text = subprocess.run(
            ["git", "-C", pico_dir, "show", f"{commit}:{MANIFEST}"],
            check=True, capture_output=True, text=True,
        ).stdout
    else:
        url = f"https://raw.githubusercontent.com/{PICO_REPO}/{commit}/{MANIFEST}"
        with urllib.request.urlopen(url) as response:
            text = response.read().decode()
    return json.loads(text)


def check_v311(manifest: dict, v311: dict) -> None:
    """Everything but the commit and the added proof-shape records is v3.1.1's: the keys, their
    shapes, params and scores, the whitelist root."""
    require(manifest["dirty"] is False, "the manifest was generated from a dirty tree")
    require(manifest["calculator"] == "closed-form", f"calculator {manifest['calculator']}")
    require(not manifest["not_generated"], f"not generated: {manifest['not_generated']}")
    strip = lambda m: {k: v for k, v in m.items() if k not in ("commit", "proof_shapes")}
    require(strip(manifest) == strip(v311), "the manifest's circuits are not v3.1.1's")


def whitelist_key(manifest: dict, machine: str) -> dict:
    keys = [k for k in manifest["keys"] if k["machine"] == machine and k["mode"] == "whitelist"]
    require(bool(keys), f"no whitelist-mode {machine} key")
    for k in keys[1:]:
        require(k["params"] == keys[0]["params"], f"{machine} keys disagree on params")
    return keys[0]


def absent_air_bytes(shape: dict) -> int:
    """The bytes Pico's encoding spends on absent AIRs, which the model, with one AIR count for
    present and absent AIRs alike, leaves out: their bits in the presence bitmap and their empty
    public-values vectors."""
    num_airs, present = shape["num_airs"], shape["num_airs_present"]
    return (math.ceil(num_airs / 8) - math.ceil(present / 8)) + 4 * (num_airs - present)


def toml_value(v) -> str:
    if isinstance(v, str):
        return json.dumps(v)
    if isinstance(v, list):
        return "[" + ", ".join(toml_value(x) for x in v) + "]"
    return str(v)


def circuit_section(machine: str, key: dict, shapes: dict) -> list[str]:
    p, mx, largest = key["params"], shapes["max"], shapes["largest"]
    shape = largest["shape"]
    whir = p["whir"]
    require(whir["k"] == 4 and whir["query_phase_pow_bits"] == 20, f"{machine} WHIR {whir}")
    # soundcalc's one `w_stack` serves the soundness bound and the size: the widest shape must be
    # the largest proof's.
    require(mx["stacked_width"] == sum(shape["stacking_widths"]), f"{machine} stacked width")
    fields = [
        ("protocol_family", "SWIRL"),
        ("name", machine),
        ("l_skip", p["l_skip"]),
        ("n_stack", p["n_stack"]),
        ("w_stack", mx["stacked_width"]),
        ("log_blowup", p["log_blowup"]),
        ("whir_folding_pow_bits", whir["folding_pow_bits"]),
        ("whir_mu_pow_bits", whir["mu_pow_bits"]),
    ]
    if whir["proximity"] == "UniqueDecoding":
        fields.append(("explicit_regime", "unique"))
    else:
        m = whir["proximity"]["ListDecoding"]["m"]
        fields += [("explicit_regime", "list"), ("explicit_m", m)]
    fields += [
        ("whir_num_queries", [r["num_queries"] for r in whir["rounds"]]),
        ("constraint_degree", p["max_constraint_degree"]),
        ("max_constraints_per_air", mx["max_constraints_per_air"]),
        ("num_airs", mx["num_airs_present"]),
        ("max_log_trace_height", mx["max_log_height"]),
        ("num_trace_columns", mx["num_trace_columns"]),
        ("max_interactions_per_air", mx["max_interactions_per_air"]),
        ("proof_size_num_airs", shape["num_airs_present"]),
        ("proof_size_max_log_trace_height", shape["max_log_height"]),
        ("proof_size_num_trace_columns", shape["num_trace_columns"]),
        ("proof_size_max_interactions_per_air", shape["max_interactions_per_air"]),
        ("proof_size_num_public_values", shape["num_public_values"]),
        ("proof_size_num_gkr_rounds", shape["num_gkr_rounds"]),
        ("proof_size_num_column_openings", shape["num_column_openings"]),
        ("proof_size_num_opening_parts", shape["num_opening_parts"]),
        ("proof_size_num_cached_commitments", shape["num_cached_commitments"]),
        ("proof_size_num_commitments", len(shape["stacking_widths"])),
    ]
    if shapes["shapes"] == 1:
        sizes = [f"# One whitelist-mode proof shape, of {largest['bytes']:,} bytes."]
    else:
        sizes = [f"# {shapes['shapes']:,} whitelist-mode proof shapes; the largest proof "
                 f"({largest['name']}) is {largest['bytes']:,} bytes."]
    absent = absent_air_bytes(shape)
    if absent:
        sizes.append(f"# The model gives it {absent} bytes less: the encoding's share of the "
                     f"{shape['num_airs'] - shape['num_airs_present']} absent AIRs.")
    lines = ["[[circuits]]", f"# {machine.upper()}: {ROLES[machine]}.", *sizes]
    lines += [f"{k} = {toml_value(v)}" for k, v in fields]
    return lines


def render(manifest: dict) -> str:
    keys = {m: whitelist_key(manifest, m) for m in ORDER}
    logup = {json.dumps(k["params"]["logup"], sort_keys=True) for k in keys.values()}
    require(len(logup) == 1, "the circuits disagree on the LogUp parameters")
    logup = keys["riscv"]["params"]["logup"]
    header = f"""# Pico v3.1.1
#
# Generated by soundcalc/zkvms/pico/regenerate_pico_config.py from Pico's soundness manifest
# (https://github.com/{PICO_REPO}/blob/{PICO_COMMIT}/{MANIFEST}),
# which Pico writes from a keygen of its production circuits and checks in CI. Do not edit;
# regenerate with
#   python3 soundcalc/zkvms/pico/regenerate_pico_config.py && python3 -m soundcalc
# The script checks that the manifest's keys, shapes, parameters and scores are those of tag
# v3.1.1 ({PICO_V311}).
# Since v3.1.1 Pico has added a pure-execution mode (brevis-network/pico#126) and the
# proof-shape records used below (brevis-network/pico#131); neither changes a key.
#
# Proof chain: RISCV -> CONVERT -> COMBINE -> COMPRESS -> EMBED -> WRAP / Groth16. DEFERRED, on the
# side, verifies the root proof of each program whose proof the guest verifies.
# COMPRESS is the final proof, through which Pico targets 128 bits. EMBED re-proves it under a
# BN254 transcript for the on-chain Groth16 step, which is held to BN254's security level; it is
# listed before COMPRESS because soundcalc takes the last circuit as the final proof.
#
# Shapes: recursion proofs are verified only under whitelisted keys, and each recursion circuit
# fixes, as constants of its key, which child AIRs are present and how tall they are. COMPRESS's
# own key fixes its shape: each of its AIRs is required and preprocessed, and the verifier holds a
# preprocessed trace's height to the key. Every proof in the chain therefore has one of finitely
# many shapes, COMPRESS and EMBED one each. The shape inputs of each circuit are the maxima over
# the shapes its whitelist-mode proofs take; the proof_size_* inputs are those of the largest of
# them, whose encoded size the model then gives exactly, except for the bytes the encoding spends
# on absent AIRs (riscv). Digests are encoded in 32 bytes: eight 32-bit KoalaBear words, or one
# BN254 element for EMBED.
#
# Soundness: the raw totals equal Pico's own calculator. On the same protocol Pico's calculator
# charges two terms more conservatively, neither of them binding: GKR sumcheck at 4 events per
# sub-round instead of 3 (0.415 bits lower) and GKR batching at 2 events per round instead of 1
# (1 bit lower). Three non-binding terms are higher here because they use the whitelist's shapes
# where Pico's calculator takes the worst case a key admits: constraint batching (Pico takes the
# GKR depth at 0; every whitelist-mode proof's GKR is at least as deep as its tallest trace),
# stacked reduction and WHIR mu batching (the widest shape's columns and stacked width).

[zkevm]
name = "Pico"
version = "3.1.1"
field = "KoalaBear^5"
hash_size_bits = 256

[swirl]
logup_max_interaction_count = {logup["max_interaction_count"]}
logup_log_max_message_length = {logup["log_max_message_length"]}
logup_pow_bits = {logup["pow_bits"]}
"""
    sections = ["\n".join(circuit_section(m, keys[m], manifest["proof_shapes"][m])) for m in ORDER]
    return header + "\n" + "\n\n".join(sections) + "\n"


def self_check(manifest: dict, path: Path) -> None:
    """Scores the configuration at `path` with soundcalc against the manifest."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from soundcalc.circuits.swirl.calculator import calculate_swirl_soundness
    from soundcalc.zkvms.zkvm import zkVM

    vm = zkVM.load_from_toml(path)
    names = [circuit.get_name() for circuit in vm.get_circuits()]
    require(names == ORDER, f"circuits {names}")
    for circuit in vm.get_circuits():
        machine = circuit.get_name()
        key = whitelist_key(manifest, machine)
        raw = calculate_swirl_soundness(
            params=circuit.params, field=circuit.field, whir=circuit.pcs,
            max_num_constraints_per_air=circuit.soundness_max_num_constraints_per_air,
            num_airs=circuit.soundness_num_airs,
            max_log_trace_height=circuit.soundness_max_log_trace_height,
            num_trace_columns=circuit.soundness_num_trace_columns,
            max_interactions_per_air=circuit.soundness_max_interactions_per_air,
        )
        for level, (group, name) in COMPONENTS.items():
            ours, theirs = raw[level], key[group][name]
            if level in ANALYSIS_GAPS:
                ok = abs(ours - theirs - ANALYSIS_GAPS[level]) <= 1e-9
            elif level in SHAPE_TERMS:
                ok = ours >= theirs - 1e-9
            else:
                ok = abs(ours - theirs) <= 1e-9
            require(ok, f"{machine} {level}: soundcalc {ours}, Pico {theirs}")
        largest = manifest["proof_shapes"][machine]["largest"]
        size = circuit.get_proof_size_bits() // 8
        require(size + absent_air_bytes(largest["shape"]) == largest["bytes"],
                f"{machine}: {size} bytes, encoded {largest['bytes']}")
        print(f"{machine:9s} {raw['total']:.4f} bits (Pico {key['soundness']['total_bits']:.4f}), "
              f"{size:,} bytes (encoded {largest['bytes']:,})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pico-dir", help="read the manifests from this Pico checkout")
    args = parser.parse_args()
    manifest = fetch(PICO_COMMIT, args.pico_dir)
    check_v311(manifest, fetch(PICO_V311, args.pico_dir))
    with tempfile.NamedTemporaryFile("w", suffix=".toml", dir=OUT.parent, delete=False) as tmp:
        tmp.write(render(manifest))
    try:
        self_check(manifest, Path(tmp.name))
        os.replace(tmp.name, OUT)
    finally:
        if os.path.exists(tmp.name):
            os.unlink(tmp.name)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
