# SOURCES — slide 28 — "Self Attention Mechanism (Not Sensitive to Words Order)"

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: 2026-10-11. The course notation quoted below is the
recreation target — kept VERBATIM. The paper is the semantic reference only.

## 1. Source URLs

- Vaswani, A. et al. (2017), "Attention Is All You Need", arXiv:1706.03762v7 —
  https://arxiv.org/html/1706.03762v7 — §3.2.1 (eq. 1) and §3.5 "Positional
  Encoding" (fetched 2026-10-11).
- Peter Bloem, "Transformers from scratch" — https://peterbloem.nl/blog/transformers
  (basic self-attention section: output depends on inputs only through pairwise dot
  products — no order term).

## 2. Downloaded figures

- None (course-original diagram; the subtitle's X4, X2, X1, X3 shuffle is
  course-illustrative).

## 3. Course notation → paper mapping

- Course "Sequential nature of the input is IGNORED" ≡ eq. (1) contains no
  position-dependent term: softmax(QK^T)V is permutation-equivariant in the input
  ordering — reordering input rows reorders output rows but changes no weight value
  (w'_ij = x_i^T x_j is pairwise; softmax is over the set).
- Course "Mitigated Later with Positional Encoder" ≡ §3.5: "Since our model
  contains no recurrence and no convolution, … we must inject some information
  about the relative or absolute position of the tokens in the sequence"
  (positional encodings added to the input embeddings).

## 4. What the sources CONFIRM

- Attention without positional encoding is order-blind (a set operation) —
  confirmed by eq. (1)'s structure and by §3.5's explicit motivation.
- The mitigation IS the positional encoder — confirmed by §3.5.
- The slide's demonstration (same diagram mechanics with the word order shuffled to
  X4, X2, X1, X3) illustrates exactly the paper-implied property: permuting which
  word sits where does not change the operation or the weight values.

## 5. Course vs paper discrepancies (NOT defects — recreation keeps course notation)

- Course defers the fix ("Mitigated Later with Positional Encoder"); the paper
  includes positional encodings in the architecture from §3.1 onward. Sequencing
  difference only.
- The specific shuffle order (X4, X2, X1, X3) is a course illustration choice —
  nothing in the source fixes it; recreation keeps the transcript's order verbatim.

## 6. Numeric verification

- n/a (0/0) — no worked example on this slide.

## 7. Open questions

- none.

## Corrections

Cross-checked against script-12 raw transcription (correction worker W-F resumption,
2026-10-11): none — consistent.

- All course labels match the established notation verbatim: Similarity / Dot Product /
  Probabilities / Soft max (rotated, two words) / Weighted SUM, W₂₁–W₂₄ (subscripted),
  Σ, Y, badge "28", and the annotations "Sequential nature of the input is IGNORED" /
  "Mitigated Later with" / "Positional Encoder".
- The shuffled subtitle "(Self Attention of word X₂ w.r.t All words in Sentence (
  X₄, X₂, X₁, X₃ )" is transcribed verbatim (unclosed-paren pattern kept) and agrees
  with the raw's bottom token row order (X₄, X₂ highlighted, X₁, X₃); the left/right
  embedding stacks read X₄, X₃, X₂, X₁ top-to-bottom (transcript-faithful; kept as
  transcribed for recreation).
- No attention formulas are printed on this slide (only symbolic diagram labels) —
  nothing to check against the course formula set. No softmax numbers — n/a (0/0).
- No [?] items in the raw. No patches.
