# 📊 DummyWHIR

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimates are indicative (1 KiB = 1024 bytes)

## zkVM Overview

| Metric | Value | Relevant circuit | Notes |
| --- | --- | --- | --- |
| Final bits of security | **128 bits** | [riscv](#riscv) | Regime: JBR |
| Final proof size (worst case) | **1193 KiB** | [embed](#embed) | |

## Circuits

- [riscv](#riscv)
- [convert](#convert)
- [combine](#combine)
- [embed](#embed)

## riscv

**Parameters:**
- Proof system: DEEP-ALI
- PCS: WHIR
- Hash size (bits): 256
- Field: Goldilocks³
- Iterations (M): 5
- Folding factors (k_i): [4, 4, 4, 4, 4]
- Constraint degree: 8
- Batch size: 200
- Batching: Powers
- Queries per iteration: [55, 31, 22, 17, 14]
- OOD samples per iteration: [1, 1, 1, 1]
- Total grinding overhead log2: 24.16
- Number of constraints: 500
- Lookup (logup): keccak
- Lookup (logup): poseidon2
- Lookup (logup): range_check_16
- Lookup (logup): bus

**Proof Size:** 1475 KiB (expected) / 1500 KiB (worst case)

| regime | total | keccak | poseidon2 | range_check_16 | bus | ALI | DEEP | OOD(i=1) | OOD(i=2) | OOD(i=3) | OOD(i=4) | Shift(i=1) | Shift(i=2) | Shift(i=3) | Shift(i=4) | batching | fin | fold(i=0,s=1) | fold(i=0,s=2) | fold(i=0,s=3) | fold(i=0,s=4) | fold(i=1,s=1) | fold(i=1,s=2) | fold(i=1,s=3) | fold(i=1,s=4) | fold(i=2,s=1) | fold(i=2,s=2) | fold(i=2,s=3) | fold(i=2,s=4) | fold(i=3,s=1) | fold(i=3,s=2) | fold(i=3,s=3) | fold(i=3,s=4) | fold(i=4,s=1) | fold(i=4,s=2) | fold(i=4,s=3) | fold(i=4,s=4) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 30 | 164 | 165 | 166 | 168 | 183 | 167 | 174 | 178 | 182 | 186 | 72 | 52 | 41 | 35 | 180 | 30 | 184 | 183 | 182 | 181 | 183 | 182 | 181 | 180 | 187 | 186 | 185 | 184 | 190 | 189 | 188 | 187 | 194 | 192 | 191 | 190 |
| JBR | 128 | 164 | 165 | 166 | 168 | 173 | 158 | 149 | 147 | 145 | 143 | 131 | 130 | 129 | 129 | 145 | 128 | 149 | 148 | 147 | 146 | 143 | 142 | 141 | 140 | 143 | 142 | 141 | 140 | 141 | 140 | 139 | 138 | 141 | 140 | 139 | 138 |


## convert

**Parameters:**
- Proof system: DEEP-ALI
- PCS: WHIR
- Hash size (bits): 256
- Field: Goldilocks³
- Iterations (M): 5
- Folding factors (k_i): [4, 4, 4, 4, 4]
- Constraint degree: 4
- Batch size: 164
- Batching: Powers
- Queries per iteration: [55, 31, 22, 17, 14]
- OOD samples per iteration: [1, 1, 1, 1]
- Total grinding overhead log2: 24.16
- Number of constraints: 300
- Lookup (logup): memory

**Proof Size:** 1217 KiB (expected) / 1241 KiB (worst case)

| regime | total | memory | ALI | DEEP | OOD(i=1) | OOD(i=2) | OOD(i=3) | OOD(i=4) | Shift(i=1) | Shift(i=2) | Shift(i=3) | Shift(i=4) | batching | fin | fold(i=0,s=1) | fold(i=0,s=2) | fold(i=0,s=3) | fold(i=0,s=4) | fold(i=1,s=1) | fold(i=1,s=2) | fold(i=1,s=3) | fold(i=1,s=4) | fold(i=2,s=1) | fold(i=2,s=2) | fold(i=2,s=3) | fold(i=2,s=4) | fold(i=3,s=1) | fold(i=3,s=2) | fold(i=3,s=3) | fold(i=3,s=4) | fold(i=4,s=1) | fold(i=4,s=2) | fold(i=4,s=3) | fold(i=4,s=4) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 30 | 165 | 183 | 169 | 176 | 180 | 184 | 188 | 72 | 52 | 41 | 35 | 182 | 30 | 186 | 185 | 184 | 183 | 185 | 184 | 183 | 182 | 189 | 188 | 187 | 186 | 192 | 191 | 190 | 189 | 195 | 194 | 193 | 192 |
| JBR | 128 | 165 | 174 | 160 | 151 | 149 | 147 | 145 | 131 | 130 | 129 | 129 | 147 | 128 | 151 | 150 | 149 | 148 | 145 | 144 | 143 | 142 | 145 | 144 | 143 | 142 | 143 | 142 | 141 | 140 | 143 | 142 | 141 | 140 |


## combine

**Parameters:**
- Proof system: DEEP-ALI
- PCS: WHIR
- Hash size (bits): 256
- Field: Goldilocks³
- Iterations (M): 4
- Folding factors (k_i): [4, 4, 4, 4]
- Constraint degree: 4
- Batch size: 164
- Batching: Powers
- Queries per iteration: [55, 31, 22, 17]
- OOD samples per iteration: [1, 1, 1]
- Total grinding overhead log2: 23.64
- Number of constraints: 300
- Lookup (logup): memory

**Proof Size:** 1199 KiB (expected) / 1221 KiB (worst case)

| regime | total | memory | ALI | DEEP | OOD(i=1) | OOD(i=2) | OOD(i=3) | Shift(i=1) | Shift(i=2) | Shift(i=3) | batching | fin | fold(i=0,s=1) | fold(i=0,s=2) | fold(i=0,s=3) | fold(i=0,s=4) | fold(i=1,s=1) | fold(i=1,s=2) | fold(i=1,s=3) | fold(i=1,s=4) | fold(i=2,s=1) | fold(i=2,s=2) | fold(i=2,s=3) | fold(i=2,s=4) | fold(i=3,s=1) | fold(i=3,s=2) | fold(i=3,s=3) | fold(i=3,s=4) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 35 | 167 | 183 | 171 | 178 | 182 | 186 | 72 | 52 | 41 | 184 | 35 | 188 | 187 | 186 | 185 | 187 | 186 | 185 | 184 | 191 | 190 | 189 | 188 | 194 | 193 | 191 | 190 |
| JBR | 129 | 167 | 174 | 162 | 153 | 151 | 149 | 131 | 130 | 129 | 149 | 129 | 153 | 152 | 151 | 150 | 147 | 146 | 145 | 144 | 147 | 146 | 145 | 144 | 145 | 144 | 143 | 142 |


## embed

**Parameters:**
- Proof system: DEEP-ALI
- PCS: WHIR
- Hash size (bits): 256
- Field: Goldilocks³
- Iterations (M): 3
- Folding factors (k_i): [4, 4, 4]
- Constraint degree: 4
- Batch size: 164
- Batching: Powers
- Queries per iteration: [55, 31, 22]
- OOD samples per iteration: [1, 1]
- Total grinding overhead log2: 23.49
- Number of constraints: 300
- Lookup (logup): memory

**Proof Size:** 1173 KiB (expected) / 1193 KiB (worst case)

| regime | total | memory | ALI | DEEP | OOD(i=1) | OOD(i=2) | Shift(i=1) | Shift(i=2) | batching | fin | fold(i=0,s=1) | fold(i=0,s=2) | fold(i=0,s=3) | fold(i=0,s=4) | fold(i=1,s=1) | fold(i=1,s=2) | fold(i=1,s=3) | fold(i=1,s=4) | fold(i=2,s=1) | fold(i=2,s=2) | fold(i=2,s=3) | fold(i=2,s=4) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 41 | 170 | 183 | 175 | 182 | 186 | 72 | 52 | 188 | 41 | 192 | 191 | 190 | 189 | 191 | 190 | 189 | 188 | 195 | 194 | 192 | 191 |
| JBR | 129 | 170 | 174 | 166 | 157 | 155 | 131 | 130 | 153 | 129 | 157 | 156 | 155 | 154 | 151 | 150 | 149 | 148 | 151 | 150 | 149 | 148 |

