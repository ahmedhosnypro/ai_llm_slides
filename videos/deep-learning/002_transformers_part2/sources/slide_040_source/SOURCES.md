# SOURCES.md — slide 040 "Normalization Parameters" (BN Algorithm 1, verbatim)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Written by the Part II web-research worker, 2026-10-11. Frame evidence of
record: `analysis/slide_040_raw.json` (read in full this run; the slide is
text/typography only — no images — so the raw's transcription is the frame
read). Web evidence: the **already-banked live fetch** of Ioffe & Szegedy
2015 (`scratch/webverify/bn_ar5iv.html`, ar5iv arXiv:1502.03167, fetched
2026-10-11 during the slide-039 verification run) — re-grepped this run, no
new WebFetch/agy spent. Sibling records: slide 039 (the covariate-shift
motivation this slide follows), slides 041–044 (P3 normalization family,
Wu & He 1803.08494).

## Slide identity

- New (curated) slide **040** ← old extraction **108** (95 frames) —
  `unique_slides/new2old_mapping.json`, frame `unique_slides/slide_040.jpg`.
- Frame facts (raw): title "Normalization Parameters" (red serif); badge
  "40". Red-bordered intro paragraph (serif, heavy inline color emphasis):
  "Instead of restricting the Activations of each layer to be strictly Zero
  mean and unit variance, Normalization allows the network to learn
  parameters γ and β that can convert the mean and variance to any value
  that Minimizes Loss." Below-left: a white algorithm panel (black border,
  LaTeX Computer-Modern styling) reproducing the paper's **Algorithm 1**
  box, with color-highlight overlays: header lines "Input: Values of x over
  a mini-batch: 𝓑 = {x_{1...m}};" / "Parameters to be learned: γ, β"
  (whole line light-green highlight) / "Output: {y_i = BN_{γ,β}(x_i)}";
  then four display equations, each with a right-aligned sans-serif comment:
  1. μ_𝓑 ← (1/m)∑_{i=1}^{m} x_i — "// mini-batch mean" (μ_𝓑 lavender)
  2. σ²_𝓑 ← (1/m)∑_{i=1}^{m} (x_i − μ_𝓑)² — "// mini-batch variance"
     (σ²_𝓑 lavender)
  3. x̂_i ← (x_i − μ_𝓑)/√(σ²_𝓑 + ε) — "// normalize" (x̂_i pink; fraction
     numerator/denominator light-blue)
  4. y_i ← γx̂_i + β ≡ BN_{γ,β}(x_i) — "// scale and shift" (y_i in an
     orange ellipse; γ, β green-highlight; x̂_i pink)
  Right half of the lower slide is empty. Bottom black letterbox band
  (video artifact, not slide content).

## Primary source

**Ioffe & Szegedy, "Batch Normalization: Accelerating Deep Network Training
by Reducing Internal Covariate Shift" (arXiv:1502.03167) — Algorithm 1
"Batch Normalizing Transform, applied to activation x over a mini-batch"**
(banked live fetch `scratch/webverify/bn_ar5iv.html`; verbatim text extracted
from it this run):

- "Algorithm 1  Batch Normalizing Transform, applied to activation x over a
  mini-batch." + "0: Values of x over a mini-batch: ℬ = {x_{1…m}};
  Parameters to be learned: γ, β" + "0: {y_i = BN_{γ,β}(x_i)}"
- "μ_ℬ ← (1/m)∑_{i=1}^{m} x_i  // mini-batch mean"
- "σ²_ℬ ← (1/m)∑_{i=1}^{m} (x_i − μ_ℬ)²  // mini-batch variance"
- "x̂_i ← (x_i − μ_ℬ)/√(σ²_ℬ + ϵ)  // normalize"
- "y_i ← γx̂_i + β ≡ BN_{γ,β}(x_i)  // scale and shift"

**Every line of the slide's algorithm panel — including the four `//`
comments and the Input/Parameters/Output header — matches the paper's
Algorithm 1 verbatim** (calligraphic 𝓑 included). The ε constant: "ϵ is a
constant added to the mini-batch variance for numerical stability" (paper,
immediately before Algorithm 1). The slide is a re-typeset of this box in
the course's own styling — it is NOT a pixel copy, so no figure download.

- Supporting §3 text (same banked fetch), behind the intro paragraph's
  claims: "we make sure that the transformation inserted in the network can
  **represent the identity transform**. To accomplish this, we introduce,
  for each activation x^(k), a pair of parameters γ^(k), β^(k), which
  **scale and shift** the normalized value… These parameters are **learned
  along with the original model parameters**, and **restore the
  representation power of the network**." + §3 opening "we will normalize
  each scalar feature independently, by making it have the mean of zero and
  the variance of 1" (the "Zero mean and unit variance" baseline the intro
  paragraph relaxes).

## What the source CONFIRMS

- The algorithm box, line by line (all four equations, all four comments,
  the Input/Parameters/Output headers, 𝓑, γ/β, ε) — Algorithm 1 verbatim.
- The γ/β mechanism ("learn parameters γ and β" that undo the strict
  normalization) — §3 verbatim (identity transform + learned parameters +
  restore representation power).
- Panel placement after slide 039's covariate-shift motivation and before
  the P3 normalization-taxonomy block (041–044): course flow, consistent
  with 039's and 043's verified Ioffe & Szegedy records.

## Course-authored elements

- The intro paragraph's WORDING — grep-verified against the banked paper
  this run: "restricting the Activations", "strictly Zero mean", "convert
  the mean and variance", "Minimizes Loss" have **0 hits** in the paper. The
  sentences are the course's own paraphrase of the §3 statements above
  ("minimizes loss" = the parameters being learned with the model).
  Keep verbatim with its inline color emphasis (blue "strictly Zero mean
  and unit variance", green-on-highlight "learn parameters γ and β", red
  underlined "convert the mean and variance to any value that Minimizes
  Loss.").
- The color-highlight overlays on the algorithm box (lavender μ/σ², pink
  x̂, light-blue fraction halves, orange y_i ellipse, green γ/β, light-green
  parameters line) and the sans-serif "//" comment styling — the paper's
  Algorithm 1 box is monochrome; all highlighting is course annotation.
- Title, red intro frame, panel geometry (left-of-center, right half
  empty), badge "40" — course layout.

## Figures used by this slide

- **None downloaded.** The algorithm panel is a re-typeset of paper
  Algorithm 1 in course styling (LaTeX-like serif, colored highlights) —
  not a reproduction of published pixels. No image asset exists to bank.

## [?] Uncertain items

- [?] Wording-provenance of the intro paragraph beyond the paper (a
  CS231n/d2l-style tutorial paraphrase may exist that the course echoes) —
  no verified published page was checked against it this run (budget);
  treated as course-authored per the 039 precedent (search-engine wording
  attributions there were contradicted by the banked text). The CLAIM is
  fully paper-confirmed; only the sentence wording is open.
- [?] exact glyph of the ε in the normalize step (raw reads "ε"; paper uses
  "ϵ") — same constant either way; build-time zoom decides the printed
  glyph.

## Corrections

- none — the raw's algorithm transcription matches the paper verbatim.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. Sources
confirm/correct DATA and record provenance; they never license inventing or
"improving" content the slide doesn't show.
