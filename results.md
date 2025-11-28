# 📊 soundcalc report

How to read this report:
- Choose a zkEVM
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimate is only indicative

# Supported zkEVMs
- [ZisK](#zisk)
- [Miden](#miden)
- [RISC0](#risc0)
- [DummyWHIR](#dummywhir)

## ZisK

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 128
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 5
- FRI folding factors: [16, 16, 16, 8, 8]
- FRI early stop degree: 32
- Batching: Powers

**Proof Size Estimate:** 928 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 185 | 167 | 162 | 166 | 170 | 174 | 174 | 177 | 53 |
| JBR | 58 | 180 | 162 | 141 | 145 | 149 | 153 | 153 | 156 | 58 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |

## Miden

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 27
- Grinding (bits): 16
- Field: Goldilocks²
- Rate (ρ): 0.125
- Trace length (H): $2^{18}$
- FRI rounds: 7
- FRI folding factors: [4, 4, 4, 4, 4, 4, 4]
- FRI early stop degree: 128
- Batching: Powers

**Proof Size Estimate:** 177 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 38 | 121 | 106 | 100 | 102 | 104 | 106 | 108 | 110 | 112 | 114 | 38 |
| JBR | 55 | 114 | 99 | 75 | 77 | 79 | 81 | 83 | 85 | 87 | 89 | 55 |
| best attack | 96 | — | — | — | — | — | — | — | — | — | — | — |

## RISC0

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 50
- Grinding (bits): 0
- Field: BabyBear⁴
- Rate (ρ): 0.25
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 128
- Batching: Powers

**Proof Size Estimate:** 582 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 33 | 115 | 100 | 92 | 96 | 100 | 104 | 108 | 33 |
| JBR | 47 | 109 | 94 | 69 | 73 | 77 | 81 | 85 | 47 |
| best attack | 99 | — | — | — | — | — | — | — | — |

## DummyWHIR

**Parameters:**
- Polynomial commitment scheme: WHIR
- Hash size (bits): 256
- Field: Goldilocks²
- Iterations (M): 5
- Folding factor (k): 4
- Constraint degree: 1
- Batch size: 100
- Batching: Powers
- Queries per iteration: [80, 35, 22, 12, 9]
- OOD samples per iteration: [2, 2, 2, 2]
- Total grinding overhead log2: 20.03

**Proof Size Estimate:** 168 KiB, where 1 KiB = 1024 bytes

| regime | total | OOD(i=1) | OOD(i=2) | OOD(i=3) | OOD(i=4) | Shift(i=1) | Shift(i=2) | Shift(i=3) | Shift(i=4) | batching | fin | fold(i=0,s=1) | fold(i=0,s=2) | fold(i=0,s=3) | fold(i=0,s=4) | fold(i=1,s=1) | fold(i=1,s=2) | fold(i=1,s=3) | fold(i=1,s=4) | fold(i=2,s=1) | fold(i=2,s=2) | fold(i=2,s=3) | fold(i=2,s=4) | fold(i=3,s=1) | fold(i=3,s=2) | fold(i=3,s=3) | fold(i=3,s=4) | fold(i=4,s=1) | fold(i=4,s=2) | fold(i=4,s=3) | fold(i=4,s=4) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 21 | 219 | 227 | 235 | 243 | 33 | 31 | 21 | 23 | 107 | 28 | 113 | 114 | 115 | 116 | 114 | 115 | 116 | 117 | 115 | 116 | 117 | 118 | 116 | 117 | 118 | 119 | 117 | 118 | 119 | 120 |
| JBR | 36 | 203 | 205 | 207 | 209 | 36 | 68 | 76 | 71 | 85 | 78 | 93 | 94 | 95 | 96 | 89 | 90 | 91 | 92 | 86 | 87 | 88 | 89 | 82 | 83 | 84 | 85 | 79 | 80 | 81 | 82 |
