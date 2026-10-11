# SOURCES.md — slide 044 "Multi Head Self Attention of Word X₂ — 'Wide' Architecture (+ Figure 2 right inset)"

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via live WebFetch
of the arXiv HTML v7 (MultiHead/head_i equations, the h=8/d_k sentence, the Figure 2
caption); no image access — frame facts below come from the script-12 raw
transcription (`analysis/slide_044_raw.json`) plus the founder/coordinator frame
note on the occlusions (2026-10-11).

## Slide identity

- New (curated) slide **044** ← old extraction slide **117**
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_044.jpg`
  (badge 44; kept frame `frame_04334.jpg`).
- Frame facts (script-12 raw of 2026-10-11, ground truth for WHAT is shown): title
  "Multi Head Self Attention of Word X₂" (X₂ red); subtitle '"Wide" Architecture' —
  its right tail OCCLUDED by the inset panel (visible glyphs read '"Wide"
  Architec...'); slide 43's five-head Wide composition (per-head layers h=1…h=5,
  per-head Dot Product → Scaling by √d → Soft max → Σ Weighted SUM pipeline,
  "Concatenated Vector 1×dH" → "Linear Transformation [T] dH×d" → output 1×d,
  d×d W legend "d: Embedding Length") PLUS a green-framed inset reproducing the
  paper's Figure 2 right topology.
- Dependency: **44 ← 43** (`slide_dependencies.json`) — child = 43's certified
  composition + delta (the green-framed inset). Build is gated on 43's
  certification; analysis/validation are not gated. This file's figure-bank
  reference is the founder-declared `shared_image_sources["44"]`.

## Primary source

- **URL**: https://arxiv.org/html/1706.03762v7 (verified live 2026-10-11; also
  verified live the same day in `../slide_014_source/` and `../slide_18_source/`)
- **Paper**: "Attention Is All You Need" — Vaswani, Shazeer, Parmar, Uszkoreit,
  Jones, Gomez, Kaiser, Polosukhin (2017), arXiv:1706.03762v7 [cs.CL]

## Figures used by this slide

**Per-figure use: Figure 2 RIGHT only** — the green-bordered inset is a course-style
redraw of Figure 2 right. (Figure 2 left is slide 38's inset; slides 14–19 draw on
Figure 1 — see `slide_dependencies.json` `shared_image_sources_note`.)

- **Figure 2** — caption (verbatim, v7, live-verified 2026-10-11): "Figure 2:
  (left) Scaled Dot-Product Attention. (right) Multi-Head Attention consists of
  several attention layers running in parallel." The inset is the RIGHT panel.
- Founder-downloaded original already banked in
  `../slide_18_source/slide18 Multi-Head Attention\n\n.png` (835×1282 RGBA;
  ⚠️ filename contains literal newline characters — always quote it in shell) —
  **do not modify that dir's files**; this slide references it. No new figures were
  downloaded into this dir.
- arXiv v7 image asset for Figure 2 recorded as `Figures/ModalNet-20.png`
  (figure-bank reference 2026-10-11; the banked founder copy of the right panel is
  the file above; Figure 1's sibling asset `Figures/ModalNet-21.png` was
  byte-verified in `../slide_014_source/SOURCES.md`).

## What the paper CONFIRMS (data behind the slide)

- The inset topology is exactly the paper's Figure 2 right, bottom-up: three
  **Linear** boxes under **V, K, Q** → a stack of h parallel **Scaled Dot-Product
  Attention** layers (annotated *h*) → **Concat** → a top **Linear**. The raw's
  inset labels (Linear, Concat, Scaled Dot-Product Attention, h, V, K, Q) match the
  figure label-for-label.
- §3.2.2 (live-verified 2026-10-11): "MultiHead(Q,K,V) =
  Concat(head_1,...,head_h)W^O" with "head_i = Attention(QW^Q_i, KW^K_i, VW^V_i)".
  (In the v7 HTML these two equations are unnumbered — v7's (2)/(3) are the FFN and
  learning-rate equations.) The slide's Wide pipeline — per-head attention →
  "Concatenated Vector 1×dH" → "Linear Transformation [T] dH×d" → output 1×d — is
  exactly this equation, and, unlike slide 45's Narrow, it RETAINS the output
  projection (the course's "Linear Transformation" = W^O), so its structure matches
  the paper's multi-head.
- §3.2.1 eq. (1): Attention(Q,K,V) = softmax(QKᵀ/√d_k)V — the operation inside each
  head (Dot Product → "Scaling by √d" → "Soft max" → Σ Weighted SUM).
- Config sentence (live-verified 2026-10-11): "In this work we employ h=8 parallel
  attention layers, or heads. For each of these we use d_k=d_v=d_model/h=64." —
  the paper's numbers behind the course's "H Heads" inset annotation.
- Projections: W_i^Q ∈ ℝ^{d_model×d_k}, etc., and W^O ∈ ℝ^{h·d_v×d_model}. The
  course's dimension bookkeeping differs (per-head d×d W → concat 1×dH → dH×d linear
  → 1×d; see `../slide_043_source/SOURCES.md` §5) — same concat-then-linear
  structure, different accounting; course numbers kept verbatim.

## Course-authored elements (no paper counterpart — not paper data, do not "fix" to paper)

- The five overlapping pastel head layers with h=1…h=5 badges and the
  Similarity/Probabilities/Weighted SUM pills; the course labels "Linear
  Transformation [T] dH×d", "Concatenated Vector 1×dH", "Scaling by √d", "Soft max",
  "Dot Product", "K,q"; the 3×3 grid of per-head W_q/W_k/W_v boxes; the green-dashed
  d×d W legend ("d: Embedding Length"); the X₂ pink highlight; the thick red curved
  arrow labeled "H¹ Heads"; the bottom-left input strip — all the course's own
  drawing in its house style, not the paper's figure pixels.
- The OCCLUSIONS are real frame content the recreation must reproduce: the inset
  panel partially covers the subtitle's right tail ('"Wide" Architec...') and the
  h=5 layer's badge.
- Course illustrates h=5 heads; the paper uses h=8. Illustration choice, kept
  verbatim.

## [?] Uncertain items

- [?] h=5 layer fill color and full extent: mostly occluded behind the inset in the
  frame; the slide-45 family pattern (h=5 = cream #F2EAD3 there) suggests cream —
  verify against the frame at build time.
- [?] Concatenated-vector bar groups: the raw read 4 labeled groups (Y¹…Y⁴, ~3 cells
  each). With five heads a fifth group (Y⁵) may exist (possibly hidden near the
  inset) or the course may draw only 4 illustrative groups — frame-only question.
- [?] W-matrix grid: the raw read 3 rows (W_q¹…W_v³); whether rows for heads 4/5
  exist (drawn or occluded) is a frame-only question.
- [?] Final output vector label: the raw reads "Y₁" while the slide tracks word X₂
  (title; cf. slide 37's Y₂ for X₂). Keep the raw's reading verbatim unless a
  build-time frame read shows otherwise.
- [?] Red curved-arrow label glyphs: raw reads "H¹ Heads" (slide 45's raw reads
  '"H" Heads' on the same family arrow) — exact glyphs a frame fact.
- [?] Subtitle tail beyond "Architec..." is occluded; presumed "Architecture".

## Corrections

- Cross-checked 2026-10-11 (correction worker): `analysis/slide_044_raw.json` vs the
  live-verified paper facts, `../slide_043_source/SOURCES.md` (parent composition)
  and the founder/coordinator frame note. The Wide architecture, the inset's
  Figure 2 right topology, and the "Linear Transformation [T] dH×d" /
  "Concatenated Vector 1×dH" labels all confirmed. ONE raw defect patched: the raw
  under-counted the head layers as four (h=1…h=4) — the frame carries slide 43's
  FIVE-head base, with the h=5 badge partially occluded by the inset (dependency
  edge 44←43 + founder frame note 2026-10-11). Patched in the raw: labels list
  (h=5 added), layout arrangement, head-layers region, main-diagram description,
  and recreation brief (five layers; inset drawn ON TOP so it occludes the subtitle
  tail and the h=5 badge as in the original).
- No other patches; the [?] items above stay.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout, verbatim
text, drawn content). This source confirms/corrects DATA and records provenance; it
never licenses inventing or "improving" content the slide doesn't show. If source
and slide disagree, record the discrepancy above — the slide wins for recreation,
the source wins for understanding.
