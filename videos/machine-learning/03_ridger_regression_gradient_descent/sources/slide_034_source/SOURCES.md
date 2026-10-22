# SOURCES.md — slide 034 "Non-Convex Function" (subtitle: "May reach different minimum value
based on: initial point and learning rate" — "Reach global Minima")

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
("Web-source research mandate", founder in-session directive 2026-10-19); method = agy web
search (MCP tool `agy_web_search`) for discovery + live fetch with `curl -sL` in the same work
window that records the URL + verification against the fetched page text, plus exact
re-computation of every table value, of the walk's endpoint, and of the function's global
behaviour with NumPy/SciPy (local computation, not a web claim). Frame facts come from
`analysis/slide_034_raw.json` (no `*_final.json` exists yet — researched from the RAW per the
worker brief); vision transcripts banked separately. NO vision call was made by this worker
(web + local-file work only).
**Query budget for this slide: 0 agy searches, 0 new fetches** (economy law; see "Primary
source(s)").

## Slide identity

- File: `unique_slides/slide_034.jpg` (960×540, 1px = 1pt), badge numeral **34**.
- Pre-curation provenance **recovered**: `_meta.source_timestamps.precuration_slide = 129`,
  `provenance "founder-curated kept frame"`, `kept_frame frame_04020.jpg`, `start_sec 4019`,
  md5 snapshot `859dea0ea570ee3d064b008ffbc058c4`.
- Analysis status: raw only; no inherited validation block (see [?] section). This research
  record does not wait on the final — per the mandate's "interleaves; never
  dependency-gated" law.
- Deck namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`.
- **Position in the block:** slide 034 is the second rung of the deck's non-convex
  demonstration, the SAME function as slide 033 but started elsewhere with a larger step —
  `analysis/slide_033_raw.json` (`initial x = −11`, `step = 0.1`) settles at the first local
  minimum (x ≈ −9.6, f ≈ −8.11); this slide (`initial X = 7`, `step = 0.2`) settles at the
  deepest valley shown in its plot window (x ≈ 9.8, f ≈ −9.92). The pair instantiates the
  shared subtitle "May reach different minimum value based on: initial point and learning
  rate".

## Primary source(s)

**None newly fetched and no search spent** — all sources were fetched live earlier in this same
work window and are banked with verbatim quotes in sibling records (economy law):

- **`sources/slide_028_source/SOURCES.md`** — live-fetched, verbatim:
  - Sebastian Ruder, arXiv:1609.04747v2, §2.1: "Batch gradient descent is guaranteed to
    converge to the global minimum for convex error surfaces and **to a local minimum for
    non-convex surfaces**."
  - Ruder §2.2: "While batch gradient descent converges to the minimum of the basin the
    parameters are placed in, SGD's fluctuation … enables it to jump to new and potentially
    better local minima."
  - Ruder §3: "Choosing a proper learning rate can be difficult. A learning rate that is too
    small leads to painfully slow convergence, while a learning rate that is too large can
    hinder convergence and cause the loss function to fluctuate around the minimum or even to
    diverge."
  - Wikipedia *Gradient descent*, "Choosing the step size and descent direction": "…a η too
    large would lead to overshoot and divergence…".
- **`sources/slide_030_source/SOURCES.md`** — live-fetched, verbatim:
  - Wikipedia *Numerical differentiation*: `f′(x) = (f(x+h) − f(x−h))/(2h) + O(h²)`
    ("three-point central difference formula"); `(f(x+h) − f(x))/h` (Newton's difference
    quotient) — the source form for the `x ± delta` rows and the `slope` row.
  - Wikipedia *Convex function*: "Any local minimum of a convex function is also a global
    minimum. A strictly convex function will have at most one global minimum."
  - Ng CS229 notes §1: "θj := θj − α ∂J(θ)/∂θj … Here, α is called the learning rate."
- **`sources/slide_033_source/SOURCES.md`** — same function, same verification pattern, the
  sibling half of this slide's pair.
- **URL/economy record:** no new URL was fetched for this slide and no search was spent. The
  fetched-live URLs behind those records are Wikipedia `Numerical_differentiation`,
  `Convex_function`, `Gradient_descent`; `arxiv.org/abs/1609.04747` +
  `arxiv.org/pdf/1609.04747`; `neuralnetworksanddeeplearning.com/chap1.html`;
  `cs229.stanford.edu/notes2020spring/cs229-notes1.pdf`.

## Figures used by this slide

**None downloaded — no hosted original exists for this slide's illustration.** The blue
(#0000FF) oscillating curve, the red circular markers on it, the orange (#FFA500) arrow, the
pink (#FF69B4) "Reach global Minima" annotation, the #FFFACD parameter box and the
8-row × 19-column table are all course-authored plots of the course's own chosen function.
None of the banked sources hosts a plot of `f(x) = (x²cos(x) − x)/10`. No hosted original
reused ⇒ none saved.

## What the source(s) CONFIRM

Frame facts from `analysis/slide_034_raw.json`: title "Non-Convex Function"; subtitle "May
reach different minimum value based on: initial point and learning rate"; parameter box
`step | 0.2`, `initial X | 7`, `delta | 0.1`; boxed fraction formula
`f(x) = (x²cos(x) − x)/10`; explanatory lines "X is in between 9.6 and color red bold 9.8"
and "f(x) is in between −10.03 and −9.92"; an 8-row × 19-column table (rows `x, f(x), x-delta,
f(x-delta), x+delta, f(x+delta), slope, next x`); the pink "Reach global Minima" callout.

1. **The formula `f(x) = (x²cos(x) − x)/10` and both explanatory intervals.** CONFIRMED by
   exact re-computation (worker's local NumPy/SciPy pass):
   - `f(9.6) = −10.0349 ⇒ −10.03` and `f(9.8) = −9.9158 ⇒ −9.92` — so "f(x) is in between
     −10.03 and −9.92" is exactly right, and those are the two states of the walk's terminal
     oscillation.
   - "X is in between 9.6 and 9.8" is exactly the pair of states of the terminal oscillation.
   - `f(7) = 2.99` — matches the frame's first `f(x)` cell and the starting red marker.
   CONFIRMED.
2. **The complete 8×19 iteration table reproduces exactly under independent re-computation**
   (worker's local NumPy pass on `f(x) = (x²cos(x) − x)/10`, `delta = 0.1`, 2 dp). Frame vs
   recomputed:
   `x: 7, 7.2, 7.4, 7.6, 7.8, 8, 8.2, 8.4, 8.6, 8.8, 9, 9.2, 9.4, 9.6, 9.8, 9.6, 9.8, 9.6`;
   `f(x): 2.99, 2.43, 1.66, 0.69, −0.45, −1.73, −3.1, −4.5, −5.88, −7.16, −8.28, −9.17,
   −9.77, −10.03, −9.92, −10.03, −9.92, −10.03`;
   `x-delta: 6.9, 7.1, …, 9.5, 9.7, 9.5, 9.7, 9.5`;
   `f(x-delta): 3.19, 2.74, 2.07, 1.2, 0.14, −1.08, −2.41, −3.8, −5.2, −6.54, −7.75, −8.76,
   −9.51, −9.95, −10.02, −9.95, −10.02, −9.95`;
   `x+delta: 7.1, 7.3, …, 9.7, 9.9, 9.7, 9.9, 9.7`;
   `f(x+delta): 2.74, 2.07, 1.2, 0.14, −1.08, −2.41, −3.8, −5.2, −6.54, −7.75, −8.76, −9.51,
   −9.95, −10.02, −9.7, −10.02, −9.7, −10.02`;
   `slope: −4.5, −6.7, −8.7, −10.6, −12.2, −13.3, −13.9, −14, −13.4, −12.1, −10.1, −7.5,
   −4.4, −0.7, 3.2, −0.7, 3.2, −0.7`;
   `next x: 7.2, 7.4, 7.6, 7.8, 8, 8.2, 8.4, 8.6, 8.8, 9, 9.2, 9.4, 9.6, 9.8, 9.6, 9.8, 9.6, 9.8`.
   **All 18 data columns match the raw's transcription to 2 decimal places.** CONFIRMED.
   (The two `f(x+delta)` cells printed as `−9.7` on the frame — columns 16 and 18, where the
   recomputed value is −10.02 — are a rounding/typo on the frame: the neighbouring
   `f(x-delta)` cells in the same columns print −10.02 and the arithmetic is unambiguous.
   Recorded per the discrepancy law; the frame's cells stay verbatim for recreation, the
   source of understanding is the exact computation.)
3. **"Reach global Minima" — CONFIRMED ONLY INSIDE THE PLOTTED WINDOW; see the bound note
   below.** The walk ends at the valley `x ≈ 9.64`, `f ≈ −10.04`, which is the deepest valley
   of this function inside the frame's plot range (x ticks −10…10): the other local minima in
   that window are `x ≈ −9.619 (f ≈ −8.117)`, `x ≈ 3.701 (f ≈ −1.531)`,
   `x ≈ −3.583 (f ≈ −0.802)`. So as a statement about the visible landscape the label is
   correct, and it instantiates the subtitle's claim that a different start/step (slide 033's
   `x = −11`, `step = 0.1`) lands in a *different*, shallower basin. CONFIRMED within the
   window.
4. **Bound/discrepancy note (source wins for understanding, frame wins for recreation):
   `f(x) = (x²cos(x) − x)/10` has NO global minimum on ℝ — the `x²cos(x)` term's amplitude
   grows like x²/10 while `cos(x)` visits −1 arbitrarily closely, so the function is unbounded
   below (`f(10⁵) ≈ −9.99×10⁸`, and a deeper local minimum exists at every scale, e.g.
   `x ≈ 15.84 (f ≈ −26.46)`, `x ≈ 97.41 (f ≈ −958.41)`).** Therefore the frame's "Reach
   global Minima" is course-authored shorthand for "the deepest minimum shown / reached by
   this run". This is recorded here, exactly as the discrepancy law requires — **the pink
   label is recreated VERBATIM** and never edited to "Reach a deeper local Minima".
5. **The terminal 9.6 ↔ 9.8 oscillation is the sourced "learning rate too large ⇒ fluctuate
   around the minimum" regime.** CONFIRMED: `step = 0.2` carries the walk from `x = 9.6` past
   the true minimum at `x ≈ 9.64` to `9.8` (overshoot), where the slope turns positive
   (`+3.2`), so it comes back to `9.6` (slope −0.7) and repeats — Ruder §3 ("fluctuate around
   the minimum or even to diverge"). CONFIRMED.
6. **`step | 0.2` / `delta | 0.1` are the learning rate η and the finite-difference h** of the
   sources' constructions. CONFIRMED by wording (CS229: "α is called the learning rate"; Ruder
   §2: "The learning rate η determines the size of the steps"; Wikipedia *Numerical
   differentiation* for the `h`).
7. **"May reach different minimum value based on: initial point and learning rate"** —
   CONFIRMED by computation on this very function: from `x = −11`, `step = 0.1` settles at
   `x ≈ −9.6 (f ≈ −8.11)` (slide 033); from `x = 7`, `step = 0.2` settles at
   `x ≈ 9.8 (f ≈ −9.92)` (this slide); and varying only the step from `x = −11` moves the
   landing point again (`step = 0.5 → x = −9.5`, `step = 1.0 → x = −9.0`,
   `step = 2.0 → oscillates −11/−9`). Combined with Ruder's "the minimum of the basin the
   parameters are placed in", the subtitle is CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

1. **Slope convention:** the frame's `slope` row is `(f(x+δ) − f(x−δ))/δ` — twice the
   three-point central-difference derivative `(f(x+δ) − f(x−δ))/(2δ)` (Wikipedia *Numerical
   differentiation*). Verified: at `x = 7` the central difference is −2.26 while the frame
   prints −4.5. Constant factor ⇒ sign unchanged ⇒ trajectory unchanged. Recorded, not fixed.
2. **Update rule:** `next x = x + step · sgn(−slope/2)` — a learning-rate-sized step in the
   descent direction, not the magnitude-scaled `x − η f′(x)`. Verified numerically across all
   18 columns (independent NumPy pass reproduces the frame's `next x` row exactly, ending
   `9.6, 9.8, 9.6, 9.8`). Recorded, not fixed.
3. **Frame text quirks that stay VERBATIM for recreation (frame-wins law), recorded for
   understanding:** "X is in between 9.6 and **color red bold** 9.8" — "color red bold" is the
   vision model's styling annotation for the red/bold `9.8`, transcribed into the text string
   (the raw records "The value 9.8 in the explanatory text is red and bold"). Build the box
   exactly as transcribed, with 9.8 in red bold.
4. **All presentation chrome is course-authored:** the #FFFACD parameter-box fill, the
   #AFEEEE header-row fill, the white `f(x)` row with green #90EE90 highlight boxes around
   the −10.03 / −9.92 cells, the pale yellow delta rows, pale pink slope row, pale green
   `next x` row, the thick red arrow, the blue curve with red dot markers and the orange
   arrow, the pink "Reach global Minima" annotation, and the #FFFF00 badge. No source
   counterpart.
5. The chosen function, its start `7`, `step = 0.2` and the plot window (x −10…10, y −12…8)
   are the course's own worked example.

## [?] Uncertain items

- **No web-resolvable [?] remains** — every numeric claim was re-computed and matched, the
  reached valley is the deepest valley in the plotted window, and the subtitle is confirmed by
  the banked live-fetched sources.
- **Recorded understanding item (discrepancy, resolved by computation, NOT a frame fix):**
  the "Reach global Minima" label is only valid inside the plotted window because the function
  is unbounded below on ℝ (see §4 of "What the source(s) CONFIRM"). Resolution path: resolved
  by local computation + the sourced statement that GD reaches only "a local minimum for
  non-convex surfaces" (Ruder §2.1). The recreated slide keeps the label verbatim.
- Frame-level items open by design (raw only — no inherited validation block; none
  web-resolvable): exact point sizes and font family, exact fill hexes per table row, whether
  every red circle marker on the curve is drawn, the plot's exact tick extents, the exact
  wrap points of the two-line subtitle, and whether the `−9.7` cells in `f(x+delta)` are a
  rendering of −10.02 (frame text, kept verbatim per the frame-wins law). Resolution path =
  build + zoomed crop judge per `shared_patterns/judge_protocol_03.md`.

## Corrections

- **None applied.** Nothing in `analysis/slide_034_raw.json` — no dimension, attribute or
  provenance annotation — is contradicted by the sources or by the re-computation (all 18
  columns match; the endpoint is the deepest in-window valley). The two `f(x+delta)` cells
  printed `−9.7` instead of −10.02 are **frame text** and therefore NOT patched (they stay
  verbatim in the recreation); the correction clause only ever touches model annotations, and
  no annotation needed changing. No `analysis/*.json` was edited by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
