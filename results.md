# zkEVM soundcalc report

Each row is a zkEVM proof system.
Each column is a different component of the proof system.
The cell values are the bits of security for each such component.

## zkEVMs
- [ZisK](#zisk)
- [miden](#miden)
- [risc0](#risc0)
- [Pico](#pico)

## ZisK

**Parameters:**
- Number of queries: 128
- Grinding (bits): 0
- Field: Goldilocks^3
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- Batching: Powers

**Proof Size Estimate:** 1352 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | FRI batching round | FRI commit round 1 | FRI commit round 2 | FRI commit round 3 | FRI commit round 4 | FRI commit round 5 | FRI query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 185 | 167 | 162 | 165 | 165 | 165 | 165 | 165 | 53 |
| JBR | 58 | 181 | 163 | 142 | 159 | 159 | 159 | 159 | 159 | 58 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |

## miden

**Parameters:**
- Number of queries: 27
- Grinding (bits): 16
- Field: Goldilocks^2
- Rate (ρ): 0.125
- Trace length (H): $2^{18}$
- Batching: Powers

**Proof Size Estimate:** 114 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | FRI batching round | FRI commit round 1 | FRI commit round 2 | FRI commit round 3 | FRI commit round 4 | FRI commit round 5 | FRI commit round 6 | FRI commit round 7 | FRI query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 38 | 121 | 106 | 100 | 105 | 105 | 105 | 105 | 105 | 105 | 105 | 38 |
| JBR | 55 | 115 | 101 | 77 | 98 | 98 | 98 | 98 | 98 | 98 | 98 | 55 |
| best attack | 96 | — | — | — | — | — | — | — | — | — | — | — |

## risc0

**Parameters:**
- Number of queries: 50
- Grinding (bits): 0
- Field: BabyBear^4
- Rate (ρ): 0.25
- Trace length (H): $2^{21}$
- Batching: Powers

**Proof Size Estimate:** 223 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | FRI batching round | FRI commit round 1 | FRI commit round 2 | FRI commit round 3 | FRI commit round 4 | FRI query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 33 | 115 | 100 | 92 | 96 | 96 | 96 | 96 | 33 |
| JBR | 47 | 110 | 95 | 70 | 90 | 90 | 90 | 90 | 47 |
| best attack | 99 | — | — | — | — | — | — | — | — |

## Pico

**Parameters:**
- Number of queries: 84
- Grinding (bits): 16
- Field: KoalaBear^4
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- Batching: Powers

**Proof Size Estimate:** 908 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | FRI batching round | FRI commit round 1 | FRI commit round 10 | FRI commit round 11 | FRI commit round 12 | FRI commit round 13 | FRI commit round 14 | FRI commit round 15 | FRI commit round 16 | FRI commit round 17 | FRI commit round 18 | FRI commit round 19 | FRI commit round 2 | FRI commit round 20 | FRI commit round 21 | FRI commit round 3 | FRI commit round 4 | FRI commit round 5 | FRI commit round 6 | FRI commit round 7 | FRI commit round 8 | FRI commit round 9 | FRI query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 50 | 113 | 99 | 90 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 50 |
| JBR | 54 | 109 | 95 | 70 | 94 | 94 | 94 | 94 | 94 | 94 | 94 | 94 | 94 | 94 | 94 | 94 | 94 | 94 | 94 | 94 | 94 | 94 | 94 | 94 | 94 | 54 |
| best attack | 99 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
