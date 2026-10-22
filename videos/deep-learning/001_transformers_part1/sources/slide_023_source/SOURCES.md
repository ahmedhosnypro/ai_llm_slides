# SOURCES.md — slide 023 "Review: Cosine Similarity"

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via WebFetch of
the reference math source (no image access — frame facts come from the script-12
raw transcription `analysis/slide_023_raw.json`).

## Slide identity

- New (curated) slide **023** ← old extraction slide **48** (diff 0.062,
  **founder frame swap**: kept frame `frame_01621.jpg`, original kept frame
  `frame_01828.jpg`) (`unique_slides/new2old_mapping.json`), frame
  `unique_slides/slide_023.jpg`.
- Frame facts (raw transcription): a math-review slide — two pale-yellow vector
  diagrams (axes, blue vector b, red vector a, green angle θ) joined by a
  red "Normalize" block arrow; white blue-bordered boxes with the normalization
  equations, the dot-product/cosine equations, and "After Normalization
  |a| = |b| = 1"; a cyan summary bar ("Cosine Similarity is between -1 , +1" /
  "It is a dot product between two Normalized vectors a and b"); bottom boxes
  "Maximize [Similarity] = Minimize -[Similarity]" and "Loss = -[Similarity]";
  badge "23"; a presenter pen-annotation artifact inside the right circle.

## Primary source

- **URL**: https://en.wikipedia.org/wiki/Cosine_similarity (verified live
  2026-10-11 via WebFetch) — reference-grade source for the standard identity
  and range facts.
- The math itself is elementary linear algebra (dot product identity) and needs
  no paper; there is no single canonical "source slide" for a cosine-similarity
  review. Contextually the slide reviews the similarity measure used by the
  attention/similarity framing of the section (the Transformer paper's
  attention is dot-product based, arXiv 1706.03762 §3.2.1 — "the dot products
  of the query with all keys").

## Figures used by this slide

- **None downloaded** — the two vector diagrams are instructor-drawn vector
  shapes (course-authored geometry), not reused figures from any publication.

## What the source CONFIRMS (data behind the slide)

All equations and stated facts on the frame are mathematically correct:

- cos(θ) = aᵀb / (|a| |b|), obtained by isolating cosine in a·b = |a||b|cos(θ);
  the source states the formula S_C(A,B) = cos(θ) = A·B / (‖A‖‖B‖).
- "Cosine Similarity is between -1 , +1" — source: "The cosine similarity always
  belongs to the interval [−1, +1]."
- After normalization (|a| = |b| = 1) the similarity equals the plain dot
  product, cos(θ) = aᵀb — the source's unit-vector discussion (normalized
  vectors reduce the denominator to 1) confirms exactly this.
- Normalized a = a/|a|, normalized b = b/|b| — standard unit-vector definition.
- "Maximize [Similarity] = Minimize -[Similarity]" and "Loss = -[Similarity]":
  arithmetically trivially correct (negation) and the standard way training
  objectives maximize a similarity by minimizing its negative.

## Course-authored elements (no source counterpart — do not "fix" to source)

- Everything visual: the two circle diagrams' geometry (b at ~60°, a at ~15°),
  the "Normalize" block arrow, the box/bar layout and colors (blue-bordered
  white boxes, cyan bar, yellow/pink bottom boxes), the bracket notation
  "[Similarity]", the phrasing "before calculate similarity" (instructor's own
  grammar — keep verbatim), and badge "23". The gray pencil icon is a
  presenter-annotation artifact (omit in a clean recreation).

## [?] Uncertain items

- [?] Exact equation rendering (fraction stacks, underlines on a/b) per the raw
  — to be honored by the build; the raw's equation strings are self-consistent.
- [?] The precise angles of a/b in the two circles (raw estimates differ left vs
  right) — layout facts only the frame can answer.

## Corrections

none — every equation and numeric claim checked against the reference source:
all correct; nothing to correct.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout, verbatim
text, drawn content). This source confirms/corrects DATA and records provenance; it
never licenses inventing or "improving" content the slide doesn't show. If source
and slide disagree, record the discrepancy above — the slide wins for recreation,
the source wins for understanding.
