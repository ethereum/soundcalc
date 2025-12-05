# 📊 Miden

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimate is only indicative

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 27
- Grinding (bits): 16
- Field: Goldilocks²
- Rate (ρ): 0.125
- Trace length (H): $2^{18}$
- FRI rounds: 7
- FRI folding factors: [4, 4, 4, 4, 4, 4, 4]
- FRI early stop degree: 128
- Batching: Powers

**Proof Size Estimate:** 177 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | commit round 5 | commit round 6 | commit round 7 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 38 | 121 | 106 | 100 | 107 | 109 | 111 | 113 | 115 | 117 | 119 | 38 |
| JBR | -2 | 120 | 105 | -2 | 15 | 27 | 39 | 51 | 63 | 75 | 87 | 56 |
| best attack | 96 | — | — | — | — | — | — | — | — | — | — | — |
