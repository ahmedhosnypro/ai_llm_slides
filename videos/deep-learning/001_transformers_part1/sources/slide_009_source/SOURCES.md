# SOURCES.md — slide 009 "Traditional RNN  Seq2Seq model / (Challenges) — [3] Very Long Sequence / Vanishing Gradient"

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via agy websearch
+ WebFetch of ar5iv HTML (no vision calls run; no image access — frame facts below
come from the verified vision pass description of 2026-10-11 and the script-12 raw
JSON).

## Slide identity

- New (curated) slide **009** ← old extraction slide **16** (diff 0.0)
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_009.jpg`
  (kept frame `frame_00551.jpg`).
- Frame facts (raw JSON): slide 6's composition with deltas — pink context-vector
  CALLOUT REMOVED (the red encoder→decoder arrow remains), blocks moved/resized;
  PLUS: blue callout "[3] Very Long Sequence" / "Vanishing Gradient" (both lines
  underlined); gray summary box "Short Sequence: RNN" / "Long Sequence: LSTM, GRU"
  / "Very Long Sequence: FAIL" (color-coded keywords); and a white/red
  BACK-PROPAGATION panel bottom-right (red brace, "Back Propagation", long
  left-pointing red arrow, a row of nabla-∇ squares growing left→right, pink
  hidden-state chain, 11 green input boxes x₀…x₁₀). Two-line "(Challenges)" title.
- DEPENDS ON slide 6 (`slide_dependencies.json`: 9←6). The base diagram references
  `../slide_006_source/` (Cho Fig 1 bank); the backprop panel is course-authored
  (see below) — no new figures needed or downloaded.

## Primary source

- **No canonical figure exists** for this slide (course-authored framing of
  standard deep-learning knowledge, per `SOURCES_MAP.md` §2).
- **Standard-DL-knowledge data behind it** (canonical citations, NOT fetched this
  pass — the claim is textbook-level and none of these are needed to confirm the
  slide's mechanism):
  - Vanishing gradient in back-propagation through time (BPTT) over long
    sequences: Bengio, Simard, Frasconi, "Learning long-term dependencies with
    gradient descent is difficult", IEEE Trans. Neural Networks 5(2), 1994.
  - LSTM gating as the remedy: Hochreiter & Schmidhuber, "Long Short-Term
    Memory", Neural Computation 9(8), 1997.
  - GRU as the other remedy: Cho et al. 2014 (already fetched, banked in
    `../slide_006_source/SOURCES.md` — the GRU was introduced there).

## What the source CONFIRMS (data behind the slide)

- **The ladder** ("Short: RNN / Long: LSTM, GRU / Very Long: FAIL"): this is the
  standard textbook treatment — plain RNNs lose gradient signal over many steps
  (Bengio et al. 1994); gated cells (LSTM 1997, GRU 2014) retain long-range
  dependencies much longer, but still degrade on very long sequences. The
  course's three-line ladder encodes exactly this progression.
- **The vanishing-gradient panel**: BPTT sends error gradients back through the
  unrolled chain (the left-pointing red arrow over the x₀…x₁₀ chain matches
  backprop against time), and the gradient signal attenuates step by step — the
  growing-∇ squares (drawn shrinking→growing left→right in the frame's reading)
  are the course's visualization of the attenuating/fading gradient. Mechanism
  confirmed as standard knowledge; the DRAWING is the course's.
- **Sutskever 2014 caveat (fetched, recorded for honesty)**: arXiv:1409.3215 —
  a deep-LSTM seq2seq claims "the LSTM did not have difficulty on long sentences"
  and "no degradation on sentences with less than 35 words". This SUPPORTS the
  ladder's middle rung (LSTM handles long better than RNN) and is NOT
  contradictory with rung 3 (the FAIL rung is about plain RNNs / extreme
  lengths, and Sutskever's model is precisely the gated-remedy side). Do not
  misquote Sutskever as evidence of failure.

## Course-authored elements (no paper counterpart — frame is ground truth)

- The numbered-challenge framing ("[3]", "(Challenges)" line), the blue callout,
  the gray summary box with its color-coded keywords, and the entire
  Back-Propagation panel (brace, arrows, ∇ squares, pink chain, x₀–x₁₀ boxes)
  are instructor visualizations. No paper draws them; the frame is ground truth.
- Removal of the pink "Context Vector (of Whole Inputs)" callout (relative to
  slide 6) and the block repositions are curation-level course edits — recreate
  as the frame shows.

## [?] Uncertain items

- [?] Nabla-square count: raw says "repeated in ~12 [?] squares of increasing
  size" while the pink chain has 11 rectangles and the green input row 11 boxes
  (x₀…x₁₀ = 11). The 12-vs-11 count stays flagged; build worker verifies against
  `unique_slides/slide_009.jpg`.
- [?] Direction reading of the ∇ progression ("increasing size left→right" per
  the raw) — frame fact; verify before build.
- [?] Slide-9 label transcription uses PLAIN digits ("o1","s1","x1",…) while
  slides 6/7/8/10 transcribe Unicode subscripts ("o₁","s₁","x₁"); the same raw's
  typography_notes says "true subscripts" and its recreation_brief step 12 says
  to verify "subscripted o/s/h/x labels". NO PATCH (no frame access this pass):
  treat labels as true subscripts per typography_notes and verify against the
  frame.

## Corrections

none — no evidenced transcription DATA error; no patch applied to
`analysis/slide_009_raw.json`. The count/X-x/subscript questions are logged as
[?], not patched.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout, verbatim
text, drawn content). This source confirms/corrects DATA and records provenance; it
never licenses inventing or "improving" content the slide doesn't show. If source
and slide disagree, record the discrepancy above — the slide wins for recreation,
the source wins for understanding.
