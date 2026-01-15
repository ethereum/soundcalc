# 📊 zkVM Soundness Summary

How to read this report:
- Click on zkVM names to view detailed individual reports
- UDR/JBR columns show bits of security under different regimes

## Overview

| zkVM | Field | Circuits | Weakest Circuit | UDR (bits) | JBR (bits) | Proof Size |
|------|-------|----------|-----------------|------------|------------|------------|
| [Airbender](airbender.md) | M31⁴ | 1 | generalized_circuit | 64 | 63 | 1951 KiB |
| [DummyWHIR](dummywhir.md) | Goldilocks³ | 1 | main | 30 | 128 | 1243 KiB |
| [Miden](miden.md) | Goldilocks² | 1 | main | 38 | 55 | 149 KiB |
| [OpenVM](openvm.md) | BabyBear⁴ | 3 | internal | 45 | 58 | 1386 KiB |
| [Pico](pico.md) | KoalaBear⁴ | 5 | riscv | 35 | 53 | 281 KiB |
| [RISC0](risc0.md) | BabyBear⁴ | 1 | main | 33 | 48 | 380 KiB |
| [ZisK](zisk.md) | Goldilocks³ | 27 | Main | 63 | 128 | 282 KiB |

## Notes

- **UDR**: Unique Decoding Regime
- **JBR**: Johnson Bound Regime
- **Weakest Circuit**: Circuit with lowest JBR security level
- **Proof Size**: Final proof size in KiB (1 KiB = 1024 bytes)
