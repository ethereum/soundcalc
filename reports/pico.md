# 📊 Pico

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimate is only indicative

## Circuits

- [riscv](#riscv)
- [convert](#convert)
- [combine](#combine)
- [compress](#compress)
- [embed](#embed)

## riscv

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 248
- Number of queries: 84
- Grinding (bits): 16
- Field: KoalaBear⁴
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- FRI rounds: 22
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 2
- Batching: Powers

**Proof Size Estimate:** 4346 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 18 | commit round 19 | commit round 2 | commit round 20 | commit round 21 | commit round 22 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 50 | 113 | 99 | 90 | 91 | 100 | 101 | 102 | 103 | 104 | 105 | 106 | 107 | 108 | 109 | 92 | 110 | 111 | 112 | 93 | 94 | 95 | 96 | 97 | 98 | 99 | 50 |
| JBR | 54 | 108 | 94 | 68 | 69 | 78 | 79 | 80 | 81 | 82 | 83 | 84 | 85 | 86 | 87 | 70 | 88 | 89 | 90 | 71 | 72 | 73 | 74 | 75 | 76 | 77 | 54 |
| best attack | 99 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |


## convert

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 248
- Number of queries: 84
- Grinding (bits): 16
- Field: KoalaBear⁴
- Rate (ρ): 0.5
- Trace length (H): $2^{20}$
- FRI rounds: 20
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 2
- Batching: Powers

**Proof Size Estimate:** 1816 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 18 | commit round 19 | commit round 2 | commit round 20 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 50 | 115 | 101 | 94 | 95 | 104 | 105 | 106 | 107 | 108 | 109 | 110 | 111 | 112 | 113 | 96 | 114 | 97 | 98 | 99 | 100 | 101 | 102 | 103 | 50 |
| JBR | 54 | 110 | 96 | 72 | 73 | 82 | 83 | 84 | 85 | 86 | 87 | 88 | 89 | 90 | 91 | 74 | 92 | 75 | 76 | 77 | 78 | 79 | 80 | 81 | 54 |
| best attack | 99 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |


## combine

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 248
- Number of queries: 84
- Grinding (bits): 16
- Field: KoalaBear⁴
- Rate (ρ): 0.5
- Trace length (H): $2^{18}$
- FRI rounds: 18
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 2
- Batching: Powers

**Proof Size Estimate:** 1711 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 18 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 50 | 115 | 103 | 96 | 97 | 106 | 107 | 108 | 109 | 110 | 111 | 112 | 113 | 114 | 98 | 99 | 100 | 101 | 102 | 103 | 104 | 105 | 50 |
| JBR | 54 | 110 | 98 | 74 | 75 | 84 | 85 | 86 | 87 | 88 | 89 | 90 | 91 | 92 | 76 | 77 | 78 | 79 | 80 | 81 | 82 | 83 | 54 |
| best attack | 99 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |


## compress

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 248
- Number of queries: 21
- Grinding (bits): 16
- Field: KoalaBear⁴
- Rate (ρ): 0.0625
- Trace length (H): $2^{17}$
- FRI rounds: 17
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 16
- Batching: Powers

**Proof Size Estimate:** 448 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 16 | commit round 17 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 35 | 115 | 104 | 94 | 95 | 104 | 105 | 106 | 107 | 108 | 109 | 110 | 111 | 96 | 97 | 98 | 99 | 100 | 101 | 102 | 103 | 35 |
| JBR | 57 | 107 | 96 | 68 | 69 | 78 | 79 | 80 | 81 | 82 | 83 | 84 | 85 | 70 | 71 | 72 | 73 | 74 | 75 | 76 | 77 | 57 |
| best attack | 99 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |


## embed

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 248
- Number of queries: 21
- Grinding (bits): 16
- Field: KoalaBear⁴
- Rate (ρ): 0.0625
- Trace length (H): $2^{15}$
- FRI rounds: 15
- FRI folding factors: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
- FRI early stop degree: 16
- Batching: Powers

**Proof Size Estimate:** 422 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 10 | commit round 11 | commit round 12 | commit round 13 | commit round 14 | commit round 15 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | commit round 8 | commit round 9 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 35 | 115 | 106 | 96 | 97 | 106 | 107 | 108 | 109 | 110 | 111 | 98 | 99 | 100 | 101 | 102 | 103 | 104 | 105 | 35 |
| JBR | 57 | 107 | 98 | 70 | 71 | 80 | 81 | 82 | 83 | 84 | 85 | 72 | 73 | 74 | 75 | 76 | 77 | 78 | 79 | 57 |
| best attack | 99 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |

