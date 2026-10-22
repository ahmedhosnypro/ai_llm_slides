# SOURCES.md — slide 014 "LOSS Function that MINIMIZES Overfitting"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search (MCP `agy_web_search`) + live `curl -sL` fetch of each URL in the same work window
that records it + local consistency checks of the slide's own equations. Frame facts come
from the slide's vision-analysis record (`analysis/slide_014_raw.json` — no `_final`
exists for this slide, so the raw is the record of the frame); NO vision calls were made by
this worker. Query economy: **0 new queries** — this slide's claims are covered by the
cluster's shared primary sources.

## Slide identity

- Frame file: `unique_slides/slide_014.jpg` (960×540, 1px = 1pt per the deck AGENTS).
- Badge number on the frame: **14** (yellow circle, black numeral). Deck rule: badge
  numeral = the file number N, no zero-padding.
- Numbering resolution: 51 founder-curated files numbered by the founder 2026-10-19; the
  pre-curation state is intentionally unrecoverable. A recovered pre-curation provenance
  value IS present in `_meta`: `source_timestamps.precuration_slide = 29` (kept frame
  `frame_01082.jpg`, t = 1081 s, `provenance: "founder-curated kept frame"`). This slide is
  one of the 35 with recovered provenance and is NOT in the 16-slide unrecoverable list.
  File number 014 and badge "14" agree; pre-curation 29 is historical only.
- Analysis record used: `analysis/slide_014_raw.json` (final absent — raw used per the
  mandate's fallback rule).

## Primary source(s)

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Ridge_regression` | Wikipedia article **"Ridge regression"** — *Overview* (the ridge estimator and its Lagrangian form) and *Tikhonov regularization for linear equations* (the augmented-form derivation, the Γ=αI ⇒ L2 statement, the conditioning benefit). This is the source for every equation on the slide. | **CONFIRMED** — fetched live 2026-10-20 in this work window (`action=raw` wikitext, 35,436 bytes + rendered HTML, 475,413 bytes). Quotes verbatim below. |
| `https://en.wikipedia.org/wiki/Tikhonov_regularization` | Wikipedia article "Tikhonov regularization" | **CONFIRMED, resolves as a redirect**: live fetch returned `#REDIRECT [[Ridge regression#Tikhonov regularization]]`. RESOLVED final URL = `https://en.wikipedia.org/wiki/Ridge_regression#Tikhonov_regularization_for_linear_equations`. Recorded so no future worker treats it as a separate article. |
| `https://en.wikipedia.org/wiki/Overfitting` | Wikipedia article **"Overfitting"** — the remedy list that motivates adding a generalization/penalty term to the loss. | **CONFIRMED (origin-level)** — banked in `sources/slide_010_source/SOURCES.md`. **No new query spent.** |
| `https://en.wikipedia.org/wiki/Lasso_(statistics)` | Wikipedia article **"Lasso (statistics)"** — the L1 counterpart (`‖β‖₁ = ∑\|βⱼ\| ≤ t`), used on slide 016. | **CONFIRMED (origin-level)** — fetched live 2026-10-20 in this work window (`action=raw`, 56,860 bytes); quoted in `sources/slide_016_source/SOURCES.md`. **No new query spent.** |

Nothing above was recorded from an unfetched search snippet.

## Figures used by this slide

**None.** The slide is entirely boxes and formula bands — two vector-definition boxes,
three full-width explanatory bands, two term boxes and a final full-width formula band,
plus the badge. `imagery: []` and every visual element is a highlight-box or the badge.
No plot, no diagram, no hosted original to save; the reason is stated here per the layout
law.

## What the source(s) CONFIRM

The slide's five equations are, verbatim from the record:

1. `Y = [y1; y2; ...; yN]  N×1` — "Original Labels from Training Samples"
2. `Ŷ = [ŷ1; ŷ2; ...; ŷN]  N×1` — "Predicted Labels from Model Ŷ = XW"
3. `Objective is Ŷ=Y and ‖W‖ is minimum` → "This is called Ridge Regularization"
4. `J(W) = Loss(X,Y,W) + λ R(W)` with "(λ is a weighting factor)"
5. `Loss Term = ‖Y−Ŷ‖² = (Y−Ŷ)ᵀ(Y−Ŷ)`; `Regularization Term R = ‖W‖² = WᵀW`
6. `J(W) = 1/2 [ (Y−Ŷ)ᵀ(Y−Ŷ) + λ WᵀW ]`

Point by point:

1. **The overall shape — a data-fit term plus a regularization term, weighted by λ.**
   Source, verbatim (*Ridge regression*, *Overview*, Lagrangian form):
   > `$\text{argmin}_{\boldsymbol{\beta}} \, \|\mathbf{Y} - \mathbf{X} \boldsymbol{\beta}\|^2 + \lambda \left(\boldsymbol\beta^\mathsf{T}\boldsymbol\beta - c\right)$`
   i.e. the objective is exactly "fit term + λ · (norm-squares term)", confirming the
   slide's `J(W) = Loss(X,Y,W) + λ R(W)` and the note "(λ is a weighting factor)".
   The source's own words for λ's role, verbatim: "the ridge (or Tikhonov)
   regularization parameter λ ≥ 0 serves as the constant shifting the diagonals of the
   moment matrix" — the same "weighting factor" semantics.
2. **The fit term is the squared distance between the predicted and the original labels.**
   Slide: "Define Loss function as squared distance between Ŷ and Y", `Loss Term =
   ‖Y−Ŷ‖² = (Y−Ŷ)ᵀ(Y−Ŷ)`. Source, verbatim (*Ridge regression*, *Tikhonov
   regularization for linear equations*):
   > "Ordinary least squares seeks to minimize the sum of squared residuals, which can be
   > compactly written as
   > `$\left\|A\mathbf{x} - \mathbf{b}\right\|_2^2,$`
   > where ‖·‖₂ is the Euclidean norm."
   The slide's `‖Y−Ŷ‖² = (Y−Ŷ)ᵀ(Y−Ŷ)` is the standard expansion of that squared
   Euclidean norm, and is confirmed by the article's own subsequent use of the
   matrix form throughout.
3. **The regularizer is the squared norm of the weight vector.** Slide: `Regularization
   Term R = ‖W‖² = WᵀW` and "Objective is Ŷ=Y and ‖W‖ is minimum". Source, verbatim
   (*Ridge regression*, *Tikhonov regularization for linear equations*):
   > "In many cases, this matrix is chosen as a scalar multiple of the identity matrix
   > (Γ = αI), giving preference to solutions with smaller norms; this is known as
   > L₂ regularization."
   and, in the same article's opening note, ridge regression is listed among the names for
   > "{{math|''L''₂}} regularization".
   So "penalize the weight vector by its squared norm ⇒ ridge" is directly confirmed.
4. **The augmented/stacked form is the same objective.** Source, verbatim:
   > "In order to give preference to a particular solution with desirable properties, a
   > regularization term can be included in this minimization:
   > `$\left\|A\mathbf{x} - \mathbf{b}\right\|_2^2 + \left\|\Gamma \mathbf{x}\right\|_2^2=\left\|\mathcal{A}\mathbf{x} - \mathcal{b}\right\|_2^2,$`
   > where `$\mathcal{A}=\begin{pmatrix}A\\\Gamma\end{pmatrix}$` and
   > `$\mathcal{b}=\begin{pmatrix}\mathbf{b}\\\boldsymbol 0\end{pmatrix}$`"
   This is the source's derivation of exactly the slide's final band: appending the
   penalty rows to the data rows. The slide's `1/2 [ (Y−Ŷ)ᵀ(Y−Ŷ) + λ WᵀW ]` is the
   same objective written with a 1/2 factor (see course-authored note 3 below).
5. **Why adding the term reduces overfitting / improves generalization.** Source, verbatim
   (*Ridge regression*, *Overview*): "In general, the method provides improved efficiency
   in parameter estimation problems in exchange for a tolerable amount of bias (see
   bias–variance tradeoff)." and verbatim (*Overfitting*, *Remedy*):
   > "To lessen the chance or amount of overfitting, several techniques are available
   > (e.g., model comparison, cross-validation, regularization, early stopping, pruning,
   > Bayesian priors, or dropout). The basis of some techniques is to either (1) explicitly
   > penalize overly complex models…"
   This confirms the slide's title claim that this loss function "MINIMIZES Overfitting".
6. **The conditioning benefit, which is why the penalty is added at all.** Source, verbatim
   (*Ridge regression*, *Overview*): "the problem of a near-singular moment matrix
   `XᵀX` is alleviated by adding positive elements to the diagonals, thereby decreasing
   its condition number. Compared to the ordinary least squares estimator, the simple ridge
   estimator has an extra term `λI` in the denominator". This is the source's explanation
   of the mechanism that slide 015 then completes.
7. **Notation.** `Ŷ = XW` (predictions are the design matrix times the weight vector),
   `Y` as the response vector and `W` as the parameter vector are all standard usages the
   source uses in its β/W conventions ("where Y is the regressand or response vector, X is
   the design matrix, and I is the identity matrix" — verbatim from the article's estimator
   passage).

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- **The 1/2 factor.** The slide writes `J(W) = 1/2 [ (Y−Ŷ)ᵀ(Y−Ŷ) + λ WᵀW ]`. The source
  states the objective without the 1/2 (`‖Y − Xβ‖² + λ(βᵀβ − c)`) and, in its
  least-squares passage, uses `(1/N)‖y − Xβ‖²₂` in the lasso-adjacent literature but not
  in this article's ridge passage. The 1/2 is a course normalization chosen so that the
  gradient drops the factor 2 (which is exactly how slide 015's `1/2[2XᵀXW − 2XᵀY] + λIW`
  line works out). **Do not "fix" the slide to the source's unscaled form** — and do not
  "fix" the source to the slide's either; the discrepancy is recorded here only.
- **The λ multiplies only WᵀW (not also the loss term).** The slide's final band applies
  1/2 to the parenthesized sum, so the loss term's 1/2 is there but the λ term's 1/2 is
  inside the brackets too — a course scaling choice; the source has no 1/2 at all.
- The two vector-definition boxes ("Original Labels / from Training Samples",
  "Predicted Labels / from Model Ŷ = XW") and the plain-language glosses "Objective is
  Ŷ=Y and ‖W‖ is minimum", "This is called Ridge Regularization", "(λ is a weighting
  factor)" — course pedagogy glosses, not source text.
- All color-coding and chrome: the mixed blue/black title with "LOSS", "MINIMIZES",
  "Overfitting" in bold blue; the light-yellow `#FFF9C4` bands; the light-pink `#FFEBEE`
  band; the light-blue `#E1F5FE` boxes and final band; red for Loss terms, blue for
  weight/regularization terms, green for conceptual highlights; the yellow badge `#FFEB3B`.
- The framing "Objective is Ŷ=Y and ‖W‖ is minimum" as the definition of ridge: a
  course paraphrase of the constraint view (the source presents it as the Lagrangian
  `argmin ‖Y−Xβ‖² + λ(βᵀβ − c)`). Recorded, not "fixed".
- **Chrome note (deck law):** the raw reports background `#FFFFFF`, agreeing with the
  deck's mandated white canvas. No divergence.

## [?] Uncertain items

| # | Item | Resolution path |
|---|---|---|
| 1 | The exact scale of λ relative to the 1/2 factors — i.e. whether the intended objective is `½‖Y−Ŷ‖² + (λ/2)‖W‖²` or `½[‖Y−Ŷ‖² + λ‖W‖²]` as written | **RESOLVED by internal consistency**: the slide writes the latter (λ inside the brackets), and slides 017/018 print λ = 3 and λ = 10 as the values that produce their W vectors. This worker's independent re-derivation confirms that λ = 3 solves `(XᵀX + 3I)W = Xᵀy` and λ = 10 solves `(XᵀX + 10I)W = Xᵀy` — i.e. the slide's λ is the λ of the source's `(XᵀX + λI)⁻¹XᵀY` form, with NO 1/2 halving it. See slide 017 / 018 records. |
| 2 | Whether the source's `‖·‖₂` and the slide's `‖·‖²` are intended identically | **RESOLVED**: the source says "‖·‖₂ is the Euclidean norm" and uses `‖Y − Xβ‖²` in its estimator passage; `‖W‖² = WᵀW` is the source's own convention (its constraint form uses βᵀβ). |
| 3 | The pastel band colors and the exact color-run assignments (which words are red/blue/green) | frame-only measurement (the raw's own notes give no pt sizes) |
| 4 | Whether the column-vector brackets are meant with a subscript `N×1` at the right of the bracket (as the raw's recreation brief specifies) | frame-only measurement |
| 5 | The exact point sizes for the title and the formula bands | frame-only measurement |

## Corrections

**None applied; one annotation CONFIRMED.** The re-derivation (slides 013/017/018 records)
confirms the annotation that the slide's λ is the plain λ of `(XᵀX + λI)⁻¹XᵀY` — no
rescaling by the 1/2 — so no patch is needed. No analysis JSON was edited by this worker.
Nothing in the sources contradicts any transcribed frame text.

## Law reminder

The frame wins for recreation; the source wins for understanding. Discrepancies above
(the missing/present 1/2 factors) are recorded, never silently applied.
