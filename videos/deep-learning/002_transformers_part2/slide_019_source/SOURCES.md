# SOURCES.md — slide 019 "Encoder – Decoder Transformer" (Fig 2L + Fig 2R + full architecture, "WE ARE HERE")

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Vision transcript of record: `transcripts/slide_019_webverify.txt` (2026-10-11,
default `images` route, `--thinking high`, via `scripts/16_vision_gate.sh`).

## CROSS-VIDEO RECAP (founding rule for this slide)

`slide_dependencies.json`: **19 ← deep-learning/001_transformers_part1:19**.
Parent record: `../001_transformers_part1/slide_019_source/SOURCES.md`
(verified 2026-10-11): the paper's Figure 1 + Figure 2 left + Figure 2 right
trio, paper §3.1 residual/LayerNorm and §3.3 FFN quotes, figure-bank
provenance (sha-verified against live arXiv assets). Per the recap rule that
verification CARRIES; the figure family bank is
`../001_transformers_part1/slide_18_source/` (do not modify). This frame's
NEW composition (no callout banners here; zoom-callout connectors; "WE ARE
HERE" pin; Alammar-styled right panel) is assessed below.

## Slide identity

- Frame `unique_slides/slide_019.jpg`, badge "19" (timeline: t≈746–762 s, old
  extraction 37).
- Frame facts (vision transcript, ground truth): title "Encoder – Decoder
  Transformer" (red, centered; en dash). THREE green-outlined panels:
  - LEFT "Scaled Dot-Product Attention": bottom-to-top Q/K/V circles →
    MatMul → (Mask (opt.) →) Scale → SoftMax → MatMul (V side-input) —
    paper Fig 2 left topology, course recolor (blue MatMul, pink Mask,
    yellow Scale, green SoftMax).
  - MIDDLE "Multi-Head Attention": V/K/Q circles → three Linear → large
    stacked "Scaled Dot-Product Attention" box with "h" annotation →
    Concat → Linear — paper Fig 2 right topology, course recolor.
  - RIGHT full encoder–decoder: Encoder column + Decoder column with
    Inputs → Input/Output Embedding → Positional Encoding → attention/
    FFN sub-layers with Add & Norm → Linear → Softmax → Output
    "Probabilities"; V/K circles under attention boxes; red dotted zoom-
    callout lines from the left/middle panels into the encoder's
    Multi-Head Attention box; dashed red cross-connection arrows
    (encoder→decoder attention; skip-style arcs); "N×" gray circle;
    bottom labels "Inputs" / "Outputs" + "(shifted right)".
  - Presenter overlay: large red map-pin "WE ARE HERE" (white on red) at
    the encoder's lower Add & Norm / Multi-Head Attention area; two yellow
    translucent highlighter blobs (encoder lower area; decoder Output
    Embedding / Positional Encoding area). Lecture artifacts, not figure
    content — do not recreate.

## Primary sources (verified live 2026-10-11)

- **arXiv 1706.03762v7 "Attention Is All You Need"** —
  https://arxiv.org/html/1706.03762v7 (live WebFetch this session):
  §3.1 "The encoder is composed of a stack of N=6 identical layers."
  (decoder stack N=6 verified live by the slide-057 worker, recorded in
  SOURCES_MAP); §3.2.1 Attention(Q,K,V) = softmax(QKᵀ/√d_k)V (parent
  record); §3.2.2 MultiHead = Concat·W^O, h=8 (live-confirmed this session,
  slide-016 record). **Paper Figure 1** (banked:
  `../001_transformers_part1/slide_18_source/The Transformer - model
  architecture..png` = live ModalNet-21.png, sha-verified) is the data
  source of the right panel; **Figure 2 left/right** (banked ModalNet-19/20)
  are the data sources of the left/middle panels.
- **Jay Alammar, "The Illustrated Transformer"** —
  https://jalammar.github.io/illustrated-transformer/ (page + full image
  inventory fetched live this session): the vision transcript identifies the
  right panel as the Alammar-styled annotated architecture (orange encoder /
  green decoder tinting, Q/K/V circles, dashed red arcs, "Probabilities"
  caption). The matching Alammar asset,
  `The_transformer_encoder_decoder_stack.png` (1218×793), is ALREADY BANKED
  in this video's `slide_057_source/` (sha-recorded there) — reference it;
  no re-download. Label-level match confirmed; pixel-level identity [?]
  (vision budget spent — zoom t≈746–762 s before building).

## Figures used by this slide

- Left panel = course redraw of **paper Figure 2 (left)** — banked original
  `../001_transformers_part1/slide_18_source/slide18 scaled dot-production
  attention figure.png`. Topology/labels confirmed; pixel style the slide's.
- Middle panel = course redraw of **paper Figure 2 (right)** — banked
  `../001_transformers_part1/slide_18_source/slide18 Multi-Head
  Attention\n\n.png` (filename contains literal newlines — quote in shell).
- Right panel = full architecture per **paper Figure 1** data in an
  **Alammar-style** rendering (candidate banked:
  `slide_057_source/The_transformer_encoder_decoder_stack.png`); Q/K/V
  circles, dashed arcs and recoloring are presentation-layer (paper Fig 1 is
  monochrome; frame wins for styling).
- No NEW downloads into this dir (everything referenced is banked elsewhere).

## What the sources CONFIRM (carried + this session's live re-checks)

- Fig 2 left chain (MatMul → Scale [Mask opt.] → SoftMax → MatMul·V) and
  Fig 2 right chain (Linear ×3 → parallel Scaled Dot-Product ×h → Concat →
  Linear): paper §3.2.1–3.2.2 + banked figures. CONFIRMED.
- Encoder/decoder stacks of N=6 identical layers, each = MHA (+masked MHA +
  cross-attention in decoder) with Add & Norm, plus FFN with Add & Norm;
  inputs/outputs with embeddings + positional encoding; Linear+softmax
  output probabilities: paper §3.1/§3.3. CONFIRMED.
- "(shifted right)" output labeling: paper Fig 1's own label. CONFIRMED.

## Course vs paper discrepancies (NOT defects — recreation keeps course form)

- Course recolors the paper figures (Part I precedent: topology/labels are
  the paper's, pixel style the slide's). "WE ARE HERE" pin, highlighter
  blobs and zoom-callout connectors are instructor pedagogy — paper has none.
- h as annotation on the stacked SDPA boxes and "N×" repetition symbol:
  paper Fig 1 uses "N×"; the "h" head-count on the middle panel is the
  course's own annotation (paper draws 8 shaded copies; course draws a
  stacked-box motif). Kept verbatim.

## Open questions

- [?] ENCODER column order on the right panel: the transcript lists
  bottom-to-top "Positional Encoding → Add & Norm → Feed Forward → Add &
  Norm → Multi-Head Attention" — INVERTED vs paper Fig 1 / Alammar (whose
  encoder reads, bottom-to-top, attention sub-layer FIRST then FFN). Either
  the frame genuinely stacks it oddly or the transcript mis-ordered the
  boxes. Zoom t≈746–762 s before building; do not silently reorder.
- [?] LEFT panel order of "Mask (opt.)" vs "Scale": transcript's listing is
  ambiguous (parent 001:019's frame and the paper read MatMul → Scale →
  Mask (opt.) → SoftMax). Zoom before build.
- [?] Right-panel pixel identity vs banked Alammar asset — zoom/compare
  before build (transcript identification is the evidence of record).
- [?] Decoder "Q" circle under Masked Multi-Head Attention; any V/K obscured
  by the highlighter blob — zoom needed.

## Script-12 raw cross-check (raw-verification worker, 2026-10-11 — raw + final
both now on disk; the record's frame facts were transcript-based)

- `analysis/slide_019_raw.json` read in full (model `images`; old extraction 37;
  kept_frame frame_00763, 17 frames). Three-panel composition, paper-figure
  provenance, and overlay set confirmed.
- [?] RESOLVED (encoder column order): raw reads the encoder stack bottom→top as
  Inputs → Input Embedding → Positional Encoding → Multi-Head Attention (with
  V/K/Q circles) → Add & Norm → Feed Forward → Add & Norm — i.e. the attention
  sub-layer sits BELOW the FFN, matching paper Figure 1. The transcript's
  "inverted" listing was its own mis-order (raw + paper agree; the standing
  zoom glance may confirm at zero cost).
- [?] RESOLVED (Mask vs Scale): raw reads the left panel chain Q,K → MatMul →
  Scale → Mask (opt.) → SoftMax → MatMul with V bypassing up the right side
  into the top MatMul — Scale BELOW Mask (opt.), matching paper Fig 2 left and
  the 001 parent's frame.
- [?] RESOLVED (decoder attention circles): raw sees V (blue), K (blue), Q
  (red) circles under BOTH decoder attention boxes (Masked MHA and cross MHA)
  — the "any V/K obscured" item is resolved.
- Refinement (pin target): raw locates the "WE ARE HERE" pin tip pointing into
  the encoder's highlighted Positional Encoding / Input Embedding area (the
  record said lower Add & Norm / MHA area) — fits the lecture's PE topic at
  t≈746–762 s; frame wins at build.
- Raw additions: the yellow overlay is a translucent BAND across the bottoms of
  BOTH panels plus a yellow POLYLINE traced from the encoder MHA output to the
  decoder MHA's V/K inputs, with two black circular-arrow doodles above each
  Positional Encoding box (refines the record's "two highlighter blobs");
  "SoftMax" (left panel) vs "Softmax" (right panel) spelling inconsistency
  confirmed — preserve.
- [?] STANDS: right-panel pixel identity vs the banked Alammar stack asset
  (vision comparison, not resolvable by raw).
- Script-13 final ALREADY LANDED: `analysis/slide_019_final.json`
  (PASS_WITH_FIXES); `slide_title` matches the raw verbatim. Corrections: none
  yet at title level — verify against the final's fix list when building.
