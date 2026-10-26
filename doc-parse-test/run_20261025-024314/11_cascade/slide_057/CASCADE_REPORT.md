# CASCADE_REPORT — slide_057 (wave-5 parse-driven recursive crop cascade)

Scope `slide_057_cascade` · worker `worker-slide_057_cascade` · 2026-10-25 · run
`doc-parse-test/run_20261025-024314`. Source frame 960×540
(`videos/deep-learning/002_transformers_part2/unique_slides/slide_057.jpg`).

**Resume provenance:** the first worker banked the full parse leg (17 call dirs, 16 crops,
manifest) and died at the judge leg (host restart 09:28 lost a 0/14 judge run; a 17:38
foreground judge pair was lost to a session exit). This resume worker completed the judge leg,
composed the final file, filled the manifest's null fields, and wrote this report. No new
full-frame parse calls, no new crops (16/16 cap), manifest schema untouched (`nodes` key kept).

## Headline

**Union transcript recall 12.5% → 49.0%** (23.5/48 = 19 EXACT + 9 NORM; frozen wave-2 baseline
6/48). **16 crops — the 16/16 backstop cap was reached** — **17 parse calls (17/24 cap)**, all
EXIT=0 finish=stop, zero full-frame calls. **Parallel parse speedup ~2.3×** (177 s summed call
latency vs 78 s active wall across 6 parallel batches).

## Recall trajectory

| stage | union recall | strings |
|---|---|---|
| frozen wave-2 (4 full-frame calls, 1024/3000 tok) | 12.5% (6/48) | all finish=length, `Decoder` ×482 loop |
| wave-3 t9k pair (9000 tok) | 12.5% (unchanged) | loop is budget-independent |
| wave-4 vj union (12 crop calls, prior art) | 46.9% (22.5/48) | 14 EXACT + 8 NORM + 1 PARTIAL |
| **wave-5 cascade (this scope, 17 calls)** | **49.0% (23.5/48)** | 19 EXACT + 9 NORM |
| (read-only prior art: `12_cascade_v2` scope, 19 calls) | 61.5% (29.5/48) | separate completed scope; remains the best variant |

This cascade's captures: `Word 0`–`Word 5` + both embedding labels (8 EXACT, crop02 — the
word row the full frame never read; the unlock was the `Word Embedding` title working as an
in-crop anchor so crop-scale reads the word row), `Encoder Block M` (crop01, judge-verified),
`Encoder Block 1/0` (crop03), `Attention` legend (crop07), `Word and Position Encoding`
(crop06, judge-verified — settles the Encoding-vs-Embedding divergence in the build's favor),
`K` (crop09) = +13.0 EXACT; plus NORMs `Encode Decoder Attention` (crop05 ×6 — first-ever read
of the 3-line blue-box labels), `Multi-Head Self Attention` (crop06, judge-verified ink),
`Word N-2`, and Y-chips `Y_0/1/2/3/5` (crop08) = +4.5.

## Calls, caps, judges

| leg | count | cap | note |
|---|---|---|---|
| full-frame parse calls | 0 | — | forbidden by scope; regions from banked call01_pass1/t9k + wave-4 judge defects |
| crop parse calls | 17 | 24 | 16 primary + 1 corroboration (`call19`, crop05 @3000 tok); all EXIT=0 |
| crops | 16 | **16 — CAP REACHED** | L1×7, L2×7, L3×2; any further sub-crop (e.g. re-crop of the "Wind N" garble) blocked by the cap |
| gateway probe | 1 | — | `PROBE-OK` rc=0 in 2.6 s (`judges/probe_resume.log`) |
| crop judges | 8 attempts / 4 banked | 6 targeted (highest-value) | crop01/02/05/06 banked rc=0 with FINAL VERDICT; crop08/09 rc=124 twice (see Blockers) |

## Wall-clock & parallelism (parse leg, from call.log timestamps)

| batch | calls | Σ latency | wall | speedup |
|---|---|---|---|---|
| B1 08:26:55 (crop01–04) | 4 | 34 s | 11 s | 3.1× |
| B2 08:28:22 (crop05–07) | 3 | 73 s | 31 s | 2.4× |
| B3 08:33:16 (crop08–11) | 4 | 40 s | 16 s | 2.5× |
| B4 08:33:32 (crop12–14) | 3 | 10 s | 4 s | 2.5× |
| B5 08:39:18 (crop15–16) | 2 | 9 s | 5 s | 1.8× |
| B6 08:41:06 (corrob crop05) | 1 | 11 s | 11 s | 1.0× |
| **total** | **17** | **177 s** | **78 s** | **~2.3×** |

Per-call: 10.4 s avg vs 84.0 s avg for the 6 banked full-frame calls (8.1× faster per call);
17/17 finish=stop vs 6/6 full-frame finish=length. Idle gaps between batches (worker-side
curation between recursions) are excluded from the active-wall figure. Judge legs are
sequential by rule (max 1 in-flight) and excluded from the parse speedup figure.

## Per-crop yield

| crop | L | novel strings | GT weighted | outcome |
|---|---|---|---|---|
| 01_enc_top_ychips_bars | 1 | 1 | +1.0 | `Encoder Block M` EXACT, judge-VERIFIED; judge also transcribed the full Y-chip row in-crop |
| 02_enc_bottom_emb | 1 | 9 | +8.5 | `Word 0–5` + `Word Embedding` + `Positional Encoding / Embedding` EXACT (judge-VERIFIED); `Word N2` NORM; the word-row unlock |
| 03_enc_mid_bars_vlabel | 1 | 2 | +2.0 | `Encoder Block 1/0` EXACT + vertical `Encoder`; scaffold headers garble |
| 04_central_kv | 1 | 0 | 0 | legend re-yield only |
| 05_dec_top_bars_attn | 1 | 2 | +0.5 | `Encode Decoder Attention` NORM ×6 (judge: 3-line ink, 10 boxes); FFN true separator "/" judge-read |
| 06_dec_bottom_tokens | 1 | 2 | +1.5 | `Multi-Head Self Attention` NORM (judge-VERIFIED) + `Word and Position Encoding` EXACT (judge-VERIFIED) |
| 07_legend | 1 | 1 | +1.0 | `Attention` EXACT (legend 3/3 complete) |
| 08_ychips_tight | 2 | 7 | +2.5 | `Y_0/1/2/3/5` NORM; garbles adjudicated via crop01 judge (same row in its crop) |
| 09_kv_column | 2 | 4 | +1.0 | `K` EXACT; `Read Forward` ×3 NOT-IN-GT candidate (judge unadjudicated) |
| 10_xchips_tight | 2 | 7 | 0 | `Wired 0–5/M2` garble family (X-row) |
| 11_wordrow_tight | 2 | 0 | 0 | empty shell — anchor-less word strip |
| 12_softmax_bar | 2 | 1 | 0 | `SOHmax` ligature garble (judge crop05 read the ink "Softmax") |
| 13_bottom_tokens | 2 | 1 | 0 | dup of crop06's `Word and Position Encoding` |
| 14_big_q | 2 | 5 | 0 | edge partials `T`/`0`/`rmalization` + dups; Q glyph-only, anchor-less |
| 15_ynum_chips_right | 3 | 0 | 0 | empty shell |
| 16_xnum_chips_right | 3 | 3 | 0 | `Wind 4/5/M2` garble; would warrant re-crop — blocked by cap |
| **total** | | **45** | **+18.0** | pass1 5.5 → union 23.5/48 = 49.0% |

## Recursion tree (16 nodes; stop_reason from manifest.json)

```
slide_057 [full-frame LOOP — never re-parsed (6/6 banked full-frame calls finish=length);
           region source = banked call01_pass1/t9k + wave-4 judge defects (provenance judge-supplement)]
├─ L1 crop01_enc_top_ychips_bars (judge-supplement, 3×, box 86,89–462,241)
│    → "Encoder Block M" [judge VERIFIED] + Y-chip row + corner class_Picture artifact
│   └─ L2 crop08_ychips_tight (gt-gap, 3×)
│        → "Yo Y1 Y2 Y3 Y5 .. Y6 Yx1 Yx1" → 5 NORM Y-chips
│       └─ L3 crop15_ynum_chips_right (gt-gap, 3×)
│            → EMPTY shell → STOP no-new-information
│        → STOP no-new-information (garbles stable at 3×; adjudicated by crop01 judge)
├─ L1 crop02_enc_bottom_emb (judge-supplement, 3×, box 86,406–462,522)
│    → ranked_table: Word Embedding, PE/E, Word 0..5, Word N2 [+8.5]
│   └─ L2 crop10_xchips_tight (gt-gap, 3×)
│        → "Wired 0..5, Wired M2" → STOP no-new-information
│       └─ L3 crop16_xnum_chips_right (gt-gap, 3×)
│            → "Wind 4/5, Wind M2" → STOP backstop (16/16 crop cap reached)
│   └─ L2 crop11_wordrow_tight (parse-block+gt-gap, 3×)
│        → EMPTY shell (anchor-less strip) → STOP no-new-information
│    → branch end STOP no-new-information (word row captured at parent scale)
├─ L1 crop03_enc_mid_bars_vlabel (judge-supplement, 3×, box 44,244–464,401)
│    → "Encoder Block 1/0" + vertical Encoder + scaffold → STOP no-new-information
├─ L1 crop04_central_kv (judge-supplement, 3×, box 424,76–596,454)
│    → legend Encoder/Decoder reads
│   └─ L2 crop09_kv_column (gt-gap, 3×)
│        → "K" EXACT + "Read Forward" ×3 garble → STOP no-new-information
├─ L1 crop05_dec_top_bars_attn (judge-supplement, 3×, box 569,49–871,356)
│    → "Encode Decoder Attention" ×6 + FFN-RELU
│   └─ L2 crop12_softmax_bar (gt-gap, 3×)
│        → "SOHmax" → STOP no-new-information
├─ L1 crop06_dec_bottom_tokens (judge-supplement, 3×, box 569,395–871,525)
│    → "Multi-Head Self Attention" + "Word and Position Encoding"
│   ├─ L2 crop13_bottom_tokens (gt-gap, 3×) → dup WPE → STOP no-new-information
│   └─ L2 crop14_big_q (gt-gap, 3×) → edge partials + dups → STOP no-new-information
└─ L1 crop07_legend (judge-supplement, 3×, box 419,401–591,509)
     → "Encoder / Decoder / Attention" 3/3 → STOP no-new-information
```

Stop reasons: **15 × no-new-information, 1 × backstop** (the 16-crop cap; parse-call cap 24,
used 17). Every node carries box_frame_px + scale + transform + parse_call_dir + judge_files +
novel_strings + stop_reason in `manifest.json` — zero null boxes (the resume worker filled the
previously-null stop_reason/parse_call_dir/novel_strings/judge_files fields from banked
evidence; schema unchanged).

## Blockers

- **crop08 judge (Y-chips tight):** attempt-1 rc=124 (gateway leg exceeded the 340 s wall),
  attempt-2 rc=124 (420 s wall, `--timeout 380`). The gateway itself was healthy (probe
  `PROBE-OK` 2.6 s; four other crop judges completed in 1–2 min). Mitigation: the identical
  Y-chip row lies inside crop01's crop and the crop01 judge transcribed all 8 chips with true
  forms (Y₀ Y₁ Y₂ Y₃ Y₄ Y₅ Y₍N-2₎ Y₍N-1₎) and positions — crop08's garbles are adjudicated by
  proxy; no scoring impact (Y_4/Y_{N-2}/Y_{N-1} were transcript misses either way).
- **crop09 judge (KV column):** attempt-1 rc=124, attempt-2 rc=124 (same signature).
  Consequence: `K` rests on the single-glyph parse read + GT badge census (no judge
  confirmation), and `Read Forward` ×3 stays an unadjudicated NOT-IN-GT hallucination
  candidate in the composed analysis. No recall impact (K counts 1.0 as a transcript string;
  Read Forward counts 0.0 either way).
- No other blockers; all deliverables landed.

## Remaining misses (20 strings, 24.5 weighted — parked with failure evidence)

- `X_0`–`X_{N-1}` (8): stable "Wired/Wind N" word-shape misread in this wave (mirrors v2's
  3-geometry finding) — parser prior, not legibility.
- `Word N-1` (1): never emitted by any parse; judge crop02 confirms it legible at (405–440,
  476–495) — a pure parse-omission target for a future pass.
- `Y_4`, `Y_{N-2}`, `Y_{N-1}` (3): chip garbles (Y5-slot confusion, Yx1 mush); judge confirms
  the true forms on-image.
- `Softmax` (1): "SOHmax" ligature garble; judge crop05 read the ink verbatim "Softmax".
- `V`, `Q` (2): glyph-only badges, anchor-less; Q judge-confirmed on-image at (833, 429).
- `SOS`, `Je`, `ne`, `suis`, `faisait` (5): sub-6 px token glyphs; judge crop06 read the row
  ≈"SOS je ne sais résultat" (last tokens low-confidence) — ink present, parser below
  legibility at the 3× scale cap.

## Honesty notes

- Headline is transcript-level recall (what doc-parse emitted across the 18 merged
  transcripts); judge-confirmed ink that no parse emitted (Word N-1, Softmax, token row, Q) is
  annotated in `compose/COMPOSED_ANALYSIS.md` but NOT scored.
- doc-parse's prompt remains non-editable (wire contract); all gains came from crop geometry
  (anchors inside crops), parse-driven recursion, and judge-supplement targeting.
- `12_cascade_v2/` (read-only) remains the stronger variant (61.5%); this scope's deliverables
  are complete and self-consistent at 49.0%.
