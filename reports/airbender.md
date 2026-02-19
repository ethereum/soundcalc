# 📊 Airbender

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimates are indicative (1 KiB = 1024 bytes)

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 87
- Grinding query phase (bits): 28
- Grinding commit phase (bits): 4
- Grinding DEEP (bits): 11
- Field: M31⁴
- Rate (ρ): 0.5
- Trace length (H): $2^{24}$
- FRI rounds: 5
- FRI folding factors: [16, 16, 16, 8, 8]
- FRI early stop degree: 128
- Number of constraints: 928
- Batch size: 1225
- Batching: Powers
- Lookup (logup): generic_lookup
- Lookup (logup): range_check_16_lookup
- Lookup (logup): range_check_19_lookup
- Lookup (logup): decoder

**Proof Size:** 1836 KiB (expected) / 1951 KiB (worst case)

| regime | total | generic_lookup | range_check_16_lookup | range_check_19_lookup | decoder | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 64 | 94 | 99 | 98 | 100 | 114 | 109 | 88 | 103 | 107 | 111 | 115 | 118 | 64 |
| JBR | 63 | 94 | 99 | 98 | 100 | 109 | 104 | 63 | 77 | 81 | 85 | 89 | 92 | 67 |
