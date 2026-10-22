# SOURCES.md — slide 021 "Inverse Problem of Singular Matrix"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search (MCP `agy_web_search`) for discovery + live `curl -sL` fetch of every URL recorded
below in this same work window + **independent local re-derivation of every number on the
slide in NumPy**. Frame facts come from the slide's vision-analysis record
(`analysis/slide_021_final.json`, verdict PASS_WITH_FIXES, recreatability 9). **No vision
calls were made by this worker.** (A local image read of `unique_slides/slide_021.jpg` was
attempted but image rendering is unavailable to this worker, so all frame facts are from the
analysis record.)
Query economy: **no new query spent on this slide** — all claims are covered by the cluster's
anchor sources, fetched live and banked in `sources/slide_019_source/SOURCES.md` and
`sources/slide_020_source/SOURCES.md` (this worker, same work window).

## Slide identity

- Frame file: `unique_slides/slide_021.jpg` (960×540), md5 `557d14e06840c67f2eebc1df964a8565`
  (matches `_meta._reconcile_md5_snapshot`). Badge numeral **21**.
- Numbering resolution: founder-curated numbering 2026-10-19; pre-curation state
  intentionally unrecoverable. `_meta` records `precuration_slide = 93` (kept frame
  `frame_02327.jpg`, t = 2326 s, `provenance: "founder-curated kept frame"`). File number 021
  and badge "21" agree; pre-curation 93 is historical only.
- Analysis record used: `analysis/slide_021_final.json` (validated by glm-5.3, 426.1 s).

## Primary source(s)

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Invertible_matrix` | **"Invertible matrix"** — the invertibility/determinant/rank criteria the slide's two conclusion chains ("Singular Matrix ⇒ No Inverse", "Non-Singular Matrix ⇒ Inverse Exists") rest on. | **CONFIRMED** — fetched live this window, HTTP 200, 440,221 bytes, no redirect. Banked with quotes in `sources/slide_020_source/SOURCES.md` (this worker). **No new query spent.** |
| `https://en.wikipedia.org/wiki/Ridge_regression` | **"Ridge regression"** — the λI diagonal shift the slide applies to produce the non-singular matrix. | **CONFIRMED** — fetched live this window, HTTP 200, 475,413 bytes. Banked in `sources/slide_019_source/SOURCES.md` (this worker) and `sources/slide_010_source/SOURCES.md` (sibling). **No new query spent.** |
| `https://cs229.stanford.edu/notes2021fall/cs229-notes1.pdf` | Stanford **CS229 Part I notes (2021 fall)** — the standard statement that XᵀX is not invertible when examples/features are linearly dependent. | **CONFIRMED** — fetched live this window, HTTP 200, 357,392 bytes (`pdftotext`-extracted). Banked in `sources/slide_020_source/SOURCES.md` (this worker). **No new query spent.** |

No URL above was recorded from an unfetched snippet; all three were re-fetched live in this
work window.

## Figures used by this slide

**None — and correctly so.** The slide is three stacked blue-outlined panels containing 3×3
matrix *tables* (typed, not plotted) with arrows between the determinant → conclusion chain.
There is no chart, image or reused source figure: `imagery: []` is correct and the
recreation brief builds everything from text/table/shape primitives. The nearest hosted
originals for the topic are the Wikipedia article pages themselves (text-only), which carry no
figure this slide reuses. Per the layout law the reason is stated rather than left silent.

## What the source(s) CONFIRM

### A. The general theory (source-confirmed)

1. **det ≠ 0 ⇔ non-singular ⇔ inverse exists** — the slide's two right-arrow chains. Verbatim
   (*Invertible matrix*):
   > "For a real matrix, this is reflected by its determinant: an invertible matrix has
   > nonzero determinant, while a matrix with determinant zero collapses volume to zero and
   > is not invertible."

   The slide's top chain `|XᵀX| = 0 ⇒ Singular Matrix ⇒ No Inverse` and middle chain
   `|XᵀX| = 5685 ⇒ Non-Singular Matrix ⇒ Inverse Exists` are exactly these two cases.
2. **The rank/linear-dependence reason a regression XᵀX can be singular.** Verbatim
   (*Invertible matrix*): "Equivalently, an n × n matrix is invertible if its rank is n … Such
   a matrix is said to be of full rank." Verbatim (CS229 2021, footnote 3):
   > "If either the number of linearly independent examples is fewer than the number of
   > features, or if the features are not linearly independent, then XᵀX will not be
   > invertible."

3. **Adding λI to the diagonal is what produces the non-singular matrix.** Verbatim
   (*Ridge regression*): "the problem of a near-singular moment matrix XᵀX is alleviated by
   adding positive elements to the diagonals, thereby decreasing its condition number" and
   "the ridge (or Tikhonov) regularization parameter λ ≥ 0 serves as the constant shifting the
   diagonals of the moment matrix." The slide's `(XᵀX + λI)` with `λ=3` and its yellow
   diagonal highlights on entries 17, 43, 95 are a direct rendering of that shift
   (14+3 = 17, 40+3 = 43, 92+3 = 95 — each highlighted cell is exactly the original diagonal
   plus 3; verified locally).

### B. Every number on the frame (independently re-derived, NumPy, this worker)

4. **`det([[14,10,15],[10,40,46],[20,80,92]]) = 0` exactly.** NumPy:
   `np.linalg.det(...) = -6.28e-16` (zero to floating point); eigenvalues
   `[1.353e2, 1.070e1, -6.28e-16]`; `matrix_rank = 2` (of 3). So the slide's claim
   **`|XᵀX| = 0` is exactly correct.** The singularity is also visible structurally:
   Row 3 = 2 × Row 2 (check: 2·(10, 40, 46) = (20, 80, 92) — holds exactly).
5. **`det([[17,10,15],[10,43,46],[20,80,95]]) = 5685`.** NumPy: `det = 5684.999999999997`,
   i.e. **5685 as printed**. And the highlighted diagonal is exactly the original diagonal
   shifted by λ=3 (14→17, 40→43, 92→95), matching the slide's `λ=3` note.
6. **The bottom table is (XᵀX + λI)⁻¹, correctly rounded.** NumPy `inv` of the λ=3 matrix is
   ```
   [[ 0.07124011  0.04397537 -0.03254178]
    [-0.00527704  0.23131047 -0.11116974]
    [-0.01055409 -0.20404573  0.11099384]]
   ```
   Rounded to two decimals this is **exactly**
   `[[0.07, 0.04, -0.03], [-0.01, 0.23, -0.11], [-0.01, -0.2, 0.11]]` — the printed inverse
   matrix, with **max deviation 0.0** after rounding. All 9 numerals verify.
7. **Regularisation restores full rank.** `matrix_rank([[17,10,15],[10,43,46],[20,80,95]]) = 3`
   and all three eigenvalues are positive `[0.694, 13.876, 140.430]` — i.e. the λ=3 matrix is
   positive definite, consistent with "Non-Singular Matrix ⇒ Inverse Exists".

### C. One structural observation (recorded for understanding, NOT a correction)

8. **The printed example matrices are NOT symmetric, so they cannot literally be Gram
   matrices XᵀX of real data.** XᵀX is always symmetric, but the printed matrix has
   `[0][2] = 15` while `[2][0] = 20`. Two checks prove this is what the slide really prints,
   and not a transcription slip:
   - The printed inverse is *asymmetric* (`0.0440` at (0,1) vs `-0.0053` at (1,0)); a
     symmetric matrix's inverse is necessarily symmetric, so the printed inverse belongs to a
     non-symmetric matrix.
   - The inverse of the **symmetric** variant (the transpose, `[[14,10,20],[10,40,80],[15,46,92]]`)
     rounds to the **transpose** of the printed inverse (`[[0.07,-0.01,-0.01],[0.04,0.23,-0.2],
     [-0.03,-0.11,0.11]]`), not to the printed one.
   So the slide uses constructed illustrative matrices rather than a real design matrix's Gram
   matrix. This does not affect any claim it demonstrates: the determinant zeros, the 5685, the
   λ=3 diagonal shift, and the printed inverse are all numerically exact for the matrices as
   printed. **Frame wins for recreation — the numbers are drawn exactly as printed.**

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The specific example matrices themselves (the 14/10/15 … and 17/10/15 … tables) and the
  chosen λ=3 — course-chosen demo numbers, no source counterpart.
- The yellow diagonal highlight cells, the red italic conclusions, the `λ=3` green annotation
  and the blue panel outlines/#F2F2F2 fills — course chrome.
- The "small diagonal slash artifact visible near 15" in the top matrix, which the analysis
  record itself flags as a video artifact and the recreation brief's step 6 explicitly excludes.
- The serif (Cambria/Times-like) typeface choice, the panel geometry, and the title #8B0000.
- The choice to show the linear-algebra fact λ(≥) ⇒ invertible through a determinant reading
  rather than through eigenvalues/condition number — pedagogy; the source states the same fact
  ("decreasing its condition number").

## [?] Uncertain items

| # | Item | Status / resolution path |
|---|---|---|
| 1 | The exact data matrix X that produced the printed XᵀX (no real X can, see §8) | **Resolved as a non-question for research purposes.** The slide's matrices are illustrative constructions; no real design matrix is recoverable and none is claimed on the frame. The demo's arithmetic verifies exactly (§4–§6), so nothing is left open for the build. |
| 2 | Whether the top matrix's `15` and the third row's `20` were swapped in the video (i.e. the course intends a symmetric matrix) | **Resolved by local arithmetic, not by assertion:** the printed inverse proves the slide prints the non-symmetric form (§8). Recorded as an observation for understanding; NOT patched (frame wins). |
| 3 | Exact point sizes, exact panel coordinates | Frame-only estimates from the analysis record; not web-resolvable. |
| 4 | Exact serif typeface ("Cambria/Times-like") | Frame-only; carried by the build stage. |

## Corrections

**None.** Every numeric claim on this frame was re-derived and found correct (§4–§6), so no
annotation in `analysis/slide_021_final.json` is contradicted by any source or by local
arithmetic. The non-symmetry of the example matrices (§8) is an observation about the course's
*choice of demo numbers*, which is transcribed frame text and course-authored content — it is
recorded here, deliberately **not** patched into the analysis JSON, and it must not be "fixed"
toward symmetry by a builder. No `analysis/*.json` file was edited by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
