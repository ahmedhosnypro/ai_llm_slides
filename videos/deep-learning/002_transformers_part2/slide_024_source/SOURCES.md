# SOURCES.md — slide 024 "Suggested Positional Encoders (Rules Controlling Good Positional Encoder)"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_024_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner round 1) + live curl of two tutorial sources (no new agy
query needed — same PE family as slides 021–023; agy already confirmed the
criteria framing for the family).

## Slide identity

- New (curated) slide **024** ← old extraction **46** (kept frame
  `frame_01289.jpg`, shown t≈1233–1288 s) (`unique_slides/slides_index.json`),
  frame `unique_slides/slide_024.jpg`.
- Frame facts (vision transcript): title "Suggested Positional Encoders";
  subtitle "(Rules Controlling Good Positional Encoder)"; badge "24". The
  same three-row strawman diagram (Word 0…Word N-1 / Pos 0…Pos N-1 / 0, δ,
  2δ, 3δ, 4δ, 5δ, …, 1-δ, 1 with "+δ" arrows) retained from slide 023, now
  annotated by a bottom blue RULES box:
  - "[1] δ value should be same for Long sequence and short sequence"
    "(same positions will be encoded with same values irrespective of the
    length of the sequence)" ("same positions", "same values" underlined)
  - "[2] Range of position encoded values should NOT depend on sequence
    length" "(predefined fixed range e.g. from 0 to 1 , form -1 to 1 , ...)"
    — the slide prints "form" (typo for "from"), keep verbatim for recreation
  - "[3] Position Encoding should be a VECTOR (not scalar) and of same
    dimension as Word Embedding" "(in order to easily combine Position
    Encoding and Word Encoding vectors)"

## Primary sources

1. **Kazemnejad, "Positional Encoding in Transformers"** —
   https://kazemnejad.com/blog/transformer_architecture_positional_encoding/
   (live curl 2026-10-11, `scratch/webverify/kazemnejad_pe.html`). Verbatim
   criteria list: "**Ideally, the following criteria should be satisfied:**
   It should output a unique encoding for each time-step (word's position in
   a sentence) / **Distance between any two time-steps should be consistent
   across sentences with different lengths.** / Our model should generalize
   to longer sentences without any efforts. / **Its values should be
   bounded.** / It must be deterministic." And on the vector requirement:
   "**it isn't a single number. Instead, it's a d-dimensional vector** that
   contains information about a specific position in a sentence."
2. **Machine Learning Mastery positional-encoding tutorial** —
   https://machinelearningmastery.com/a-gentle-introduction-to-positional-encoding-in-transformer-models-part-1/
   (live curl 2026-10-11, `scratch/webverify/mlm_pe.html`): "each
   position/index is mapped to a vector"; "Transformers use a smart
   positional encoding scheme".
3. **arXiv 1706.03762v7 §3.5** (live curl 2026-10-11,
   `scratch/webverify/paper_v7.html`): "positional encodings have the same
   dimension d_model as the embeddings, so that the two can be summed" — the
   "same dimension as Word Embedding" rule; and the sinusoidal choice is the
   one that satisfies the paper's extrapolation goal ("may allow the model to
   extrapolate to sequence lengths longer than the ones encountered during
   training").

## What the source CONFIRMS (rule → source mapping)

- Rule [1] (same positions → same values regardless of length): Kazemnejad's
  "Distance between any two time-steps should be consistent across sentences
  with different lengths" + "It should output a unique encoding for each
  time-step" + "must be deterministic".
- Rule [2] (range independent of sequence length; fixed ranges 0..1 / −1..1):
  Kazemnejad's "Its values should be bounded" + "should generalize to longer
  sentences"; the concrete example ranges (0..1, −1..1) are the course's own
  examples of bounded ranges (0..1 was slide 023's failed normalization; −1..1
  is what sin/cos naturally produce — cf. slide 032's bounded −1..1 claim in
  the Part II map).
- Rule [3] (vector, same dimension as word embedding): Kazemnejad "it isn't a
  single number. Instead, it's a d-dimensional vector"; §3.5 "same dimension
  d_model as the embeddings".

## Figures used by this slide

- **None.** Course-original diagram (same family as 022/023; row 3 reused
  with the rules annotation added). Nothing downloaded.

## Course-authored elements

- The numbered [1]/[2]/[3] rules composition (the sources list criteria
  without these numbers), the parenthetical explanations, the "form -1 to 1"
  typo (keep verbatim), badge "24".

## [?] Uncertain items

- none. (The "form" typo is a frame fact, recorded above; not a transcription
  uncertainty — both the script-12 raw and the vision transcript read "form".)

## Corrections

- none — every rule is consistent with the sources; nothing to correct.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. This source
confirms/corrects DATA and records provenance; it never licenses inventing or
"improving" content the slide doesn't show.
