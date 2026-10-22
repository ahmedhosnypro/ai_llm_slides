# SOURCES.md — slide 020 "[2] Ridge Regularization to overcome Inverse Problem of Singular Matrix"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search (MCP `agy_web_search`) for discovery + live `curl -sL` fetch of every URL recorded
below in this same work window + local arithmetic verification. Frame facts come from the
slide's vision-analysis record (`analysis/slide_020_final.json`, verdict PASS_WITH_FIXES,
recreatability 8). **No vision calls were made by this worker.**
Query economy: **no new query spent on this slide** — every claim is covered by the cluster's
anchor sources already fetched live and banked in `sources/slide_019_source/SOURCES.md`
(this worker, same work window) and `sources/slide_010_source/SOURCES.md` (sibling worker).

## Slide identity

- Frame file: `unique_slides/slide_020.jpg` (960×540). Badge numeral **20** (yellow circle,
  black text). Deck rule: badge numeral = the file number N, no zero-padding.
- Numbering resolution: founder-curated numbering 2026-10-19; pre-curation state unrecoverable
  by owner-replacement. `_meta` records recovered provenance: `precuration_slide = 92`
  (kept frame `frame_02323.jpg`, t = 2322 s, `provenance: "founder-curated kept frame"`).
  File number 020 and badge "20" agree; pre-curation 92 is historical only.
- Analysis record used: `analysis/slide_020_final.json`. The frame is a **title-only
  section-divider** slide (two bold red #C00000 lines, the second underlined; yellow badge;
  a mouse cursor the validation record correctly rules a screen-recording artifact and
  excludes from recreation; thin border frame). `verbatim_text.bullets` was populated by the
  validator from the title itself.

## Primary source(s)

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Ridge_regression` | Wikipedia **"Ridge regression"** — the estimator whose λI term "overcomes the inverse problem". | **CONFIRMED** — fetched live this window, HTTP 200, 475,413 bytes. Banked with quotes in `sources/slide_019_source/SOURCES.md` (this worker, same window) and `sources/slide_010_source/SOURCES.md` (sibling). **No new query spent.** |
| `https://en.wikipedia.org/wiki/Invertible_matrix` | Wikipedia **"Invertible matrix"** — the singularity/non-invertibility terminology the divider's title uses. | **CONFIRMED** — fetched live this window, HTTP 200, 440,221 bytes, final URL unchanged (no redirect). |
| `https://cs229.stanford.edu/notes2021fall/cs229-notes1.pdf` | Stanford **CS229 Part I notes (2021 fall)** — the standard course statement of exactly why XᵀX has "no inverse". | **CONFIRMED** — fetched live this window: `curl -sL --max-time 60 -A "Mozilla/5.0"` → HTTP 200, 357,392 bytes, PDF 1.5, text-extracted with `pdftotext`. |
| `https://en.wikipedia.org/wiki/Ridge_regression` (references for Hoerl & Kennard) | Bibliographic record of the 1970 paper that introduced ridge. | **CONFIRMED** via the fetched article's reference list (see §3.4). The paper's own pages are fetch-blocked — see the attempt log under [?] §1. |

## Figures used by this slide

**None — and correctly so.** Title-only divider: `imagery: []`, `visual_elements` holds only
the badge, the cursor artifact, and the border. No chart, diagram or source figure exists on
this frame, so nothing was downloaded. Per the layout law the reason is stated here rather
than left silent.

## What the source(s) CONFIRM

1. **The terminology "singular matrix" ⇔ "no inverse", and the determinant criterion.** Verbatim
   (*Invertible matrix*, lead): "In linear algebra, an **invertible matrix** (*non-singular*,
   non-degenerate or regular) is a square matrix that has an inverse." And: "For a real matrix,
   this is reflected by its determinant: **an invertible matrix has nonzero determinant, while
   a matrix with determinant zero collapses volume to zero and is not invertible.**"
   This is the exact vocabulary of the divider's title — "Inverse Problem of **Singular
   Matrix**" = the linear-regression normal-equation step that inverts XᵀX.
2. **The rank formulation (the state XᵀX can fall into).** Verbatim: "Equivalently, an n × n
   matrix is invertible if its rank is n, by the rank-nullity theorem. Such a matrix is said to
   be of full rank." Confirms the slide 21 example matrix (which has rank 2 of 3 — verified
   locally, see slide 021's record) as a textbook singular case.
3. **The standard-course statement of the "inverse problem" in regression, which is precisely
   what this divider announces.** Verbatim (CS229 2021 fall notes, footnote 3 to the closed-form
   solution):
   > "Note that in the above step, we are implicitly assuming that XᵀX is an invertible
   > matrix. This can be checked before calculating the inverse. If either the number of
   > linearly independent examples is fewer than the number of features, or if the features
   > are not linearly independent, then XᵀX will not be invertible. Even in such cases, it is
   > possible to "fix" the situation with additional techniques, which we skip here for the
   > sake of simplicity."

   The slide's "[2]" divider names the *first* of those fix techniques — ridge — and slide 21
   supplies the worked example.
4. **Ridge is the remedy for the near-singular moment matrix, with the Hoerl & Kennard
   provenance.** Verbatim (*Ridge regression*, overview):
   > "In the ordinary least squares solution of Y = Xβ + ε, the problem of a near-singular
   > moment matrix XᵀX is alleviated by adding positive elements to the diagonals, thereby
   > decreasing its condition number. Compared to the ordinary least squares estimator, the
   > simple ridge estimator has an extra term λI in the denominator: β̂_λ = (XᵀX + λI)⁻¹XᵀY"

   And the article's own reference list, verbatim: "Hoerl, Arthur E.; Kennard, Robert W. (1970).
   "Ridge Regression: Biased Estimation for Nonorthogonal Problems". Technometrics. 12 (1):
   55–67. doi:10.2307/1267351. JSTOR 1267351." So the technique the divider names is exactly
   Hoerl & Kennard's 1970 ridge estimator, history CONFIRMED from the live-fetched article.
5. **Mechanism, at the algebra level (why λI guarantees invertibility).** Verbatim (*Ridge
   regression*, *Tikhonov regularization for linear equations*): "The operator A*A + ΓᵀΓ is
   then a self-adjoint bounded invertible operator." With Γ = αI this is the same λI shift that
   makes the matrix invertible (its eigenvalues are all shifted strictly positive).
6. **"Overcome" as stabilisation, not just repair.** Verbatim: "the problem of a near-singular
   moment matrix XᵀX is alleviated by adding positive elements to the diagonals, **thereby
   decreasing its condition number**" — confirms the divider's framing that ridge *overcomes*
   the inverse problem, including the ill-conditioned (near-singular) case slide 022 then
   continues into.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The section numbering "[2]" and the deck's section-divider style (title-only frame, bold
   #C00000 centred text, second line underlined, #FFFF00 yellow badge, thin border).
- The exact two-line break: "[2] Ridge Regularization to overcome" / "Inverse Problem of
  Singular Matrix".
- The word "overcome" (the sources say "alleviated" / "fix the situation"); the deck's stronger
  verb is course-authored pedagogy and is not contradicted by any source.
- The mouse pointer near bottom-center and the border frame: the validation record explicitly
  rules the cursor a screen-recording artifact and the brief's step 5 forbids reproducing it;
  the border is course chrome.
- Background #F0F0F0 measured on this frame vs the deck's mandated white `FFFFFF` canvas:
  deck house-chrome law governs the recreation (AGENTS.md "House chrome — THIS deck").
  Recorded only so the measured value is not mistaken for a source fact.

## [?] Uncertain items

| # | Item | Status / resolution path |
|---|---|---|
| 1 | The Hoerl & Kennard 1970 paper's own abstract | **Attempted, fetch-blocked (NOT recorded as a source).** `https://www.tandfonline.com/doi/abs/10.1080/00401706.1970.10488634` → HTTP 403 (bot challenge, 5,726 bytes, no article); `https://www.jstor.org/stable/1267351` → HTTP 200 but serves only a "Client Challenge" bot wall (3,038 bytes, no content); Semantic Scholar API `DOI:10.1080/00401706.1970.10488634` → HTTP 404 "Paper with id … not found". The bibliographic record IS confirmed from the live-fetched Wikipedia article (§3.4). The abstract text seen in an agy search snippet is a **LEAD only** and was not recorded as a source. Recommend the orchestrator bank the three fetch-blocked URLs in the fleet map's do-not-reuse section. |
| 2 | Whether the divider's "[2]" numbering matches a numbered agenda elsewhere in the deck | Frame-only; the frame shows no agenda list. No web resolution possible; carried by the build stage. |
| 3 | Exact title point size, exact border weight, badge diameter | Frame-only measurements from the vision record's own estimates; no source can supply them. |

## Corrections

**None.** No dimension, attribute or provenance guess in `analysis/slide_020_final.json` is
contradicted by any source. The sources *confirm* the divider's terminology
(singular/non-singular, invertibility, determinant criterion, ridge as the remedy) rather than
correcting it. No `analysis/*.json` file was edited by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
