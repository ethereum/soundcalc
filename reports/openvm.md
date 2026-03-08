# 📊 OpenVM

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimates are indicative (1 KiB = 1024 bytes)

## zkVM Overview

| Metric | Value | Relevant circuit | Notes |
| --- | --- | --- | --- |
| Final proof size (worst case) | **8231 KiB** | [internal](#internal) | |
| Final bits of security | **85 bits** | [app](#app) | Regime: UDR |

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
- Grinding commit phase (bits): 20
- Grinding DEEP (bits): 5
- Field: BabyBear⁴
- Rate (ρ): 0.5
- Trace length (H): $2^{23}$
- FRI rounds: 23
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 2
- Number of constraints: 15000
- Batch size: 80000
- Batching: Powers

**Proof Size:** 234635 KiB (expected) / 235651 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 18 | commit round 19 | commit round 2 | commit round 20 | commit round 21 | commit round 22 | commit round 23 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 85 | 109 | 103 | 85 | 122 | 131 | 132 | 133 | 134 | 135 | 136 | 137 | 138 | 139 | 140 | 123 | 141 | 142 | 142 | 143 | 124 | 125 | 126 | 127 | 128 | 129 | 130 | 100 |
| JBR | 58 | 104 | 98 | 58 | 95 | 104 | 105 | 106 | 107 | 108 | 109 | 110 | 111 | 112 | 113 | 96 | 114 | 115 | 116 | 117 | 97 | 98 | 99 | 100 | 101 | 102 | 103 | 106 |


## leaf

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 193
- Grinding query phase (bits): 20
- Grinding commit phase (bits): 20
- Grinding DEEP (bits): 5
- Field: BabyBear⁴
- Rate (ρ): 0.5
- Trace length (H): $2^{23}$
- FRI rounds: 23
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 2
- Number of constraints: 15000
- Batch size: 80000
- Batching: Powers

**Proof Size:** 234635 KiB (expected) / 235651 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 18 | commit round 19 | commit round 2 | commit round 20 | commit round 21 | commit round 22 | commit round 23 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 85 | 109 | 103 | 85 | 122 | 131 | 132 | 133 | 134 | 135 | 136 | 137 | 138 | 139 | 140 | 123 | 141 | 142 | 142 | 143 | 124 | 125 | 126 | 127 | 128 | 129 | 130 | 100 |
| JBR | 58 | 104 | 98 | 58 | 95 | 104 | 105 | 106 | 107 | 108 | 109 | 110 | 111 | 112 | 113 | 96 | 114 | 115 | 116 | 117 | 97 | 98 | 99 | 100 | 101 | 102 | 103 | 106 |


## internal

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 118
- Grinding query phase (bits): 20
- Grinding commit phase (bits): 16
- Grinding DEEP (bits): 5
- Field: BabyBear⁴
- Rate (ρ): 0.25
- Trace length (H): $2^{21}$
- FRI rounds: 21
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 4
- Number of constraints: 15000
- Batch size: 4000
- Batching: Powers
- Lookup (logup): lookup

**Proof Size:** 7687 KiB (expected) / 8231 KiB (worst case)

| regime | total | lookup | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 18 | commit round 19 | commit round 2 | commit round 20 | commit round 21 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 90 | 134 | 109 | 105 | 90 | 119 | 128 | 129 | 130 | 131 | 132 | 133 | 134 | 134 | 135 | 136 | 120 | 137 | 138 | 121 | 122 | 123 | 124 | 125 | 126 | 127 | 100 |
| JBR | 59 | 134 | 103 | 98 | 59 | 88 | 97 | 98 | 99 | 100 | 101 | 102 | 103 | 104 | 105 | 106 | 89 | 107 | 108 | 90 | 91 | 92 | 93 | 94 | 95 | 96 | 133 |

