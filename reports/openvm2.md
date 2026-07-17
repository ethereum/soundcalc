# 📊 OpenVM2 (v2.0.0)

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimates are indicative (1 KiB = 1024 bytes)

## zkVM Overview

| Metric | Value | Relevant circuit | Notes |
| --- | --- | --- | --- |
| Final bits of security | **100 bits** | [app](#app) | Regime: UDR |
| Final proof size | **270 KiB** | [root](#root) | |

## Circuits

- [app](#app)
- [leaf](#leaf)
- [internal_for_leaf](#internal_for_leaf)
- [internal_recursive](#internal_recursive)
- [hook](#hook)
- [root](#root)

## app

**Parameters:**
- Proof system: SWIRL
- PCS: WHIR
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
- Max constraints per AIR: 3183
- Number of AIRs: 72
- Max log trace height: 24
- Number of trace columns: 24381
- Max interactions per AIR: 976
- Soundness max constraints per AIR: 5000
- Soundness number of AIRs bound: 100
- Soundness max log trace height bound: 24
- Soundness trace columns bound: 30000
- Soundness max interactions per AIR bound: 1000
- Proof-size number of AIRs bound: 100
- Proof-size max log trace height bound: 24
- Proof-size trace columns bound: 30000
- Proof-size max interactions per AIR bound: 1000
- Proof-size public values bound: 20

**Proof Size:** 26175 KiB

| regime | total | constraint_batching | gkr_batching | gkr_sumcheck | logup | stacked_reduction | whir | whir_fold_rbr | whir_gamma_batching | whir_mu_batching | whir_ood_rbr | whir_proximity_gaps | whir_query | whir_shift_rbr | whir_sumcheck | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 100 | 111 | 123 | 122 | 102 | 107 | 100 | 104 | 116 | 102 | 104 | 104 | 100 | 100 | 127 | 117 |


## leaf

**Parameters:**
- Proof system: SWIRL
- PCS: WHIR
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
- Max constraints per AIR: 282
- Number of AIRs: 42
- Max log trace height: 21
- Number of trace columns: 1679
- Max interactions per AIR: 78
- Soundness max constraints per AIR: 1000
- Soundness number of AIRs bound: 50
- Soundness max log trace height bound: 21
- Soundness trace columns bound: 2000
- Soundness max interactions per AIR bound: 100
- Proof-size number of AIRs bound: 50
- Proof-size max log trace height bound: 21
- Proof-size trace columns bound: 2000
- Proof-size max interactions per AIR bound: 100
- Proof-size public values bound: 121

**Proof Size:** 15509 KiB

| regime | total | constraint_batching | gkr_batching | gkr_sumcheck | logup | stacked_reduction | whir | whir_fold_rbr | whir_gamma_batching | whir_mu_batching | whir_ood_rbr | whir_proximity_gaps | whir_query | whir_shift_rbr | whir_sumcheck | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 100 | 113 | 123 | 122 | 102 | 111 | 100 | 105 | 116 | 102 | 107 | 105 | 100 | 100 | 126 | 117 |


## internal_for_leaf

**Parameters:**
- Proof system: SWIRL
- PCS: WHIR
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
- Max constraints per AIR: 282
- Number of AIRs: 42
- Max log trace height: 19
- Number of trace columns: 1663
- Max interactions per AIR: 78
- Soundness max constraints per AIR: 1000
- Soundness number of AIRs bound: 50
- Soundness max log trace height bound: 19
- Soundness trace columns bound: 2000
- Soundness max interactions per AIR bound: 100
- Proof-size number of AIRs bound: 50
- Proof-size max log trace height bound: 19
- Proof-size trace columns bound: 2000
- Proof-size max interactions per AIR bound: 100
- Proof-size public values bound: 121

**Proof Size:** 2393 KiB

| regime | total | constraint_batching | gkr_batching | gkr_sumcheck | logup | stacked_reduction | whir | whir_fold_rbr | whir_gamma_batching | whir_mu_batching | whir_ood_rbr | whir_proximity_gaps | whir_query | whir_shift_rbr | whir_sumcheck | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JBR | 100 | 110 | 123 | 122 | 100 | 108 | 100 | 103 | 111 | 102 | 100 | 103 | 100 | 100 | 134 | 116 |


## internal_recursive

**Parameters:**
- Proof system: SWIRL
- PCS: WHIR
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
- Max constraints per AIR: 282
- Number of AIRs: 42
- Max log trace height: 19
- Number of trace columns: 1663
- Max interactions per AIR: 78
- Soundness max constraints per AIR: 1000
- Soundness number of AIRs bound: 50
- Soundness max log trace height bound: 19
- Soundness trace columns bound: 2000
- Soundness max interactions per AIR bound: 100
- Proof-size number of AIRs bound: 50
- Proof-size max log trace height bound: 19
- Proof-size trace columns bound: 2000
- Proof-size max interactions per AIR bound: 100
- Proof-size public values bound: 121

**Proof Size:** 2393 KiB

| regime | total | constraint_batching | gkr_batching | gkr_sumcheck | logup | stacked_reduction | whir | whir_fold_rbr | whir_gamma_batching | whir_mu_batching | whir_ood_rbr | whir_proximity_gaps | whir_query | whir_shift_rbr | whir_sumcheck | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JBR | 100 | 110 | 123 | 122 | 100 | 108 | 100 | 103 | 111 | 102 | 100 | 103 | 100 | 100 | 134 | 116 |


## hook

**Parameters:**
- Proof system: SWIRL
- PCS: WHIR
- Field: BabyBear⁴
- Regime: JBR
- `m`: 1
- `l_skip`: 2
- `n_stack`: 18
- `w_stack`: 80
- Log blowup: 2
- WHIR queries per round: [193, 42, 24]
- WHIR folding PoW (bits): 12
- WHIR query-phase PoW (bits): 20
- WHIR μ PoW (bits): 11
- Max constraints per AIR: 1000
- Number of AIRs: 50
- Max log trace height: 20
- Number of trace columns: 2000
- Max interactions per AIR: 100
- Proof-size public values bound: 18

**Proof Size:** 1330 KiB

| regime | total | constraint_batching | gkr_batching | gkr_sumcheck | logup | stacked_reduction | whir | whir_fold_rbr | whir_gamma_batching | whir_mu_batching | whir_ood_rbr | whir_proximity_gaps | whir_query | whir_shift_rbr | whir_sumcheck | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JBR | 100 | 112 | 123 | 122 | 101 | 110 | 100 | 102 | 112 | 100 | 102 | 102 | 100 | 100 | 129 | 118 |


## root

**Parameters:**
- Proof system: SWIRL
- PCS: WHIR
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
- Proof-size public values bound: 16

**Proof Size:** 270 KiB

| regime | total | constraint_batching | gkr_batching | gkr_sumcheck | logup | stacked_reduction | whir | whir_fold_rbr | whir_gamma_batching | whir_mu_batching | whir_ood_rbr | whir_proximity_gaps | whir_query | whir_shift_rbr | whir_sumcheck | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JBR | 100 | 111 | 123 | 122 | 100 | 109 | 100 | 105 | 112 | 107 | 100 | 105 | 100 | 100 | 136 | 117 |
