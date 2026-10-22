# SOURCES.md — slide 019 "Transformer block anatomy (paper figures)" — working title, see [?]

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via WebFetch of
arXiv HTML v7 (no vision calls run; no image access — frame facts below come from
the verified vision pass description of 2026-10-11).

## Slide identity

- New (curated) slide **019** ← old extraction slide **44**
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_019.jpg`.
- Frame facts (vision pass, ground truth for WHAT is shown): the same **three
  paper figures** as slide 018 — Figure 1 (full architecture) plus Figure 2
  left (Scaled Dot-Product Attention) and Figure 2 right (Multi-Head Attention)
  as enlarged insets — but the two banners are **replaced by three color
  callouts**: **Normalization Layer (blue)**, **Feed Forward Layer (gray)**,
  **Residual Connections (green)**; **green residual arrows** looping the
  sub-layers; and **recoloring of the "Add & Norm" and "Feed Forward" blocks**
  to match the callouts.

> **Relationship to the figure bank:** the paper originals are banked in
> `../slide_18_source/` (founder downloads + its own SOURCES.md; that dir's name
> predates curation — this slide is old extraction 44, and the bank serves the
> whole 14–19 figure family per the video AGENTS.md). Do not modify the bank;
> this slide references it.

## Primary source

- **URL**: https://arxiv.org/html/1706.03762v7 (verified live 2026-10-11)
- **Paper**: "Attention Is All You Need" — Vaswani, Shazeer, Parmar, Uszkoreit,
  Jones, Gomez, Kaiser, Polosukhin (2017), arXiv:1706.03762v7 [cs.CL]

## Figures used by this slide

**Per-figure use: Figure 1 + Figure 2 left + Figure 2 right** (consistent with
the vision verification; same trio as slide 018, with different pedagogy
overlaid).

- **Figure 1** — caption (verbatim, v7): "Figure 1: The Transformer - model
  architecture."
- **Figure 2 (left)** — caption (verbatim, v7): "(left) Scaled Dot-Product
  Attention. …"
- **Figure 2 (right)** — caption (verbatim, v7): "… (right) Multi-Head Attention
  consists of several attention layers running in parallel."
- All three originals are banked in `../slide_18_source/` (founder downloads,
  **do not modify that dir's files**; this slide references them). No new
  figures were downloaded into this dir.
- arXiv v7 asset provenance (verified live 2026-10-11, **byte-identical to the
  founder's downloads** — byte size and sha256 all match):
  - Figure 1: https://arxiv.org/html/1706.03762v7/Figures/ModalNet-21.png
    (in-page src `1706.03762v7/Figures/ModalNet-21.png`, id `S3.F1.g1`),
    159,152 bytes, sha256 `56d69ccc…` = bank's `The Transformer - model
    architecture..png`.
  - Figure 2 left: https://arxiv.org/html/1706.03762v7/Figures/ModalNet-19.png
    (in-page src `1706.03762v7/Figures/ModalNet-19.png`, id `S3.F2.g1`),
    26,323 bytes, sha256 `6d40a44e…` = bank's `slide18 scaled dot-production
    attention figure.png`.
  - Figure 2 right: https://arxiv.org/html/1706.03762v7/Figures/ModalNet-20.png
    (in-page src `1706.03762v7/Figures/ModalNet-20.png`, id `S3.F2.g2`),
    65,853 bytes, sha256 `ba8a3ede…` = bank's `slide18 Multi-Head Attention\n\n.png`
    (filename contains literal newlines — quote it in shell).

## What the paper CONFIRMS (data behind the slide)

- The "Residual Connections" callout and green looping arrows: §3.1 — "We employ
  a residual connection [11] around each of the two sub-layers, followed by
  layer normalization [1]. That is, the output of each sub-layer is
  LayerNorm(x + Sublayer(x))" — a residual wraps EVERY sub-layer, which is what
  the looping arrows depict.
- The "Normalization Layer" callout: layer normalization [1] applied after each
  residual (the "Add & Norm" blocks in Figure 1 are exactly this construct).
- The "Feed Forward Layer" callout: §3.3 — a "position-wise fully connected
  feed-forward network … applied to each position separately and identically",
  verbatim **FFN(x) = max(0, xW₁ + b₁)W₂ + b₂** ("two linear transformations
  with a ReLU activation in between") — the "Feed Forward" blocks in Figure 1.
- Figure-1 topology these callouts point into: encoder/decoder stacks of N=6
  identical layers (§3.1), each with multi-head self-attention and (decoder
  additionally) encoder-decoder attention sub-layers.
- The Multi-Head Attention inset: §3.2.2 — MultiHead(Q, K, V) =
  Concat(head₁, …, head_h)Wᴼ, head_i = Attention(QW_i^Q, KW_i^K, VW_i^V), with
  h = 8 and d_k = d_v = d_model/h = 64.
- The Scaled Dot-Product Attention inset: §3.2.1 equation (1) —
  Attention(Q, K, V) = softmax(QKᵀ/√d_k) V.

## Course-authored elements (no paper counterpart — not paper data, do not "fix" to paper)

- The three color callouts and their color coding (Normalization Layer = blue,
  Feed Forward Layer = gray, Residual Connections = green), the green residual
  arrows' exact routing, the recoloring of the "Add & Norm" and "Feed Forward"
  blocks, and the enlarged insets are instructor pedagogy on the FRAME. The
  paper's Figure 1 is monochrome and carries none of this; the frame is ground
  truth for these stylings.

## [?] Uncertain items

- RESOLVED (raw): title string = "Encoder – Decoder Transformer" (en dash).
- RESOLVED (raw): residual arrows are curved bypass loops beside each
  sub-layer into its 'Add & Norm' — one per sub-layer (encoder Multi-Head
  Attention, encoder Feed Forward, decoder Masked Multi-Head Attention,
  decoder Multi-Head Attention, decoder Feed Forward), with thin curved
  leader lines running from the 'Residual Connections' legend box to them.
- RESOLVED (raw): legend wording verbatim — 'Normalization Layer' (blue),
  'Feed Forward Layer' (gray), 'Residual Connections' (green); recolored set:
  'Add & Norm' ×5 orange, 'Feed Forward' ×2 gray, both 'Multi-Head Attention'
  blocks orange with thick red borders, 'Masked Multi-Head Attention' purple
  with thick red border, 'Linear'/'Softmax' green, embeddings brown.
- STILL OPEN [?]: the V-circle fill under the three attention blocks — the
  raw's own labels contradict themselves (V green [?] vs V blue [?]); K blue /
  Q red are consistent across all three groups.

## Corrections

none — raw transcription matches the paper exactly (Scaled Dot-Product chain
MatMul → Scale → Mask (opt.) → SoftMax → MatMul with V bypass; Linear ×3 →
SDA stack (h) → Concat → Linear; Figure 1 topology with 'Add & Norm' 5×,
'Feed Forward' 2×, capital-H attention labels). Notes for the builder: this
frame renders the repeat glyph as "N x" (spaced) and the small diagram's
letters as uppercase Q/K/V while the center diagram's q is lowercase (the raw
flags this deliberately) — per-frame styling, follow the frame; the V-circle
color question above stays open ([?]) for build-time verification.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout, verbatim
text, drawn content). This source confirms/corrects DATA and records provenance; it
never licenses inventing or "improving" content the slide doesn't show. If source
and slide disagree, record the discrepancy above — the slide wins for recreation,
the source wins for understanding.
