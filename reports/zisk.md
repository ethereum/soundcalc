# 📊 ZisK

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimate is only indicative

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
- [VirtualTable0-compressor](#virtualtable0-compressor)
- [VirtualTable1-compressor](#virtualtable1-compressor)
- [Recursive2](#recursive2)
- [Final](#final)

## Main

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
- Number of columns: 51
- Batch size: 61
- Batching: Powers

**Proof Size Estimate:** 699.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 186 | 167 | 163 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 62 | 179 | 161 | 128 | 134 | 138 | 142 | 146 | 149 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |


## Rom

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
- Number of columns: 5
- Batch size: 18
- Batching: Powers

**Proof Size Estimate:** 570.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 189 | 168 | 164 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 62 | 183 | 161 | 130 | 134 | 138 | 142 | 146 | 149 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |


## Mem

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
- Number of columns: 20
- Batch size: 29
- Batching: Powers

**Proof Size Estimate:** 603.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 187 | 167 | 164 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 62 | 181 | 161 | 129 | 134 | 138 | 142 | 146 | 149 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |


## RomData

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 128
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 5
- FRI folding factors: [16, 16, 8, 8, 8]
- FRI early stop degree: 32
- Number of columns: 13
- Batch size: 19
- Batching: Powers

**Proof Size Estimate:** 537.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 188 | 168 | 165 | 170 | 174 | 178 | 181 | 184 | 53 |
| JBR | 62 | 181 | 162 | 131 | 135 | 139 | 143 | 146 | 149 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |


## InputData

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 128
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 5
- FRI folding factors: [16, 16, 8, 8, 8]
- FRI early stop degree: 32
- Number of columns: 19
- Batch size: 27
- Batching: Powers

**Proof Size Estimate:** 561.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 187 | 168 | 165 | 170 | 174 | 178 | 181 | 184 | 53 |
| JBR | 62 | 181 | 162 | 131 | 135 | 139 | 143 | 146 | 149 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |


## MemAlign

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 128
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 5
- FRI folding factors: [16, 16, 8, 8, 8]
- FRI early stop degree: 32
- Number of columns: 39
- Batch size: 59
- Batching: Powers

**Proof Size Estimate:** 657.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 186 | 168 | 164 | 170 | 174 | 178 | 181 | 184 | 53 |
| JBR | 62 | 180 | 162 | 129 | 135 | 139 | 143 | 146 | 149 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |


## MemAlignByte

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
- Number of columns: 23
- Batch size: 25
- Batching: Powers

**Proof Size Estimate:** 591.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 187 | 167 | 164 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 62 | 180 | 161 | 130 | 134 | 138 | 142 | 146 | 149 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |


## MemAlignReadByte

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
- Number of columns: 16
- Batch size: 18
- Batching: Powers

**Proof Size Estimate:** 570.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 187 | 167 | 164 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 62 | 181 | 161 | 130 | 134 | 138 | 142 | 146 | 149 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |


## MemAlignWriteByte

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
- Number of columns: 21
- Batch size: 23
- Batching: Powers

**Proof Size Estimate:** 585.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 187 | 167 | 164 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 62 | 180 | 161 | 130 | 134 | 138 | 142 | 146 | 149 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |


## Arith

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 128
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 5
- FRI folding factors: [16, 16, 8, 8, 8]
- FRI early stop degree: 32
- Number of columns: 62
- Batch size: 64
- Batching: Powers

**Proof Size Estimate:** 672.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 186 | 168 | 164 | 170 | 174 | 178 | 181 | 184 | 53 |
| JBR | 62 | 179 | 162 | 129 | 135 | 139 | 143 | 146 | 149 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |


## Binary

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
- Number of columns: 47
- Batch size: 49
- Batching: Powers

**Proof Size Estimate:** 663.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 186 | 167 | 163 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 62 | 179 | 161 | 129 | 134 | 138 | 142 | 146 | 149 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |


## BinaryAdd

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
- Number of columns: 16
- Batch size: 18
- Batching: Powers

**Proof Size Estimate:** 570.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 187 | 167 | 164 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 62 | 181 | 161 | 130 | 134 | 138 | 142 | 146 | 149 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |


## BinaryExtension

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
- Number of columns: 38
- Batch size: 40
- Batching: Powers

**Proof Size Estimate:** 636.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 186 | 167 | 163 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 62 | 180 | 161 | 129 | 134 | 138 | 142 | 146 | 149 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |


## Add256

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 128
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 32
- Number of columns: 67
- Batch size: 69
- Batching: Powers

**Proof Size Estimate:** 659.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 185 | 169 | 164 | 171 | 175 | 179 | 183 | 53 |
| JBR | 62 | 179 | 163 | 130 | 136 | 140 | 144 | 148 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## ArithEq

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 128
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 32
- Number of columns: 57
- Batch size: 434
- Batching: Powers

**Proof Size Estimate:** 1754.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 186 | 169 | 162 | 171 | 175 | 179 | 183 | 53 |
| JBR | 62 | 179 | 163 | 128 | 136 | 140 | 144 | 148 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## ArithEq384

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 128
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 32
- Number of columns: 51
- Batch size: 536
- Batching: Powers

**Proof Size Estimate:** 2060.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 186 | 169 | 161 | 171 | 175 | 179 | 183 | 53 |
| JBR | 62 | 179 | 163 | 127 | 136 | 140 | 144 | 148 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## Keccakf

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 128
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 5
- FRI folding factors: [16, 16, 8, 8, 8]
- FRI early stop degree: 32
- Number of columns: 71
- Batch size: 265
- Batching: Powers

**Proof Size Estimate:** 1275.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 185 | 168 | 161 | 170 | 174 | 178 | 181 | 184 | 53 |
| JBR | 62 | 179 | 162 | 127 | 135 | 139 | 143 | 146 | 149 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |


## Sha256f

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 128
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{18}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 8, 8]
- FRI early stop degree: 32
- Number of columns: 113
- Batch size: 1265
- Batching: Powers

**Proof Size Estimate:** 4171.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 185 | 171 | 162 | 173 | 177 | 181 | 184 | 53 |
| JBR | 62 | 178 | 165 | 128 | 138 | 142 | 146 | 149 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## SpecifiedRanges

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 128
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 32
- Number of columns: 86
- Batch size: 88
- Batching: Powers

**Proof Size Estimate:** 716.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 185 | 169 | 164 | 171 | 175 | 179 | 183 | 53 |
| JBR | 62 | 178 | 163 | 130 | 136 | 140 | 144 | 148 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## VirtualTable0

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 128
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 32
- Number of columns: 137
- Batch size: 139
- Batching: Powers

**Proof Size Estimate:** 869.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 184 | 169 | 163 | 171 | 175 | 179 | 183 | 53 |
| JBR | 62 | 178 | 163 | 129 | 136 | 140 | 144 | 148 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## VirtualTable1

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 128
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 32
- Number of columns: 172
- Batch size: 174
- Batching: Powers

**Proof Size Estimate:** 974.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 184 | 169 | 163 | 171 | 175 | 179 | 183 | 53 |
| JBR | 62 | 177 | 163 | 129 | 136 | 140 | 144 | 148 | 62 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## ArithEq-compressor

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 64
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{18}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 8]
- FRI early stop degree: 32
- Number of columns: 119
- Batch size: 163
- Batching: Powers

**Proof Size Estimate:** 450.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 43 | 185 | 171 | 164 | 172 | 176 | 180 | 184 | 43 |
| JBR | 63 | 177 | 163 | 128 | 136 | 140 | 144 | 148 | 63 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## ArithEq384-compressor

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 64
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{18}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 8]
- FRI early stop degree: 32
- Number of columns: 119
- Batch size: 163
- Batching: Powers

**Proof Size Estimate:** 450.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 43 | 185 | 171 | 164 | 172 | 176 | 180 | 184 | 43 |
| JBR | 63 | 177 | 163 | 128 | 136 | 140 | 144 | 148 | 63 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## Keccakf-compressor

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 64
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{18}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 8]
- FRI early stop degree: 32
- Number of columns: 119
- Batch size: 163
- Batching: Powers

**Proof Size Estimate:** 450.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 43 | 185 | 171 | 164 | 172 | 176 | 180 | 184 | 43 |
| JBR | 63 | 177 | 163 | 128 | 136 | 140 | 144 | 148 | 63 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## Sha256f-compressor

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 64
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{19}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 32
- Number of columns: 119
- Batch size: 163
- Batching: Powers

**Proof Size Estimate:** 470.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 43 | 185 | 170 | 163 | 171 | 175 | 179 | 183 | 43 |
| JBR | 63 | 177 | 162 | 127 | 135 | 139 | 143 | 147 | 63 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## VirtualTable0-compressor

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 64
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{18}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 8]
- FRI early stop degree: 32
- Number of columns: 119
- Batch size: 163
- Batching: Powers

**Proof Size Estimate:** 450.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 43 | 185 | 171 | 164 | 172 | 176 | 180 | 184 | 43 |
| JBR | 63 | 177 | 163 | 128 | 136 | 140 | 144 | 148 | 63 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## VirtualTable1-compressor

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 64
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{18}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 8]
- FRI early stop degree: 32
- Number of columns: 119
- Batch size: 163
- Batching: Powers

**Proof Size Estimate:** 450.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 43 | 185 | 171 | 164 | 172 | 176 | 180 | 184 | 43 |
| JBR | 63 | 177 | 163 | 128 | 136 | 140 | 144 | 148 | 63 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## Recursive2

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 43
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.125
- Trace length (H): $2^{17}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 8]
- FRI early stop degree: 32
- Number of columns: 92
- Batch size: 136
- Batching: Powers

**Proof Size Estimate:** 275.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 35 | 185 | 171 | 164 | 172 | 176 | 180 | 184 | 35 |
| JBR | 63 | 176 | 163 | 127 | 134 | 138 | 142 | 147 | 63 |
| best attack | 129 | — | — | — | — | — | — | — | — |


## Final

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 32
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.0625
- Trace length (H): $2^{16}$
- FRI rounds: 2
- FRI folding factors: [32, 32]
- FRI early stop degree: 1024
- Number of columns: 98
- Batch size: 142
- Batching: Powers

**Proof Size Estimate:** 201.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 29 | 185 | 172 | 164 | 172 | 177 | 29 |
| JBR | 63 | 175 | 163 | 126 | 133 | 138 | 63 |
| best attack | 128 | — | — | — | — | — | — |

