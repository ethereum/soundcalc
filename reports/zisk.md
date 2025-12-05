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
- [ArithEq Compressor](#aritheq-compressor)
- [ArithEq384 Compressor](#aritheq384-compressor)
- [Keccakf Compressor](#keccakf-compressor)
- [Sha256f Compressor](#sha256f-compressor)
- [VirtualTable1 Compressor](#virtualtable1-compressor)
- [Recursive1](#recursive1)
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
- Batching: Powers

**Proof Size Estimate:** 886 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 186 | 167 | 163 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 49 | 185 | 166 | 49 | 75 | 99 | 123 | 142 | 160 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 628 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 190 | 168 | 164 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 51 | 189 | 167 | 51 | 75 | 99 | 123 | 142 | 160 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 694 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 188 | 167 | 164 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 50 | 186 | 166 | 50 | 75 | 99 | 123 | 142 | 160 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 582 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 188 | 168 | 165 | 170 | 174 | 178 | 181 | 184 | 53 |
| JBR | 57 | 187 | 167 | 57 | 81 | 105 | 124 | 142 | 160 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 630 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 188 | 168 | 165 | 170 | 174 | 178 | 181 | 184 | 53 |
| JBR | 56 | 187 | 167 | 56 | 81 | 105 | 124 | 142 | 160 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 822 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 187 | 168 | 164 | 170 | 174 | 178 | 181 | 184 | 53 |
| JBR | 55 | 185 | 167 | 55 | 81 | 105 | 124 | 142 | 160 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 670 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 187 | 167 | 164 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 50 | 186 | 166 | 50 | 75 | 99 | 123 | 142 | 160 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 628 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 188 | 167 | 164 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 51 | 187 | 166 | 51 | 75 | 99 | 123 | 142 | 160 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 658 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 188 | 167 | 164 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 51 | 186 | 166 | 51 | 75 | 99 | 123 | 142 | 160 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 852 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 186 | 168 | 164 | 170 | 174 | 178 | 181 | 184 | 53 |
| JBR | 55 | 185 | 167 | 55 | 81 | 105 | 124 | 142 | 160 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 814 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 186 | 167 | 163 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 49 | 185 | 166 | 49 | 75 | 99 | 123 | 142 | 160 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 628 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 188 | 167 | 164 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 51 | 187 | 166 | 51 | 75 | 99 | 123 | 142 | 160 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 760 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 187 | 167 | 163 | 169 | 173 | 177 | 181 | 184 | 53 |
| JBR | 50 | 185 | 166 | 50 | 75 | 99 | 123 | 142 | 160 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 878 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 186 | 169 | 164 | 171 | 175 | 179 | 183 | 53 |
| JBR | 61 | 185 | 168 | 61 | 87 | 111 | 135 | 159 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 3068 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 186 | 169 | 162 | 171 | 175 | 179 | 183 | 53 |
| JBR | 58 | 185 | 168 | 58 | 87 | 111 | 135 | 159 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 3680 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 186 | 169 | 161 | 171 | 175 | 179 | 183 | 53 |
| JBR | 58 | 185 | 168 | 58 | 87 | 111 | 135 | 159 | 63 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## Keccakf

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 128
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{16}$
- FRI rounds: 3
- FRI folding factors: [16, 16, 16]
- FRI early stop degree: 32
- Batching: Powers

**Proof Size Estimate:** 24694 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 180 | 173 | 163 | 175 | 179 | 183 | 53 |
| JBR | 63 | 179 | 172 | 79 | 111 | 135 | 159 | 63 |
| best attack | 128 | — | — | — | — | — | — | — |


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
- Batching: Powers

**Proof Size Estimate:** 7942 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 185 | 171 | 162 | 173 | 177 | 181 | 184 | 53 |
| JBR | 63 | 184 | 170 | 69 | 99 | 123 | 142 | 160 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 992 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 185 | 169 | 164 | 171 | 175 | 179 | 183 | 53 |
| JBR | 61 | 184 | 168 | 61 | 87 | 111 | 135 | 159 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 1238 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 185 | 169 | 163 | 171 | 175 | 179 | 183 | 53 |
| JBR | 60 | 183 | 168 | 60 | 87 | 111 | 135 | 159 | 63 |
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
- Batching: Powers

**Proof Size Estimate:** 1508 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 184 | 169 | 163 | 171 | 175 | 179 | 183 | 53 |
| JBR | 60 | 183 | 168 | 60 | 87 | 111 | 135 | 159 | 63 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## ArithEq Compressor

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
- Batching: Powers

**Proof Size Estimate:** 916 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 43 | 185 | 171 | 164 | 172 | 176 | 180 | 184 | 43 |
| JBR | 63 | 184 | 170 | 66 | 94 | 118 | 142 | 161 | 63 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## ArithEq384 Compressor

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
- Batching: Powers

**Proof Size Estimate:** 916 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 43 | 185 | 171 | 164 | 172 | 176 | 180 | 184 | 43 |
| JBR | 63 | 184 | 170 | 66 | 94 | 118 | 142 | 161 | 63 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## Keccakf Compressor

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 64
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{21}$
- FRI rounds: 5
- FRI folding factors: [16, 16, 16, 8, 8]
- FRI early stop degree: 32
- Batching: Powers

**Proof Size Estimate:** 974 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 43 | 185 | 168 | 161 | 169 | 173 | 177 | 181 | 184 | 43 |
| JBR | 48 | 184 | 167 | 48 | 76 | 100 | 124 | 143 | 161 | 63 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |


## Sha256f Compressor

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
- Batching: Powers

**Proof Size Estimate:** 946 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 43 | 185 | 170 | 163 | 171 | 175 | 179 | 183 | 43 |
| JBR | 60 | 184 | 169 | 60 | 88 | 112 | 136 | 160 | 63 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## VirtualTable1 Compressor

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
- Batching: Powers

**Proof Size Estimate:** 916 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 43 | 185 | 171 | 164 | 172 | 176 | 180 | 184 | 43 |
| JBR | 63 | 184 | 170 | 66 | 94 | 118 | 142 | 161 | 63 |
| best attack | 128 | — | — | — | — | — | — | — | — |


## Recursive1

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
- Batching: Powers

**Proof Size Estimate:** 625 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 35 | 185 | 172 | 164 | 172 | 176 | 180 | 184 | 35 |
| JBR | 64 | 184 | 171 | 67 | 95 | 119 | 143 | 162 | 64 |
| best attack | 129 | — | — | — | — | — | — | — | — |


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
- Batching: Powers

**Proof Size Estimate:** 625 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 35 | 185 | 172 | 164 | 172 | 176 | 180 | 184 | 35 |
| JBR | 64 | 184 | 171 | 67 | 95 | 119 | 143 | 162 | 64 |
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
- Batching: Powers

**Proof Size Estimate:** 449 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 29 | 185 | 173 | 164 | 172 | 177 | 29 |
| JBR | 63 | 184 | 172 | 68 | 101 | 131 | 63 |
| best attack | 128 | — | — | — | — | — | — |

