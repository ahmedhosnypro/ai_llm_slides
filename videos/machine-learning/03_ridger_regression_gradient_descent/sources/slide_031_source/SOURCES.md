# SOURCES.md — slide 031 "Convex Function, Learning Rate =0.3, Start at X=3"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
("Web-source research mandate", founder in-session directive 2026-10-19); method = agy web
search (MCP tool `agy_web_search`) for discovery + live fetch with `curl -sL` in the same work
window that records the URL + verification against the fetched page text, plus exact
re-computation of every table value on the frame with NumPy (local computation, not a web
claim). Frame facts come from `analysis/slide_031_raw.json` (no `*_final.json` exists yet —
researched from the RAW per the worker brief; the frame wins for recreation either way); vision
transcripts banked separately. NO vision call was made by this worker (web + local-file work
only).
**Query budget for this slide: 0 agy searches, 0 new fetches — every source is already banked
live in this same work window** (economy law; see "Primary source(s)").

## Slide identity

- File: `unique_slides/slide_031.jpg` (960×540, 1px = 1pt), badge numeral **31**.
- Pre-curation provenance **recovered**: `_meta.source_timestamps.precuration_slide = 126`,
  `provenance "founder-curated kept frame"`, `kept_frame frame_03818.jpg`, `start_sec 3817`,
  md5 snapshot `e7d73945948d25437fe961106e18dfd9`.
- Analysis status: `analysis/slide_031_raw.json` only (raw exists; the final/validation record
  has not been produced yet — this research record does not wait on it, per the
  "interleaves, never dependency-gated" law). No `uncertain_items` block is available yet, so
  the [?] section below carries only the research-derived items and the frame-level items
  visible in the raw.
- Deck namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`.
- **Position in the block:** slide 031 is the middle rung of the deck's learning-rate sweep on
  the SAME convex function — `analysis/slide_030_raw.json` (η = 0.2 → reaches the minimum in 11
  columns), slide 031 (η = 0.3 → **overshoots and oscillates**), `slide_032_raw.json`
  (η = 0.4 → still reaches the minimum in 6 columns). Its sources are the banked records of
  slides 028 and 030, not new queries.

## Primary source(s)

**None newly fetched and no search spent — all four sources were fetched live earlier in this
same work window and are banked, with verbatim quotes, in the sibling records below.** Per the
source-research.md economy law ("Reuse banked records: if a sibling slide's SOURCES.md already
covers the claim, cross-reference it and note 'no new query spent'"):

- **`sources/slide_028_source/SOURCES.md`** — the learning-rate trade-off, live-fetched:
  - Wikipedia *Gradient descent*, "Choosing the step size and descent direction":
    > "Since using a step size η that is too small would slow convergence, and a η too large
    > would lead to overshoot and divergence, finding a good setting of η is an important
    > practical problem."
  - Sebastian Ruder, arXiv:1609.04747v2, §3:
    > "Choosing a proper learning rate can be difficult. A learning rate that is too small
    > leads to painfully slow convergence, while a learning rate that is too large can hinder
    > convergence and cause the loss function to fluctuate around the minimum or even to
    > diverge."
  - Michael Nielsen, *Neural Networks and Deep Learning* ch.1:
    > "…we don't want η to be too small… At the same time [if not small enough] we might end
    > up with ΔC > 0, which obviously would not be good!"
  - Ng CS229 notes §1: "θj := θj − α ∂J(θ)/∂θj … Here, α is called the learning rate."
- **`sources/slide_030_source/SOURCES.md`** — the function/table machinery of this slide, also
  live-fetched in the same window:
  - Wikipedia *Numerical differentiation*: `f′(x) = (f(x+h) − f(x−h))/(2h) + O(h²)` (the
    "three-point central difference formula") and `(f(x+h) − f(x))/h` (Newton's difference
    quotient) — the source form for the `x ± delta` rows.
  - Wikipedia *Convex function*: "Any local minimum of a convex function is also a global
    minimum. A strictly convex function will have at most one global minimum."
  - Ruder §2.1: batch GD "is guaranteed to converge to the global minimum for convex error
    surfaces"; CS229: "J is a convex quadratic function… gradient descent always converges
    (assuming the learning rate α is not too large) to the global minimum."
- URL/economy note: because both records already hold the fetched-live URLs (Wikipedia GD /
  Numerical differentiation / Convex function; arXiv:1609.04747 abs + pdf;
  neuralnetworksanddeeplearning.com/chap1.html; cs229.stanford.edu/notes2020spring/
  cs229-notes1.pdf), **this slide spent 0 queries and 0 fetches.**

## Figures used by this slide

**None downloaded — no hosted original exists for this slide's illustration.** As for slide
030, every graphic is course-authored: the green (#00B050-ish) parabola with light gray grid,
the green point at (5,1), the red point at (3,9), the black horizontal chord (3,9)→(7,9),
the red dashed lines at x = 5 and y = 1, the red-bordered annotation box, and the 9-row ×
17-column oscillation table. None is a redraw of a hosted figure; `analysis/slide_031_raw.json`
claims no external figure provenance. No hosted original reused ⇒ none saved.

## What the source(s) CONFIRM

Frame facts from `analysis/slide_031_raw.json`: title "Convex Function, Learning Rate =0.3,
Start at X=3"; parameter table `step | 0.3`, `initial X | 3`, `delta | 0.1`; red-bordered
formula box `f(x)=(x-5)^2+1`; annotation lines "X is in between 4.8 and color red bold 5.1"
and "f(x) is in between 1.04 and 1.01"; the purple "Bouncing" label with a purple arrow to the
oscillating table columns; a 9-row × 17-column table with rows `x, f(x), x-delta, f(x-delta),
x+delta, f(x+delta), slope, next x`.

1. **`f(x) = (x-5)² + 1` with minimum at `(5,1)` and `f(5) = 1`.** CONFIRMED (exact
   computation + the banked convex-function law; see slide 030 record for the quotes).
2. **The annotation "X is in between 4.8 and color red bold 5.1" / "f(x) is in between 1.04
   and 1.01"** — CONFIRMED by exact re-computation: `f(4.8) = 1.04`, `f(5.1) = 1.01`, and
   the two bracketing values are precisely the two states of the oscillation. CONFIRMED.
3. **The whole iteration table reproduces exactly under independent re-computation** (worker's
   local NumPy pass, values to 2 dp, on `f(x)=(x-5)²+1` with `delta = 0.1`):
   `x: 3, 3.3, 3.6, 3.9, 4.2, 4.5, 4.8, 5.1, 4.8, 5.1, 4.8, 5.1, 4.8, 5.1, 4.8, 5.1`;
   `f(x): 9, 3.89, 2.96, 2.21, 1.64, 1.25, 1.04, 1.01, 1.04, 1.01, 1.04, 1.01, 1.04, 1.01,
   1.04, 1.01`;
   `x-delta: 2.9, 3.2, 3.5, 3.8, 4.1, 4.4, 4.7, 5, 4.7, 5, …`;
   `f(x-delta): 5.41, 4.24, 3.25, 2.44, 1.81, 1.36, 1.09, 1, 1.09, 1, …`;
   `x+delta: 3.1, 3.4, 3.7, 4, 4.3, 4.6, 4.9, 5.2, 4.9, 5.2, …`;
   `f(x+delta): 4.61, 3.56, 2.69, 2, 1.49, 1.16, 1.01, 1.04, 1.01, 1.04, …`;
   `slope: -8, -6.8, -5.6, -4.4, -3.2, -2, -0.8, 0.4, -0.8, 0.4, -0.8, 0.4, …`;
   `next x: 3.3, 3.6, 3.9, 4.2, 4.5, 4.8, 5.1, 4.8, 5.1, 4.8, 5.1, …`.
   **All 16 data columns match the raw's transcription to 2 decimal places.** CONFIRMED.
4. **The "Bouncing" label and the purple arrow pointing at the oscillating 4.8 / 5.1 columns:
   this is the sourced "learning rate too large ⇒ fluctuate around the minimum" regime.**
   CONFIRMED by the banked slide-028 quotes: Wikipedia *Gradient descent* ("a η too large
   would lead to overshoot and divergence"), Ruder §3 ("a learning rate that is too large can
   hinder convergence and cause the loss function to **fluctuate around the minimum** or even
   to diverge"), Nielsen ("we might end up with ΔC > 0"). The frame shows exactly the
   fluctuation case — and specifically the reason it happens here, which is confirmable
   arithmetically: with `step = 0.3` the walk leaves `x = 4.8` in the descent direction and
   lands on `5.1`, i.e. it *overshoots* the minimum at `5.0` by 0.1, then the slope turns
   positive and it comes back to `4.8` — a permanent 4.8 ↔ 5.1 oscillation whose amplitude
   equals the overshoot. (With η = 0.2, slide 030's value, the walk lands exactly on the
   minimum and stops.) CONFIRMED as the intended teaching point.
5. **The red point at (3,9) and the black chord from (3,9) to (7,9) on the graph** — CONFIRMED
   arithmetically as the level line `f(x) = 9` on the parabola (both roots of
   `(x-5)²+1 = 9` are `x = 3` and `x = 7`; the frame labels `(3,9)` and `(7,9)`). The chord is
   the secant line whose slope is the difference quotient of the slope rows. CONFIRMED.
6. **`step | 0.3` is the learning rate η of the sources' update.** CONFIRMED by wording
   (CS229 "α is called the learning rate"; Ruder §2 "The learning rate η determines the size
   of the steps"; the deck's sibling slide 026 "moving step is a hyper parameter, AKA Learning
   Rate").

## Course-authored elements (no source counterpart — do NOT "fix" to source)

1. **Slope convention:** the frame's `slope` row is `(f(x+δ) − f(x−δ))/δ`, twice the
   three-point central-difference derivative `(f(x+δ) − f(x−δ))/(2δ)` (Wikipedia *Numerical
   differentiation*). Verified numerically: at `x = 3` the central difference is `−4.00`
   while the frame prints `−8`. Constant factor ⇒ no change of sign ⇒ no change of the
   trajectory. Recorded, not fixed.
2. **Update rule:** `next x = x + step · sgn(−slope/2)` — a learning-rate-sized step in the
   descent direction — not the magnitude-scaled `x − η f′(x)`. Verified numerically across all
   16 columns (independent NumPy pass reproduces the frame's `next x` row exactly, including
   the terminal 4.8/5.1 oscillation). Under the canonical magnitude update the walk from
   `x = 3` with `f′(3) = −4` would take `x ← 3.6, 4.08, …` and converge without bouncing, so
   the frame's "Bouncing" demonstration is a property of the course's sign-step scheme, chosen
   to make the overshoot visible. Recorded, not fixed.
3. **"X is in between 4.8 and color red bold 5.1"** — the literal phrase "color red bold" is
   transcription noise from the vision model annotating the red/bold styling of `5.1`
   (the raw itself records: "The number 5.1 in the annotation is red bold as stated by the
   literal text color red bold", and `analysis/slide_031_raw.json` typography_notes repeats
   it). **Frame text stays verbatim for recreation per the frame-wins law** (build the box
   text exactly as transcribed, with 5.1 in red bold); recorded here only for understanding.
4. **All presentation chrome is course-authored:** the #FFFF99/yellow parameter-table fills,
   the red-bordered white formula box, the red-bordered white annotation box, the purple
   `#7030A0` "Bouncing" label + purple arrow, the pink row-band fills (#D9EAD3/#CFE2F3/
   #FCE5CD/#D9D9D9) of the 9×17 table, the red arrow to the first columns, and the #FFFF00
   badge. No source counterpart; nothing to "fix" toward a source.
5. The chosen function, start point `X = 3`, `delta = 0.1` and the three-value η sweep
   (0.2/0.3/0.4) are the course's own worked example.

## [?] Uncertain items

- **No web-resolvable [?] remains** — every numeric claim was re-computed and matched, and
  the qualitative claim ("Bouncing" = too-large-η fluctuation) is confirmed by the banked
  live-fetched sources.
- Open for the build/judge stage (frame-level, **not** web-resolvable, and listed because
  `analysis/slide_031_final.json` does not exist yet so the worker could not inherit a
  validation block): exact row-band fill hexes per row, the exact grid/tick extents of the
  plot (raw states x and y ticks −5, 0, 5, 10, 15), whether the two red dashed lines extend to
  the axis, exact font sizes, and the intended colour split of the title
  (raw: "Convex Function," red, "Learning Rate =0.3," green, "Start at X=3" blue). Resolution
  path = build + zoomed crop judge per `shared_patterns/judge_protocol_03.md`.
- **Understanding note (recorded, not a bug to fix):** with the frame's sign-step rule the
  4.8 ↔ 5.1 oscillation never terminates — the table's later columns simply repeat the two
  states. The frame presents that repetition as the lesson ("Bouncing"); the sources'
  mitigation options (learning-rate decay/schedules — Ruder §3 "Learning rate schedules … try
  to adjust the learning rate during training by e.g. annealing") are *not* what the slide
  teaches, and would be an addition the frame does not show, so none is proposed.

## Corrections

- **None applied.** There is no `analysis/slide_031_final.json` to patch, and nothing in
  `analysis/slide_031_raw.json` — no dimension, attribute or provenance annotation — is
  contradicted by the sources or by the re-computation (all 16 table columns match). No
  `analysis/*.json` was edited by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
