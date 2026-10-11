# SOURCES.md — slide 022 "Suggested Positional Encoders (Use Word Index as Position Encoding)"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_022_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner round 1) + live curl of two tutorial sources + one agy search.

## Slide identity

- New (curated) slide **022** ← old extraction **45** (old group split with new
  slide 023; **founder frame swap** — kept frame `frame_01037.jpg`, mid-group
  state, over the group's final kept frame `frame_01233.jpg`; shown t≈984–1232 s)
  (`unique_slides/slides_index.json`), frame `unique_slides/slide_022.jpg`.
- Frame facts (vision transcript): title "Suggested Positional Encoders"
  (maroon), subtitle "(Use Word Index as Position Encoding)" ("Word Index"
  underlined); badge "22". Three stacked rows in a blue-bordered panel, each
  labeled left ("Sequence of words with Length N", "Position Embedding",
  "Use Position Index"): Word 0…Word 5, …, Word N-2, Word N-1 (cream boxes,
  red italic) / Pos 0…Pos 5, …, Pos N-2, Pos N-1 (pale boxes) / bare indices
  0…5, …, N-2, N-1; "+δ" arrows between consecutive position boxes (8 shown).
  Bottom light-cyan panel: "Use δ=1" / "First position Encoding = 0 , Last
  Position Encoding = N-1" / "(Depends on Seq. Length)" (underlined); red
  "Problems:" heading + three bullets:
  1. "If N is large ( e.g. seq. Length = 1024 ) Large position Values will
     dominate when Combine Position Embedding to Word Embedding"
  2. "If System is trained with Max seq length =256 how can the system deal
     with Larger sequence values"
  3. "Position Encoding is scalar and Word embedding is vector (how to Combine
     them ?)"
  Mouse-cursor artifact overlapping the "N-1" box (recording artifact).

## Primary sources

1. **Kazemnejad, Amirhossein, "Positional Encoding in Transformers"** —
   https://kazemnejad.com/blog/transformer_architecture_positional_encoding/
   (verified live 2026-10-11 via curl; page HTML saved at
   `scratch/webverify/kazemnejad_pe.html`). Verbatim, confirming the slide's
   "Use the linear index" strawman and its problems: "Another idea is to
   assign a number to each time-step linearly. That is, the first word is
   given "1", the second word is given "2", and so on. **The problem with this
   approach is that not only the values could get quite large, but also our
   model can face sentences longer than the ones in training.** In addition,
   our model may not see any sample with one specific length which would hurt
   generalization of our model."
2. **Machine Learning Mastery, "A Gentle Introduction to Positional Encoding
   in Transformer Models"** —
   https://machinelearningmastery.com/a-gentle-introduction-to-positional-encoding-in-transformer-models-part-1/
   (verified live 2026-10-11 via curl; saved at
   `scratch/webverify/mlm_pe.html`). Verbatim, confirming the scalar-vs-vector
   problem: "There are many reasons why **a single number, such as the index
   value, is not used** to represent an item's position in transformer models.
   For long sequences, **the indices can grow large in magnitude**. If you
   normalize the index value to lie between 0 and 1, it can create problems
   for variable length sequences… **Transformers use a smart positional
   encoding scheme, where each position/index is mapped to a vector.**"
3. **arXiv 1706.03762v7 §3.5** (same live-verified fetch as slide 021's) — the
   formal anchor: "positional encodings have the same dimension d_model as the
   embeddings, so that the two can be summed" — the resolution of Problem 3
   (slide 021's green box already states the vector-length requirement).
- agy search (2026-10-11) independently ranks the same three failure modes
  (magnitude domination; training-length ceiling / extrapolation;
  scalar-not-vector representational insufficiency). Its redirect URLs were
  NOT independently verified and are not cited.

## What the source CONFIRMS

- The naive scheme itself (row labels "Use Position Index", 0…N-1, "+δ" step,
  δ=1, first=0, last=N-1): Kazemnejad's "assign a number to each time-step
  linearly" — verbatim concept match.
- Problem 1 (large values dominate): Kazemnejad "the values could get quite
  large"; MLM "the indices can grow large in magnitude". The slide's concrete
  numbers (N=1024 example) are the course's own illustration.
- Problem 2 (length ceiling): Kazemnejad "our model can face sentences longer
  than the ones in training" + "may not see any sample with one specific
  length which would hurt generalization"; the slide's example max length 256
  is course-chosen. Also consistent with the paper's motivation for choosing
  sinusoids: "may allow the model to extrapolate to sequence lengths longer
  than the ones encountered during training" (§3.5, live-verified on slide
  021's fetch).
- Problem 3 (scalar vs vector): MLM "a single number… is not used… each
  position/index is mapped to a vector"; resolution per §3.5 (same d_model).

## Figures used by this slide

- **None.** Course-original three-row strawman diagram (no published figure
  reuse found or expected for this pedagogical setup). Nothing downloaded.

## Course-authored elements

- Title/subtitle wording, δ-notation with "+δ" arrows and "Use δ=1" /
  "First…=0 , Last…=N-1" line, the three-row layout, the cyan Problems panel,
  the numeric examples (1024, 256), badge "22".

## [?] Uncertain items

- [?] Which specific tutorial (if any) the course's exact Problems wording
  derives from — the three problems are standard and each is confirmed by the
  sources above, but the wording (e.g. "Use δ=1", the 1024/256 examples) reads
  course-authored; no verbatim word-level match exists in the fetched pages.

## Corrections

- none — frame content is a consistent pedagogical strawman; both sources
  agree with every claim made.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. This source
confirms/corrects DATA and records provenance; it never licenses inventing or
"improving" content the slide doesn't show.
