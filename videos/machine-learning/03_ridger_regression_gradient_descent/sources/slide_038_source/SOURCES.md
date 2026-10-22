# SOURCES.md — slide 038 "Gradient Descent (GD) vs Stochastic Gradient Descent (SGD)"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search + live `curl -sL` fetch of every recorded URL in the same work window that records it +
verification against the fetched page text. **This slide spent 0 new search queries** — it is a
section-divider slide whose only content is the two standard algorithm names, and every source
that defines both was already fetched live in this worker's window for slides 037/039 (see
cross-references; ECONOMY LAW honored). Frame facts come from the slide's analysis records
(`analysis/slide_038_final.json`, which exists, cross-checked against `slide_038_raw.json`); NO
vision calls were made by this worker.

**Query-budget disclosure for this worker (wave 2, slides 037–044), per the economy law:**
3 searches total, all spent on the perceptron-criterion / GD-update cluster:
1. agy MCP: "perceptron learning rule error function sum over misclassified samples gradient
   descent update rule modified weights" → led to the Illinois CS 440 and other perceptron-rule
   pages.
2. agy CLI (`agy -p`): "perceptron criterion function error sum misclassified samples gradient
   descent Duda Hart Stork" → led to the DHS Chapter-5 lecture PDF and Cornell CS 4780.
3. agy MCP: "perceptron criterion function 'sum of' misclassified samples '-w^T x' gradient
   descent update rule lecture notes" → re-confirmed the same DHS/Cornell cluster.
Everything slides 038/039/040–044 needed beyond those leads was fetched directly from canonical
known locations with no additional query.

## Slide identity

- Frame file: `unique_slides/slide_038.jpg` (960×540, 1px = 1pt per the deck AGENTS.md).
- Badge number on the frame: **38** (yellow circle, black numeral).
- Numbering resolution: founder-curated set (51 files, numbered by the founder 2026-10-19).
  Recovered pre-curation provenance in `_meta`: `source_timestamps.precuration_slide = 133`,
  kept frame `frame_04692.jpg`, t = 4691 s, `provenance: "founder-curated kept frame"`.
  Current file number 038 and badge "38" agree; pre-curation 133 is historical only.
- Analysis record used: `analysis/slide_038_final.json` (verdict PASS_WITH_FIXES,
  recreatability 9/10) — the mandate's "frame facts from the vision-analysis record" is
  satisfied by the final; the raw agrees.

## Primary source(s)

All URLs were fetched live in this work window (HTTP 200). None recorded from an unfetched
snippet.

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Gradient_descent` (also `?action=raw` wikitext, 40,753 bytes, md5 `7ccec322feaf8d35ed83b689bc2ab29a`) | Wikipedia **"Gradient descent"** — the canonical definition of GD. | **CONFIRMED** — fetched live this window; verbatim lead quoted below. |
| `https://en.wikipedia.org/wiki/Stochastic_gradient_descent` (also `action=raw` wikitext, 58,106 bytes, md5 `a0179f74b0046c7c9a1e65d9de51c7d3`) | Wikipedia **"Stochastic gradient descent"** — definition of SGD as the stochastic approximation of GD, the single-sample update, the mini-batch compromise, and the GD/SGD relationship. | **CONFIRMED** — fetched live this window; quotes below. |
| `https://cs231n.github.io/optimization-1/` (47,579 bytes, md5 `cfad649b103495ddcc77732c07930767`) | Stanford **CS231n** notes, *Optimization* — vanilla Gradient Descent → Mini-batch → SGD trichotomy with pseudocode. | **CONFIRMED** — fetched live this window; quotes below. |
| `https://scikit-learn.org/stable/modules/sgd.html` (96,457 bytes, md5 `f7b236d97a732d6bce3b51d7d4e64128`) | scikit-learn **"1.5. Stochastic Gradient Descent"** — the (batch) GD vs SGD distinction in the reference implementation's own words. | **CONFIRMED** — fetched live this window; quotes below. |

## Figures used by this slide

**None — and correctly so.** The frame hosts no figure: `imagery` holds only the badge and the
mouse cursor; `visual_elements` holds only the border and the badge. The nearest hosted
originals for either term are Wikipedia's `Gradient Descent in 2D.webm` and the SGD article's
`stogra.png` ("Fluctuations in the total objective function as gradient steps with respect to
mini-batches are taken.") — neither is reused or redrawn by this title-only slide, so nothing
was downloaded; the reason is stated here per the layout law.

## What the source(s) CONFIRM

1. **"Gradient Descent (GD)" is a standard, separately-named algorithm** — Wikipedia, verbatim:
   > "Gradient descent is a method for unconstrained mathematical optimization. It is a
   > first-order iterative algorithm for minimizing a differentiable multivariate function."

   cs231n's vanilla-GD pseudocode ("`weights_grad = evaluate_gradient(loss_fun, data,
   weights)` / `weights += -step_size * weights_grad`") is the concrete form of the same
   method. CONFIRMED.
2. **"Stochastic Gradient Descent (SGD)" is a standard, separately-named algorithm, and the
   "vs" of this slide is a recognized contrast, not a course invention** — Wikipedia
   (*Stochastic gradient descent*), verbatim:
   > "It can be regarded as a stochastic approximation of gradient descent optimization, since
   > it replaces the actual gradient (calculated from the entire data set) by an estimate
   > thereof, calculated from a randomly selected subset of the data."

   and scikit-learn, verbatim:
   > "Stochastic gradient descent is an optimization method for unconstrained optimization
   > problems. In contrast to (batch) gradient descent, SGD approximates the true gradient of
   > E(w,b) by considering a single training example at a time."

   The slide's GD-vs-SGD juxtaposition names exactly this standard distinction. CONFIRMED.
3. **The deck's sequencing** — the deck introduces GD earlier in the lecture and uses this
   slide to introduce SGD; cs231n presents the same order (Vanilla GD → Mini-batch GD → SGD as
   the extreme single-sample case), confirming the pedagogy is a natural reading of the
   standard sources, not a distortion. CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The three-line centered layout, the red/blue run coloring ("Gradient Descent" red + "(GD)"
  blue), the ~44–54 pt bold sans-serif styling, the `#F5F5F5` background + thin gray border,
  and the badge — all course-authored chrome/styling. Note the deck's own house-chrome law
  (AGENTS.md) governs the outer template for recreation regardless of the record's
  per-slide color values.
- The mouse-cursor arrow near the second title line is a screen-recording artifact, retained
  only for frame fidelity (the analysis record already flags it as such; the final record's
  brief step 7 says to include it only for frame-accurate fidelity).
- The "(GD)" / "(SGD)" parenthetical acronyms are the course's own emphasis choice; the
  sources use the full names and abbreviations SGD/GD interchangeably, none as a styled
  parenthetical.

## [?] Uncertain items

The open items in `slide_038_final.json` are all frame-local measurements with no web
resolution path (they remain `[?]` by design and must be carried into the build's uncertain
list rather than guessed as fact):

| # | Item | Resolution path |
|---|---|---|
| 1 | Exact font family ("likely Arial or Calibri") | frame-only measurement |
| 2 | Exact point sizes (~54pt / ~44pt mid-ranges of a 48–60pt source range) | frame-only measurement |
| 3 | Badge diameter (~0.4in estimate) | frame-only measurement |
| 4 | Border thickness (~2pt assumption) | frame-only measurement |

No source-based resolution exists or is needed for these; nothing from the web contradicts
them.

## Corrections

**None.** The slide carries no equations, numbers, dimensions, or provenance guesses that a
source could patch; its annotations are frame-local measurements the source cannot and must
not touch. No edit to `analysis/*.json` was made by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
