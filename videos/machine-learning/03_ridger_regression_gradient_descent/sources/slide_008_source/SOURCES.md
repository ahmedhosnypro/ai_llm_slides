# SOURCES.md — slide 008 "[1] Ridge Regularizer to Minimize Overfitting (Also Known as L2 regularizer)"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
("Web-source research mandate", founder in-session directive 2026-10-19). Method: agy web
search at original discovery (by my earlier records) + live `curl -sL --max-time 60 -A
"Mozilla/5.0"` re-fetch of each recorded URL in this work window. Fetch-tool note: the
WebFetch tool returned timeouts on these hosts earlier in the assignment, so `curl -sL` is
the fetch tool of record. **No new query spent** for this slide — the ridge source and the
overfitting/norm anchors were all located, fetched live, and banked by my own
`slide_003_source`, `slide_004_source`, and `slide_007_source` records (economy law: reuse
banked records, cross-reference, note "no new query spent"). Frame facts come from
`analysis/slide_008_final.json`; **no vision calls were made by this worker**.

## Slide identity

- Frame file: `unique_slides/slide_008.jpg` (960x540, 1px = 1pt per the deck AGENTS).
  Badge numeral on the frame: **8** (yellow circle, black numeral).
- Founder-curated numbering (2026-10-19). Recovered provenance from the analysis `_meta`
  only: `source_timestamps.precuration_slide = 12` (kept frame `frame_00447.jpg`,
  t = 446 s, `provenance: "founder-curated kept frame"`). Current file number 008 and badge
  "8" agree; 12 is historical provenance only and is never used for the badge.
- Analysis record used: `analysis/slide_008_final.json` (verdict PASS_WITH_FIXES,
  recreatability 9/10). Title-only slide (two text lines); no bullets, equations, or imagery.

## Primary source(s)

**No new query spent.** The ridge-regularization source was located and banked by my own
`slide_003_source` / `slide_004_source` records; re-fetched live in this work window to verify
this slide's two-line claim:

- **https://en.wikipedia.org/wiki/Ridge_regression** — Wikipedia article **"Ridge
  regression"** (Tikhonov regularization for linear equations). Re-fetched live in this work
  window: HTTP 200 (after three attempts with backoff; the first two returned a transient
  connection failure `000`), `text/html`, 475,413 bytes. CONFIRMED.

The "overfitting" and the norm anchors for this slide are origin-level cross-references to
already-fetched, already-banked sources:

| URL | Banked by | Used here for |
|---|---|---|
| `https://en.wikipedia.org/wiki/Overfitting` (*Remedy* section) | `slide_007_source` | The direction "to Minimize Overfitting": the remedy for an overfitted model is a penalty/regularization term. |
| `https://en.wikipedia.org/wiki/Euclidean_norm` (L2 ≡ Euclidean) | `slide_004_source` | The "L2" in the subtitle: the ridge penalty is the squared 2-norm (Euclidean) norm of the weights, and slide 004's record establishes the identity `‖a‖₂² = aᵀa` with `‖a‖₂` the Euclidean/ℓ2 norm. |

No snippet-derived URL is recorded. No figure was downloaded (see next section).

## Figures used by this slide

None. The slide is a centered two-line title block ("[1] Ridge Regularizer to Minimize
Overfitting" + "(Also Known as L2 regularizer)") with a yellow slide-number badge — no
charts, diagrams, plots, or imagery. The source articles contain figures, but none is a
figure this slide reuses or redraws, so nothing was copied into this directory. The
"Ridge regression" article's geometry is the teacher's own pedagogical introduction to a
section header, not a sourced visual.

## What the source(s) CONFIRM

The slide has two on-slide claims; both are confirmed by the fetched/ banked sources:

1. **"Ridge Regularizer"** (ridge is a regularized estimator that adds a penalty term) —
   CONFIRMED. Wikipedia *Ridge regression*, verbatim (Tikhonov section): *"In order to give
   preference to a particular solution with desirable properties, a regularization term can
   be included in this minimization: ‖Ax − b‖₂² + ‖Γx‖₂²."* and the closed form: *"the simple
   ridge estimator has an extra term λI in the denominator: β̂_λ = (XᵀX + λI)⁻¹XᵀY."* The
   article also states the purpose: *"Ridge regression was developed as a possible solution to
   the imprecision of least square estimators when linear regression models have some
   multicollinear (highly correlated) independent variables."* This ties directly back to
   slide 007's problems [1] (singular / near-singular `XᵀX`) and [2] (the inversion of the
   Gramian), which is exactly the context the slide's "[1]" reference points to.

2. **"to Minimize Overfitting"** (the regularization is applied to reduce overfitting) —
   CONFIRMED in direction. The ridge article states it buys *"improved efficiency in
   parameter estimation problems in exchange for a tolerable amount of bias"* — i.e. it
   deliberately shrinks the coefficients to improve generalization, which is the standard
   anti-overfitting trade. The *Overfitting* article's *Remedy* section (banked in
   `slide_007_source`, and cross-referenced here with no new query) lists regularization as a
   remedy whose basis is to *"explicitly penalize overly complex models"*. Ridge's `λ‖Γx‖₂²`
   penalty is precisely such a penalty on the weights, so shrinking-weights ridge is the
   implemented form of "minimize overfitting" the slide names.

3. **"Also Known as L2 regularizer"** (ridge = L2 regularization) — CONFIRMED by the
   article's own wording. Wikipedia *Ridge regression*, verbatim: *"L2 regularization is used
   in many contexts aside from linear regression, such as classification with logistic
   regression or support vector machines, and ma[chine learning]…"*. The penalty term
   `‖Γx‖₂²` is literally the **squared ℓ2 (Euclidean) norm**, and slide 004's banked record
   established the exact identity the deck uses (`‖a‖₂² = aᵀa`, `‖a‖₂` = Euclidean/L2 norm),
   so "L2 regularizer" is the correct synonym for the ridge penalty.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The title-block typography and layout: `#C00000` bold title line, `#0000CC` italic blue
  parenthetical line, both horizontally centered; yellow `#FFFF00` badge with black numeral
  "8"; thin gray `#808080` frame; the slide background `#F0F0F0`. These are the deck's chrome,
  not sourced facts.
- The specific wording and the bracketed back-reference "[1]" tying this slide to the first
  problem category on slide 007 — an authoring choice, not a source phrase.
- The deck's own lowercase-cased parenthetical "(Also Known as L2 regularizer)" phrasing.
- The white mouse-pointer cursor the vision record flags as a video-capture artifact (the
  analysis record already excludes it from recreation).
- Chrome note (deck law, not a research finding): the vision record reports background
  `#F0F0F0`; this deck's measured house chrome (AGENTS.md) governs the outer template and
  overrides per-slide analysis values. Recorded so no builder mistakes `#F0F0F0` for a source
  fact.

## [?] Uncertain items

The analysis record lists only frame-local typography uncertainties (exact font point sizes;
badge outline described only as "dark"; border "dark" vs `#808080`). None of these are
source-resolvable and none concerns the slide's two substantive claims — both "ridge
regularizer" and "L2 regularizer" are **CONFIRMED** above with fetched URLs. No `[?]` marker
on a substantive claim is removed here because the record carried none on these claims.

## Corrections

**None proposed.** The slide is a title-only statement; it carries no equations, no numeric
model values, no dimension annotations, and no provenance guesses that a source contradicts.
The two conceptual labels ("regularizer", "L2") are corroborated verbatim by the ridge
article. Per the mandate, corrections would patch model annotations only and never
transcribed frame text; nothing here needs a patch and no analysis JSON was edited by this
worker.

## Law reminder

The frame wins for recreation; the source wins for understanding. Discrepancies above are
recorded, never silently applied.
