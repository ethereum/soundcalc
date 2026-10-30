#!/usr/bin/env bash
# Regenerates zisk.toml by extracting circuit parameters from ZisK's codebase proving key.
#
# Requires Rust (https://rustup.rs) and pil2-proofman's build dependencies:
#   Linux (apt-get): protobuf-compiler build-essential libbenchmark-dev libomp-dev libgmp-dev
#                    nlohmann-json3-dev nasm libsodium-dev cmake openmpi-bin openmpi-common
#                    libopenmpi-dev wget git
#   macOS (brew):    protobuf libomp gmp nlohmann-json nasm libsodium cmake open-mpi wget git
#
# Optional environment variables:
#   PIL2_PROOFMAN_DIR  use this local pil2-proofman checkout instead of cloning it
#   PROVING_KEY_DIR    use this proving key instead of downloading it
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
ZISK_SETUP="$SCRIPT_DIR/zisk-setup"

cleanup() {
    echo "=== Performing cleanup ==="
    rm -rf "$ZISK_SETUP"
}

trap cleanup EXIT

echo "=== 1. Check Rust is installed ==="
if ! command -v cargo &> /dev/null; then
    echo "Error: Cargo not found. Please install Rust first: https://rustup.rs"
    exit 1
fi
cargo --version

mkdir -p "$ZISK_SETUP"

echo "=== 2. Download ZisK proving key ==="
if [[ -n "${PROVING_KEY_DIR:-}" ]]; then
    echo "Using proving key at $PROVING_KEY_DIR"
else
    wget https://storage.googleapis.com/zisk-setup/zisk-provingkey-1.4.0-alpha.tar.gz -O "$ZISK_SETUP/zisk-provingkey.tar.gz"
    tar -xzf "$ZISK_SETUP/zisk-provingkey.tar.gz" -C "$ZISK_SETUP"
    PROVING_KEY_DIR="$ZISK_SETUP/provingKey"
fi

echo "=== 3. Clone pil2-proofman ==="
if [[ -n "${PIL2_PROOFMAN_DIR:-}" ]]; then
    echo "Using pil2-proofman at $PIL2_PROOFMAN_DIR"
    PIL2_DIR="$PIL2_PROOFMAN_DIR"
else
    PIL2_DIR="$ZISK_SETUP/pil2-proofman"
    git clone --depth 1 --branch v1.4.0-alpha https://github.com/0xPolygonHermez/pil2-proofman.git "$PIL2_DIR"
fi

echo "=== 4. Generate ZisK TOML ==="
cargo run --manifest-path "$PIL2_DIR/Cargo.toml" --bin proofman-cli soundness -k "$PROVING_KEY_DIR" -a -o "$SCRIPT_DIR/zisk.toml"

echo "=== 5. Calculate soundness info ==="
cd "$REPO_ROOT"
python3 -m soundcalc

echo "=== DONE ==="
echo "Generated TOML: $SCRIPT_DIR/zisk.toml"
