# 📊 zkVM Soundness Summary

How to read this report:
- Click on zkVM names to view detailed individual reports
- Security shows the best bits of security across the reported regimes

## Overview

| zkVM | Version | Security | Proof Size | PCS | Field | Circuits | Weakest Circuit |
|------|---------|----------|------------|-----|-------|----------|-----------------|
| [Airbender](airbender.md) | — | **64** bits (UDR) | 1951 KiB | FRI | M31⁴ | 1 | generalized_circuit |
| [OpenVM](openvm.md) | 1.5.0 | **100** bits (UDR) | 8231 KiB | FRI | BabyBear⁴ | 3 | app |
| [OpenVM2](openvm2.md) | 2.0.0-beta | **100** bits (UDR) | 140 KiB | SWIRL | BabyBear⁴ | 4 | app |
| [Pico](pico.md) | — | **53** bits (JBR) | 281 KiB | FRI | KoalaBear⁴ | 5 | riscv |
| [SP1](sp1.md) | 6.1.0 | **100** bits (UDR) | 1267 KiB | Jagged + FRI | KoalaBear⁴ | 2 | core |
| [ZisK](zisk.md) | 0.16.1 | **128** bits (JBR) | 313 KiB | FRI | Goldilocks³ | 44 | Dma |

## Notes

- **Security**: Best bits of security across the reported regimes
- **Weakest Circuit**: Circuit determining the overall security level
- **Proof Size**: Final proof size in KiB (1 KiB = 1024 bytes)
