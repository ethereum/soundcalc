# 📊 ZisK

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimates are indicative (1 KiB = 1024 bytes)

## zkVM Overview

| Metric | Value | Relevant circuit | Notes |
| --- | --- | --- | --- |
| Final proof size (worst case) | **313 KiB** | [Final_Compressed](#final_compressed) | |
| Final bits of security | **128 bits** | [Main](#main) | Regime: JBR |

## Circuits

- [Main](#main)
- [Rom](#rom)
- [Mem](#mem)
- [RomData](#romdata)
- [InputData](#inputdata)
- [MemAlign](#memalign)
- [MemAlignByte](#memalignbyte)
- [MemAlignReadByte](#memalignreadbyte)
- [MemAlignWriteByte](#memalignwritebyte)
- [Arith](#arith)
- [Binary](#binary)
- [BinaryAdd](#binaryadd)
- [BinaryExtension](#binaryextension)
- [Add256](#add256)
- [ArithEq](#aritheq)
- [ArithEq384](#aritheq384)
- [Keccakf](#keccakf)
- [Sha256f](#sha256f)
- [Poseidon2](#poseidon2)
- [SpecifiedRanges](#specifiedranges)
- [VirtualTable0](#virtualtable0)
- [VirtualTable1](#virtualtable1)
- [ArithEq-compressor](#aritheq-compressor)
- [ArithEq384-compressor](#aritheq384-compressor)
- [Keccakf-compressor](#keccakf-compressor)
- [Sha256f-compressor](#sha256f-compressor)
- [SpecifiedRanges-compressor](#specifiedranges-compressor)
- [Recursive2](#recursive2)
- [Final](#final)
- [Final_Compressed](#final_compressed)

## Main

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of constraints: 146
- Batch size: 61
- Batching: Powers

**Proof Size:** 890 KiB (expected) / 1292 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 184 | 167 | 163 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 178 | 161 | 128 | 134 | 137 | 140 | 143 | 146 | 149 | 128 |


## Rom

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of constraints: 3
- Batch size: 18
- Batching: Powers

**Proof Size:** 656 KiB (expected) / 1056 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 190 | 168 | 164 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 183 | 161 | 128 | 132 | 135 | 138 | 141 | 144 | 147 | 128 |


## Mem

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of constraints: 34
- Batch size: 29
- Batching: Powers

**Proof Size:** 718 KiB (expected) / 1120 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 186 | 167 | 164 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 179 | 161 | 128 | 133 | 136 | 139 | 142 | 145 | 148 | 128 |


## RomData

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Number of constraints: 23
- Batch size: 19
- Batching: Powers

**Proof Size:** 603 KiB (expected) / 997 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 187 | 168 | 165 | 170 | 173 | 176 | 179 | 182 | 185 | 111 |
| JBR | 128 | 180 | 161 | 128 | 132 | 135 | 138 | 141 | 144 | 147 | 128 |


## InputData

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Number of constraints: 26
- Batch size: 27
- Batching: Powers

**Proof Size:** 646 KiB (expected) / 1040 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 187 | 168 | 165 | 170 | 173 | 176 | 179 | 182 | 185 | 111 |
| JBR | 128 | 180 | 161 | 128 | 133 | 136 | 139 | 142 | 145 | 148 | 128 |


## MemAlign

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Number of constraints: 40
- Batch size: 59
- Batching: Powers

**Proof Size:** 821 KiB (expected) / 1217 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 186 | 168 | 164 | 170 | 173 | 176 | 179 | 182 | 185 | 111 |
| JBR | 128 | 179 | 162 | 128 | 134 | 137 | 140 | 143 | 146 | 149 | 128 |


## MemAlignByte

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of constraints: 16
- Batch size: 25
- Batching: Powers

**Proof Size:** 694 KiB (expected) / 1093 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 187 | 167 | 164 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 180 | 160 | 128 | 132 | 135 | 138 | 141 | 144 | 147 | 128 |


## MemAlignReadByte

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of constraints: 10
- Batch size: 18
- Batching: Powers

**Proof Size:** 656 KiB (expected) / 1056 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 188 | 167 | 164 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 181 | 160 | 128 | 132 | 135 | 138 | 141 | 144 | 147 | 128 |


## MemAlignWriteByte

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of constraints: 15
- Batch size: 23
- Batching: Powers

**Proof Size:** 683 KiB (expected) / 1082 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 188 | 167 | 164 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 181 | 160 | 128 | 132 | 135 | 138 | 141 | 144 | 147 | 128 |


## Arith

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Number of constraints: 65
- Batch size: 64
- Batching: Powers

**Proof Size:** 848 KiB (expected) / 1244 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 185 | 168 | 164 | 170 | 173 | 176 | 179 | 182 | 185 | 111 |
| JBR | 128 | 179 | 162 | 128 | 134 | 137 | 140 | 143 | 146 | 149 | 128 |


## Binary

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of constraints: 14
- Batch size: 49
- Batching: Powers

**Proof Size:** 826 KiB (expected) / 1227 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 188 | 167 | 163 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 181 | 161 | 128 | 133 | 136 | 139 | 142 | 145 | 148 | 128 |


## BinaryAdd

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of constraints: 9
- Batch size: 18
- Batching: Powers

**Proof Size:** 656 KiB (expected) / 1056 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 188 | 167 | 164 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 181 | 160 | 128 | 132 | 135 | 138 | 141 | 144 | 147 | 128 |


## BinaryExtension

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of constraints: 8
- Batch size: 40
- Batching: Powers

**Proof Size:** 777 KiB (expected) / 1179 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 188 | 167 | 163 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 182 | 161 | 128 | 133 | 136 | 139 | 142 | 145 | 148 | 128 |


## Add256

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 64
- Number of constraints: 36
- Batch size: 69
- Batching: Powers

**Proof Size:** 816 KiB (expected) / 1165 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 186 | 169 | 164 | 171 | 174 | 177 | 180 | 183 | 111 |
| JBR | 128 | 179 | 162 | 128 | 134 | 137 | 140 | 143 | 146 | 128 |


## ArithEq

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 231
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 64
- Number of constraints: 93
- Batch size: 434
- Batching: Powers

**Proof Size:** 2799 KiB (expected) / 3151 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 185 | 169 | 162 | 171 | 174 | 177 | 180 | 183 | 111 |
| JBR | 128 | 178 | 163 | 128 | 137 | 140 | 143 | 146 | 149 | 128 |


## ArithEq384

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 232
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 64
- Number of constraints: 76
- Batch size: 536
- Batching: Powers

**Proof Size:** 3366 KiB (expected) / 3720 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 112 | 185 | 169 | 161 | 171 | 174 | 177 | 180 | 183 | 112 |
| JBR | 128 | 179 | 163 | 128 | 137 | 140 | 143 | 146 | 149 | 128 |


## Keccakf

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 217
- Grinding query phase (bits): 23
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{17}$
- FRI rounds: 4
- FRI folding factors: [8, 8, 8, 8]
- FRI early stop degree: 64
- Number of constraints: 2432
- Batch size: 4065
- Batching: Powers

**Proof Size:** 20975 KiB (expected) / 21244 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 113 | 180 | 172 | 162 | 174 | 177 | 180 | 183 | 113 |
| JBR | 128 | 174 | 166 | 128 | 140 | 143 | 146 | 149 | 128 |


## Sha256f

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 231
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{18}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Number of constraints: 115
- Batch size: 1265
- Batching: Powers

**Proof Size:** 7215 KiB (expected) / 7549 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 185 | 171 | 162 | 173 | 176 | 179 | 182 | 185 | 111 |
| JBR | 128 | 178 | 165 | 128 | 138 | 141 | 144 | 147 | 150 | 128 |


## Poseidon2

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 114
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{17}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Number of constraints: 85
- Batch size: 182
- Batching: Powers

**Proof Size:** 682 KiB (expected) / 832 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 93 | 185 | 172 | 165 | 173 | 176 | 179 | 182 | 185 | 93 |
| JBR | 128 | 177 | 164 | 128 | 135 | 138 | 141 | 144 | 148 | 128 |


## SpecifiedRanges

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 64
- Number of constraints: 16
- Batch size: 107
- Batching: Powers

**Proof Size:** 1020 KiB (expected) / 1369 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 187 | 169 | 164 | 171 | 174 | 177 | 180 | 183 | 111 |
| JBR | 128 | 180 | 162 | 128 | 134 | 137 | 140 | 143 | 146 | 128 |


## VirtualTable0

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Number of constraints: 6
- Batch size: 69
- Batching: Powers

**Proof Size:** 875 KiB (expected) / 1270 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 189 | 168 | 163 | 170 | 173 | 176 | 179 | 182 | 185 | 111 |
| JBR | 128 | 182 | 162 | 128 | 134 | 137 | 140 | 143 | 146 | 149 | 128 |


## VirtualTable1

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Number of constraints: 6
- Batch size: 90
- Batching: Powers

**Proof Size:** 989 KiB (expected) / 1384 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 189 | 168 | 163 | 170 | 173 | 176 | 179 | 182 | 185 | 111 |
| JBR | 128 | 182 | 162 | 128 | 134 | 137 | 140 | 143 | 146 | 150 | 128 |


## ArithEq-compressor

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 110
- Grinding query phase (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{18}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of constraints: 179
- Batch size: 198
- Batching: Powers

**Proof Size:** 726 KiB (expected) / 871 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 94 | 184 | 171 | 164 | 172 | 175 | 178 | 181 | 184 | 94 |
| JBR | 128 | 176 | 163 | 128 | 135 | 138 | 141 | 144 | 147 | 128 |


## ArithEq384-compressor

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 110
- Grinding query phase (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{18}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of constraints: 179
- Batch size: 198
- Batching: Powers

**Proof Size:** 726 KiB (expected) / 871 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 94 | 184 | 171 | 164 | 172 | 175 | 178 | 181 | 184 | 94 |
| JBR | 128 | 176 | 163 | 128 | 135 | 138 | 141 | 144 | 147 | 128 |


## Keccakf-compressor

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 110
- Grinding query phase (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{20}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Number of constraints: 179
- Batch size: 198
- Batching: Powers

**Proof Size:** 771 KiB (expected) / 940 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 94 | 184 | 169 | 162 | 170 | 173 | 176 | 179 | 182 | 185 | 94 |
| JBR | 128 | 177 | 162 | 128 | 136 | 139 | 142 | 145 | 148 | 151 | 128 |


## Sha256f-compressor

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 110
- Grinding query phase (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{19}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 64
- Number of constraints: 179
- Batch size: 198
- Batching: Powers

**Proof Size:** 743 KiB (expected) / 892 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 94 | 184 | 170 | 163 | 171 | 174 | 177 | 180 | 183 | 94 |
| JBR | 128 | 176 | 162 | 128 | 135 | 138 | 141 | 144 | 147 | 128 |


## SpecifiedRanges-compressor

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 110
- Grinding query phase (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{18}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of constraints: 179
- Batch size: 198
- Batching: Powers

**Proof Size:** 726 KiB (expected) / 871 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 94 | 184 | 171 | 164 | 172 | 175 | 178 | 181 | 184 | 94 |
| JBR | 128 | 176 | 163 | 128 | 135 | 138 | 141 | 144 | 147 | 128 |


## Recursive2

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 73
- Grinding query phase (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.125
- Trace length (H): $2^{17}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of constraints: 158
- Batch size: 145
- Batching: Powers

**Proof Size:** 398 KiB (expected) / 487 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 80 | 184 | 171 | 164 | 172 | 175 | 178 | 181 | 184 | 80 |
| JBR | 128 | 176 | 163 | 128 | 135 | 138 | 141 | 144 | 147 | 128 |


## Final

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 43
- Grinding query phase (bits): 22
- Field: Goldilocks³
- Rate (ρ): 0.03125
- Trace length (H): $2^{16}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 32
- Number of constraints: 160
- Batch size: 152
- Batching: Powers

**Proof Size:** 266 KiB (expected) / 305 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 63 | 184 | 172 | 163 | 171 | 175 | 179 | 183 | 63 |
| JBR | 128 | 174 | 163 | 128 | 135 | 139 | 143 | 147 | 128 |


## Final_Compressed

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 54
- Grinding query phase (bits): 22
- Field: Goldilocks³
- Rate (ρ): 0.0625
- Trace length (H): $2^{15}$
- FRI rounds: 3
- FRI folding factors: [8, 8, 8]
- FRI early stop degree: 1024
- Number of constraints: 158
- Batch size: 145
- Batching: Powers

**Proof Size:** 269 KiB (expected) / 313 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 71 | 184 | 173 | 165 | 173 | 176 | 179 | 71 |
| JBR | 128 | 175 | 164 | 129 | 136 | 139 | 142 | 128 |

