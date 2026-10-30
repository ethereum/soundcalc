# 📊 ZisK (v1.4.0-alpha)

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimates are indicative (1 KiB = 1024 bytes)

## zkVM Overview

| Metric | Value | Relevant circuit | Notes |
| --- | --- | --- | --- |
| Final bits of security | **128 bits** | [Main](#main) | Regime: JBR |
| Final proof size (worst case) | **247 KiB** | [Final_Compressed](#final_compressed) | |

## Circuits

- [Main](#main)
- [Rom](#rom)
- [Mem](#mem)
- [InputData](#inputdata)
- [RomData](#romdata)
- [MemAlign](#memalign)
- [MemAlignLarge](#memalignlarge)
- [MemAlignByte](#memalignbyte)
- [MemAlignReadByte](#memalignreadbyte)
- [MemAlignWriteByte](#memalignwritebyte)
- [MemAlignByteLarge](#memalignbytelarge)
- [MemAlignReadByteLarge](#memalignreadbytelarge)
- [Arith](#arith)
- [Binary](#binary)
- [BinaryLarge](#binarylarge)
- [BinaryHuge](#binaryhuge)
- [BinaryAdd](#binaryadd)
- [BinaryAddLarge](#binaryaddlarge)
- [BinaryAddHuge](#binaryaddhuge)
- [BinaryAddHi](#binaryaddhi)
- [BinaryAddHiLarge](#binaryaddhilarge)
- [BinaryAddHiHuge](#binaryaddhihuge)
- [BinaryExtension](#binaryextension)
- [BinaryExtensionLarge](#binaryextensionlarge)
- [Add256](#add256)
- [ArithEq](#aritheq)
- [ArithEqLarge](#aritheqlarge)
- [Arith256X](#arith256x)
- [Arith256XLarge](#arith256xlarge)
- [ArithSecp256K1](#arithsecp256k1)
- [ArithSecp256K1Large](#arithsecp256k1large)
- [ArithBn254](#arithbn254)
- [ArithBn254Large](#arithbn254large)
- [ArithEq384](#aritheq384)
- [ArithEq384Large](#aritheq384large)
- [TwistedEdwards](#twistededwards)
- [Keccakf](#keccakf)
- [Sha256f](#sha256f)
- [Poseidon](#poseidon)
- [Poseidon2KoalaBear](#poseidon2koalabear)
- [Blake2br](#blake2br)
- [Blake3f](#blake3f)
- [Blake2s](#blake2s)
- [Dma](#dma)
- [Dma64Aligned](#dma64aligned)
- [Dma64AlignedLarge](#dma64alignedlarge)
- [Dma64AlignedMemSet](#dma64alignedmemset)
- [Dma64AlignedMem](#dma64alignedmem)
- [Dma64AlignedMemLarge](#dma64alignedmemlarge)
- [Dma64AlignedMemCpy](#dma64alignedmemcpy)
- [DmaUnaligned](#dmaunaligned)
- [DmaPrePost](#dmaprepost)
- [JumpDest](#jumpdest)
- [VirtualTableZisk0](#virtualtablezisk0)
- [VirtualTableZisk1](#virtualtablezisk1)
- [Keccakf-compressor](#keccakf-compressor)
- [Poseidon2KoalaBear-compressor](#poseidon2koalabear-compressor)
- [Recursive2](#recursive2)
- [Final](#final)
- [Final_Compressed](#final_compressed)

## Main

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 194
- Batching: Powers
- Initial commitment trees (base field columns): [2, 152, 87, 6]
- Out-of-domain evaluations sent: 194
- Number of constraints: 713
- Lookup (logup): Direct_gsum_[1000]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[7890]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[102]
- Lookup (logup): Range Check_gsum_[103]

**Proof Size:** 1299 KiB (expected) / 1336 KiB (worst case)

| regime | total | Direct_gsum_[1000] | Lookup_gsum_[5000] | Lookup_gsum_[7890] | Permutation_gsum_[10] | Range Check_gsum_[102] | Range Check_gsum_[103] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 164 | 164 | 159 | 162 | 169 | 182 | 167 | 163 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 164 | 164 | 159 | 162 | 169 | 175 | 160 | 128 | 135 | 140 | 144 | 148 | 128 |


## Rom

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 21
- Batching: Powers
- Initial commitment trees (base field columns): [1, 1, 9, 6]
- Out-of-domain evaluations sent: 21
- Number of constraints: 9
- Lookup (logup): Lookup_gsum_[7890]
- Lookup (logup): Permutation_gsum_[10]

**Proof Size:** 903 KiB (expected) / 940 KiB (worst case)

| regime | total | Lookup_gsum_[7890] | Permutation_gsum_[10] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 165 | 188 | 167 | 166 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 165 | 181 | 160 | 130 | 134 | 139 | 143 | 147 | 128 |


## Mem

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 70
- Batching: Powers
- Initial commitment trees (base field columns): [1, 48, 33, 6]
- Out-of-domain evaluations sent: 70
- Number of constraints: 84
- Lookup (logup): Direct_gsum_[11]
- Lookup (logup): Lookup_gsum_[10]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[105]

**Proof Size:** 1026 KiB (expected) / 1063 KiB (worst case)

| regime | total | Direct_gsum_[11] | Lookup_gsum_[10] | Permutation_gsum_[10] | Range Check_gsum_[104] | Range Check_gsum_[105] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 167 | 167 | 166 | 166 | 185 | 167 | 164 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 167 | 167 | 166 | 166 | 177 | 160 | 128 | 134 | 139 | 143 | 147 | 128 |


## InputData

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 25
- Batching: Powers
- Initial commitment trees (base field columns): [1, 9, 14, 6]
- Out-of-domain evaluations sent: 25
- Number of constraints: 30
- Lookup (logup): Direct_gsum_[11]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[102]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 930 KiB (expected) / 966 KiB (worst case)

| regime | total | Direct_gsum_[11] | Permutation_gsum_[10] | Range Check_gsum_[102] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 167 | 169 | 166 | 187 | 167 | 166 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 167 | 169 | 166 | 179 | 160 | 129 | 134 | 139 | 143 | 147 | 128 |


## RomData

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 20
- Batching: Powers
- Initial commitment trees (base field columns): [1, 10, 6, 6]
- Out-of-domain evaluations sent: 20
- Number of constraints: 25
- Lookup (logup): Direct_gsum_[12]
- Lookup (logup): Lookup_gsum_[10]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[102]

**Proof Size:** 918 KiB (expected) / 955 KiB (worst case)

| regime | total | Direct_gsum_[12] | Lookup_gsum_[10] | Permutation_gsum_[10] | Range Check_gsum_[102] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 167 | 167 | 169 | 187 | 167 | 166 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 167 | 167 | 169 | 179 | 160 | 130 | 134 | 139 | 143 | 147 | 128 |


## MemAlign

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 63
- Batching: Powers
- Initial commitment trees (base field columns): [1, 32, 12, 6]
- Out-of-domain evaluations sent: 63
- Number of constraints: 46
- Lookup (logup): Lookup_gsum_[133]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]

**Proof Size:** 860 KiB (expected) / 896 KiB (worst case)

| regime | total | Lookup_gsum_[133] | Lookup_gsum_[88] | Permutation_gsum_[10] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 168 | 167 | 168 | 186 | 168 | 166 | 172 | 176 | 180 | 184 | 111 |
| JBR | 128 | 168 | 167 | 168 | 178 | 161 | 129 | 135 | 139 | 143 | 147 | 128 |


## MemAlignLarge

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{23}$
- FRI rounds: 5
- FRI folding factors: [16, 16, 16, 8, 8]
- FRI early stop degree: 64
- Batch size: 63
- Batching: Powers
- Initial commitment trees (base field columns): [1, 32, 12, 6]
- Out-of-domain evaluations sent: 63
- Number of constraints: 46
- Lookup (logup): Lookup_gsum_[133]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]

**Proof Size:** 961 KiB (expected) / 1001 KiB (worst case)

| regime | total | Lookup_gsum_[133] | Lookup_gsum_[88] | Permutation_gsum_[10] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 165 | 166 | 186 | 166 | 164 | 170 | 174 | 178 | 182 | 185 | 111 |
| JBR | 128 | 166 | 165 | 166 | 178 | 159 | 128 | 134 | 138 | 142 | 146 | 149 | 128 |


## MemAlignByte

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 25
- Batching: Powers
- Initial commitment trees (base field columns): [1, 16, 12, 6]
- Out-of-domain evaluations sent: 25
- Number of constraints: 16
- Lookup (logup): Direct_gsum_[10]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[106]

**Proof Size:** 938 KiB (expected) / 975 KiB (worst case)

| regime | total | Direct_gsum_[10] | Lookup_gsum_[88] | Permutation_gsum_[10] | Range Check_gsum_[104] | Range Check_gsum_[106] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 168 | 165 | 169 | 169 | 187 | 167 | 166 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 168 | 165 | 169 | 169 | 180 | 160 | 129 | 134 | 139 | 143 | 147 | 128 |


## MemAlignReadByte

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 18
- Batching: Powers
- Initial commitment trees (base field columns): [1, 10, 9, 6]
- Out-of-domain evaluations sent: 18
- Number of constraints: 10
- Lookup (logup): Direct_gsum_[10]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 923 KiB (expected) / 960 KiB (worst case)

| regime | total | Direct_gsum_[10] | Lookup_gsum_[88] | Permutation_gsum_[10] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 168 | 166 | 169 | 188 | 167 | 166 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 168 | 166 | 169 | 180 | 160 | 130 | 134 | 139 | 143 | 147 | 128 |


## MemAlignWriteByte

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 23
- Batching: Powers
- Initial commitment trees (base field columns): [1, 14, 12, 6]
- Out-of-domain evaluations sent: 23
- Number of constraints: 15
- Lookup (logup): Direct_gsum_[10]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[106]

**Proof Size:** 935 KiB (expected) / 971 KiB (worst case)

| regime | total | Direct_gsum_[10] | Lookup_gsum_[88] | Permutation_gsum_[10] | Range Check_gsum_[104] | Range Check_gsum_[106] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 168 | 165 | 169 | 169 | 188 | 167 | 166 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 168 | 165 | 169 | 169 | 180 | 160 | 129 | 134 | 139 | 143 | 147 | 128 |


## MemAlignByteLarge

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{23}$
- FRI rounds: 5
- FRI folding factors: [16, 16, 16, 8, 8]
- FRI early stop degree: 64
- Batch size: 25
- Batching: Powers
- Initial commitment trees (base field columns): [1, 16, 12, 6]
- Out-of-domain evaluations sent: 25
- Number of constraints: 16
- Lookup (logup): Direct_gsum_[10]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[106]

**Proof Size:** 929 KiB (expected) / 969 KiB (worst case)

| regime | total | Direct_gsum_[10] | Lookup_gsum_[88] | Permutation_gsum_[10] | Range Check_gsum_[104] | Range Check_gsum_[106] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 165 | 167 | 164 | 168 | 168 | 187 | 166 | 165 | 170 | 174 | 178 | 182 | 185 | 111 |
| JBR | 128 | 165 | 167 | 164 | 168 | 168 | 180 | 159 | 128 | 133 | 137 | 141 | 145 | 148 | 128 |


## MemAlignReadByteLarge

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{23}$
- FRI rounds: 5
- FRI folding factors: [16, 16, 16, 8, 8]
- FRI early stop degree: 64
- Batch size: 18
- Batching: Powers
- Initial commitment trees (base field columns): [1, 10, 9, 6]
- Out-of-domain evaluations sent: 18
- Number of constraints: 10
- Lookup (logup): Direct_gsum_[10]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 914 KiB (expected) / 954 KiB (worst case)

| regime | total | Direct_gsum_[10] | Lookup_gsum_[88] | Permutation_gsum_[10] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 165 | 167 | 165 | 168 | 188 | 166 | 165 | 170 | 174 | 178 | 182 | 185 | 111 |
| JBR | 128 | 165 | 167 | 165 | 168 | 180 | 159 | 129 | 133 | 137 | 141 | 145 | 148 | 128 |


## Arith

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 66
- Batching: Powers
- Initial commitment trees (base field columns): [1, 45, 46, 6]
- Out-of-domain evaluations sent: 66
- Number of constraints: 69
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Lookup_gsum_[330]
- Lookup (logup): Lookup_gsum_[331]
- Lookup (logup): Lookup_gsum_[5000]

**Proof Size:** 937 KiB (expected) / 974 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Lookup_gsum_[330] | Lookup_gsum_[331] | Lookup_gsum_[5000] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 165 | 168 | 166 | 185 | 168 | 165 | 172 | 176 | 180 | 184 | 111 |
| JBR | 128 | 167 | 165 | 168 | 166 | 178 | 161 | 129 | 135 | 139 | 143 | 147 | 128 |


## Binary

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 49
- Batching: Powers
- Initial commitment trees (base field columns): [1, 39, 15, 6]
- Out-of-domain evaluations sent: 49
- Number of constraints: 14
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Lookup_gsum_[125]
- Lookup (logup): Lookup_gsum_[5000]

**Proof Size:** 981 KiB (expected) / 1018 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Lookup_gsum_[125] | Lookup_gsum_[5000] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 164 | 166 | 188 | 167 | 165 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 164 | 166 | 180 | 160 | 128 | 134 | 139 | 143 | 147 | 128 |


## BinaryLarge

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 93
- Batching: Powers
- Initial commitment trees (base field columns): [1, 78, 30, 6]
- Out-of-domain evaluations sent: 93
- Number of constraints: 26
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Lookup_gsum_[125]
- Lookup (logup): Lookup_gsum_[5000]

**Proof Size:** 1076 KiB (expected) / 1113 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Lookup_gsum_[125] | Lookup_gsum_[5000] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 163 | 166 | 187 | 167 | 164 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 163 | 166 | 179 | 160 | 128 | 135 | 140 | 144 | 148 | 128 |


## BinaryHuge

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 180
- Batching: Powers
- Initial commitment trees (base field columns): [1, 156, 57, 6]
- Out-of-domain evaluations sent: 180
- Number of constraints: 49
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Lookup_gsum_[125]
- Lookup (logup): Lookup_gsum_[5000]

**Proof Size:** 1252 KiB (expected) / 1289 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Lookup_gsum_[125] | Lookup_gsum_[5000] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 162 | 166 | 186 | 167 | 163 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 162 | 166 | 178 | 160 | 128 | 135 | 140 | 144 | 148 | 128 |


## BinaryAdd

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 19
- Batching: Powers
- Initial commitment trees (base field columns): [1, 11, 9, 6]
- Out-of-domain evaluations sent: 19
- Number of constraints: 11
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 925 KiB (expected) / 961 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Lookup_gsum_[5000] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 166 | 167 | 188 | 167 | 166 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 166 | 167 | 180 | 160 | 130 | 134 | 139 | 143 | 147 | 128 |


## BinaryAddLarge

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 33
- Batching: Powers
- Initial commitment trees (base field columns): [1, 22, 18, 6]
- Out-of-domain evaluations sent: 33
- Number of constraints: 20
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 958 KiB (expected) / 995 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Lookup_gsum_[5000] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 166 | 166 | 187 | 167 | 165 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 166 | 166 | 179 | 160 | 129 | 134 | 139 | 143 | 147 | 128 |


## BinaryAddHuge

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 60
- Batching: Powers
- Initial commitment trees (base field columns): [1, 44, 33, 6]
- Out-of-domain evaluations sent: 60
- Number of constraints: 37
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 1019 KiB (expected) / 1056 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Lookup_gsum_[5000] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 166 | 165 | 186 | 167 | 165 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 166 | 165 | 179 | 160 | 128 | 134 | 139 | 143 | 147 | 128 |


## BinaryAddHi

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 21
- Batching: Powers
- Initial commitment trees (base field columns): [1, 12, 12, 6]
- Out-of-domain evaluations sent: 21
- Number of constraints: 14
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 931 KiB (expected) / 968 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Lookup_gsum_[5000] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 166 | 167 | 188 | 167 | 166 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 166 | 167 | 180 | 160 | 130 | 134 | 139 | 143 | 147 | 128 |


## BinaryAddHiLarge

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 36
- Batching: Powers
- Initial commitment trees (base field columns): [1, 24, 21, 6]
- Out-of-domain evaluations sent: 36
- Number of constraints: 25
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 966 KiB (expected) / 1003 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Lookup_gsum_[5000] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 166 | 166 | 187 | 167 | 165 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 166 | 166 | 179 | 160 | 129 | 134 | 139 | 143 | 147 | 128 |


## BinaryAddHiHuge

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 66
- Batching: Powers
- Initial commitment trees (base field columns): [1, 48, 39, 6]
- Out-of-domain evaluations sent: 66
- Number of constraints: 47
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 1036 KiB (expected) / 1073 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Lookup_gsum_[5000] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 166 | 165 | 186 | 167 | 164 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 166 | 165 | 178 | 160 | 128 | 134 | 139 | 143 | 147 | 128 |


## BinaryExtension

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 45
- Batching: Powers
- Initial commitment trees (base field columns): [1, 34, 18, 6]
- Out-of-domain evaluations sent: 45
- Number of constraints: 30
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Lookup_gsum_[124]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Range Check_gsum_[102]

**Proof Size:** 978 KiB (expected) / 1015 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Lookup_gsum_[124] | Lookup_gsum_[5000] | Range Check_gsum_[102] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 164 | 166 | 169 | 187 | 167 | 165 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 164 | 166 | 169 | 179 | 160 | 128 | 134 | 139 | 143 | 147 | 128 |


## BinaryExtensionLarge

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 85
- Batching: Powers
- Initial commitment trees (base field columns): [1, 68, 36, 6]
- Out-of-domain evaluations sent: 85
- Number of constraints: 58
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Lookup_gsum_[124]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Range Check_gsum_[102]

**Proof Size:** 1069 KiB (expected) / 1106 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Lookup_gsum_[124] | Lookup_gsum_[5000] | Range Check_gsum_[102] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 163 | 166 | 168 | 186 | 167 | 164 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 163 | 166 | 168 | 178 | 160 | 128 | 135 | 140 | 144 | 148 | 128 |


## Add256

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 8]
- FRI early stop degree: 64
- Batch size: 69
- Batching: Powers
- Initial commitment trees (base field columns): [1, 47, 51, 6]
- Out-of-domain evaluations sent: 69
- Number of constraints: 52
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 865 KiB (expected) / 900 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Permutation_gsum_[10] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 168 | 165 | 167 | 186 | 169 | 166 | 173 | 177 | 181 | 185 | 111 |
| JBR | 128 | 168 | 165 | 167 | 178 | 162 | 130 | 136 | 140 | 144 | 148 | 128 |


## ArithEq

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 8]
- FRI early stop degree: 64
- Batch size: 480
- Batching: Powers
- Initial commitment trees (base field columns): [2, 45, 39, 6]
- Out-of-domain evaluations sent: 480
- Number of constraints: 125
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5002]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104, 105]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[107]

**Proof Size:** 858 KiB (expected) / 894 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Lookup_gsum_[5002] | Permutation_gsum_[10] | Range Check_gsum_[104, 105] | Range Check_gsum_[104] | Range Check_gsum_[107] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 168 | 169 | 168 | 170 | 169 | 169 | 185 | 169 | 164 | 173 | 177 | 181 | 185 | 111 |
| JBR | 128 | 168 | 169 | 168 | 170 | 169 | 169 | 177 | 162 | 128 | 137 | 141 | 145 | 149 | 128 |


## ArithEqLarge

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 480
- Batching: Powers
- Initial commitment trees (base field columns): [2, 45, 39, 6]
- Out-of-domain evaluations sent: 480
- Number of constraints: 125
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5002]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104, 105]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[107]

**Proof Size:** 943 KiB (expected) / 980 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Lookup_gsum_[5002] | Permutation_gsum_[10] | Range Check_gsum_[104, 105] | Range Check_gsum_[104] | Range Check_gsum_[107] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 168 | 167 | 169 | 168 | 168 | 185 | 168 | 163 | 172 | 176 | 180 | 184 | 111 |
| JBR | 128 | 167 | 168 | 167 | 169 | 168 | 168 | 177 | 161 | 128 | 137 | 141 | 145 | 149 | 128 |


## Arith256X

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 8]
- FRI early stop degree: 64
- Batch size: 266
- Batching: Powers
- Initial commitment trees (base field columns): [2, 19, 29, 6]
- Out-of-domain evaluations sent: 266
- Number of constraints: 64
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5002]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104, 105]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[107]

**Proof Size:** 790 KiB (expected) / 825 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Lookup_gsum_[5002] | Permutation_gsum_[10] | Range Check_gsum_[104, 105] | Range Check_gsum_[104] | Range Check_gsum_[107] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 168 | 169 | 168 | 170 | 169 | 170 | 185 | 169 | 164 | 173 | 177 | 181 | 185 | 111 |
| JBR | 128 | 168 | 169 | 168 | 170 | 169 | 170 | 178 | 162 | 128 | 136 | 140 | 144 | 148 | 128 |


## Arith256XLarge

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 266
- Batching: Powers
- Initial commitment trees (base field columns): [2, 19, 29, 6]
- Out-of-domain evaluations sent: 266
- Number of constraints: 64
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5002]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104, 105]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[107]

**Proof Size:** 878 KiB (expected) / 915 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Lookup_gsum_[5002] | Permutation_gsum_[10] | Range Check_gsum_[104, 105] | Range Check_gsum_[104] | Range Check_gsum_[107] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 168 | 167 | 169 | 168 | 169 | 185 | 168 | 163 | 172 | 176 | 180 | 184 | 111 |
| JBR | 128 | 167 | 168 | 167 | 169 | 168 | 169 | 178 | 161 | 128 | 136 | 140 | 144 | 148 | 128 |


## ArithSecp256K1

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 8]
- FRI early stop degree: 64
- Batch size: 280
- Batching: Powers
- Initial commitment trees (base field columns): [2, 27, 39, 6]
- Out-of-domain evaluations sent: 280
- Number of constraints: 65
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5002]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104, 105]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[107]

**Proof Size:** 820 KiB (expected) / 855 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Lookup_gsum_[5002] | Permutation_gsum_[10] | Range Check_gsum_[104, 105] | Range Check_gsum_[104] | Range Check_gsum_[107] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 168 | 169 | 168 | 170 | 169 | 169 | 185 | 169 | 164 | 173 | 177 | 181 | 185 | 111 |
| JBR | 128 | 168 | 169 | 168 | 170 | 169 | 169 | 178 | 162 | 128 | 136 | 140 | 144 | 148 | 128 |


## ArithSecp256K1Large

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 280
- Batching: Powers
- Initial commitment trees (base field columns): [2, 27, 39, 6]
- Out-of-domain evaluations sent: 280
- Number of constraints: 65
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5002]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104, 105]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[107]

**Proof Size:** 908 KiB (expected) / 945 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Lookup_gsum_[5002] | Permutation_gsum_[10] | Range Check_gsum_[104, 105] | Range Check_gsum_[104] | Range Check_gsum_[107] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 168 | 167 | 169 | 168 | 168 | 185 | 168 | 163 | 172 | 176 | 180 | 184 | 111 |
| JBR | 128 | 167 | 168 | 167 | 169 | 168 | 168 | 178 | 161 | 128 | 136 | 140 | 144 | 148 | 128 |


## ArithBn254

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 8]
- FRI early stop degree: 64
- Batch size: 337
- Batching: Powers
- Initial commitment trees (base field columns): [2, 33, 39, 6]
- Out-of-domain evaluations sent: 337
- Number of constraints: 80
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5002]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104, 105]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[107]

**Proof Size:** 835 KiB (expected) / 870 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Lookup_gsum_[5002] | Permutation_gsum_[10] | Range Check_gsum_[104, 105] | Range Check_gsum_[104] | Range Check_gsum_[107] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 168 | 169 | 168 | 170 | 169 | 169 | 185 | 169 | 164 | 173 | 177 | 181 | 185 | 111 |
| JBR | 128 | 168 | 169 | 168 | 170 | 169 | 169 | 178 | 162 | 128 | 137 | 141 | 145 | 149 | 128 |


## ArithBn254Large

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 337
- Batching: Powers
- Initial commitment trees (base field columns): [2, 33, 39, 6]
- Out-of-domain evaluations sent: 337
- Number of constraints: 80
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5002]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104, 105]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[107]

**Proof Size:** 919 KiB (expected) / 956 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Lookup_gsum_[5002] | Permutation_gsum_[10] | Range Check_gsum_[104, 105] | Range Check_gsum_[104] | Range Check_gsum_[107] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 168 | 167 | 169 | 168 | 168 | 185 | 168 | 163 | 172 | 176 | 180 | 184 | 111 |
| JBR | 128 | 167 | 168 | 167 | 169 | 168 | 168 | 178 | 161 | 128 | 136 | 140 | 144 | 148 | 128 |


## ArithEq384

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 8]
- FRI early stop degree: 64
- Batch size: 552
- Batching: Powers
- Initial commitment trees (base field columns): [2, 35, 39, 6]
- Out-of-domain evaluations sent: 552
- Number of constraints: 94
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5002]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104, 105]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[107]

**Proof Size:** 844 KiB (expected) / 879 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Lookup_gsum_[5002] | Permutation_gsum_[10] | Range Check_gsum_[104, 105] | Range Check_gsum_[104] | Range Check_gsum_[107] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 168 | 169 | 168 | 170 | 169 | 169 | 185 | 169 | 163 | 173 | 177 | 181 | 185 | 111 |
| JBR | 128 | 168 | 169 | 168 | 170 | 169 | 169 | 177 | 162 | 128 | 137 | 141 | 145 | 149 | 128 |


## ArithEq384Large

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 552
- Batching: Powers
- Initial commitment trees (base field columns): [2, 35, 39, 6]
- Out-of-domain evaluations sent: 552
- Number of constraints: 94
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5002]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104, 105]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[107]

**Proof Size:** 928 KiB (expected) / 965 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Lookup_gsum_[5002] | Permutation_gsum_[10] | Range Check_gsum_[104, 105] | Range Check_gsum_[104] | Range Check_gsum_[107] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 168 | 167 | 169 | 168 | 168 | 185 | 168 | 162 | 172 | 176 | 180 | 184 | 111 |
| JBR | 128 | 167 | 168 | 167 | 169 | 168 | 168 | 178 | 161 | 128 | 137 | 141 | 145 | 149 | 128 |


## TwistedEdwards

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{18}$
- FRI rounds: 4
- FRI folding factors: [16, 8, 8, 8]
- FRI early stop degree: 64
- Batch size: 414
- Batching: Powers
- Initial commitment trees (base field columns): [2, 41, 62, 6]
- Out-of-domain evaluations sent: 414
- Number of constraints: 70
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[5002]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104, 105]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[107]

**Proof Size:** 733 KiB (expected) / 768 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Lookup_gsum_[5002] | Permutation_gsum_[10] | Range Check_gsum_[104, 105] | Range Check_gsum_[104] | Range Check_gsum_[107] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 170 | 171 | 170 | 171 | 170 | 170 | 185 | 171 | 166 | 175 | 179 | 182 | 185 | 111 |
| JBR | 128 | 170 | 171 | 170 | 171 | 170 | 170 | 178 | 164 | 129 | 138 | 142 | 145 | 148 | 128 |


## Keccakf

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 214
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 3628
- Batching: Powers
- Initial commitment trees (base field columns): [3, 467, 142, 6]
- Out-of-domain evaluations sent: 3628
- Number of constraints: 459
- Lookup (logup): Lookup_gsum_[126]
- Lookup (logup): Lookup_gsum_[127]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]

**Proof Size:** 1906 KiB (expected) / 1943 KiB (worst case)

| regime | total | Lookup_gsum_[126] | Lookup_gsum_[127] | Lookup_gsum_[5000] | Permutation_gsum_[10] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 112 | 162 | 164 | 167 | 166 | 183 | 168 | 160 | 172 | 176 | 180 | 184 | 112 |
| JBR | 128 | 162 | 164 | 167 | 166 | 176 | 162 | 128 | 140 | 144 | 148 | 152 | 128 |


## Sha256f

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{19}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 8, 8]
- FRI early stop degree: 64
- Batch size: 1261
- Batching: Powers
- Initial commitment trees (base field columns): [2, 102, 14, 6]
- Out-of-domain evaluations sent: 1261
- Number of constraints: 113
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[108]

**Proof Size:** 851 KiB (expected) / 885 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Permutation_gsum_[10] | Range Check_gsum_[108] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 169 | 170 | 171 | 185 | 170 | 163 | 174 | 178 | 182 | 185 | 111 |
| JBR | 128 | 169 | 170 | 171 | 177 | 163 | 128 | 138 | 142 | 146 | 149 | 128 |


## Poseidon

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{17}$
- FRI rounds: 3
- FRI folding factors: [16, 16, 16]
- FRI early stop degree: 64
- Batch size: 534
- Batching: Powers
- Initial commitment trees (base field columns): [2, 84, 302, 6]
- Out-of-domain evaluations sent: 534
- Number of constraints: 431
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 1191 KiB (expected) / 1222 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Permutation_gsum_[10] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 171 | 170 | 168 | 183 | 172 | 166 | 176 | 180 | 184 | 111 |
| JBR | 128 | 171 | 170 | 168 | 175 | 165 | 130 | 139 | 143 | 147 | 128 |


## Poseidon2KoalaBear

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 8]
- FRI early stop degree: 64
- Batch size: 420
- Batching: Powers
- Initial commitment trees (base field columns): [2, 195, 298, 6]
- Out-of-domain evaluations sent: 420
- Number of constraints: 218
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 1534 KiB (expected) / 1570 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Permutation_gsum_[10] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 168 | 168 | 164 | 184 | 169 | 164 | 173 | 177 | 181 | 185 | 111 |
| JBR | 128 | 168 | 168 | 164 | 176 | 162 | 128 | 137 | 141 | 145 | 149 | 128 |


## Blake2br

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 8]
- FRI early stop degree: 64
- Batch size: 264
- Batching: Powers
- Initial commitment trees (base field columns): [3, 122, 138, 6]
- Out-of-domain evaluations sent: 264
- Number of constraints: 104
- Lookup (logup): Lookup_gsum_[129]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Permutation_gsum_[128]
- Lookup (logup): Permutation_gsum_[132]
- Lookup (logup): Range Check_gsum_[100]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 1143 KiB (expected) / 1178 KiB (worst case)

| regime | total | Lookup_gsum_[129] | Lookup_gsum_[5000] | Lookup_gsum_[88] | Permutation_gsum_[10] | Permutation_gsum_[128] | Permutation_gsum_[132] | Range Check_gsum_[100] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 164 | 168 | 170 | 166 | 168 | 166 | 171 | 167 | 185 | 169 | 164 | 173 | 177 | 181 | 185 | 111 |
| JBR | 128 | 164 | 168 | 170 | 166 | 168 | 166 | 171 | 167 | 177 | 162 | 128 | 136 | 140 | 144 | 148 | 128 |


## Blake3f

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 8]
- FRI early stop degree: 64
- Batch size: 572
- Batching: Powers
- Initial commitment trees (base field columns): [2, 114, 101, 6]
- Out-of-domain evaluations sent: 572
- Number of constraints: 65
- Lookup (logup): Lookup_gsum_[129]
- Lookup (logup): Lookup_gsum_[130]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[106]

**Proof Size:** 1078 KiB (expected) / 1113 KiB (worst case)

| regime | total | Lookup_gsum_[129] | Lookup_gsum_[130] | Lookup_gsum_[5000] | Permutation_gsum_[10] | Range Check_gsum_[104] | Range Check_gsum_[106] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 164 | 167 | 168 | 168 | 167 | 170 | 185 | 169 | 163 | 173 | 177 | 181 | 185 | 111 |
| JBR | 128 | 164 | 167 | 168 | 168 | 167 | 170 | 178 | 162 | 128 | 137 | 141 | 145 | 149 | 128 |


## Blake2s

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 8]
- FRI early stop degree: 64
- Batch size: 365
- Batching: Powers
- Initial commitment trees (base field columns): [2, 57, 52, 6]
- Out-of-domain evaluations sent: 365
- Number of constraints: 33
- Lookup (logup): Lookup_gsum_[129]
- Lookup (logup): Lookup_gsum_[131]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[106]

**Proof Size:** 897 KiB (expected) / 932 KiB (worst case)

| regime | total | Lookup_gsum_[129] | Lookup_gsum_[131] | Lookup_gsum_[5000] | Permutation_gsum_[10] | Range Check_gsum_[104] | Range Check_gsum_[106] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 165 | 168 | 168 | 169 | 168 | 171 | 186 | 169 | 164 | 173 | 177 | 181 | 185 | 111 |
| JBR | 128 | 165 | 168 | 168 | 169 | 168 | 171 | 179 | 162 | 128 | 137 | 141 | 145 | 149 | 128 |


## Dma

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 48
- Batching: Powers
- Initial commitment trees (base field columns): [1, 36, 21, 6]
- Out-of-domain evaluations sent: 48
- Number of constraints: 54
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[77]
- Lookup (logup): Lookup_gsum_[8001]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Permutation_gsum_[8000]
- Lookup (logup): Range Check_gsum_[102]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[105]

**Proof Size:** 881 KiB (expected) / 917 KiB (worst case)

| regime | total | Lookup_gsum_[5000] | Lookup_gsum_[77] | Lookup_gsum_[8001] | Permutation_gsum_[10] | Permutation_gsum_[8000] | Range Check_gsum_[102] | Range Check_gsum_[104] | Range Check_gsum_[105] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 169 | 168 | 168 | 166 | 170 | 169 | 169 | 186 | 168 | 166 | 172 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 169 | 168 | 168 | 166 | 170 | 169 | 169 | 178 | 161 | 129 | 135 | 139 | 143 | 147 | 128 |


## Dma64Aligned

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 62
- Batching: Powers
- Initial commitment trees (base field columns): [1, 35, 36, 6]
- Out-of-domain evaluations sent: 62
- Number of constraints: 102
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Direct_gsum_[8200]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[102]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 904 KiB (expected) / 941 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Direct_gsum_[8200] | Lookup_gsum_[5000] | Lookup_gsum_[88] | Permutation_gsum_[10] | Range Check_gsum_[102] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 166 | 167 | 167 | 165 | 167 | 169 | 185 | 168 | 166 | 172 | 176 | 180 | 184 | 111 |
| JBR | 128 | 167 | 166 | 167 | 167 | 165 | 167 | 169 | 177 | 161 | 129 | 135 | 139 | 143 | 147 | 128 |


## Dma64AlignedLarge

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 212
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{23}$
- FRI rounds: 5
- FRI folding factors: [16, 16, 16, 8, 8]
- FRI early stop degree: 64
- Batch size: 62
- Batching: Powers
- Initial commitment trees (base field columns): [1, 35, 36, 6]
- Out-of-domain evaluations sent: 62
- Number of constraints: 102
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Direct_gsum_[8200]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[102]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 1006 KiB (expected) / 1046 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Direct_gsum_[8200] | Lookup_gsum_[5000] | Lookup_gsum_[88] | Permutation_gsum_[10] | Range Check_gsum_[102] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 165 | 164 | 165 | 165 | 163 | 165 | 167 | 185 | 166 | 164 | 170 | 174 | 178 | 182 | 185 | 111 |
| JBR | 128 | 165 | 164 | 165 | 165 | 163 | 165 | 167 | 177 | 159 | 128 | 134 | 138 | 142 | 146 | 149 | 128 |


## Dma64AlignedMemSet

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 30
- Batching: Powers
- Initial commitment trees (base field columns): [1, 14, 15, 6]
- Out-of-domain evaluations sent: 30
- Number of constraints: 71
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Direct_gsum_[8200]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 834 KiB (expected) / 871 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Direct_gsum_[8200] | Lookup_gsum_[5000] | Permutation_gsum_[10] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 166 | 167 | 165 | 169 | 185 | 168 | 167 | 172 | 176 | 180 | 184 | 111 |
| JBR | 128 | 167 | 166 | 167 | 165 | 169 | 178 | 161 | 130 | 135 | 139 | 143 | 147 | 128 |


## Dma64AlignedMem

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 46
- Batching: Powers
- Initial commitment trees (base field columns): [1, 26, 18, 6]
- Out-of-domain evaluations sent: 46
- Number of constraints: 91
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Direct_gsum_[8200]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 859 KiB (expected) / 896 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Direct_gsum_[8200] | Lookup_gsum_[5000] | Permutation_gsum_[10] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 166 | 167 | 165 | 169 | 185 | 168 | 166 | 172 | 176 | 180 | 184 | 111 |
| JBR | 128 | 167 | 166 | 167 | 165 | 169 | 177 | 161 | 129 | 135 | 139 | 143 | 147 | 128 |


## Dma64AlignedMemLarge

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 4
- FRI folding factors: [32, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 46
- Batching: Powers
- Initial commitment trees (base field columns): [1, 26, 18, 6]
- Out-of-domain evaluations sent: 46
- Number of constraints: 91
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Direct_gsum_[8200]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 965 KiB (expected) / 1001 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Direct_gsum_[8200] | Lookup_gsum_[5000] | Permutation_gsum_[10] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 165 | 166 | 164 | 168 | 185 | 167 | 165 | 171 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 165 | 166 | 164 | 168 | 177 | 160 | 128 | 134 | 139 | 143 | 147 | 128 |


## Dma64AlignedMemCpy

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 52
- Batching: Powers
- Initial commitment trees (base field columns): [1, 31, 30, 6]
- Out-of-domain evaluations sent: 52
- Number of constraints: 87
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Direct_gsum_[8200]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 887 KiB (expected) / 924 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Direct_gsum_[8200] | Lookup_gsum_[5000] | Permutation_gsum_[10] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 166 | 167 | 164 | 169 | 185 | 168 | 166 | 172 | 176 | 180 | 184 | 111 |
| JBR | 128 | 167 | 166 | 167 | 164 | 169 | 177 | 161 | 129 | 135 | 139 | 143 | 147 | 128 |


## DmaUnaligned

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 52
- Batching: Powers
- Initial commitment trees (base field columns): [1, 24, 12, 6]
- Out-of-domain evaluations sent: 52
- Number of constraints: 76
- Lookup (logup): Direct_gsum_[5000]
- Lookup (logup): Direct_gsum_[8201]
- Lookup (logup): Lookup_gsum_[10]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104]

**Proof Size:** 846 KiB (expected) / 883 KiB (worst case)

| regime | total | Direct_gsum_[5000] | Direct_gsum_[8201] | Lookup_gsum_[10] | Lookup_gsum_[5000] | Lookup_gsum_[88] | Permutation_gsum_[10] | Range Check_gsum_[104] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 165 | 168 | 167 | 167 | 167 | 169 | 185 | 168 | 166 | 172 | 176 | 180 | 184 | 111 |
| JBR | 128 | 167 | 165 | 168 | 167 | 167 | 167 | 169 | 178 | 161 | 129 | 135 | 139 | 143 | 147 | 128 |


## DmaPrePost

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 83
- Batching: Powers
- Initial commitment trees (base field columns): [1, 66, 32, 6]
- Out-of-domain evaluations sent: 83
- Number of constraints: 85
- Lookup (logup): Lookup_gsum_[8002]
- Lookup (logup): Lookup_gsum_[8003]
- Lookup (logup): Lookup_gsum_[88]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Permutation_gsum_[8000]

**Proof Size:** 949 KiB (expected) / 986 KiB (worst case)

| regime | total | Lookup_gsum_[8002] | Lookup_gsum_[8003] | Lookup_gsum_[88] | Permutation_gsum_[10] | Permutation_gsum_[8000] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 168 | 169 | 166 | 166 | 167 | 185 | 168 | 165 | 172 | 176 | 180 | 184 | 111 |
| JBR | 128 | 168 | 169 | 166 | 166 | 167 | 177 | 161 | 128 | 135 | 139 | 143 | 147 | 128 |


## JumpDest

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 64
- Batching: Powers
- Initial commitment trees (base field columns): [2, 32, 28, 6]
- Out-of-domain evaluations sent: 64
- Number of constraints: 67
- Lookup (logup): Direct_gsum_[8100]
- Lookup (logup): Lookup_gsum_[5000]
- Lookup (logup): Lookup_gsum_[8101]
- Lookup (logup): Lookup_gsum_[8102]
- Lookup (logup): Permutation_gsum_[10]
- Lookup (logup): Range Check_gsum_[104]
- Lookup (logup): Range Check_gsum_[106]

**Proof Size:** 889 KiB (expected) / 926 KiB (worst case)

| regime | total | Direct_gsum_[8100] | Lookup_gsum_[5000] | Lookup_gsum_[8101] | Lookup_gsum_[8102] | Permutation_gsum_[10] | Range Check_gsum_[104] | Range Check_gsum_[106] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 166 | 167 | 166 | 167 | 166 | 169 | 170 | 185 | 168 | 166 | 172 | 176 | 180 | 184 | 111 |
| JBR | 128 | 166 | 167 | 166 | 167 | 166 | 169 | 170 | 178 | 161 | 129 | 135 | 139 | 143 | 147 | 128 |


## VirtualTableZisk0

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 78
- Batching: Powers
- Initial commitment trees (base field columns): [55, 12, 21, 6]
- Out-of-domain evaluations sent: 78
- Number of constraints: 8
- Lookup (logup): Lookup_gsum_[5000, 5000]
- Lookup (logup): Lookup_gsum_[5000]

**Proof Size:** 936 KiB (expected) / 973 KiB (worst case)

| regime | total | Lookup_gsum_[5000, 5000] | Lookup_gsum_[5000] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 167 | 167 | 188 | 168 | 165 | 172 | 176 | 180 | 184 | 111 |
| JBR | 128 | 167 | 167 | 181 | 161 | 129 | 135 | 139 | 143 | 147 | 128 |


## VirtualTableZisk1

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 211
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 64
- Batch size: 98
- Batching: Powers
- Initial commitment trees (base field columns): [59, 23, 36, 6]
- Out-of-domain evaluations sent: 98
- Number of constraints: 13
- Lookup (logup): Lookup_gsum_[102]
- Lookup (logup): Lookup_gsum_[104, 103, 106, 100, 108, 330, 5002]
- Lookup (logup): Lookup_gsum_[105]
- Lookup (logup): Lookup_gsum_[107]
- Lookup (logup): Lookup_gsum_[124, 126]
- Lookup (logup): Lookup_gsum_[125, 8001]
- Lookup (logup): Lookup_gsum_[125]
- Lookup (logup): Lookup_gsum_[126, 8002, 133, 125]
- Lookup (logup): Lookup_gsum_[127, 129, 124]
- Lookup (logup): Lookup_gsum_[5002, 8101, 88, 77, 8003, 8102, 331, 127]

**Proof Size:** 986 KiB (expected) / 1022 KiB (worst case)

| regime | total | Lookup_gsum_[102] | Lookup_gsum_[104, 103, 106, 100, 108, 330, 5002] | Lookup_gsum_[105] | Lookup_gsum_[107] | Lookup_gsum_[124, 126] | Lookup_gsum_[125, 8001] | Lookup_gsum_[125] | Lookup_gsum_[126, 8002, 133, 125] | Lookup_gsum_[127, 129, 124] | Lookup_gsum_[5002, 8101, 88, 77, 8003, 8102, 331, 127] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 111 | 170 | 169 | 170 | 170 | 168 | 168 | 168 | 168 | 168 | 168 | 188 | 168 | 165 | 172 | 176 | 180 | 184 | 111 |
| JBR | 128 | 170 | 169 | 170 | 170 | 168 | 168 | 168 | 168 | 168 | 168 | 180 | 161 | 128 | 135 | 139 | 143 | 147 | 128 |


## Keccakf-compressor

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 103
- Grinding query phase (bits): 27
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{19}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 8, 8]
- FRI early stop degree: 128
- Batch size: 1624
- Batching: Powers
- Initial commitment trees (base field columns): [43, 344, 144, 12]
- Out-of-domain evaluations sent: 1624
- Number of constraints: 1006
- Lookup (logup): Connection_gprod_[1]
- Lookup (logup): Lookup_gsum_[1000]
- Lookup (logup): Lookup_gsum_[250]
- Lookup (logup): Lookup_gsum_[500]

**Proof Size:** 822 KiB (expected) / 840 KiB (worst case)

| regime | total | Connection_gprod_[1] | Lookup_gsum_[1000] | Lookup_gsum_[250] | Lookup_gsum_[500] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 96 | 166 | 162 | 166 | 168 | 182 | 170 | 161 | 172 | 176 | 180 | 183 | 96 |
| JBR | 128 | 166 | 162 | 166 | 168 | 174 | 162 | 128 | 139 | 143 | 147 | 150 | 128 |


## Poseidon2KoalaBear-compressor

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 103
- Grinding query phase (bits): 27
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{19}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 8, 8]
- FRI early stop degree: 128
- Batch size: 1389
- Batching: Powers
- Initial commitment trees (base field columns): [43, 290, 123, 12]
- Out-of-domain evaluations sent: 1389
- Number of constraints: 928
- Lookup (logup): Connection_gprod_[1]
- Lookup (logup): Lookup_gsum_[1000]
- Lookup (logup): Lookup_gsum_[250]
- Lookup (logup): Lookup_gsum_[500]

**Proof Size:** 756 KiB (expected) / 774 KiB (worst case)

| regime | total | Connection_gprod_[1] | Lookup_gsum_[1000] | Lookup_gsum_[250] | Lookup_gsum_[500] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 96 | 166 | 163 | 167 | 168 | 182 | 170 | 161 | 172 | 176 | 180 | 183 | 96 |
| JBR | 128 | 166 | 163 | 167 | 168 | 174 | 162 | 128 | 138 | 142 | 146 | 149 | 128 |


## Recursive2

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 106
- Grinding query phase (bits): 24
- Field: Goldilocks³
- Rate (ρ): 0.25
- Trace length (H): $2^{19}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 8, 8]
- FRI early stop degree: 128
- Batch size: 1156
- Batching: Powers
- Initial commitment trees (base field columns): [43, 236, 102, 12]
- Out-of-domain evaluations sent: 1156
- Number of constraints: 854
- Lookup (logup): Connection_gprod_[1]
- Lookup (logup): Lookup_gsum_[1000]
- Lookup (logup): Lookup_gsum_[250]
- Lookup (logup): Lookup_gsum_[500]

**Proof Size:** 708 KiB (expected) / 728 KiB (worst case)

| regime | total | Connection_gprod_[1] | Lookup_gsum_[1000] | Lookup_gsum_[250] | Lookup_gsum_[500] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 95 | 166 | 163 | 167 | 168 | 182 | 170 | 162 | 172 | 176 | 180 | 183 | 95 |
| JBR | 128 | 166 | 163 | 167 | 168 | 174 | 162 | 128 | 138 | 142 | 146 | 149 | 128 |


## Final

**Parameters:**
- Proof system: DEEP-ALI
- PCS: FRI
- Hash size (bits): 256
- Number of queries: 51
- Grinding query phase (bits): 27
- Field: Goldilocks³
- Rate (ρ): 0.0625
- Trace length (H): $2^{18}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 8]
- FRI early stop degree: 128
- Batch size: 1122
- Batching: Powers
- Initial commitment trees (base field columns): [43, 236, 60, 21]
- Out-of-domain evaluations sent: 1122
- Number of constraints: 427
- Lookup (logup): Connection_gprod_[1]
- Lookup (logup): Lookup_gsum_[1000]
- Lookup (logup): Lookup_gsum_[250]
- Lookup (logup): Lookup_gsum_[500]

**Proof Size:** 372 KiB (expected) / 382 KiB (worst case)

| regime | total | Connection_gprod_[1] | Lookup_gsum_[1000] | Lookup_gsum_[250] | Lookup_gsum_[500] | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 73 | 167 | 164 | 168 | 169 | 183 | 170 | 160 | 171 | 175 | 179 | 183 | 73 |
| JBR | 128 | 167 | 164 | 168 | 169 | 174 | 161 | 128 | 138 | 142 | 146 | 150 | 128 |


## Final_Compressed

**Parameters:**
- Proof system: DEEP-ALI
- PCS: STIR
- Hash size (bits): 256
- Field: Goldilocks³
- Iterations (M): 3
- Folding factors (k_i): [4, 3, 3]
- Initial rate (ρ): $2^{-5}$
- Initial log-degree: 18
- Batch size: 649
- Batching: Powers
- Queries per iteration: [41, 26, 22]
- OOD samples per iteration: [1, 1]
- Total grinding overhead log2: 27.64
- Initial commitment trees (base field columns): [43, 128, 36, 21]
- Out-of-domain evaluations sent: 649
- Number of constraints: 276
- Lookup (logup): Connection_gprod_[1]
- Lookup (logup): Lookup_gsum_[1000]
- Lookup (logup): Lookup_gsum_[250]
- Lookup (logup): Lookup_gsum_[500]

**Proof Size:** 240 KiB (expected) / 247 KiB (worst case)

| regime | total | Connection_gprod_[1] | Lookup_gsum_[1000] | Lookup_gsum_[250] | Lookup_gsum_[500] | ALI | DEEP | OOD(i=1) | OOD(i=2) | batching | fin | fold(i=0) | shift(i=1) | shift(i=2) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 44 | 167 | 165 | 169 | 170 | 183 | 170 | 178 | 181 | 160 | 44 | 170 | 66 | 51 |
| JBR | 128 | 167 | 165 | 169 | 170 | 174 | 161 | 156 | 157 | 128 | 129 | 138 | 128 | 128 |

