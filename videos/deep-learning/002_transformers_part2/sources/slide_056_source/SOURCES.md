# SOURCES.md — 002 slide 056 "Decoder Final Output"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Machine-verified 2026-10-11 by the Part II
web-verification worker: vision transcript banked
(`transcripts/slide_056_vision_2026-10-11.txt`, default `images` route, one
probe, `--thinking high --max-tokens 65536`, via `scripts/16_vision_gate.sh`),
web confirmation via live fetches (no new agy call needed — the two sources
for this slide were already fetched live this session for slides 052/053).

## Slide identity

- Video-2 (002_transformers_part2) curated slide **056** ← old extraction
  slide **139** (`unique_slides/new2old_mapping.json`), frame
  `unique_slides/slide_056.jpg` (kept from t≈4854 s; shown only 4852–4853 s,
  2 frames — a brief transitional slide), badge numeral 56.
- Content (banked vision transcript): title verbatim **"Decoder Final
  Output"** (red); blue subtitle **"Probability of each word in Vocab"**
  over a large red curly brace on the top row. Bottom-to-top: navy bar
  **"Last Decoder Block"** → row of 4 green circles → green-outlined panel
  **"Linear Projection"** containing a dense all-to-all fan of thin blue
  lines from the 4 green circles to **16 magenta circles** (the projected
  vocab-sized vector) → maroon bar **"Softmax"** (16 upward arrows) → top
  row of **16 light-blue circles** = output probabilities. Red left-margin
  labels **"Vocab Size"** annotate both the magenta and light-blue rows.
  The 4-vs-16 counts are diagrammatic only (no numeric labels).

## Primary source — CONFIRMED (mechanism), paper verbatim

- **Paper**: "Attention Is All You Need" — Vaswani et al. 2017,
  arXiv:1706.03762v7, quote verified live 2026-10-11 from
  https://arxiv.org/html/1706.03762v7 (HTML banked at
  `../scratch/paper_v7.html`, extracted during the slide-053 session):
  - §3.1 (end): "**We also use the usual learned linear transformation and
    softmax function to convert the decoder output to predicted next-token
    probabilities.**" — exactly the slide's "Last Decoder Block" →
    "Linear Projection" → "Softmax" → "Probability of each word in Vocab".
- No discrepancy: the slide is the standard decoder-tail schematic; the
  drawn dense fan (4 green → 16 magenta) is the linear transformation
  (d_model → vocab_size) in pictogram form, and the top row is the softmax
  distribution over the vocabulary.

## Tutorial counterpart — Jay Alammar, "The Illustrated Transformer" (live page, banked HTML)

- Its section **"The Final Linear and Softmax Layer"** (verified live,
  `../scratch/alammar_it.html`): describes "final Linear layer which is
  followed by a Softmax Layer", converting the decoder stack output "into a
  much, much larger vector called a logits vector" — the same tail with the
  same small-vector→vocab-vector framing. Its example shows example tokens
  ("the", "robot"-style) rather than the slide's generic circle rows.
- Figure downloaded into this dir (2026-10-11):
  - `transformer_decoder_output_softmax.png` — Alammar's decoder-output
    Linear+Softmax figure. 869×561 RGBA, 70,754 bytes, fetched live from
    https://jalammar.github.io/images/t/transformer_decoder_output_softmax.png
    — reference-grade ground truth for the tail concept (slide's palette
    and circle pictograms are the lecturer's own; NOT a pixel match).

## What the source CONFIRMS / CORRECTS

- CONFIRMED: decoder final block → learned linear projection to a
  vocab-sized logits vector → softmax → per-word output probabilities;
  "Vocab Size" as the projected dimension.
- CORRECTED: nothing — no slide-vs-source disagreement found.
- Continuity: 056 completes the decoder chain 052 (stack) → 054 (masked
  self-attention stage) → 055 (cross-attention stage) → 056 (final Linear +
  Softmax); the paper tail quote also appears in slide 057's record
  (§3.1 verified there too).

## [?] Open questions

1. Whether the 4 green circles are meant as d_model=4 (generic
   illustration) — diagrammatic only, no label `[?]` (recreation keeps the
   drawn counts; nothing to web-confirm).
2. Exact brace span (2nd–15th circle) — cosmetic, frame-level `[?]` only.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what each slide shows; web
sources confirm/correct data and provenance, never license inventing content.
`[?]` markers are removed only with a confirming URL recorded here.

## Script-12 raw cross-check (2026-10-11, web-research verification worker)

Cross-checked against `analysis/slide_056_raw.json` (script-12 raw landed
after this record was written from the banked vision transcript).

- CONFIRMED by raw: title "Decoder Final Output" (red) + blue subtitle
  "Probability of each word in Vocab" over a red curly brace; bottom→top
  stack navy "Last Decoder Block" bar → 4 green up-arrows → 4 green circles
  → green-bordered "Linear Projection" panel containing 16 magenta circles
  fully connected to the 4 green circles by 64 thin blue lines → 16 red
  up-arrows → dark-red "Softmax" bar → 16 blue up-arrows → 16 pale-blue
  circles; red "Vocab Size" labels at the left of BOTH the pale row and the
  magenta row; badge "56"; identity metadata (old extraction slide 139,
  kept frame_04854, shown 4852–4853 s, 2 frames — the brief transitional
  slide). The raw pins the exact counts the record described as
  diagrammatic: 16 pale, 16 magenta, 4 green, 4×16 = 64 lines. No source
  claims in this record are contradicted; the downloaded Alammar reference
  figure remains reference-only (raw describes generic circle pictograms,
  consistent with "lecturer's own palette — NOT a pixel match").
- RAISED (cosmetic, keeps `[?]`): brace span — the raw reads the red curly
  brace as spanning "the full width of the 16 pale output circles", while
  the banked transcript read 2nd–15th circle. Open question 2 stays `[?]`
  as a frame-level cosmetic check for the build pass (two independent
  reads disagree).
- Open question 1 (4 green circles as generic d_model) — raw adds no label
  or count semantics; remains `[?]` (recreation keeps drawn counts; nothing
  to web-confirm).
- New raw detail (no conflict): light-gray panel #E9E9E9 on a white outer
  margin; magenta circles outline-less; pale circles thin blue-gray
  outlines — build-level only.
- No new published-figure claim appears in the raw; nothing to fetch.
- Corrections needed: none.
