# SOURCES.md — 002 slide 057 "encoder + decoder composed on one slide" (working title — no raw analysis yet; title TBD from frame)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory; founder-flagged special slide with MANDATORY
decoder web research). Machine-verified 2026-10-11 by the Part II web-research
worker (no vision calls run — no image access; frame facts below come from the
founder's directive + `slide_dependencies.json`, not a raw transcription).

## Slide identity

- Video-2 (002_transformers_part2) curated slide **057** ← old extraction slide
  **147** (`unique_slides/new2old_mapping.json`), frame
  `unique_slides/slide_057.jpg` (kept from t≈4934 s), badge numeral 57.
- Founder flag + `slide_dependencies.json` `special.57`: **encoder (from slide
  47 — chain 47 ← 46 ← 45 ← 28) + decoder composed professionally on ONE
  slide.** MANDATORY web research for the correct decoder architecture — DONE
  2026-10-11 (see below). First candidate to verify against the frame: 001's
  banked Figure 1 (arXiv 1706.03762v7 Figure 1 IS the encoder+decoder
  composition).
- In-video dependency: `57 ← 47` (`slide_dependencies.json` edges).

## Primary source

- **Paper**: "Attention Is All You Need" — Vaswani, Shazeer, Parmar, Uszkoreit,
  Jones, Gomez, Kaiser, Polosukhin (2017), arXiv:1706.03762v7.
  - **§3.1 "Decoder"** (verified live via WebFetch 2026-10-11): "The decoder is
    also composed of a stack of N=6 identical layers." Decoder layer = three
    sub-layers: (1) **masked multi-head attention** (mask ensures position i
    attends only to known outputs < i), (2) **encoder-decoder multi-head
    attention** (queries from the decoder layer below; keys/values from the
    encoder output), (3) **position-wise feed-forward** — each sub-layer with
    residual connection + LayerNorm; final **Linear + softmax** on top; decoder
    inputs are the **output embeddings shifted right** (position-shifted,
    per Figure 1's "Outputs (shifted right)").
  - **Figure 1** = the canonical encoder+decoder composition (confirmed as
    such by research query, 2026-10-11): encoder stack left, decoder stack
    right, K/V feeding encoder output into the cross-attention.
- **Banked first candidate** (do NOT re-download; byte-identity proven):
  `../001_transformers_part1/slide_18_source/The Transformer - model architecture..png`
  = live asset https://arxiv.org/html/1706.03762v7/Figures/ModalNet-21.png
  (159,152 bytes, sha256[:16] `56d69ccc192b90c3`, verified byte-identical
  2026-10-11).

## Figures used / downloaded (into this dir, 2026-10-11)

- `Transformer_decoder.png` — Jay Alammar, "The Illustrated Transformer"
  (https://jalammar.github.io/illustrated-transformer/), decoder-side figure.
  879×279 RGBA, 38,751 bytes, fetched live from
  https://jalammar.github.io/images/t/Transformer_decoder.png
- `The_transformer_encoder_decoder_stack.png` — same page, N× stacked
  encoder+decoder composition figure. 1218×793 RGBA, 127,812 bytes, fetched
  live from
  https://jalammar.github.io/images/t/The_transformer_encoder_decoder_stack.png
- **Not duplicated**: the paper's Figure 1 (first candidate) stays in 001's
  bank — reference it by the path above; `slide_dependencies.json`
  `shared_image_sources.57` already points at `001_transformers_part1/slide_18_source/`.

## What the source CONFIRMS

- The correct decoder architecture for the composition: N=6 identical decoder
  layers of [Masked Multi-Head Attention → Encoder-Decoder (cross) Attention →
  Feed Forward], each wrapped with residual + LayerNorm, over shifted-right
  output embeddings + positional encodings, topped by Linear + Softmax.
- Figure 1 is the established canonical single-image encoder+decoder
  composition; the Alammar decoder figure is the established standalone
  decoder-side walkthrough (research-verified 2026-10-11).
- No data discrepancy found so far between the paper's §3.1 topology and the
  banked Figure 1's decoder column.

## Course-authored elements

- **Whether 002's frame reuses the banked Figure 1 pixels, the course's own
  redraw (as in 001's figure family), or composes its slide-47 encoder with a
  separately drawn decoder**: `[?]` `[pending raw]` — script-12 has not run for
  this slide; the frame comparison (vision) decides which candidate is the
  match. Slide frame is ground truth; do not force a candidate onto the frame.
- The encoder half should follow the slide-47 chain's certified composition
  (deps `57 ← 47`, chain through 46/45/28) — per-slide build law, not a web
  question.

## [?] Open questions

1. Which decoder figure (if any) the slide actually reuses — banked Fig 1 vs
   course redraw vs one of the downloaded Alammar candidates — resolve against
   `unique_slides/slide_057.jpg` in the vision pass.
2. Whether the slide includes the final Linear/Softmax + "Output
   Probabilities" tail and the "Outputs (shifted right)" input label.
3. Slide's verbatim title/banners — `[pending raw]`.

## Corrections

None yet — record any slide-vs-source discrepancy here when the raw analysis
and vision pass land (fidelity law: slide wins for recreation, source wins for
understanding).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what each slide shows; web sources
confirm/correct data and provenance, never license inventing content. `[?]`
markers are removed only with a confirming URL recorded here.
