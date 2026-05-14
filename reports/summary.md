# 📊 zkVM Soundness Summary

How to read this report:
- Click on zkVM names to view detailed individual reports
- Security shows the best bits of security across the reported regimes

## Overview

| zkVM | Version | Security | Expected Proof Size | Worst-Case Proof Size | Proof system | Field | Circuits |
|------|---------|----------|---------------------|-----------------------|--------------|-------|----------|
| [Airbender](airbender.md) | — | **67** bits (JBR) | 1836 KiB | 1951 KiB | DEEP-ALI + FRI | M31⁴ | 1 |
| [OpenVM](openvm.md) | 1.5.0 | **100** bits (UDR) | 7687 KiB | 8231 KiB | DEEP-ALI + FRI | BabyBear⁴ | 3 |
| [OpenVM2](openvm2.md) | 2.0.0-beta | **100** bits (UDR) | TODO | TODO | SWIRL + WHIR | BabyBear⁴ | 4 |
| [Pico](pico.md) | — | **53** bits (JBR) | 232 KiB | 281 KiB | DEEP-ALI + FRI | KoalaBear⁴ | 5 |
| [SP1](sp1.md) | 6.1.0 | **100** bits (UDR) | 529 KiB | 887 KiB | Jagged + FRI | KoalaBear⁴ | 3 |
| [Venus](venus.md) | 0.1.6 | **128** bits (JBR) | 269 KiB | 313 KiB | DEEP-ALI + FRI | Goldilocks³ | 44 |
| [ZisK](zisk.md) | 0.16.1 | **128** bits (JBR) | 269 KiB | 313 KiB | DEEP-ALI + FRI | Goldilocks³ | 44 |

## Notes

- **Security**: Best bits of security across the reported regimes
- **Proof Size**: Final proof size in KiB (1 KiB = 1024 bytes)
