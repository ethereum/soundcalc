# 📊 OpenVM2 (v2.0.0-beta)

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimates are indicative (1 KiB = 1024 bytes)

## zkVM Overview

| Metric | Value | Relevant circuit | Notes |
| --- | --- | --- | --- |
| Final proof size (worst case) | **140 KiB** | [root](#root) | |
| Final bits of security | **100 bits** | [app](#app) | Regime: UDR |

## Circuits

- [app](#app)
- [leaf](#leaf)
- [internal](#internal)
- [root](#root)

## app

**Parameters:**
- Proof system: SWIRL
- Inner PCS: WHIR
- Field: BabyBear⁴
- Regime: UDR
- `l_skip`: 4
- `n_stack`: 20
- `w_stack`: 2048
- Log blowup: 1
- WHIR queries per round: [193, 88, 81, 81]
- WHIR folding PoW (bits): 5
- WHIR query-phase PoW (bits): 20
- WHIR μ PoW (bits): 15
- Max constraints per AIR: 5000
- Number of AIRs: 100
- Max log trace height: 24
- Number of trace columns: 30000
- Max interactions per AIR: 1000

**Proof Size:** 24165 KiB (expected) / 24272 KiB (worst case)

| regime | total | OOD(i=1) | OOD(i=2) | OOD(i=3) | Shift(i=1) | Shift(i=2) | Shift(i=3) | batching | constraint_batching | fin | fold(i=0,s=1) | fold(i=0,s=2) | fold(i=0,s=3) | fold(i=0,s=4) | fold(i=1,s=1) | fold(i=1,s=2) | fold(i=1,s=3) | fold(i=1,s=4) | fold(i=2,s=1) | fold(i=2,s=2) | fold(i=2,s=3) | fold(i=2,s=4) | fold(i=3,s=1) | fold(i=3,s=2) | fold(i=3,s=3) | fold(i=3,s=4) | gkr_batching | gkr_sumcheck | logup | stacked_reduction | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 100 | 104 | 108 | 112 | 100 | 100 | 100 | 104 | 111.3 | 100 | 106 | 107 | 108 | 109 | 106 | 107 | 108 | 109 | 107 | 108 | 109 | 110 | 108 | 109 | 110 | 111 | 123.6 | 122.0 | 102 | 107.8 | 117.4 |


## leaf

**Parameters:**
- Proof system: SWIRL
- Inner PCS: WHIR
- Field: BabyBear⁴
- Regime: UDR
- `l_skip`: 4
- `n_stack`: 17
- `w_stack`: 2048
- Log blowup: 2
- WHIR queries per round: [118, 84, 81]
- WHIR folding PoW (bits): 4
- WHIR query-phase PoW (bits): 20
- WHIR μ PoW (bits): 13
- Max constraints per AIR: 1000
- Number of AIRs: 50
- Max log trace height: 20
- Number of trace columns: 2000
- Max interactions per AIR: 100

**Proof Size:** 14775 KiB (expected) / 14840 KiB (worst case)

| regime | total | OOD(i=1) | OOD(i=2) | Shift(i=1) | Shift(i=2) | batching | constraint_batching | fin | fold(i=0,s=1) | fold(i=0,s=2) | fold(i=0,s=3) | fold(i=0,s=4) | fold(i=1,s=1) | fold(i=1,s=2) | fold(i=1,s=3) | fold(i=1,s=4) | fold(i=2,s=1) | fold(i=2,s=2) | fold(i=2,s=3) | fold(i=2,s=4) | gkr_batching | gkr_sumcheck | logup | stacked_reduction | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 100 | 107 | 111 | 100 | 100 | 104 | 113.7 | 100 | 107 | 108 | 109 | 110 | 107 | 108 | 109 | 110 | 108 | 109 | 110 | 111 | 123.6 | 122.0 | 102 | 111.7 | 117.4 |


## internal

**Parameters:**
- Proof system: SWIRL
- Inner PCS: WHIR
- Field: BabyBear⁴
- Regime: JBR
- `m`: 2
- `l_skip`: 2
- `n_stack`: 17
- `w_stack`: 512
- Log blowup: 3
- WHIR queries per round: [68, 30, 20]
- WHIR folding PoW (bits): 18
- WHIR query-phase PoW (bits): 20
- WHIR μ PoW (bits): 20
- Max constraints per AIR: 1000
- Number of AIRs: 50
- Max log trace height: 19
- Number of trace columns: 2000
- Max interactions per AIR: 100

**Proof Size:** 2164 KiB (expected) / 2186 KiB (worst case)

| regime | total | OOD(i=1) | OOD(i=2) | Shift(i=1) | Shift(i=2) | batching | constraint_batching | fin | fold(i=0,s=1) | fold(i=0,s=2) | fold(i=0,s=3) | fold(i=0,s=4) | fold(i=1,s=1) | fold(i=1,s=2) | fold(i=1,s=3) | fold(i=1,s=4) | fold(i=2,s=1) | fold(i=2,s=2) | fold(i=2,s=3) | fold(i=2,s=4) | gkr_batching | gkr_sumcheck | logup | stacked_reduction | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JBR | 100 | 100 | 101 | 100 | 100 | 102 | 116.5 | 103 | 110 | 111 | 112 | 113 | 106 | 107 | 108 | 109 | 103 | 104 | 105 | 106 | 123.6 | 122.0 | 105 | 114.5 | 122.1 |


## root

**Parameters:**
- Proof system: SWIRL
- Inner PCS: WHIR
- Field: BabyBear⁴
- Regime: JBR
- `m`: 1
- `l_skip`: 2
- `n_stack`: 18
- `w_stack`: 18
- Log blowup: 4
- WHIR queries per round: [57, 28, 19]
- WHIR folding PoW (bits): 20
- WHIR query-phase PoW (bits): 20
- WHIR μ PoW (bits): 20
- Max constraints per AIR: 1000
- Number of AIRs: 50
- Max log trace height: 21
- Number of trace columns: 2000
- Max interactions per AIR: 100

**Proof Size:** 121 KiB (expected) / 140 KiB (worst case)

| regime | total | OOD(i=1) | OOD(i=2) | Shift(i=1) | Shift(i=2) | batching | constraint_batching | fin | fold(i=0,s=1) | fold(i=0,s=2) | fold(i=0,s=3) | fold(i=0,s=4) | fold(i=1,s=1) | fold(i=1,s=2) | fold(i=1,s=3) | fold(i=1,s=4) | fold(i=2,s=1) | fold(i=2,s=2) | fold(i=2,s=3) | fold(i=2,s=4) | gkr_batching | gkr_sumcheck | logup | stacked_reduction | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JBR | 100 | 100 | 101 | 100 | 101 | 107 | 116.2 | 103 | 112 | 113 | 114 | 115 | 108 | 109 | 110 | 111 | 105 | 106 | 107 | 108 | 123.6 | 122.0 | 105 | 114.2 | 121.8 |

