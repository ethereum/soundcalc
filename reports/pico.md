# 📊 Pico

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimate is only indicative

## zkEVM Overview

| Metric | Value |
| --- | --- |
| Final proof size | **232.0 KiB** (circuit: embed) |
| Final bits of security | **53** (JBR, circuit: riscv) |

## Circuits

- [riscv](#riscv)
- [convert](#convert)
- [combine](#combine)
- [compress](#compress)
- [embed](#embed)

## riscv

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 248
- Number of queries: 84
- Grinding (bits): 16
- Field: KoalaBear⁴
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 22
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 2
- Number of columns: 1278
- Batch size: 1435
- Batching: Powers

**Proof Size Estimate:** 2225.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 18 | commit round 19 | commit round 2 | commit round 20 | commit round 21 | commit round 22 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 50 | 113 | 99 | 90 | 101 | 110 | 111 | 112 | 113 | 114 | 115 | 116 | 117 | 118 | 119 | 102 | 120 | 121 | 122 | 103 | 104 | 105 | 106 | 107 | 108 | 109 | 50 |
| JBR | 53 | 108 | 95 | 65 | 76 | 85 | 86 | 87 | 88 | 89 | 90 | 91 | 92 | 93 | 94 | 77 | 95 | 96 | 97 | 78 | 79 | 80 | 81 | 82 | 83 | 84 | 53 |


## convert

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 248
- Number of queries: 84
- Grinding (bits): 16
- Field: KoalaBear⁴
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 20
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 2
- Number of columns: 467
- Batch size: 485
- Batching: Powers

**Proof Size Estimate:** 934.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 18 | commit round 19 | commit round 2 | commit round 20 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 50 | 115 | 101 | 94 | 103 | 112 | 113 | 114 | 115 | 116 | 117 | 118 | 119 | 120 | 121 | 104 | 122 | 105 | 106 | 107 | 108 | 109 | 110 | 111 | 50 |
| JBR | 53 | 110 | 97 | 68 | 78 | 87 | 88 | 89 | 90 | 91 | 92 | 93 | 94 | 95 | 96 | 79 | 97 | 80 | 81 | 82 | 83 | 84 | 85 | 86 | 53 |


## combine

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 248
- Number of queries: 84
- Grinding (bits): 16
- Field: KoalaBear⁴
- Rate (ρ): 0.5
- Trace length (H): $2^{18}$
- FRI rounds: 18
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 2
- Number of columns: 467
- Batch size: 485
- Batching: Powers

**Proof Size Estimate:** 861.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 18 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 50 | 115 | 103 | 96 | 105 | 114 | 115 | 116 | 117 | 118 | 119 | 120 | 121 | 122 | 106 | 107 | 108 | 109 | 110 | 111 | 112 | 113 | 50 |
| JBR | 53 | 110 | 99 | 70 | 80 | 89 | 90 | 91 | 92 | 93 | 94 | 95 | 96 | 97 | 81 | 82 | 83 | 84 | 85 | 86 | 87 | 88 | 53 |


## compress

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 248
- Number of queries: 21
- Grinding (bits): 16
- Field: KoalaBear⁴
- Rate (ρ): 0.0625
- Trace length (H): $2^{17}$
- FRI rounds: 17
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 16
- Number of columns: 467
- Batch size: 485
- Batching: Powers

**Proof Size Estimate:** 253.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 35 | 115 | 104 | 94 | 103 | 112 | 113 | 114 | 115 | 116 | 117 | 118 | 119 | 104 | 105 | 106 | 107 | 108 | 109 | 110 | 111 | 35 |
| JBR | 56 | 105 | 95 | 56 | 66 | 75 | 76 | 77 | 78 | 79 | 80 | 81 | 82 | 67 | 68 | 69 | 70 | 71 | 72 | 73 | 74 | 57 |


## embed

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 248
- Number of queries: 21
- Grinding (bits): 16
- Field: KoalaBear⁴
- Rate (ρ): 0.0625
- Trace length (H): $2^{15}$
- FRI rounds: 15
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 16
- Number of columns: 467
- Batch size: 485
- Batching: Powers

**Proof Size Estimate:** 232.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 35 | 115 | 106 | 96 | 105 | 114 | 115 | 116 | 117 | 118 | 119 | 106 | 107 | 108 | 109 | 110 | 111 | 112 | 113 | 35 |
| JBR | 57 | 105 | 97 | 58 | 68 | 77 | 78 | 79 | 80 | 81 | 82 | 69 | 70 | 71 | 72 | 73 | 74 | 75 | 76 | 57 |

