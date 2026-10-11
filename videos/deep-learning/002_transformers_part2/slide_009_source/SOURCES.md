# SOURCES.md — slide 009 "Using  FF NN  for Multiplication of a Vector by a Matrix"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Written 2026-10-11 by the Part II web-verification
worker.

## Slide identity

- Frame `unique_slides/slide_009.jpg`, badge numeral **9** (matches file id).
- Old extraction: slide 9 ← old 9 (`unique_slides/new2old_mapping.json`).
- Dependency: 009 is the PARENT of 010 (edge 10 ← 009) and head of pattern group
  P1 [9,10,12,14,16].

## Vision transcript of record

- `transcripts/slide009_vision_2026-10-11.txt` — ONE default-route (`images`) probe,
  `--thinking high --max-tokens 65536`, via `scripts/16_vision_gate.sh`; winner
  `images (round 1, attempt 1)`, degenerate events 0. Cross-checked against the
  pre-existing script-12 raw `analysis/slide_009_raw.json` — consistent.

## Frame facts (vision, ground truth)

- Title (verbatim, with double spaces): "Using  FF NN  for Multiplication of a
  Vector by a Matrix"; badge "9" (yellow circle, red border).
- LEFT panel: fully-connected K₄,₄ network — 4 pink input circles x₁..x₄ (stacked,
  heading "Input Word X", "X" red) → 4 white Σ nodes each containing a sigmoid
  S-curve glyph → outputs y₁..y₄ (green arrows) with green bias inputs b₁..b₄
  from below; 16 edges; weight labels grouped near each input (near x₁:
  w_11,w_21,w_31,w_41; near x₂: w_12,w_22,w_32,w_42; near x₃: w_13,w_23,w_33,w_43;
  near x₄: w_14,w_24,w_34,w_44).
- RIGHT panel, equation-as-graphic left→right:
  **Yᵀ [y₁ y₂ y₃ y₄] = Sigmoid( X [x₁ x₂ x₃ x₄] · [w_11 w_21 w_31 w_41;
  w_12 w_22 w_32 w_42; w_13 w_23 w_33 w_43; w_14 w_24 w_34 w_44] + [b₁; b₂; b₃;
  b₄] )** — "= Sigmoid" in blue italic; blue curly braces; X row vector in a pink
  container ("X" red below); 4×4 weight grid in a light-green container (row
  fills yellow/orange/orange/green); blue "+"; bias column b₁..b₄ in a green
  container with a red curly brace.

## Primary source

- **Slide itself: course-authored pedagogy** (instructor-built diagram + equation
  graphic; the probe explicitly finds no match to Vaswani Fig 1/2, Bloem, or
  Alammar artwork).
- **Canonical math reference (agy-confirmed 2026-10-11, `../scratch/agy_s009.txt`)**:
  Goodfellow, Bengio, Courville, *Deep Learning*, Chapter 6 (Deep Feedforward
  Networks) — the fully-connected layer as y = σ(xW + b):
  https://www.deeplearningbook.org/contents/mlp.html (canonical URL; the book
  chapter was not re-fetched this run — the identity y = σ(Wx+b) is standard and
  the URL is the book's official site).
- **In-course relevance**: this is the "linear transformation of inputs" step the
  self-attention pipeline uses (W_q/W_k/W_v projections — slides 008's legend
  (1×d)·W(d×d)=(1×d) and 001's 30–33 family); the course teaches the FC layer
  first, then reuses it for attention projections.

## What the source CONFIRMS (math behind the slide)

- **Indexing convention, internally consistent** (verified against the edge
  labels): w_ij = weight from INPUT j to OUTPUT i (first index = output). Then
  y_i = Σ_j w_ij·x_j + b_i passed through sigmoid — exactly the standard
  column-vector form y = σ(Wx + b) with W's rows = outputs; the slide renders X
  as a row vector times this W (row-vector product x·M gives the same y_i).
  The displayed matrix is therefore the standard W, not a transposed error.
- 16 weights (4×4), 4 biases, sigmoid activation per Σ node — matches the
  Goodfellow ch. 6 single-layer formulation.
- No numeric cell VALUES are shown (symbols only) — no data to recompute.

## Course-authored elements (do not "fix" to a source)

- Clip-art node/edge styling, colored matrix-cell fills, the "Input Word X"
  heading (the generic vector is framed as a word embedding), the Yᵀ row-vector
  notation, and the double-space title spacing — all instructor's own; keep
  verbatim (title spacing is frame ground truth, not an error to correct).

## [?] Uncertain items

- [?] One matrix-cell glyph in the left panel's near-x₃ weight stack read only
  partially ("consistent with w_13", probe) — the right-panel matrix reads
  cleanly, so the convention is certain; the single glyph needs only a build-time
  zoom glance.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows; the Goodfellow
reference confirms the math. Discrepancies are recorded above, never silently
"fixed".

## Script-12 raw cross-check (raw-verification worker, 2026-10-11)

- `analysis/slide_009_raw.json` re-read in full (model `images`; old extraction 9;
  kept_frame frame_00275, 147 frames — the longest-taught slide of the review
  block). Fully consistent with this record: 16 weight labels grouped by source
  input (x₁ blue, x₂ purple, x₃ orange, x₄ green), equation graphic
  Yᵀ = Sigmoid{ X·W + b } with the 4×4 matrix printed W₁₁ W₂₁ W₃₁ W₄₁ / W₁₂ … /
  W₁₃ … / W₁₄ … (first index = output — the record's indexing verification
  stands), bias column b₁..b₄, cursor artifact in the right panel.
- [?] RESOLVED (single glyph): raw's label list reads all 16 matrix/stack labels
  cleanly, including the near-x₃ group W₁₃ W₂₃ W₃₃ W₄₃ — the record's
  "one partially-read cell glyph" is resolved toward w_13 (raw + right-panel
  matrix agree). Convention unchanged.
- Script-13 final: NOT YET LANDED for 009. Corrections: none yet — verify against
  script-13 final when it lands.
