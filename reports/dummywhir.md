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
- Constraint degree: 3
- Batch size: 100
- Batching: Powers
- Queries per iteration: [119, 47, 29, 22, 18]
- OOD samples per iteration: [2, 2, 2, 2]
- Total grinding overhead log2: 16.88

**Proof Size Estimate:** 191 KiB, where 1 KiB = 1024 bytes

| regime | total | OOD(i=1) | OOD(i=2) | OOD(i=3) | OOD(i=4) | Shift(i=1) | Shift(i=2) | Shift(i=3) | Shift(i=4) | batching | fin | fold(i=0,s=1) | fold(i=0,s=2) | fold(i=0,s=3) | fold(i=0,s=4) | fold(i=1,s=1) | fold(i=1,s=2) | fold(i=1,s=3) | fold(i=1,s=4) | fold(i=2,s=1) | fold(i=2,s=2) | fold(i=2,s=3) | fold(i=2,s=4) | fold(i=3,s=1) | fold(i=3,s=2) | fold(i=3,s=3) | fold(i=3,s=4) | fold(i=4,s=1) | fold(i=4,s=2) | fold(i=4,s=3) | fold(i=4,s=4) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 25 | 219 | 227 | 235 | 243 | 95 | 59 | 43 | 29 | 106 | 25 | 113 | 114 | 115 | 116 | 114 | 115 | 116 | 117 | 115 | 116 | 117 | 118 | 116 | 117 | 118 | 119 | 117 | 118 | 119 | 120 |
| JBR | 40 | 198 | 197 | 196 | 195 | 125 | 122 | 118 | 107 | 77 | 133 | 84 | 85 | 86 | 87 | 73 | 74 | 75 | 76 | 62 | 63 | 64 | 65 | 51 | 52 | 53 | 54 | 40 | 41 | 42 | 43 |
