# 📊 Airbender

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimates are indicative (1 KiB = 1024 bytes)

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 63
- Grinding (bits): 28
- Field: M31⁴
- Rate (ρ): 0.5
- Trace length (H): $2^{24}$
- FRI rounds: 5
- FRI folding factors: [16, 16, 16, 8, 8]
- FRI early stop degree: 128
- Number of columns: 1224
- Batch size: 1238
- Batching: Powers

**Proof Size:** 1347 KiB (expected) / 1425 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 54 | 113 | 98 | 88 | 99 | 103 | 107 | 111 | 114 | 54 |
| JBR | 56 | 108 | 93 | 63 | 73 | 77 | 81 | 85 | 88 | 56 |
