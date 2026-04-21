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
| Final bits of security | **100.0 bits** | [leaf](#leaf) | Regime: SWIRL |

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

| regime | total | constraint_batching | gkr_batching | gkr_sumcheck | logup | stacked_reduction | whir | whir.fold_rbr | whir.gamma_batching | whir.mu_batching | whir.ood_rbr | whir.proximity_gaps | whir.query | whir.shift_rbr | whir.sumcheck | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWIRL | 100.1 | 111.3 | 123.6 | 122.0 | 102.7 | 107.8 | 100.1 | 106.6 | 116.0 | 104.6 | 104.6 | 106.6 | 100.1 | 100.1 | 127.0 | 117.4 |


## leaf

**Parameters:**
- Proof system: SWIRL
- Inner PCS: WHIR
- Field: BabyBear⁴
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

| regime | total | constraint_batching | gkr_batching | gkr_sumcheck | logup | stacked_reduction | whir | whir.fold_rbr | whir.gamma_batching | whir.mu_batching | whir.ood_rbr | whir.proximity_gaps | whir.query | whir.shift_rbr | whir.sumcheck | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWIRL | 100.0 | 113.7 | 123.6 | 122.0 | 102.7 | 111.7 | 100.0 | 107.0 | 116.7 | 104.0 | 107.6 | 107.0 | 100.0 | 100.0 | 126.0 | 117.4 |


## internal

**Parameters:**
- Proof system: SWIRL
- Inner PCS: WHIR
- Field: BabyBear⁴
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

| regime | total | constraint_batching | gkr_batching | gkr_sumcheck | logup | stacked_reduction | whir | whir.fold_rbr | whir.gamma_batching | whir.mu_batching | whir.ood_rbr | whir.proximity_gaps | whir.query | whir.shift_rbr | whir.sumcheck | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWIRL | 100.1 | 116.5 | 123.6 | 122.0 | 105.5 | 114.5 | 100.1 | 103.1 | 112.9 | 102.1 | 101.0 | 103.1 | 100.1 | 100.1 | 134.2 | 122.1 |


## root

**Parameters:**
- Proof system: SWIRL
- Inner PCS: WHIR
- Field: BabyBear⁴
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

| regime | total | constraint_batching | gkr_batching | gkr_sumcheck | logup | stacked_reduction | whir | whir.fold_rbr | whir.gamma_batching | whir.mu_batching | whir.ood_rbr | whir.proximity_gaps | whir.query | whir.shift_rbr | whir.sumcheck | zerocheck_sumcheck |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWIRL | 100.5 | 116.2 | 123.6 | 122.0 | 105.3 | 114.2 | 100.5 | 105.3 | 113.2 | 107.2 | 100.5 | 105.3 | 100.7 | 100.7 | 136.5 | 121.8 |

