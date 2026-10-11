# SOURCES.md — slide 012 "Using FF NN for Multiplication of Vector by a Multiple Matrices"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Vision transcript of record:
`transcripts/slide_012_webverify.txt` (2026-10-11, default `images` route,
`--thinking high`, via `scripts/16_vision_gate.sh`).

## Slide identity

- Frame `unique_slides/slide_012.jpg`, badge "12". In pattern group P1
  [9,10,12,14,16] (founder: common pattern, not content dependency); no
  dependency edge — fresh verification done here.
- Frame facts (vision transcript, ground truth for WHAT is shown): title
  "Using  FF NN  for Multiplication of Vector by a Multiple Matrices"
  ("Multiple Matrices" underlined); blue subtitle "Example: Multiply Vector of
  Current Word by Multiple  (different) W_q   (Queries of Multiple Heads)";
  top-left token row X_1..X_4 under label "Embedding Vector of Current Word
  X_2"; THREE 4x4 weight grids labeled "W_Q of Head 1/2/3" on green / tan /
  lavender panels, each cell labeled W_ij (16 per grid); an "X_j" marker
  (purple) at Head 2's right edge marking the multiplying vector; a large "="
  to three per-head result vectors y_1..y_4 captioned "Corresponding
  Projection at Head 1/2/3" with final symbols Y_2^(1), Y_2^(2), Y_2^(3).
  Implied operation: X_2 · W_Q^(head) = Y_2^(head), per head.
- Video artifact: a black mouse-cursor graphic drawn inside the Head 1 grid
  (presenter pointer) — not slide content.
- Position in the lecture: review block; this is the slide that introduces
  (recaps from Part I) the idea that EACH head multiplies the current word's
  embedding by its OWN W_q — the query projection step of multi-head
  attention. FF NN in the title refers to the linear projection (feed-forward
  layer) doing the multiplication.

## Primary sources (both verified live 2026-10-11)

- **Vaswani et al. 2017, "Attention Is All You Need"** —
  https://arxiv.org/html/1706.03762v7, §3.2.2 "Multi-Head Attention"
  (WebFetch-confirmed verbatim excerpts): "Instead of performing a single
  attention function with d_model-dimensional keys, values and queries, we
  found it beneficial to" / "linearly project the queries, keys and values
  h times with different, learned linear projections to d_k, d_k and d_v
  dimensions"; head_i = Attention(QW_i^Q, KW_i^K, VW_i^V) with
  W_i^Q, W_i^K ∈ R^{d_model×d_k}, W_i^V ∈ R^{d_model×d_v};
  "In this work we employ h=8 parallel attention layers, or heads."
  **This is the paper-level establishment that each head owns its own learned
  W_q** — the exact claim the slide teaches.
- **Peter Bloem, "Transformers from scratch"** —
  https://peterbloem.nl/blog/transformers (WebFetch-confirmed): heads indexed
  r "each with different matrices W_q^r, W_k^r, W_v^r"; the "wide" self-
  attention variety gives every head a full-size k×k projection (matching the
  course's d×d per-head W legend from 001 slide 37). This is the course
  notation's provenance (001 precedent: slides 31–33, 37, 43).

## Figures used by this slide

**None — course-authored diagram.** No published figure is redrawn: the
element-by-element labeled 4x4 W grids with per-head color panels are the
instructor's own teaching drawing (Alammar-like multi-head color coding, but
the content — an explicit vector × W_Q expansion per head, no softmax/score
machinery — matches no published figure). Download decision: nothing
downloaded into this dir.

## What the sources CONFIRM

- Per-head, different, learned W_q matrices (the slide's whole point):
  Vaswani §3.2.2 (h=8 heads, "different, learned linear projections") +
  Bloem (W_q^r per head). CONFIRMED.
- Multiplying the CURRENT word's embedding by W_q yields the query — the
  slide's X_2 · W_Q^(head) = Y_2^(head): same semantics; the paper then runs
  attention with the projected q. The slide stops at the projection (that
  comes on later slides) — course's deliberate pedagogical order, not an
  error.
- The 4x4 d×d per-head W shape matches the course's own convention recorded
  for 001 (slide-37 legend: per-head W matrices d×d, "wide" variety per
  Bloem). Slide is internally consistent with that convention.

## Course vs paper discrepancies (NOT defects — recreation keeps course form)

- Course: h=3 heads (Head 1/2/3) and d=4; paper: h=8, d_model=512, d_k=64.
  Illustration choice, kept verbatim.
- Course dimension bookkeeping (d×d per head, output 1×d per head, NO
  concatenation shown on this slide) vs paper (d_k=d_model/h, concat +
  W^O). The concat/linear step appears on later slides (001's 43 pattern).
- Title wording "Multiplication of Vector by a Multiple Matrices" is the
  instructor's own (grammatically loose) English — verbatim, do not correct.

## Open questions

- none. (Subscript order inside the grids as printed — W_11 W_21 W_31 W_41
  across the top row — is legible and consistent across the three grids per
  the transcript; noted verbatim for recreation.)

## Script-12 raw cross-check (raw-verification worker, 2026-10-11 — raw landed
after this file's research; the record's frame facts were transcript-based)

- `analysis/slide_012_raw.json` read in full (model `images`; old extraction 17;
  kept_frame frame_00461, 74 frames). FULLY CONFIRMS the record: title with
  underlined "Multiple Matrices"; subtitle verbatim; three panels "W_Q of Head
  1/2/3"; identical 16-cell grids printed W_11 W_21 W_31 W_41 / W_12 … / W_13 … /
  W_14 … (raw: "subscript reads column,row" — the as-printed convention the
  record mandates stands); captions "Corresponding Projection at Head 1/2/3"
  (singular, vs 016's plural "Projections"); result symbols Y_2^(1)/(2)/(3);
  cursor artifact inside the Head 1 grid near W_12/W_22.
- [?] RESOLVED (Head-2 marker): raw reads "X_2 (magenta annotation below Head 2
  matrix, small arrow pointing up to cell W_43)" — the record's "X_j marker
  (purple) at Head 2's right edge" refines to: label X_2, magenta (#CC00CC),
  placed BELOW the Head-2 matrix, arrow pointing UP at cell W_43.
- No concat/linear stage on this slide (consistent with the record's
  course-order note; concat appears on the 017 pattern).
- Script-13 final: NOT YET LANDED for 012. Corrections: none yet — verify against
  script-13 final when it lands.
