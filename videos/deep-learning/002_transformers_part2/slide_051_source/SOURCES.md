# SOURCES.md — 002 slide 051 "split halves of the Transformer architecture figure" (working title — no raw analysis yet; title TBD from frame)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory; founder-flagged special slide). Machine-verified
2026-10-11 by the Part II web-research worker (no vision calls run — no image
access; the frame placement below is deliberately left to the vision worker).

## Slide identity

- Video-2 (002_transformers_part2) curated slide **051** ← old extraction slide
  **122** (`unique_slides/new2old_mapping.json`), frame
  `unique_slides/slide_051.jpg` (kept from t≈4129 s), badge numeral 51.
- Founder flag + `slide_dependencies.json` `special.51`: this slide shows **001's
  slide-18 source image (arXiv 1706.03762v7 Figure 1) split into left and right
  halves, placed at different measured positions on this slide**.
- Cross-video dependency: `51 ← deep-learning/001_transformers_part1:18`
  (001 slide 18 = the Fig 1 + Fig 2L + Fig 2R paper-figures slide; its provenance
  record is `001_transformers_part1/slide_018_source/SOURCES.md`).
- `[pending raw]` — 002 script-12 analysis has NOT run for this slide yet; the
  frame facts above come from the founder's directive, not a raw transcription.

## Primary source

- **Paper**: "Attention Is All You Need" — Vaswani, Shazeer, Parmar, Uszkoreit,
  Jones, Gomez, Kaiser, Polosukhin (2017), arXiv:1706.03762v7 — **Figure 1**,
  "The Transformer - model architecture."
- **Live asset URL**: https://arxiv.org/html/1706.03762v7/Figures/ModalNet-21.png
  (NOTE: under `/Figures/`, NOT `/assets/` — see Failed-findings note in the map).
- **Banked original** (do NOT modify):
  `../001_transformers_part1/slide_18_source/The Transformer - model architecture..png`
- **Byte-identity proof (2026-10-11)**: banked file = live arXiv asset, both
  159,152 bytes, sha256 prefix `56d69ccc192b90c3` — the bank's Figure 1 is
  byte-identical to the paper's published asset. So BOTH halves of this slide
  inherit the bank's provenance in full.

## Figures used

The banked Figure 1 (1520×2239 RGBA) **split into left/right halves at the image
midline x=760**. Machine-derived in this dir from the banked original (bank
original untouched):

- `fig1_left_half_x0-760.png` (760×2239, sha256[:16] `93b5ff68248fb219`)
- `fig1_right_half_x760-1520.png` (760×2239, sha256[:16] `7fd176d5bc3298cf`)

Measured facts about the split line (deterministic pixel analysis, 2026-10-11):

- The figure's central white gap between the encoder and decoder columns spans
  x=716–803 (two ≥98%-white bands: 716–756 and 765–803).
- The midline x=760 passes through that gap and **clips a 9-px black vertical
  connector line at x=758–766 (rows y=802–1107)** — part of the K/V arrow
  assembly feeding encoder output into the decoder's Encoder-Decoder Attention.
  A literal "split in half" produces exactly this clipping; each half keeps a
  4–5 px stub of that line.
- Reassembly of the two halves is pixel-identical to the banked original
  (verified programmatically) — the halves are a lossless decomposition.
- Alternative semantic cut candidates (if the frame shows cleaner-cut halves):
  mid-band cuts at x=736 or x=784, which leave the connector line wholly on the
  right half. `[?]` — adjudicate against the frame before composing.

## What the source CONFIRMS

- Provenance: whatever this slide shows as its two halves is (per the founder)
  the paper's Figure 1 — the canonical encoder+decoder composition. Left half =
  the paper's encoder column (input embedding, positional encoding, N×
  [Multi-Head Attention + Feed Forward], each with Add & Norm); right half = the
  decoder column (output embedding shifted right, positional encoding, N×
  [Masked MHA + Encoder-Decoder Attention + Feed Forward], final Linear +
  Softmax). (Layout per the paper's Figure 1 / §3.1 and the bank's SOURCES.md —
  not re-verified pixel-by-pixel here.)
- The half files in this dir are certified-lossless derivatives of that banked,
  byte-identical asset.

## Course-authored elements

- **Placement and size of each half on THIS frame**: `[?]` pending the vision
  pass — the vision worker must PIL-measure (or template-match) each half's
  position/scale against `unique_slides/slide_051.jpg` and compose exactly
  (founder directive: "Attention needed"). Vision work goes through
  `.agents/skills/image-analysis` (banked `.txt` transcripts).
- Whether the halves are recolored/redrawn by the course or used as-is:
  `[?]` pending raw + vision.
- House chrome (red frame, yellow badge "51", title line) is course chrome per
  the playlist law (`../AGENTS.md`, `../shared_patterns/house_chrome.js`).

## [?] Open questions

1. Exact cut line used by the course (midline x=760 vs x=736/784 band cuts) —
   resolve against the frame.
2. Whether the course applies any recolor/scale beyond placement — resolve
   against the frame.
3. Slide's verbatim title/banners — `[pending raw]` (script-12 has not run).

## Corrections

None yet — record any slide-vs-source discrepancy here when the raw analysis
and vision pass land (fidelity law: slide wins for recreation, source wins for
understanding).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what each slide shows; web sources
confirm/correct data and provenance, never license inventing content. `[?]`
markers are removed only with a confirming URL recorded here.
