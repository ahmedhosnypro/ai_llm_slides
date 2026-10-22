# SOURCES.md — slide 033 "Non-Convex Function" (subtitle: "May reach different minimum value
based on: initial point and learning rate")

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
("Web-source research mandate", founder in-session directive 2026-10-19); method = agy web
search (MCP tool `agy_web_search`) for discovery + live fetch with `curl -sL` in the same work
window that records the URL + verification against the fetched page text, plus exact
re-computation of every table value and of the walk's endpoint with NumPy/SciPy (local
computation, not a web claim). Frame facts come from `analysis/slide_033_raw.json` (no
`*_final.json` exists yet — researched from the RAW per the worker brief); vision transcripts
banked separately. NO vision call was made by this worker (web + local-file work only).
**Query budget for this slide: 0 agy searches, 0 new fetches** (economy law; see "Primary
source(s)").

## Slide identity

- File: `unique_slides/slide_033.jpg` (960×540, 1px = 1pt), badge numeral **33**.
- Pre-curation provenance: **unrecoverable** — the raw's `_meta.source_timestamps` has no
  `kept_frame`/`precuration_slide`, only `provenance: "analysis pending; precuration id
  unrecoverable (owner removed frames/ + pre-curation state)"`, and slide 33 is on the deck
  AGENTS.md unrecoverable list (1,2,3,13,24–29,33,35,36,43,44,47). Expected gap, not an error.
- Analysis status: raw only; no inherited validation block (see [?] section). This research
  record does not wait on the final — per the mandate's "interleaves; never
  dependency-gated" law.
- Deck namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`.
- **Position in the block:** slide 033 opens the deck's non-convex demonstration with
  `f(x) = (x²cos(x) − x)/10`, `initial x = −11`, `step = 0.1`, `delta x = 0.1` → the walk
  settles in the FIRST local minimum (x ≈ −9.6). Its sibling slide 034 re-runs the SAME
  function from `initial X = 7` with `step = 0.2` and settles in the deepest in-view valley
  (x ≈ 9.8). Together they demonstrate the frame's own subtitle.

## Primary source(s)

**None newly fetched and no search spent** — all sources were fetched live earlier in this same
work window and are banked with verbatim quotes in sibling records (economy law):

- **`sources/slide_030_source/SOURCES.md`** — live-fetched, verbatim:
  - Wikipedia *Numerical differentiation*: `f′(x) = (f(x+h) − f(x−h))/(2h) + O(h²)` ("three-point
    central difference formula") and `(f(x+h) − f(x))/h` (Newton's difference quotient) — the
    source form for this slide's `x-delta` / `x+delta` rows and its `slope` row.
  - Wikipedia *Convex function*: "Any local minimum of a convex function is also a global
    minimum. A strictly convex function will have at most one global minimum." (the convex-side
    law that makes the *non*-convex contrast teachable).
- **`sources/slide_028_source/SOURCES.md`** — live-fetched, verbatim:
  - Sebastian Ruder, arXiv:1609.04747v2, §2.1: **"Batch gradient descent is guaranteed to
    converge to the global minimum for convex error surfaces and to a local minimum for
    non-convex surfaces."** — the direct source statement for this slide's headline.
  - Ruder §2.2: **"While batch gradient descent converges to the minimum of the basin the
    parameters are placed in, SGD's fluctuation, on the one hand, enables it to jump to new and
    potentially better local minima."** — the "different minimum depending on the initial
    point" half of the frame's subtitle.
  - Ruder §3: "Choosing a proper learning rate can be difficult. A learning rate that is too
    small leads to painfully slow convergence, while a learning rate that is too large can
    hinder convergence and cause the loss function to fluctuate around the minimum or even to
    diverge." — the "…and learning rate" half.
  - Wikipedia *Gradient descent* ("overshoot and divergence"); Ng CS229 notes §1
    (`θj := θj − α ∂J/∂θj`, "α is called the learning rate"); Nielsen *NNDL* ch.1.
- **URL/economy record:** no new URL was fetched for this slide and no search was spent. The
  fetched-live URLs behind those records are Wikipedia `Numerical_differentiation`,
  `Convex_function`, `Gradient_descent`; `arxiv.org/abs/1609.04747` +
  `arxiv.org/pdf/1609.04747`; `neuralnetworksanddeeplearning.com/chap1.html`;
  `cs229.stanford.edu/notes2020spring/cs229-notes1.pdf`.

## Figures used by this slide

**None downloaded — no hosted original exists for this slide's illustration.** The green
(#00B050) oscillating curve, the red/orange initial point near (−11, 1.15), the thick orange
(#ED7D31) arrow down to a green square marker at the first local minimum, the purple
(`#7030A0`) "Reach Local Minima" callout, and the 8-row × 16-column table are all
course-authored plots of the course's own chosen function. None of the banked sources hosts a
plot of `f(x) = (x²cos(x) − x)/10`. No hosted original reused ⇒ none saved.

## What the source(s) CONFIRM

Frame facts from `analysis/slide_033_raw.json`: title "Non-Convex Function"; subtitle "May
reach different minimum value based on: initial point and learning rate"; parameter box
`step | 0.1`, `initial x | −11`, `delta x | 0.1`; formula `f(x) = (x²cos(x) − x)/10`
rendered as a fraction; annotation "X is in between −9.7 and color red bold −9.6" and
"f(x) is in between −8.08 and −8.011"; an 8-row × 16-column table (rows `x, f(x), x-delta,
f(x-delta), x+delta, f(x+delta), slope, next x`); "Reach Local Minima".

1. **The headline "Non-Convex Function" and the subtitle "May reach different minimum value
   based on: initial point and learning rate".** CONFIRMED by the banked live-fetched sources:
   Ruder §2.1 — batch GD converges "to a local minimum for non-convex surfaces" (i.e. not
   necessarily the global one); Ruder §2.2 — batch GD "converges to the minimum of the basin
   the parameters are placed in", so where you start decides which basin you end in; Ruder §3 —
   the learning rate governs whether the walk fluctuates around that minimum or diverges.
   CONFIRMED.
2. **The formula `f(x) = (x²cos(x) − x)/10` and the entire annotation about the reached
   valley.** CONFIRMED by exact re-computation (worker's local NumPy pass):
   - `f(−11) = 1.1536 ⇒ 1.15` — matches the frame's first `f(x)` cell and the red initial
     point near (−11, 1.15).
   - `f(−9.6) = −8.1149 ⇒ −8.11`; `f(−9.7) = −8.08`; `f(−9.8) = −7.96` — so the stated
     intervals "X is in between −9.7 and −9.6" and "f(x) is in between −8.08 and −8.11" are
     exactly right, and the highlighted end of the oscillation is the table's `f(x) = −8.11`
     cell at `x = −9.6`.
   - The true local minimum of this function near that valley is at `x ≈ −9.619`,
     `f ≈ −8.1167` (SciPy local-minimum search on a dense grid) — i.e. the walk's endpoint
     is the genuine local minimum, so the purple "Reach Local Minima" callout is CORRECT.
     CONFIRMED.
3. **The complete 8×16 iteration table reproduces exactly under independent re-computation**
   (worker's local NumPy pass on `f(x) = (x²cos(x) − x)/10`, `delta x = 0.1`, values rounded
   to 2 dp). Frame vs recomputed:
   `x: −11, −10.9, −10.8, −10.7, −10.6, −10.5, −10.4, −10.3, −10.2, −10.1, −10, −9.9, −9.8,
   −9.7, −9.6, −9.5`;
   `f(x): 1.15, −0.04, −1.19, −2.26, −3.27, −4.19, −5.03, −5.77, −6.41, −6.95, −7.39, −7.72,
   −7.96, −8.08, −8.11, −8.05`;
   `x-delta: −11.1 … −9.6`;
   `f(x-delta): 2.39, 1.15, −0.04, −1.19, −2.26, −3.27, −4.19, −5.03, −5.77, −6.41, −6.95,
   −7.39, −7.72, −7.96, −8.08, −8.11`;
   `x+delta: −10.9 … −9.4`;
   `f(x+delta): −0.04, −1.19, −2.26, −3.27, −4.19, −5.03, −5.77, −6.41, −6.95, −7.39, −7.72,
   −7.96, −8.08, −8.11, −8.05, −7.89`;
   `slope: −24.3, −23.4, −22.2, −20.8, −19.3, −17.6, −15.8, −13.8, −11.8, −9.8, −7.7, −5.7,
   −3.6, −1.5, 0.3, 2.2`;
   `next x: −10.9, −10.8, −10.7, −10.6, −10.5, −10.4, −10.3, −10.2, −10.1, −10, −9.9, −9.8,
   −9.7, −9.6, −9.7, −9.6`.
   **All 16 data columns match the raw's transcription to 2 decimal places.** CONFIRMED.
4. **The walk's endpoint and its terminal oscillation.** CONFIRMED arithmetically: the walk
   runs monotonically down to `x = −9.6` (slope −1.5 at −9.7, +0.3 at −9.6) and then bounces
   `−9.7 ↔ −9.6` — i.e. the learning rate `step = 0.1` overshoots the true minimum at
   `x ≈ −9.619` by less than one step, producing a two-point oscillation. This is precisely
   the sourced "learning rate too large ⇒ fluctuate around the minimum" regime (Ruder §3),
   here on a non-convex surface.
5. **`step | 0.1` / `delta x | 0.1` are the learning rate η and the finite-difference h** of
   the sources' constructions. CONFIRMED by wording (CS229: "α is called the learning rate";
   Ruder §2: "The learning rate η determines the size of the steps"; Wikipedia *Numerical
   differentiation* for the `h`).

## Course-authored elements (no source counterpart — do NOT "fix" to source)

1. **Slope convention:** the frame's `slope` row is `(f(x+δ) − f(x−δ))/δ` — twice the
   three-point central-difference derivative `(f(x+δ) − f(x−δ))/(2δ)` (Wikipedia *Numerical
   differentiation*). Verified: at `x = −11` the central difference is −12.19 while the frame
   prints −24.3. Constant factor ⇒ sign unchanged ⇒ trajectory unchanged. Recorded, not fixed.
2. **Update rule:** `next x = x + step · sgn(−slope/2)` — a learning-rate-sized step in the
   descent direction, not the magnitude-scaled `x − η f′(x)`. Verified numerically across all
   16 columns (independent NumPy pass reproduces the frame's `next x` row exactly, including
   the terminal `−9.7, −9.6` oscillation). Recorded, not fixed.
3. **Frame text quirks that stay VERBATIM for recreation (frame-wins law), recorded for
   understanding:**
   - "X is in between −9.7 and **color red bold** −9.6" — the phrase "color red bold" is the
     vision model's styling annotation for the red/bold rendering of `−9.6`, transcribed into
     the text string (the raw itself records "−9.6 appear red/bold" and repeats the phrase in
     typography_notes). Build the box exactly as transcribed, with −9.6 in red bold.
   - "f(x) is in between −8.08 and **−8.011**" — the frame literally prints −8.011 while its
     own table cell shows −8.11; the true value is `f(−9.6) = −8.1149`. The raw records the
     literal print ("The second line literally shows −8.011 even though the table cell shows
     −8.11"). Recreate the frame's literal text; the understanding value is −8.11.
4. **All presentation chrome is course-authored:** the #FFFF00 parameter-box label fills, the
   pale row-band fills (#E2EFDA / #DDEBF7 / #E4DFEC / #FCE4D6), the red block arrow, the
   green curve + orange arrow + green-square local-minimum marker style, the purple
   "Reach Local Minima" rounded callout, the red bold highlighting of −9.6 / −8.11, and the
   #FFFF00 badge. No source counterpart.
5. The chosen test function `f(x) = (x²cos(x) − x)/10`, its start `−11`, `step = 0.1` and the
   plot window (x ticks −12…−2, y ticks 0…−10) are the course's own worked example.

## [?] Uncertain items

- **No web-resolvable [?] remains** — every numeric claim was re-computed and matched, the
  reached valley is the true local minimum, and the qualitative subtitle is confirmed by the
  banked live-fetched sources.
- **Understanding notes recorded (not frame bugs to fix):**
  1. `f(x) = (x²cos(x) − x)/10` is **not** bounded below on ℝ (the `x²cos(x)` term's amplitude
     grows like x²/10: `f(10⁵) ≈ −9.99×10⁸`). The "global minimum" framing on the sibling
     slide 034 therefore only holds within the plotted window — see
     `sources/slide_034_source/SOURCES.md`.
  2. The frame's claim that the reached minimum depends on the *learning rate* is
     numerically substantiable for this function under the course's sign-step rule: from
     `x = −11`, `step = 0.1` settles at `x ≈ −9.6` (f ≈ −8.11), `step = 0.5` settles at
     `x = −9.5` (f ≈ −8.05), `step = 1.0` settles at `x = −9.0` (f ≈ −6.48), and `step = 2.0`
     oscillates between −11 and −9 without settling. Resolution path: resolved here by
     computation; the frame's statement stands.
- Frame-level items open by design (raw only — no inherited validation block; none
  web-resolvable): exact point sizes, exact fill hexes for the row bands and the parameter
  box, whether the green-square marker at the local minimum is labelled, the plot's exact
  tick extents, and the styling boundaries of the two-line subtitle (raw: "initial point" in
  red, "learning rate" in blue). Resolution path = build + zoomed crop judge per
  `shared_patterns/judge_protocol_03.md`.

## Corrections

- **None applied.** Nothing in `analysis/slide_033_raw.json` — no dimension, attribute or
  provenance annotation — is contradicted by the sources or by the re-computation (all 16
  columns match, the endpoint is the true local minimum). No `analysis/*.json` was edited by
  this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
