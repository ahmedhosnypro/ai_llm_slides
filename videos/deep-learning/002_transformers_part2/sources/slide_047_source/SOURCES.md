# SOURCES — slide 47 — (untitled full-bleed) "Encoder Block" — framed encoder-layer dataflow

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: `transcripts/slide_047_vision_2026-10-11.txt` (2026-10-11,
default `images` route, thinking=high, streamed — banked by this worker). NOTE:
this frame is the founder-kept FINAL state of the old-115 group (46/47 split;
47 ← 46 in the dependency graph) — the same diagram as slide 46, restyled as the
wrapped ENCODER BLOCK.

## Slide content (from the vision transcript — ground truth)

- Badge 47. White frame with red border; vertical label "Encoder Block" (red) on
  the left; "Block Input" box (bottom-left) and "Block Output" box (top-left);
  tan/orange inner panel. Bottom-to-top: X₀…X₄, …(5 green dots)…, X_{N-2},
  X_{N-1} (segmented 3–4 color token cells) → thick lavender block arrows →
  dark-maroon "Multi Head Self Attention Block" → Y₀…Y_{N-1} row → dashed-green
  Add&Norm group #1 (per-token red ⊕ + orange curved residual arcs + lower
  orange "Layer Normalization" bar) → Y row → per-token orange "FFN" boxes under
  the "Feed Forward Networks [ One Hidden with  RELU Activation]" label (RELU
  pills) → Y row → dashed-green Add&Norm group #2 (⊕ + upper "Layer
  Normalization" bar) → thin red arrows → top Y row → "Block Output".
- RESOLVES slide 46's [?]: the penultimate token subscript is **N−2** (46's
  "N3" glyph is the same N−2 at worse resolution).
- Dependency 47←46←45←28: this is the chain's framing step — the same two
  sub-layers get a named block boundary (Input/Output), prefiguring the
  encoder+decoder composition (slide 57 ← 47).

## 1. Source URLs (fetched live 2026-10-11)

- Vaswani, A. et al. (2017), "Attention Is All You Need", arXiv:1706.03762v7 —
  https://arxiv.org/html/1706.03762v7 — **§3.1** (fetched live 2026-10-11,
  verbatim; same quotes as `../slide_046_source/SOURCES.md` §1): two sub-layers
  (multi-head self-attention; position-wise FFN), "residual connection around
  each of the two sub-layers, followed by layer normalization" — the slide's
  two ⊕/LayerNorm groups. "The encoder is composed of a stack of N=6 identical
  layers" — the semantic anchor for the course's "Encoder Block" wrapper
  (the course draws ONE such block and omits the Nx repetition tag, exactly as
  the transcript notes vs Vaswani Figure 1). Figure 1 bank: 001
  `../001_transformers_part1/slide_18_source/` (do NOT re-download).

## 2. Downloaded figures

- None (course-original per-token redrawing of the encoder layer; no published
  figure matches pixel-wise — instructor style).

## 3. What the sources CONFIRM

- Encoder layer = MHSA sub-layer then FFN sub-layer, each wrapped
  residual+LayerNorm (post-LN): §3.1 — confirmed (drawn twice here).
- "Encoder Block" framing: §3.1 — the encoder stack is N=6 identical layers;
  one block's internals are exactly this diagram. Confirmed.
- Per-token streams with explicit residual loops: §3.1's residual connection
  around each sub-layer — confirmed.
- Token indices 0…N−1 (sequence length N): course indexing; no source conflict.

## 4. Course vs source discrepancies (recreation keeps course verbatim)

- The Nx repetition tag ("×6") is OMITTED (course draws a single block) —
  presentation choice, recorded (transcript notes the same vs Figure 1).
- Mask/softmax/embedding modules from Figure 1 are absent — course focus on the
  layer internals; not a conflict.
- Slide 46 vs 47 styling differences (caption boxes vs Block Input/Output boxes;
  gray vs orange LayerNorm bars; FFN container with neuron-dots vs orange FFN
  boxes with dots+labels) are the SAME diagram at two build states — each frame
  wins for its own recreation.

## 5. Numeric verification

- Indices 0…N−1 with penultimate N−2 (resolves 46's "N3" [?]). No other
  numerals (badge 47). No dimension numbers on the slide.

## 6. Open questions

- none outstanding from the frame (46's subscript question is RESOLVED here as
  N−2; 46's SOURCES.md records the resolution pointer).

## Corrections

none yet — verify against script-12 raw transcription when it lands.

## Cross-check (parallel web-verification worker, 2026-10-11 — reconciliation note by this worker)

The parallel worker's independent map row for 047 agrees with this record
("cleanest full-encoder frame of the 45→46→47 chain — resolves subscripts as
X_{N-2}, X_{N-1} / Y_{N-2}, Y_{N-1}; CONFIRMED two-sub-layer + both Add&Norm
groups"). No unique deltas to mirror.
