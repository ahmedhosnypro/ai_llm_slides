# SOURCES.md — slide 015 (Figure 1, plain + recolored with data-flow arrows)

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via WebFetch of
arXiv HTML v7 (no vision calls run; no image access — frame facts below come from
the verified vision pass description of 2026-10-11).

## Slide identity

- New (curated) slide **015** ← old extraction slide **29**
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_015.jpg`.
- **Dependency edge: 15 ← 14** (`slide_dependencies.json`) — build gated on slide
  14's certification. This slide re-uses slide 14's Figure 1 in two renderings.
- Frame facts (vision pass, ground truth): **Figure 1 of the paper shown twice** —
  once plain, once recolored in the course's style (encoder orange / decoder
  green) with red data-flow arrows overlaid.

## Primary source

- **URL**: https://arxiv.org/html/1706.03762v7 (verified live 2026-10-11)
- **Paper**: "Attention Is All You Need" — Vaswani, Shazeer, Parmar, Uszkoreit,
  Jones, Gomez, Kaiser, Polosukhin (2017), arXiv:1706.03762v7 [cs.CL]

## Figures used by this slide

**Per-figure use: Figure 1 ONLY** (consistent with the vision verification; this
slide does not draw on Figure 2 left/right).

- **Figure 1** — caption (verbatim, v7): "Figure 1: The Transformer - model
  architecture."
- Founder-downloaded original already banked in
  `../slide_18_source/The Transformer - model architecture..png` (1520×2239) —
  **slides 14 and 15 MUST use the downloaded images (founder explicit)** — **do
  not modify that dir's files**. No new figures were downloaded into this dir.
- arXiv v7 asset provenance (verified live, byte-identical to the founder's
  download — 159,152 bytes):
  https://arxiv.org/html/1706.03762v7/Figures/ModalNet-21.png
  (in-page src `1706.03762v7/Figures/ModalNet-21.png`, id `S3.F1.g1`).

## What the paper CONFIRMS (data behind the slide)

- Topology of both copies = the paper's Figure 1 exactly: encoder stack (N×)
  over Positional Encoding / Inputs; decoder stack (N×) with Masked Multi-Head
  Attention + Multi-Head Attention + Feed Forward sub-layers, each Add & Norm;
  Linear → Softmax → Output Probabilities; "Outputs (shifted right)".
- The recolored copy's orange/green split corresponds to real paper structure:
  encoder stack vs decoder stack ("The encoder is composed of a stack of N=6
  identical layers" / "The decoder is also composed of a stack of N=6 identical
  layers").
- The red data-flow arrows trace the paper's own data path: Inputs → embeddings
  (+ positional encodings) → encoder stack; encoder output → decoder's
  encoder-decoder attention ("the memory keys and values come from the output of
  the encoder"); decoder → Linear → Softmax → output probabilities.

## Course-authored elements (no paper counterpart — not paper data, do not "fix" to paper)

- The orange/green color assignment, the red arrow styling, and the choice to
  show the figure twice (plain + recolored) are course presentation choices. The
  paper's Figure 1 has its own fixed coloring; the frame's recoloring is ground
  truth for the recreation.

## [?] Uncertain items

- RESOLVED (raw): the recolored copy carries exactly TWO small solid red
  up-arrows — one beside 'Inputs' (bottom-left of the encoder region), one
  beside 'Output Probabilities' (top of the decoder region). The large red
  right-pointing block arrow between the panels (~46–55% width, ~52–62%
  height) is a transition arrow (plain copy → annotated copy), not a
  data-flow arrow. No full-path arrow tracing exists on the frame per the raw.

## Corrections

none — raw transcription consistent with paper labels (capital-H "Multi-Head
Attention"/"Masked Multi-Head Attention"; full label set; per panel 5×
Add & Norm, 2× Feed Forward, 2× Multi-Head Attention, 1× Masked = paper
topology; Nx placement left-of-encoder / right-of-decoder as in Figure 1).
Note: the earlier vision-pass phrasing "red data-flow arrows tracing the full
data path" is superseded by the raw's two small red up-arrows (see [?] above).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout, verbatim
text, drawn content). This source confirms/corrects DATA and records provenance; it
never licenses inventing or "improving" content the slide doesn't show. If source
and slide disagree, record the discrepancy above — the slide wins for recreation,
the source wins for understanding.
