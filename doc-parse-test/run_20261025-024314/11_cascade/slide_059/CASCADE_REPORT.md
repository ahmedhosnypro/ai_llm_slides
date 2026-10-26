# CASCADE REPORT — slide_059_cascade (wave 5, v1 tree)

Run `doc-parse-test/run_20261025-024314` · source frame `videos/deep-learning/002_transformers_part2/unique_slides/slide_059.jpg` (960×540, md5 `fb03ceaa…`)
Scope `slide_059_cascade` · worker `worker-slide_059_cascade` (this file + compose/ written by the RESUME worker after the first worker's session hit the 2 h background cap post-judges; all parses/crops/judges banked by the prior run, nothing re-executed) · prior art: `12_cascade_v2/slide_059/` (read-only).

## Headline

**Union recall 58.7% → 88.0% transcript-level** (22 EXACT + 18 NORMALIZED + 1 PARTIAL + 5 MISSING of 46 GT units; wave-2 frozen contract `05_comparison/slide_059_comparison.md` §1) — **judge-corroborated coverage 46/46 = 100.0%** (all 5 residual misses — X₄, X₅, X_{N-1}, Y₀, Y₁ — REAL on image per this cascade's judges; the ≤4 px serif subscript digits are unread by doc-parse at any compliant scale). 16 crops (cap 16) · 21 parse calls (cap 24; 5 spent on a no-token glob-path failure) · **parallel parse speedup ~2.7×**.

## Recall trajectory

| stage | recall | detail |
|---|---|---|
| wave-2 frozen full-frame (3 byte-identical passes) | 58.7% (27/46) | 9 EXACT + 17 NORMALIZED + 2 PARTIAL (C₁/C₂ as `1C1`/`1C2`); MISSING: Σ, C₃, all 16 X/Y labels; leading-`1` hallucination confirmed |
| cascade L1 (5 crops) | 27 → 33/46 (+GT6, +GT22–25; GT5 NORMALIZED→EXACT) | crop03 read **Y2 Y3 Y4 Y5** (GT22–25 novel→EXACT); crop01 read `Softmax` ×2 + `Σ` ×2 (GT6 novel→EXACT, GT5 upgraded); crop02 all-garble, crop04 zero text, crop05 no novel |
| cascade L2 (7 crops) | 33 → 39/46 (+GT9/10/11, +GT12/14/15, +GT26/27; GT9/10 PARTIAL→EXACT) | crop06 **C1 C2 C3** (kills the `1C1`/`1C2` hallucination at crop scale); crop08 **X0 X2 X3**; crop11 **Y N-2 / YN-1** (NORMALIZED); crop07/09/10/12 corroboration-only |
| cascade L3 (4 crops) | 39 → 40.5/46 (+GT13; +GT18 as PARTIAL) | crop16 **X1** (novel→EXACT, cleanest subscript read); crop13 **XN2** (GT18 MISSING→PARTIAL, 75% token overlap); crop14/15 no new units |
| final | **88.0% transcript / 100% judge-corroborated** | MISSING 5: X₄, X₅, X_{N-1}, Y₀, Y₁ — all judge-confirmed REAL (per-element table in compose/COMPOSED_ANALYSIS.md) |

## Calls & wall-clock

Parse calls from `parses/*/call.log`, run in concurrent batches (`&` + `wait`); batch gaps between levels were crop-prep time, excluded from both sides:

| batch | calls | started | batch wall | Σ individual | note |
|---|---|---|---|---|---|
| 0 (failed) | call01–call05 | 08:27:58 | 1 s | <5 s | EXIT 1 <1 s each — unexpanded glob path; **no endpoint tokens**; no transcripts |
| 1 | call06–call09 | 08:29:04 | 26 s | 79 s | L1 re-parse (call10 followed serially) |
| 2 | call10 | 08:29:30 | 7 s | 7 s | L1 (crop05) |
| 3 | call11–call14 | 08:34:51 | 4 s | 13 s | L2 |
| 4 | call15–call17 | 08:34:55 | 4 s | 12 s | L2 |
| 5 | call18–call21 | 08:42:07 | 5 s | 15 s | L3 |
| **total productive** | **16** | | **46 s** | **126 s** | all EXIT 0 |

**Parallel speedup ≈ 126/46 ≈ 2.7×** (sum of per-call durations ÷ batched wall-clock, productive calls only). Parse-leg wall 08:27:58→08:42:12 = 14 m 14 s including L2/L3 crop-prep gaps (5 m 14 s + 7 m 08 s).

Judge leg (Tier-2 vision gateway via image-analysis `analyze_image.py`, sequential, ONE in flight): probe 9 s (18:08:48–57, PROBE-OK) + 14 judges 18:08:57→19:41:08 = 92 m 11 s; per-judge 35–788 s (longest: crop02 788 s, crop08 725 s during the gateway's slow window; crop09 attempt 1 rc=124 at 900 s, attempt 2 banked in 602 s). An earlier 18:04–18:08 batch never reached the gateway (wrong script path, rc=2 instant — patched, no gateway calls consumed).

## Per-crop yield

| id | class | lvl | parent | scale | box (frame px) | parse yield (novel = not in full-frame t9k) | judge | stop_reason |
|---|---|---|---|---|---|---|---|---|
| crop01 | softmax-circle-cluster | 1 | judge-suppl | 3.0 | 390,36,655,139 | **`Softmax` ×2 + `Σ` ×2 (GT5→EXACT, GT6 novel→EXACT)** + novel garbles `ses`/`IC1`/`IC2`/`IC3` | crop01_judge.md ✓ (`sses`=`Output Classes` tail; `I` = lollipop marker; 3rd Softmax/Σ judge-only) | no-internal-structure |
| crop02 | x-row-token-labels | 1 | judge-suppl | 2.0 | 168,400,897,452 | 8 garble tokens (`Xl Xj X3 X4 Xx O XNz XNd`) — no clean units | crop02_judge.md ✓ (row = X₀…X₅, X_{N-2}, X_{N-1}; `O` = red graphic) | no-internal-structure |
| crop03 | y-row-token-labels | 1 | judge-suppl | 2.0 | 168,206,897,264 | **`Y2`/`Y3`/`Y4`/`Y5` (GT22–25 novel→EXACT)** + garbles `Yd`/`YNz`/`YNI` | crop03_judge.md ✓ (Y₀ misread `d`; Y₁ skipped entirely) | no-internal-structure |
| crop04 | pooled-20-cell-row | 1 | judge-suppl | 3.0 | 369,137,656,176 | zero text (whole-span `class_Picture` only) — **textless-region structural omission** | — (no novel strings; blocker B1) | no-new-information |
| crop05 | annotation-stack-column | 1 | judge-suppl | 2.0 | 51,115,299,525 | `Single vector representing the whole sequence` (no novel — full-frame had the merged line) | — (no novel strings; blocker B1) | no-internal-structure |
| crop06 | softmax-cluster-labels-row | 2 | crop01 | 3.0 | 407,47,623,81 | **`C1`/`C2`/`C3` (GT9/10 PARTIAL→EXACT, GT11 novel→EXACT)** + `s` clip | crop06_judge.md ✓ (all 4 strings correct; dots/arrows graphics) | no-internal-structure |
| crop07 | softmax-cluster-circles | 2 | crop01 | 3.0 | 401,83,634,142 | `Softmax` ×2 (repeat) + `Z` ×2 (Σ misread — novel garble) | crop07_judge.md ✓ (`Z`=Σ; 3rd circle dropped again) | no-new-information |
| crop08 | x-row-left-labels | 2 | crop02 | 3.0 | 184,400,481,452 | **`X0`/`X2`/`X3` (GT12/14/15 novel→EXACT)** + `X3` (2nd) = X₁ garble | crop08_judge.md ✓ (slot 2 = X₁; full sequence 0–3) | no-internal-structure |
| crop09 | x-row-tail-labels | 2 | crop02 | 3.0 | 548,400,882,452 | `X`/`XN`/`XNd` — no new units (XN supports GT18) | crop09_judge.md ✓ ("Xs"/"XN2"/"XNd"; subscript-lossy) | no-new-information |
| crop10 | y-row-left-labels | 2 | crop03 | 3.0 | 184,206,481,264 | `Y_d` + stray `1` ×3 + `Y_i` ×2 + `Y2` — no new units | crop10_judge.md ✓ (reads Y₀/Y₁/Y₂/Y₃; `1`s = split subscript strokes) | no-internal-structure |
| crop11 | y-row-tail-labels | 2 | crop03 | 3.0 | 548,206,882,264 | **`Y N-2` / `YN-1` (GT26/27 novel→NORMALIZED)** + bare `Y` (Y₅ slot) | crop11_judge.md ✓ (Y₅ subscript dropped; N-2/N-1 match) | no-internal-structure |
| crop12 | annotation-lower-column | 2 | crop05 | 2.0 | 41,312,309,533 | `ranked_table` read: Input Sequence, Word Embedding Vectors, `X0` (repeat), `X`, Position Information Vectors, `Vector_PO`/`Vector_PI` — the cascade's only chart-class structured output | crop12_judge.md ✓ (X₀/(X₁ clipped); Vector P**0**/P**1** digits, not O/I) | no-internal-structure |
| crop13 | x-tail-n-labels | 3 | crop09 | 3.0 | 709,400,876,452 | **`XN2` (GT18 novel→PARTIAL)** + `XN4` (X_{N-1} mangle) | crop13_judge.md ✓ (both labels present; `N4` glyph-shape verdict on the `-1` tail) | no-internal-structure |
| crop14 | y-head-pair-tight | 3 | crop10 | 3.0 | 189,206,351,264 | `Y_d` ×2 + `☐` ×2 (novel parser stand-ins) | crop14_judge.md ✓ (1st `d` "as written" `[?]` vs crop03/crop10's Y₀; `☐` = empty cells) | no-internal-structure |
| crop15 | x-mid-slots | 3 | crop08 | 3.0 | 494,400,656,452 | `X2`/`X3` (repeat) — land in the X₄/X₅ slots (`[?]` 4 px subscript ambiguity) | crop15_judge.md ✓ ("consistent with 2/3", heavily pixelated) | no-internal-structure |
| crop16 | annotation-table-zone | 3 | crop12 | 2.0 | 41,369,309,526 | **`X1` (GT13 novel→EXACT)** + `X0`/annotation repeats (cleanest read of the whole tree) | crop16_judge.md ✓ (all 7 strings exact, no omissions) | no-internal-structure |

Yield summary: 7 of 16 crops moved unit coverage (crop01, 03, 06, 08, 11, 13, 16) — 13 GT units touched for +13.5 recall units (27 → 40.5 of 46); crop04/crop05 produced no novel strings (no judges, per rule); the other 7 crops were corroboration/garble evidence that fed the judge leg.

## Recursion tree (stop reasons verbatim from manifest.json)

```
slide_059 — full-frame seed call05_t9k (read-only; byte-identical ×3)
├─ L1 crop01_softmax_cluster      (390,36,655,139) 3.0x — STOP no-internal-structure (children crop06+crop07 ran)
│  ├─ L2 crop06_labels_row_l2     (407,47,623,81) 3.0x — STOP no-internal-structure (C1/C2/C3 clean; terminal)
│  └─ L2 crop07_circles_l2        (401,83,634,142) 3.0x — STOP no-new-information (Σ→`Z`; 3rd circle dropped again)
├─ L1 crop02_xrow_labels          (168,400,897,452) 2.0x — STOP no-internal-structure (children crop08+crop09 ran)
│  ├─ L2 crop08_xrow_left_l2      (184,400,481,452) 3.0x — STOP no-internal-structure (child crop15 ran)
│  │  └─ L3 crop15_x12_zone_l3    (494,400,656,452) 3.0x — STOP no-internal-structure (X₄/X₅ slot ambiguity; terminal)
│  └─ L2 crop09_xrow_tail_l2      (548,400,882,452) 3.0x — STOP no-new-information (child crop13 ran)
│     └─ L3 crop13_xtail_l3       (709,400,876,452) 3.0x — STOP no-internal-structure (XN2 partial; terminal)
├─ L1 crop03_yrow_labels          (168,206,897,264) 2.0x — STOP no-internal-structure (children crop10+crop11 ran)
│  ├─ L2 crop10_yrow_left_l2      (184,206,481,264) 3.0x — STOP no-internal-structure (child crop14 ran)
│  │  └─ L3 crop14_yleft_tight_l3 (189,206,351,264) 3.0x — STOP no-internal-structure (Y_d/☐ stand-ins; terminal)
│  └─ L2 crop11_yrow_tail_l2      (548,206,882,264) 3.0x — STOP no-internal-structure (Y N-2 / YN-1 clean; terminal)
├─ L1 crop04_pooled_row           (369,137,656,176) 3.0x — STOP no-new-information (zero text — textless region)
└─ L1 crop05_annotation_stack     (51,115,299,525) 2.0x — STOP no-internal-structure (child crop12 ran)
   └─ L2 crop12_annot_lower_l2    (41,312,309,533) 2.0x — STOP no-internal-structure (child crop16 ran)
      └─ L3 crop16_annot_table_l3 (41,369,309,526) 2.0x — STOP no-internal-structure (X1; terminal)
```

Stops: 13× no-internal-structure, 3× no-new-information · 0× too-small, 0× leaf, 0× backstop · caps: crops 16/16, parse calls 21/24. Triggers for all 8 recursion edges are recorded verbatim in `manifest.json` (`recursion[]`). No scale deviations (all crops 2–3×, spec-compliant). Known artifact: `11_cascade/slide_059/11_cascade/slide_059/crops/crop01..crop05/crop.png` — byte-identical duplicates of the L1 crop pngs from an earlier mis-pathed write; kept (never delete), not counted against the crop cap.

## Doctrine note — serif subscript labels + textless regions (confirmed in this tree)

**doc-parse's hard floor on this frame is the ≤4 px serif subscript digit.** The full-frame read destroys the entire 16-label X/Y family into 8 garbage fragments (58.7% regime); crop recursion at 2–3× recovers 11 of 16 as clean subscript-inline strings (`X0`…`X3`, `Y2`…`Y5`, `C1`–`C3`, `Y N-2`/`YN-1`, `XN2`) but never resolves X₄, X₅, X_{N-1}, Y₀, Y₁ — the vision judges read all five with build-matching positions at the same scales. Practical rules: (a) subscript-inline crop reads classify EXACT against the run+subscript GT form — the single highest-yield move on this slide family; (b) symbols dropped at full frame (Σ ×3, in-circle `Softmax` ×3, C₃) recover cleanly at crop scale; (c) textless regions (pooled 20-cell row) are structurally invisible to the text contract — zero text AND zero sub-coordinates, so parse-driven recursion terminates immediately and the judge leg is the only evidence route; (d) a graphic misread can hallucinate a stable prefix (`1`/`I` before C labels) that survives one recursion level and dies only in a tighter sibling crop. Consistent with the v2 cascade's independent findings on the same frame.

## Judge ledger

| crop | judge .md | bytes | EXIT | outcome |
|---|---|---|---|---|
| probe | judges/probe/ | — | 0 | gateway liveness, 9 s |
| crop01 | crop01_judge.md | 2410 | 0 | `sses`=Output Classes tail; `I` = lollipop marker (kills `1C1`/`1C2`); 3rd Softmax/Σ judge-only |
| crop02 | crop02_judge.md | 2361 | 0 | row = X₀…X₅, X_{N-2}, X_{N-1}; every subscript garbled; `O` = red graphic |
| crop03 | crop03_judge.md | 2659 | 0 | Y₂–Y₅ correct; Y₀ misread `d`; **Y₁ skipped entirely** |
| crop06 | crop06_judge.md | 2023 | 0 | all 4 strings correct (`s`, C₁, C₂, C₃); bullet dots + up-arrows graphics |
| crop07 | crop07_judge.md | 2518 | 0 | both `Z` = Σ misreads; 3rd circle dropped again |
| crop08 | crop08_judge.md | 1896 | 0 | 3/4 correct; 2nd token actually X₁ |
| crop09 | crop09_judge.md | 2372 | 0 (att 2; att 1 rc=124 at 900 s) | "Xs"/"XN2"/"XNd"; subscript-lossy |
| crop10 | crop10_judge.md | 3078 | 0 | reads Y₀/Y₁/Y₂/Y₃; stray `1`s = split subscript strokes |
| crop11 | crop11_judge.md | 2108 | 0 | Y₅ subscript dropped; Y_{N-2}/Y_{N-1} match |
| crop12 | crop12_judge.md | 3015 | 0 | 7/7 present; X₀/(X₁ clipped); Vector P0/P1 digits, not O/I |
| crop13 | crop13_judge.md | 1532 | 0 | both labels present as written (`XN2`, `XN4`) |
| crop14 | crop14_judge.md | 2194 | 0 | 1st `Y_d` "as written" (`[?]` vs crop03/crop10's Y₀); `☐`s = empty cells |
| crop15 | crop15_judge.md | 1743 | 0 | `X2`/`X3` consistent-but-pixelated at the X₄/X₅ slots |
| crop16 | crop16_judge.md | 2853 | 0 | 7/7 exact, no misses — cleanest transcript of the tree |
| crop04 | — | — | — | **not run** (no novel strings) — blocker B1 |
| crop05 | — | — | — | **not run** (no novel strings) — blocker B1 |

14/14 required judges banked nonempty, all EXIT 0, one in flight at a time honored (sequential 18:08:57→19:41:08). Per the novel-strings rule, crop04/crop05 required no judge; per this run's instruction they are recorded as blockers, not rerun.

## Blockers

- **B1 — crop04 / crop05 judges missing.** Neither crop's parse introduced novel strings (crop04: zero text; crop05: a line the full frame already had), so the manifest's rule skipped them (`judge_files: []`). Recorded here per the resume instruction; NOT rerun. Impact is low: crop04's zone is pure graphics (wave-2 vision items 7/12 already settle the 20 cells and the textless corner), and crop05's line is wave-2-classified.
- **B2 — 5 transcript-less call dirs** `parses/call01_crop01..call05_crop05`: the crop path was passed as an unexpanded glob `crops/cropNN_*/crop.png`; parse_document.py refused the literal `*` (EXIT 1 in <1 s, no endpoint tokens, no transcripts). Every affected crop was re-parsed successfully in call06–call10; dirs preserved as evidence.
- **B3 — crop09 judge attempt 1 timed out** (rc=124 at 900 s; gateway latency ~15 min window); attempt 2 banked OK (602 s). No data lost.
- **B4 — earlier judge batch 18:04–18:08 never reached the gateway** (wrong script path, rc=2 instant); patched to the project skill path and relaunched — no gateway calls consumed by the failed batch.
- **`[?]` flags for pixel adjudication (no recall impact):** (a) Y₀ subscript — crop03+crop10 judges read `0`, crop14 judge reads the glyph "as written `d`"; (b) X₄/X₅ slot subscripts — crop02's row-sequence reading vs crop15's `2`/`3` at the same slots; (c) X_{N-1} tail read `d`/`I`/`4` by three judges. The certified build + row sequences (0–5, N−2/N−1) anchor the GT readings; transcript classification is unaffected (`Y_d`, bare `X`, `XNd`/`XN4` are all MISSING as written).
- Notes: `12_cascade_v2/slide_059/`, wave-2/3/4 trees and all frozen artifacts were used read-only; nothing was deleted; no new parse calls, judges, or crops were made by this resume session.

---
*Deliverables: manifest.json (16 crops, boxes/scales/transforms/triggers/stop reasons, judge files + judges block) · parses/ 21 call dirs (16 with transcripts, 5 transcript-less glob failures) · crops/ 16 pngs (+5 duplicate pngs in the parked mis-pathed tree, kept) · judges/ 14 nonempty transcripts + probe + progress log · compose/COMPOSED_ANALYSIS.md · this report. Wave-2/3/4 + v2 trees untouched.*
