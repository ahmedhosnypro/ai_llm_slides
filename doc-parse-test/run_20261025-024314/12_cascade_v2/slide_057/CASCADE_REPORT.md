# CASCADE_REPORT — slide_057 (wave-5B requirement-compliant crop cascade)

Scope `slide_057_cascade_v2` · worker `worker-slide_057_cascade_v2` · 2026-10-25 · run
`doc-parse-test/run_20261025-024314`. Source frame 960×540
(`videos/deep-learning/002_transformers_part2/unique_slides/slide_057.jpg`). The full frame was
NEVER re-parsed (6/6 historical full-frame calls loop with finish=length; crop-first is the whole
game) — the region source was the banked `call01_pass1`/t9k transcripts, supplemented per protocol
with wave-4 judge-defect regions (provenance `judge-supplement`).

## Headline

**Union transcript recall 12.5% → 61.5%** (29.5/48; wave-4 vj mark 46.9% beaten by +14.6 pp).
**16 crops, 19 parse calls** (all EXIT=0, finish=stop; zero full-frame calls), **parallel speedup
~2.4×** (115 s summed call latency vs 48 s wall across 5 parallel batches).

## Recall trajectory

| stage | union recall | strings |
|---|---|---|
| frozen wave-2 (4 full-frame calls, 1024/3000 tok) | 12.5% (6/48) | all finish=length, `Decoder` ×482 |
| wave-3 t9k pair (9000 tok) | 12.5% (unchanged) | loop is budget-independent |
| wave-4 vj union (12 crop calls) | 46.9% (22.5/48) | 14 EXACT + 8 NORM + 1 PARTIAL |
| **wave-5B cascade (this scope, 19 calls)** | **61.5% (29.5/48)** | 20 EXACT + 9 NORM + 1 PARTIAL |

This cascade's captures: `Word 0`–`Word 5` (6 EXACT — crop14 + byte-identical corroboration) and
`Multi-Head Self-Attention` (NORM — crop08 "Multi-Head Self Attention" + byte-identical
corroboration) = **+7.0 weighted**. The word row was 0/8 across wave-4's 3 rounds; the unlock was
the **`Word Embedding` title as in-crop anchor** (the crop-scale law: keep text anchors inside
every crop — the anchor-less word strip shelled, and the wrong anchor, "Positional Encoding /
Embedding", poisoned the X-strip with chart scaffolding).

## Recursion tree (16 nodes; parse-driven where the parse carried structure, judge-supplement elsewhere)

```
slide_057 [full-frame LOOP — never re-parsed; region source = banked pass1/t9k]
├─ L1 crop01_badge57 (parse-driven, call01_pass1 block <x_.0586><y_.0789>57, box estimated:true)
│    → "7" + class_Picture(full-crop corner artifact) → STOP no-new-information
├─ L1 crop02_encoder_panel (judge-supplement, encoder container 65,131–448,510, 2×)
│    → class_Chart(full-crop corner; table rows = word boxes misread "Window/Wind")
│    → content-driven sub-targets ↓
├─ L1 crop03_decoder_panel (judge-supplement, decoder panel 555,49–854,516, 2×)
│    → class_Picture(corner; 27-line bar stack; "Sohmax") → content-driven sub-targets ↓
├─ L1 crop04_central_kv (judge-supplement, central 415,85–575,440, 3×)
│    → legend "Encoder/Decoder" + class_Picture(corner) → STOP no-new-information
│   ├─ L2 crop05_xchips_strip (X row; 3×) → class_Chart(corner) "Wind 0..5/M2"
│   │    └─ L3 crop13_xstrip_notitle (title sliver excluded; 3×) → SAME stable misread
│   │         → STOP no-new-information (X row unresolvable: 3 geometries, same garble)
│   ├─ L2 crop06_wordrow_strip (word row alone; 3×) → EMPTY shell → STOP no-new-information
│   │    └─ L3 crop14_wordrow_wembtitle (Word Embedding title anchor; 2×)
│   │         → +6 EXACT `Word 0..Word 5`; class_Chart(corner); "Word M2/M3" garbles
│   │         → STOP backstop (level-4 last-2-boxes crop blocked by the 16-crop cap)
│   ├─ L2 crop07_ychips_tail (Y_5..Y_{N-1}; 3×) → "Y4 Ys1 Yn.1 A" → STOP no-new-information
│   ├─ L2 crop08_bigq_context (Q + MH-SA + purple-bar anchors; 3×) → +1 NORM MH-SA → STOP no-new-information
│   ├─ L2 crop09_tokens_row (tokens minus purple-bar ink; 3×) → shell → STOP no-new-information
│   │    └─ L3 crop16_tokens_left (left half; 3×) → shell → STOP no-new-information (9th token failure)
│   ├─ L2 crop10_attn_box_cluster (2×3 navy boxes; 3×) → shell → STOP no-new-information
│   ├─ L2 crop11_softmax_bar (Softmax bar + neighbors; 3×) → "Sohmax" → STOP no-new-information
│   └─ L2 crop12_mh_sa_row (lavender row; 3×) → "Wall-Head Soft Attention" ×2 → STOP no-new-information
└─ L3 crop15_q_tokens_right (Q + tokens right + purple-bar end; 3×) → shell → STOP no-new-information
```

Stop reasons: **15 × no-new-information, 1 × backstop** (16-crop cap; parse-call cap 24, used 19).
Every node carries box+scale+transform+stop_reason in `manifest.json` — zero null boxes.

## Per-crop yield

| crop | targets | new GT (weighted) | outcome |
|---|---|---|---|
| 01_badge57 | 57 | 0 | "7" partial; 57 already banked full-frame |
| 02_encoder_panel | encoder bars/chips/rows | 0 | region re-yield; word rows garble "Window/Wind" |
| 03_decoder_panel | bar stack | 0 | 27 lines; "Sohmax" first-ever Softmax-ink read |
| 04_central_kv | K/V/Q legend | 0 | legend re-yield |
| 05_xchips_strip | X×8 | 0 | "Wind N" scaffold (title sliver) |
| 06_wordrow_strip | Word×8 | 0 | empty shell (anchor-less) |
| 07_ychips_tail | Y_{N-2} | 0 | 5th garble "Ys1" |
| 08_bigq_context | Q, MH-SA | **+1.0** | "Multi-Head Self Attention" ×2 byte-identical |
| 09_tokens_row | tokens | 0 | shell |
| 10_attn_box_cluster | ED-Attention exact | 0 | shell (volatility: parent read the boxes) |
| 11_softmax_bar | Softmax | 0 | "Sohmax" repeated |
| 12_mh_sa_row | MH-SA | 0 | garble corroboration "Wall-Head Soft Attention" |
| 13_xstrip_notitle | X×8 | 0 | same "Wind N" misread, 3rd geometry |
| 14_wordrow_wembtitle | Word×8 | **+6.0** | Word 0..5 EXACT ×2 reads; N-2/N-1 garbled |
| 15_q_tokens_right | Q, suis/faisait | 0 | shell |
| 16_tokens_left | SOS/Je/ne | 0 | shell |
| **total** | | **+7.0** | 22.5 → 29.5/48 |

## Parallelism & speed

| phase | calls | Σ latency | wall | speedup |
|---|---|---|---|---|
| L1 (×4 in 1 Bash, & + wait) | 4 | 34 s | 19 s | 1.8× |
| L2 batch A (×4) | 4 | 28 s | 9 s | 3.1× |
| L2 batch B (×4) | 4 | 10 s | 4 s | 2.5× |
| L3 (×4) | 4 | 24 s | 8 s | 3.0× |
| corroboration (×3) | 3 | 19 s | 8 s | 2.4× |
| **total** | **19** | **115 s** | **48 s** | **~2.4×** |

Per-call: 6.1 s avg vs 88.7 s avg for the full-frame calls (14.6× faster per call), 19/19
finish=stop vs 6/6 full-frame finish=length. Vision-gateway judge legs are sequential by rule
(max 1 in-flight) and are excluded from the parse speedup figure.

## Remaining misses (18 strings, 18.0 weighted — parked with failure evidence)

- `X_0`–`X_{N-1}` (8): stable "Wind N" word-shape misread in 3 geometries (with title, without
  title, wave-4 lollipop). The X row is structurally identical to the Y row (which reads 7/8);
  the misread is a parser word-shape prior, not a legibility limit.
- `Word N-2`, `Word N-1` (2): "Word M2/M3" garble; 6 sibling cells exact; level-4 crop blocked by
  the 16-crop backstop.
- `SOS`, `Je`, `ne`, `suis`, `faisait` (5): sub-6 px glyphs; 9 consecutive strip failures across
  3 waves — below parser legibility at the 2–3× scale cap.
- `Y_{N-2}` (1): 5 garbles (YsN/YN/Ys1) — subscript mush at 8.5 pt serif.
- `Q` (1): 3 failures (shell/garble/shell) — glyph-only badge; the parser reads badges only with
  anchors, and no anchor adjoins it.
- `Softmax` (1): "Sohmax" ×3 — stable ligature misread; judge leg (crop03) adjudicated: ink is
  verbatim "Softmax", the 'ft' ligature cluster is dropped by the OCR.

## Honesty notes

- doc-parse's prompt remains non-editable (wire contract); all gains came from input-form
  engineering (anchor-aware crop geometry) + parse-driven recursion + judge-supplement targeting.
- The primary judge for every crop is its doc-parse re-parse (19 banked call dirs). Vision-gateway
  judges (Tier-2, sequential, 60 s-paced retries) were added for the 9 crops with novel strings;
  outcomes banked under `judges/`.
- Recall figures are transcript-level vs the frozen 48-string GT inventory (no new pixel
  adjudication in this wave); classifications per the EXACT/NORMALIZED/PARTIAL rules.
