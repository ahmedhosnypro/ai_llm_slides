# SOURCES.md — slide 010 "RNN  Seq2Seq model [with Attention]"

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via agy websearch
+ WebFetch of ar5iv HTML (no vision calls run; no image access — frame facts below
come from the verified vision pass description of 2026-10-11 and the script-12 raw
JSON).

## Slide identity

- New (curated) slide **010** ← old extraction slide **19** (diff 0.0)
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_010.jpg`
  (kept frame `frame_00645.jpg`).
- Frame facts (raw JSON): title "RNN  Seq2Seq model [with Attention]" (serif,
  "Attention" in blue) + subtitle "[ To overcome Bottleneck challenge]"
  ("Bottleneck challenge" blue + underlined); encoder bottom-left, decoder
  top-right with captions "Encoder" / "Decoder" (NO "(RNN)" — differs from slide
  6); two lavender attention boxes (left one above the encoder containing a small
  white "attention" node fed by thin lines from ALL THREE encoder top cells; right
  one beneath the decoder's state cells) joined by dashed pink/magenta curves;
  thick dark-red context-vector arrow encoder-red-dot → decoder-first-cell (kept
  from slide 6); green callout "weighted sum of the hidden states" (blue bold
  italic); pink callout "Context Vector (of Whole Inputs)"; gray summary box
  "Decoder Utilizes:" with bullets "Context Vector" / "Weighted sum of hidden
  states". Mouse cursor above the summary box = recording artifact, omit.
- DEPENDS ON slide 6 (`slide_dependencies.json`: 10←6) — its diagram is a
  modified re-use of the slide-6 composition; the ATTENTION delta's source is
  below.

## Primary source

- **URL**: https://ar5iv.labs.arxiv.org/html/1409.0473 (verified live 2026-10-11);
  paper: https://arxiv.org/abs/1409.0473
- **Paper**: "Neural Machine Translation by Jointly Learning to Align and
  Translate" — Bahdanau, Cho, Bengio (ICLR 2015), arXiv:1409.0473.

## Figures used by this slide

- **Figure 1** — caption (verbatim, ar5iv): "The graphical illustration of the
  proposed model trying to generate the t-th target word y_{t} given a source
  sentence (x1, x2, …, xT)."
- **Downloaded into this dir**: `rnnsearch.svg`
  (https://ar5iv.labs.arxiv.org/html/1409.0473/assets/rnnsearch.svg, 29,544
  bytes, fetched 2026-10-11) — the paper's original Figure 1. Reference for
  topology/labels; the course REDRAWS it in its own style (orange/yellow blocks,
  callout boxes). No pixel match is expected.
- The base encoder/decoder containers still reference
  `../slide_006_source/` (Cho 2014 Fig 1 bank) per the 10←6 dependency edge.

## What the source CONFIRMS (data behind the slide)

- **Attention receives ALL encoder hidden states**: Bahdanau's annotations h_j
  (j = 1…T_x) all feed the alignment model — Eq. 5 computes the context as
  "a weighted sum of these annotations": c_i = Σ_{j=1}^{T_x} α_ij h_j. The
  slide's attention box wired to all three encoder top cells, and the green
  callout "weighted sum of the hidden states", are exactly this.
- **Per-step context for the decoder**: the paper computes a FRESH c_i at every
  target word y_i (Eq. 5 is indexed by i), weighted by alignment probabilities
  α_ij = softmax(e_ij) with e_ij = a(s_{i−1}, h_j), "an alignment model which
  scores how well the inputs around position j and the output at position i
  match". The slide's two attention boxes with dashed pink curves between encoder
  side and decoder side depict this per-step weighting; the gray summary box
  ("Decoder Utilizes: Context Vector / Weighted sum of hidden states") states the
  paper's point that attention REPLACES the single fixed vector with a weighted
  sum (while the slide KEEPS the red context-vector arrow — see below).
- **The motivation line**: the paper's abstract "conjecture that the use of a
  fixed-length vector is a bottleneck" is what the slide's subtitle "[ To
  overcome Bottleneck challenge]" refers back to (slide 7's challenge).

## Course-authored elements (no paper counterpart — frame is ground truth)

- **The classic course simplification**: the slide's encoder looks UNIDIRECTIONAL
  (single h₁/h₂ chain, one hidden row) whereas Bahdanau's encoder is a
  bidirectional RNN with annotations h_j = [h→_j; h←_j] ("concatenating the
  forward hidden state and the backward one"). The slide also omits explicit
  α/e labels and the a-network internals. This is deliberate pedagogy on the
  FRAME — recreate the slide as shown; never "fix" it into the paper's
  bidirectional form.
- **The retained red context-vector arrow + pink "Context Vector (of Whole
  Inputs)" callout alongside the attention boxes**: the paper does NOT draw a
  fixed-c arrow in Figure 1 (attention's whole point is c_i varies per step);
  the course keeps it to show what the decoder previously used vs. now also
  uses. Frame wins — draw both paths exactly as shown.
- Caption change "Encoder"/"Decoder" (without "(RNN)"), the serif title block
  with blue emphasis words, the gold badge, and the gray footer strip are
  course-level chrome.

## [?] Uncertain items

- [?] Number of dashed pink attention curves (raw says "two-to-three" fan out
  from the left attention box) — frame fact; the build worker pins the count
  from `unique_slides/slide_010.jpg`.
- [?] Whether the right attention box also connects upward into the decoder's
  state cells ("a further dashed curve continuing up toward the decoder cells")
  — frame fact, verify before build.
- [?] Exact target of the green callout's connector (raw: to the left attention
  box's top-right corner) — frame fact.

## Corrections

none — the raw transcription matches the paper's mechanism where it encodes data,
and the course-authored deltas are frame-owned; no patch applied to
`analysis/slide_010_raw.json`.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout, verbatim
text, drawn content). This source confirms/corrects DATA and records provenance; it
never licenses inventing or "improving" content the slide doesn't show. If source
and slide disagree, record the discrepancy above — the slide wins for recreation,
the source wins for understanding.
