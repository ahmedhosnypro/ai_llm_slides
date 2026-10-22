# SOURCES.md — slide 010 "Using  FF NN  for Multiplication of ONE Vector by a Matrix" (W_q example; Sigmoid→Linear / bias→0 deltas)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Written 2026-10-11 by the Part II web-verification
worker.

## Slide identity

- Frame `unique_slides/slide_010.jpg`, badge numeral **10** (matches file id).
- Old extraction: slide 10 ← old 10 (`unique_slides/new2old_mapping.json`).
- Dependency: **10 ← 009** (in-video edge) — delta-variant of slide 009's
  composition; head of pattern group P1 [9,10,12,14,16].
- NOTE: no script-12 raw existed for this slide at research time — this file's
  frame facts come from the vision probe below.

## Vision transcript of record

- `transcripts/slide010_vision_2026-10-11.txt` — ONE default-route (`images`) probe,
  `--thinking high --max-tokens 65536`, via `scripts/16_vision_gate.sh`; winner
  `images (round 1, attempt 1)`, degenerate events 0. **Transcript is truncated
  mid-§4 (sections 5 "Numbers/Data" and 6 "Build state" were never emitted; no
  substance lost — badge numeral and all data tokens were captured in §2/§3).
  Recorded honestly per verdict law; no second probe spent (one-per-slide rule).**

## Frame facts (vision, ground truth)

- Title (red bold, verbatim): "Using  FF NN  for Multiplication of ONE Vector by
  a Matrix" (double spaces as in 009; the ONE is new vs slide 9's title).
- Subtitle (blue italic bold): "Example: Multiply Vector of Current Word X by
  W_q (Query) {Remember: W_q is Squared Matrix}" — "X"/"W_q" red, the {…}
  reminder in green.
- LEFT panel (delta of 009): "Input Word X", pink input circles x₁..x₄, 4 Σ nodes
  (each with a small multicolored pie wedge), outputs y₁..y₄; 16 colored edges
  with W₁₁..W₄₄ labels (tiny, partially uncertain [?] on several subscripts).
- MIDDLE, two stacked strips: top **Yᵀ [y₁ y₂ y₃ y₄] = Sigmoid**; bottom
  **Yᵀ [y₁ y₂ y₃ y₄] = Linear**; black oval callout "IF No Non-linearity" +
  thick red downward arrow between them.
- RIGHT, two stacked panels: top **X [x₁..x₄] · [4×4 W grid, row 1 =
  W11 W21 W31 W41; row 2 = W12 W22 W32 W42; row 3 = W13 W23 W33 W43; row 4 =
  W14 W24 W34 W44] + [b₁ b₂ b₃ b₄]**; bottom identical but bias column =
  **0 0 0 0**; black oval callout "IF No Bias" + red downward arrow between the
  bias columns.
- Both matrix grids carry small colored swatches per cell; x/y/b boxes pink/
  yellow as in 009.

## Primary sources

- **Slide itself: course-authored didactic figure** (probe: matches no published
  figure — not Vaswani Fig 1/2, not Bloem, not Alammar).
- **FC-layer framing (agy-confirmed 2026-10-11, `../scratch/agy_s010.txt`)**:
  Goodfellow, Bengio, Courville, *Deep Learning* ch. 6 presents the linear/affine
  baseline (ŷ = Wᵀx + b) before adding non-linearities —
  https://www.deeplearningbook.org/contents/mlp.html. "Linear" (= no
  non-linearity) and "no bias" (b = 0) are exactly the degenerate cases the slide
  isolates.
- **W_q naming (paper)**: Vaswani et al. 2017, arXiv:1706.03762v7 §3.2.2 —
  Q = XW^Q with W^Q ∈ ℝ^{d_model×d_k}, a learned projection of the input
  embeddings (paper text verified live in the fleet map + 001's records; agy
  confirmed the substance same day — its "quote" is paraphrase-style, recorded
  here as substance-confirmation, not verbatim).

## What the sources CONFIRM

- The two deltas are mathematically exact: removing the activation gives a
  linear/affine map; setting b = 0 gives a pure matrix multiply. Both are the
  paper's actual situation for attention projections (Q = XW^Q: linear, and the
  paper's projections have no bias term — the bias lives in the FFN, §3.3).
- "W_q is Squared Matrix" = the COURSE's own d×d bookkeeping — the same
  course-vs-paper dimension convention recorded in 001's slide-37/43 records
  (per-head W drawn d×d; paper reduces to d_model×d_k with d_k = d_model/h).
  Course wins for recreation; recorded as a known convention difference, not an
  error to fix.
- Same W-indexing convention as slide 009 (first index = output, displayed rows
  = outputs) — consistent with 009's edge labels; subscripts on THIS frame's
  grids agree with 009's where legible.

## Course-authored elements (do not "fix" to a source)

- The black "IF No Non-linearity" / "IF No Bias" oval callouts, the red delta
  arrows, colored matrix swatches, the "Current Word" framing, and the
  double-space title spacing — instructor's own; keep verbatim.

## [?] Uncertain items

- [?] Several left-panel edge weight subscripts too small to read with certainty
  (W22/W24/W33/W34/W42/W41 group) — the right-panel grids read cleanly and pin
  the convention; per-glyph state needs only a build-time zoom glance.
- [?] Transcript truncation (§5/§6 missing) — no data loss expected; if the build
  needs artifact positions, measure the frame directly.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows; Goodfellow ch. 6
and the paper §3.2.2 confirm the math/naming. Discrepancies are recorded above,
never silently "fixed".

## Script-12 raw cross-check (raw-verification worker, 2026-10-11 — raw landed
after this file's research; the record's frame facts were transcript-based)

- `analysis/slide_010_raw.json` read in full (model `glm-5.3-flash`; old
  extraction 10; kept_frame frame_00309, 34 frames). FULLY CONFIRMS the record's
  transcript-based frame facts: title "...of ONE Vector by a Matrix" (double
  spaces); subtitle "Example: Multiply Vector of Current Word X by W_q (Query)
  {Remember: W_q is Squared Matrix}"; middle strips Yᵀ[y₁..y₄] = Sigmoid / =
  Linear with the two-line "IF No Non-linearity" callout; right panels with the
  4×4 W_q grids (row 1 = W_11 W_21 W_31 W_41 … same as-printed convention as
  009) over bias columns b₁..b₄ vs 0,0,0,0 with the "IF No Bias" callout; badge
  "10".
- [?] RESOLVED (transcript truncation): the raw completed ALL sections
  (equations, animation state, full recreation brief) — no data was lost to the
  probe's mid-§4 truncation; nothing further to recover.
- [?] NARROWED (left-panel edge subscripts): raw reads the 16 weight labels
  grouped by source input (blue/magenta/orange/green ×4: W_11..W_41, W_12..W_42,
  W_13..W_43, W_14..W_44) — same convention as 009/012. Per-glyph certainty on
  the tiny edge labels remains a build-time zoom glance.
- Raw equation note (implied, not printed): "Y = W_q · X + b" — matches the
  record's semantics section.
- Script-13 final: NOT YET LANDED for 010. Corrections: none yet — verify against
  script-13 final when it lands.
