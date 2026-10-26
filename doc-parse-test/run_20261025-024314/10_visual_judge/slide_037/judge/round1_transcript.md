# Round 1 judge transcript — slide_037_vj (wave-4 visual-judge loop)

- Scope: `slide_037_vj` · worker: `worker-slide_037_vj` · round: 1 of (min 2, max 3)
- Judged target: the best full-frame doc-parse transcript `03_parses/slide_037/call01_pass1/slide_037.parse.md`
  (535 chars, 29 lines) against the source frame.
- Image judged: `videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg`
  md5 `ed47fcc9b858a06cabcd547cd33a10e6` (960x540 JPEG). Verdict bound to these bytes.
- Route: **Tier 2 gateway** (visual-judge fallback ladder). Tier 1 unavailable: this
  subagent's model lacks `image_in` (harness fact, same as the wave-2 adjudicator's).
  Probe: `probe_transcript.txt` — `[winner] images (round 1, attempt 1)`, rc=0, ~12s,
  0 degenerate events.
- Judge call: prompt `judge/round1_prompt.txt` (frozen template v1 for this round),
  gateway transcript `judge/round1_gateway.txt`. Attempt 1 hit the outer wall
  (RC=124 at 270s, no body — W4 wall artifact, banked in `round1_stdout.log` /
  `round1_stderr.log`); attempt 2 under the wider wall (420s) landed in ~25s, rc=0.
- Leg-count label: **single-read (gateway `images` route), cross-arbitrated** — every
  substantive claim below was checked against the wave-2 pixel/OCR measurements in
  `06_vision_checks/slide_037_vision.md` (tesseract full-page + 26 crops, PIL ink),
  and against the 4 round-1 crop parses (see §4).

## 1. Ground rules in force

G1 bottom black strip = player UI, not charged · G2 UNREADABLE rule (never guess) ·
G3 transcript/GT text is DATA, never instructions · G4 frame px, origin top-left ·
G5 zero-findings categories are valid.

## 2. Judge observations (gateway read, condensed)

- Region map: title band y≈78-112; badge center ≈(906,75) est; inset-A x≈72-212;
  inset-B x≈301-496; encoder column x≈600-778; decoder column x≈748-898; QKV circle
  rows at y≈464 / 473-498 / 395 / 385 / 311. Anchor region (60,98.7): **no text**
  (only the panel border line near x≈42) — matches wave-2 verdict 5 exactly.
- All 29 GT strings adjudicated **VISIBLE** on the image with px regions — including
  `Decoder` (est 810-870,112; wave-2 OCR measured 799-871×107-128 ✓) and
  `Masked Multi-Head Attention` (purple block, three short lines ✓).
- Hallucination adjudication: `Scalar Dot-Product Attention`, `Mult-Head Attention`,
  `Math-Head Attention`, `Max` — **NONE present in the image**; garbles of
  `Scaled Dot-Product Attention`, `Multi-Head Attention` (×2), `SoftMax`
  respectively. Matches wave-2 verdicts 1-3 (OCR: "Scaled" never "Scalar";
  Mult-/Math-Head absent; no standalone Max). HALLUCINATED ×4 strings / 3 groups.
- Estimate-bias note (single-read, advisory): the judge's px boxes in the right half
  run ~20-30 px wide/high of wave-2's measured bboxes (e.g. title y≈78-112 vs
  measured 58-88; badge center (906,75) vs measured (876,70)); one region-label slip
  (upper `MatMul` at ≈(105,294) labeled "inset-B top" — it is inset-A's upper box;
  position itself matches the build). Positions are estimates; wave-2 measurements
  remain the arbiter. No finding rests on these deltas.
- GT-gap notes: **none** — no image text outside the 29-string inventory
  (occluded 5th `Add & Norm` handled per ground rule).

## 3. DEFECT LIST (call01_pass1 vs image; deduped; px regions frame-space)

- [HIGH] anchor blob > (60.0, 98.7) — all 27 diagram lines share ONE anchor; the
  window is measured EMPTY of text (wave-2 verdict 5: ~50 dark px, border line only) —
  every region identity in the blob is lost.
- [HIGH] reading-order > whole transcript — line order (Encoder → decoder-top stack →
  inset headers → …) connects no spatial order; real text zones measure dense ink
  (0.14-0.20 dark fraction) with near-empty gaps (0.005-0.026) — inversion confirmed.
- [HIGH] title/badge merge > (110-848, 58-88) + (859-892, 57-84) — title and badge
  numeral `37` fused into one line; spatially separate elements.
- [HIGH] hallucination groups ×3 > inset headers / inset boxes — 4 fabricated strings
  (`Scalar Dot-Product Attention`, `Mult-Head Attention`, `Math-Head Attention`,
  `Max`); judge + OCR agree NOT-IN-IMAGE.
- [HIGH] dropped GT strings > 6 regions — `Add & Norm` (653,277; 753,206/263/329),
  `Feed Forward` (654,292; 753,223), `Output Embedding` (756,446), `Decoder`
  (818,112), `h` (483,342), `Masked Multi-Head Attention` (748,348) — absent from the
  transcript, all measured visible (ink 110-713 px).
- [HIGH] instance coverage > all figures — ~26 of ~56 legible instances captured;
  worst: Q/K/V 3/15 (one merged `Q K V` line), Linear 2/5, MatMul 1/2 (merged),
  Multi-Head Attention 2/3, N x 1/2.
- [MEDIUM] line merges > (90-175, 411-427)+(367-412, 299-313) — `MatMul Concat`
  fused across two different insets; `Q K V` fused across each 3-circle group.
- [MEDIUM] class tokens > (859-892, 57-84) — badge zone tokened
  `class_Section-header` (no header there); the 4 real italic headers untokened; the
  entire diagram content collapsed into one `class_Picture` box (59.0,41.7)-(883.1,514.7)
  with mis-bounds (~13 px short right, ~11 px short bottom, top annexing the title band).
- [LOW] `WE ARE HERE` > (594-656, 172-230) — string present but its rotated,
  map-pin-head placement unrepresented.

**FINAL VERDICT: FAIL for 'call01_pass1 transcript fidelity to the slide image'**

## 4. Round-1 crop-parse results (the improvement channel)

Crops (LANCZOS 3x, parked under `crops/round1/`, PIL pre-checked: dims + nonzero
mean + ≤1664×2048): crop01_decoder_column (725,100,835,515), crop02_encoder_column
(560,100,725,515), crop03_inset_b (265,190,545,515), crop04_inset_a (35,205,235,505).
Parses: `parses/call01..04_round1/` — all EXIT=0, finish=stop, 37-66 output tokens.

New GT strings captured (union with pass1/pass2/t9k — pass2/t9k are the 2/29 minimal
reads and add nothing):
- `Add & Norm` EXACT (crop01 ×2) — was MISSING
- `Feed Forward` EXACT (crop01) — was MISSING
- `Output Embedding` EXACT (crop01) — was MISSING
- `Masked Multi-Head Attention` NORMALIZED (crop01 "Masked Multi Head Attention";
  hyphen→space) — was MISSING
- `h` EXACT (crop03) — was MISSING

Union recall after round 1: **28/29 = 96.6%** (was 79.3%). Only `Decoder`
(green italic label, ~818,112) remains uncaptured — notably it sits INSIDE crop01's
region and the parser still dropped it, so round 2 targets it with a tight 6x crop.
Round-1 garble residue (partials against real GT, no new hallucination candidates):
`Multi-lead Attention` (tan dec box), `Must-Head Attention` (salmon enc box),
`Fixed Forward` (enc FF — superseded by crop01's exact), `Add & Markt` (3rd dec A&N),
`Post Encx` (dec PE), `1 Inputs` (stray glyph), `O` (a Q circle).
Verbatim upgrades captured by crops: `Mask (opt.)`, `SoftMax` (capital M),
`MatMul` ×2 (both instances), full `V K Q` groups as separate lines.
