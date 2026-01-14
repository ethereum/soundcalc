#!/usr/bin/env bash
# Regenerates zisk.toml by extracting circuit parameters from ZisK's codebase proving key.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cleanup() {
    echo "=== Performing cleanup ==="
    rm -rf "$SCRIPT_DIR/zisk-setup"
}

trap cleanup EXIT

echo "=== 1. Check Rust is installed ==="
if ! command -v cargo &> /dev/null || ! command -v rustup &> /dev/null; then
    echo "Error: Rust/Cargo/Rustup not found. Please install Rust first: https://rustup.rs"
    exit 1
fi
rustup default stable
rustc --version
cargo --version

echo "=== 2. Install dependencies ==="
# Detect OS and install dependencies accordingly
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - use Homebrew
    if ! command -v brew &> /dev/null; then
        echo "Error: Homebrew not found. Please install Homebrew first: https://brew.sh"
        exit 1
    fi
    echo "Detected macOS, using Homebrew..."
    brew install \
        python3 \
        protobuf \
        libomp \
        gmp \
        nlohmann-json \
        nasm \
        libsodium \
        cmake \
        open-mpi \
        wget \
        git
else
    # Linux - use apt-get
    echo "Detected Linux, using apt-get..."
    sudo apt-get update
    sudo apt-get install -y \
        python3 \
        python3-pip \
        protobuf-compiler \
        build-essential \
        libbenchmark-dev \
        libomp-dev \
        libgmp-dev \
        nlohmann-json3-dev \
        nasm \
        libsodium-dev \
        cmake \
        openmpi-bin \
        openmpi-common \
        libopenmpi-dev \
        wget \
        tar \
        git
fi

echo "=== 3. Download ZisK proving key ==="
ZISK_SETUP="$SCRIPT_DIR/zisk-setup"
mkdir -p "$ZISK_SETUP"
wget https://storage.googleapis.com/zisk-setup/zisk-provingkey-pre-0.15.0.tar.gz -O "$ZISK_SETUP/zisk-provingkey.tar.gz"
tar -xvzf "$ZISK_SETUP/zisk-provingkey.tar.gz" -C "$ZISK_SETUP"

echo "=== 4. Clone pil2-proofman ==="
PIL2_DIR="$ZISK_SETUP/pil2-proofman"
git clone https://github.com/0xPolygonHermez/pil2-proofman.git "$PIL2_DIR"

echo "=== 5. Generate ZisK TOML ==="
cargo run --manifest-path "$PIL2_DIR/Cargo.toml" --bin proofman-cli soundness -k "$ZISK_SETUP/provingKey" -a -o "$SCRIPT_DIR/zisk.toml"

echo "=== 6. Calculate soundness info ==="
python3 -m soundcalc --print-only ZisK

echo "=== DONE ==="
echo "Generated TOML: $SCRIPT_DIR/zisk.toml"
