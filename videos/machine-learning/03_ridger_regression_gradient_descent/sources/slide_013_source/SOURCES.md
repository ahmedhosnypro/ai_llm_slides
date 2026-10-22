# SOURCES.md — slide 013 "Effect of Overfitting on model parameter "W"" (unregularized / λ=0 case)

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search (MCP `agy_web_search`) + live `curl -sL` fetch of each URL in the same work window
that records it + **independent local re-derivation of every number on the slide** against
the ordinary-least-squares normal equation (numpy, in this work window; no vision, no
network). Frame facts come from the slide's vision-analysis record
(`analysis/slide_013_raw.json` — no `_final` exists for this slide, so the raw is the
record of the frame, as the mandate directs); NO vision calls were made by this worker.
Query economy: **0 new queries** — covered by the cluster's shared sources.

## Slide identity

- Frame file: `unique_slides/slide_013.jpg` (960×540, 1px = 1pt per the deck AGENTS).
- Badge number on the frame: **13** (yellow circle, black numeral). Deck rule: badge
  numeral = the file number N, no zero-padding.
- Numbering resolution: this slide is one of the **16 honestly unrecoverable** ones
  (1,2,3,**13**,24-29,33,35,36,43,44,47 per the deck AGENTS): the founder removed the
  pre-curation state, and `_meta` carries **no `source_timestamps` block at all**
  (only `frame`, `model`, `elapsed_s`). File number 013 and badge "13" are the only
  authority; there is no old-numbering mapping to consult and none should be hunted for
  (owner-replaced-state law). The deck AGENTS explicitly says not to treat this gap as an
  error.
- Analysis record used: `analysis/slide_013_raw.json` (final absent — the raw is used, per
  the mandate's fallback rule). Note: this raw is one of the "three pending raws
  (033/043/044)"? — no; the deck AGENTS names 033/043/044 as pending for badge checks.
  Slide 013's badge "13" is present in the raw's labels and regions and is self-consistent.

## Primary source(s)

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Ridge_regression` | Wikipedia article **"Ridge regression"** — its *Overview* statement of the ridge estimator, and the λ↓0 limit ("the ridge estimator converges to the minimum-norm ordinary least squares estimator"). That limit is exactly what this slide displays, since slide 013 carries **no λ at all** — its three W vectors are pure ordinary least squares. | **CONFIRMED** — fetched live 2026-10-20 in this work window (`action=raw` wikitext, 35,436 bytes + rendered HTML). Quotes verbatim below. |
| `https://en.wikipedia.org/wiki/Robust_regression` | Wikipedia article **"Robust regression"** — OLS sensitivity to outliers and leverage points in the explanatory variables. | **CONFIRMED (origin-level)** — fetched live 2026-10-20 in this work window, banked in `sources/slide_012_source/SOURCES.md`. **No new query spent.** |
| `https://en.wikipedia.org/wiki/Overfitting` | Wikipedia article **"Overfitting"** — the overfit-vs-generalize definition | **CONFIRMED (origin-level)** — banked in `sources/slide_010_source/SOURCES.md`. **No new query spent.** |

Nothing above was recorded from an unfetched search snippet.

## Figures used by this slide

**None.** The slide is three rows of tables + red column vectors W + yellow ellipse norm
callouts + blue arrows; no plot or diagram. `imagery` is absent from the raw record and
every visual element is a table, a "diagram" (the bracketed W column vector), a
highlight-box, an arrow or the badge. There is no hosted original to download; the reason
is stated here per the layout law.

## What the source(s) CONFIRM

**Headline result: every printed number on this slide is reproduced exactly by the
ordinary-least-squares normal equation on the table contents the analysis record
transcribes.** Re-derivation method (numpy, this work window): design matrix
X = [1, x1, x2] (bias + two features), solve `XᵀX W = Xᵀy`; test predictions
`ŷ = w₀ + w₁·x1 + w₂·x2`.

The slide's data (from the raw): the training table (all three rows share it) has 8
samples — row `X1` = 1, 2, 3, 4, 8, 9, 10, **11** (row 1) / **30** (row 2) / **60**
(row 3, X8 cell yellow-highlighted); row `X2` = 1, 3, 5, 6, 16, 7, 5, 3 (unchanged);
row `y` = 2, 4, 6, 8, 16, 18, 20, 22 (unchanged). Test table (all rows): `X1` = 30, 40,
50; `X2` = 15, 20, 25.

| Row | Train X8 cell | Slide's printed W | Re-derived W (full precision) | Slide's `||W||²` | Re-derived `||W||²` | Slide's test y | Re-derived test ŷ |
|---|---|---|---|---|---|---|---|
| 1 | 11 | `[0; 2; 0]` | `[0.0000; 2.0000; 0.0000]` | **4** | **4.0000** | 60, 80, 100 | 60, 80, 100 |
| 2 | 30 | `[2.7; 0.67; 0.64]` | `[2.6925; 0.6700; 0.6428]` | **8.11** | **8.1119** | 32.4, 42.3, 52.3 | 32.4349, 42.3490, 52.2631 |
| 3 | 60 | `[4; 0.29; 0.78]` | `[3.9980; 0.2880; 0.7844]` | **16.7** | **16.6822** | 24.4, 31.2, 38 | 24.4033, 31.2050, 38.0068 |

Every cell of that table matches to the slide's own display precision (W shown to 2 dp,
norm to 2 dp, predictions to 1 dp). Specific confirmations:

1. **Row 1 is the "Perfect Data / Y follows x1" fit.** W = [0; 2; 0] gives
   `ŷ = 2·x1` exactly, `||W||² = 0 + 4 + 0 = 4`, and test predictions exactly
   60, 80, 100 — identical to slide 012's printed test table. The slide's row-1 norm
   callout `||W||² = 4` is exact (4.0000), and `0² + 2² + 0² = 4` also holds.
2. **Row 2 reproduces W = [2.7; 0.67; 0.64] and `||W||² = 8.11`.** Full-precision
   [2.6925; 0.6700; 0.6428] rounds to exactly the printed values; `||W||² = 8.1119`
   rounds to 8.11. Note for the builder: 8.11 is computed from the **full-precision** W
   (the 2-dp printed W would give 8.0946 → 8.09), so the course computed the norm before
   rounding W. Do not "recompute" the ellipse text from the rounded W.
3. **Row 3 reproduces W = [4; 0.29; 0.78] and `||W||² = 16.7`.** Full-precision
   [3.9980; 0.2880; 0.7844] rounds exactly to the printed values (3.9980 → "4");
   `||W||² = 16.6822` → 16.7.
4. **The test predictions match to the printed precision.** Re-derived
   [32.4349, 42.3490, 52.2631] → 32.4, 42.3, 52.3 and [24.4033, 31.2050, 38.0068] →
   24.4, 31.2, 38. All six values are the full-precision model's predictions, correctly
   rounded — not values recomputed from the rounded W (which would give 32.39, 42.29,
   52.19 / 24.40, 31.20, 38.00).
5. **This slide is the UNREGULARIZED case (λ = 0 / plain least squares).** The slide
   prints no λ, and the numbers are the pure OLS solution. Source confirmation, verbatim
   (*Ridge regression*, *Overview*):
   > "Note that as λ↓0, the constraint eventually becomes non-binding, and the ridge
   > estimator converges to the minimum-norm ordinary least squares estimator, here
   > denoted as `$\hat{\boldsymbol{\beta}}=\hat{\boldsymbol{\beta}}_0$`:"
   with
   > `$\lim_{\lambda\downarrow 0} \hat{\boldsymbol{\beta}}_{\lambda}=\mathbf{X}^+\mathbf{Y}=\hat{\boldsymbol{\beta}}_0$`
   and, from the same article's *Tikhonov regularization for linear equations* section:
   > "The effect of regularization may be varied by the scale of the matrix Γ. For Γ = 0
   > this reduces to the unregularized least-squares solution, provided that (AᵀA)⁻¹
   > exists."
   So the row-1..row-3 escalation on this slide is precisely the "regularization parameter
   = 0" behavior the deck then contrasts with λ = 3 (slide 017) and λ = 10 (slide 018).
6. **The escalation is the slide's pedagogical payload: `||W||²` grows 4 → 8.11 → 16.7 as
   the outlier grows 11 → 30 → 60.** Source account of why the *parameters* move, verbatim
   (*Robust regression*, "Presence of outliers"):
   > "Because the least squares predictions are dragged towards the outliers, and because
   > the variance of the estimates is artificially inflated, the result is that outliers
   > can be masked."
   and verbatim (introduction): "least squares estimates for regression models are highly
   sensitive to outliers: an outlier with twice the error magnitude of a typical
   observation contributes four (two squared) times as much to the squared error loss, and
   therefore has more leverage over the regression estimates." The re-derived table above
   is the quantitative form of that statement for this dataset.
7. **The outlier is in an explanatory variable (a leverage point).** Verbatim (*Robust
   regression*): "The method is robust to outliers in the response variable, but turned out
   not to be resistant to outliers in the explanatory variables (leverage points). In fact,
   when there are outliers in the explanatory variables, the method has no advantage over
   least squares." Matches the slide's construction: only row X1's X8 cell changes; rows
   X2 and y are held fixed (visually, the yellow highlight marks exactly that one cell).

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The synthetic 8-sample dataset and the 3-sample test set (values listed above) — a
  course-authored teaching dataset, not a published benchmark. The x2 row's deliberate
  non-monotonicity (…16, 7, 5, 3) makes `y = 2·x1` the only exact rule.
- The three-row "perfect → outlier 30 → outlier 60" ladder with identical tables except
  the highlighted X8 cell, and the horizontal Train → W → Test flow with blue arrows.
- The display choice to show W to 2 dp, `||W||²` to 2 dp and the test predictions to
  1 dp, with the norm computed from the full-precision W (see §2/§3 above). Do not
  "normalize" these roundings.
- The red bracketed column-vector rendering of W, the yellow ellipse norm callouts, and
  the color scheme (red W values, blue y-row values, bold blue headers, black body).
- No λ appears on this slide whereas slides 017/018 print λ=3 / λ=10 — a deliberate
  staging choice by the course (this slide = the unregularized baseline). Recorded, not
  "fixed" by adding a λ.
- The raw record's own uncertainty about the Train/Test label boxes ("Train label
  white-on-blue box; Test label black-on-yellow box") — a model annotation,
  frame-verifiable only.
- **Chrome note (deck law):** the raw reports background `#FFFFFF`, which agrees with the
  deck's mandated white canvas. No divergence.

## [?] Uncertain items

| # | Item | Resolution path |
|---|---|---|
| 1 | `||W||²` values are shown to 2 dp while W is shown to 2 dp; a naive recomputation from the rounded W gives 8.09 / 16.69 instead of 8.11 / 16.7 | **RESOLVED by re-derivation**: the course computed the norm from the full-precision W. Recorded so the builder does not "correct" the ellipse text. |
| 2 | Test-prediction rounding: 38.0068 printed as "38"; 31.2050 as "31.2" | **RESOLVED by re-derivation** (full-precision model → 1-dp display). Recorded, not a defect. |
| 3 | The exact display font/point sizes and the ellipse's exact geometry | frame-only measurement |
| 4 | Whether the W vector is 3×1 (bias + 2 features) or 2×1 | **RESOLVED by re-derivation**: only the 3-parameter (bias + x1 + x2) reading reproduces the printed W values and the printed test predictions simultaneously. Recorded as the confirmed reading. |
| 5 | Whether the Train/Test label tags are white-on-blue and black-on-yellow respectively (raw's typography note) | frame-only measurement |

## Corrections

**None applied; one annotation is CONFIRMED (no patch needed).** The re-derivation
confirms the raw's implicit reading that the W vectors are the ordinary-least-squares
solution of the printed training tables with a bias term — so nothing in the annotation
needs patching. The raw's transcribed frame text (all table values, both W sets, all three
norm values, all nine test predictions) is exactly correct as transcribed, which is a
strong result: no correction of any kind is warranted. Per the mandate, no analysis JSON
was edited by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding. Discrepancies above are
recorded, never silently applied.
