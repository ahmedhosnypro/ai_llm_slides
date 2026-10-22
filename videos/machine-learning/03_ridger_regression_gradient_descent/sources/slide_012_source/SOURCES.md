# SOURCES.md — slide 012 "Effect of Overfitting on model parameter "W""

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search (MCP `agy_web_search`) + live `curl -sL` fetch of each URL in the same work window
that records it + **independent local re-derivation of the slide's own numbers** against
the ordinary-least-squares normal equation (a numpy solve in the project's Python; no
vision, no network). Frame facts come from the slide's vision-analysis record
(`analysis/slide_012_final.json`); NO vision calls were made by this worker. Query
economy: **0 new queries** — this slide's claims are covered by the cluster's shared
sources, already fetched live for slides 010/011.

## Slide identity

- Frame file: `unique_slides/slide_012.jpg` (960×540, 1px = 1pt per the deck AGENTS).
- Badge number on the frame: **12** (yellow circle, black numeral). Deck rule: badge
  numeral = the file number N, no zero-padding.
- Numbering resolution: 51 founder-curated files numbered by the founder 2026-10-19; the
  pre-curation state is intentionally unrecoverable. A recovered pre-curation provenance
  value IS present in `_meta`: `source_timestamps.precuration_slide = 18` (kept frame
  `frame_00751.jpg`, t = 750 s, `provenance: "founder-curated kept frame"`). This slide is
  one of the 35 with recovered provenance and is NOT in the 16-slide unrecoverable list.
  File number 012 and badge "12" agree; pre-curation 18 is historical only.
- Analysis record used: `analysis/slide_012_final.json` (verdict PASS_WITH_FIXES,
  recreatability 9). Raw not needed.

## Primary source(s)

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Robust_regression` | Wikipedia article **"Robust regression"** — the canonical account of OLS sensitivity to outliers, leverage points in the explanatory variables, and Cook's-distance influence. This is the source behind this slide's whole demonstration. | **CONFIRMED** — fetched live 2026-10-20 in this work window (`action=raw` wikitext, 22,500 bytes). Quotes verbatim below. |
| `https://en.wikipedia.org/wiki/Outlier` | Wikipedia article **"Outlier"** — outlier/influence detection in regression. | **CONFIRMED (origin-level)** — fetched live 2026-10-20 in this work window (`action=raw`, 28,734 bytes). Quotes verbatim below. |
| `https://en.wikipedia.org/wiki/Ridge_regression` | Wikipedia article **"Ridge regression"** — the unregularized (λ↓0) limit and the ridge estimator, which is the deck's eventual remedy. | **CONFIRMED (origin-level)** — fetched live 2026-10-20 and banked with quotes in `sources/slide_014_source/SOURCES.md` / `slide_015_source/SOURCES.md`. **No new query spent.** |
| `https://en.wikipedia.org/wiki/Overfitting` | Wikipedia article **"Overfitting"** — overfit-vs-generalize definition. | **CONFIRMED (origin-level)** — banked in `sources/slide_010_source/SOURCES.md`. **No new query spent.** |

Nothing above was recorded from an unfetched search snippet.

## Figures used by this slide

**None.** This slide is built entirely from tables, colored label boxes, a curved arrow
and a question box — no plot, no diagram, no hosted figure to download. The analysis
record confirms `imagery: []` and every `visual_element` is a table, a highlight-box, an
arrow or the badge. There is therefore no source-page original to save; the reason is
stated here per the layout law.

## What the source(s) CONFIRM

The slide's own numbers were independently re-derived by this worker (numpy, in this work
window) from the ordinary-least-squares normal equation on the exact table contents the
analysis record transcribes. This is the strongest evidence available and it is a
**complete match**:

**The slide's data (from `analysis/slide_012_final.json`):** the perfect training table
has 8 samples. Row `X1` (feature x1) = 1, 2, 3, 4, 8, 9, 10, 11; row `X2` (feature x2)
= 1, 3, 5, 6, 16, 7, 5, 3; row `y` = 2, 4, 6, 8, 16, 18, 20, 22. The Test table has
three samples: `X1` = 30, 40, 50; `X2` = 15, 20, 25. The two outlier training tables are
identical to the perfect one except the X8 cell of row X1, which becomes 30 (middle) and
60 (bottom), highlighted yellow.

1. **"Perfect Data / Y follows x1" is exactly true.** The design matrix
   X = [1, x1, x2] (with a bias column) and y as above give the OLS solution
   **W = [0; 2; 0]** with `||W||² = 0² + 2² + 0² = 4.000`, i.e. the prediction is exactly
   `ŷ = 2·x1` — matching the label "Y follows x1" verbatim, and matching slide 013's
   first row (W = [0; 2; 0], `||W||² = 4`). Re-derived value: `W = [0. 2. 0.]`,
   `||W||^2 = 4.000`.
2. **The Test table row `y = 60, 80, 100` is the unregularized fit's own prediction.**
   Feeding the three test samples through W = [0; 2; 0] gives `ŷ = 60, 80, 100` — exactly
   the values printed on the slide (and on slide 013's row-1 test table). This confirms
   the label chain "Perfect Data → Y follows x1" → test predictions on the same model.
3. **The outlier genuinely distorts the model parameter W — which is the slide's title
   claim.** Replacing only the X8 cell of row X1 (11 → 30 → 60) and re-solving OLS gives:

   | Train table | Re-derived W (OLS, λ=0) | Re-derived `||W||²` |
   |---|---|---|
   | perfect (X8's x1 = 11) | [0.000; 2.000; 0.000] | 4.000 |
   | first outlier (X8's x1 = 30) | [2.693; 0.670; 0.643] | 8.112 |
   | second outlier (X8's x1 = 60) | [3.998; 0.288; 0.784] | 16.682 |

   The bias term and the x1 coefficient blow up as the outlier grows — the parameter
   vector is "dragged towards" the outlier, exactly as the source describes. These
   re-derived values reproduce slide 013's row 2 (`W = [2.7; 0.67; 0.64]`,
   `||W||² = 8.11`) and row 3 (`W = [4; 0.29; 0.78]`, `||W||² = 16.7`) to the slide's own
   rounding. This worker's derivation is therefore corroborated by the deck's own numbers,
   not asserted.
4. **The source's account of the mechanism.** Verbatim (*Robust regression*, introduction):
   > "For example, least squares estimates for regression models are highly sensitive to
   > outliers: an outlier with twice the error magnitude of a typical observation
   > contributes four (two squared) times as much to the squared error loss, and therefore
   > has more leverage over the regression estimates."
   and verbatim (same article, "Presence of outliers"):
   > "In the presence of outliers that do not come from the same data-generating process as
   > the rest of the data, least squares estimation is inefficient and can be biased.
   > Because the least squares predictions are dragged towards the outliers, and because
   > the variance of the estimates is artificially inflated, the result is that outliers
   > can be masked."
5. **The outlier here sits in an EXPLANATORY VARIABLE (a leverage point), which is the
   case where even robust estimators lose their advantage.** Verbatim (*Robust regression*):
   > "In 1964, Huber introduced M-estimation for regression. The M in M-estimation stands
   > for 'maximum likelihood type'. The method is robust to outliers in the response
   > variable, but turned out not to be resistant to outliers in the explanatory variables
   > (leverage points). In fact, when there are outliers in the explanatory variables, the
   > method has no advantage over least squares."
   This is precisely the slide's construction: the distortion is injected into row **X1**
   (a feature), while rows X2 and y are left untouched. Source terminology for the
   slide's "x8 is Outlier" labels.
6. **Irrelevance of the untouched feature.** The re-derived W above shows the x2
   coefficient staying small (0 → 0.643 → 0.784) while the x1 coefficient and the bias
   move violently — consistent with the slide's "Again / Y follows x1" callout pointing
   back at the middle table.
7. **The closing question "What will be the effect of X8 Outlier values on the trained
   model ???" is answered by the next two slides (013, then 014–018: the ridge-penalized
   objective).** Verbatim (*Robust regression*, on the diagnosis of influential points):
   > "In regression problems, an alternative approach may be to only exclude points which
   > exhibit a large degree of influence on the estimated coefficients, using a measure
   > such as Cook's distance."
   and (*Outlier*): "Mahalanobis distance and leverage are often used to detect outliers,
   especially in the development of linear regression models." The deck's chosen remedy is
   regularization rather than exclusion — a course choice, recorded below.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The synthetic dataset itself: the specific values 1,2,3,4,8,9,10,11 / 1,3,5,6,16,7,5,3 /
  2,4,6,8,16,18,20,22 and the test triples 30/40/50 and 15/20/25 are a course-authored
  teaching dataset, not a published benchmark. The x2 row is deliberately non-monotonic
  (…16, 7, 5, 3) so that y = 2·x1 is the only exact rule — a course construction.
- The three-row "perfect → outlier 30 → outlier 60" escalation and the vertical stacking of
  the three training tables as a before/after ladder.
- All chrome and styling: the red title, the blue "Training Data"/"Test Data" label boxes
  with white bold text, the two identical red "x8 is Outlier" boxes, the red "Again /
  Y follows x1" callout and the curved red arrow, the blue-bordered white question box,
  the yellow cell highlights on the changed X8 cells, and the yellow slide badge.
- The x8/X8 capitalization inconsistency ("x8 is Outlier" in the labels vs "X8" in the
  table header and in the question) — transcribed frame text, preserved.
- The chart-palette-style table colors (blue y-row values, black X1/X2-row values, bold
  blue headers).
- **Chrome note (deck law):** the vision record reports background `#FFFFFF` for this
  slide, which already agrees with the deck's mandated white canvas — no divergence here.
- The course's chosen remedy is *regularization* (slides 014+) rather than the source's
  robust-regression/Cook's-distance exclusion path. Recorded as a course choice; not
  "fixed" toward the source.

## [?] Uncertain items

| # | Item | Resolution path |
|---|---|---|
| 1 | Exact font family (record guesses Arial/Calibri) | frame-only; any bold sans-serif reproduces the slide |
| 2 | The perfect training table's `colors` array contains `#FF0000` but no red element is described inside that table — an internal inconsistency in the vision record, unverifiable without the image (this worker's model has no image input, so no frame re-read was possible) | frame-only re-measurement by the owning builder/judge |
| 3 | Corrected positions for the `again_callout` and `question_callout` (the validator moved them off the original overlapping coordinates, trusting the arrangement text) — exact on-slide placement unverifiable | frame-only measurement |
| 4 | Percent positions of the title, badge and the four left-column labels — best-effort reconstructions from qualitative placement | frame-only measurement |
| 5 | The red arrow's exact curvature, thickness and endpoints | frame-only measurement |
| 6 | Whether the row labeled `X1`/`X2` in the tables is intended as "feature 1"/"feature 2" (as this record's re-derivation assumes, with a bias/intercept column in W) or as something else | resolved by internal consistency: only that reading reproduces both the printed W values on slide 013 and the printed test predictions 60/80/100 exactly |

## Corrections

**None applied, none proposed.** The slide's transcribed frame text (labels, table values,
the question) is fully self-consistent with the OLS re-derivation, and the record's model
annotations (region percentages, color arrays, chart/table type guesses) are either
frame-local measurements or explicitly flagged as uncertain by the validator. No source
contradicts any transcribed text. Per the mandate, no analysis JSON was edited by this
worker; any patch would need the orchestrator's hand.

## Law reminder

The frame wins for recreation; the source wins for understanding. Discrepancies above are
recorded, never silently applied.
