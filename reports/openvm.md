# 📊 OpenVM

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimates are indicative (1 KiB = 1024 bytes)

## zkVM Overview

| Metric | Value | Relevant circuit | Notes |
| --- | --- | --- | --- |
| Final proof size (worst case) | **1386 KiB** | [internal](#internal) | |
| Final bits of security | **58 bits** | [internal](#internal) | Regime: JBR |

## Circuits

- [app](#app)
- [leaf](#leaf)
- [internal](#internal)

## app

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 100
- Grinding query phase (bits): 16
- Field: BabyBear⁴
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 22
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 2
- Number of constraints: 11366
- Batch size: 14162
- Batching: Powers

**Proof Size:** 21913 KiB (expected) / 22364 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 18 | commit round 19 | commit round 2 | commit round 20 | commit round 21 | commit round 22 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 57 | 110 | 99 | 88 | 103 | 112 | 113 | 114 | 115 | 116 | 117 | 118 | 119 | 120 | 121 | 104 | 122 | 122 | 123 | 105 | 106 | 107 | 108 | 109 | 110 | 111 | 57 |
| JBR | 60 | 105 | 94 | 61 | 76 | 85 | 86 | 87 | 88 | 89 | 90 | 91 | 92 | 93 | 94 | 77 | 95 | 96 | 97 | 78 | 79 | 80 | 81 | 82 | 83 | 84 | 60 |


## leaf

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 100
- Grinding query phase (bits): 16
- Field: BabyBear⁴
- Rate (ρ): 0.5
- Trace length (H): $2^{23}$
- FRI rounds: 23
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 2
- Number of constraints: 885
- Batch size: 1798
- Batching: Powers

**Proof Size:** 3253 KiB (expected) / 3727 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 18 | commit round 19 | commit round 2 | commit round 20 | commit round 21 | commit round 22 | commit round 23 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 57 | 113 | 98 | 90 | 102 | 111 | 112 | 113 | 114 | 115 | 116 | 117 | 118 | 119 | 120 | 103 | 121 | 122 | 122 | 123 | 104 | 105 | 106 | 107 | 108 | 109 | 110 | 57 |
| JBR | 60 | 109 | 93 | 63 | 75 | 84 | 85 | 86 | 87 | 88 | 89 | 90 | 91 | 92 | 93 | 76 | 94 | 95 | 96 | 97 | 77 | 78 | 79 | 80 | 81 | 82 | 83 | 60 |


## internal

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 44
- Grinding query phase (bits): 16
- Field: BabyBear⁴
- Rate (ρ): 0.25
- Trace length (H): $2^{21}$
- FRI rounds: 21
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 4
- Number of constraints: 801
- Batch size: 1472
- Batching: Powers
- Lookup (logup): lookup

**Proof Size:** 1218 KiB (expected) / 1386 KiB (worst case)

| regime | total | lookup | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 18 | commit round 19 | commit round 2 | commit round 20 | commit round 21 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 45 | 132 | 113 | 100 | 91 | 103 | 112 | 113 | 114 | 115 | 116 | 117 | 118 | 118 | 119 | 120 | 104 | 121 | 122 | 105 | 106 | 107 | 108 | 109 | 110 | 111 | 45 |
| JBR | 58 | 132 | 107 | 93 | 60 | 72 | 81 | 82 | 83 | 84 | 85 | 86 | 87 | 88 | 89 | 90 | 73 | 91 | 92 | 74 | 75 | 76 | 77 | 78 | 79 | 80 | 58 |

