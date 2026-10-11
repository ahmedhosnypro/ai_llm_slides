# SOURCES.md — slide 007 "Traditional RNN  Seq2Seq model / (Challenges) — [1] Bottleneck"

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via agy websearch
+ WebFetch of ar5iv HTML (no vision calls run; no image access — frame facts below
come from the verified vision pass description of 2026-10-11 and the script-12 raw
JSON).

## Slide identity

- New (curated) slide **007** ← old extraction slide **14** (founder-swapped frame;
  old group 14 was SPLIT by curation into new slides 7 and 8 — this one is the
  founder-picked earlier state, state A, kept frame `frame_00416.jpg`)
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_007.jpg`.
- Frame facts (raw JSON): slide 6's exact composition PLUS the delta: a light-blue
  rounded callout box left-middle with four bold blue centered lines —
  "[1] Bottleneck" (underlined), "The meaning of the entire input sequence  is",
  "Expected to be captured  by a single context vector" (underline on "by a single
  context vector"), "with fixed  dimensionality" (underline on "fixed
  dimensionality") — plus a second title line "(Challenges)" in blue. Mouse cursor
  over the box = recording artifact, omit on recreation.
- DEPENDS ON slide 6 (`slide_dependencies.json`: 7←6). The base diagram references
  `../slide_006_source/` (Cho Fig 1 bank); no new figures needed or downloaded.

## Primary source

- **URL**: https://ar5iv.labs.arxiv.org/html/1409.0473 (verified live 2026-10-11
  via agy + WebFetch); paper: https://arxiv.org/abs/1409.0473
- **Paper**: "Neural Machine Translation by Jointly Learning to Align and
  Translate" — Bahdanau, Cho, Bengio (ICLR 2015), arXiv:1409.0473.
- (The underlying diagram itself is Cho 2014, arXiv:1406.1078 — provenance banked
  in `../slide_006_source/SOURCES.md`.)

## Figures used by this slide

None new. The diagram is the slide-6 composition (Cho 2014 Figure 1 redraw;
`../slide_006_source/rnn_encdec.svg`). The slide's own delta is a text callout —
there is no figure behind it.

## What the source CONFIRMS (data behind the slide)

- **The "Bottleneck" word itself**: Bahdanau abstract — the authors "conjecture
  that the use of a fixed-length vector is a **bottleneck** in improving the
  performance of this basic encoder–decoder architecture". The slide's "[1]
  Bottleneck" header is the paper's own term.
- **The claim's content**: Bahdanau intro — a neural network "needs to compress
  all the necessary information of a source sentence into a fixed-length vector";
  the abstract of the same family (encoder–decoders) says they "encode a source
  sentence into a fixed-length vector from which a decoder generates a
  translation" (agy-quoted). Cho 2014 (slide 6's paper) states c is "a summary of
  the whole input sequence" with fixed dimensionality. Together these confirm the
  slide's three claims: (a) the ENTIRE input sequence's meaning, (b) captured by a
  SINGLE context vector, (c) of FIXED dimensionality.
- The callout text is course phrasing of this published critique — the DATA is
  confirmed; the wording remains the slide's.

## Course-authored elements (no paper counterpart — frame is ground truth)

- The numbered-challenge framing ("[1]", "(Challenges)" title line), the
  light-blue callout box styling, the underlined emphasis phrases, and the exact
  line breaks / double-spaces ("The meaning of the entire input sequence  is",
  "Expected to be captured  by a single context vector", "with fixed
  dimensionality") are instructor text on the FRAME. The papers phrase the same
  idea differently; do not "correct" the wording to the papers.
- Leader lines from the box to the context-vector arrow region are course-added
  annotation.

## [?] Uncertain items

- [?] Which exact words are underlined beyond what the raw JSON records ("[1]
  Bottleneck", "by a single context vector", "fixed  dimensionality" are recorded;
  underline extent is a frame fact the build worker verifies against
  `unique_slides/slide_007.jpg`).

## Corrections

none — the callout is course-authored text; the paper confirms its claims but
shows no mis-transcription; no patch applied to `analysis/slide_007_raw.json`.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout, verbatim
text, drawn content). This source confirms/corrects DATA and records provenance; it
never licenses inventing or "improving" content the slide doesn't show. If source
and slide disagree, record the discrepancy above — the slide wins for recreation,
the source wins for understanding.
