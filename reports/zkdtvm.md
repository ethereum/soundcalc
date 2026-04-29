# 📊 zkDTVM (v0.1.0)

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimates are indicative (1 KiB = 1024 bytes)

## zkVM Overview

| Metric | Value | Relevant circuit | Notes |
| --- | --- | --- | --- |
| Final bits of security | **100 bits** | [core](#core) | Regime: UDR |
| Final proof size (worst case) | **1206 KiB** | [compress](#compress) | |

## Circuits

- [core](#core)
- [compress](#compress)

## core

**Parameters:**
- Proof system: Jagged
- PCS: FRI
- Hash size (bits): 248
- Number of queries: 193
- Grinding query phase (bits): 20
- Field: KoalaBear⁴
- Rate (ρ): 0.5
- Dense trace length: $2^{21}$
- Trace length: 4194304
- Trace width: 31209
- FRI rounds: 21
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 2
- Dense batch size: 62928
- Batching: Powers
- Lookup (logup): lookup

**Proof Size:** 184556 KiB (expected) / 185445 KiB (worst case)

| regime | total | lookup | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 18 | commit round 19 | commit round 2 | commit round 20 | commit round 21 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase | reduce to dense PCS | zerocheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 100 | 105 | 100 | 104 | 113 | 114 | 115 | 116 | 117 | 118 | 119 | 120 | 121 | 122 | 105 | 122 | 123 | 106 | 107 | 108 | 109 | 110 | 111 | 112 | 100 | 116 | 109 |


## compress

**Parameters:**
- Proof system: Jagged
- PCS: FRI
- Hash size (bits): 248
- Number of queries: 118
- Grinding query phase (bits): 20
- Field: KoalaBear⁴
- Rate (ρ): 0.25
- Dense trace length: $2^{20}$
- Trace length: 2097152
- Trace width: 326
- FRI rounds: 20
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 4
- Dense batch size: 128
- Batching: Powers
- Lookup (logup): lookup

**Proof Size:** 703 KiB (expected) / 1206 KiB (worst case)

| regime | total | lookup | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 18 | commit round 19 | commit round 2 | commit round 20 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase | reduce to dense PCS | zerocheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 100 | 105 | 106 | 104 | 113 | 114 | 115 | 116 | 117 | 118 | 119 | 120 | 121 | 121 | 105 | 122 | 106 | 107 | 108 | 109 | 110 | 111 | 112 | 100 | 116 | 115 |

