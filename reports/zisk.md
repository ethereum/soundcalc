# 📊 ZisK (v0.16.1)

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimates are indicative (1 KiB = 1024 bytes)

## zkVM Overview

| Metric | Value | Relevant circuit | Notes |
| --- | --- | --- | --- |
| Final bits of security | **128 bits** | [Dma](#dma) | Regime: JBR |
| Final proof size (worst case) | **313 KiB** | [Final_Compressed](#final_compressed) | |

## Circuits

- [Dma](#dma)
- [DmaMemCpy](#dmamemcpy)
- [DmaInputCpy](#dmainputcpy)
- [Dma64Aligned](#dma64aligned)
- [Dma64AlignedInputCpy](#dma64alignedinputcpy)
- [Dma64AlignedMemSet](#dma64alignedmemset)
- [Dma64AlignedMem](#dma64alignedmem)
- [Dma64AlignedMemCpy](#dma64alignedmemcpy)
- [DmaUnaligned](#dmaunaligned)
- [DmaPrePost](#dmaprepost)
- [DmaPrePostMemCpy](#dmaprepostmemcpy)
- [DmaPrePostInputCpy](#dmaprepostinputcpy)
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
- [Blake2br](#blake2br)
- [SpecifiedRanges](#specifiedranges)
- [VirtualTable0](#virtualtable0)
- [VirtualTable1](#virtualtable1)
- [DmaPrePost-compressor](#dmaprepost-compressor)
- [ArithEq-compressor](#aritheq-compressor)
- [ArithEq384-compressor](#aritheq384-compressor)
- [Keccakf-compressor](#keccakf-compressor)
- [Sha256f-compressor](#sha256f-compressor)
- [Blake2br-compressor](#blake2br-compressor)
- [Recursive2](#recursive2)
- [Final](#final)
- [Final_Compressed](#final_compressed)

## Dma

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 46
- Batching: Powers
- Number of constraints: 49
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[77]
- Lookup (logup): Lookup_gsum_[8001]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Permutation_gsum_[8000]
- Lookup (logup): Range Check_gsum_[102]
- Lookup (logup): Range Check_gsum_[103]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 748 KiB (expected) / 1142 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Lookup_gsum_[77] | Lookup_gsum_[8001] | Permutation_gsum_[10] | Permutation_gsum_[8000] | Range Check_gsum_[102] | Range Check_gsum_[103] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 169 | 168 | 168 | 166 | 170 | 169 | 169 | 186 | 168 | 166 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 166 | 169 | 168 | 168 | 166 | 170 | 169 | 169 | 179 | 161 | 133 | 138 | 141 | 144 | 147 | 150 | 154 | 128 |


## DmaMemCpy

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 33
- Batching: Powers
- Number of constraints: 22
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[77]
- Lookup (logup): Lookup_gsum_[8001]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Permutation_gsum_[8000]
- Lookup (logup): Range Check_gsum_[102]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 679 KiB (expected) / 1072 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Lookup_gsum_[77] | Lookup_gsum_[8001] | Permutation_gsum_[10] | Permutation_gsum_[8000] | Range Check_gsum_[102] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 169 | 168 | 168 | 166 | 170 | 169 | 187 | 168 | 166 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 166 | 169 | 168 | 168 | 166 | 170 | 169 | 180 | 161 | 133 | 138 | 141 | 144 | 147 | 150 | 153 | 128 |


## DmaInputCpy

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 27
- Batching: Powers
- Number of constraints: 20
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[8001]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Permutation_gsum_[8000]
- Lookup (logup): Range Check_gsum_[102]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[105]

**Proof Size:** 646 KiB (expected) / 1040 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Lookup_gsum_[8001] | Permutation_gsum_[10] | Permutation_gsum_[8000] | Range Check_gsum_[102] | Range Check_gsum_[104] | Range Check_gsum_[105] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 168 | 168 | 166 | 170 | 170 | 170 | 187 | 168 | 167 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 166 | 168 | 168 | 166 | 170 | 170 | 170 | 180 | 161 | 133 | 137 | 140 | 143 | 146 | 149 | 153 | 128 |


## Dma64Aligned

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 62
- Batching: Powers
- Number of constraints: 88
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Direct_gsum_[8200]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[102]
- Lookup (logup): Range Check_gsum_[103]

**Proof Size:** 838 KiB (expected) / 1233 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Direct_gsum_[8200] | Lookup_gsum_[5000] | Lookup_gsum_[88] | Permutation_gsum_[10] | Range Check_gsum_[102] | Range Check_gsum_[103] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 166 | 167 | 167 | 165 | 167 | 169 | 185 | 168 | 166 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 167 | 166 | 167 | 167 | 165 | 167 | 169 | 178 | 162 | 133 | 139 | 142 | 145 | 148 | 151 | 154 | 128 |


## Dma64AlignedInputCpy

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 44
- Batching: Powers
- Number of constraints: 52
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Direct_gsum_[8200]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[102]
- Lookup (logup): Range Check_gsum_[103]

**Proof Size:** 738 KiB (expected) / 1131 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Direct_gsum_[8200] | Lookup_gsum_[5000] | Lookup_gsum_[88] | Permutation_gsum_[10] | Range Check_gsum_[102] | Range Check_gsum_[103] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 166 | 167 | 167 | 166 | 167 | 169 | 186 | 168 | 166 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 167 | 166 | 167 | 167 | 166 | 167 | 169 | 179 | 161 | 133 | 138 | 141 | 144 | 147 | 150 | 154 | 128 |


## Dma64AlignedMemSet

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 30
- Batching: Powers
- Number of constraints: 62
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Direct_gsum_[8200]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[103]

**Proof Size:** 662 KiB (expected) / 1056 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Direct_gsum_[8200] | Lookup_gsum_[5000] | Permutation_gsum_[10] | Range Check_gsum_[103] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 166 | 167 | 165 | 169 | 186 | 168 | 167 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 167 | 166 | 167 | 165 | 169 | 178 | 161 | 133 | 138 | 141 | 144 | 147 | 150 | 153 | 128 |


## Dma64AlignedMem

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 46
- Batching: Powers
- Number of constraints: 81
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Direct_gsum_[8200]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[103]

**Proof Size:** 748 KiB (expected) / 1142 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Direct_gsum_[8200] | Lookup_gsum_[5000] | Permutation_gsum_[10] | Range Check_gsum_[103] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 166 | 167 | 165 | 169 | 185 | 168 | 166 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 167 | 166 | 167 | 165 | 169 | 178 | 161 | 133 | 138 | 141 | 144 | 147 | 150 | 154 | 128 |


## Dma64AlignedMemCpy

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 52
- Batching: Powers
- Number of constraints: 69
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Direct_gsum_[8200]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[103]

**Proof Size:** 781 KiB (expected) / 1174 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Direct_gsum_[8200] | Lookup_gsum_[5000] | Permutation_gsum_[10] | Range Check_gsum_[103] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 166 | 167 | 164 | 169 | 185 | 168 | 166 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 167 | 166 | 167 | 164 | 169 | 178 | 161 | 133 | 138 | 141 | 144 | 147 | 150 | 154 | 128 |


## DmaUnaligned

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 52
- Batching: Powers
- Number of constraints: 75
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Direct_gsum_[8201]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[103]

**Proof Size:** 781 KiB (expected) / 1174 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Direct_gsum_[8201] | Lookup_gsum_[5000] | Lookup_gsum_[88] | Permutation_gsum_[10] | Range Check_gsum_[103] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 165 | 167 | 167 | 166 | 169 | 185 | 168 | 166 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 167 | 165 | 167 | 167 | 166 | 169 | 178 | 161 | 133 | 138 | 141 | 144 | 147 | 150 | 154 | 128 |


## DmaPrePost

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 83
- Batching: Powers
- Number of constraints: 69
- Lookup (logup): Lookup_gsum_[8002]
- Lookup (logup): Lookup_gsum_[8003]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Permutation_gsum_[8000]

**Proof Size:** 951 KiB (expected) / 1346 KiB (worst case)

| regime | total | Lookup_gsum_[8002] | Lookup_gsum_[8003] | Lookup_gsum_[88] | Permutation_gsum_[10] | Permutation_gsum_[8000] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 168 | 169 | 166 | 166 | 167 | 185 | 168 | 165 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 168 | 169 | 166 | 166 | 167 | 179 | 162 | 133 | 139 | 142 | 145 | 148 | 151 | 155 | 128 |


## DmaPrePostMemCpy

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 70
- Batching: Powers
- Number of constraints: 38
- Lookup (logup): Lookup_gsum_[8002]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Permutation_gsum_[8000]

**Proof Size:** 881 KiB (expected) / 1276 KiB (worst case)

| regime | total | Lookup_gsum_[8002] | Lookup_gsum_[88] | Permutation_gsum_[10] | Permutation_gsum_[8000] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 168 | 166 | 166 | 167 | 186 | 168 | 165 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 168 | 166 | 166 | 167 | 179 | 162 | 133 | 139 | 142 | 145 | 148 | 151 | 154 | 128 |


## DmaPrePostInputCpy

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 44
- Batching: Powers
- Number of constraints: 20
- Lookup (logup): Lookup_gsum_[8002]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Permutation_gsum_[8000]

**Proof Size:** 738 KiB (expected) / 1131 KiB (worst case)

| regime | total | Lookup_gsum_[8002] | Lookup_gsum_[88] | Permutation_gsum_[10] | Permutation_gsum_[8000] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 168 | 166 | 167 | 167 | 187 | 168 | 166 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 168 | 166 | 167 | 167 | 180 | 161 | 133 | 138 | 141 | 144 | 147 | 150 | 154 | 128 |


## Main

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Batch size: 61
- Batching: Powers
- Number of constraints: 144
- Lookup (logup): Direct_gsum_[1000]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[7890]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[102]
- Lookup (logup): Range Check_gsum_[106]

**Proof Size:** 890 KiB (expected) / 1292 KiB (worst case)

| regime | total | Direct_gsum_[1000] | Lookup_gsum_[5000] | Lookup_gsum_[7890] | Permutation_gsum_[10] | Range Check_gsum_[102] | Range Check_gsum_[106] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 166 | 166 | 161 | 164 | 169 | 184 | 167 | 165 | 171 | 174 | 177 | 180 | 183 | 186 | 111 |
| JBR | 128 | 166 | 166 | 166 | 161 | 164 | 169 | 178 | 161 | 133 | 139 | 142 | 145 | 148 | 151 | 154 | 128 |


## Rom

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 221
- Grinding query phase (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Batch size: 18
- Batching: Powers
- Number of constraints: 3
- Lookup (logup): Lookup_gsum_[7890]

**Proof Size:** 635 KiB (expected) / 1019 KiB (worst case)

| regime | total | Lookup_gsum_[7890] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 190 | 168 | 166 | 171 | 174 | 177 | 180 | 183 | 186 | 111 |
| JBR | 128 | 166 | 183 | 161 | 133 | 137 | 140 | 143 | 146 | 149 | 152 | 128 |


## Mem

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Batch size: 29
- Batching: Powers
- Number of constraints: 34
- Lookup (logup): Direct_gsum_[11]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[102]
- Lookup (logup): Range Check_gsum_[103]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 718 KiB (expected) / 1120 KiB (worst case)

| regime | total | Direct_gsum_[11] | Permutation_gsum_[10] | Range Check_gsum_[102] | Range Check_gsum_[103] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 167 | 169 | 167 | 169 | 186 | 167 | 166 | 171 | 174 | 177 | 180 | 183 | 186 | 111 |
| JBR | 128 | 166 | 167 | 169 | 167 | 169 | 179 | 161 | 133 | 138 | 141 | 144 | 147 | 150 | 153 | 128 |


## RomData

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 19
- Batching: Powers
- Number of constraints: 23
- Lookup (logup): Direct_gsum_[11]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[102]

**Proof Size:** 603 KiB (expected) / 997 KiB (worst case)

| regime | total | Direct_gsum_[11] | Permutation_gsum_[10] | Range Check_gsum_[102] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 168 | 169 | 187 | 168 | 167 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 167 | 168 | 169 | 180 | 161 | 133 | 137 | 140 | 143 | 146 | 149 | 152 | 128 |


## InputData

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 27
- Batching: Powers
- Number of constraints: 30
- Lookup (logup): Direct_gsum_[11]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[102]
- Lookup (logup): Range Check_gsum_[103]

**Proof Size:** 646 KiB (expected) / 1040 KiB (worst case)

| regime | total | Direct_gsum_[11] | Permutation_gsum_[10] | Range Check_gsum_[102] | Range Check_gsum_[103] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 168 | 170 | 167 | 187 | 168 | 167 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 167 | 168 | 170 | 167 | 179 | 161 | 133 | 137 | 140 | 143 | 146 | 149 | 153 | 128 |


## MemAlign

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 59
- Batching: Powers
- Number of constraints: 40
- Lookup (logup): Lookup_gsum_[133]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[107]

**Proof Size:** 821 KiB (expected) / 1217 KiB (worst case)

| regime | total | Lookup_gsum_[133] | Permutation_gsum_[10] | Range Check_gsum_[107] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 168 | 168 | 167 | 186 | 168 | 166 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 168 | 168 | 167 | 179 | 162 | 133 | 139 | 142 | 145 | 148 | 151 | 154 | 128 |


## MemAlignByte

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Batch size: 25
- Batching: Powers
- Number of constraints: 16
- Lookup (logup): Direct_gsum_[10]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[103]
- Lookup (logup): Range Check_gsum_[107]

**Proof Size:** 694 KiB (expected) / 1093 KiB (worst case)

| regime | total | Direct_gsum_[10] | Lookup_gsum_[88] | Permutation_gsum_[10] | Range Check_gsum_[103] | Range Check_gsum_[107] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 168 | 165 | 169 | 169 | 187 | 167 | 166 | 171 | 174 | 177 | 180 | 183 | 186 | 111 |
| JBR | 128 | 166 | 168 | 165 | 169 | 169 | 180 | 160 | 133 | 137 | 140 | 143 | 146 | 149 | 152 | 128 |


## MemAlignReadByte

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Batch size: 18
- Batching: Powers
- Number of constraints: 10
- Lookup (logup): Direct_gsum_[10]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[103]

**Proof Size:** 656 KiB (expected) / 1056 KiB (worst case)

| regime | total | Direct_gsum_[10] | Lookup_gsum_[88] | Permutation_gsum_[10] | Range Check_gsum_[103] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 168 | 166 | 169 | 188 | 167 | 166 | 171 | 174 | 177 | 180 | 183 | 186 | 111 |
| JBR | 128 | 166 | 168 | 166 | 169 | 181 | 160 | 133 | 137 | 140 | 143 | 146 | 149 | 152 | 128 |


## MemAlignWriteByte

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Batch size: 23
- Batching: Powers
- Number of constraints: 15
- Lookup (logup): Direct_gsum_[10]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[103]
- Lookup (logup): Range Check_gsum_[107]

**Proof Size:** 683 KiB (expected) / 1082 KiB (worst case)

| regime | total | Direct_gsum_[10] | Lookup_gsum_[88] | Permutation_gsum_[10] | Range Check_gsum_[103] | Range Check_gsum_[107] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 168 | 165 | 169 | 169 | 188 | 167 | 166 | 171 | 174 | 177 | 180 | 183 | 186 | 111 |
| JBR | 128 | 166 | 168 | 165 | 169 | 169 | 181 | 160 | 133 | 137 | 140 | 143 | 146 | 149 | 152 | 128 |


## Arith

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 64
- Batching: Powers
- Number of constraints: 65
- Lookup (logup): Lookup_gsum_[330]
- Lookup (logup): Lookup_gsum_[331]
- Lookup (logup): Lookup_gsum_[5000]

**Proof Size:** 848 KiB (expected) / 1244 KiB (worst case)

| regime | total | Lookup_gsum_[330] | Lookup_gsum_[331] | Lookup_gsum_[5000] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 165 | 168 | 166 | 185 | 168 | 166 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 165 | 168 | 166 | 179 | 162 | 133 | 139 | 142 | 145 | 148 | 151 | 154 | 128 |


## Binary

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Batch size: 49
- Batching: Powers
- Number of constraints: 14
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Lookup_gsum_[125]
- Lookup (logup): Lookup_gsum_[5000]

**Proof Size:** 826 KiB (expected) / 1227 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Lookup_gsum_[125] | Lookup_gsum_[5000] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 164 | 166 | 188 | 167 | 165 | 171 | 174 | 177 | 180 | 183 | 186 | 111 |
| JBR | 128 | 166 | 164 | 166 | 181 | 161 | 133 | 138 | 141 | 144 | 147 | 150 | 153 | 128 |


## BinaryAdd

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Batch size: 18
- Batching: Powers
- Number of constraints: 9
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Range Check_gsum_[103]

**Proof Size:** 656 KiB (expected) / 1056 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Lookup_gsum_[5000] | Range Check_gsum_[103] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 166 | 167 | 188 | 167 | 166 | 171 | 174 | 177 | 180 | 183 | 186 | 111 |
| JBR | 128 | 166 | 166 | 167 | 181 | 160 | 133 | 137 | 140 | 143 | 146 | 149 | 152 | 128 |


## BinaryExtension

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Batch size: 40
- Batching: Powers
- Number of constraints: 8
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Lookup_gsum_[124]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Range Check_gsum_[102]

**Proof Size:** 777 KiB (expected) / 1179 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Lookup_gsum_[124] | Lookup_gsum_[5000] | Range Check_gsum_[102] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 164 | 166 | 169 | 188 | 167 | 165 | 171 | 174 | 177 | 180 | 183 | 186 | 111 |
| JBR | 128 | 166 | 164 | 166 | 169 | 182 | 161 | 133 | 138 | 141 | 144 | 147 | 150 | 153 | 128 |


## Add256

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 64
- Batch size: 69
- Batching: Powers
- Number of constraints: 36
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[103]

**Proof Size:** 816 KiB (expected) / 1165 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Permutation_gsum_[10] | Range Check_gsum_[103] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 168 | 165 | 167 | 186 | 169 | 166 | 173 | 176 | 179 | 182 | 185 | 111 |
| JBR | 128 | 168 | 165 | 167 | 179 | 162 | 133 | 139 | 142 | 145 | 148 | 151 | 128 |


## ArithEq

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 231
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 64
- Batch size: 470
- Batching: Powers
- Number of constraints: 103
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5002]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[103, 104]
- Lookup (logup): Range Check_gsum_[103]
- Lookup (logup): Range Check_gsum_[108]

**Proof Size:** 2994 KiB (expected) / 3346 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Lookup_gsum_[5002] | Permutation_gsum_[10] | Range Check_gsum_[103, 104] | Range Check_gsum_[103] | Range Check_gsum_[108] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 168 | 169 | 168 | 170 | 169 | 169 | 185 | 169 | 164 | 173 | 176 | 179 | 182 | 185 | 111 |
| JBR | 128 | 168 | 169 | 168 | 170 | 169 | 169 | 178 | 163 | 133 | 142 | 145 | 148 | 151 | 154 | 128 |


## ArithEq384

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 232
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 64
- Batch size: 536
- Batching: Powers
- Number of constraints: 76
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5002]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[103, 104]
- Lookup (logup): Range Check_gsum_[103]
- Lookup (logup): Range Check_gsum_[108]

**Proof Size:** 3366 KiB (expected) / 3720 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Lookup_gsum_[5002] | Permutation_gsum_[10] | Range Check_gsum_[103, 104] | Range Check_gsum_[103] | Range Check_gsum_[108] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 112 | 168 | 169 | 168 | 170 | 169 | 169 | 185 | 169 | 163 | 173 | 176 | 179 | 182 | 185 | 112 |
| JBR | 128 | 168 | 169 | 168 | 170 | 169 | 169 | 179 | 163 | 133 | 142 | 145 | 148 | 151 | 154 | 128 |


## Keccakf

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 217
- Grinding query phase (bits): 23
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{17}$
- FRI rounds: 4
- FRI folding factors: [8, 8, 8, 8]
- FRI early stop degree: 64
- Batch size: 4065
- Batching: Powers
- Number of constraints: 2432
- Lookup (logup): Lookup_gsum_[126]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]

**Proof Size:** 20975 KiB (expected) / 21244 KiB (worst case)

| regime | total | Lookup_gsum_[126] | Lookup_gsum_[5000] | Permutation_gsum_[10] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 113 | 163 | 171 | 167 | 180 | 172 | 164 | 176 | 179 | 182 | 185 | 113 |
| JBR | 128 | 163 | 171 | 167 | 174 | 166 | 132 | 145 | 148 | 151 | 154 | 128 |


## Sha256f

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 231
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{18}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 1265
- Batching: Powers
- Number of constraints: 115
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[109]

**Proof Size:** 7215 KiB (expected) / 7549 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Permutation_gsum_[10] | Range Check_gsum_[109] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 170 | 171 | 172 | 185 | 171 | 164 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 170 | 171 | 172 | 178 | 165 | 132 | 143 | 146 | 149 | 152 | 155 | 128 |


## Poseidon2

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 114
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{17}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 182
- Batching: Powers
- Number of constraints: 85
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]

**Proof Size:** 682 KiB (expected) / 832 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Permutation_gsum_[10] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 93 | 171 | 170 | 185 | 172 | 166 | 174 | 177 | 180 | 183 | 186 | 93 |
| JBR | 128 | 171 | 170 | 177 | 164 | 133 | 140 | 143 | 146 | 149 | 153 | 128 |


## Blake2br

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{18}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 651
- Batching: Powers
- Number of constraints: 189
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Permutation_gsum_[127]
- Lookup (logup): Range Check_gsum_[103]

**Proof Size:** 3874 KiB (expected) / 4207 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Permutation_gsum_[10] | Permutation_gsum_[127] | Range Check_gsum_[103] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 170 | 169 | 171 | 170 | 184 | 171 | 165 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 170 | 169 | 171 | 170 | 177 | 165 | 133 | 142 | 145 | 148 | 151 | 155 | 128 |


## SpecifiedRanges

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 229
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 64
- Batch size: 107
- Batching: Powers
- Number of constraints: 16
- Lookup (logup): Lookup_gsum_[102]
- Lookup (logup): Lookup_gsum_[103, 104]
- Lookup (logup): Lookup_gsum_[104, 105, 106, 107, 108]
- Lookup (logup): Lookup_gsum_[104]
- Lookup (logup): Lookup_gsum_[108, 109]
- Lookup (logup): Lookup_gsum_[108]

**Proof Size:** 1020 KiB (expected) / 1369 KiB (worst case)

| regime | total | Lookup_gsum_[102] | Lookup_gsum_[103, 104] | Lookup_gsum_[104, 105, 106, 107, 108] | Lookup_gsum_[104] | Lookup_gsum_[108, 109] | Lookup_gsum_[108] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 171 | 171 | 171 | 171 | 171 | 171 | 187 | 169 | 166 | 173 | 176 | 179 | 182 | 185 | 111 |
| JBR | 128 | 171 | 171 | 171 | 171 | 171 | 171 | 180 | 162 | 132 | 139 | 142 | 145 | 148 | 151 | 128 |


## VirtualTable0

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 69
- Batching: Powers
- Number of constraints: 6
- Lookup (logup): Lookup_gsum_[124, 8001]
- Lookup (logup): Lookup_gsum_[125, 124]
- Lookup (logup): Lookup_gsum_[125]
- Lookup (logup): Lookup_gsum_[126, 331, 8002, 133, 125]
- Lookup (logup): Lookup_gsum_[330]
- Lookup (logup): Lookup_gsum_[5002, 88, 77, 8003, 126]

**Proof Size:** 875 KiB (expected) / 1270 KiB (worst case)

| regime | total | Lookup_gsum_[124, 8001] | Lookup_gsum_[125, 124] | Lookup_gsum_[125] | Lookup_gsum_[126, 331, 8002, 133, 125] | Lookup_gsum_[330] | Lookup_gsum_[5002, 88, 77, 8003, 126] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 168 | 168 | 168 | 168 | 169 | 168 | 189 | 168 | 165 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 168 | 168 | 168 | 168 | 169 | 168 | 182 | 162 | 133 | 139 | 142 | 145 | 148 | 151 | 154 | 128 |


## VirtualTable1

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 230
- Grinding query phase (bits): 16
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 90
- Batching: Powers
- Number of constraints: 6
- Lookup (logup): Lookup_gsum_[5000]

**Proof Size:** 989 KiB (expected) / 1384 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 189 | 168 | 165 | 172 | 175 | 178 | 181 | 184 | 187 | 111 |
| JBR | 128 | 167 | 182 | 162 | 133 | 139 | 142 | 145 | 148 | 151 | 155 | 128 |


## DmaPrePost-compressor

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 110
- Grinding query phase (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{18}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Batch size: 198
- Batching: Powers
- Number of constraints: 179
- Lookup (logup): Connection_gprod_[1]

**Proof Size:** 726 KiB (expected) / 871 KiB (worst case)

| regime | total | Connection_gprod_[1] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 94 | 166 | 184 | 171 | 165 | 173 | 176 | 179 | 182 | 185 | 94 |
| JBR | 128 | 166 | 176 | 163 | 133 | 140 | 143 | 146 | 149 | 152 | 128 |


## ArithEq-compressor

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 110
- Grinding query phase (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{18}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Batch size: 198
- Batching: Powers
- Number of constraints: 179
- Lookup (logup): Connection_gprod_[1]

**Proof Size:** 726 KiB (expected) / 871 KiB (worst case)

| regime | total | Connection_gprod_[1] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 94 | 166 | 184 | 171 | 165 | 173 | 176 | 179 | 182 | 185 | 94 |
| JBR | 128 | 166 | 176 | 163 | 133 | 140 | 143 | 146 | 149 | 152 | 128 |


## ArithEq384-compressor

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 110
- Grinding query phase (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{18}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Batch size: 198
- Batching: Powers
- Number of constraints: 179
- Lookup (logup): Connection_gprod_[1]

**Proof Size:** 726 KiB (expected) / 871 KiB (worst case)

| regime | total | Connection_gprod_[1] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 94 | 166 | 184 | 171 | 165 | 173 | 176 | 179 | 182 | 185 | 94 |
| JBR | 128 | 166 | 176 | 163 | 133 | 140 | 143 | 146 | 149 | 152 | 128 |


## Keccakf-compressor

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 110
- Grinding query phase (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{20}$
- FRI rounds: 6
- FRI folding factors: [8, 8, 8, 8, 8, 4]
- FRI early stop degree: 32
- Batch size: 198
- Batching: Powers
- Number of constraints: 179
- Lookup (logup): Connection_gprod_[1]

**Proof Size:** 771 KiB (expected) / 940 KiB (worst case)

| regime | total | Connection_gprod_[1] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 94 | 164 | 184 | 169 | 163 | 171 | 174 | 177 | 180 | 183 | 186 | 94 |
| JBR | 128 | 164 | 177 | 162 | 133 | 141 | 144 | 147 | 150 | 153 | 156 | 128 |


## Sha256f-compressor

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 110
- Grinding query phase (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{19}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 64
- Batch size: 198
- Batching: Powers
- Number of constraints: 179
- Lookup (logup): Connection_gprod_[1]

**Proof Size:** 743 KiB (expected) / 892 KiB (worst case)

| regime | total | Connection_gprod_[1] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 94 | 165 | 184 | 170 | 164 | 172 | 175 | 178 | 181 | 184 | 94 |
| JBR | 128 | 165 | 176 | 162 | 133 | 140 | 143 | 146 | 149 | 152 | 128 |


## Blake2br-compressor

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 110
- Grinding query phase (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{18}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Batch size: 198
- Batching: Powers
- Number of constraints: 179
- Lookup (logup): Connection_gprod_[1]

**Proof Size:** 726 KiB (expected) / 871 KiB (worst case)

| regime | total | Connection_gprod_[1] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 94 | 166 | 184 | 171 | 165 | 173 | 176 | 179 | 182 | 185 | 94 |
| JBR | 128 | 166 | 176 | 163 | 133 | 140 | 143 | 146 | 149 | 152 | 128 |


## Recursive2

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 73
- Grinding query phase (bits): 20
- Field: Goldilocks³
- Rate (ρ): 0.125
- Trace length (H): $2^{17}$
- FRI rounds: 5
- FRI folding factors: [8, 8, 8, 8, 8]
- FRI early stop degree: 32
- Batch size: 145
- Batching: Powers
- Number of constraints: 158
- Lookup (logup): Connection_gprod_[1]

**Proof Size:** 398 KiB (expected) / 487 KiB (worst case)

| regime | total | Connection_gprod_[1] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 80 | 168 | 184 | 171 | 166 | 173 | 176 | 179 | 182 | 185 | 80 |
| JBR | 128 | 168 | 176 | 163 | 133 | 140 | 143 | 146 | 149 | 152 | 128 |


## Final

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 43
- Grinding query phase (bits): 22
- Field: Goldilocks³
- Rate (ρ): 0.03125
- Trace length (H): $2^{16}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 32
- Batch size: 139
- Batching: Powers
- Number of constraints: 154
- Lookup (logup): Connection_gprod_[1]

**Proof Size:** 253 KiB (expected) / 292 KiB (worst case)

| regime | total | Connection_gprod_[1] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 63 | 169 | 184 | 172 | 164 | 172 | 176 | 180 | 184 | 63 |
| JBR | 128 | 169 | 175 | 163 | 133 | 140 | 144 | 148 | 152 | 128 |


## Final_Compressed

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 54
- Grinding query phase (bits): 22
- Field: Goldilocks³
- Rate (ρ): 0.0625
- Trace length (H): $2^{15}$
- FRI rounds: 3
- FRI folding factors: [8, 8, 8]
- FRI early stop degree: 1024
- Batch size: 145
- Batching: Powers
- Number of constraints: 158
- Lookup (logup): Connection_gprod_[1]

**Proof Size:** 269 KiB (expected) / 313 KiB (worst case)

| regime | total | Connection_gprod_[1] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 71 | 170 | 184 | 173 | 166 | 174 | 177 | 180 | 71 |
| JBR | 128 | 170 | 175 | 164 | 134 | 141 | 144 | 147 | 128 |

