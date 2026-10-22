# SOURCES.md — slide 037 "Transformer Blocks (stacked over Multi-Head)" (cross-video child of 001:19)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_037_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner) cross-checked against `analysis/slide_037_raw.json` (raw's
label list matches the transcript on every block name). This slide is a
**cross-video child of 001 slide 19** (dep `37 ← 001:19`,
`slide_dependencies.json`): the parent record
`../001_transformers_part1/slide_019_source/SOURCES.md` and the figure bank
`../001_transformers_part1/slide_18_source/` CARRY for the figure trio; only
NEW visual differences of this frame are recorded here (recap rule per the
video AGENTS.md). Web evidence re-confirmed live this session from the banked
paper fetch (`scratch/webverify/paper_v7.html`, captions quoted below); no
new agy query spent — figure identity is founder-established (CONFIRMED) and
the paper text is already live.

## Slide identity

- New (curated) slide **037** ← old extraction **104** —
  `unique_slides/new2old_mapping.json`, frame `unique_slides/slide_037.jpg`.
- Frame facts (vision transcript): title "Transformer Blocks (stacked over
  Multi-Head)"; badge "37". Three green-bordered panels left-to-right joined
  by red dashed zoom lines:
  1. LEFT: "Scaled Dot-Product Attention" — chain bottom-to-top
     Q/K/V circles → MatMul → Scale → Mask (opt.) → SoftMax → MatMul, with
     the right-side skip line into the second MatMul.
  2. MIDDLE: "Multi-Head Attention" — V/K/Q circles → 3 Linear boxes (gray
     stacked shadows = h parallel heads) → Scaled Dot-Product Attention
     (stacked shadow, "}" + "h" brace) → Concat → Linear.
  3. RIGHT: full encoder–decoder in **Alammar styling** (peach Encoder
     panel, light-green Decoder panel; Inputs → Input Embedding + Positional
     Encoding circle → Add & Norm → Multi-Head Attention (V/K/Q circles) →
     Add & Norm → Feed Forward → Add & Norm; decoder: Outputs (shifted
     right) → Output Embedding + PE → Add & Norm → Masked Multi-Head
     Attention → Add & Norm → Multi-Head Attention (encoder K/V cross-arrows)
     → Add & Norm → Feed Forward → Add & Norm → Linear → SoftMax → Output
     Probabilities; N× circles on both panels; red dashed feedback arc from
     the top Output down to "Outputs (shifted right)").
  - Lecture overlays: red "WE ARE HERE" map-pin anchored at the ENCODER's
    Multi-Head Attention / Add & Norm region (red circle partially covering
    that block); red dashed leader lines crossing mid-slide whitespace.
  - Transcript notes the small "Add & Norm" labels are the least-certain
    text (very small font) — consistent with the paper's construct either
    way.

## Primary source (figure family — CONFIRMED, carried from the parent)

**arXiv 1706.03762v7 "Attention Is All You Need"** — figures banked in
`../001_transformers_part1/slide_18_source/` (founder downloads; sha256
verified byte-identical to the live arXiv assets per the SOURCES_MAP Part II
provenance block):
- Figure 1 = `The Transformer - model architecture..png` (= ModalNet-21.png,
  159,152 B) — caption (banked v7 fetch, verbatim): "Figure 1: The
  Transformer - model architecture. Most competitive neural sequence
  transduction models have an encoder-decoder structure…".
- Figure 2 left = `slide18 scaled dot-production attention figure.png` (=
  ModalNet-19.png, 26,323 B) — caption: "Figure 2: (left) Scaled Dot-Product
  Attention. (right) Multi-Head Attention consists of several attention
  layers running in parallel."
- Figure 2 right = `slide18 Multi-Head Attention\n\n.png` (= ModalNet-20.png,
  65,853 B; filename contains literal newlines — quote in shell).
The course redraws these in its own style; topology and labels are the
paper's (left/middle panels match the paper's chain labels exactly).
- Right-panel Alammar styling — candidate figure already banked in
  `../slide_057_source/The_transformer_encoder_decoder_stack.png`
  (1218×793, Jay Alammar "The Illustrated Transformer",
  https://jalammar.github.io/illustrated-transformer/, live-verified in the
  map's 057 row); referenced, not re-downloaded. Same styling call as the
  video-2 019 record ("paper Fig 1 data in Alammar styling").

## What the paper CONFIRMS (carried + re-checked)

- Scaled Dot-Product Attention chain (MatMul → Scale → Mask (opt.) → SoftMax
  → MatMul, V-skip) — §3.2.1 equation (1) and Figure 2 left, verbatim.
- Multi-Head chain (Linear×3 → parallel SDA ×h → Concat → Linear) — §3.2.2
  and Figure 2 right, verbatim; "h" = head count.
- Encoder/decoder stack (N× identical layers; two sub-layers each with
  Add & Norm; decoder's masked MHA + cross-MHA + FFN; shifted-right outputs;
  Linear+softmax → output probabilities) — §3.1 and Figure 1, verbatim.

## NEW visual differences on THIS frame (vs the parent trio composition)

- Title "Transformer Blocks (stacked over Multi-Head)" (parent 001:19 title:
  "Encoder – Decoder Transformer"; video-2 sibling 019's title likewise).
- "WE ARE HERE" pin anchored at the ENCODER's Multi-Head Attention /
  Add & Norm region (course position marker, not in any published figure).
- Long red dashed feedback arc on the decoder's right edge (autoregressive
  next-token loop) — course-added annotation.
- Stacked gray shadow copies behind the middle panel's boxes (= h parallel
  heads rendering) — course style.
- No yellow highlighter blobs on this frame (sibling 019 has two).
- Q/K/V circle colors read consistently as Q red, K blue, V blue on all
  three groups of THIS frame (the parent record's V-color [?] resolves
  toward blue here, pending the parent's own build-time zoom).

## Figures used by this slide

- Paper Figures 1 + 2 left + 2 right — banked in
  `../001_transformers_part1/slide_18_source/` (reference; no download into
  this dir). Alammar stack figure referenced from
  `../slide_057_source/`. Nothing new downloaded (recap rule).

## Course-authored elements

- The zoom-ladder composition with dashed red leader lines, the "WE ARE
  HERE" pin, the feedback arc, panel headings in red italic, the stacked-
  shadow h rendering, badge "37" — keep verbatim for recreation.

## [?] Uncertain items

- [?] small "Add & Norm" label text at the frame's font size (transcript's
  least-certain read) — build-time zoom; expected "Add & Norm" per the paper
  and the parent record.
- [?] right-panel pixel identity vs the banked Alammar stack figure (HIGH
  styling call, as in the 019/057 records; pixel match is a build-time
  question).

## Corrections

- none — the transcript's block chains match the paper verbatim; the raw
  agrees.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. Sources
confirm/correct DATA and record provenance; they never license inventing or
"improving" content the slide doesn't show.
