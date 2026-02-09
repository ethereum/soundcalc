# 📊 zkVM Soundness Summary

How to read this report:
- Click on zkVM names to view detailed individual reports
- UDR/JBR columns show bits of security under different regimes

## Overview

| zkVM | Field | Circuits | Weakest Circuit | UDR (bits) | JBR (bits) | Proof Size |
|------|-------|----------|-----------------|------------|------------|------------|
| [Airbender](airbender.md) | M31⁴ | 1 | generalized_circuit | 64 | 63 | 1951 KiB |
| [DummyWHIR](dummywhir.md) | Goldilocks³ | 2 | main | 30 | 128 | 974 KiB |
| [OpenVM](openvm.md) | BabyBear⁴ | 3 | internal | 45 | 58 | 1386 KiB |
| [Pico](pico.md) | KoalaBear⁴ | 5 | riscv | 35 | 53 | 281 KiB |
| [SP1](sp1.md) | KoalaBear⁴ | 4 | core | 98 | 0 | 1001 KiB |
| [ZisK](zisk.md) | Goldilocks³ | 30 | Main | 63 | 128 | 313 KiB |

## Notes

- **UDR**: Unique Decoding Regime
- **JBR**: Johnson Bound Regime
- **Weakest Circuit**: Circuit with lowest JBR security level
- **Proof Size**: Final proof size in KiB (1 KiB = 1024 bytes)
