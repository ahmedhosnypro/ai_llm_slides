# SOURCES.md — slide 008 "Traditional RNN  Seq2Seq model / (Challenges) — [2] Sequential Processing"

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via agy websearch
+ WebFetch of ar5iv HTML (no vision calls run; no image access — frame facts below
come from the verified vision pass description of 2026-10-11 and the script-12 raw
JSON).

## Slide identity

- New (curated) slide **008** ← old extraction slide **14** (old group 14 was SPLIT
  by founder curation into new slides 7 and 8 — this one is the group's FINAL
  state, state B, kept frame `frame_00502.jpg`) (`unique_slides/new2old_mapping.json`),
  frame `unique_slides/slide_008.jpg`.
- Frame facts (raw JSON): slide 6's composition PLUS the delta: a light-blue
  callout box left-middle — "[2] Sequential Processing" (underlined) / "Can NOT do
  processing in Parallel" — and two small light-blue boxes "Wait / Till Processing
  X₁" and "Wait / Till Processing X₂" with blue leader lines down to the h₁ and
  h₂ arrows, plus the "(Challenges)" second title line. Scissors-shaped cursor at
  the callout's right edge = recording artifact, omit on recreation.
- DEPENDS ON slide 6 (`slide_dependencies.json`: 8←6). The base diagram references
  `../slide_006_source/` (Cho Fig 1 bank); no new figures needed or downloaded.

## Primary source

- No canonical paper figure exists for this slide (course-authored framing, per
  `SOURCES_MAP.md` §2). The mechanism it teaches is standard and is evidenced by:
- **Sutskever, Vinyals, Le 2014** (arXiv:1409.3215, verified live 2026-10-11):
  §2 "the LSTM maps the input sequence to a vector of a fixed dimensionality"
  given by the last hidden state — a sequentially-accumulating single vector; and
  the seq2seq literature's encoder reads the input symbol by symbol (Cho 2014,
  `../slide_006_source/SOURCES.md`) — recurrence is inherently serial: step t
  needs state t−1 (the paper equations h⟨t⟩ = f(h⟨t−1⟩, x⟨t⟩) make the
  dependency explicit).
- **Bahdanau, Cho, Bengio 2014** (arXiv:1409.0473, verified live): the same
  fixed-length-vector architecture critique that motivates slides 7 and 10.

## Figures used by this slide

None new. Diagram = slide-6 composition (Cho 2014 Fig 1 redraw;
`../slide_006_source/rnn_encdec.svg`). The delta is text callouts — no figure
behind them.

## What the source CONFIRMS (data behind the slide)

- **The sequential-processing claim**: in the encoder-decoder family (Cho 2014;
  Sutskever 2014), the input is consumed one symbol at a time through a recurrent
  chain — hidden state h⟨t⟩ is a function of h⟨t−1⟩ — so step t literally
  waits for step t−1 and the encoder CANNOT process x₁, x₂, x₃ in parallel. This
  is exactly the slide's "[2] Sequential Processing / Can NOT do processing in
  Parallel" and its "Wait Till Processing X₁/X₂" boxes tied to the h₁/h₂ arrows.
- (Context: removing this constraint is the Transformer's selling point — arXiv
  1706.03762, already banked in `../slide_18_source/` — the course then presents
  attention/transformers as the fixes. Not slide data; background only.)

## Course-authored elements (no paper counterpart — frame is ground truth)

- The numbered-challenge framing ("[2]", "(Challenges)" line), the callout
  wording ("Can NOT do processing in Parallel" with that capitalization, "Wait /
  Till Processing" boxes), the light-blue styling, the leader-line placement, and
  the badge chrome are instructor additions. The papers never draw "Wait" boxes;
  the frame is ground truth for all of it.
- [?] The raw transcribes the Wait boxes with an UPPERCASE X ("X₁", "X₂") while
  every diagram label on the same slide (and slides 6/7/10) uses lowercase x
  ("x₁"). Both Wait-box transcriptions agree with each other, but the mixed case
  is suspicious. NO PATCH: no evidence overrides the frame's own text — the build
  worker must check `unique_slides/slide_008.jpg` and keep exactly what is printed
  (uppercase X as transcribed, unless the frame shows lowercase).

## [?] Uncertain items

- [?] Uppercase "X" vs lowercase "x" in "Wait / Till Processing X₁" and "X₂" (see
  above; frame-verifiable, not source-verifiable).
- [?] Underline extent on "[2] Sequential Processing" (recorded as underlined;
  verify against the frame).

## Corrections

none — no evidenced transcription DATA error; no patch applied to
`analysis/slide_008_raw.json`. The X/x question is logged above, not patched.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout, verbatim
text, drawn content). This source confirms/corrects DATA and records provenance; it
never licenses inventing or "improving" content the slide doesn't show. If source
and slide disagree, record the discrepancy above — the slide wins for recreation,
the source wins for understanding.
