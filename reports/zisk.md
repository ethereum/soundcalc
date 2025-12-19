# 📊 ZisK

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimate is only indicative

## zkEVM Overview

| Metric | Value |
| --- | --- |
| Final proof size | **282.0 KiB** (circuit: Final) |
| Final bits of security | **128** (JBR, circuit: Main) |

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
- [SpecifiedRanges](#specifiedranges)
- [VirtualTable0](#virtualtable0)
- [VirtualTable1](#virtualtable1)
- [ArithEq-compressor](#aritheq-compressor)
- [ArithEq384-compressor](#aritheq384-compressor)
- [Keccakf-compressor](#keccakf-compressor)
- [Sha256f-compressor](#sha256f-compressor)
- [Recursive2](#recursive2)
- [Final](#final)

## Main

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of columns: 146
- Batch size: 61
- Batching: Powers

**Proof Size Estimate:** 1292.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 184 | 167 | 163 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 178 | 161 | 128 | 134 | 137 | 140 | 143 | 146 | 149 | 128 |


## Rom

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of columns: 3
- Batch size: 18
- Batching: Powers

**Proof Size Estimate:** 1056.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 190 | 168 | 164 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 183 | 161 | 128 | 132 | 135 | 138 | 141 | 144 | 147 | 128 |


## Mem

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of columns: 34
- Batch size: 29
- Batching: Powers

**Proof Size Estimate:** 1120.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 186 | 167 | 164 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 179 | 161 | 128 | 133 | 136 | 139 | 142 | 145 | 148 | 128 |


## RomData

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Number of columns: 23
- Batch size: 19
- Batching: Powers

**Proof Size Estimate:** 997.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 187 | 168 | 165 | 170 | 173 | 176 | 179 | 182 | 185 | 111 |
| JBR | 128 | 180 | 161 | 128 | 132 | 135 | 138 | 141 | 144 | 147 | 128 |


## InputData

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Number of columns: 26
- Batch size: 27
- Batching: Powers

**Proof Size Estimate:** 1040.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 187 | 168 | 165 | 170 | 173 | 176 | 179 | 182 | 185 | 111 |
| JBR | 128 | 180 | 161 | 128 | 133 | 136 | 139 | 142 | 145 | 148 | 128 |


## MemAlign

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Number of columns: 40
- Batch size: 59
- Batching: Powers

**Proof Size Estimate:** 1217.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 186 | 168 | 164 | 170 | 173 | 176 | 179 | 182 | 185 | 111 |
| JBR | 128 | 179 | 162 | 128 | 134 | 137 | 140 | 143 | 146 | 149 | 128 |


## MemAlignByte

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of columns: 16
- Batch size: 25
- Batching: Powers

**Proof Size Estimate:** 1093.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 187 | 167 | 164 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 180 | 160 | 128 | 132 | 135 | 138 | 141 | 144 | 147 | 128 |


## MemAlignReadByte

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of columns: 10
- Batch size: 18
- Batching: Powers

**Proof Size Estimate:** 1056.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 188 | 167 | 164 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 181 | 160 | 128 | 132 | 135 | 138 | 141 | 144 | 147 | 128 |


## MemAlignWriteByte

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of columns: 15
- Batch size: 23
- Batching: Powers

**Proof Size Estimate:** 1082.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 188 | 167 | 164 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 181 | 160 | 128 | 132 | 135 | 138 | 141 | 144 | 147 | 128 |


## Arith

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Number of columns: 65
- Batch size: 64
- Batching: Powers

**Proof Size Estimate:** 1244.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 185 | 168 | 164 | 170 | 173 | 176 | 179 | 182 | 185 | 111 |
| JBR | 128 | 179 | 162 | 128 | 134 | 137 | 140 | 143 | 146 | 149 | 128 |


## Binary

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of columns: 14
- Batch size: 49
- Batching: Powers

**Proof Size Estimate:** 1227.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 188 | 167 | 163 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 181 | 161 | 128 | 133 | 136 | 139 | 142 | 145 | 148 | 128 |


## BinaryAdd

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of columns: 9
- Batch size: 18
- Batching: Powers

**Proof Size Estimate:** 1056.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 188 | 167 | 164 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 181 | 160 | 128 | 132 | 135 | 138 | 141 | 144 | 147 | 128 |


## BinaryExtension

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of columns: 8
- Batch size: 40
- Batching: Powers

**Proof Size Estimate:** 1179.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 188 | 167 | 163 | 169 | 172 | 175 | 178 | 181 | 184 | 111 |
| JBR | 128 | 182 | 161 | 128 | 133 | 136 | 139 | 142 | 145 | 148 | 128 |


## Add256

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 64
- Number of columns: 36
- Batch size: 69
- Batching: Powers

**Proof Size Estimate:** 1165.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 186 | 169 | 164 | 171 | 174 | 177 | 180 | 183 | 111 |
| JBR | 128 | 179 | 162 | 128 | 134 | 137 | 140 | 143 | 146 | 128 |


## ArithEq

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 231
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 64
- Number of columns: 93
- Batch size: 434
- Batching: Powers

**Proof Size Estimate:** 3151.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 185 | 169 | 162 | 171 | 174 | 177 | 180 | 183 | 111 |
| JBR | 128 | 178 | 163 | 128 | 137 | 140 | 143 | 146 | 149 | 128 |


## ArithEq384

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 232
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 64
- Number of columns: 76
- Batch size: 536
- Batching: Powers

**Proof Size Estimate:** 3720.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 112 | 185 | 169 | 161 | 171 | 174 | 177 | 180 | 183 | 112 |
| JBR | 128 | 179 | 163 | 128 | 137 | 140 | 143 | 146 | 149 | 128 |


## Keccakf

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 217
- Grinding (bits): 23
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{17}$
- FRI rounds: 4
- FRI folding factors: [8, 8, 8, 8]
- FRI early stop degree: 64
- Number of columns: 2432
- Batch size: 4065
- Batching: Powers

**Proof Size Estimate:** 21244.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 113 | 180 | 172 | 162 | 174 | 177 | 180 | 183 | 113 |
| JBR | 128 | 174 | 166 | 128 | 140 | 143 | 146 | 149 | 128 |


## Sha256f

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 231
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{18}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Number of columns: 115
- Batch size: 1265
- Batching: Powers

**Proof Size Estimate:** 7549.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 185 | 171 | 162 | 173 | 176 | 179 | 182 | 185 | 111 |
| JBR | 128 | 178 | 165 | 128 | 138 | 141 | 144 | 147 | 150 | 128 |


## SpecifiedRanges

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 64
- Number of columns: 18
- Batch size: 88
- Batching: Powers

**Proof Size Estimate:** 1267.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 187 | 169 | 164 | 171 | 174 | 177 | 180 | 183 | 111 |
| JBR | 128 | 180 | 162 | 128 | 134 | 137 | 140 | 143 | 146 | 128 |


## VirtualTable0

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Number of columns: 6
- Batch size: 69
- Batching: Powers

**Proof Size Estimate:** 1270.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 189 | 168 | 163 | 170 | 173 | 176 | 179 | 182 | 185 | 111 |
| JBR | 128 | 182 | 162 | 128 | 134 | 137 | 140 | 143 | 146 | 149 | 128 |


## VirtualTable1

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Number of columns: 6
- Batch size: 90
- Batching: Powers

**Proof Size Estimate:** 1384.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 189 | 168 | 163 | 170 | 173 | 176 | 179 | 182 | 185 | 111 |
| JBR | 128 | 182 | 162 | 128 | 134 | 137 | 140 | 143 | 146 | 150 | 128 |


## ArithEq-compressor

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 110
- Grinding (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{18}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of columns: 179
- Batch size: 198
- Batching: Powers

**Proof Size Estimate:** 871.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 94 | 184 | 171 | 164 | 172 | 175 | 178 | 181 | 184 | 94 |
| JBR | 128 | 176 | 163 | 128 | 135 | 138 | 141 | 144 | 147 | 128 |


## ArithEq384-compressor

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 110
- Grinding (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{18}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of columns: 179
- Batch size: 198
- Batching: Powers

**Proof Size Estimate:** 871.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 94 | 184 | 171 | 164 | 172 | 175 | 178 | 181 | 184 | 94 |
| JBR | 128 | 176 | 163 | 128 | 135 | 138 | 141 | 144 | 147 | 128 |


## Keccakf-compressor

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 110
- Grinding (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{20}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Number of columns: 179
- Batch size: 198
- Batching: Powers

**Proof Size Estimate:** 940.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 94 | 184 | 169 | 162 | 170 | 173 | 176 | 179 | 182 | 185 | 94 |
| JBR | 128 | 177 | 162 | 128 | 136 | 139 | 142 | 145 | 148 | 151 | 128 |


## Sha256f-compressor

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 110
- Grinding (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{19}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 64
- Number of columns: 179
- Batch size: 198
- Batching: Powers

**Proof Size Estimate:** 892.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 94 | 184 | 170 | 163 | 171 | 174 | 177 | 180 | 183 | 94 |
| JBR | 128 | 176 | 162 | 128 | 135 | 138 | 141 | 144 | 147 | 128 |


## Recursive2

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 73
- Grinding (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.125
- Trace length (H): $2^{17}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Number of columns: 158
- Batch size: 145
- Batching: Powers

**Proof Size Estimate:** 487.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 80 | 184 | 171 | 164 | 172 | 175 | 178 | 181 | 184 | 80 |
| JBR | 128 | 176 | 163 | 128 | 135 | 138 | 141 | 144 | 147 | 128 |


## Final

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 43
- Grinding (bits): 22
- Field: Goldilocks³
- Rate (ρ): 0.03125
- Trace length (H): $2^{16}$
- FRI rounds: 3
- FRI folding factors: [16, 16, 16]
- FRI early stop degree: 512
- Number of columns: 160
- Batch size: 152
- Batching: Powers

**Proof Size Estimate:** 282.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 63 | 184 | 172 | 163 | 171 | 175 | 179 | 63 |
| JBR | 128 | 174 | 163 | 128 | 135 | 139 | 143 | 128 |

