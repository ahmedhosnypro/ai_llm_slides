# SOURCES.md — slide 040 "Training of Linear Regression Model / usnig SGD / Solved Example"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search + live `curl -sL` fetch of every recorded URL in the same work window that records it +
verification against the fetched page text. **This slide spent 0 new search queries** — it is a
section-divider announcing a course worked example; its claim is only that training a linear
model with SGD is a standard thing, fully covered by the cluster's already-fetched sources
(cross-referenced below per the ECONOMY LAW; worker query disclosure in
`sources/slide_038_source/SOURCES.md`). Frame facts come from `analysis/slide_040_raw.json`; NO
vision calls were made by this worker.

## Slide identity

- Frame file: `unique_slides/slide_040.jpg` (960×540, 1px = 1pt per the deck AGENTS.md).
- Badge number on the frame: **40** (yellow circle, black numeral; `labels` include "40").
- Numbering resolution: founder-curated set (51 files). Recovered pre-curation provenance in
  `_meta`: `source_timestamps.precuration_slide = 138`, kept frame `frame_04835.jpg`,
  t = 4834 s, `provenance: "founder-curated kept frame"`. Current file number 040 and badge
  "40" agree; pre-curation 138 is historical only.
- Analysis record used: `analysis/slide_040_raw.json` (no `_final.json` yet; not
  dependency-gated).

## Primary source(s)

All URLs were fetched live in this work window (HTTP 200). None recorded from an unfetched
snippet. All are origin-level carry-overs from the slides 037/038/039 fetches — no new query
spent.

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://scikit-learn.org/stable/modules/sgd.html` | scikit-learn **"1.5. Stochastic Gradient Descent"** — SGD is "a simple yet very efficient approach to fitting linear classifiers and regressors"; the per-example update rule; the efficiency claim. | **CONFIRMED (origin-level)** — fetched live this window, 96,457 bytes, md5 `f7b236d97a732d6bce3b51d7d4e64128`; quotes banked in `sources/slide_039_source/SOURCES.md`. |
| `https://en.wikipedia.org/wiki/Stochastic_gradient_descent` | Wikipedia **"Stochastic gradient descent"** — the per-sample gradient update for linear models, the least-squares case, and SGD's use "since at least 1960 for training linear regression models, originally under the name ADALINE". | **CONFIRMED (origin-level)** — fetched live this window, `action=raw` 58,106 bytes, md5 `a0179f74b0046c7c9a1e65d9de51c7d3`; quotes banked in `sources/slide_039_source/SOURCES.md`. |
| `https://en.wikipedia.org/wiki/Perceptron` | Wikipedia **"Perceptron"** — the single-sample update the worked example actually executes (see slide 042's record). | **CONFIRMED (origin-level)** — fetched live this window; quotes banked in `sources/slide_037_source/SOURCES.md`. |
| `https://www.ccs.neu.edu/home/vip/teach/MLcourse/2_GD_REG_pton_NN/materials/DHS_liniar_disc_intro_perceptron.pdf` | DHS Ch. 5 teaching PDF — single-sample correction rule + convergence conditions behind the worked example. | **CONFIRMED (origin-level)** — banked byte-identical at `sources/slide_037_source/DHS_liniar_disc_intro_perceptron.pdf` (md5 `47235972a70be5152744c50b8a64f77d`), fetched live this window. |

## Figures used by this slide

**None — and correctly so.** This is a title-only divider (title + subtitle + "Solved Example"
+ badge + a recording-artifact pointer icon); no figure exists on the frame and no source
figure is reused. The worked example it announces (slides 041–044) is course-authored — its
data table, scatter plot, and computation stacks have no hosted counterpart. Reason stated per
the layout law.

## What the source(s) CONFIRM

1. **The claim implied by the title — that a linear model can be trained with SGD, as a
   standard, worked-example-worthy procedure** — scikit-learn, verbatim:
   > "Stochastic Gradient Descent (SGD) is a simple yet very efficient approach to fitting
   > linear classifiers and regressors under convex loss functions ..."

   and its update rule (the per-sample step the example executes):
   > "The algorithm iterates over the training examples and for each example updates the model
   > parameters according to the update rule given by w ← w − η[α ∂R(w)/∂w + ∂L(w^T x_i + b,
   > y_i)/∂w]"

   CONFIRMED.
2. **Training a linear model one sample at a time is historically standard, not a course
   novelty** — Wikipedia (*Stochastic gradient descent*), verbatim:
   > "Stochastic gradient descent has been used since at least 1960 for training linear
   > regression models, originally under the name ADALINE."

   and the least-squares per-sample gradient form:
   > "... we can write ∇_w Q_i(w) = −q(x_i'w) x_i ... In least squares, q(x_i'w) = y_i − x_i'w"

   CONFIRMED — the same single-sample structure the deck's example uses for its linear
   discriminant.
3. **The "Solved Example" that follows (slides 041–044) executes a standard algorithm** — it
   trains the linear discriminant W by the single-sample update of slide 039/037 with the
   deck's δ_i sign convention, keeping the weight whenever the sample is already correctly
   classified ("Keep same Weight"). Both halves are confirmed by the banked sources
   (Wikipedia perceptron update; Illinois "If y' = y, do nothing"; DHS Algorithm 4). See
   `sources/slide_042_source/SOURCES.md` for the point-by-point record.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The title wording itself — "Training of Linear Regression Model" — is the course's own
  naming for a worked example that actually trains a **linear discriminant / classifier**
  (binary classes C₁/C₂ with a sign decision and a perceptron-criterion style update, as the
  following slides show). No source dictates the title; the frame's wording is preserved
  verbatim for recreation (its spelling "usnig" in the subtitle is likewise frame text).
- The pointer/pen icon at bottom-center, the three-line centered layout, the red/blue/red
  color split, and the badge — course chrome/artifacts.
- All numbers, data, and step-by-step computations of the announced example (slides 041–044)
  — instructor-authored; recorded as course elements in those records, never "fixed" toward
  any source.

## [?] Uncertain items

- None web-resolvable. The frame-local items (exact point sizes ~44pt/36pt, font family
  "likely Calibri or Arial", the pointer icon's identity) are frame-only measurements carried
  as `[?]` into the build's uncertain list; no source speaks to them.

## Corrections

**None.** No dimension annotation, attribute guess, or provenance guess in
`analysis/slide_040_raw.json` is contradicted by the fetched sources; transcribed frame text
(including "usnig") stays verbatim. No edit to `analysis/*.json` was made by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
