# SOURCES.md — slide 017 "Adding Ridge Regularizer to the model  λ=3"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search (MCP `agy_web_search`) + live `curl -sL` fetch of each recorded URL in the same work
window that records it + **independent local re-derivation of every number on the slide**
against the ridge closed form `W = (XᵀX + λI)⁻¹Xᵀy` (numpy solve, this work window; no
vision, no network). Frame facts come from the slide's vision-analysis record
(`analysis/slide_017_raw.json` — no `_final` exists for this slide, so the raw is the record
of the frame); NO vision calls were made by this worker. Query economy: **0 new queries**.

## Slide identity

- Frame file: `unique_slides/slide_017.jpg` (960×540, 1px = 1pt per the deck AGENTS).
- Badge number on the frame: **17** (yellow circle, black numeral). Deck rule: badge
  numeral = the file number N, no zero-padding.
- Numbering resolution: 51 founder-curated files numbered by the founder 2026-10-19; the
  pre-curation state is intentionally unrecoverable. A recovered pre-curation provenance
  value IS present in `_meta`: `source_timestamps.precuration_slide = 72`, kept frame
  `frame_02081.jpg`, t = 2080 s, `provenance: "founder-curated 2026-10-19 (frame swap from
  group)"`. So this slide is one of the 35 with recovered provenance, and it is flagged as
  a **frame swap from a dedup group** — the kept frame is not necessarily the last frame of
  its phash group, so treat its animation/animation_state reading as provisional. NOT in
  the 16-slide unrecoverable list. File number 017 and badge "17" agree; pre-curation 72 is
  historical only.
- Analysis record used: `analysis/slide_017_raw.json` (final absent — raw used per the
  mandate's fallback rule).

## Primary source(s)

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Ridge_regression` | Wikipedia article **"Ridge regression"**, § *Overview* — the source's own ridge estimator `(XᵀX + λI)⁻¹XᵀY`, which this slide numerically instantiates at λ = 3. | **CONFIRMED** — fetched live 2026-10-20 in this work window (`action=raw` wikitext + rendered HTML); quoted in `sources/slide_015_source/SOURCES.md`. |
| `https://icml.cc/Conferences/2004/proceedings/papers/354.pdf` | **Ng 2004 ICML** — the λ/α trade-off parameter definition. | **CONFIRMED (origin-level)** — downloaded live 2026-10-20 into `sources/slide_016_source/`; **no new query spent**. |
| `https://en.wikipedia.org/wiki/Robust_regression` | Wikipedia article **"Robust regression"** — why the outlier rows behave as they do. | **CONFIRMED (origin-level)** — banked in `sources/slide_012_source/SOURCES.md`. **No new query spent.** |

Nothing above was recorded from an unfetched search snippet.

## Figures used by this slide

**None.** The slide is three rows of red-bordered tables + red-bordered W boxes + blue
arrows + a title bar + a badge. No plot, no diagram, no hosted original to download; the
reason is stated here per the layout law.

## What the source(s) CONFIRM

**Every printed number on this slide is reproduced by the ridge closed form at λ = 3.**

The slide's data (from `analysis/slide_017_raw.json`): all three rows share the training
table — 8 samples, row `X1` = 1, 2, 3, 4, 8, 9, 10, **11** (row 1) / **30** (row 2, yellow) /
**60** (row 3, yellow); row `X2` = 1, 3, 5, 6, 16, 7, 5, 3; row `y` = 2, 4, 6, 8, 16, 18,
20, 22. Test table (all rows): `X1` = 30, 40, 50; `X2` = 15, 20, 25.

Method: `X = [1, x1, x2]` (bias + two features), `W = (XᵀX + λI)⁻¹Xᵀy` with **λ = 3** (the
slide's title parameter), test predictions `ŷ = w₀ + w₁·x1 + w₂·x2`.

| Row | Train X8 | Slide's printed W | Re-derived W (λ=3, full precision) | Slide's `‖W‖²` | Re-derived `‖W‖²` | Slide's test y | Re-derived test ŷ |
|---|---|---|---|---|---|---|---|
| 1 | 11 | `[0.1; 1.95; 0.03]` | `[0.1009; 1.9520; 0.0259]` | **3.8** | **3.8213** | 59, 78.7, 98.4 | 59.051, 78.701, 98.351 |
| 2 | 30 | `[1.2; 0.72; 0.77]` | `[1.1602; 0.7157; 0.7671]` | **2.45** | **2.4468** | 34.1, 45.1, 56.1 | 34.137, 45.130, 56.122 |
| 3 | 60 | `[1.77; 0.32; 0.99]` | `[1.7683; 0.3184; 0.9926]` | **4.2** | **4.2135** | 26.2, 34.4, 42.5 | 26.211, 34.358, 42.506 |

Row-by-row confirmations:

1. **Row 1 — W = [0.1; 1.95; 0.03] is the λ = 3 ridge solution.** Full-precision
   [0.1009; 1.9520; 0.0259] rounds to exactly the printed values (0.0259 → 0.03 at 2 dp).
   `‖W‖² = 3.8213` → the printed 3.8. Test predictions [59.051, 78.701, 98.351] → the
   printed 59, 78.7, 98.4.
2. **Row 2 — W = [1.2; 0.72; 0.77] and `‖W‖² = 2.45` reproduce exactly.** Full-precision
   [1.1602; 0.7157; 0.7671] → 1.2 / 0.72 / 0.77; `‖W‖² = 2.4468` → 2.45. Test predictions
   [34.137, 45.130, 56.122] → 34.1, 45.1, 56.1 — **all three exact at the printed 1-dp
   precision**.
3. **Row 3 — W = [1.77; 0.32; 0.99] and `‖W‖² = 4.2` reproduce exactly.**
   Full-precision [1.7683; 0.3184; 0.9926] → 1.77 / 0.32 / 0.99; `‖W‖² = 4.2135` → 4.2.
   Test predictions [26.211, 34.358, 42.506] → 26.2, 34.4, 42.5 — **all three exact**.
4. **The λ = 3 label in the title is the λ of the source's estimator, not a rescaled one.**
   Solving `(XᵀX + 3I)W = Xᵀy` — i.e. the source's verbatim formula
   `$\hat{\boldsymbol{\beta}}_{\lambda} = \left(\mathbf{X}^{\mathsf{T}} \mathbf{X} + \lambda \mathbf{I}\right)^{-1} \mathbf{X}^{\mathsf{T}} \mathbf{Y}$`
   with λ = 3 — reproduces the slide. This settles slide 014/015's open question about the
   `1/2` factors: the printed λ is used undivided. Source, verbatim (*Ridge regression*,
   *Overview*): "the ridge (or Tikhonov) regularization parameter λ ≥ 0 serves as the
   constant shifting the diagonals of the moment matrix."
5. **The comparison chain this slide completes.** λ = 0 (slide 013) gives
   `‖W‖²` = 4.000 → 8.112 → 16.682 across perfect → outlier-30 → outlier-60, while λ = 3
   (this slide) gives 3.821 → 2.447 → 4.214 — i.e. the ridge penalty holds the weight-norm
   roughly flat as the outlier grows, instead of letting it more than quadruple. Source,
   verbatim (*Ridge regression*, *Overview*): "In general, the method provides improved
   efficiency in parameter estimation problems in exchange for a tolerable amount of bias
   (see bias–variance tradeoff)" — the bias introduced here is visible as the row-1
   predictions drifting from the perfect 60/80/100 to 59/78.7/98.4.
6. **The source's statement that the ridge fit is deliberately not the residual-minimizing
   fit.** This slide's λ = 3 solution does NOT drive the training residuals to zero (its
   `w₁` = 1.95 rather than the λ = 0 value 2.000). Source, verbatim: "the ridge estimator
   converges to the minimum-norm ordinary least squares estimator" as λ ↓ 0 — the
   contrapositive direction (λ > 0 ⇒ not the residual minimizer) being exactly what the
   slide demonstrates.
7. **Why the middle row's norm goes DOWN (2.447 < 3.821) while the λ = 0 norm goes UP**
   (8.112 > 4.000): with the penalty in place, the fit prefers small weights and absorbs
   the outlier into the residual rather than into the parameters. Source, verbatim (*Robust
   regression*): "Because the least squares predictions are dragged towards the outliers…"
   — i.e. at λ = 0 the parameters are dragged toward the outlier, which is what raises
   `‖W‖²`; at λ = 3 the penalty resists that drag. Confirmed as the mechanism behind the
   slide's chosen numbers.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The synthetic 8-sample training dataset and 3-sample test dataset (values above) — a
  course teaching dataset, not a published benchmark.
- The three-row ladder (perfect → outlier 30 → outlier 60) at a FIXED λ = 3, and the
  choice of λ = 3 specifically as the deck's first regularization strength (λ = 10
  follows on slide 018). The specific values 3 and 10 are course choices; no source
  prescribes them.
- The display scalings: W components at 2 dp, `‖W‖²` at 2 dp, test predictions at 1 dp, and
  row 1's first prediction as a bare integer "59" (the exact value is 59.051 — i.e.
  truncated, not rounded to 59.1). Recorded so the builder does not "round" it into 59.1.
- All chrome: the `#F2F2F2` background, red `#CC0000` table/box borders, blue `#0000FF`
  "Train"/"Test" label tabs and arrows, red bold W-vector values, yellow `#FFFF00` cell
  highlights, the title's red/blue color runs ("Ridge" and "λ" blue, everything else red),
  and the yellow badge.
- 'Train'/'Test' tab labels overlapping the table top-left corners — a course styling.
- **Chrome note (deck law):** the raw reports background `#F2F2F2`, whereas this deck's
  measured house chrome mandates a white `FFFFFF` canvas. Deck house-chrome law governs the
  outer template and overrides the per-slide value (per the deck AGENTS). Recorded so the
  `#F2F2F2` in the analysis JSON is not mistaken for a source fact — it is neither.
- The `_meta`'s "frame swap from group" flag: this kept frame may not be the fully-built
  (last) frame of its phash group, so any reading that the slide is "fully revealed" is
  provisional. Recorded, not acted on.

## [?] Uncertain items

| # | Item | Resolution path |
|---|---|---|
| 1 | Whether W components are displayed at 2 dp consistently (row 1's third component 0.0259 → printed 0.03; row 1's first prediction 59.051 → printed "59") | **RESOLVED by re-derivation**: the slide truncates/floors some values and rounds others. The exact numbers are recorded here; the builder must render the printed values, not recomputed ones. |
| 2 | Whether the test y-values in row 1 (59, 78.7, 98.4) come from the full-precision W or the printed 2-dp W | **RESOLVED**: from the full-precision W (the printed 2-dp W gives 59.05, 78.66, 98.31). Recorded. |
| 3 | Exact font sizes, table cell dimensions, arrow geometry | frame-only measurement |
| 4 | Whether the Train/Test label tabs sit above or overlap the tables | frame-only measurement |
| 5 | The exact shading/edge of the yellow highlighted cells | frame-only measurement |

## Corrections

**None applied; one annotation CONFIRMED (no patch needed).** The annotation that the W
vectors are 3-parameter (bias + x1 + x2) ridge solutions with the plain λ shown in the
title is confirmed by the re-derivation, which reproduces every printed value. No analysis
JSON was edited by this worker, and no transcribed frame text is contradicted by any
source.

## Law reminder

The frame wins for recreation; the source wins for understanding. Discrepancies above (the
`#F2F2F2` background, the truncated "59") are recorded, never silently applied.
