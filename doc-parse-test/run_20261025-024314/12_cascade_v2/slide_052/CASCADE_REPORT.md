---
# CASCADE REPORT — slide_052_cascade_v2 (wave 5B, requirement-compliant)

Run `doc-parse-test/run_20261025-024314` · source frame `videos/deep-learning/002_transformers_part2/unique_slides/slide_052.jpg` (960×540)

## Headline

**Union recall 75.0% → 90.9% transcript-level** (20 EXACT + 0 NORMALIZED + 0 PARTIAL + 2 MISSING of 22 GT units) — **judge-corroborated coverage 22/22 = 100.0%** (the 2 transcript misses, K and V, are REAL per 3 independent vision judges each; doc-parse cannot read the 15-px glyphs at compliant crop scales). 16 crops (cap 16) · 17 parse calls (cap 24) · **parallel speedup ~2.5×**.

## Recall trajectory

| stage | recall | detail |
|---|---|---|
| wave-2 frozen full-frame | 75.0% (16.5/22) | self-stop 145 tokens; 5×3 grids shredded; Encoder + trailing Picture region hallucinations confirmed |
| cascade L1 (8 crops) | +GT9, GT22; GT5 PARTIAL→EXACT | badge `52`, encoder-box labels; crop06 badge judge-recovers GT22 |
| cascade L2 (5 crops) | +GT21 clean `Y` | Y-row isolation beats row garble |
| cascade L3 (3 crops) | K/V still unread by doc-parse | judge leg proves them REAL |
| final | **90.9% transcript / 100% judge-corroborated** | trajectory in compose/COMPOSED_ANALYSIS.md |

## Crop tree (16 crops, 3 levels — manifest.json is the record; stops per node)

| id | class | level | judge | stop_reason |
|---|---|---|---|---|
| crop01 | picture | L1 | crop01_judge.md | no-new-information |
| crop02 | upper_boxes | L1 | crop02_judge.md | no-new-information |
| crop03 | lower_boxes | L1 | none needed | no-new-information |
| crop04 | wordrow | L1 | none needed | no-new-information |
| crop05 | leftpanel | L1 | crop05_judge.md | no-new-information |
| crop06 | badge | L1 | crop06_judge.md | leaf |
| crop07 | kv_q1 | L1 | none needed | no-new-information |
| crop08 | y_row | L1 | crop08_judge.md | no-new-information |
| crop09 | kv_band | L2 | crop09_judge.md | no-new-information |
| crop10 | y_left | L2 | crop10_judge.md | no-new-information |
| crop11 | y_right | L2 | none needed | no-new-information |
| crop12 | q_context | L2 | crop12_judge.md | no-new-information |
| crop13 | box5 | L2 | crop13_judge.md | no-new-information |
| crop14 | k_band | L3 | crop14_judge.md | no-new-information |
| crop15 | v_band | L3 | crop15_judge.md | no-new-information |
| crop16 | inputs_row | L3 | crop16_judge.md | no-new-information |

Stops: **15× no-new-information, 1× leaf** (crop06). Backstop: crops 16/16 (cap reached), parse calls 17/24.

## Per-crop yield (recovered content)

- crop02: 5 upper 3D boxes + 5 Q circles + residual bar title · crop05: Transformer Encoder box + I/feel/Sick + SOS legend · crop06: badge **52** (GT22) · crop08→crop10/11: Y tags isolated from row garble · crop12: Q row context readable at 3× · crop13: 5th masked box (crop03 returned 4/5) · crop16: dropped `I` instance recovered · crop09/14/15: K/V bands — doc-parse misreads glyphs as `Y1/Y2` or returns empty; vision judges read K and V cleanly.

## Key finding (doctrine candidate)

**doc-parse cannot read 15-px glyph circles (K, V) at compliant crop scales** (≥480 px @2–3×): 172 px context → label dominates; 162 px band → glyph confusion (`Y1/Y2`); K-only/V-only bands → callout tail dominates / empty. Vision-gateway judges read K/V without difficulty (3 independent reads each). The loss is the parser's, not the image's — the judge leg is the compliant recovery route. (Wave 4 had read K/V only from 44–45 px crops, violating the prep rule.)

## WAVE-5B compliance checklist

1. Crop every class block → manifest.json, 16 crops incl. origin-only estimated crop01
2. Judge rerun per crop → parses/ 17 call dirs + judges/ 13 non-empty transcripts (12 judged crops + 1 degenerate retry banked)
3. Position tracking → manifest box_frame_px/scale/stop_reason populated, 0 nulls (gate-checked)
4. Parallel parse calls in one subagent → batched `&`+`wait` max 4 concurrent, ~2.5× speedup
5. Recursive until semantic stop → L1 8 / L2 5 / L3 3, stop reasons per node above
6. One composed file → compose/COMPOSED_ANALYSIS.md (position-tracked, y-ordered, provenance, hallucination + GT-gap sections)

## Honesty notes

- K and V remain transcript-misses (hence 90.9%); the 100% figure is **judge-corroborated coverage**, labeled as such, never folded into transcript recall.
- crop01's origin-only region (906.5,517.6) is the wave-2-CONFIRMED hallucination region; cropped and judged, kept classified hallucination-candidate — zero recall credit.
- Process note: the first assigned worker was quarantined after 3 narration-without-execution early-ends; a fresh verification worker confirmed integrity; this report was assembled from the banked artifacts (manifest.json, compose/, judges/, 02_worker_logs/slide_052_cascade_v2_commands.log) and written by the closing worker.

---
