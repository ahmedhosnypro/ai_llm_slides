# SOURCES.md — slide 010 "Overfit vs. Generalized Model Fits" [derived catalog title — no title text appears on the frame; not rendered]

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search (MCP `agy_web_search`; CLI fallback `agy -p` was verified working and used for token
check) + live `curl -sL` fetch of each URL in the same work window that records it +
independent local re-derivation of the slide's numbers against the closed form. Frame facts
come from the slide's vision-analysis record (`analysis/slide_010_final.json`); NO vision
calls were made by this worker (no `scripts/16_vision_gate.sh`, no vision model). Effort:
2 search queries for the whole 010–018 cluster (see economy-law note at the end of this
section) — this slide spent 0 additional queries beyond the cluster's shared first query.

## Slide identity

- Frame file: `unique_slides/slide_010.jpg` (960×540, 1px = 1pt per the deck AGENTS).
- Badge number on the frame: **10** (yellow circle, black numeral). Deck rule (measured
  house chrome, AGENTS.md): badge numeral = the file number N, no zero-padding.
- Numbering resolution: this deck is 51 founder-curated files numbered by the founder
  2026-10-19; the founder removed the pre-curation index/mapping, and the pre-curation
  state is intentionally unrecoverable. For this slide a recovered pre-curation
  provenance value IS present in the analysis `_meta`:
  `source_timestamps.precuration_slide = 16` (kept frame `frame_00593.jpg`, t = 592 s,
  `provenance: "founder-curated kept frame"`). So this slide is one of the 35 with
  recovered provenance; it is NOT in the 16-slide "honestly unrecoverable" list
  (1,2,3,13,24-29,33,35,36,43,44,47). Current file number 010 and badge "10" agree; the
  pre-curation number 16 is historical provenance only and must not be used for the badge.
- Analysis record used: `analysis/slide_010_final.json` (verdict PASS_WITH_FIXES,
  recreatability 7). `slide_010_raw.json` not needed (final exists).

## Primary source(s)

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Overfitting` | Wikipedia article **"Overfitting"** — sections *Statistical inference*→*Regression*, *Machine learning*→*Consequences*, *Remedy*, *Underfitting*. The article's own Figures 1 & 2 are the hosted originals for the overfit-vs-generalized contrast. | **CONFIRMED** — fetched live 2026-10-20 in this work window via `curl -sL --max-time 60 -A "Mozilla/5.0" "https://en.wikipedia.org/w/index.php?title=Overfitting&action=raw"` (25,959 bytes of wikitext) plus the rendered HTML page. Quotes below are verbatim from the fetched wikitext. |
| `https://en.wikipedia.org/wiki/Ridge_regression` | Wikipedia article **"Ridge regression"** (incl. its *Tikhonov regularization for linear equations* section) — the regularization remedy the deck arrives at from slide 014 onward. | **CONFIRMED** — fetched live 2026-10-20, same window, `action=raw` wikitext (35,436 bytes) + rendered HTML (475,413 bytes). |
| `https://en.wikipedia.org/wiki/Tikhonov_regularization` | Wikipedia article "Tikhonov regularization" | **CONFIRMED, resolves as a redirect**: live fetch returned `#REDIRECT [[Ridge regression#Tikhonov regularization]]` (180 bytes). RESOLVED final URL = `https://en.wikipedia.org/wiki/Ridge_regression#Tikhonov_regularization_for_linear_equations`. Content is the Ridge-regression article's section of that name. Not a separate article — recorded so no future worker treats it as one. |

Nothing above was recorded from an unfetched search snippet.

## Figures used by this slide

Two figures hosted by the "Overfitting" article were downloaded into this directory
exactly as served (original filenames preserved) and hash-verified by an independent
second fetch:

- `Overfitting.svg` — the article's **Figure 1**. Its verbatim caption, quoted from the
  fetched wikitext: *"Figure 1. The green line represents an overfitted model and the
  black line represents a regularized model. While the green line best follows the
  training data, it is too dependent on that data and is likely to have a higher error
  rate on new unseen data, illustrated by black-outlined dots, compared to the black
  line."* 41,460 bytes, md5 `db37833e49868db18f8ea4cd87ff5ede`. Re-fetch byte-identity:
  **IDENTICAL**.
- `Pyplot overfitting.png` — the article's **Figure 2**. Its verbatim caption: *"Figure 2.
  Noisy (roughly linear) data is fitted to a linear function and a polynomial function.
  Although the polynomial function is a perfect fit, the linear function can be expected
  to generalize better: If the two functions were used to extrapolate beyond the fitted
  data, the linear function should make better predictions."* 108,345 bytes, 1637×1253 px
  RGBA, md5 `98a6ab56b7bab5ae09773c820e92c148`. Re-fetch byte-identity: **IDENTICAL**.

**Provenance note — these figures are NOT reused or redrawn by slide 010.** The slide's
construction is two side-by-side scatter panels (gray grid, ~12 orange data points, one
blue fitted line per panel, red dashed verticals + green dashed horizontals as residual
projections, red axis arrowheads, a bright-green x-axis marker, a mouse-pointer cursor in
the left panel only, and a two-line caption under each panel). Neither hosted figure
shows scatter points with residual projection lines. They are banked here as
reference-grade ground truth for the **concept and palette family only** — do not treat
them as the slide's figure or as a pixel/layout reference. No other hosted original
exists for this slide's figure; the slide's two-panel scatter construction is
course-authored (see next section).

Palette forensics on the banked originals (per the source-research palette law): both
hosted figures ARE colored, not grayscale — `Pyplot overfitting.png` is white background
with red `#FF0000`, green `#008000`, matplotlib default blue `#1F77B4`, a light-gray
`#D4D4D4` grid and black axes (1,174 distinct RGB colors); `Overfitting.svg` uses
`#0006FF` (blue), `#FF0000` (red), `#FF3C3C`, `#5B92FF` and `#00AD6A` (green) on white.
The family (gray grid + red + green + blue line) matches slide 010's own palette
(`#D3D3D3` grid, `#FF0000` dashed verticals, `#008000` dashed horizontals, `#0000FF`
fitted line), which is evidence the instructor's source figure was matplotlib-generated
in the same idiom — but the slide's orange `#FFA500` data points, the bright-green
`#00FF00` x-axis marker and the mouse cursor have NO counterpart in either hosted figure
and are therefore course-added.

## What the source(s) CONFIRM

1. **The core concept pair on the slide** — "minimize the residuals only" ⇒ overfit;
   "residuals are not minimized" ⇒ generalizes. Source, verbatim (*Overfitting*,
   *Regression* / definitional passage):
   > "Generally, a learning algorithm is said to overfit relative to a simpler one if it
   > is more accurate in fitting known data (hindsight) but less accurate in predicting
   > new data (foresight)."
   and
   > "overfitting occurs when a model begins to 'memorize' training data rather than
   > 'learning' to generalize from a trend."
   This is exactly the slide's left/right caption pair: the left fit drives the training
   residuals to a minimum ("try to minimize the residuals ONLY") and the right fit does
   not ("Residuals are not minimized").
2. **"Fails to detect the Pattern" / "Successes to detect the Pattern"** — the verbatim
   caption of the article's Figure 2 (quoted in full in the Figures section above) states
   the same contrast in the source's own words: *"Although the polynomial function is a
   > perfect fit, the linear function can be expected to generalize better"*. The slide's
   spelling "Successes" is verbatim frame text and is preserved — it is not corrected to
   "succeeds".
3. **Why a fit that minimizes residuals is the overfitted one** — *Overfitting*,
   *Consequences*: "The most obvious consequence of overfitting is poor performance on the
   validation dataset." and the *Machine learning* section: "In this process of
   overfitting, the performance on the training examples still increases while the
   performance on unseen data becomes worse." This confirms the slide's pedagogical
   direction (left = training-residual-minimal, right = generalization-preserving).
4. **The remedy direction the deck takes after this slide** — *Overfitting*, *Remedy*:
   "To lessen the chance or amount of overfitting, several techniques are available
   (e.g., model comparison, cross-validation, regularization, early stopping, pruning,
   Bayesian priors, or dropout). The basis of some techniques is to either (1) explicitly
   penalize overly complex models…". This is the documented bridge from this slide to the
   ridge-regularization loss of slides 014–018, whose closed form the Ridge-regression
   article confirms verbatim (see slide 015's SOURCES.md).
5. **Terminology** — "overfit", "generalize(generalization)", "training data", "pattern".
   All are standard usages confirmed by the source; the slide uses them in the same sense.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The two-panel scatter-with-residual-projections construction itself (the course's own
  figure; neither hosted article figure is a redraw of it).
- All four caption strings verbatim: "Overfit (try to minimize the residuals ONLY)",
  "Fails to detect the Pattern", "Generalized (Residuals are not minimized)", "Successes
  to detect the Pattern" — including the non-standard "Successes" and the ALL-caps
  "ONLY".
- The mouse-pointer cursor (white fill, black outline) in the left panel only, and the
  absence of a cursor in the right panel — a live-presentation capture artifact, not slide
  content. (The analysis record's own uncertain-items list already flags it as an
  artifact.)
- Every numeric/geometric particular of the plot: ~12 data points per panel, the
  positive-trend scatter, the fitted lines' intercept/slope, one red dashed vertical and
  one green dashed horizontal per point, the bright-green x-axis marker, the light-gray
  `#D3D3D3` grid, the `#F5F5F5` background the vision record reports, and the panel
  x-splits (left ~4–48%, right ~52–96%).
- No slide title exists on the frame; the derived title "Overfit vs. Generalized Model
  Fits" is a catalog label from the analysis record and must NOT be rendered.
- **Chrome note (deck law, not a research finding):** the vision record reports
  background `#F5F5F5`, while this deck's measured house chrome (AGENTS.md, "House
  chrome — THIS deck") mandates a white `FFFFFF` canvas. Frame-vs-house-rule is settled by
  the deck AGENTS' house-chrome law, which overrides per-slide analysis values for the
  outer template. Recorded here only so no builder mistakes the `#F5F5F5` in the analysis
  JSON for a source fact — it is neither.

## [?] Uncertain items

Each is frame-local geometry with no source counterpart (the sources confirm the concept,
not these pixel-level particulars). None can be resolved from any web source; all remain
`[?]` and must be carried forward into the build's uncertain list rather than guessed as
fact:

| # | Item | Resolution path |
|---|---|---|
| 1 | Exact data-point count per panel ("approximately 12") | frame-only measurement (no hosted original to count) |
| 2 | Exact count of red dashed vertical / green dashed horizontal projection lines (the record's one-line-per-point reading is an interpretation, flagged as such by the validator) | frame-only measurement |
| 3 | Fitted-line intercept and slope in each panel (only "positive slope" and "left ≠ right" are known) | frame-only measurement |
| 4 | Panel border presence/color | frame-only measurement (the record omits borders) |
| 5 | Caption text alignment (assumed centered) | frame-only measurement |
| 6 | Position of the bright-green x-axis marker along the x-axis | frame-only measurement |
| 7 | Whether the vision record's `#F5F5F5` background is a frame fact or a tone artifact | deck house-chrome law (white canvas) governs the recreation; recorded, not resolved |

## Corrections

**None.** The slide carries no equations, no numeric model values, no dimension
annotations and no provenance guesses that a source could patch. The analysis record's
model annotations (chart types, color hexes, count qualifiers, region percentages) are
all frame-local measurements, and the record already marks the fuzzy ones as
"approximate/inferred in source" — which is the honest state. Nothing in the sources
contradicts any transcribed frame text, so no patch is proposed. Per the mandate,
corrections patch model annotations only; no analysis JSON was edited by this worker in
any case.

## Law reminder

The frame wins for recreation; the source wins for understanding. Discrepancies above are
recorded, never silently applied.
