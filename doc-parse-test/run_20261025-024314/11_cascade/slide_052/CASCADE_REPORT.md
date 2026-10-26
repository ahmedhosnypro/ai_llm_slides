# CASCADE REPORT — slide_052_cascade (wave 5, v1 tree)

Run `doc-parse-test/run_20261025-024314` · source frame `videos/deep-learning/002_transformers_part2/unique_slides/slide_052.jpg` (960×540)
Scope `slide_052_cascade` · worker `worker-slide_052_cascade` (fresh worker finishing after the first worker's session was killed mid-judges) · prior art: `12_cascade_v2/slide_052/` (read-only).

## Headline

**Union recall 75.0% → 86.4% transcript-level** (19 EXACT + 0 NORMALIZED + 0 PARTIAL + 3 MISSING of 22 GT units; wave-2 basis and matching rule) — **judge-corroborated coverage 22/22 = 100.0%** (K and V REAL per 2 independent judges each; Y tags REAL per 1 judge, with a `[?]` subscript wording conflict vs the certified build). 12 crops (cap 16) · 12 parse calls (cap 24) · **parallel parse speedup ~2.7×**.

## Recall trajectory

| stage | recall | detail |
|---|---|---|
| wave-2 frozen full-frame | 75.0% (16.5/22) | 16 EXACT + GT5 PARTIAL; MISSING: GT9 SOS legend, GT18 K, GT19 V, GT21 Y, GT22 badge `52` |
| cascade L1 (7 crops) | +GT9, +GT22; GT5 PARTIAL→EXACT; GT20 instances 2/5→5/5 | crop05 recovered the SOS legend; crop07 recovered the badge numeral; crop02 read 5 complete `Encode Decoder Attention` lines + 5× `Q` |
| cascade L2 (3 crops) | +0 transcript | crop08/crop09/crop10: garbles and clips only (`Res`, `Ya`/`Y2`, 5th-box fragments); K/V/Q/Y glyphs unread by doc-parse |
| cascade L3 (2 crops, 6× deviation) | +0 transcript | crop11/crop12: truncated label fragments / zero text; K/V still unread |
| final | **86.4% transcript / 100% judge-corroborated** | trajectory table per element in compose/COMPOSED_ANALYSIS.md |

## Calls & wall-clock

Parse calls (12, all EXIT 0, from `parses/*/call.log`), run in 4 concurrent batches (`&` + `wait`, max 4):

| batch | calls | started | batch wall | Σ individual |
|---|---|---|---|---|
| 1 | call01–call04 | 08:25:17 | 16 s | 56 s |
| 2 | call05–call07 | 08:25:43 | 9 s | 20 s |
| 3 | call8–call10 | 08:28:36 | 10 s | 24 s |
| 4 | call11–call12 | 08:32:20 | 5 s | 7 s |
| **total** | **12** | | **40 s** | **107 s** |

**Parallel speedup ≈ 107/40 ≈ 2.7×** (sum of per-call durations ÷ batched wall-clock; batch gaps between levels were crop-prep time, excluded from both sides). Judge leg (sequential, one in flight): 2 probes (3 s + 3 s, EXIT 0) + 6 judges this session (crop05 68 s, crop07 137 s, crop08 45 s, crop09 140 s, crop10 131 s, crop11 144 s ≈ 11 min) + 2 inherited judge attempts killed by the session exit.

## Per-crop yield

| id | class | lvl | parent | scale | box (frame px) | parse yield (novel = not in full-frame t9k) | judge | stop_reason |
|---|---|---|---|---|---|---|---|---|
| crop01 | picture | 1 | seed | 3.0 | 711,374,960,540 | zero text (full-span Picture; re-read of the (906.5,517.6) hallucination region) | empty (killed) — not required, no novel strings | no-new-information |
| crop02 | upper_boxes | 1 | judge-suppl | 2.8 | 329,155,906,305 | **5× Encode Decoder Attention (GT5 EXACT) + 5× Q (GT20 5/5)** + Residual (GT3) | crop02_judge.md (inherited) | no-new-information |
| crop03 | lower_boxes | 1 | judge-suppl | 2.8 | 329,332,906,428 | 4× Masked Multi-Head Self Attention (GT6 i1–4) | empty (killed) — not required, no novel strings | no-new-information |
| crop04 | left_kv_y | 1 | judge-suppl | 3.0 | 28,145,357,295 | Masked Multi-head Self Attention Block (GT2 tail) | — (no novel strings) | no-new-information |
| crop05 | encoder_inputs | 1 | judge-suppl | 3.0 | 29,286,341,539 | **SOS = Start Of Sentence (GT9, novel→EXACT)** + Transformer Encoder (GT8) + I feel Sick (GT10–12) | crop05_judge.md ✓ | no-new-information |
| crop06 | word_boxes | 1 | judge-suppl | 2.8 | 319,426,906,534 | Word and Position Encoding (GT7) + SOS/Je/me/sens/malade (GT13–17) | — (no novel strings) | no-new-information |
| crop07 | badge | 1 | judge-suppl | 3.0 | 794,16,960,124 | **52 (GT22, novel→EXACT)** | crop07_judge.md ✓ | no-new-information |
| crop08 | kv_q_zone | 2 | crop04 | 3.0 | 264,151,436,274 | Res (GT3 clip) + Encode Decoder Attention (GT5 i1); K/V/Q1 unread | crop08_judge.md ✓ (reads K, V, Q1) | too-small |
| crop09 | y_tags_row | 2 | crop04 | 3.0 | 42,239,268,286 | Ya/Y2 (GT21 garble) | crop09_judge.md ✓ (reads Y₀/Y₁/Y₂) | too-small |
| crop10 | box5_right | 2 | crop03 | 3.0 | 693,332,892,428 | 5th box: Masked/Multi-Head/Self Attention (GT6 i5) + Ml-Head garble | crop10_judge.md ✓ | no-new-information |
| crop11 | kv_tight | 3 | crop08 | 6.0 | 280,154,370,276 | Enc/Deco/Atten (GT5 i1 truncated); K/V unread | crop11_judge.md ✓ (reads K, V) | too-small |
| crop12 | y_tight | 3 | crop09 | 6.0 | 57,241,143,269 | zero text | — (no novel strings) | too-small |

Yield summary: 5 of 12 crops added transcript content; 2 of those recovered previously-MISSING GT units (crop05→GT9, crop07→GT22) and 1 upgraded a PARTIAL to EXACT (crop02→GT5, plus GT20 instance coverage 2/5→5/5). L2/L3 crops yielded zero new doc-parse strings but produced the judge evidence that closes K/V/Y.

## Recursion tree (stop reasons verbatim from manifest.json)

```
slide_052 — full-frame seed call05_t9k (read-only)
├─ L1 crop01_picture        (711,374,960,540) 3.0x — STOP no-new-information (full-span child == parent)
├─ L1 crop02_upper_boxes    (329,155,906,305) 2.8x — STOP no-new-information (full-span Chart carries all content)
├─ L1 crop03_lower_boxes    (329,332,906,428) 2.8x — STOP no-new-information
│  └─ L2 crop10_box5_right  (693,332,892,428) 3.0x — STOP no-new-information (full-span; tighter compliant child impossible)
├─ L1 crop04_left_kv_y      (28,145,357,295) 3.0x — STOP no-new-information (children crop08+crop09 both ran)
│  ├─ L2 crop08_kv_q_zone   (264,151,436,274) 3.0x — STOP too-small (K/V glyphs 15–22 px; 6× child still failed)
│  │  └─ L3 crop11_kv_tight (280,154,370,276) 6.0x — STOP too-small (parser reads glyphs as graphics; terminal)
│  └─ L2 crop09_y_tags_row  (42,239,268,286) 3.0x — STOP too-small (Y tags ~16 px; 6× child returned zero text)
│     └─ L3 crop12_y_tight  (57,241,143,269) 6.0x — STOP too-small (zero text; terminal)
├─ L1 crop05_encoder_inputs (29,286,341,539) 3.0x — STOP no-new-information
├─ L1 crop06_word_boxes     (319,426,906,534) 2.8x — STOP no-new-information
└─ L1 crop07_badge          (794,16,960,124) 3.0x — STOP no-new-information
```

Stops: 8× no-new-information, 4× too-small · 0× leaf, 0× no-internal-structure, 0× backstop · caps: crops 12/16, parse calls 12/24. One documented deviation: crop11/crop12 ran at 6× (spec 2–3×) as the last attempt before a too-small stop on 15–22 px glyphs — recorded in manifest notes.

## Doctrine note — K/V glyph limitation (confirmed in this tree)

**doc-parse cannot resolve the ~15 px K/V circle glyphs at full frame OR at any compliant crop scale.** Full-frame (3 passes, byte-identical): dropped. Crop cascade: 3× zone crop (crop08) read only `Res` + the blue-box label; a 6× tight crop (crop11, 540×732, ≥480 px wide) still returned zero K/V — the parser treats the glyphs as graphics at every scale tried, while both crops' vision judges read K and V cleanly (frame centers within ~1–2 px of the certified build). The same holds for the ~16 px Y tags (garbled `Ya`/`Y2` at 3×, zero text at 6×). Practical rule for the pipeline: **on dense K/V/Q schematics, small glyph labels are a doc-parse blind spot that crop scaling does not fix — route them through the crop-judge (vision) leg, which reads them reliably.** Consistent with the v2 cascade's independent finding on the same frame.

## Judge ledger

| crop | judge .md | bytes | EXIT | outcome |
|---|---|---|---|---|
| crop01 | crop01_judge.md | 0 (inherited, killed mid-run) | — | not required (parse had zero text); file preserved |
| crop02 | crop02_judge.md | 3419 (inherited) | 0 | 5 stacks REAL, "Encode" confirmed; 5 Q circles; bar top-clipped |
| crop03 | crop03_judge.md | 0 (inherited, killed mid-run) | — | not required (no novel strings); file preserved |
| crop05 | crop05_judge.md | 2090 | 0 | all 3 strings REAL verbatim; SOS legend underlined initials; clipped "S" explained |
| crop07 | crop07_judge.md | 1910 | 0 | "52" REAL at ≈(865,60)–(882,76); clipped "er!" `[?]` |
| crop08 | crop08_judge.md | 1864 | 0 | "Res"/label REAL; **K, V, Q1 read with build-matching positions** |
| crop09 | crop09_judge.md | 2222 | 0 | 3 Y tags REAL; reads Y₀/Y₁/Y₂ (`[?]` vs build's plain `Y`) |
| crop10 | crop10_judge.md | 1940 | 0 | 5th box REAL verbatim; Ml-Head = misread of clipped Multi-Head |
| crop11 | crop11_judge.md | 1770 | 0 | Enc/Deco/Atten = truncated GT5 i1; **K, V read** |
| crop12 | — | — | — | not required (parse had zero text) |
| probes | probe_call.log, probe2_call.log | — | 0, 0 | gateway liveness (one per session) |

Every crop whose parse introduced novel strings (crop05/07/08/09/10/11) now has a nonempty judge transcript — done criterion met. One judge in flight at a time was honored (6 sequential runs, 45–144 s each).

## Blockers

None outstanding. Notes: (a) the inherited `crop01_judge.md` / `crop03_judge.md` are empty — the previous worker's judge runs were killed by the session exit (their call logs have no EXIT lines); per the novel-strings rule neither crop required a judge, so they were not rerun and the files were preserved as evidence. (b) `12_cascade_v2/` was used read-only as the report-format reference; nothing was written there. (c) The Y-row subscript question (Y₀/Y₁/Y₂ vs the certified build's plain `Y`) is flagged `[?]` in the composed analysis for pixel adjudication — it is a GT-wording conflict, not a recall item.

---
*Deliverables: manifest.json (12 crops, boxes/scales/transforms/stop reasons) · parses/ 12 call dirs · crops/ 12 pngs · judges/ 8 nonempty transcripts + 2 probe pairs · compose/COMPOSED_ANALYSIS.md · this report. Wave-2/3/4 trees untouched; nothing deleted.*
