# 📊 zkVM Soundness Summary

How to read this report:
- Click on zkVM names to view detailed individual reports
- Security shows the best bits of security across the reported regimes
- Only zkVMs with at least [100 bits of security](https://blog.ethereum.org/2025/12/18/zkevm-security-foundations#three-milestones) and an expected proof size below 600 KiB are shown

## Overview

| zkVM | Version | Security | Expected Proof Size | Worst-Case Proof Size | Proof system | Field | Circuits |
|------|---------|----------|---------------------|-----------------------|--------------|-------|----------|
| [OpenVM2](openvm2.md) | 2.0.0 | **100** bits (mixed) | 270 KiB | 270 KiB | SWIRL + WHIR | BabyBear⁴ | 6 |
| [SP1](sp1.md) | 6.1.0 | **100** bits (UDR) | 524 KiB | 555 KiB | Jagged + FRI | KoalaBear⁴ | 3 |
| [Venus](venus.md) | 0.1.6 | **128** bits (JBR) | 268 KiB | 274 KiB | DEEP-ALI + FRI | Goldilocks³ | 44 |
| [ZisK](zisk.md) | 1.4.0-alpha | **128** bits (JBR) | 240 KiB | 247 KiB | Mixed(DEEP-ALI + FRI, DEEP-ALI + STIR) | Goldilocks³ | 60 |
| [zkDTVM](zkdtvm.md) | 0.8.0 | **128** bits (mixed) | 200 KiB | 200 KiB | Mixed(Jagged + FRI, SWIRL + WHIR) | KoalaBear⁵ | 4 |

## Notes

- **Security**: Best bits of security across the reported regimes
- **Proof Size**: Final proof size in KiB (1 KiB = 1024 bytes)
