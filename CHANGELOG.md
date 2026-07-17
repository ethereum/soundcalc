# TOML config changelog

toml format changes, newest-first.

### 2026-07-17 — SWIRL
- allow optional circuit-level `proof_size_*` bounds for OpenVM backend-codec proof size estimates; by default proof sizing uses the corresponding `soundness_*` bound where present
- allow optional circuit-level `soundness_*` bounds to be used for security calculations while reporting the unprefixed circuit shape fields as the actual circuit specs
- allow circuit-level `logup_pow_bits` override, falling back to `[swirl].logup_pow_bits`

### 2026-05-02 — WHIR
- allow custom folding factors in WHIR

### 2026-04-20 (`1d4371a`) — Lookups
- removed `alphabet_size_H`

### 2026-03-16 (`b3f6610`) — FRI
- rename `grinding_bits_batching` → `grinding_batching_phase`
