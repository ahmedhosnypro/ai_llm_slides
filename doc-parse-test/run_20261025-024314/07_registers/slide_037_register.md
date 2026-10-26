# Register — slide_037 (doc-parse accuracy audit, wave 2)

Scope: `slide_037` · worker: `worker-slide_037` · wave 2 (post-adjudication).
Inputs: wave-1 transcripts `03_parses/slide_037/call01_pass1/slide_037.parse.md`
(535 chars) + `call02_pass2/slide_037.parse.md` (166 chars); GT =
`04_ground_truth/slide_037/` (inventory + frozen build chain + `_sim/draw_record.json`);
adjudication = `06_vision_checks/slide_037_vision.md` (verdicts 1–14; pixel-evidence
method: tesseract full-page + 26 crops to 12x, PIL/numpy ink/geometry, build m0 fit
fx=0.9623x+17.1 / fy=0.9605y−0.22). Verdict N below = adjudication of wave-1 claim N.
Coordinates are in **build/pt space** unless marked "frame" (see finding R10).

**Headline numbers:** label-level text_recall 79.3% (23/29); instance-level coverage
26/56 legible instances = 46% (≈30 distinct visible strings, ≈48–50–57 instances
depending on counting; adjudicator estimate 40–60% — LOW-to-MEDIUM); hallucinated
content confirmed = 3 groups / 4 strings; pass1↔pass2 Jaccard 0.087; both calls
finish=stop EXIT=0.

---

## Findings (severity-ranked)

### R1 · BLOCKER · confidence high · corroborated — hallucinated-content
Pass1 emitted 4 strings matching no ground truth, in 3 confirmed hallucination groups:
`Scalar Dot-Product Attention` (call01 line 8 of the blob), `Mult-Head Attention` +
`Math-Head Attention` (lines 11, 18), `Max` (line 14).
Evidence: `06_vision_checks/slide_037_vision.md` verdicts 1–3 — full-page OCR finds
"Scaled" never "Scalar" and exactly 2 SDPA instances (inset-A title ~(67,224)+(106,242);
mauve inset-B box ~(315,345) OCR "Scaled Dot-Product Atteanbon"); "Mult-Head"/"Math-Head"
explicitly absent (False/False) while the real strings measure present (`Multi-Head
Attention` ×3: inset-B title conf92 (321,209), salmon enc box ink=443, tan dec box
ink=713; `Masked Multi-Head Attention` ×1 in the purple block); no standalone "Max"
(real: `Mask (opt.)` conf90 (98,351), `SoftMax` inset, `Softmax` dec-top ink=87).
Second read = the adjudicator's OCR+ink measurement. Class: **HALLUCINATED** (×3;
`hallucinated_confirmed=3` covers 4 strings). Impact: a builder consuming pass1
verbatim would print fabricated headers on a verbatim-fidelity pipeline.

### R2 · BLOCKER · confidence high · corroborated — dropped-region (pass2 total collapse)
Pass2 (maxtok 3000) returned 166 chars / 27 tokens: title + `37` fused into one line and
a single `class_Picture` — **zero diagram text** for a slide whose entire content is 3
vector diagrams (~30 distinct visible strings). Evidence: call02 transcript;
`06_vision_checks` verdicts 12–13 (≈30 distinct strings, ≈48–50 instances measured on
the frame). Second read = pass1 transcript (which did extract 23/29 labels) + the
adjudicator's ink sweep. Class: **REAL** / dropped-region. Reliability twin: pass1↔pass2
Jaccard 0.087 (see R6) — the lane's output is not stable enough to trust single-read.

### R3 · MAJOR · confidence high · corroborated — dropped-region (6 confirmed omissions, pass1)
Pass1 missed 6 GT labels: `Add & Norm` (0 of 4 legible instances; boxes with ink
110/176/162/188 px), `Feed Forward` (0 of 2; ink 376/527), `Output Embedding` (OCR
"Outond I Envtedidirg"), `Decoder` panel label (OCR, 799–871 × 107–128), `h` (ink=21 in
the tan circle (483,342)), `Masked Multi-Head Attention` (OCR "Magked NuUY Hoad …eryhon").
Evidence: verdicts 4, 11; GT boxes in `04_ground_truth/slide_037/inventory.md` §labels.
Second read = adjudicator ink/OCR. Class: **REAL** / dropped-region.
**Occlusion leniency (verdict 11):** the 5th `Add & Norm` (653,342 69×11.5) is FULLY
occluded by the red disc (label ink 4+4 px vs 43–188 px readable controls; red core
x663–686 y318–340) — legitimately unreadable on the image, must NOT count against the
parse; the "~2 partially illegible" wave-1 upper bound refines to exactly 1 fully
hidden (the decoder MHA box label is cleanly readable, ink 713).

### R4 · MAJOR · confidence high · corroborated — dropped-region (sweep folded, with reconciliation)
The adjudicator's dropped-region sweep (verdict 12) enumerates the visible-text
inventory beyond claims 1–11: `WE/ARE/HERE` pin text (frame 594–656 × 172–230, tilted),
`Positional Encoding` ×2 (586–646 × 396–425; 810–870 × 398–427), `Input Embedding`
(646–710 × 427–449), decoder-top `Output`/`Probabilities`/`Softmax`/`Linear`
(741–804 × 108–182), `Inputs` (652–700 × 471–487) + `Outputs (shifted right)`
(734–813 × 467–500), `Scale`, inset-B `Linear` ×4, `N x` ×2, badge `37`.
**Reconciliation (transcript-checked, and material for fairness):** for **pass2** all of
these are genuinely dropped strings (R2). For **pass1** the blob transcript DOES contain
most of them as text (`WE ARE HERE`, `Positional Encoding` ×2, `Input Embedding`,
`Output`/`Probabilities`/`Softmax`/`Linear`, `Inputs`, `Outputs`, `(shifted right)`,
`Scale`, 2× `Linear`, `Nx`) — what pass1 drops is their **region identity and instance
coverage**: all 27 lines share one anchor at (60.0, 98.7) (measured empty, R5), no
per-item coordinates, `N x` 1/2 instances, `Linear` 2/5, V/K/Q letters 3/15 (one merged
`Q K V` line), `MatMul` 1/2 (merged), `Multi-Head Attention` 2/3. Class: **REAL** /
dropped-region (region-level for pass1, string-level for pass2). Severity MAJOR either
way; the sweep's "a text extractor should have caught" framing is honored at the level
each pass actually failed.

### R5 · MAJOR · confidence high · corroborated — coordinate-misalignment + reading-order-inversion
The pass1 blob anchor `<x_0.0625><y_0.1828>` → (60.0, 98.7) lands on pixels measured
EMPTY of text (verdict 5: only ~50 dark px in an 80×50 window, forming the panel's left
border line at x≈42; zero text) — 128.3 px from the nearest real text zone in my wave-1
frame-px reading, and empty in build-space too. The blob's line order (`Encoder` →
decoder-top stack → inset headers → …) connects no spatial order: the three real text
zones measure dense ink (dark fraction 0.14–0.20) with near-empty gaps (0.005–0.026).
Evidence: verdict 5; `05_comparison/slide_037_comparison.md` §2 row 3. Second read =
adjudicator pixel measurement. Class: **REAL** (coordinate-misalignment +
reading-order-inversion).

### R6 · MAJOR · confidence high · corroborated — reliability instability
pass1 vs pass2: Jaccard 0.087 over GT strings detected (2 shared of union 23); output
133 vs 27 tokens (4.9×) with 3000-token headroom unused (both finish=stop — collapse is
model behavior, not truncation); latency 51.8 s vs 128.3 s. Evidence: call transcripts +
`05_comparison` §4; corroborated by verdict 13's coverage estimate (LOW-to-MEDIUM,
"quality defects on top"). Class: **REAL**. Consequence: no string beyond title/`37` is
corroborated by a second parse read; everything else in pass1 is single-read.

### R7 · MINOR · confidence high · corroborated — class-token-mismatch (badge as Section-header)
Both passes token the badge zone `class_Section-header` at (0.9277, 0.168) — measured:
yellow badge circle frame x859–892 y57–84 (center (876,70), d≈34 = build's d36 @(893,71)
under the 0.96 fit) with numeral ink 41 px; no header there. The 4 real italic headers
measure untokened: SDPA (67–215, 224–254), MHA (321–475, 209–221), `Encoder`
(580–644, 113–125), `Decoder` (799–871, 107–128). Evidence: verdict 8. Class: **REAL**
/ class-token-mismatch.

### R8 · MINOR · confidence high · corroborated — table-structure-loss (flowchart-label merges)
Pass1 merged separate boxes into single lines: `MatMul Concat` (separate boxes, frame
90–175 × 411–427 and 367–412 × 299–313, different insets, each OCR-read independently)
and `Q K V` (5 groups of 3 circles at measured positions). Evidence: verdict 6. Class:
**REAL** / structure loss (flowchart analog of table-structure-loss).

### R9 · MINOR · confidence high · corroborated — dropped-region (mega-Picture mis-bounds)
Pass2's single `class_Picture` box (59.0, 41.7)–(883.1, 514.7) build-space: right edge
~13 px short (true 896), bottom ~11 px short (true 526), top at y41.7 sits above the
title ink (y58–88) — inside the chrome border rather than the title band proper — and
the left edge annexes the left column; the left/center insets are never region-marked
and the three real figure regions measure disjoint (0.14–0.20 ink vs 0.005–0.026 gaps).
Evidence: verdicts 7, 14. Class: **REAL** / dropped-region + class-token-mismatch
(diagrams are vector shapes, not pictures).

### R10 · MINOR · confidence high · corroborated — space-convention note (correction to wave-1 §2)
Verdict 14 measures the parse's coordinate tokens as internally consistent with the
**build/pt space**: badge (893,71), A&N box (653,342 69×11.5), MatMul (76,429), Concat
(364,312), title x96–864/y50–100 all match the certified build within 1–2 px. My wave-1
comparison converted tokens ×960/×540 as frame-px (the skill's stated convention), which
overstates right-half offsets by ~17–20 px (frame = 0.9623·build_x + 17.1). Amended
reading: where matchable, the parse's anchors are MORE accurate than wave-1 §2 credited;
the remaining true coordinate defects are R5 (blob anchor) and R9 (picture box bounds).
Class: **REAL** (measurement-framing correction, not a parse defect); wave-1
`coord_plausible_pct` figures stand as computed (75% pass1 / 100% pass2) under the
stated conversion.

### Non-defects (positive confirmations, corroborated)
- Title verbatim `Transformer Blocks (stacked over Multi-Head)`, left-anchored at the
  text-box edge (red ink bbox frame x110–848 y58–88, ~31 px glyphs ≈ 35 pt bold red) —
  verdict 9. Both passes agree; the only fully corroborated content.
- Badge numeral `37` correct (digits too small for tesseract; value per certified chrome
  law, ink confirmed) — verdict 12 last bullet.
- Bottom black strip (rows y≈517–540, luminance 20–21, 92% dark) is player progress-bar
  UI; correctly excluded by parse and build alike — verdict 10.
- WE/ARE/HERE, Positional Encoding ×2, Input Embedding, decoder-top stack, Inputs/
  Outputs/(shifted right), Scale, Linear ×4, N x: present in the pass1 blob as strings
  (single-read; region-less) — see R4.

---

## Scores (0–10, one-line justifications)

- **accuracy: 4/10** — label recall 79.3% is undercut by 3 confirmed hallucination
  groups, instance coverage of only 46% (26/56), two label merges, and zero structure;
  the occluded 5th `Add & Norm` is fairly excused (R3) and does not move the number.
- **reliability: 4/10** — both calls finished stop/EXIT=0 with clean stderr (lane
  mechanics good), but pass2's total diagram-text collapse and the 0.087 pass1↔pass2
  Jaccard make any single read untrustworthy.
- **detail: 3/10** — 28 flat lines vs ~56 instances, one (wrong) anchor for all diagram
  text, 2 class tokens for a 7-region slide, no box/arrow/dash/color/font facts.
- **recreation_power: 2/10** — from pass1 alone a builder gets the title, badge numeral
  and ~half the label vocabulary with no geometry, colors, or grouping (pass2 alone:
  nothing but the title); the certified build encodes 202 shapes + 75 hexes + z-order
  that the parse cannot approach.
