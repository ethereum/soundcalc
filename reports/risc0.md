# 📊 RISC0

How to read this report:
- Table rows correspond to security regimes
- Table columns correspond to proof system components
- Cells show bits of security per component
- Proof size estimate is only indicative

**Parameters:**
- Polynomial commitment scheme: FRI
- Hash size (bits): 256
- Number of queries: 50
- Grinding (bits): 0
- Field: BabyBear⁴
- Rate (ρ): 0.25
- Trace length (H): $2^{21}$
- FRI rounds: 4
- FRI folding factors: [16, 16, 16, 16]
- FRI early stop degree: 128
- Number of columns: 279
- Batch size: 283
- Batching: Powers

**Proof Size Estimate:** 380.0 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | batching | commit round 1 | commit round 2 | commit round 3 | commit round 4 | query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 33 | 115 | 100 | 92 | 100 | 104 | 108 | 112 | 33 |
| JBR | 48 | 109 | 93 | 63 | 71 | 75 | 79 | 83 | 48 |
| best attack | 99 | — | — | — | — | — | — | — | — |
