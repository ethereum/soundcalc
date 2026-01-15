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
- Grinding (bits): 28
- Field: M31⁴
- Rate (ρ): 0.5
- Trace length (H): $2^{24}$
- FRI rounds: 5
- FRI folding factors: [16, 16, 16, 8, 8]
- FRI early stop degree: 128
- Number of columns: 1224
- Batch size: 1225
- Batching: Powers

**Proof Size:** 1836 KiB (expected) / 1951 KiB (worst case)

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 64 | 113 | 98 | 88 | 99 | 103 | 107 | 111 | 114 | 64 |
| JBR | 63 | 108 | 93 | 63 | 73 | 77 | 81 | 85 | 88 | 67 |
