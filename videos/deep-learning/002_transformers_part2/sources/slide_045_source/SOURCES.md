# SOURCES — slide 45 — "Feed Forward Neural Network"

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: `transcripts/slide_045_vision_2026-10-11.txt` (2026-10-11,
default `images` route, thinking=high, streamed — banked by this worker).

## Slide content (from the vision transcript — ground truth)

- Title "Feed Forward Neural Network" (badge 45). Bottom-to-top per-token
  dataflow: X₁…X_N ("Word Embedding + Positional Information") → dark-navy
  "Multi Head Self Attention Block" → Y₁…Y_N ("Output of Self Attention") →
  residual "+" nodes (orange curved arrows from the X row — "Residual
  Connections", "Input to Self Attention") inside a dashed-green Add & Norm
  panel → gray "Layer Normalization" bar → Y₁…Y_N → white container "Feed
  Forward Networks [ One Hidden with RELU Activation]" containing one small
  per-token sub-network (green dots → pink connections → output dots, RELU pill)
  per position → top Y₁…Y_N row.
- Banner (yellow): "Feed Forward Network for each Vector (After applying
  Normalization)"; "One Hidden Layer with RELU Activation, [Size: at least double
  Input dimension]"; "Linear Activation Output Layer [Size: same Input Vector
  dimension]".
- Dependency 45←28 (001 family): the attention block is the course's own
  self-attention composition from Part I slides 26–30 (X_i tokens in, Y_i out).

## 1. Source URLs (fetched live 2026-10-11)

- Vaswani, A. et al. (2017), "Attention Is All You Need", arXiv:1706.03762v7 —
  https://arxiv.org/html/1706.03762v7 —
  **§3.3 "Position-wise Feed-Forward Networks"** (fetched live 2026-10-11,
  verbatim): "each of the layers in our encoder and decoder contains a fully
  connected feed-forward network, which is **applied to each position separately
  and identically**. This consists of **two linear transformations with a ReLU
  activation in between**. FFN(x)=max(0, xW₁+b₁)W₂+b₂ … The dimensionality of
  input and output is d_model=512, and the inner-layer has dimensionality
  d_ff=2048."
  **§3.1** (same fetch): "the output of each sub-layer is LayerNorm(x +
  Sublayer(x))" — the residual + LayerNorm band the slide draws between attention
  and FFN. Figures banked in 001's `../001_transformers_part1/slide_18_source/`
  (Figure 1 shows Add & Norm after each sub-layer; do NOT re-download).
- Jay Alammar, "The Illustrated Transformer" —
  https://jalammar.github.io/illustrated-transformer/ (live 2026-10-11, verified
  in 001's research): the closest published depiction of the per-token/residual
  style; the course's drawing is its own (see transcript's resemblance note).

## 2. Downloaded figures

- None (course-original composition; the paper's Figure 1 bank already exists in
  001 `slide_18_source/` and the slide does not reproduce it).

## 3. What the sources CONFIRM

- Per-token FFN ("for each Vector"): §3.3 "applied to each position separately
  and identically" — confirmed.
- Two linear layers with ReLU between; second (output) layer linear and same
  dimension as input: §3.3 confirmed (W₁: d_model→d_ff with ReLU; W₂: d_ff→d_model).
- FFN input = normalized attention output ("After applying Normalization"): §3.1
  LayerNorm(x + Sublayer(x)) ordering (post-norm, original paper) — confirmed by
  Figure 1's topology (Add & Norm between sub-layers).
- Residual connections around the attention sub-layer: §3.1 confirmed ("residual
  connection [11] around each of the two sub-layers, followed by layer
  normalization").
- Layer Normalization as the norm used: §3.1 (ref [1] = Ba et al. 2016) and this
  lecture's slides 41/44 ("Transformer choice").

## 4. Course vs source discrepancies (recreation keeps course verbatim)

- Hidden-layer size: course "[Size: at least double Input dimension]" vs paper
  d_ff = 2048 = 4×d_model. The course's rule of thumb is a weaker lower bound —
  NOT a contradiction, but the paper's concrete ratio is 4×. Recreation keeps the
  course text verbatim; understanding-side note recorded here.
- The slide labels ALL rows Y_i (attention output, post-Add&Norm, post-FFN);
  the paper distinguishes Sublayer(x), LayerNorm output, FFN output. Course
  notation kept.
- "Multi Head Self Attention Block" is the course's block naming (Part I
  family); paper: "Multi-Head Attention".

## 5. Numeric verification

- d_ff=2048, d_model=512 (paper) vs course "at least double"/"same dimension" —
  recorded above. No other numerals on the slide (badge 45; token indices 1..N).

## 6. Open questions

- [?] Which rows exactly carry "Y_6" vs ellipsis tokens mid-row (small text at
  960px; transcript marked Y_5/Y_6 and X_5 best-effort). The founder frame-swap
  note does not apply here (46/47 are the swapped pair, not 45).
- [?] Whether the lecturer cited d_ff=2048 verbally (frame shows no number).

## Corrections

none yet — verify against script-12 raw transcription when it lands.

## Cross-check (second web-verification worker, 2026-10-11 — appended, nothing above edited)

- Independent Vaswani fetch agrees verbatim on both quotes: §3.3 "two linear
  transformations with a ReLU activation in between", "FFN(x) = max(0, xW1 + b1)W2
  + b2", d_model=512 / d_ff=2048; §3.1 "the output of each sub-layer is
  LayerNorm(x + Sublayer(x))".
- No script-12 raw exists for 045; the two independent vision transcripts agree on
  the banner text (including "at least double Input dimension" and "same Input
  Vector dimension"), the Add&Norm dashed grouping, and the
  "Word_Embedding + Positional_Information" caption with literal underscores.
