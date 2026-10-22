# SOURCES — slide 46 — (untitled full-bleed) Transformer ENCODER LAYER, complete per-token dataflow

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: `transcripts/slide_046_vision_2026-10-11.txt` (2026-10-11,
default `images` route, thinking=high, streamed — banked by this worker). NOTE:
this frame is the founder-kept MID-GROUP state of the old-115 group split
(46/47; founder kept frame_03828.jpg) — slide 47 is the same group's next state
(see its own SOURCES.md).

## Slide content (from the vision transcript — ground truth)

- No title text; full-bleed diagram inside red+blue borders; badge numeral cut
  off/unreadable at this frame [?] (badge = 46 per file id and curation).
- Bottom-to-top per-token dataflow, N=8 drawn columns, tokens X_0…X_5, …,
  X_N-1 (zero-based indexing) whose boxes are split yellow|pink sub-cells,
  caption "Word Embedding + Positional Information":
  → dark-navy "Multi Head Self Attention Block"
  → ⊕ residual add (orange curved bypass arcs from the X row; "Residual
     Connections")
  → Y row "Output of Self Attention"
  → gray "Layer Normalization" bar (green dashed Add&Norm group)
  → Y row (FFN input) → white "Feed Forward Networks [ One Hidden with
     RELU Activation]" container with 8 per-token sub-networks (RELU pills)
  → ⊕ residual add #2 (arcs from the FFN-input Y row)
  → Y row → second "Layer Normalization" bar (green dashed group)
  → final Y row (last two boxes highlighted yellow) + "Final Output" label box.
- Dependency 46←45 (45←28): extends slide 45's composition with the second
  Add & Norm group and the Final Output row; same family, same paper anchors.

## 1. Source URLs (fetched live 2026-10-11)

- Vaswani, A. et al. (2017), "Attention Is All You Need", arXiv:1706.03762v7 —
  https://arxiv.org/html/1706.03762v7 — **§3.1** (fetched live 2026-10-11,
  verbatim): "Each layer has two sub-layers. The first is a multi-head
  self-attention mechanism, and the second is a simple, position-wise fully
  connected feed-forward network. We employ a **residual connection [11] around
  each of the two sub-layers, followed by layer normalization [1]**. That is,
  the output of each sub-layer is LayerNorm(x + Sublayer(x))…"
  — the slide's TWO ⊕ + LayerNorm groups = exactly these two sub-layer wraps.
  **§3.5** (same fetch): "we add 'positional encodings' to the input embeddings
  at the bottoms of the encoder and decoder stacks… same dimension d_model as
  the embeddings, so that the two can be summed" — the slide's split
  yellow|pink token cells ("Word Embedding + Positional Information").
  Figure 1 bank: 001 `../001_transformers_part1/slide_18_source/` (do NOT
  re-download).

## 2. Downloaded figures

- None (course-original composition; no published figure reproduces this exact
  per-token column layout).

## 3. What the sources CONFIRM

- Two sub-layers per encoder layer, each wrapped residual+LayerNorm (post-LN):
  §3.1 — confirmed (the slide draws both groups).
- Per-token FFN inside the layer: §3.3 (see `../slide_045_source/SOURCES.md`) —
  confirmed.
- Residuals at both levels: §3.1 — confirmed.
- Input = word embeddings + positional encodings summed at the stack bottom:
  §3.5 — confirmed.
- Topology matches the canonical post-LN encoder layer: input → MHSA →
  Add → LayerNorm → FFN → Add → LayerNorm → output (transcript's own
  resemblance analysis concurs; NOT Vaswani Fig 1 pixel-wise — no encoder/
  decoder split, no Nx tag).

## 4. Course vs source discrepancies (recreation keeps course verbatim)

- Indexing: slide 46 numbers tokens X_0…X_N-1 (zero-based) while sibling
  slide 45 uses X_1…X_N (one-based). Course inconsistency between slides;
  each frame wins for its own recreation.
- The "Output of Self Attention" Y row is drawn BETWEEN the ⊕ node and the
  LayerNorm bar; §3.1's LayerNorm(x + Sublayer(x)) makes the same value the
  LayerNorm input. Same operation; drawing order is the course's. Slide 45 drew
  the Y row before the ⊕ — mid-group/build-state difference between the two
  slides, kept per frame.
- "N3" penultimate subscript is a low-legibility glyph [?] — likely N−2/N−3;
  47's frame (same group) may disambiguate; resolve there.
- "Final Output" label box and yellow-highlighted last columns are course
  emphasis; nothing in the source conflicts.

## 5. Numeric verification

- No numerals on the slide (badge unreadable here). n/a beyond indices.

## 6. Open questions

- [?] The penultimate token subscript ("N3") on every row — RESOLVED 2026-10-11
  by slide 47's frame (same old group, cleaner glyphs): it reads **N−2**. See
  `../slide_047_source/SOURCES.md`.
- [?] Badge numeral not visible at this frame; curation says slide 46.

## Corrections

none yet — verify against script-12 raw transcription when it lands.

## Cross-check (parallel web-verification worker, 2026-10-11 — reconciliation note by this worker)

A parallel worker processed this range concurrently. Its per-slide record for
046 survives in the SOURCES_MAP rows; unique findings mirrored here:

- Script-12 raw `analysis/slide_046_raw.json` EXISTS and agrees with the frame
  reading (per the parallel worker's map row).
- Rightmost token subscripts flagged [?] by the parallel worker as "plausibly
  N-2/N-1, cf. 047" — RESOLVED in this record (N−2, via slide 47's frame).

## Raw-landing verification (slide 46, 2026-10-11 — raw pass; nothing above edited)

- `analysis/slide_046_raw.json` (script-12; kept frame frame_03828.jpg — the founder-kept
  mid-group state of the 46/47 split, t≈3827–3899 s, old extraction 115) now EXISTS and was
  read in full. It CONFIRMS the composition verbatim: no title, no badge numeral visible
  (raw: "No slide number, no watermark, no course logo, no date visible"), dark-blue outer
  frame, pink "Final Output" callout, four token rows of 8 segmented boxes (X row with 4
  green ellipsis dots; the three Y rows with 5 blue dots each), dark-blue "Multi Head Self
  Attention Block" bar, two "Layer Normalization" units (gray bar — 'Layer' red bold italic
  + 'Normalization' black bold — each with 8 dark-red ⊕ circles inside a light-green dashed
  rounded container), "Feed Forward Networks [ One Hidden with  RELU Activation]" (double
  space confirmed) with 8 per-token mini FFN icons each carrying a tiny red "RELU" tag,
  orange curved residual connectors, left annotations ("Input  to Self Attention" red /
  "Residual Connections" orange ×2 / "Output of Self Attention" blue), and the bottom
  caption "Word Embedding  +  Positional Information" clipped by the letterbox strip.
  Per-token icons carry ONLY the RELU tag at this build state (no "MLP" caption here —
  contrast with slide 48, where the raw resolves that caption as "MLP").
- Subscripts: the raw reads the two rightmost tokens as "X_N3 [?], X_N4 [?]" (raw's own
  hypothesis: "possibly N−3/N−4") — i.e. the same low-legibility glyphs behind the original
  "N3" flag. The record's resolution via slide 47's clean frame (penultimate N−2, final
  N−1 — same diagram family, cleaner glyphs) remains PRIMARY; a build-time PIL zoom of
  `unique_slides/slide_046.jpg`'s rightmost tokens is the decisive check [?] (escalate to a
  founder frame check if the zoom is ambiguous).
- The earlier transcript's "last two boxes highlighted yellow" (final row) is NOT
  corroborated by the raw — it reads all 32 token boxes as the same 4-segment pastel style
  (pink/yellow/pale-green/lavender). Treat the yellow-highlight claim as unverified [?];
  the frame is ground truth at build time.
- No source changes (Vaswani §3.1 two-sub-layer/residual-LayerNorm and §3.5
  embedding+positional anchors unaffected; banked Fig 1 stays in 001's slide_18_source/).
