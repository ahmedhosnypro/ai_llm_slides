# SOURCES.md — slide 004 "Concept of LOSS Function"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
("Web-source research mandate", founder in-session directive 2026-10-19); method = agy web
search (MCP, `agy_web_search`) for discovery + live fetch with `curl -sL` and `pdftotext`
extraction for PDFs. Frame facts come from `analysis/slide_004_final.json`; no vision calls
were made by this worker.

## Slide identity

- File: `unique_slides/slide_004.jpg` (960x540, 1px = 1pt), badge numeral **4**.
- Founder-curated numbering (2026-10-19); `_meta.precuration_slide: 4` — the pre-curation
  provenance happened to match, so no remap applies (pre-curation index removed by founder).
- `analysis/slide_004_final.json` verdict PASS_WITH_FIXES; recreatability 8/10.
- First content slide of the loss-function topic cluster (slides 003-009).

## Primary source(s)

All URLs below were fetched live in this work window (HTTP 200; text extracted and quoted
verbatim). None recorded from an unfetched snippet.

1. **https://www.cis.upenn.edu/~cis5150/cis515-12-sl4.pdf** — University of Pennsylvania
   CIS 5150 (Fundamentals of Linear Algebra & Optimization) lecture slides, Chapter 4
   "Vector Norms and Matrix Norms". Fetched live: HTTP 200, `application/pdf`, 421385 bytes,
   8 pages; extracted with `pdftotext -layout`. This is the primary anchor for the
   norm/transpose identity.
2. **https://en.wikipedia.org/wiki/Euclidean_norm** — fetched live: HTTP 200, 466895 bytes.
   Secondary anchor for the Euclidean-norm definition.
3. **https://see.stanford.edu/materials/aimlcs229/cs229-notes1.pdf** — Stanford CS229 notes
   Part I, §1 "LS/LMS" cost function and §2.2 "Least squares revisited". Fetched live in this
   work window: HTTP 200, `application/pdf`, 235162 bytes, 30 pages. (Same source banked in
   `sources/slide_003_source/SOURCES.md`; re-verified here for the loss form.) This record adds
   the §1 cost-function quote.
4. **https://en.wikipedia.org/wiki/Ridge_regression** — fetched live in this work window:
   HTTP 200, 475413 bytes. Used for the "residual sum of squares" naming and the
   ‖Xβ̂−Y‖² form. (Banked primarily in slide 007/008 records.)

## Figures used by this slide

None. The slide's content is boxes and equations drawn in the deck's own pedagogy style
(colored red/blue/yellow-bordered rectangles) — no hosted original figure exists to save. The
source pages do host their own typeset equations (CS229's J(θ), UPenn's ‖u‖₂² = uᵀu) but
these are the source's own typesetting of standard notation, not figures the slide reuses or
redraws; no figure asset was therefore copied into this directory.

## What the source(s) CONFIRM

- **`‖a‖₂ = aᵀa` (the "Remember" box on the slide)** — CONFIRMED with one notational caveat,
  which the sources make explicit. UPenn CIS515 Ch. 4 defines, verbatim: "we have the Euclidean
  norm ‖x‖₂, defined such that, ‖x‖₂ = (|x₁|² + ··· + |xₙ|²)^{1/2}" — i.e. the 2-norm is the
  **square root** — and then states verbatim: "In particular, when u = v, in the complex case
  we get **‖u‖₂² = u*u**, and in the real case, this becomes **‖u‖₂² = uᵀu**." Wikipedia,
  Euclidean norm, verbatim: "The Euclidean norm of a vector x is ‖x‖ = √(x·x)."
  → The identity the slide is invoking (the norm's *square* equals the transpose product) is
  exactly right; the slide's shorthand drops the square on ‖·‖₂. UPenn also gives, verbatim,
  "⟨u,v⟩ = uᵀv = vᵀu" for real column vectors, which underwrites the (Y−Ŷ)ᵀ(Y−Ŷ) form below.
- **`Loss = ‖Y − Ŷ‖₂ = (Y − Ŷ)ᵀ(Y − Ŷ)` — the Residual Sum of Squares (RSS)** — CONFIRMED as
  the standard least-squares loss. Wikipedia, Ridge regression, verbatim: "RSS
  = ‖X β̂ − Y‖² … where RSS is the residual sum of squares". scikit-learn's Ridge user guide
  (fetched live in this work window at
  `https://scikit-learn.org/stable/modules/linear_model.html`, HTTP 200), verbatim: "The ridge
  coefficients minimize a penalized residual sum of squares: min_w ‖Xw − y‖²₂ + α‖w‖²₂".
- **The slide's definition "Loss function as squared distance between Ŷ and Y"** — CONFIRMED:
  this is the squared Euclidean distance of the residual vector, the textbook least-squares
  loss.
- **`Ŷ = XW` predicted, X `N×(d+1)` matrix "Given", Y `N×1` labels vector "Given", W "Model
  Parameter" "Required"** — CONFIRMED at the standard-notation level by CS229 §2.2 (design
  matrix X with intercept column; target vector ~y; parameters θ); see
  `sources/slide_003_source/SOURCES.md` for the verbatim design-matrix quote. sklearn's Ridge
  docs state the model as ‖y − Xw‖²₂ with "coefficients w of the linear model".
- **`‖a‖₂ = aᵀa`'s use in the "Remember" box alongside `Loss = (Y − Ŷ)ᵀ(Y − Ŷ)`** — the two
  equations are consistent with each other under the standard identity; the slide is teaching
  that the RSS is exactly the aᵀa form with a = Y − Ŷ.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- **The two-box pedagogical setup** ("Original Labels" red-bordered box / "Predicted Labels"
  red-bordered box; "Objective is Ŷ=Y" and "If Ŷ≠Y ⇒ There is an Error (Loss)" boxes; the
  "Define Loss function as…" salmon box above the yellow-bordered formula box) is entirely the
  instructor's teaching scaffold. No source organizes the loss concept this way.
- **"Objective is Ŷ=Y"** — a pedagogical framing statement, not a sourced theorem.
- **"W is Model Parameter → Required"** and the Given/Required tagging — course pedagogy.
- **All colors (#FF0000 red borders, #0000FF blue, #FFFF00 yellow borders, #FAEBD7 salmon
  fill, #FFFF00 badge) and the box geometry** — deck style, no source counterpart.
- **The ½ factor is NOT in this slide's loss** (`Loss = ‖Y−Ŷ‖₂ = (Y−Ŷ)ᵀ(Y−Ŷ)`) while CS229's
  J(θ) has the ½ — a convention difference, not an error. CS229 §1 verbatim: "J(θ) =
  (1/2)Σᵢ(h_θ(x⁽ⁱ⁾) − y⁽ⁱ⁾)²". Both conventions are in standard use; the deck's own
  convention is recorded and used consistently on slide 005 (which does carry the ½).

## [?] Uncertain items

- **`‖a‖₂ = aᵀa` and `Loss = ‖Y − Ŷ‖₂ = (Y − Ŷ)ᵀ(Y − Ŷ)` are shorthand for the squared norm.**
  RESOLVED (with an inline trail): the sources confirm the underlying identity is
  ‖a‖₂² = aᵀa, and that ‖a‖₂ itself is the square root (UPenn CIS515 Ch. 4; Wikipedia
  Euclidean norm). For RECREATION the frame text is rendered exactly as printed (verbatim-text
  rule; the frame wins for recreation); the understanding-level correction is recorded here
  and must not be "fixed" into the equation's rendered content.
- `analysis/slide_004_final.json`'s own open items stay frame-level and are not
  web-resolvable: exact font sizes / box dimensions / pixel coordinates; the color of the
  "Remember" header (black `#000000` assumed vs. blue `#0000FF`).

## Corrections

- **None.** Every annotation in `analysis/slide_004_final.json` that these sources can speak
  to is confirmed: Y is an N×1 (analysis writes n×1) labels vector, Ŷ = XW is the prediction,
  X is N×(d+1), W is the parameter vector, and the loss is the RSS
  ‖Y − Ŷ‖² = (Y−Ŷ)ᵀ(Y−Ŷ). No dimension, attribute, or provenance guess is contradicted.
  The norm-shorthand above is a notation-level observation about the *frame's* equation
  text, recorded for understanding; it does not contradict any model annotation.
- No edit to `analysis/*.json` was made by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
