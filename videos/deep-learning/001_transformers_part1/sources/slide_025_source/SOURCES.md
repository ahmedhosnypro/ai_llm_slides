# SOURCES.md — slide 025 "Encoder – Decoder Transformer" (three-panel zoom)

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via the
figure-family records in `slide_018_source/SOURCES.md` (arXiv HTML v7 verified
live 2026-10-11 there; asset byte-sizes and sha256 recorded there) + script-12
raw transcription `analysis/slide_025_raw.json` as the only eye on the frame.
No new fetches needed for this slide — the paper and its figures were verified
live earlier today by the figure-family worker.

## Slide identity

- New (curated) slide **025** ← old extraction slide **50** (diff 0.0)
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_025.jpg`.
- Frame facts (raw transcription): a **zoom-ladder slide** — three panels:
  LEFT = tan "Scaled Dot-Product Attention" flowchart (Q/K/V circles → MatMul →
  Scale → Mask (opt.) → SoftMax → MatMul, green corner brackets); CENTER =
  "Multi-Head Attention" panel (V/K/q circles → three Linear boxes → stacked
  Scaled Dot-Product Attention boxes annotated "h" → Concat → Linear, green
  border); RIGHT = full encoder-decoder Transformer architecture (peach
  Encoder + green Decoder, all paper-Figure-1 blocks) with the two Multi-Head
  Attention boxes outlined in red and a yellow highlight behind the decoder's
  upper stack. Red dashed callout lines connect left → center → the red
  MHA boxes; a dark-red speech bubble "WE ARE HERE" points at the left panel.
  Title "Encoder – Decoder Transformer" (en dash); badge "25".

> **Relationship to the figure bank:** the paper originals are banked in
> `../slide_18_source/` (founder downloads + its own SOURCES.md; that dir name
> predates the 2026-10-11 curation). The bank serves the whole figure family;
> do not modify it. This slide is old extraction 50.

## Primary source

- **URL**: https://arxiv.org/html/1706.03762v7 (verified live 2026-10-11 in
  `slide_018_source/SOURCES.md`)
- **Paper**: "Attention Is All You Need" — Vaswani, Shazeer, Parmar, Uszkoreit,
  Jones, Gomez, Kaiser, Polosukhin (2017), arXiv:1706.03762v7 [cs.CL]

## Figures used by this slide

**Per-figure use: all three — Figure 1 + Figure 2 left + Figure 2 right** (the
same trio as slides 018/019, here redrawn in the course's style as three panels
of a zoom ladder: Fig 2-left panel → Fig 2-right panel → Fig 1 architecture).

- **Figure 1** — caption (verbatim, v7): "Figure 1: The Transformer - model
  architecture." Original banked: `../slide_18_source/The Transformer - model
  architecture..png` (159,152 bytes, sha256 `56d69ccc…`); asset
  https://arxiv.org/html/1706.03762v7/Figures/ModalNet-21.png (id `S3.F1.g1`).
- **Figure 2 (left)** — caption (verbatim, v7): "(left) Scaled Dot-Product
  Attention. …" Original banked: `../slide_18_source/slide18 scaled
  dot-production attention figure.png` (26,323 bytes, sha256 `6d40a44e…`);
  asset https://arxiv.org/html/1706.03762v7/Figures/ModalNet-19.png
  (id `S3.F2.g1`).
- **Figure 2 (right)** — caption (verbatim, v7): "… (right) Multi-Head Attention
  consists of several attention layers running in parallel." Original banked:
  `../slide_18_source/slide18 Multi-Head Attention\n\n.png` (65,853 bytes,
  sha256 `ba8a3ede…`; filename contains literal newlines — quote in shell);
  asset https://arxiv.org/html/1706.03762v7/Figures/ModalNet-20.png
  (id `S3.F2.g2`).
- No new figures were downloaded into this dir.

## What the paper CONFIRMS (data behind the slide)

- LEFT panel = Figure 2 left; its math is §3.2.1 equation (1), verbatim:
  **Attention(Q, K, V) = softmax(QKᵀ/√d_k) V** — "the dot products of the query
  with all keys, divide each by √d_k, and apply a softmax function to obtain the
  weights on the values", i.e. the MatMul → Scale → Mask (opt.) → SoftMax →
  MatMul pipeline the panel draws (Mask optional = padding/masking step, §3.2.3.1
  for the decoder's use).
- CENTER panel = Figure 2 right; its math is §3.2.2, verbatim:
  **MultiHead(Q, K, V) = Concat(head₁, …, head_h) Wᴼ** with
  **head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)** — h parallel Linear →
  Scaled Dot-Product Attention branches → Concat → Linear, exactly the panel's
  flow; the "h" annotation = the number of heads ("we employ h = 8 parallel
  attention layers, or heads", d_k = d_v = d_model/h = 64, §3.2.2).
- RIGHT panel = Figure 1 redrawn: every transcribed block label matches the
  paper's figure labels — Input Embedding, Positional Encoding, Add & Norm,
  Multi-Head Attention, Feed Forward, Masked Multi-Head Attention, Output
  Embedding, Outputs (shifted right), Linear, Softmax, Output Probabilities,
  Inputs, Nx. Stack counts behind the "Nx" glyphs: N = 6 identical layers per
  stack (§3.1); residual + layer norm = LayerNorm(x + Sublayer(x)) (§3.1).
- The zoom ladder itself is coherent with the paper: the two red-outlined
  Multi-Head Attention boxes inside the architecture (encoder self-attention,
  decoder cross-attention over the encoder output, §3.2.3) are exactly the two
  constructs whose internals the left/center panels blow up.

## Course-authored elements (no paper counterpart — do not "fix" to paper)

- The zoom-ladder composition, the "WE ARE HERE" speech bubble, the red dashed
  callout lines, the green corner brackets, the red outlines on the MHA boxes,
  the yellow highlight rectangle over the decoder stack, the tan/green panel
  containers and full recoloring, and the course-styled Q/K/V circles. The
  paper's figures are monochrome and contain none of this.
- Casing quirks the raw explicitly preserves are FRAME facts, not errors:
  "SoftMax" (left panel, matching the paper's Figure 2) vs "Softmax" (decoder,
  matching Figure 1), and lowercase "q" in the center panel. Keep verbatim.

## [?] Uncertain items

- [?] Exact in-figure glyph casing of the paper's Figure 2 labels ("SoftMax",
  "Mask (opt.)") is read here from the banked PNGs' established content, not
  from an OCR of this slide; the raw's transcription is consistent with it, and
  the frame is ground truth regardless.
- [?] Exact attachment points of the four red dashed callout lines and the tail
  target of the "WE ARE HERE" bubble — layout facts only the frame can answer.
- [?] The number of offset (rear) Scaled-Dot-Product copies in the center panel
  stack ("3-4" per raw) — frame-level detail.

## Corrections

none — every label set checked against the paper's Figures 1/2 and §3.2.1/§3.2.2
text (verified live today in the figure-family records): matches; nothing to
correct.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout, verbatim
text, drawn content). This source confirms/corrects DATA and records provenance; it
never licenses inventing or "improving" content the slide doesn't show. If source
and slide disagree, record the discrepancy above — the slide wins for recreation,
the source wins for understanding.
