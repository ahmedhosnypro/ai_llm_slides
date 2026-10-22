# SOURCES.md — slide 017 "Encoder – Decoder Transformer"

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via WebFetch of
arXiv HTML v7 (no vision calls run; no image access — frame facts below come from
the verified vision pass description of 2026-10-11).

## Slide identity

- New (curated) slide **017** ← old extraction slide **32**
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_017.jpg`.
- Frame facts (vision pass, ground truth for WHAT is shown): title
  "Encoder – Decoder Transformer"; the paper's **Figure 1** shown in course style
  (paper topology and labels, slide pixels) carrying **4 instructor callouts**:
  (1) the decoder output at step t−1 is fed as the decoder input at step t;
  (2) the first decoder block has no input from encoder attention; (3) an input
  positional encoder; (4) an output positional encoder.

## Primary source

- **URL**: https://arxiv.org/html/1706.03762v7 (verified live 2026-10-11)
- **Paper**: "Attention Is All You Need" — Vaswani, Shazeer, Parmar, Uszkoreit,
  Jones, Gomez, Kaiser, Polosukhin (2017), arXiv:1706.03762v7 [cs.CL]

## Figures used by this slide

**Per-figure use: Figure 1 ONLY** (consistent with the vision verification; this
slide does not draw on Figure 2 left/right).

- **Figure 1** — caption (verbatim, v7): "Figure 1: The Transformer - model
  architecture."
- Founder-downloaded original already banked in `../slide_18_source/The
  Transformer - model architecture..png` — **do not modify that dir's files**;
  this slide references it. No new figures were downloaded into this dir.
- arXiv v7 asset provenance (verified live, byte-identical to the founder's
  download — 159,152 bytes, sha256 `56d69ccc…`):
  https://arxiv.org/html/1706.03762v7/Figures/ModalNet-21.png
  (in-page src `1706.03762v7/Figures/ModalNet-21.png`, id `S3.F1.g1`).

## What the paper CONFIRMS (data behind the slide)

- The figure identity and its topology: the diagram the callouts annotate is the
  paper's Figure 1 (§3.1, "Encoder and Decoder Stacks"). The decoder's first
  sub-layer block is **"Masked Multi-Head Attention"** and it takes only the
  decoder-side inputs — no edge from the encoder output; the encoder output
  feeds the second decoder sub-layer (the encoder-decoder "Multi-Head
  Attention"). So callout (2) matches the figure's own topology.
- The mechanism behind callout (2) is real, not just drawing: §3.2.3.1 — inside
  the decoder's first attention block, masking "ensure[s] that the predictions
  for position i can depend only on the known outputs at positions less than i",
  with the output embeddings "offset by one position".
- Callout (1) ("output at step t−1 fed as input at step t"): Figure 1's decoder
  input arm is labelled "Outputs (shifted right)", and §3.2.3.1 describes the
  decoder attending only to previously-generated positions during decoding.
- Callouts (3)/(4): Figure 1 carries one "Positional Encoding" block on the
  input side and one on the output side; §3.5 defines positional encoding and
  the paper chose the sinusoidal version ("it may allow the model to extrapolate
  to sequence lengths longer than the ones encountered during training").
- Stack counts behind the "Nx" glyphs: "The encoder is composed of a stack of
  N=6 identical layers" and "The decoder is also composed of a stack of N=6
  identical layers" (§3.1).
- Per-sublayer structure behind any Add & Norm reading of the figure: "We employ
  a residual connection [11] around each of the two sub-layers, followed by
  layer normalization [1]. That is, the output of each sub-layer is
  LayerNorm(x + Sublayer(x))" (§3.1).

## Course-authored elements (no paper counterpart — not paper data, do not "fix" to paper)

- The 4 callouts and their exact wording, arrow/box placements and highlights
  over the figure, plus the course color styling, are instructor pedagogy on the
  FRAME. The paper contains none of them; the frame is ground truth for them.

## [?] Uncertain items

- RESOLVED (raw): callout strings pinned verbatim — (1) 'Decoder Output (at
  step “t-1”)' / 'Is supplied as Decoder Input (at step “t”)'; (2) 'First
  Decoder Block' / 'No Input from Encoder Attention'; (3) 'Input Positional
  Encoder' / '(Position of Input Word within the Input Sequence)'; (4) 'Output
  Positional Encoder' / '(Position of Output Word within the Output
  Sequence)' — curly quotes around t-1/t preserved.
- RESOLVED (raw): anchors — (1) the decoder-input rule (yellow highlight
  behind 'Outputs (shifted right)' + the red dashed feedback arrow from
  'Output Probabilities' back down to it); (2) the first decoder block: the
  raw's diagram gives Masked Multi-Head Attention no encoder edge (encoder
  V,K feed only the second Multi-Head Attention), matching §3.2.3.1/§3.2.3;
  (3)/(4) the input-side and output-side 'Positional Encoding' ⊕ nodes.

## Corrections

none — raw transcription consistent with paper labels (capital-H attention
labels; 'Add & Norm' 5× (2 encoder + 3 decoder), 'Feed Forward' 2×,
'Multi-Head Attention' 2×, 'N x' 2×; encoder-output V,K feed only the second
decoder Multi-Head Attention = §3.2.3). Notes for the builder: this frame
renders the repeat glyph as "N x" (spaced) — per-frame course styling vs "Nx"
(14–16) and "N×" (18); and the callouts say "Input/Output Positional Encoder"
while the diagram blocks read "Positional Encoding" — course wording, frame
wins.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout, verbatim
text, drawn content). This source confirms/corrects DATA and records provenance; it
never licenses inventing or "improving" content the slide doesn't show. If source
and slide disagree, record the discrepancy above — the slide wins for recreation,
the source wins for understanding.
