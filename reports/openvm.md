# 📊 OpenVM (v1.5.0)

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimates are indicative (1 KiB = 1024 bytes)

## zkVM Overview

| Metric | Value | Relevant circuit | Notes |
| --- | --- | --- | --- |
| Final proof size (worst case) | **8231 KiB** | [internal](#internal) | |
| Final bits of security | **100 bits** | [app](#app) | Regime: UDR |

## Circuits

- [app](#app)
- [leaf](#leaf)
- [internal](#internal)

## app

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 193
- Grinding query phase (bits): 20
- Grinding batching phase (bits): 20
- Field: BabyBear⁴
- Rate (ρ): 0.5
- Trace length (H): $2^{23}$
- FRI rounds: 23
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 2
- Batch size: 80000
- Batching: Powers
- Grinding DEEP (bits): 5
- Number of constraints: 15000

**Proof Size:** 234635 KiB (expected) / 235651 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 18 | commit round 19 | commit round 2 | commit round 20 | commit round 21 | commit round 22 | commit round 23 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 100 | 109 | 103 | 105 | 102 | 111 | 112 | 113 | 114 | 115 | 116 | 117 | 118 | 119 | 120 | 103 | 121 | 122 | 122 | 123 | 104 | 105 | 106 | 107 | 108 | 109 | 110 | 100 |
| JBR | 75 | 104 | 98 | 78 | 75 | 84 | 85 | 86 | 87 | 88 | 89 | 90 | 91 | 92 | 93 | 76 | 94 | 95 | 96 | 97 | 77 | 78 | 79 | 80 | 81 | 82 | 83 | 106 |


## leaf

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 193
- Grinding query phase (bits): 20
- Grinding batching phase (bits): 20
- Field: BabyBear⁴
- Rate (ρ): 0.5
- Trace length (H): $2^{23}$
- FRI rounds: 23
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 2
- Batch size: 80000
- Batching: Powers
- Grinding DEEP (bits): 5
- Number of constraints: 15000

**Proof Size:** 234635 KiB (expected) / 235651 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 18 | commit round 19 | commit round 2 | commit round 20 | commit round 21 | commit round 22 | commit round 23 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 100 | 109 | 103 | 105 | 102 | 111 | 112 | 113 | 114 | 115 | 116 | 117 | 118 | 119 | 120 | 103 | 121 | 122 | 122 | 123 | 104 | 105 | 106 | 107 | 108 | 109 | 110 | 100 |
| JBR | 75 | 104 | 98 | 78 | 75 | 84 | 85 | 86 | 87 | 88 | 89 | 90 | 91 | 92 | 93 | 76 | 94 | 95 | 96 | 97 | 77 | 78 | 79 | 80 | 81 | 82 | 83 | 106 |


## internal

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 118
- Grinding query phase (bits): 20
- Grinding batching phase (bits): 16
- Field: BabyBear⁴
- Rate (ρ): 0.25
- Trace length (H): $2^{21}$
- FRI rounds: 21
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 4
- Batch size: 4000
- Batching: Powers
- Grinding DEEP (bits): 5
- Number of constraints: 15000
- Lookup (logup): lookup

**Proof Size:** 7687 KiB (expected) / 8231 KiB (worst case)

| regime | total | lookup | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 18 | commit round 19 | commit round 2 | commit round 20 | commit round 21 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 100 | 134 | 109 | 105 | 106 | 103 | 112 | 113 | 114 | 115 | 116 | 117 | 118 | 118 | 119 | 120 | 104 | 121 | 122 | 105 | 106 | 107 | 108 | 109 | 110 | 111 | 100 |
| JBR | 72 | 134 | 103 | 98 | 75 | 72 | 81 | 82 | 83 | 84 | 85 | 86 | 87 | 88 | 89 | 90 | 73 | 91 | 92 | 74 | 75 | 76 | 77 | 78 | 79 | 80 | 133 |

