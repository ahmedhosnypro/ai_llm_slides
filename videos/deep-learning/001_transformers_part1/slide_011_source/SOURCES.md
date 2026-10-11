# SOURCES.md — slide 011 "Transformer" (subtitle: "Attention is All You Need")

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via arXiv HTML
v7 WebFetch + agy search; no image access — frame facts below come from the
script-12 raw transcription (`../analysis/slide_011_raw.json`).

## Slide identity

- New (curated) slide **011** ← old extraction slide **20**, diff 0.0
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_011.jpg`,
  kept frame `frame_00748.jpg` (645–747 s of the lecture).
- Frame facts (vision pass — ground truth for WHAT is shown): course-style
  simplified Transformer architecture — LEFT encoder column (lavender
  'attention' sub-block on an orange "Multi Head Self Attention Blocks" block,
  inputs x₁ x₂ x₃) and RIGHT decoder column (yellow "Multi Head Self Attention
  Blocks" block, outputs o₁ o₂ o₃, a lavender self-loop block labeled
  "Encoder-Decoder Attention"); thick red arrow + dashed salmon curves linking
  encoder→decoder; beige note box "Attention Mechanism supports:" with three
  bullets (Parallelization of Encoder, / Parallelization of Decoder
  (Training Mode Only) / Very Long  Sequence length — 'Parallelization' and
  'Sequence length' styled as blue underlined hyperlinks).

## Primary source

- **URL**: https://arxiv.org/html/1706.03762v7 (verified live 2026-10-11);
  v5 PDF banked in `../slide_012_source/` (the same paper, page 1, is slide 12).
- **Paper**: "Attention Is All You Need" — Vaswani et al. (2017),
  arXiv:1706.03762 [cs.CL].

## What the source CONFIRMS (data behind the slide)

- **Architecture concept**: the paper's abstract — "The best performing models
  also connect the encoder and decoder through an attention mechanism." The
  slide's encoder-block → attention → decoder-block topology (with explicit
  cross-attention link) matches this framing; the slide's title/subtitle name
  the paper itself.
- **"Parallelization of Encoder"** (and of Decoder in training mode): abstract
  (v5, verified via pdftotext) — "...show these models to be superior in
  quality while being more parallelizable and requiring significantly less time
  to train."
- **"Very Long  Sequence length"**: §4 "Why Self-Attention" (v7, verified live)
  — Table 1 gives Self-Attention O(1) sequential operations and O(1) maximum
  path length vs Recurrent O(n) / O(n); "The shorter these paths between any
  combination of positions in the input and output sequences, the easier it is
  to learn long-range dependencies."

## Course-authored elements (no paper counterpart — do not "fix" to paper)

- ALL on-slide labels are the course's own wording, not the paper's Figure 1
  labels ("Multi Head Self Attention Blocks" ×2, the small 'attention' box,
  "Encoder-Decoder Attention" ×2, red Encoder/Decoder italics, x/o token
  treatment). Paper Fig 1 uses Nx stacks / Multi-Head Attention / Masked
  Multi-Head Attention / Add & Norm / Feed Forward / Positional Encoding.
- The orange/yellow/lavender palette, the thick red arrow, the dashed salmon
  connectors, the note box, and its bullets' phrasing (including the trailing
  comma in "Parallelization of Encoder ,", the space in "( Training Mode
  Only)", and the double space in "Very Long  Sequence length") are frame-
  faithful course text — recreate verbatim, never normalize.
- No figure was downloaded: the diagram is a course simplification, not a reuse
  of a public figure's pixels. agy suggested Jay Alammar /
  Wikipedia diagrams as conceptually similar, but their known labels/palettes
  do not match this slide's wording — recorded under [?], not treated as a
  match. (Paper Figure 1 belongs to the 14–19 family per AGENTS.md, not here.)

## [?] Uncertain items

- [?] Exact anchor of the red italic "Decoder" label — raw's Header region says
  "at right of subtitle line"; a layout fact only the frame can pin.
- [?] Dashed salmon connector count: raw itself hedges "Two or three thin
  DASHED salmon-pink curved lines" — needs a frame re-look (2 vs 3).
- [?] Whether any public simplified-transformer figure the course may have
  redrawn exists with these exact labels — agy search inconclusive (its two
  candidates don't use this wording); treated as course-authored.

## Corrections

none — no evidenced transcription DATA errors found (the abstract's
parallelization claims and the §4 long-sequence rationale check out; nothing on
the frame contradicted the source data).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout,
verbatim text, drawn content). This source confirms/corrects DATA and records
provenance; it never licenses inventing or "improving" content the slide doesn't
show. If source and slide disagree, record the discrepancy above — the slide
wins for recreation, the source wins for understanding.
