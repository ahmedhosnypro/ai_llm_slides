# SOURCES.md — slide 016 "Using FF NN for Multiplication of Multiple Vectors by Multiple Matrices"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Vision transcript of record:
`transcripts/slide_016_webverify.txt` (2026-10-11, default `images` route,
`--thinking high`, via `scripts/16_vision_gate.sh`; banked by the earlier run —
reused as-is, no second probe spent on this slide).

## Slide identity

- Frame `unique_slides/slide_016.jpg`, badge "16" (timeline: t≈562–630 s, old
  extraction 26). Pattern group P1 [9,10,12,14,16] (founder: common pattern,
  not content dependency); no dep edge — fresh verification done here.
- Frame facts (vision transcript, ground truth for WHAT is shown): title
  "Using  FF NN  for Multiplication of Multiple Vectors by  Multiple Matrices";
  blue subtitle "Usage: Multiply Vectors of All Words by Multiple  (different)
  W_k   (Keys of Multiple Heads)". LEFT: five embedding-vector rows (X_1..X_5,
  each 4 circles x_1..x_4; rows 1–4 pink-outlined, row 5 blue-outlined).
  MIDDLE: three 4x4 weight grids "W_k of Head 1/2/3" on green / orange-tan /
  lavender panels, same W_ij index pattern in each. Large "=". BOTTOM: three
  5-row x 4-col output grids "Corresponding Projections at Head 1/2/3" (y_1..y_4
  per row), with a right-side caption column "Corresponding Projection of Word
  #1..#5". Bottom-left callout: "Sequence of 5 Words / Network with 3 Heads /
  Embedding Dimension=4".
- Video artifacts (do not recreate): mouse cursor over Head-1 grid near W_33;
  letterbox bars top/bottom. Head-1 row-1 first cell subscript [?] (reads
  W_?1, plausibly W_11) — JPEG blur; follow the Heads-2/3 pattern.
- Position in the lecture: P1 review block; this completes the progression 012
  (one vector × multiple W_q) → 014 (all vectors × one W_k/W_v) → 016 (all
  vectors × multiple per-head W_k): the KEY-projection step of multi-head
  attention computed for the whole sequence, per head.

## Primary sources (both re-confirmed live 2026-10-11, this session)

- **Vaswani et al. 2017, "Attention Is All You Need"** —
  https://arxiv.org/html/1706.03762v7, §3.2.2 (WebFetch-confirmed verbatim):
  "linearly project the queries, keys and values h times with different,
  learned linear projections"; head_i = Attention(QW^Q_i, KW^K_i, VW^V_i);
  MultiHead(Q,K,V) = Concat(head_1,...,head_h)W^O; "In this work we employ
  h=8 parallel attention layers, or heads." §3.2.3: "In a self-attention layer
  all of the keys, values and queries come from the same place."
  **Establishes exactly the slide's claim: EVERY word's embedding is multiplied
  by EACH head's own learned W_k.**
- **Peter Bloem, "Transformers from scratch"** —
  https://peterbloem.nl/blog/transformers (WebFetch-confirmed): several
  self-attention mechanisms indexed r "each with different matrices
  W_q^r, W_k^r, W_v^r"; "For input x_i each attention head produces a
  different output vector y_i^r"; the matrices are k×k (wide flavor — matches
  the course's squared d×d per-head W convention, 001 slide-37 legend /
  002 slide-012 precedent). Course notation provenance.

## Figures used by this slide

**None — course-authored diagram** (same conclusion as P1 siblings 012/014:
the element-labeled 4x4 grids with per-head color panels match no published
figure; Alammar-like color coding but no redraw of Vaswani Fig 1/2, Bloem, or
Alammar). Download decision: nothing downloaded into this dir.

## What the sources CONFIRM

- Per-head, different, learned W_k matrices applied to ALL words in the
  sequence (Y_i^(head) = X_i · W_k^(head) for every word i and head): paper
  §3.2.2 + §3.2.3. CONFIRMED.
- The multiplication itself is a linear (feed-forward) projection — the "FF NN"
  in the title — grounding carried from slide 014's record (Goodfellow Ch 6:
  linear-activation zero-bias FFN ≡ matrix multiply). CONFIRMED.
- d×d squared per-head W ("Embedding Dimension=4", 4x4 grids): course's wide-
  flavor convention per Bloem's k×k matrices. Internally consistent with 012/014.

## Course vs paper discrepancies (NOT defects — recreation keeps course form)

- Course: 5 words, 3 heads, d=4; paper: sequence length n, h=8,
  d_model=512, d_k=d_model/h=64. Illustration choice, kept verbatim.
- Course dimension bookkeeping (d×d per head, output vectors d-dim per head,
  NO concat/linear step shown on this slide) vs paper (project DOWN to d_k,
  concat + W^O). The concat step is 001:43's material (parent of 002 slide
  017); here the course deliberately stops at the per-head key projections.
- "Multiple Vectors by Multiple Matrices" title wording is the instructor's
  own (grammatically loose) English — verbatim, do not correct.

## Open questions

- [?] Head-1 grid row-1 first-cell subscript (W_?1 vs W_11) — JPEG blur;
  transcript resolves it as following the Heads-2/3 W_rowcol pattern. Zoom
  the video frame (t≈562–630 s) before building if the cell labels matter.

## Script-12 raw cross-check (raw-verification worker, 2026-10-11 — raw + final
both now on disk; the record's frame facts were transcript-based)

- `analysis/slide_016_raw.json` read in full (model `images`; old extraction 26;
  kept_frame frame_00631, 69 frames). FULLY CONFIRMS the record: five
  "Embedding Vector of Word #N" rows; "W_k of Head 1/2/3" grids with identical
  cell pattern (raw prints row 1 = w₁₁ w₂₁ w₃₁ w₄₁ in ALL THREE grids); large
  red "="; "Corresponding Projections at Head 1/2/3" (plural) + right column
  "Corresponding Projection of Word #1..#5"; summary box "Sequence of 5 Words /
  Network with 3 Heads / Embedding Dimension=4"; cursor artifact near Head 1's
  row 3.
- [?] RESOLVED (Head-1 first-cell subscript): raw reads W₁₁ (row 1 identical
  across all three grids) — resolves the record's "W_?1" JPEG-blur item toward
  W_11 (raw + Heads-2/3 pattern agree).
- Raw additions: a thin red curved brace-like arc hugging the upper panel's
  right inner edge, grouping the three W_k matrices [?]; pill fill cycle
  green/orange/purple per output group; matrix row fills
  yellow/pink/orange/green.
- Script-13 final ALREADY LANDED: `analysis/slide_016_final.json`
  (PASS_WITH_FIXES); `slide_title` matches the raw verbatim. Corrections: none
  yet at title level — verify against the final's fix list when building.
