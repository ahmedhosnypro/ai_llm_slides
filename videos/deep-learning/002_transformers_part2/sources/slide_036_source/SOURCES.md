# SOURCES.md — slide 036 "Multi Head Self Attention Block" (block I/O semantics)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_036_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner) cross-checked against `analysis/slide_036_raw.json` (raw
agrees on the six info-panel strings verbatim; subscript reading difference
recorded below). Web evidence from the already-live banked paper fetch
(`scratch/webverify/paper_v7.html`, quoted verbatim below) + banked Figure 1
in 001's `slide_18_source/`. No new agy query spent — the slide's claims are
fully covered by the live-verified paper.

## Slide identity

- New (curated) slide **036** ← old extraction **103** —
  `unique_slides/new2old_mapping.json`, frame `unique_slides/slide_036.jpg`.
  First content slide of the 035 "Building Transformer Block" sequence.
- Frame facts (vision transcript): title "Multi Head Self Attention Block"
  (red); badge "36". Cream info panel (blue border):
  - "Input:" — "Word Embedding + Positional Information   [First Transformer
    Block]" / "Output of Previous Transformer Block   [Stacked Transformer
    Blocks]"
  - "Output:" — "Encoded Vectors of Input Sequence   [With Same Input
    Vectors Dimension]"
  - "Remember:" — "Different Input Sequences should be of Same Length
    (Fixed Length Sequences)" / "[Apply  Pad or Cut]" / "Output Sequence is
    of same Length as Input Sequence"
  Bottom diagram: X_0..X_5, …, X_{N-2}, X_{N-1} token strips (bottom row,
  yellow-bar caption "Word  Embedding  +  Positional  Information") → blue
  up-arrows → navy bar "Multi Head Self Attention Block" → up-arrows →
  Y_0..Y_5, …, Y_{N-2}, Y_{N-1} (top row); left labels "Input to Self
  Attention" / "Output of Self Attention". One-to-one per-token flow, no
  lateral connections. Artifacts: cursor near the Remember block;
  letterboxing.

## Primary sources

1. **arXiv 1706.03762v7** (live curl 2026-10-11, banked):
   - §3.5 — "we add 'positional encodings' to the input embeddings at the
     bottoms of the encoder and decoder stacks" — the FIRST block's input
     ("Word Embedding + Positional Information").
   - §3.1 / Figure 1 — the encoder is "a stack of N=6 identical layers",
     each layer's first sub-layer = multi-head self-attention (Fig 1 banked
     in 001 `../001_transformers_part1/slide_18_source/`) — "Output of
     Previous Transformer Block" feeding a stacked block.
   - §3.2.2 — "MultiHead(Q, K, V) = Concat(head_1, …, head_h) W^O, where
     head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)", projections
     W_i^Q ∈ R^{d_model×d_k} … and W^O ∈ R^{h·d_v×d_model} — the output is
     back in d_model: the block's output has THE SAME per-token dimension as
     its input ("With Same Input Vectors Dimension"). The residual wrap
     (§3.1 LayerNorm(x + Sublayer(x))) requires this same-shape property.
   - "The Transformer carries the d_model dimension through every layer"
     (h=8, d_k=d_v=d_model/h=64 with reduced per-head dims — "the total
     computational cost is similar to that of single-head attention with
     full dimensionality") — per-token vectors stay d_model-dimensional.
2. Course-authored practice note — "Different Input Sequences should be of
   Same Length (Fixed Length Sequences)" / "[Apply Pad or Cut]" — an
   operational batching statement; the paper does not discuss padding.
   Standard deep-learning practice, no published figure/text reproduced.

## What the sources CONFIRM

- Input semantics (first block = embeddings + PE; stacked blocks = previous
  block's output) — paper §3.5 + Fig 1 stack topology.
- Output semantics ("Encoded Vectors of Input Sequence, same dimension as
  input") — §3.2.2 W^O ∈ R^{h·d_v×d_model} + §3.1 same-shape residual+norm
  requirement.
- Length preservation (output sequence same length as input) — self-
  attention produces one output per input position (per-position attended
  vectors; §3.2.1 equation (1) applied to each position), the property the
  slide's one-to-one X_i→Y_i arrows draw.
- The 0-based indexing X_0..X_{N-1} on this slide — consistent with 034's
  0-based position row and 046's verified zero-based record (course uses
  0-based indexing in the block-building sequence; 045's 1-based X_1..X_N is
  the recorded inconsistency).

## Subscript reading note (raw vs vision)

- The script-12 raw read "Y_1..Y_6, Y_{N/2} [?], Y_{N+1} [?]" (1-based, its
  own tails flagged uncertain). The gated vision transcript (thinking high)
  read "Y_0..Y_5, …, Y_{N-2}, Y_{N-1}" / same for X, explicitly "glyphs
  legible, no [?] needed", and matches the deck-wide 0-based convention +
  034's 0..N-1 position row. **Read of record: 0-based, tails N-2/N-1**;
  build-time zoom may re-confirm (residual [?] on the tail glyphs only).

## Figures used by this slide

- **None.** Course-authored schematic (vision: no direct copy of any
  published figure; "same visual idiom" as Alammar-style token rows only).
  Banked Fig 1 referenced for the stack topology, not embedded.

## [?] Uncertain items

- [?] tail subscripts N-2/N-1 (vision) vs the raw's [?]-flagged N/2, N+1 —
  resolved toward vision's read per the note above; final check at build
  zoom.

## Corrections

- Subscript indexing corrected from the raw's 1-based reading to the
  vision's 0-based reading (recorded above).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. Sources
confirm/correct DATA and record provenance; they never license inventing or
"improving" content the slide doesn't show.
