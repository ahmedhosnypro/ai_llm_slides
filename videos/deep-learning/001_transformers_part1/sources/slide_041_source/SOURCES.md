# SOURCES.md — slide 041 "Encoder – Decoder Transformer" (three-level zoom, WE ARE HERE on Multi-Head Attention)

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via WebFetch of
arXiv HTML v7. No vision calls run; no image access — frame facts below come from
the script-12 raw transcription, which is the record of the frame.

## Slide identity

- New (curated) slide **041** ← old extraction slide **84**
  (`unique_slides/new2old_mapping.json` — CORRECTED in the W-G cross-check
  2026-10-11; this file previously misrecorded 101, which belongs to slide
  042; the two raws have distinct kept frames, frame_03836.jpg vs
  frame_03987.jpg, so both could not be old 101), frame
  `unique_slides/slide_041.jpg`, badge "41".
- Frame facts (raw transcription): red title "Encoder – Decoder Transformer";
  THREE diagrams tied by red dotted zoom lines —
  **left**: small green-bordered "Scaled Dot-Product Attention" schematic
  (bottom-up: Q/K/V circles → MatMul → Scale → Mask (opt.) → SoftMax → MatMul,
  V fed up the right side into the top MatMul);
  **center**: tan "Multi-Head Attention" zoom (bottom: V/K/q circles → three
  "Linear" boxes → stacked Scaled Dot-Product Attention block with "× h" →
  Concat → Linear), with a red **"WE ARE HERE"** map pin on its top-left
  corner;
  **right**: full Encoder–Decoder architecture panel (tan Encoder / pale-green
  Decoder; Inputs → Input Embedding → ⊕ Positional Encoding → V/K/Q circles →
  Multi-Head Attention → Add & Norm → Add & Norm + Feed Forward, N×; decoder:
  "Outputs (shifted right)" → Output Embedding → ⊕ → Masked Multi-Head
  Attention → Add & Norm → Multi-Head Attention (fed by encoder K,V [?]) →
  Add & Norm → Add & Norm + Feed Forward → Linear → Softmax → "Output
  Probabilities"; dark-red dashed autoregressive curve; yellow highlight
  bands).
- Position in the course: navigation slide opening the transformer-block
  treatment — the course zooms from the whole architecture (right) into the
  encoder's Multi-Head Attention block (center zoom) down to its scaled
  dot-product core (left), with the pin marking where the lecture now stands
  (multi-head, after slides 40/42's Wide/Narrow intro).

## Primary source

- **URL**: https://arxiv.org/html/1706.03762v7 — "Attention Is All You Need"
  (Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin,
  2017), arXiv:1706.03762v7 [cs.CL] (verified live 2026-10-11).

## Figures used by this slide

**Per-figure use: Figure 1 + Figure 2 left + Figure 2 right** — the course
redraws all three paper figures in its own style on ONE slide (right panel =
Figure 1; center zoom = Figure 2 right; left schematic = Figure 2 left).

- **Figure 1** — caption (verbatim, v7): "Figure 1: The Transformer - model
  architecture."
- **Figure 2 (left)** — caption: "(left) Scaled Dot-Product Attention. …"
- **Figure 2 (right)** — caption: "… (right) Multi-Head Attention consists of
  several attention layers running in parallel."
- All three originals are **already banked** in `../slide_18_source/`
  (founder downloads — do not modify that dir's files; this slide references
  the bank per the video AGENTS.md figure-family rule). arXiv v7 asset
  provenance (verified byte-identical there on 2026-10-11):
  - Figure 1: https://arxiv.org/html/1706.03762v7/Figures/ModalNet-21.png
  - Figure 2 left: https://arxiv.org/html/1706.03762v7/Figures/ModalNet-19.png
  - Figure 2 right: https://arxiv.org/html/1706.03762v7/Figures/ModalNet-20.png
- **No new figures downloaded into this dir** (AGENTS.md forbids re-downloading
  the banked arXiv figures; the bank is the reference).

## What the paper CONFIRMS (data behind the slide)

- **Left schematic = Figure 2 left, topology AND labels**: the paper figure's
  bottom-up chain is MatMul → Scale → Mask (opt.) → SoftMax → MatMul, with Q,K
  entering the first MatMul and V bypassing up to the second — the slide's
  chain matches (including the verbatim figure label "Mask (opt.)" and the
  figure's block spelling "SoftMax"; the right panel's "Softmax" spelling
  difference is the instructor's, preserved as transcribed).
- **Center zoom = Figure 2 right**: h parallel branches of Linear → Scaled
  Dot-Product Attention → Concat → Linear; the paper figure draws a stack of
  parallel Scaled Dot-Product Attention boxes — the slide's "stack of ~4
  offset copies" mirrors that, and the "× h" annotation matches "h parallel
  attention layers, or heads" with h=8, d_k=d_v=d_model/h=64 (§3.2.2).
- **Right panel = Figure 1**: encoder/decoder stacks with N× marks, Input /
  Output Embedding, Positional Encoding (⊕), Add & Norm, Feed Forward, Masked
  Multi-Head Attention (decoder only), Linear, Softmax, "Outputs (shifted
  right)" → "Output Probabilities" — all paper figure labels. Stack counts
  behind N×: N=6 identical layers both sides (§3.1).
- **The raw's "[?] K,V from the encoder top feeding the decoder's second MHA"
  is CONFIRMED by the paper**: §3.2.3 first bullet — "In 'encoder-decoder
  attention' layers, the queries come from the previous decoder layer, and the
  memory keys and values come from the output of the encoder. This allows
  every position in the decoder to attend over all positions in the input
  sequence." Figure 1 draws exactly those arrows into the decoder's
  Multi-Head Attention block. (Frame-level rendering of those arrows still
  re-checks at build — see [?] below; the CONCEPT is no longer uncertain.)
- **The autoregressive dashed loop** ("Outputs (shifted right)" feeding back
  around to "Output Probabilities"): §3.2.3.1 — masked self-attention
  "to ensure that the predictions for position i can depend only on the known
  outputs at positions less than i" — i.e., generation proceeds output →
  next-input, which the dashed curve depicts.

## Course-authored elements (no paper counterpart — do not "fix" to a source)

- The three-level zoom composition, the "WE ARE HERE" pin, the red dotted
  connector lines, the yellow highlight bands and red block borders, the
  color scheme (tan encoder / pale-green decoder, purple masked-MHA, pastel
  blocks), the lowercase "q" circle in the center zoom (course's own token
  style), and the title — all instructor pedagogy on the FRAME.

## [?] Uncertain items

- [?] The paper-level [?] on the encoder K,V → decoder MHA connection is
  RESOLVED (see CONFIRMS); the frame-level question of exactly how those
  arrows are drawn on THIS frame re-checks at build (raw flagged it [?]).
- [?] Green "corner handles/brackets" on the left schematic and center zoom —
  tiny decoration detail; re-check at build.
- [?] Salmon highlight on the rightmost Linear box in the center zoom [?] —
  tiny color detail; re-check at build.
- [?] Exact extent of the yellow highlight band across the Multi-Head
  Attention level — layout fact; re-check at build.

## Corrections

- **Cross-check 2026-10-11 (W-G, post-banking):** none — consistent (raw).
  No patches to `analysis/slide_041_raw.json`: the paper-level [?] (encoder
  K,V → decoder MHA) was already resolved above; the remaining [?]s
  (arrow rendering, corner brackets, salmon tint, highlight-band extent) are
  frame-level details the raw flags but cannot answer. Frame facts in this
  file re-verified against the raw (Fig-2-left chain, Fig-2-right chain, Fig-1
  labels, SoftMax/Softmax spelling split, lowercase q). **SOURCES.md-side fix:**
  the slide-identity line above misrecorded the old extraction number as 101;
  corrected to 84 per `unique_slides/new2old_mapping.json` (42 is the old-101
  slide).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout,
verbatim text, drawn content). The sources confirm/correct DATA and record
provenance; they never license inventing or "improving" content the slide
doesn't show. If source and slide disagree, record the discrepancy — the slide
wins for recreation, the source wins for understanding.
