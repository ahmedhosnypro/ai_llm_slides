# SOURCES.md — 002 slide 059 "Transformer Encoder as a Classifier" (architecture)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Machine-verified 2026-10-11 by the Part II
web-verification worker: vision transcript banked
(`transcripts/slide_059_vision_2026-10-11.txt`, default `images` route, one
probe, `--thinking high --max-tokens 65536`, via `scripts/16_vision_gate.sh`);
web verification: live keras.io fetch + one `agy` query (convergent) + paper
HTML already banked this session.

## Slide identity

- Video-2 (002_transformers_part2) curated slide **059** ← old extraction
  slide **149** (`unique_slides/new2old_mapping.json`), frame
  `unique_slides/slide_059.jpg` (kept from t≈5128 s; shown 5007–5127 s =
  121 frames, heavily taught), badge numeral 59. Content slide of the
  section divider 058 ("Transformer Encoder as a Classifier").
- Content (banked vision transcript), bottom→top: **Input Sequence** band =
  dashed-green row of **"Word Embedding Vectors"** cells **X_1 … X_5 …,
  X_{N-2}, X_{N-1}** ⊕ (dark-red circled plus) dashed-orange row of
  **"Position Information Vectors"** cells **Vector_{P0} … Vector_{P5} …,
  Vector_{P(N-2)}, Vector_{P(N-1)}** → **Transformer Encoder** (pale rose
  container with dark-red bars labeled **"Transformer Block"** top and
  bottom + vertical ellipses, i.e. N stacked identical blocks) →
  **Output Sequence** (light-blue container, cells **Y_1 … Y_5 …,
  Y_{N-2}, Y_{N-1}**) → white box **"Global Average Pooling"** (red italic
  annotation: "Single vector representing the whole sequence") → tan bar
  **"Softmax Layer"** carrying three navy circular nodes (yellow "Softmax",
  white Σ), with fan-in lines from the pooled vector → blue labels
  **C_1, C_2, C_3** under **"Output Classes"**.

## Primary sources — CONFIRMED (mechanism)

- **Paper**: "Attention Is All You Need" — Vaswani et al. 2017,
  arXiv:1706.03762v7 (https://arxiv.org/html/1706.03762v7 — HTML banked at
  `../scratch/paper_v7.html`, quotes verified live this session):
  - §3.1 encoder = stack of N=6 identical layers (the slide's stacked
    "Transformer Block" bars); input = embeddings + positional encodings
    (the slide's Word + Position vectors added element-wise); output =
    sequence of per-position encodings (the slide's Output Sequence Y_i).
  - §3.5 PE semantics (banked in the fleet record; 032 row of SOURCES_MAP).
- **The classifier tail (GAP + softmax) — verified live 2026-10-11**:
  **Apoorv Nandan, "Text classification with Transformer", Keras code
  example** — https://keras.io/examples/nlp/text_classification_with_transformer/
  (HTML banked at `../scratch/keras_tct.html`). Live-verified model:
  `TokenAndPositionEmbedding` (token embedding + positional embedding —
  the slide's Word + Position vector rows) → `TransformerBlock` →
  `layers.GlobalAveragePooling1D()` → Dense → `Dense(2, activation="softmax")`
  → class probabilities. The slide draws the same pipeline with a generic N
  (sequence length), N (blocks), and 3 classes (course choices; the example
  uses 1 block / 2 classes). One `agy` query independently named this same
  example — convergent with the direct fetch (the page itself hosts NO
  architecture figure, only logos; the slide's cartoon is course-drawn).
- **Alternate classifier pattern (context only)**: BERT — Devlin et al. 2018,
  arXiv:1810.04805 — classifies from a dedicated [CLS] token, NOT global
  average pooling; the slide's GAP tail is the Keras-example style, so BERT
  is recorded as the contrast pattern, not this slide's source `[?]` for any
  deeper comparison.

## Pattern-family note (founder dependency 59 ← 001:38)

- Founder assumption (pending veto, `slide_dependencies.json`): 059 is
  **pattern-derived from 001 slide 38** ("Self Attention Mechanism (Adding
  Scaling)" — the paper Figure 2-left inset family). 001's verified family
  record: `../../../001_transformers_part1/slide_038_source/SOURCES.md`
  (paper §3.2.1 MatMul → Scale → Mask → SoftMax → MatMul pipeline in course
  style). Slide 059 shares that family's stage-labeled, flat-color-vector
  teaching style but is a DIFFERENT composition (whole-encoder classifier,
  no Figure-2 inset) — per the dependency law: re-use the family's verified
  patterns, do NOT clone 001:38's composition.

## Figures downloaded

- None: keras.io hosts no architecture figure (verified — logos only), and
  the slide's cartoon is course-authored. Reference-only: banked paper
  Figure 1 (`../001_transformers_part1/slide_18_source/…`) for the encoder
  stack; the keras.io example page (code-level ground truth for the GAP
  tail); `../scratch/keras_tct.html` banked copy.

## What the source CONFIRMS / CORRECTS

- CONFIRMED: embeddings + positional vectors added element-wise before the
  encoder; N stacked identical blocks; per-position outputs; GAP collapsing
  the sequence to one vector; softmax over classes at the top.
- CORRECTED: nothing contradicts the sources. Presentation notes (slide's
  own, kept verbatim for recreation): position rows start at Vector_{P0}
  while embedding rows start at X_1 (an indexing-offset quirk of the
  slide's labels); sequence ends at index N−1 (1-based X but 0-based P).
- The slide's "+": element-wise addition — same op as paper §3.1
  (embeddings + PE) and the Keras example's embedding add.

## [?] Open questions

1. Exact pixel origin of the cartoon: course-authored `[?]` (no matching
   published figure found; keras.io has none; style is the deck's own).
2. Whether the lecture also mentions the BERT-style [CLS] alternative
   verbally — not decidable from the frame `[?]`.
3. The exact softmax-node design (navy circle + red rim + Σ) and the
   fan-in line count — cosmetic, frame-level `[?]`.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what each slide shows; web
sources confirm/correct data and provenance, never license inventing content.
`[?]` markers are removed only with a confirming URL recorded here.
