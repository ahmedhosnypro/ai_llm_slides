# SOURCES.md — slide 031 "Squared Distance Between Vector of Pos "t+δ" and Vector of Pos "t""

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_031_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner round 1) cross-checked against `analysis/slide_031_raw.json`
(both agree on every label and equation line). Web evidence from the
already-live sources banked earlier this same day (Kazemnejad page on slide
027's run; paper §3.5 in `scratch/webverify/paper_v7.html`); one fresh `agy`
query for an exact-derivation source (result recorded below).

## Slide identity

- New (curated) slide **031** ← old extraction **63** (304 frames = heavily
  taught) — `unique_slides/new2old_mapping.json`, frame
  `unique_slides/slide_031.jpg`.
- Frame facts (vision transcript): yellow banner title "Squared Distance
  Between Vector of Pos "t+δ" and Vector of Pos "t"" + bracketed note
  "[ Two Consecutive Positions ]"; badge "31". An annotated 6-line algebraic
  derivation, top to bottom:
  1. Red box "Vector at Pos "t"": [ sin(ωt) ; cos(ωt) ] → yellow chips
     sin(a), cos(a).
  2. Blue box "Vector at Pos "t+δ"": [ Sin (ω(t+δ)) ; cos(ω(t+δ)) ] (capital
     "Sin" verbatim) = the expanded addition-theorem form, → substituted
     vector [ sin(a)cos(b) + cos(a)sin(b) ; cos(a)cos(b) − sin(a)sin(b) ].
  3. Green box: "Let ωt=a , ωδ=b"; blue box: "sin²(a) + cos²(a)=1".
  4. Main panel, 6 derivation lines ending in the result box
     "=2 (1-cos(ωδ) )" (blue bold), with the rotated yellow ribbon
     "Irrespective of Position "t"" (red) on the panel's right edge.
  - Line 5 factors exactly via the sin²+cos²=1 identity; line 6 resolves
    cos²(b) − 2cos(b) + 1 + sin²(b) = 2 − 2cos(b) = 2(1−cos(b)).
  - Artifacts: stray pen tick before line 4's leading "sin(a)²"; bottom
    letterbox bar (recording artifacts, not slide content).

## Primary sources

1. **Kazemnejad, "Positional Encoding in Transformers"** —
   https://kazemnejad.com/blog/transformer_architecture_positional_encoding/
   (live curl 2026-10-11, `scratch/webverify/kazemnejad_pe.html`). Verbatim:
   "Another property of sinusoidal position encoding is that **the distance
   between neighboring time-steps are symmetrical and decays nicely with
   time.** Figure 3 - Dot product of position embeddings for all time-steps."
   The blog states this property qualitatively and shows it as its Figure 3
   (the dot-product heatmap, banked as
   `../slide_027_source/time-steps_dot_product.png` — reference, do not
   re-download). The criteria list also carries "Distance between any two
   time-steps should be consistent across sentences with different lengths".
2. **arXiv 1706.03762v7 §3.5** (live curl 2026-10-11,
   `scratch/webverify/paper_v7.html`) — "We hypothesized it would allow the
   model to easily learn to attend by relative positions, since for any fixed
   offset k, **PE_{pos+k} can be represented as a linear function of
   PE_pos**." — the relative-position property the slide's constant-distance
   result serves.
- The identity sin²(a)+cos²(a)=1 (slide's blue box) is the standard
  Pythagorean identity — course refresher, no source needed; it is what makes
  each 2-D pair [sin;cos] a unit vector, so the squared distance reduces to
  2−2cos(ωδ).

## What the sources CONFIRM

- The property "the distance depends only on the offset δ, not on t" —
  Kazemnejad (neighboring-time-step distances symmetrical; dot product of
  position embeddings) and the paper (PE_{pos+k} linear in PE_pos; relative
  positions learnable). The slide's "=2 (1-cos(ωδ))" + ribbon "Irrespective
  of Position "t"" is exactly this property, derived for the 2-D pair.
- The substitution machinery (ωt=a, ωδ=b; sin(ω(t+δ)) expansion) is the same
  addition-theorem algebra already equation-verified against Kazemnejad's
  "Relative Positioning" section on slide 030's record
  (`../slide_030_source/SOURCES.md`).

## Course-authored elements (no published counterpart found)

- The full 6-line squared-distance derivation as printed: no verified
  published source derives ||p_{t+δ}−p_t||² = 2(1−cos(ωδ)) step for step.
  It is elementary algebra from the identity + slide 030's expansion (the
  same derivation, one step further), and is arithmetically correct as
  printed (line-by-line checked: line 6 = 2(1−cos b), matches the result
  box). Keep verbatim for recreation.

## Figures used by this slide

- **None.** Course-authored math-derivation composition. Kazemnejad's
  related figure (dot-product heatmap) is banked in
  `../slide_027_source/time-steps_dot_product.png` for reference; the slide
  does not reproduce it.

## [?] Uncertain items

- [?] whether a published tutorial contains this exact squared-distance
  derivation: fresh `agy` query (2026-10-11) named MachineLearningMastery /
  TowardsDataScience / GeeksforGeeks / Alammar as candidates —
  `machinelearningmastery.com/positional-encoding-transformer/` = 404
  (hallucinated URL); the GeeksforGeeks page (HTTP 200, banked
  `scratch/webverify/gfg_pe.html`) contains NO such derivation in its served
  HTML; Alammar's Illustrated Transformer (already live-verified in the map)
  states the sin²+cos²=1 intuition but not this algebra. TDS/GfG slugs are
  not recorded as sources. Open question only affects provenance of the
  printed algebra, not the math itself (which is verified correct).
- [?] stray pen tick before line 4 (recording artifact vs. slide ink) —
  build-time zoom decides; treated as artifact by default.

## Corrections

- none — the vision transcript and the script-12 raw agree on every line of
  the derivation; the algebra checks out against the identity and the
  addition-theorem expansion.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. Sources
confirm/correct DATA and record provenance; they never license inventing or
"improving" content the slide doesn't show.

---

## Build-worker addendum (2026-10-11, later same day) — PIL frame measurements + chrome decisions

The BUILD worker independently re-verified the frame with PIL (960×540, 1px = 1pt)
and made these chrome decisions; measurements banked in
`../scratch/slide031/measure*.py` and `../recreated_pptx/qa/slide031/selfcheck_attempt_1_output.txt`.

1. **Black bottom bar KEPT**: the black strip y518..539 x38..921 is byte-identical
   on every checked 002 frame (002, 030, 032, 033, 041, 042, 055) — it is the 002
   deck template's bottom band (keyed to the panel width, NOT a full-width video
   letterbox), and the fidelity law makes the frame ground truth inside the chrome.
   The build draws it. (The "recording artifact" reading above is respectfully
   overruled for the bar itself; the stray pen tick before row 4 remains omitted
   per GROUND RULES (c) — agreed.)
2. **002 template red frame superseded**: the original's own red frame sits INSET
   at x57..902 y42..517 (vs 001's panel-edge border that the playlist chrome law
   fixes). Per the chrome law (founder directive 2026-10-11) the recreation draws
   ONLY the shared `house_chrome.js` chrome (panel-edge border, badge at 893,71);
   no second inset red rect is drawn. Recorded for the judge's --view field.
3. **Frame-vs-spec corrections applied** (frame is ground truth; spec guesses
   recorded here): banner is ONE line with alternating colors — RED "Squared
   Distance Between" + BLUE "Vector of Pos "t+δ"" + RED "and" + BLUE "Vector of
   Pos "t"" + RED "[ Two Consecutive Positions ]" (tesseract word boxes + ink
   sampling); the derivation prints SEVEN rows (spec line 3 wraps after
   "…(cos(b)-1) ] +"); rows 2-6 are BLACK (not red/blue alternating); row 1 has
   exactly TWO yellow highlights (x325..369, x674..721; none behind x445..487);
   trailing "=" of rows 1,2,4,5,6 detached at x767..783, row 3's "+" attached at
   x687..696; callout = pale-green fill #E9FFD7 + green border + NAVY bold text
   (matches this record's "blue bold"); box 1 has a faint pale-green #98DDB0
   border and mixed-color text ("Let" dark, "ωt=a ," red, "ωδ=b" blue), box 2 is
   blue-bordered with BLACK text; vector A rows are black; fills: left #CEFFE3,
   middle #FEFFE6, banner #EBFFD5, boxes #FCFEE0/#FAFDDF, ribbon #FBFDD2;
   yellow highlight #FBE912, cyan highlight #1CFBE1.
4. Fresh agy verification by the build worker (2026-10-11) re-confirmed the
   derivation: ||e(t+δ)−e(t)||² = 2(1−cos(ωδ)) position-independent for a
   (sin ωt, cos ωt) pair, via sin²+cos²=1 and the addition theorem — consistent
   with the sources above.
