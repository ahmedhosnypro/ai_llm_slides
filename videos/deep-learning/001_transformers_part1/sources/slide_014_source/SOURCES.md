# SOURCES.md — slide 014 "Encoder – Decoder Transformer"

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via WebFetch of
arXiv HTML v7 (no vision calls run; no image access — frame facts below come from
the verified vision pass description of 2026-10-11).

## Slide identity

- New (curated) slide **014** ← old extraction slide **28**
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_014.jpg`.
- Frame facts (vision pass, ground truth for WHAT is shown): title
  "Encoder – Decoder Transformer"; **Figure 1 of the paper shown twice** — upright
  copy on the left, a 90°-rotated copy on the right — joined by a red arrow;
  course captions "Orientation is not the Issue" / "Let us focus on the Building
  blocks".

## Primary source

- **URL**: https://arxiv.org/html/1706.03762v7 (verified live 2026-10-11)
- **Paper**: "Attention Is All You Need" — Vaswani, Shazeer, Parmar, Uszkoreit,
  Jones, Gomez, Kaiser, Polosukhin (2017), arXiv:1706.03762v7 [cs.CL]

## Figures used by this slide

**Per-figure use: Figure 1 ONLY** (consistent with the vision verification; this
slide does not draw on Figure 2 left/right).

- **Figure 1** — caption (verbatim, v7): "Figure 1: The Transformer - model
  architecture."
- Founder-downloaded original already banked in `../slide_18_source/The Transformer -
  model architecture..png` (1520×2239) — **do not modify that dir's files**; this
  slide references it. No new figures were downloaded into this dir.
- arXiv v7 asset provenance (verified live, byte-identical to the founder's
  download — 159,152 bytes):
  https://arxiv.org/html/1706.03762v7/Figures/ModalNet-21.png
  (in-page src `1706.03762v7/Figures/ModalNet-21.png`, id `S3.F1.g1`).

## What the paper CONFIRMS (data behind the slide)

- The figure identity: the twice-shown diagram is the paper's Figure 1, and the
  slide's title names exactly what the paper's §3.1 ("Encoder and Decoder Stacks")
  describes — "The Transformer follows this overall architecture using stacked
  self-attention and point-wise, fully connected layers for both the encoder and
  decoder." Encoder–decoder composition is the paper's own framing.
- The figure's internal labels are the paper's (Nx encoder stack, Nx decoder
  stack, Positional Encoding, Add & Norm, Feed Forward, Multi-Head Attention,
  Masked Multi-Head Attention, Linear, Softmax, "Outputs (shifted right)",
  Inputs / Output Probabilities).
- The stack counts behind the "Nx" glyphs: "The encoder is composed of a stack of
  N=6 identical layers" and "The decoder is also composed of a stack of N=6
  identical layers."

## Course-authored elements (no paper counterpart — not paper data, do not "fix" to paper)

- The 90° rotation of the right copy of Figure 1, the red arrow, and the two
  captions "Orientation is not the Issue" / "Let us focus on the Building blocks"
  are instructor pedagogy on the FRAME. The paper obviously contains neither; the
  frame is ground truth for them.

## [?] Uncertain items

- RESOLVED (raw): the red arrow connects nothing specific — it is a freestanding
  thick dark-red open arc (~270°, solid triangular head) in the gutter between
  the two panels at mid-height (~44–51% width, ~48–64% height), a rotation
  indicator between the vertical copy and the rotated copy.
- RESOLVED (raw): rotation direction is 90° CLOCKWISE — the raw's geometry
  (Inputs upper-left, encoder strip on top, Output Probabilities at far right,
  flow left→right) is exactly the CW result; its original "counter-clockwise"
  wording contradicted its own geometry and was patched (see Corrections).

## Corrections

Raw cross-check done 2026-10-11 (W-D re-run). Three evidenced patches to
`../analysis/slide_014_raw.json` (`_meta` untouched):

1. **Block-label casing**: "Multi-head Attention" / "Masked Multi-head
   Attention" → "Multi-Head Attention" / "Masked Multi-Head Attention"
   (replace_all across labels, descriptions, brief; 0 lowercase remnants).
   Evidence: the paper's Figure 1 labels (banked byte-identical original), the
   founder-verified rule that the redraws keep the paper's labels, and all five
   sibling raws (slides 015–019) transcribing capital H.
2. **Missing flat label**: the left copy's flat labels list held only 4×
   "Add & Norm" vs the 5 boxes the raw's own structured description enumerates
   (2 encoder + 3 decoder), the paper topology, and the right copy's list (5×).
   Inserted one "Add & Norm" after the copy-1 "Feed Forward" (now 5+5).
3. **Rotation-direction word**: "counter-clockwise" → "clockwise" (2 sites:
   right-panel description + recreation brief step 9). The raw's own geometry
   (Inputs upper-left, encoder strip on top, Output Probabilities far right,
   flow left→right) is the 90°-CW result; CCW would mirror it.

Kept as transcribed: the box-text reading note "bottom-to-top" for the rotated
panel's vertical labels (direct observation; under a rigid CW rotation text
would read top-to-bottom, so the course likely drew the vertical labels
bottom-to-top in a rebuilt landscape panel — builder verifies against frame).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout, verbatim
text, drawn content). This source confirms/corrects DATA and records provenance; it
never licenses inventing or "improving" content the slide doesn't show. If source
and slide disagree, record the discrepancy above — the slide wins for recreation,
the source wins for understanding.
