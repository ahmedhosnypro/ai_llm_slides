# SOURCES — slide 41 — "Normalization" (taxonomy tree)

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: `transcripts/slide_041_vision_2026-10-11.txt` (2026-10-11,
default `images` route, thinking=high, streamed — banked by this worker).

## Slide content (from the vision transcript — ground truth)

- Title "Normalization" (badge 41). A two-way taxonomy tree:
  "Normalization of" → **"Activations Outputs"** → {Batch Normalization, Instance
  Normalization, Group Normalization, Layer Normalization} and → **"Weights"** →
  {Weight Normalization}. Course-made drawing (red arrows, blue/green/mint boxes);
  no published figure is reproduced.
- Frame shows the top box reading only "Normalization of" (second line "of") — the
  completed statement (e.g. "Normalization of X…") is not visible at this frame;
  possible mid-build state or slide-internal cut. Recreation keeps the frame
  verbatim. [?] nothing further was ever drawn (no second frame shows more).

## 1. Source URLs (all fetched live 2026-10-11)

- Wu, Y. & He, K. (2018), "Group Normalization", ECCV 2018 —
  https://arxiv.org/abs/1803.08494 (ar5iv render:
  https://ar5iv.labs.arxiv.org/html/1803.08494). Its §2 "Related Work" /
  Figure 2 presents EXACTLY this grouping: BN, IN, GN, LN are the
  **normalization-method family that normalizes activations over chosen axes of the
  feature tensor**, contrasted with weight-space methods.
- Salimans, T. & Kingma, D.P. (2016), "Weight Normalization: A Simple
  Reparameterization to Accelerate Training of Deep Neural Networks", NIPS 2016 —
  https://arxiv.org/abs/1602.07868 (verified live 2026-10-11). The paper behind the
  slide's "Weights" branch.
- Ba, J.L., Kiros, J.R., Hinton, G.E. (2016), "Layer Normalization" —
  https://arxiv.org/abs/1607.06450 (verified live 2026-10-11). LayerNorm is the
  member of this taxonomy that the Transformer uses (arXiv 1706.03762 §3.1
  Add & Normalize) — this slide motivates the transformer's choice.
- agy (2026-10-11): confirmed Wu & He Figure 2 as the canonical grouping of the
  four activation-normalization methods with weight normalization treated
  separately.

## 2. Downloaded figures

- None for THIS slide (course-made text taxonomy; no figure to reuse).
- The taxonomy FIGURE of the family (Wu & He Figure 2, `all_norms.svg`) is
  downloaded once into `../slide_042_source/all_norms.svg` — see that dir's
  SOURCES.md — because slides 42–44 (pattern group P3) draw the corresponding
  feature-map-tensor diagrams.

## 3. What the sources CONFIRM

- The slide's partition (normalize ACTIVATIONS/OUTPUTS: Batch / Instance / Group /
  Layer; normalize WEIGHTS: Weight Normalization) matches the standard taxonomy —
  Wu & He §2 organize exactly these four as activation-normalization methods
  (each selecting different axes of the (N, C, H, W) tensor), and place Weight
  Normalization (Salimans & Kingma) as the separate weight-space alternative.
- The four activation members and their definitions:
  BatchNorm (Ioffe & Szegedy 2015, arXiv:1502.03167) — over (N,H,W) per channel;
  InstanceNorm (Ulyanov 2016, arXiv:1607.08022) — per sample per channel;
  LayerNorm (Ba et al. 2016) — over (C,H,W) per sample; GroupNorm (this paper) —
  per sample over channel groups. (Definitions per Wu & He §2/Fig 2.)

## 4. Course vs source discrepancies

- None material. The slide is a course-authored summary; it adds no numbers.
- Note: the top box's truncated "Normalization of" reading is a frame/build-state
  artifact, not a source discrepancy.

## 5. Numeric verification

- n/a (0/0) — no numbers on the slide.

## 6. Open questions

- [?] Whether the "of" second line in the top box was ever completed in the video
  (the founder's curated frame shows it as-is; recreation follows the frame).
- [?] Whether the lecturer also cited Ioffe & Szegedy (BN) / Ulyanov (IN)
  explicitly — not visible on the slide; the taxonomy slide itself needs no
  further confirmation (CONFIRMED taxonomy provenance above).

## Corrections

none yet — verify against script-12 raw transcription when it lands.

## Cross-check (second web-verification worker, 2026-10-11 — appended, nothing above edited)

- Independent re-fetches agree with this record: Wu & He ar5iv render (BN/LN/IN/GN
  = the feature-normalization family; WN "normalizes filter weights rather than
  features"), Salimans & Kingma abs 1602.07868 (WN decouples weight-vector length
  from direction), Huang et al. survey abs 2009.12836 (taxonomy statement verified;
  the activation-vs-weight split is NOT in its abstract — the [?] above stands).
- Script-12 raw `analysis/slide_041_raw.json` EXISTS and agrees verbatim on every
  label (Batch/Instance/Group/Layer/Weight Normalization; "Normalization of"
  two-line root box) — the "Corrections: none yet" note above is now satisfied.
- Vision transcript of record confirmed banked at
  `transcripts/slide_041_vision_2026-10-11.txt` (also independently re-banked by
  the second worker — identical slide, same route).

## Raw-landing verification (slide 41, 2026-10-11 — raw pass; nothing above edited)

- `analysis/slide_041_raw.json` (script-12; kept frame frame_03305.jpg, t≈3258–3304 s, old
  extraction 110) read in full by this worker: every string agrees with this record — root
  box prints exactly "Normalization" / "of" (two lines), parents "Activations Outputs" (dark
  blue) / "Weights" (green), leaves Batch / Instance / Group / Layer Normalization (light
  cyan) + Weight Normalization (light green), red connectors, badge 41. Full-build state
  confirmed (all 8 boxes + all arrows visible; the earlier "mid-build?" worry is settled —
  the frame is the completed state as curated).
- One addition for the build worker: the raw logs a black mouse cursor overlapping the word
  "Batch" (recording artifact) — omit from recreation (same rule as other capture artifacts).
- No corrections; both [?] items above stand (frame-limited). Sources unchanged (Wu & He /
  Salimans & Kingma / Ba et al. — all previously live-verified).
