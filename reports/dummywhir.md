# 📊 DummyWHIR

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimate is only indicative

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
| UDR | 21 | 219 | 227 | 235 | 243 | 33 | 31 | 21 | 23 | 107 | 28 | 114 | 115 | 116 | 117 | 115 | 116 | 117 | 118 | 116 | 117 | 118 | 119 | 117 | 118 | 119 | 120 | 118 | 119 | 120 | 121 |
| JBR | -12 | 217 | 222 | 227 | 232 | 39 | 69 | 76 | 71 | -12 | 78 | 1 | 7 | 13 | 19 | 10 | 16 | 22 | 28 | 19 | 25 | 31 | 37 | 28 | 34 | 40 | 46 | 37 | 43 | 49 | 55 |
