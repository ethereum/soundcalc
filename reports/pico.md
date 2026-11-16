# 📊 Pico (v3.1.1)

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimates are indicative (1 KiB = 1024 bytes)

## zkVM Overview

| Metric | Value | Relevant circuit | Notes |
| --- | --- | --- | --- |
| Final bits of security | **128 bits** | [riscv](#riscv) | Regime: mixed |
| Final proof size (worst case) | **292 KiB** | [compress](#compress) | |

## Circuits

- [riscv](#riscv)
- [convert](#convert)
- [combine](#combine)
- [deferred](#deferred)
- [embed](#embed)
- [compress](#compress)

## riscv

**Parameters:**
- Proof system: SWIRL
- PCS: WHIR
- Field: KoalaBear⁵
- Regime: UDR
- `l_skip`: 4
- `n_stack`: 19
- `w_stack`: 640
- Log blowup: 1
- WHIR queries per round: [261, 119, 110, 109]
- WHIR folding PoW (bits): 5
- WHIR query-phase PoW (bits): 20
- WHIR μ PoW (bits): 15
- Max constraints per AIR: 2989
- Number of AIRs: 19
- Max log trace height: 23
- Number of trace columns: 3877
- Max interactions per AIR: 1843
- Proof-size number of AIRs bound: 19
- Proof-size max log trace height bound: 23
- Proof-size trace columns bound: 1450
- Proof-size max interactions per AIR bound: 121
- Proof-size public values bound: 261
- Proof-size GKR rounds: 31
- Proof-size column openings: 1624
- Proof-size opening parts: 21
- Proof-size cached commitments: 0
- Proof-size commitments: 3

**Proof Size:** 11309 KiB (expected) / 11309 KiB (worst case)

| regime | total | constraint_batching | gkr_batching | gkr_sumcheck | logup | stacked_reduction | whir | whir_fold_rbr | whir_gamma_batching | whir_mu_batching | whir_ood_rbr | whir_proximity_gaps | whir_query | whir_shift_rbr | whir_sumcheck | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 128 | 143 | 154 | 153 | 133 | 142 | 128 | 136 | 146 | 136 | 136 | 136 | 128 | 128 | 158 | 149 |


## convert

**Parameters:**
- Proof system: SWIRL
- PCS: WHIR
- Field: KoalaBear⁵
- Regime: UDR
- `l_skip`: 4
- `n_stack`: 17
- `w_stack`: 92
- Log blowup: 2
- WHIR queries per round: [160, 114, 109]
- WHIR folding PoW (bits): 4
- WHIR query-phase PoW (bits): 20
- WHIR μ PoW (bits): 13
- Max constraints per AIR: 170
- Number of AIRs: 21
- Max log trace height: 19
- Number of trace columns: 1409
- Max interactions per AIR: 34
- Proof-size public values bound: 119
- Proof-size GKR rounds: 25
- Proof-size column openings: 1554
- Proof-size opening parts: 42
- Proof-size cached commitments: 0
- Proof-size commitments: 2

**Proof Size:** 1370 KiB (expected) / 1370 KiB (worst case)

| regime | total | constraint_batching | gkr_batching | gkr_sumcheck | logup | stacked_reduction | whir | whir_fold_rbr | whir_gamma_batching | whir_mu_batching | whir_ood_rbr | whir_proximity_gaps | whir_query | whir_shift_rbr | whir_sumcheck | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 128 | 147 | 154 | 153 | 133 | 143 | 128 | 136 | 147 | 138 | 138 | 136 | 128 | 128 | 157 | 148 |


## combine

**Parameters:**
- Proof system: SWIRL
- PCS: WHIR
- Field: KoalaBear⁵
- Regime: UDR
- `l_skip`: 4
- `n_stack`: 17
- `w_stack`: 27
- Log blowup: 2
- WHIR queries per round: [160, 114, 109]
- WHIR folding PoW (bits): 4
- WHIR query-phase PoW (bits): 20
- WHIR μ PoW (bits): 13
- Max constraints per AIR: 170
- Number of AIRs: 21
- Max log trace height: 17
- Number of trace columns: 1409
- Max interactions per AIR: 34
- Proof-size public values bound: 119
- Proof-size GKR rounds: 23
- Proof-size column openings: 1554
- Proof-size opening parts: 42
- Proof-size cached commitments: 0
- Proof-size commitments: 2

**Proof Size:** 715 KiB (expected) / 715 KiB (worst case)

| regime | total | constraint_batching | gkr_batching | gkr_sumcheck | logup | stacked_reduction | whir | whir_fold_rbr | whir_gamma_batching | whir_mu_batching | whir_ood_rbr | whir_proximity_gaps | whir_query | whir_shift_rbr | whir_sumcheck | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 128 | 147 | 154 | 153 | 133 | 143 | 128 | 136 | 147 | 140 | 138 | 136 | 128 | 128 | 157 | 148 |


## deferred

**Parameters:**
- Proof system: SWIRL
- PCS: WHIR
- Field: KoalaBear⁵
- Regime: UDR
- `l_skip`: 4
- `n_stack`: 17
- `w_stack`: 27
- Log blowup: 2
- WHIR queries per round: [160, 114, 109]
- WHIR folding PoW (bits): 4
- WHIR query-phase PoW (bits): 20
- WHIR μ PoW (bits): 13
- Max constraints per AIR: 170
- Number of AIRs: 21
- Max log trace height: 17
- Number of trace columns: 1409
- Max interactions per AIR: 34
- Proof-size public values bound: 119
- Proof-size GKR rounds: 23
- Proof-size column openings: 1554
- Proof-size opening parts: 42
- Proof-size cached commitments: 0
- Proof-size commitments: 2

**Proof Size:** 715 KiB (expected) / 715 KiB (worst case)

| regime | total | constraint_batching | gkr_batching | gkr_sumcheck | logup | stacked_reduction | whir | whir_fold_rbr | whir_gamma_batching | whir_mu_batching | whir_ood_rbr | whir_proximity_gaps | whir_query | whir_shift_rbr | whir_sumcheck | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 128 | 147 | 154 | 153 | 133 | 143 | 128 | 136 | 147 | 140 | 138 | 136 | 128 | 128 | 157 | 148 |


## embed

**Parameters:**
- Proof system: SWIRL
- PCS: WHIR
- Field: KoalaBear⁵
- Regime: JBR
- `m`: 2
- `l_skip`: 4
- `n_stack`: 16
- `w_stack`: 11
- Log blowup: 4
- WHIR queries per round: [65, 34, 24]
- WHIR folding PoW (bits): 16
- WHIR query-phase PoW (bits): 20
- WHIR μ PoW (bits): 18
- Max constraints per AIR: 170
- Number of AIRs: 21
- Max log trace height: 16
- Number of trace columns: 1409
- Max interactions per AIR: 34
- Proof-size public values bound: 119
- Proof-size GKR rounds: 21
- Proof-size column openings: 1554
- Proof-size opening parts: 42
- Proof-size cached commitments: 0
- Proof-size commitments: 2

**Proof Size:** 233 KiB (expected) / 233 KiB (worst case)

| regime | total | constraint_batching | gkr_batching | gkr_sumcheck | logup | stacked_reduction | whir | whir_fold_rbr | whir_gamma_batching | whir_mu_batching | whir_ood_rbr | whir_proximity_gaps | whir_query | whir_shift_rbr | whir_sumcheck | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JBR | 128 | 144 | 154 | 153 | 130 | 140 | 128 | 128 | 142 | 133 | 130 | 128 | 128 | 128 | 163 | 145 |


## compress

**Parameters:**
- Proof system: SWIRL
- PCS: WHIR
- Field: KoalaBear⁵
- Regime: JBR
- `m`: 2
- `l_skip`: 4
- `n_stack`: 16
- `w_stack`: 25
- Log blowup: 4
- WHIR queries per round: [65, 34, 24]
- WHIR folding PoW (bits): 16
- WHIR query-phase PoW (bits): 20
- WHIR μ PoW (bits): 18
- Max constraints per AIR: 170
- Number of AIRs: 21
- Max log trace height: 16
- Number of trace columns: 1409
- Max interactions per AIR: 34
- Proof-size public values bound: 119
- Proof-size GKR rounds: 22
- Proof-size column openings: 1554
- Proof-size opening parts: 42
- Proof-size cached commitments: 0
- Proof-size commitments: 2

**Proof Size:** 292 KiB (expected) / 292 KiB (worst case)

| regime | total | constraint_batching | gkr_batching | gkr_sumcheck | logup | stacked_reduction | whir | whir_fold_rbr | whir_gamma_batching | whir_mu_batching | whir_ood_rbr | whir_proximity_gaps | whir_query | whir_shift_rbr | whir_sumcheck | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JBR | 128 | 144 | 154 | 153 | 130 | 140 | 128 | 128 | 142 | 132 | 130 | 128 | 128 | 128 | 163 | 145 |

