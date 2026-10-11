# SOURCES.md — slide 021 "[1] Position Encoding" (PE concept intro: positions → function → vectors)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11: vision
transcript of record
`transcripts/slide_021_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner round 1) + live curl of the paper + one agy search.

## Slide identity

- New (curated) slide **021** ← old extraction slide **41** (kept frame
  `frame_00956.jpg`, shown t≈885–955 s) (`unique_slides/slides_index.json`),
  frame `unique_slides/slide_021.jpg`.
- Frame facts (vision transcript): title "[1] Position Encoding" ("[1]" red,
  "Position Encoding" dark blue); badge "21". Three-stage vertical pipeline in
  a blue-bordered panel: (1) dashed blue "Position Information" row of boxes
  0, 1, 2, 3, 4, 5, …(5 dots)…, N-2, N-1; (2) navy bar "function to map the
  positions to real valued vectors" ("function" in yellow) labeled "Positional
  Encoder"; (3) dashed green row of boxes Vector_P0 … Vector_P5, …,
  Vector_PN-2, Vector_PN-1 ("Vector" blue bold, red italic subscript) with a
  red curly brace down to a green-bordered note box: "Real valued vectors
  representing  positions" / "(Vector for each position)" / "Vector Length  =
  Word Embedding length". Yellow leader-line note box outside the panel:
  "[1] Function with Fixed Parameters" / "[2] Function with TRAINABLE
  Parameters". Gray mouse-cursor artifact near box "0" (recording artifact,
  omit in recreation).

## Primary source

- **URL**: https://arxiv.org/html/1706.03762v7 — Vaswani et al. 2017,
  "Attention Is All You Need", **§3.5 "Positional Encoding"** — fetched live
  2026-10-11 via curl (whole-page HTML saved at
  `scratch/webverify/paper_v7.html` for reuse by the PE-family slides).
- The slide is the **concept intro** for that section: it defines the
  positional-encoder stage and its two implementation options before any
  formula is shown (the sin/cos formulas arrive later in this deck's PE block,
  cf. slide 032 "Sin/Cos Positional Encoder").

## What the source CONFIRMS (verbatim from §3.5, live-verified 2026-10-11)

- Purpose: "Since our model contains no recurrence and no convolution, in
  order for the model to make use of the order of the sequence, **we must
  inject some information about the relative or absolute position of the
  tokens in the sequence. To this end, we add "positional encodings" to the
  input embeddings at the bottoms of the encoder and decoder stacks.**" —
  confirms the slide's Position-Information → per-position-vectors framing.
- Vector length: "The positional encodings have the same dimension d_model as
  the embeddings, so that the two can be summed." — confirms the green box's
  "Vector Length = Word Embedding length".
- The fixed-vs-trainable note is the paper's own dichotomy: "**There are many
  choices of positional encodings, learned and fixed [9].** In this work, we
  use sine and cosine functions of different frequencies…" plus "We also
  experimented with using learned positional embeddings [9] instead, and found
  that the two versions produced nearly identical results" — confirms note
  "[1] Function with Fixed Parameters / [2] Function with TRAINABLE
  Parameters" as exactly the paper's sinusoidal (fixed) vs learned (trainable)
  pair.
- Real-valued vectors, one per position index 0…N-1: matches the paper's
  PE(pos, 2i) indexing over positions ("where pos is the position and i is the
  dimension").
- agy search (2026-10-11) independently confirms the canonical pair: fixed =
  Vaswani et al. 2017 (arXiv:1706.03762); trainable/learned = position lookup
  table N × d_model as used by BERT (arXiv:1810.04805) and GPT-1 (OpenAI
  tech report); both must be d_model-long to add element-wise to token
  embeddings.

## Figures used by this slide

- **None.** The drawing is a course-original schematic (dashed indexed rows,
  navy function bar, brace annotation) — the vision transcript explicitly
  finds no resemblance to Vaswani Fig 1/2 or any Alammar/d2l/Bloem figure.
  Nothing downloaded. (PE-matrix / curve illustrations that the later PE
  slides may reuse are catalogued in SOURCES_MAP.md Part II download
  candidates 1–3; not needed here.)

## Course-authored elements (no source counterpart)

- Title "[1] Position Encoding" (the "[1]" sub-series numbering), the
  three-stage flow composition, the Vector_Pi label style, the red curly
  brace, the yellow note box, badge "21".

## [?] Uncertain items

- none. (No formulas on this slide; nothing numeric to cross-check beyond the
  equality "Vector Length = Word Embedding length", which §3.5 confirms.)

## Corrections

- none — frame content is fully consistent with §3.5's framing; nothing to
  correct against the source.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout,
verbatim text, drawn content). This source confirms/corrects DATA and records
provenance; it never licenses inventing or "improving" content the slide
doesn't show.
