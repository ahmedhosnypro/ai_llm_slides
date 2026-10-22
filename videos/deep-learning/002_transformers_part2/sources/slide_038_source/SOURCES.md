# SOURCES.md — slide 038 "Residual Connections and Normalization" (⊕ + LayerNorm added over the MHSA block)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_038_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner) cross-checked against `analysis/slide_038_raw.json` (raw
agrees on the info-panel strings, the "NOT Batch Normalization" bar, and the
row labels; raw's uncertain tail subscripts noted below). Web evidence from
the already-live banked paper fetch (`scratch/webverify/paper_v7.html`,
quoted verbatim below; reference identities [1]/[11] extracted and verified
this session). No new agy query spent — the slide's claims are fully covered
by the live-verified paper.

## Slide identity

- New (curated) slide **038** ← old extraction **106** —
  `unique_slides/new2old_mapping.json`, frame `unique_slides/slide_038.jpg`.
  Second content slide of the 035 "Building Transformer Block" sequence
  (36 → 38: adds the residual + normalization stages to 36's bare MHSA
  block).
- Frame facts (vision transcript): title "Residual Connections and
  Normalization" (red); badge "38". Info panel: "Adding Residual
  Connection:" + the two input lines from slide 036; "Adding "LAYER"
  Normalization" + "Encoded Vectors of Input Sequence   [With Same Input
  Vectors Dimension" (closing bracket missing verbatim). Diagram
  (bottom-to-top): X_1..X_6, …, X_(N-1), X_N → navy bar "Multi Head Self
  Attention Block" → Y'_1..Y'_N; dark-red ⊕ nodes (one per column); orange
  curved residual skip arrows from each X_i column into its ⊕; green arrows
  ⊕ → gray bar "Layer Normalization (in red italic) (NOT Batch
  Normalization) (in black bold)"; red arrows LayerNorm → Y_1..Y_N (top
  row). Left labels: "Output of Self Attention" (blue) / "Residual
  Connections" (orange) / "Input to Self Attention" (red); yellow caption
  "Word_Embedding + Positional_Information" (underscored). Green dashed
  rounded rectangle encloses the LayerNorm stage. Artifacts: cursor at the
  LayerNorm bar's top edge near Y_6; bottom-left black rectangle
  (letterbox).

## Primary sources

1. **arXiv 1706.03762v7 §3.1** (live curl 2026-10-11, banked) — verbatim:
   "We employ a **residual connection** [11] around each of the two
   sub-layers, followed by **layer normalization** [1]. That is, the output
   of each sub-layer is **LayerNorm(x + Sublayer(x))**, where Sublayer(x) is
   the function implemented by the sub-layer itself." — exactly this slide's
   pipeline: Y' = Sublayer(x) (MHSA block output), ⊕ residual add of the
   input x, then Layer Normalization, giving Y. Reference [11] = He et al.,
   "Deep Residual Learning for Image Recognition" (CVPR 2016); reference
   [1] = Ba, Kiros, Hinton, "Layer Normalization" (arXiv:1607.06450) — both
   identities extracted from the banked reference list this session.
2. **"(NOT Batch Normalization)"** — the paper's choice is layer
   normalization [1] (Ba et al. 2016), not batch normalization (Ioffe &
   Szegedy 2015, arXiv:1502.03167). The contrast is the topic of the next
   slides (039–041) and the verified Wu & He 1803.08494 taxonomy record
   (`../slide_041_source/SOURCES.md`); the paper itself only uses LayerNorm
   in §3.1.

## What the sources CONFIRM

- Residual-connection + layer-normalization wrap around the sub-layer, in
  exactly this order (add first, then normalize) — §3.1 verbatim; the
  slide's X→⊕(via MHSA Y')→LayerNorm→Y is the per-token picture of
  LayerNorm(x + Sublayer(x)).
- Output rows same dimension as input ("Encoded Vectors of Input Sequence
  [With Same Input Vectors Dimension") — §3.2.2 W^O ∈ R^{h·d_v×d_model} +
  §3.1 same-shape residual requirement (verified on slide 036's record).
- "Layer Normalization" (NOT Batch) — §3.1 + Ba et al. [1].

## Indexing note (course inconsistency, frame wins)

- THIS slide uses 1-based X_1..X_N / Y'_1..Y'_N / Y_1..Y_N (transcript +
  raw agree), while slide 036 (same info-panel text) reads 0-based
  X_0..X_{N-1}. The deck is internally inconsistent between these adjacent
  slides (also 045's 1-based vs 046's 0-based, recorded in their
  SOURCES.md). Recreation follows EACH frame's own indexing; the raw's
  uncertain tail glyphs ([Y_5?], [Y_N3?]) are superseded by the vision
  read's N-1/N tails on this frame [?] build-time zoom on the top-row
  rightmost box (transcript shows a "Y'_N → Y_N" oddity there).

## Figures used by this slide

- **None.** Course-authored schematic in the Alammar visual idiom (vision:
  custom redrawn variant; no published figure reproduced). No download.

## Course-authored elements

- The "Adding …" info-panel framing, the bracketed pedagogical labels, the
  "(NOT Batch Normalization)" annotation, the underscored bottom caption,
  the colored per-dimension sub-cells, the green dashed stage highlight,
  badge "38" — keep verbatim (including the missing closing bracket) for
  recreation.

## [?] Uncertain items

- [?] top-row rightmost box (Y'_N vs Y_N rendering at frame resolution) —
  build-time zoom.
- [?] prime glyphs on the Y' row could be misread at 960×540 (transcript
  note) — build-time zoom.

## Corrections

- none beyond the indexing note (frame-internal inconsistency, recorded, not
  "fixed").

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. Sources
confirm/correct DATA and record provenance; they never license inventing or
"improving" content the slide doesn't show.
