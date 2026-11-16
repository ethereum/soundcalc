# TOML config changelog

toml format changes, newest-first.

### 2026-11-08 — SWIRL proof shape
- added optional `proof_size_num_gkr_rounds`, `proof_size_num_column_openings`, `proof_size_num_opening_parts`, `proof_size_num_cached_commitments` and `proof_size_num_commitments` to SWIRL `[[circuits]]` sections: the LogUp-GKR layers, the batch-constraint column openings and opening parts, the cached-trace commitments and the stacked commitments of one proof, for a circuit whose proof shapes are known (for example its largest proof's); unset, each keeps the bound or the OpenVM layout used so far (unset opening parts are `num_airs + num_commitments - 1`, so they follow `proof_size_num_commitments`); only affects the proof size

### 2026-10-23 — Initial commitment
- added optional `initial_tree_widths` to FRI and STIR `[[circuits]]` sections: the number of base field columns in each tree committed before the PCS; if unset, all `batch_size` functions are assumed to live in one tree; only affects the proof size
- added optional `num_evals` (default `0`) to DEEP-ALI `[[circuits]]` sections (FRI, STIR and WHIR): the number of out-of-domain evaluations sent in the proof; only affects the proof size

### 2026-07-23 — SWIRL
- unified SWIRL circuit loading on the OpenVM-style keys; in SWIRL `[[circuits]]` sections: renamed `log_inv_rate` → `log_blowup`, `num_queries` → `whir_num_queries`, `trace_columns` → `num_trace_columns`, `grinding_batching_phase` → `whir_mu_pow_bits`, `swirl_folding_pow_bits` → `whir_folding_pow_bits`
- removed derived SWIRL keys: `num_iterations`, `folding_factors`, `log_degree`, `batch_size`, `power_batching`, `grinding_bits_queries`, `num_ood_samples`, `grinding_bits_ood`, `grinding_bits_folding`, `swirl_whir_k`, `swirl_query_phase_pow_bits`, `air_max_degree`
- moved SWIRL LogUp keys to the `[swirl]` table: `max_interaction_count` → `logup_max_interaction_count`, `log_max_message_length` → `logup_log_max_message_length`, `grinding_bits_lookup` → `logup_pow_bits`
- allow optional circuit-level `proof_size_*` bounds for OpenVM backend-codec proof size estimates; by default proof sizing uses the corresponding `soundness_*` bound where present
- allow optional circuit-level `soundness_*` bounds to be used for security calculations while reporting the unprefixed circuit shape fields as the actual circuit specs
- allow circuit-level `logup_pow_bits` override, falling back to `[swirl].logup_pow_bits`

### 2026-07-23 — Protocol family
- moved `protocol_family` from the `[zkevm]` section to each `[[circuits]]` section, so a VM can mix proof-system families across circuits

### 2026-05-02 — WHIR
- allow custom folding factors in WHIR

### 2026-04-20 (`1d4371a`) — Lookups
- removed `alphabet_size_H`

### 2026-03-16 (`b3f6610`) — FRI
- rename `grinding_bits_batching` → `grinding_batching_phase`
