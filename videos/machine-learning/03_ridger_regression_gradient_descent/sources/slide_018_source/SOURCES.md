# SOURCES.md — slide 018 "Adding Ridge Regularizer to the model  λ=10"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search (MCP `agy_web_search`) + live `curl -sL` fetch of each recorded URL in the same work
window that records it + **independent local re-derivation of every number on the slide**
against the ridge closed form `W = (XᵀX + λI)⁻¹Xᵀy` (numpy solve, this work window; no
vision, no network). Frame facts come from the slide's vision-analysis record
(`analysis/slide_018_raw.json` — no `_final` exists for this slide, so the raw is the record
of the frame); NO vision calls were made by this worker. Query economy: **0 new queries**.
This worker's model has **no image input**, so no frame re-read was possible; where the
frame would settle a question, that is stated explicitly below instead of being guessed.

## Slide identity

- Frame file: `unique_slides/slide_018.jpg` (960×540, 1px = 1pt per the deck AGENTS).
- Badge number on the frame: **18** (yellow circle, black numeral). Deck rule: badge
  numeral = the file number N, no zero-padding.
- Numbering resolution: 51 founder-curated files numbered by the founder 2026-10-19; the
  pre-curation state is intentionally unrecoverable. A recovered pre-curation provenance
  value IS present in `_meta`: `source_timestamps.precuration_slide = 74`, kept frame
  `frame_02176.jpg`, t = 2175 s, `provenance: "founder-curated kept frame"`. One of the 35
  with recovered provenance; NOT in the 16-slide unrecoverable list. File number 018 and
  badge "18" agree; pre-curation 74 is historical only.
- Analysis record used: `analysis/slide_018_raw.json` (final absent — raw used per the
  mandate's fallback rule).

## Primary source(s)

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Ridge_regression` | Wikipedia article **"Ridge regression"**, § *Overview* — the source's own ridge estimator `(XᵀX + λI)⁻¹XᵀY`, which this slide numerically instantiates at λ = 10. | **CONFIRMED** — fetched live 2026-10-20 in this work window; quoted in `sources/slide_015_source/SOURCES.md`. |
| `https://en.wikipedia.org/wiki/Matrix_calculus` | Wikipedia article **"Matrix calculus"** — the derivative identities behind the closed form. | **CONFIRMED (origin-level)** — banked in `sources/slide_015_source/SOURCES.md`. **No new query spent.** |
| `https://en.wikipedia.org/wiki/Robust_regression` | Wikipedia article **"Robust regression"** — outlier/leverage behaviour. | **CONFIRMED (origin-level)** — banked in `sources/slide_012_source/SOURCES.md`. **No new query spent.** |
| `https://icml.cc/Conferences/2004/proceedings/papers/354.pdf` | **Ng 2004 ICML** — the λ/α trade-off parameter. | **CONFIRMED (origin-level)** — banked in `sources/slide_016_source/`. **No new query spent.** |

Nothing above was recorded from an unfetched search snippet.

## Figures used by this slide

**None.** The slide is three rows of tables + red-bordered W boxes + blue arrows + a title
bar + a badge. No plot, no diagram, no hosted original to download; the reason is stated
here per the layout law.

## What the source(s) CONFIRM

**Nearly every printed number on this slide is reproduced by the ridge closed form at
λ = 10 — with one genuine mismatch and one internal inconsistency, both documented below.**

The slide's data (from `analysis/slide_018_raw.json`): all three rows share the training
table — 8 samples, row `x1` = 1, 2, 3, 4, 8, 9, 10, **11** (row 1) / **30** (row 2, yellow) /
**60** (row 3, yellow); row `x2` = 1, 3, 5, 6, 16, 7, 5, 3; row `y` = 2, 4, 6, 8, 16, 18,
20, 22. Test table (all rows): `x1` = 30, 40, 50; `x2` = 15, 20, 25.

Method: `X = [1, x1, x2]` (bias + two features), `W = (XᵀX + λI)⁻¹Xᵀy` with **λ = 10** (the
slide's subtitle parameter), test predictions `ŷ = w₀ + w₁·x1 + w₂·x2`.

| Row | Train X8 | Slide's printed W | Re-derived W (λ=10, full precision) | Slide's `‖W‖²` | Re-derived `‖W‖²` | Slide's test y | Re-derived test ŷ |
|---|---|---|---|---|---|---|---|
| 1 | 11 | `[[0.13],[1.87],[0.09]]` | `[0.1339; 1.8660; 0.0874]` | **3.5** | **3.5075** | 57.4, 76.5, 95.6 | 57.425, 76.522, 95.619 |
| 2 | 30 | `[[0.54],[0.73],[0.81]]` | `[0.5422; 0.7342; 0.8054]` | **1.48** | **1.4817** | 34.6, **46.4**, 57.4 | 34.649, **46.018**, 57.387 |
| 3 | 60 | `[[0.82],[0.33],[1.1]]` | `[0.8206; 0.3330; 1.0637]` | **1.92** | **1.9157** | 26.8, 35.4, 44.1 | 26.766, 35.414, 44.062 |

Row-by-row confirmations:

1. **Row 1 — all nine printed values reproduce.** `[0.1339; 1.8660; 0.0874]` rounds to
   exactly the printed `[[0.13],[1.87],[0.09]]`; `‖W‖² = 3.5075`, which the slide renders at
   1 dp as **3.5**; test predictions [57.425, 76.522, 95.619] → 57.4, 76.5, 95.6.
2. **Row 2 — W and the norm reproduce; one test prediction does not.** `[0.5422; 0.7342;
   0.8054]` rounds exactly to the printed `[[0.54],[0.73],[0.81]]`; `‖W‖² = 1.4817` → 1.48.
   Test predictions re-derive to [34.649, **46.018**, 57.387]: 34.6 ✓, 57.4 ✓, but the
   slide's printed middle value **46.4 ≠ 46.0**. Recomputing from the slide's own *printed*
   W gives 45.94 → 45.9, which also is not 46.4. **The printed 46.4 is not reproducible from
   either the exact or the printed W** — see the discrepancy note at the end of this
   section. The frame wins: 46.4 is rendered as printed.
3. **Row 3 — all nine printed values reproduce, with one mixed-precision display detail.**
   `[0.8206; 0.3330; 1.0637]` rounds to 0.82 / 0.33 / **1.06** at 2 dp; the slide prints the
   third component as "1.1" (1 dp). `‖W‖² = 1.9157` → 1.92. Test predictions
   [26.766, 35.414, 44.062] → 26.8, 35.4, 44.1 — all three exact.
4. **The λ = 10 label is the λ of the source's estimator, undivided.** Solving
   `(XᵀX + 10I)W = Xᵀy` — the source's verbatim
   `$\hat{\boldsymbol{\beta}}_{\lambda} = \left(\mathbf{X}^{\mathsf{T}} \mathbf{X} + \lambda \mathbf{I}\right)^{-1} \mathbf{X}^{\mathsf{T}} \mathbf{Y}$`
   with λ = 10 — reproduces the slide. Source, verbatim (*Ridge regression*, *Overview*):
   "the ridge (or Tikhonov) regularization parameter λ ≥ 0 serves as the constant shifting
   the diagonals of the moment matrix."
5. **The λ = 3 → λ = 10 progression is numerically visible in the deck's own terms.**
   Overall `‖W‖²` at λ = 3 (slide 017): 3.821 → 2.447 → 4.214. At λ = 10 (this slide):
   3.508 → 1.482 → 1.916. Stronger shrinkage, exactly as the source's bias–variance framing
   predicts: "In general, the method provides improved efficiency in parameter estimation
   problems in exchange for a tolerable amount of bias (see bias–variance tradeoff)." The
   trade cost is visible in row 1's predictions drifting further from the perfect-fit values
   60/80/100 (λ=0) → 59/78.7/98.4 (λ=3) → 57.4/76.5/95.6 (λ=10).
6. **The λ = 0 → λ = 3 → λ = 10 sequence across slides 013/017/018 is a monotone
   regularization-strength ladder**, matching the source's λ ≥ 0 parameterization: λ = 0 is
   the unregularized least-squares limit ("For Γ = 0 this reduces to the unregularized
   least-squares solution, provided that (AᵀA)⁻¹ exists" — verbatim, *Ridge regression*).

### Discrepancy recorded (frame wins; source wins for understanding)

**Row 2's middle test value 46.4 cannot be reproduced.** The exact λ = 10 solution gives
46.018 → 46.0; the slide's own printed W gives 45.94 → 45.9; the slide prints **46.4**.
Note that this worker cannot re-read the frame (no image input), so the frame reading is
the analysis record's. What can be said from the sources and the arithmetic: (a) 46.4 is
not the value produced by the model the slide itself prints, so it is most likely a
lecture-time hand annotation or a display typo; (b) the analysis record independently
notices "a small red pencil-like mark appears near the middle y value" in the row-2 test
table, which is consistent with a hand-corrected figure; (c) the recorded value remains
the frame's, and no source replaces it. **Do not silently write 46.0 or 45.9 into the
build** — render 46.4 as printed and carry the discrepancy into the QA record.

### Internal inconsistency in the analysis record (proposed correction, for the orchestrator)

The raw's row-2 and row-3 train tables record the **y row** as `2, 4, 30, 8, 16, 18, 20,
22` and `2, 4, 60, 8, 16, 18, 20, 22` — i.e. a yellow "30"/"60" appearing in the y row at
the X3 position — and its visual-element descriptions assert "The cells X8=30 in the x1
row and X3=30 in the y row are yellow-highlighted". That y-row reading is **mutually
inconsistent with the rest of the same slide**: substituting y = (2, 4, 30, 8, 16, 18, 20,
22) with x1's X8 = 30 into the λ = 10 ridge solve gives W = [1.523; 0.662; 1.048],
`‖W‖² = 3.856 and predictions ≈ [37.11, 48.98, 60.84] — nothing like the slide's printed
[0.54; 0.73; 0.81], 1.48, [34.6, 46.4, 57.4]. By contrast, leaving the y row at
2, 4, 6, 8, 16, 18, 20, 22 reproduces the printed W, the printed `‖W‖²` and three of the
four printed predictions exactly (see the table above). **Proposed patch (NOT applied by
this worker — the orchestrator edits analysis JSONs):** correct the *descriptive annotation*
in `visual_elements`/`regions` that claims a highlighted 30/60 in the y row at X3, and
annotate the row-2/row-3 train-table descriptions as "y row unchanged (2, 4, 6, 8, 16, 18,
20, 22); the yellow highlight is on the X8 cell of the x1 row only" — matching slides
012/013/017, whose y rows are all 2, 4, 6, 8, 16, 18, 20, 22 and which the slide's own
numbers are consistent with. **This is an annotation patch, not a transcription rewrite.**
If a future frame re-read shows the frame genuinely prints 30/60 in the y row, then the
frame wins, the printed y row stands, and the W/`‖W‖²`/test values were computed from a
different (y-unchanged) dataset — which would itself be a finding about the course's slide
construction. Either way, nothing is silently changed.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The synthetic 8-sample training dataset and 3-sample test dataset — a course teaching
  dataset, not a published benchmark.
- The three-row ladder at a FIXED λ = 10, and the choice of 10 as the deck's second
  regularization strength. Course choices; no source prescribes them.
- The display scalings and the mixed precision: W components at 2 dp except row 3's third
  component printed as "1.1" (exact 1.0637); `‖W‖²` at 1 dp for row 1 (3.5075 → 3.5) but
  2 dp for rows 2–3 (1.4817 → 1.48, 1.9157 → 1.92); test predictions at 1 dp.
- Row 2's printed test value 46.4 (see the discrepancy note) and the small red pencil-like
  mark near it — a lecture annotation, not recomputed model output.
- All chrome: white background, red `#C00000` table/W-box borders, blue `#0000FF`/`#0000CC`
  arrows and λ, yellow `#FFFF00` highlights, light-green `#CCFFCC` table header cells,
  dark-green header text, red Test prediction values, the title's red/blue color runs
  ("Ridge" and "λ" blue), and the yellow badge.
- The Light-green header-cell styling and the lowercase row labels (`x1`, `x2`, `y`) on this
  slide versus the capitalized `X1`/`X2`/`y` on slides 012/013/017 — a course styling
  inconsistency between slides; recorded, not harmonized.
- **Chrome note (deck law):** the raw reports background `#FFFFFF`, agreeing with the deck's
  mandated white canvas. No divergence.

## [?] Uncertain items

| # | Item | Resolution path |
|---|---|---|
| 1 | Row 2's middle test-y value: printed 46.4, exact ridge 46.0, printed-W recomputation 45.9 | **RESOLVED to the extent web sources can**: not reproducible from either the exact or the printed model, so it is a frame/lecture artifact. The frame wins — render 46.4. Recorded in the discrepancy note. |
| 2 | The y rows of rows 2 and 3 (recorded as containing 30/60 at X3) | **PROPOSED CORRECTION** documented above for the orchestrator; the rest of the slide's own numbers are reproduced only with the y row unchanged. Frame re-read needed for final adjudication (this worker's model has no image input). |
| 3 | Row 3's W third component printed "1.1" vs exact 1.0637 (2-dp would be 1.06) | **RESOLVED by re-derivation**: a mixed-precision display choice. Render as printed. |
| 4 | Exact font sizes, table cell dimensions, arrow geometry | frame-only measurement |
| 5 | Whether the W boxes' red border is `#C00000` and its fill pure white | frame-only measurement |
| 6 | The lowercase `x1`/`x2` row labels vs slides 013/017's capitalized `X1`/`X2` | frame-only: the record transcribes lowercase here; frame text wins, keep lowercase |

## Corrections

**One correction PROPOSED (documented, NOT applied — the orchestrator edits analysis
JSONs):** the y-row reading in the row-2/row-3 train-table descriptions and the associated
"X3=30/60 in the y row is yellow-highlighted" annotation, as detailed in the internal
inconsistency note above. Evidence: the slide's own printed W, `‖W‖²` and test predictions
are reproduced to display precision only when the y row is 2, 4, 6, 8, 16, 18, 20, 22
(unchanged), and the same y row is what slides 012/013/017 record. Nothing in any web
source contradicts this; it is an internal-consistency finding plus a re-derivation.

**One discrepancy RECORDED (no correction possible):** the printed 46.4 in row 2's middle
test-y, which no computation reproduces. Frame wins; render as printed.

No analysis JSON was edited by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding. Discrepancies above are
recorded, never silently applied.
