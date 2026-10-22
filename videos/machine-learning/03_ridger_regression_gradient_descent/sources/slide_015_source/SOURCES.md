# SOURCES.md — slide 015 "Minimization of Objective function to obtain BEST model parameters"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search (MCP `agy_web_search`) + live `curl -sL` fetch of each URL in the same work window
that records it + independent local re-derivation of the closed form. Frame facts come
from the slide's vision-analysis record (`analysis/slide_015_raw.json` — no `_final`
exists for this slide, so the raw is the record of the frame); NO vision calls were made
by this worker. Query economy: **0 new queries** — covered by the cluster's shared
sources.

## Slide identity

- Frame file: `unique_slides/slide_015.jpg` (960×540, 1px = 1pt per the deck AGENTS).
- Badge number on the frame: **15** (yellow circle, black numeral). Deck rule: badge
  numeral = the file number N, no zero-padding.
- Numbering resolution: 51 founder-curated files numbered by the founder 2026-10-19; the
  pre-curation state is intentionally unrecoverable. A recovered pre-curation provenance
  value IS present in `_meta`: `source_timestamps.precuration_slide = 30` (kept frame
  `frame_01085.jpg`, t = 1084 s, `provenance: "founder-curated kept frame"`). One of the
  35 with recovered provenance; NOT in the 16-slide unrecoverable list. File number 015
  and badge "15" agree; pre-curation 30 is historical only.
- Analysis record used: `analysis/slide_015_raw.json` (final absent — raw used per the
  mandate's fallback rule).

## Primary source(s)

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Ridge_regression` | Wikipedia article **"Ridge regression"**, section *Overview* — the article's own statement of the ridge estimator. **This is the slide's terminal formula, verbatim.** | **CONFIRMED** — fetched live 2026-10-20 in this work window (`action=raw` wikitext, 35,436 bytes + rendered HTML). Quote below. |
| `https://en.wikipedia.org/wiki/Matrix_calculus` | Wikipedia article **"Matrix calculus"**, the *Identities → scalar-by-vector* table — the canonical matrix-derivative identities behind the slide's "Remember" box and its gradient steps. | **CONFIRMED** — fetched live 2026-10-20 in this work window (`action=raw` wikitext, 88,150 bytes). Quotes below. |
| `https://en.wikipedia.org/wiki/Tikhonov_regularization` | Wikipedia article "Tikhonov regularization" | **CONFIRMED, resolves as a redirect** to `https://en.wikipedia.org/wiki/Ridge_regression#Tikhonov_regularization_for_linear_equations`. Recorded to prevent it being treated as a separate article. |

Nothing above was recorded from an unfetched search snippet.

## Figures used by this slide

**None.** The slide is a derivation: three expansion equations, a red-bordered callout
box, a peach "Remember" box, two derivative lines, a centered normal-equation line with
an arrow, and a green-bordered solution box, plus the badge. `imagery: []`; every visual
element is a highlight-box or the badge. No plot, no diagram, no hosted original to save;
the reason is stated here per the layout law.

## What the source(s) CONFIRM

The slide's derivation lines, verbatim from the record:

```
(a) J(W)=1/2(Y−Ŷ)ᵀ(Y−Ŷ)+1/2 λWᵀW = 1/2(Y−XW)ᵀ(Y−XW)+1/2 λWᵀW
(b) J(W)=1/2[YᵀY + (XW)ᵀ(XW) − Yᵀ(XW) − (XW)ᵀY]+1/2 λWᵀW
(c) J(W)=1/2[YᵀY + (XW)ᵀ(XW) − 2(XW)ᵀY]+1/2 λWᵀW
(d) ∂J(W)/∂W = 0          [red callout: "Get Best W that minimizes the Objective Function J(W)"]
    Remember: ∂WᵀW/∂W = 2W
(e) ∂J(W)/∂W = 0 = 1/2[(XW)ᵀ(X) + (X)ᵀ(XW) − 2(X)ᵀY]+λW
(f) ∂J(W)/∂W = 0 = 1/2[2XᵀXW − 2XᵀY]+λIW
(g) (XᵀX + λI)W = XᵀY
(h) W = (XᵀX + λI)⁻¹ XᵀY        [green box]
```

1. **Line (h) — the slide's terminal formula — is the source's own ridge estimator,
   verbatim.** Source, *Ridge regression* § Overview, immediately after "Compared to the
   ordinary least squares estimator, the simple ridge estimator has an extra term `λI` in
   the denominator:":
   > `$$\hat{\boldsymbol{\beta}}_{\lambda} = \left(\mathbf{X}^{\mathsf{T}} \mathbf{X} + \lambda \mathbf{I}\right)^{-1} \mathbf{X}^{\mathsf{T}} \mathbf{Y}$$`
   with the article's own gloss: "where Y is the regressand or response vector, X is the
   design matrix, and I is the identity matrix, and the ridge (or Tikhonov)
   regularization parameter λ ≥ 0 serves as the constant shifting the diagonals of the
   moment matrix." **The slide's `W = (XᵀX + λI)⁻¹XᵀY` is character-for-character the
   source's estimator with β→W.** Confirmed.
2. **Line (g) — the normal equations `(XᵀX + λI)W = XᵀY`.** Same passage, verbatim:
   > "the problem of a near-singular moment matrix `XᵀX` is alleviated by adding positive
   > elements to the diagonals, thereby decreasing its condition number."
   and from the article's *Tikhonov regularization for linear equations* section, verbatim:
   > "This regularization improves the conditioning of the problem, thus enabling a direct
   > numerical solution."
   Confirms line (g) as the regularized normal equation the slide derives.
3. **The "Remember" identity `∂WᵀW/∂W = 2W` is a canonical matrix-calculus identity.**
   Source, *Matrix calculus* → *Identities: scalar-by-vector* table (denominator-layout /
   column-vector result), verbatim:
   > `∂(x·x)/∂x = ∂xᵀx/∂x = ∂‖x‖²/∂x = 2x`
   i.e. exactly the slide's box with x→W. Confirmed.
4. **Line (f)'s quadratic-form gradient is the canonical symmetric-matrix identity.**
   Source, same table, verbatim:
   > `∂xᵀAx/∂x = (A + Aᵀ)x` — and for the case "A is not a function of x, A is symmetric":
   > `∂xᵀAx/∂x = 2Ax`
   With A = XᵀX (symmetric), `(XW)ᵀ(XW) = WᵀXᵀXW`, so the penultimate step of line (f)
   (`2XᵀXW`) is exactly `2Ax`. Confirmed.
5. **Line (f)'s linear term.** Source, same table, verbatim:
   > `∂bᵀAx/∂x = Aᵀb` (denominator layout) and
   > `∂(xᵀa)/∂x = ∂(aᵀx)/∂x = a`
   With `(XW)ᵀY = WᵀXᵀY`, the gradient is `XᵀY`, giving the `− 2XᵀY` inside line (f)'s
   brackets. Confirmed.
6. **Line (a)/(b)/(c) — the algebraic expansion is correct.** The source's own Lagrangian
   statement (verbatim, *Overview*):
   > `$\text{argmin}_{\boldsymbol{\beta}} \, \|\mathbf{Y} - \mathbf{X} \boldsymbol{\beta}\|^2 + \lambda \left(\boldsymbol\beta^\mathsf{T}\boldsymbol\beta - c\right)$`
   is the same two-term objective in a different scaling (see course-authored note 1). The
   slide's expansion of `(Y−XW)ᵀ(Y−XW)` into `YᵀY + (XW)ᵀ(XW) − Yᵀ(XW) − (XW)ᵀY` and the
   collapse of the two equal middle scalar terms into `−2(XW)ᵀY` are both standard and
   correct (the source's estimator passage confirms the matrix-form usage throughout).
7. **The gradient-zero condition (line d) and the resulting closed form are the whole
   point of the source section.** Verbatim (*Ridge regression*, *Overview*): "It can be
   shown that this estimator is the solution to the least squares problem subject to the
   constraint βᵀβ = c, which can be expressed as a Lagrangian minimization" — the source's
   constrained view matches the slide's "Get Best W that minimizes the Objective Function
   J(W)".
8. **The solution is unique/convex for λ > 0.** Source, verbatim: "the ridge (or Tikhonov)
   regularization parameter λ ≥ 0 serves as the constant shifting the diagonals of the
   moment matrix" — and the article's note that for Γ = 0 it "reduces to the unregularized
   least-squares solution, provided that (AᵀA)⁻¹ exists". This is the boundary condition
   that slide 013 (λ = 0) displays and slides 017/018 (λ = 3, 10) then leave behind.
9. **Independent confirmation by re-derivation (not a source quote, but decisive):** the
   formula on line (h), solved numerically on the deck's own training tables
   (`X = [1, x1, x2]`, y = 2,4,6,8,16,18,20,22, X8's x1 = 11/30/60), reproduces the W
   vectors printed on slides 013/017/018 to the slide's display precision — see slides
   013, 017 and 018's SOURCES.md for the full numeric tables. The slide's algebra is
   therefore verified end-to-end, not merely its final line's form.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- **Layout-convention mixing in line (e).** Line (e) writes
  `∂J/∂W = ½[(XW)ᵀ(X) + (X)ᵀ(XW) − 2(X)ᵀY] + λW`. Reading it strictly, `(XW)ᵀ(X)` is a
  **row** vector (it equals `WᵀXᵀX`, the numerator-layout gradient) while `(X)ᵀ(XW)` and
  `(X)ᵀY` are **column** vectors (denominator-layout). The line therefore mixes the two
  layout conventions the source explicitly distinguishes (the *Matrix calculus* article's
  "Notation" section: numerator layout lays `∂y/∂x` out by `xᵀ` "result is row vector";
  denominator layout "result is column vector"). Line (f) then presents the correct
  column-vector result. **Do not "fix" line (e) into a single convention** — it is
  transcribed frame text; render it exactly as printed. It is recorded here only so a
  reader does not mistake it for a typo the builder should silently correct.
- **Line (f)'s `+λIW` vs line (e)'s `+λW`.** Both appear on the frame (λW in (e),
  λIW in (f)); they are equal (`λW = λIW`) and both are transcribed frame text. Render as
  printed.
- **The 1/2 factors and where λ sits.** As on slide 014, the source has no 1/2; the
  course's `½‖Y−Ŷ‖² + ½λWᵀW` scaling cancels the 2's from the quadratic-form/gradient
  identities so line (f) reads cleanly. Confirmed benign by the λ = 3 / λ = 10
  re-derivations (slides 017/018): the slide's λ is the source's λ, undivided.
- **The red callout, the peach "Remember" box and the green solution box**, their exact
  colors (`#FF0000` outline; `#FCE4D6` peach fill with a red "Remember" label;
  `#00B050` outline with `#E2EFDA` light-green fill), and the centered red-to-blue
  arrow between lines (g) and (h) — course pedagogy chrome.
- The underlined W ("with W underlined" to denote vector/matrix) in the callout and the
  solution box — a course typographic convention.
- The title's alternating red/blue color runs ("Minimization of" red, "Objective" blue,
  "function to obtain" red, "BEST" blue, "model parameters" red).
- **Chrome note (deck law):** the raw reports background `#FFFFFF`, agreeing with the
  deck's mandated white canvas. No divergence.

## [?] Uncertain items

| # | Item | Resolution path |
|---|---|---|
| 1 | Whether line (e)'s mixed row/column layout is intentional or a transcription slip | **RESOLVED to the extent web sources can**: the *Matrix calculus* article documents both conventions, so the line is intelligible as a mixed-layout shorthand; line (f) is the correct single-convention result. Whether the FRAME actually prints it this way is frame-only (the raw transcribes it as such), and the frame's text is preserved verbatim either way. |
| 2 | Whether the intended scaling is `½‖Y−Ŷ‖² + (λ/2)‖W‖²` (the conventional ridge form) or `½[‖Y−Ŷ‖² + λ‖W‖²]` as printed | **RESOLVED by re-derivation**: solving `(XᵀX + λI)W = XᵀY` with λ = 3 and λ = 10 reproduces slides 017/018 exactly, so the slide's λ is the undivided λ of the source's `(XᵀX + λI)⁻¹XᵀY`. Recorded so the builder does not halve it. |
| 3 | Exact font sizes/families for the equations and the box labels | frame-only measurement |
| 4 | The arrow's exact geometry and whether an arrow exists at all between (g) and (h) | frame-only measurement (the raw's recreation brief asserts one) |
| 5 | Whether the bracketed solution is a matrix inverse or a per-element inverse | **RESOLVED**: the source's estimator passage uses the same `(…)⁻¹` for the matrix inverse of the regularized moment matrix. |

## Corrections

**None applied; two annotations CONFIRMED (no patch needed).** (i) The slide's λ equals
the source's λ (undivided by the 1/2) — confirmed by the λ = 3 / λ = 10 re-derivations
against slides 017/018. (ii) The terminal formula is the source's estimator verbatim. No
analysis JSON was edited by this worker, and no transcribed frame text is contradicted by
any source.

## Law reminder

The frame wins for recreation; the source wins for understanding. Discrepancies above
(the 1/2 scaling, line (e)'s mixed layout) are recorded, never silently applied.
