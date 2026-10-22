# SOURCES.md — slide 003 "Matrix Notation for Linear Regression and Classification (N- Samples)"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
("Web-source research mandate", founder in-session directive 2026-10-19); method = agy web
search (MCP, `agy_web_search`) for discovery + live fetch with `curl -sL` / `pdftotext`
extraction for PDFs (WebFetch timed out on these hosts, so curl was the fetch tool of
record). Frame facts come from `analysis/slide_003_final.json`; no vision calls were made by
this worker.

## Slide identity

- File: `unique_slides/slide_003.jpg` (960x540, 1px = 1pt), badge numeral **3**.
- Founder-curated numbering (2026-10-19); no pre-curation remap applies (pre-curation index
  intentionally removed by the founder).
- `analysis/slide_003_final.json` verdict PASS_WITH_FIXES; recreatability 9/10.
- This slide is ALSO the deck's measured house-chrome reference frame (deck AGENTS.md:
  "measured from `unique_slides/slide_003.jpg` and verified constant across 001/005/009/018/040")
  — but the analysis JSON records a #FFFFFF background with gray #808080 box borders, which is
  this slide's *content* style, not the house chrome the builders use. Noted for the record;
  no source is involved.

## Primary source(s)

All four URLs below were fetched live in this work window (HTTP 200; text extracted and
quoted verbatim below). None recorded from an unfetched snippet.

1. **http://cs229.stanford.edu/notes/cs229-notes1.pdf** — served live at
   `https://see.stanford.edu/materials/aimlcs229/cs229-notes1.pdf` (the Google-redirected URL
   resolved here via `curl -sL`); Stanford CS229 Lecture Notes Part I "Linear Regression",
   **Section 2.2 "Least squares revisited"** and **Section 2 "The normal equations"**. Fetched
   live: HTTP 200, `application/pdf`, 235162 bytes, 30 pages; text extracted with `pdftotext
   -layout`. This is the primary anchor for the design-matrix convention and the normal
   equations.
2. **https://www.di.fc.ul.pt/~jpn/r/PRML/chapter3.html** — a worked-notes page for
   Christopher M. Bishop, *Pattern Recognition and Machine Learning* (PRML) Chapter 3,
   "Linear Basis Models (section 3.1)" and "Regularization (section 3.1.4)". Fetched live:
   HTTP 200, 853620 bytes. Used as the secondary anchor for the φ₀=1 convention and the
   design-matrix/closed-form statements.
3. **https://en.wikipedia.org/wiki/Ridge_regression** — fetched live: HTTP 200, 475413 bytes.
   Used for the ridge-closed-form and multicollinearity/near-singular claims (banked in the
   records for slides 007/008; cross-referenced there).
4. **https://en.wikipedia.org/wiki/Numerical_methods_for_linear_least_squares** — fetched
   live: HTTP 200, 133630 bytes. Used for inversion-cost/conditioning claims (cross-referenced
   in slide 007's record).

Sibling-record cross-references (no new query spent): the course/CSAI provenance is
origin-level in `sources/slide_001_source/SOURCES.md`.

## Figures used by this slide

None. The slide's matrices, boxes, arrow and badge are **course-authored vector diagrams
drawn in the deck's own style** — no hosted original figure exists to save. The CS229 notes
PDF contains its own layout of the design matrix (its §2.2 matrix page) but that is the
source's own typesetting of the same standard notation, not a figure the slide reuses or
redraws pixel-for-pixel; per the economy/figures rule it was therefore not downloaded as a
slide figure. (The PDF itself is recorded in the fetch log above and remains available at the
cited URL; it was not copied into this directory because no figure asset on it is reused by
the frame.)

## What the source(s) CONFIRM

- **Design-matrix convention `X_{N×(d+1)}` with N samples and an extra column for the
  intercept ("bias"), and `W` a `(d+1)×1` weight vector** — CONFIRMED, CS229 notes1 §2.2,
  verbatim: "define the design matrix X to be the **m-by-n matrix (actually m-by-n + 1, if we
  include the intercept term)** that contains the training examples' input values in its
  rows". With the deck's symbols (N samples, d features) this is exactly N×(d+1) for X and
  (d+1)×1 for W, including the leading b/w₀ entry. The same PDF's matrix shows the design
  matrix rows as the sample inputs and θ as the parameter column.
- **The first column of the design matrix is all 1s** (the slide's expanded matrix, whose
  first column is "all 1s") — CONFIRMED, PRML chapter 3 notes, verbatim: the linear model
  "y(x,w) = w₀ + w₁x₁ + … + wₙx_N" is written with basis functions where
  "**by convention, φ₀(x) = 1**", and the corresponding page states "**the design matrix
  such that Φᵢⱼ = φⱼ₊₁(xᵢ)**" — i.e. the constant basis occupies the first column. (CS229 names
  this extra column "the intercept term"; PRML names it the bias basis φ₀=1.)
- **Compact matrix form `Y = XW` with X the matrix, Y the labels vector** — CONFIRMED at the
  standard-notation level: CS229 §2.2 rewrites the least-squares objective in "matrix-vectorial
  notation" with the design matrix X and target vector ~y; the normal-equations derivation is
  carried out entirely in that Xθ / ~y compact form.
- **Single-sample form `y = wᵀx`** (the slide's "Remember y = W^T X = X^T W") — CONFIRMED,
  PRML chapter 3 notes, verbatim: the linear model is "y(x,w) = w₀ + w₁x₁ + …", and with the
  basis convention the closed-form line is written in the notes' matrix-vector notation. The
  linear-model-as-dot-product convention `y = wᵀφ(x)` is Bishop PRML §3.1's own opening.
- **`Y_{N×1}` is the labels/target vector** — CONFIRMED: CS229 uses "~y" (the vector of
  training outputs y⁽¹⁾…y⁽ᵐ⁾) throughout §2.2/§2; PRML's notes use `y` as "the training data
  output" in `w_ML = (ΦᵀΦ)⁻¹Φᵀy`.
- **Column labels `X_1…X_n` for features/samples and `y_1…y_n` for labels** — CONFIRMED as
  standard indexing: CS229's construction has "the (i, j) entry of this matrix … given by the
  (i, j)-entry of Bᵀ", i.e. rows are the samples x⁽ⁱ⁾, and the target vector is indexed
  y⁽ⁱ⁾. The slide's specific colouring of X₁ (yellow), X₂ (cyan), X_n (pink) and the red label
  colouring are course-authored (see below).

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- **"In General: N >>> d"** — the slide's own statement. Both fetched sources assume the
  standard least-squares setting but neither asserts "N >>> d" as a general fact; it is the
  instructor's framing for this lecture (and it matters for the *later* slides' problems —
  see slide 007's record). Do not treat it as a sourced theorem; do not remove it.
- **The colored headers X₁ (#FFFF99 yellow), X₂ (#CCFFFF cyan), X_n (#FFC0CB pink)** and the
  **red labels "N Training Samples", y₁…y_n** — pure course pedagogy/recolouring; no source
  counterpart.
- **"Remember" / "In General" box styling, the blue black-box border colors, the gray arrow**
  — deck pedagogy furniture.
- **The two-layer presentation (matrix diagram → expanded bracketed equation → compact form)**
  and the underlining of W, X, Y in the "Y = XW" lines — course-authored notation emphasis,
  not a source convention.
- **`(N- Samples)` hyphen in the title** — course-authored frame text.

## [?] Uncertain items

- `analysis/slide_003_final.json`'s own open items remain frame-level, not web-resolvable:
  the reconstructed `subtitle_or_header` ("N Training Samples" is the side label, not a real
  subtitle); the title font-size estimate (30-34pt); whether the three box borders are
  #808080 (inferred, never explicitly labelled in the analysis).
- No web-resolvable [?] remained on this slide after the CS229/PRML fetches.

## Corrections

- **None required.** Every annotation in `analysis/slide_003_final.json` that the sources can
  speak to is confirmed: X is N×(d+1) with the leading all-ones column, Y is N×1, W is
  (d+1)×1, and `y = WᵀX` / `Y = XW` are the standard forms. No dimension annotation,
  attribute guess, or provenance guess is contradicted.
- Precisely because "N >>> d" is not asserted by any fetched source, it is recorded above as
  course-authored rather than treated as a discrepancy needing a patch — the frame text
  stands and no annotation is wrong.
- No edit to `analysis/*.json` was made by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
