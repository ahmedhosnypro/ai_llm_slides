# SOURCES.md — slide 019 "Test Data"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search (MCP `agy_web_search`) for discovery + live `curl -sL` fetch of every URL recorded
below, in this same work window + independent local re-derivation of the deck's numbers
(NumPy). Frame facts come from the slide's vision-analysis record
(`analysis/slide_019_raw.json` — **no `slide_019_final.json` exists**, so the raw is the
authoritative record for this slide). **No vision calls were made by this worker.**
Query economy: this slide is the first of the 019–027 matrix-inverse / ridge / gradient-descent
cluster, so the cluster's anchor sources are established here and cross-referenced by
020–027 ("no new query spent").

## Slide identity

- Frame file: `unique_slides/slide_019.jpg` (960×540, 1px = 1pt per the deck AGENTS.md).
  Local image read was attempted by this worker but the sandbox cannot render images for it;
  per the deck's no-vision law all frame facts below therefore come from the analysis record.
- Badge numeral on the frame: **19** (yellow circle, black numeral). Per the deck's verified
  rule the badge numeral = the file number N, no zero-padding.
- Numbering resolution: 51 founder-curated files numbered by the founder 2026-10-19; the
  pre-curation state is intentionally unrecoverable (owner-replaced-state law). A recovered
  pre-curation provenance value IS present in `_meta`: `source_timestamps.precuration_slide
  = 75` (kept frame `frame_02177.jpg`, t = 2176 s, `provenance: "founder-curated 2026-10-19
  (frame swap from group)"`). File number 019 and badge "19" agree; pre-curation 75 is
  historical only.
- Analysis record used: `analysis/slide_019_raw.json` (no final exists; `_meta.elapsed_s`
  314.8, model `images`). No `[?]` markers are present in this record.
- Frame md5: `f8a4feb271e79be71d946cc8628d1c51` (matches the `_meta._reconcile_md5_snapshot`).

## Primary source(s)

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Ridge_regression` | Wikipedia **"Ridge regression"** (incl. its *Tikhonov regularization for linear equations* section) — the closed-form ridge estimator this slide's entire table is built on. | **CONFIRMED** — fetched live this window: `curl -sL --max-time 45 -A "Mozilla/5.0"` → HTTP 200, 475,413 bytes, final URL `https://en.wikipedia.org/wiki/Ridge_regression` (no redirect). Also already banked verbatim by the sibling worker: `sources/slide_010_source/SOURCES.md` — cross-referenced, **no new query spent**. |
| `https://en.wikipedia.org/wiki/Gradient_descent` | Wikipedia **"Gradient descent"** — negative-gradient direction, update rule, learning rate η, convex ⇒ local minima are global minima. | **CONFIRMED** — fetched live this window, HTTP 200, 610,975 bytes, no redirect. |

Both URLs were fetched live in the same work window that records them; nothing below is
quoted from an unfetched search snippet. (The cluster's two agy searches — "ridge regression
normal equation (XᵀX + λI) inverse makes singular XᵀX invertible positive definite
regularization" and "Hoerl and Kennard 1970 …" — were used only to locate these canonical
pages; their snippets were treated as leads.)

## Figures used by this slide

**None — and correctly so.** The slide is a pure typographic comparison grid (an `Outlier X_s`
column, three regularization columns, right-pointing progression arrows). No source figure is
reused or redrawn: `imagery` is empty and `visual_elements` holds only tables/arrows/badge.
The rainbow/3-D surface plots and MATLAB-style figures the deck later uses (slides 025/027) are
course-rendered, and no hosted original for those was needed here. Per the layout law the
reason is stated rather than left silent.

## What the source(s) CONFIRM

1. **The ridge closed form the slide's three columns instantiate.** Verbatim (*Ridge
   regression*, overview):
   > "In the ordinary least squares solution of Y = Xβ + ε, the problem of a near-singular
   > moment matrix XᵀX is alleviated by adding positive elements to the diagonals, thereby
   > decreasing its condition number. Compared to the ordinary least squares estimator, the
   > simple ridge estimator has an extra term λI in the denominator: β̂_λ = (XᵀX + λI)⁻¹XᵀY"

   The slide's three column headers ("NO Regularizer with (as if λ=0)", "Ridge Regularizer
   with λ=3", "Ridge Regularizer with λ=10") are exactly this estimator evaluated at λ = 0, 3, 10.
2. **λ's role — the diagonal shift, and that λ ≥ 0.** Verbatim: "the ridge (or Tikhonov)
   regularization parameter λ ≥ 0 serves as the constant shifting the diagonals of the moment
   matrix." Confirms the slide's λ=3 / λ=10 values are ordinary ridge parameters, and that the
   "as if λ=0" caption in the first column header is the correct λ = 0 special case.
3. **Why larger λ is expected to shrink ‖W‖² — the slide's column trend.** Verbatim (same
   article, *Tikhonov regularization for linear equations*): "In many cases, this matrix is
   chosen as a scalar multiple of the identity matrix (Γ = αI), giving preference to solutions
   with smaller norms; this is known as L₂ regularization." The slide's printed ‖W‖² values do
   shrink monotonically as λ grows in the printed columns (λ=3 → λ=10: 3.8→3.5, 2.45→1.48,
   4.2→1.92 for rows 1/2/3), i.e. the demonstration's *direction* matches the source's
   "preference to solutions with smaller norms" statement.
4. **The evaluation protocol the slide uses (train on the outlier-augmented data, then predict
   on three FIXED test points).** The fixed test rows are the slide's own reference data
   (z₁ = (30, 15), y = 60; z₂ = (40, 20), y = 80; z₃ = (50, 25), y = 100) and are internally
   consistent: y = 2·x₁ holds exactly on all three (60 = 2·30, 80 = 2·40, 100 = 2·50). No
   source is needed for course-chosen demo data; the source confirms the estimator being
   applied, not the data values.

**Independent local re-derivation (this worker, NumPy):**

5. **The "NO Regularizer" column's first row is exactly reproducible.** With the three clean
   points ((30,15,60),(40,20,80),(50,25,100)) plus outlier row 1 (11, 3, 22) appended and a
   bias column of 1s, the λ=0 (least-squares / least-norm) solution is W = (bias 0, w₁ 2, w₂ 0)
   — i.e. exactly the printed **W = (2, 0)**, **‖W‖² = 4**, and predictions **y = 60, 80, 100**
   on Test1/Test2/Test3. The outlier row (11, 3) is itself interpolated (2·11 = 22), so the
   generalisation the column intends is visible: the extra point does not move the fit.
6. **The slide's printed ‖W‖² values are only sometimes the sum of squares of the printed W.**
   Recomputed ‖W‖² = w₁² + w₂²: NO row 1 → 4.00 (printed 4 ✓), NO row 2 → 7.74 (printed 8.11),
   NO row 3 → 16.08 (printed 16.7); λ=3 row 1 → 3.81 (printed 3.8 ✓), λ=3 row 2 → 1.96 (printed
   2.45), λ=3 row 3 → 3.24 (printed 4.2); λ=10 row 1 → 3.51 (printed 3.5 ✓), λ=10 row 2 → 0.82
   (printed 1.48), λ=10 row 3 → 0.78 (printed 1.92). So **5 of the 9 printed ‖W‖² values do
   not equal the squared norm of the printed W vector**.
7. **The slide's printed green test predictions are not the dot product of the printed W with
   the test point** for the ridge columns (e.g. λ=3 row 2, printed W = (1.2, 0.72) vs Test1
   (30, 15) prints y = 34.1, while 1.2·30 + 0.72·15 = 46.8). Systematically, the printed
   predictions in each ridge row ARE consistent with an *effective* W whose second component
   equals the printed W₂ but whose first component differs by a nearly constant offset per
   row (≈ −0.43 for λ=3 row 2; ≈ −1.07 for λ=3 row 3; ≈ +0.85 for λ=10 row 1), i.e. the
   printed W₁ is the outlier in that triple.
8. **I could not reproduce the printed ridge W's under the standard closed form.** Tested
   exhaustively: outlier appended vs replacing the corresponding clean row × intercept column
   present/absent × ridge penalty applied to all coefficients vs intercept left unpenalised ×
   λ ∈ {0, 3, 10}, solving (XᵀX + λI)⁻¹Xᵀy exactly. Only cell "NO / row 1" reproduces (see §5).
   The remaining values are consistent in *direction* with the source's shrinkage statement
   but not in *value*.
9. **A plausible explanation is on-slide, not invented here:** this lecture's own slide 026
   record states "GD will approximately find this minimum value but at a variable number of
   steps depending on the used Learning Rate" — the printed W vectors therefore plausibly
   come from an *iterative (gradient-descent) run at a fixed number of steps* rather than the
   exact closed form, which would explain both the value mismatch and the systematic W₁
   offset. This is recorded as the most economical explanation, **not as a fact**; the frame
   values stand unchanged for recreation.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The demo dataset itself (the three z-points, the three outlier rows (11,3,22) / (30,3,22) /
  (60,3,22), and the exact test points) — course-chosen illustrative data, no source counterpart.
  Note the outlier rows share the third coordinate 22 and differ only in x₁ (11 / 30 / 60).
- The λ values shown (0, 3, 10), the choice of three fixed test points, and the three-row
  "one outlier at a time" layout.
- The right-pointing arrows between the three main columns, presented as "increasing
  regularization strength": the source's shrinkage statement supports the direction, but the
  arrow styling is course-authored.
- Palette and chrome: blue column headers (#0000FF), red W and ‖W‖² values (#FF0000), green
  predictions (#008000), yellow badge (#FFFF00) and blue-bordered header box. The source
  article has no palette, so every colour here is course-authored.
- The apparent typo in the vision-transcribed caption "NO Regularizer with (as if λ=0)" — the
  parenthetical reading is preserved verbatim from the analysis record (transcribed frame text
  is never edited by research).

## [?] Uncertain items

| # | Item | Status / resolution path |
|---|---|---|
| 1 | Do the printed W / ‖W‖² / prediction triples come from a gradient-descent run (slide 026's "variable number of steps") rather than the closed form? | **Partly resolved.** The values are NOT reproducible under the exact closed form (§6–§8), and the systematic per-row W₁ offset in the predictions (§7) points to an iterative or partially-converged origin. The deck's own slide 026 states GD only "approximately" finds the minimum. Remaining gap: which initialisation/learning rate/step count — not web-resolvable; needs the course's code. Recorded as a discrepancy, not a correction. |
| 2 | Exact font point sizes, box geometry and arrow coordinates | frame-only measurements; no source can supply a course slide's pt sizes. Carried by the builder/judge stages. |
| 3 | Whether the "Outlier Row 1/2/3" values are *appended to* or *replace* the clean data | Not stated on the frame. Both variants were tested numerically (§8); neither reproduces the printed ridge values, so the frame does not disclose the construction. Recorded, not guessed. |

## Corrections

**None.** No dimension, attribute, or provenance guess in `analysis/slide_019_raw.json` is
contradicted by any source. The numeric inconsistencies listed in "What the sources CONFIRM"
§6–§8 are internal-to-slide (course demo values vs their own printed formula) — they are
**not** transcription errors that research may patch: the frame's numbers are transcribed frame
text and the frame wins for recreation. They are recorded here as discrepancies with their
evidence trail so the orchestrator and any later judge/pilot can see the arithmetic.
No `analysis/*.json` file was edited by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
