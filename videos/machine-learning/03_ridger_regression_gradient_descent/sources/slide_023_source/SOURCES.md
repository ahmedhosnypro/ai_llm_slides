# SOURCES.md — slide 023 "Inverse of High Dimension Matrix"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search (MCP `agy_web_search`) for discovery + live `curl -sL` fetch of every URL recorded below
in this same work window + PDF text extraction (`pdftotext`) + local arithmetic. Frame facts
come from the slide's vision-analysis record (`analysis/slide_023_final.json`, verdict
PASS_WITH_FIXES, recreatability 9). **No vision calls were made by this worker.**
Query economy: **1 new query spent in this cluster's third search** ("CS229 Stanford lecture
notes normal equations versus gradient descent 'when d is large' use gradient descent
computational cost") to locate the live CS229 notes URLs whose 404 variants I first tried;
all remaining claims reuse anchors banked in `sources/slide_019_source/SOURCES.md`,
`…/slide_020_source/SOURCES.md` and `…/slide_021_source/SOURCES.md` (**no new query spent**).

## Slide identity

- Frame file: `unique_slides/slide_023.jpg` (960×540). Badge numeral **23**. Title top-left
  in red, four stacked coloured content boxes below (green "Recall:" / blue complexity /
  plain example line / yellow "Solution:").
- Numbering resolution: founder-curated numbering 2026-10-19; pre-curation state
  intentionally unrecoverable. `_meta` records `precuration_slide = 105` (kept frame
  `frame_02540.jpg`, t = 2539 s, `provenance: "founder-curated kept frame"`). File number 023
  and badge "23" agree; pre-curation 105 is historical only.
- Analysis record used: `analysis/slide_023_final.json` (validated by glm-5.3, 405.3 s).
  Frame's verbatim claims (transcribed, never edited by research):
  - equation: `W = (X^T X + λI)^(-1) X^T Y`
  - labels: `Recall:`, `if Feature vectors are of dimension d`, `(X^T X) is of size d+1 x d+1`,
    `Solution:`
  - body: "The standard matrix inversion algorithm has a time complexity of O(n^3), which means
    that the computation time increases rapidly with the size of the matrix (increasing cubically
    with the number of components)."
  - "For Example: if Features vector is of size 1000 then Inverse calculation is or order
    1,000,000,000 which is impractical"
  - "Instead of using Least Squares with Matrix inversion," / "use Gradient Descent iterative
    solution"

## Primary source(s)

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://cs229.stanford.edu/main_notes.pdf` | Stanford **CS229 notes (current main notes PDF, 5,355,993 bytes)** — the normal-equations closed form recalled in the green box, and the explicit `d+1-by-d+1` dimension statement. | **CONFIRMED** — fetched live this window: `curl -sL --max-time 90 -A "Mozilla/5.0"` → HTTP 200, PDF v1.5, text-extracted with `pdftotext -layout` (12,580 lines). |
| `https://cs229.stanford.edu/notes2021fall/cs229-notes1.pdf` | Stanford **CS229 Part I notes (2021 fall, 357,392 bytes)** — same closed form, plus the invertibility caveat slide 020/021 already used. | **CONFIRMED** — fetched live this window, HTTP 200, PDF v1.5, text-extracted. |
| `https://en.wikipedia.org/wiki/Gaussian_elimination` | **"Gaussian elimination"** — the O(n³) cost of the standard matrix-inversion algorithm. | **CONFIRMED** — fetched live this window, HTTP 200, 368,265 bytes. Banked in `sources/slide_022_source/SOURCES.md` (this worker). **No new query spent.** |
| `https://en.wikipedia.org/wiki/Computational_complexity_of_mathematical_operations` | **"Computational complexity of mathematical operations"** — the matrix-algebra complexity table (multiplication/inversion O(n³) family). | **CONFIRMED** — fetched live this window, HTTP 200, 455,652 bytes, no redirect. |
| `https://en.wikipedia.org/wiki/Computational_complexity_of_matrix_multiplication` | **"Computational complexity of matrix multiplication"** — states that inversion/determinant/Gaussian elimination share matrix multiplication's asymptotic complexity. | **CONFIRMED** — fetched live this window, HTTP 200, 414,433 bytes, no redirect. (The specific quoted sentence carries Wikipedia's own "[citation needed]" tag; recorded honestly, and it is not load-bearing for the slide's claim, which is independently carried by the Gaussian-elimination page below.) |
| `https://en.wikipedia.org/wiki/Gradient_descent` | **"Gradient descent"** — the iterative remedy named in the yellow Solution box. | **CONFIRMED** — fetched live this window, HTTP 200, 610,975 bytes. Banked in `sources/slide_019_source/SOURCES.md` (this worker). **No new query spent.** |
| `https://en.wikipedia.org/wiki/Ridge_regression` | **"Ridge regression"** — the (XᵀX + λI)⁻¹XᵀY estimator the slide recalls. | **CONFIRMED** — fetched live this window, HTTP 200, 475,413 bytes. Banked in `sources/slide_019_source/SOURCES.md` (this worker) and `sources/slide_010_source/SOURCES.md` (sibling). **No new query spent.** |

## Figures used by this slide

**None — and correctly so.** The slide is typographic only: four coloured rounded-rectangle
boxes with text and one inline equation (`imagery: []`, `visual_elements` holds only the
highlight boxes and the badge). No chart, diagram or reused source figure exists on the frame,
so nothing was downloaded. Per the layout law the reason is stated rather than left silent.

## What the source(s) CONFIRM

1. **The recalled estimator, verbatim.** The green box's `W = (X^T X + λI)^(-1) X^T Y` matches
   the CS229 closed form exactly. Verbatim (CS229 main notes, section 1.2):
   > "we set its derivatives to zero, and obtain the normal equations: XᵀXθ = Xᵀỹ. Thus, the
   > value of θ that minimizes J(θ) is given in closed form by the equation
   > θ = (XᵀX)⁻¹Xᵀỹ"

   and the ridge version (Wikipedia *Ridge regression*): "the simple ridge estimator has an
   extra term λI in the denominator: β̂_λ = (XᵀX + λI)⁻¹XᵀY". The slide's W/λ/upper-case-Y
   notation is the course's house style for the same object (θ/λ/ỹ in CS229, β/λ/Y in
   Wikipedia) — notation difference only, not a content difference.
2. **The dimension claim `(X^T X) is of size d+1 x d+1`, verbatim from the source.** CS229 main
   notes, Newton's-method section:
   > "H is a d-by-d matrix (actually, **d+1-by-d+1, assuming that we include the intercept
   > term**) called the Hessian"

   The +1 is the intercept column. Verbatim (CS229, linear-regression setup): "x0 = 1 (this is
   the intercept term), so that". And Wikipedia *Design matrix*: "The simple linear regression
   model is yi = β0 + β1xi + εi, where β0 is the y-intercept and β1 is the slope of the
   regression line … where the **first column of 1s in the design matrix allows estimation of
   the y-intercept** while the second column contains the x-values associated with each
   observation." So with d feature dimensions plus the intercept column of 1s, the design
   matrix is m × (d+1) and its Gram/moment matrix XᵀX is (d+1) × (d+1) — exactly the slide's
   annotation. This also matches the slide's feature dimension for the earlier demo data
   (test points carry two features x₁, x₂ – see slide 019).
3. **The O(n³) complexity claim, verbatim.** Wikipedia *Gaussian elimination*,
   *Computational efficiency*:
   > "Computationally, for an n × n matrix, this method needs only O(n³) arithmetic
   > operations, while using Leibniz formula for determinants requires (n n!) operations …"

   and "to solve a system of n equations for n unknowns by performing row operations on the
   matrix until it is in echelon form, and then solving for each unknown in reverse order …
   for a total of approximately 2n³/3 operations." Also confirming the *family*: "Problems that
   have the same asymptotic complexity as matrix multiplication include determinant, matrix
   inversion, Gaussian elimination" (*Computational complexity of matrix multiplication*), and
   the table in *Computational complexity of mathematical operations* lists "Schoolbook matrix
   multiplication O(n³)" alongside Strassen / Coppersmith–Winograd — the slide's phrase "the
   **standard** matrix inversion algorithm" correctly picks the textbook O(n³) member of that
   family.
4. **The worked example, arithmetic-confirmed.** "if Features vector is of size 1000 then
   Inverse calculation is or order 1,000,000,000". With the intercept, the moment matrix is
   1001 × 1001; the leading term is n³ = 1.001×10⁹ ≈ 10⁹, and the Gaussian-elimination count
   cited above is ≈ 2n³/3 ≈ 6.7×10⁸. Either way the slide's "of order 1,000,000,000" is the
   right order of magnitude (10⁹-class cubic growth). The verbatim phrase "is or order"
   (apparent typo for "of order") is preserved exactly as transcribed — transcribed frame text
   is never edited by research.
5. **That gradient descent is an iterative alternative to the closed form, verbatim.**
   Wikipedia *Gradient descent*: "one starts with a guess x₀ for a local minimum of f, and
   considers the sequence x₀, x₁, x₂, … such that x_{n+1} = x_n − η_n∇f(x_n), n ≥ 0" — i.e.
   the slide's "use Gradient Descent iterative solution". CS229 likewise presents the normal
   equations as the *non-iterative* option against gradient descent ("Gradient descent gives
   one way of minimizing J. Let's discuss a second way of doing so, this time performing the
   minimization explicitly and **without resorting to an iterative algorithm**").

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The four-box pedagogical architecture (green Recall / blue complexity / plain example /
  yellow Solution) and its coloured fills (#E2EFDA, #DDEBF7, #FFF2CC) — course chrome.
- The specific example size "1000" (both readings, 1000 vs 1001, give the same order of
  magnitude; the slide chose the round number) and the value 1,000,000,000.
- The comparative recommendation itself — "Instead of using Least Squares with Matrix
  inversion, use Gradient Descent iterative solution" — is the course's own pedagogical
  conclusion. Its two premises are source-confirmed (inversion is O(n³); gradient descent is
  iterative and needs no inverse). The sources confirm the premises, not the recommendation as
  a quoted directive; see [?] §1 for how far this worker could verify the comparative form.
- Word-level choices ("number of components" for n, the "Recall:"/"Solution:" labels, the
  apparent "or order" typo) are transcribed frame text.

## [?] Uncertain items

| # | Item | Status / resolution path |
|---|---|---|
| 1 | The comparative directive's exact standard form ("when d is large, prefer gradient descent") as an authoritative quote | **Partly resolved.** Premises confirmed verbatim (§3 and §5); however, the exact "prefer gradient descent when d is large" sentence was NOT found in either CS229 PDF fetched here, and CS229 only presents both methods. The agy search's synthesis for that claim was treated as a LEAD, not a source. Verified alternatives: CS229 notes2021 (closed form + "without resorting to an iterative algorithm"), Wikipedia Gaussian elimination (O(n³)), Wikipedia Gradient descent (iterative update rule). Recorded as an attempt log so the orchestrator can bank the search-Lead in the do-not-reuse section if it wants; no claim in this record depends on it. |
| 2 | Whether "Features vector is of size 1000" means d = 1000 exactly (moment matrix 1001×1001) or 1000 columns including the intercept | Both readings → 10⁹-class cost (§4); immaterial to the frame. Recorded, not guessed. |
| 3 | Exact font point sizes / box geometry / margin widths | Frame-only estimates from the analysis record; not web-resolvable. |

## Corrections

**None.** Every external claim on this frame — the estimator, the (d+1)×(d+1) dimension, the
O(n³) cost, the iterative nature of gradient descent — is confirmed verbatim by the sources
above, and the example arithmetic checks out. No dimension or provenance annotation in
`analysis/slide_023_final.json` is contradicted. No `analysis/*.json` file was edited by this
worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
