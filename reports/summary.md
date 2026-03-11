# 📊 zkVM Soundness Summary

How to read this report:
- Click on zkVM names to view detailed individual reports
- Security shows the best bits of security across regimes (UDR/JBR)

## Overview

| zkVM | Version | Security | Proof Size | PCS | Field | Circuits | Weakest Circuit |
|------|---------|----------|------------|-----|-------|----------|-----------------|
| [Airbender](airbender.md) | — | **67** bits (JBR) | 1951 KiB | FRI | M31⁴ | 1 | generalized_circuit |
| [OpenVM](openvm.md) | 1.5.0 | **100** bits (UDR) | 8231 KiB | FRI | BabyBear⁴ | 3 | app |
| [Pico](pico.md) | — | **53** bits (JBR) | 281 KiB | FRI | KoalaBear⁴ | 5 | riscv |
| [SP1](sp1.md) | — | **98** bits (UDR) | 1001 KiB | Unknown | KoalaBear⁴ | 4 | wrap |
| [ZisK](zisk.md) | 0.16.0 | **128** bits (JBR) | 313 KiB | FRI | Goldilocks³ | 44 | Dma |

## Notes

- **Security**: Best bits of security across UDR (Unique Decoding) and JBR (Johnson Bound) regimes
- **Weakest Circuit**: Circuit determining the overall security level
- **Proof Size**: Final proof size in KiB (1 KiB = 1024 bytes)
