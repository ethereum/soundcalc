# 📊 DummyWHIR

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimates are indicative (1 KiB = 1024 bytes)

## zkVM Overview

| Metric | Value | Relevant circuit | Notes |
| --- | --- | --- | --- |
| Final proof size (worst case) | **974 KiB** | [dummy](#dummy) | |
| Final bits of security | **128 bits** | [main](#main) | Regime: JBR |

## Circuits

- [main](#main)
- [dummy](#dummy)

## main

**Parameters:**
- Polynomial commitment scheme: WHIR
- Hash size (bits): 256
- Field: Goldilocks³
- Iterations (M): 5
- Folding factor (k): 4
- Constraint degree: 8
- Batch size: 164
- Batching: Powers
- Queries per iteration: [55, 31, 22, 17, 14]
- OOD samples per iteration: [1, 1, 1, 1]
- Total grinding overhead log2: 24.16

**Proof Size:** 1219 KiB (expected) / 1243 KiB (worst case)

| regime | total | OOD(i=1) | OOD(i=2) | OOD(i=3) | OOD(i=4) | Shift(i=1) | Shift(i=2) | Shift(i=3) | Shift(i=4) | batching | fin | fold(i=0,s=1) | fold(i=0,s=2) | fold(i=0,s=3) | fold(i=0,s=4) | fold(i=1,s=1) | fold(i=1,s=2) | fold(i=1,s=3) | fold(i=1,s=4) | fold(i=2,s=1) | fold(i=2,s=2) | fold(i=2,s=3) | fold(i=2,s=4) | fold(i=3,s=1) | fold(i=3,s=2) | fold(i=3,s=3) | fold(i=3,s=4) | fold(i=4,s=1) | fold(i=4,s=2) | fold(i=4,s=3) | fold(i=4,s=4) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 30 | 176 | 180 | 184 | 188 | 72 | 52 | 41 | 35 | 182 | 30 | 186 | 185 | 184 | 183 | 185 | 184 | 183 | 182 | 189 | 188 | 187 | 186 | 192 | 191 | 190 | 188 | 195 | 194 | 193 | 192 |
| JBR | 128 | 151 | 149 | 147 | 145 | 131 | 130 | 129 | 129 | 142 | 128 | 146 | 145 | 144 | 143 | 140 | 139 | 138 | 137 | 140 | 139 | 138 | 137 | 138 | 137 | 136 | 135 | 138 | 137 | 136 | 135 |


## dummy

**Parameters:**
- Polynomial commitment scheme: WHIR
- Hash size (bits): 256
- Field: Goldilocks³
- Iterations (M): 4
- Folding factor (k): 4
- Constraint degree: 4
- Batch size: 128
- Batching: Powers
- Queries per iteration: [55, 31, 22, 17]
- OOD samples per iteration: [1, 1, 1]
- Total grinding overhead log2: 23.64
- Lookup (logup): dummy_lookup

**Proof Size:** 951 KiB (expected) / 974 KiB (worst case)

| regime | total | dummy_lookup | OOD(i=1) | OOD(i=2) | OOD(i=3) | Shift(i=1) | Shift(i=2) | Shift(i=3) | batching | fin | fold(i=0,s=1) | fold(i=0,s=2) | fold(i=0,s=3) | fold(i=0,s=4) | fold(i=1,s=1) | fold(i=1,s=2) | fold(i=1,s=3) | fold(i=1,s=4) | fold(i=2,s=1) | fold(i=2,s=2) | fold(i=2,s=3) | fold(i=2,s=4) | fold(i=3,s=1) | fold(i=3,s=2) | fold(i=3,s=3) | fold(i=3,s=4) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 35 | 190 | 178 | 182 | 186 | 72 | 52 | 41 | 185 | 35 | 188 | 187 | 186 | 185 | 187 | 186 | 185 | 184 | 191 | 190 | 189 | 188 | 194 | 193 | 191 | 190 |
| JBR | 129 | 190 | 153 | 151 | 149 | 131 | 130 | 129 | 145 | 129 | 148 | 147 | 146 | 145 | 142 | 141 | 140 | 139 | 142 | 141 | 140 | 139 | 140 | 139 | 138 | 137 |

