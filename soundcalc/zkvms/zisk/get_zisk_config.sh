#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cleanup() {
    echo "=== Performing cleanup ==="
    rm -rf "$SCRIPT_DIR/zisk-setup"
}

trap cleanup EXIT

echo "=== 1. Check and install Rust ==="
if ! command -v cargo &> /dev/null; then
    echo "Rust not found. Installing..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
else
    echo "Rust is already installed."
fi

rustup default stable
rustc --version
cargo --version

echo "=== 2. Check Python is installed ==="
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
else
    echo "Python3 is already installed:"
    python3 --version
fi

echo "=== 3. Install dependencies ==="
sudo apt-get update
sudo apt-get install -y \
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

echo "=== 4. Download ZisK proving key ==="
ZISK_SETUP="$SCRIPT_DIR/zisk-setup"
mkdir -p "$ZISK_SETUP"
wget https://storage.googleapis.com/zisk-setup/zisk-provingkey-pre-0.15.0.tar.gz -O "$ZISK_SETUP/zisk-provingkey.tar.gz"
tar -xvzf "$ZISK_SETUP/zisk-provingkey.tar.gz" -C "$ZISK_SETUP"

echo "=== 5. Clone pil2-proofman ==="
PIL2_DIR="$ZISK_SETUP/pil2-proofman"
git clone --branch pre-develop-0.15.0 https://github.com/0xPolygonHermez/pil2-proofman.git "$PIL2_DIR"

echo "=== 6. Generate ZisK TOML ==="
cargo run --manifest-path "$PIL2_DIR/Cargo.toml" --bin proofman-cli soundness -k "$ZISK_SETUP/provingKey" -a -o "$SCRIPT_DIR/zisk.toml"

echo "=== 7. Calculate soundness info ==="
python3 -m soundcalc --print-only Zisk

echo "=== DONE ==="
echo "Generated TOML: $SCRIPT_DIR/zisk.toml"
