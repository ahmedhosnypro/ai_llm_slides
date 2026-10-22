# SOURCES.md — slide 018 "Multi-Head Attention (paper figures)" — working title, see [?]

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via WebFetch of
arXiv HTML v7 (no vision calls run; no image access — frame facts below come from
the verified vision pass description of 2026-10-11).

## Slide identity

- New (curated) slide **018** ← old extraction slide **42**
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_018.jpg`.
- Frame facts (vision pass, ground truth for WHAT is shown): **all three paper
  figures on one slide** — Figure 1 (full architecture) on the right; Figure 2
  left (Scaled Dot-Product Attention) and Figure 2 right (Multi-Head Attention)
  as **enlarged insets** on the left; **red dashed connectors** from the insets
  to **red-outlined Multi-Head Attention blocks** inside the architecture; two
  banners: "Both Encoder and Decoder Blocks Contain 'Multi-Head Self Attention'
  block" and "'h' Heads / Outputs of Heads are concatenated".

> **Relationship to the historical dir `../slide_18_source/`:** that dir is the
> FOUNDER'S FIGURE BANK for this whole figure family — the founder-downloaded
> paper originals (Figure 1 + Figure 2 left + Figure 2 right) live there with its
> own SOURCES.md provenance record. **This slide 018 = old extraction 42**; the
> dir's name "slide_18_source" predates the 2026-10-11 curation (it dates from
> the pre-curation numbering, when "slide 18" was a different, now-culled frame
> of the same topic). Do not modify the bank; this slide references it.

## Primary source

- **URL**: https://arxiv.org/html/1706.03762v7 (verified live 2026-10-11)
- **Paper**: "Attention Is All You Need" — Vaswani, Shazeer, Parmar, Uszkoreit,
  Jones, Gomez, Kaiser, Polosukhin (2017), arXiv:1706.03762v7 [cs.CL]

## Figures used by this slide

**Per-figure use: Figure 1 + Figure 2 left + Figure 2 right** (consistent with
the vision verification — this is the only slide in the 14–19 family showing all
three together; slide 019 repeats the same three).

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

- The Scaled Dot-Product Attention inset is Figure 2 left, and its math is
  §3.2.1 equation (1), verbatim:
  **Attention(Q, K, V) = softmax(QKᵀ/√d_k) V** — computed as "the dot products
  of the query with all keys, divide each by √d_k, and apply a softmax function
  to obtain the weights on the values" (MatMul → Scale → Mask (opt.) → SoftMax →
  MatMul in the figure).
- The Multi-Head Attention inset is Figure 2 right, and its math is §3.2.2,
  verbatim: **MultiHead(Q, K, V) = Concat(head₁, …, head_h) Wᴼ** with
  **head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)** (h parallel Linear → Scaled
  Dot-Product Attention branches → Concat → Linear).
- The banner "'h' Heads / Outputs of Heads are concatenated": §3.2.2 — "we
  employ **h = 8** parallel attention layers, or heads. For each of these we use
  **d_k = d_v = d_model/h = 64**", and the outputs "are concatenated and once
  again projected, resulting in the final values, as depicted in Figure 2".
- The banner "Both Encoder and Decoder Blocks Contain 'Multi-Head Self
  Attention' block": §3.1 — each encoder layer's first sub-layer is a
  "multi-head self-attention mechanism"; each decoder layer's first sub-layer is
  (masked) multi-head self-attention over its own inputs (§3.2.3.1); the red-
  outlined blocks in the Figure-1 stacks are where these live.
- Figure-1 stack counts behind the "Nx" glyphs: N=6 identical layers on both
  sides (§3.1); per-sublayer residual + layer norm = "LayerNorm(x +
  Sublayer(x))" (§3.1).

## Course-authored elements (no paper counterpart — not paper data, do not "fix" to paper)

- The **enlarged insets** (both Figure 2 panels blown up as left-side callouts),
  the **red dashed connectors**, the **red outlines** on the Multi-Head Attention
  blocks, and BOTH banners' wording are instructor pedagogy on the FRAME. The
  paper contains none of them; the frame is ground truth for them.

## [?] Uncertain items

- RESOLVED (raw): title string = "Encoder – Decoder Transformer" (en dash).
- RESOLVED (raw): the two red dashed curved arrows are NOT inset→block
  connectors — (1) from the encoder stack's top curving right/down into the
  decoder's middle Multi-Head Attention (arrowhead at its V/K circles); (2)
  along the right edge from 'Outputs (shifted right)' up to 'Output
  Probabilities' (autoregressive feedback). The insets relate to the
  architecture through the red-outlined, yellow-highlighted Multi-Head
  Attention blocks; the earlier vision-pass phrase "connectors from the
  insets to the outlined blocks" is superseded by the raw.
- RESOLVED (raw): banner strings verbatim — "Both Encoder and Decoder Blocks
  Contain" / "\"Multi-Head Self Attention\" block" and "\"h\" Heads" /
  "Outputs of Heads are concatenated" (4-line callout, first line black,
  remaining lines red).

## Corrections

none — raw transcription matches the paper exactly: Scaled Dot-Product chain
MatMul → Scale → Mask (opt.) → SoftMax → MatMul with the V bypass into the top
MatMul (Figure 2 left); Linear ×3 → stacked Scaled Dot-Product Attention (h)
→ Concat → Linear (Figure 2 right); full Figure 1 topology with capital-H
attention labels and 'SoftMax' (insets) vs 'Softmax' (decoder box) kept
distinct as the figures show. Notes for the builder: this frame renders the
repeat glyph as "N×" (times sign) — per-frame styling vs "Nx"/"N x"
elsewhere; the inset circle letters are lowercase q/k/v per the raw (slide
019's raw reads its small diagram's letters uppercase Q/K/V — cross-slide
difference; follow each frame).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout, verbatim
text, drawn content). This source confirms/corrects DATA and records provenance; it
never licenses inventing or "improving" content the slide doesn't show. If source
and slide disagree, record the discrepancy above — the slide wins for recreation,
the source wins for understanding.
