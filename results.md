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
- FRI folding factor: 16
- FRI early stop degree: 32
- Batching: Powers

**Proof Size Estimate:** 992 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | FRI batching round | FRI commit rounds (×5) | FRI query phase |
| --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 185 | 167 | 162 | 165 | 53 |
| JBR | 58 | 181 | 163 | 142 | 159 | 58 |
| best attack | 128 | — | — | — | — | — |

## Miden

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 27
- Grinding (bits): 16
- Field: Goldilocks²
- Rate (ρ): 0.125
- Trace length (H): $2^{18}$
- FRI folding factor: 4
- FRI early stop degree: 128
- Batching: Powers

**Proof Size Estimate:** 175 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | FRI batching round | FRI commit rounds (×7) | FRI query phase |
| --- | --- | --- | --- | --- | --- | --- |
| UDR | 38 | 121 | 106 | 100 | 105 | 38 |
| JBR | 55 | 115 | 101 | 77 | 98 | 55 |
| best attack | 96 | — | — | — | — | — |

## RISC0

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 50
- Grinding (bits): 0
- Field: BabyBear⁴
- Rate (ρ): 0.25
- Trace length (H): $2^{21}$
- FRI folding factor: 16
- FRI early stop degree: 256
- Batching: Powers

**Proof Size Estimate:** 576 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | FRI batching round | FRI commit rounds (×4) | FRI query phase |
| --- | --- | --- | --- | --- | --- | --- |
| UDR | 33 | 115 | 100 | 92 | 96 | 33 |
| JBR | 47 | 110 | 95 | 70 | 90 | 47 |
| best attack | 99 | — | — | — | — | — |

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
| JBR | 36 | 203 | 205 | 207 | 209 | 36 | 68 | 76 | 71 | 53 | 78 | 62 | 64 | 66 | 68 | 59 | 61 | 63 | 65 | 57 | 59 | 61 | 63 | 54 | 56 | 58 | 60 | 52 | 54 | 56 | 58 |
