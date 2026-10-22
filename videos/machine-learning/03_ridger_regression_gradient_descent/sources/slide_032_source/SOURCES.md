# SOURCES.md — slide 032 "Convex Function, Learning Rate =0.4, Start at X=3"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
("Web-source research mandate", founder in-session directive 2026-10-19); method = agy web
search (MCP tool `agy_web_search`) for discovery + live fetch with `curl -sL` in the same work
window that records the URL + verification against the fetched page text, plus exact
re-computation of every table value on the frame with NumPy (local computation, not a web
claim). Frame facts come from `analysis/slide_032_raw.json` (no `*_final.json` exists yet —
researched from the RAW per the worker brief); vision transcripts banked separately. NO vision
call was made by this worker (web + local-file work only).
**Query budget for this slide: 0 agy searches, 0 new fetches — every source is already banked
live in this same work window** (economy law; see "Primary source(s)").

## Slide identity

- File: `unique_slides/slide_032.jpg` (960×540, 1px = 1pt), badge numeral **32**.
- Pre-curation provenance **recovered**: `_meta.source_timestamps.precuration_slide = 127`,
  `provenance "founder-curated kept frame"`, `kept_frame frame_03845.jpg`, `start_sec 3844`,
  md5 snapshot `e42058a774e44d9f870a5e4670ecdffd`.
- Analysis status: raw only (`analysis/slide_032_final.json` not yet produced). This research
  record does not wait on it — per the mandate's "interleaves; never dependency-gated" law.
- Deck namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`.
- **Position in the block:** third rung of the deck's learning-rate sweep on the SAME convex
  function — slide 030 (η = 0.2 → 11 columns to the minimum), slide 031 (η = 0.3 → overshoots
  into a permanent 4.8 ↔ 5.1 oscillation), slide 032 (η = 0.4 → **reaches the minimum in 6
  columns**). Slide 032 is the case that lands exactly on the minimum.

## Primary source(s)

**None newly fetched and no search spent** — every source was fetched live earlier in this same
work window and is banked with verbatim quotes in sibling records (economy law: cross-reference
rather than re-spend):

- **`sources/slide_030_source/SOURCES.md`** — live-fetched, verbatim:
  - Wikipedia *Numerical differentiation*: `f′(x) = (f(x+h) − f(x−h))/(2h) + O(h²)` (the
    "three-point central difference formula") and `(f(x+h) − f(x))/h` (Newton's difference
    quotient) — the source form for the `x ± delta` rows.
  - Wikipedia *Convex function*: "Any local minimum of a convex function is also a global
    minimum. A strictly convex function will have at most one global minimum."
  - Ng CS229 notes §1: "θj := θj − α ∂J(θ)/∂θj … Here, α is called the learning rate" and
    "…J is a convex quadratic function… gradient descent always converges (assuming the
    learning rate α is not too large) to the global minimum."
- **`sources/slide_031_source/SOURCES.md`** — live-fetched, verbatim (same URLs, banked once):
  - Wikipedia *Gradient descent*, "Choosing the step size and descent direction": "Since using
    a step size η that is too small would slow convergence, and a η too large would lead to
    overshoot and divergence, finding a good setting of η is an important practical problem."
  - Sebastian Ruder, arXiv:1609.04747v2, §2.1: "Batch gradient descent is guaranteed to
    converge to the global minimum for convex error surfaces…"; §3: "Choosing a proper
    learning rate can be difficult. A learning rate that is too small leads to painfully slow
    convergence, while a learning rate that is too large can hinder convergence and cause the
    loss function to fluctuate around the minimum or even to diverge."
  - Michael Nielsen, *Neural Networks and Deep Learning* ch.1: "…we need to choose the learning
    rate η to be small enough that Equation (9) … is a good approximation. If we don't, we
    might end up with ΔC > 0…"
- **URL/economy record:** the fetched-live URLs behind those records (Wikipedia
  `Gradient_descent` / `Numerical_differentiation` / `Convex_function`;
  `arxiv.org/abs/1609.04747` + `arxiv.org/pdf/1609.04747`;
  `neuralnetworksanddeeplearning.com/chap1.html`;
  `cs229.stanford.edu/notes2020spring/cs229-notes1.pdf`) were each fetched once in this window
  and are re-used here. **This slide spent 0 queries and 0 fetches.**

## Figures used by this slide

**None downloaded — no hosted original exists for this slide's illustration.** Every graphic is
course-authored: the blue (#0000FF) parabola over a light-gray grid with ticks
(−6, 0, 5, 10, 15 on x; 0, 5, 10, 15 on y), the red (#FF0000) dashed vertical at x = 5, the
red dot + red label `(2,10)`, the green (#008000) dot + label `(5,1)`, the black horizontal
line at y = 10 from x = 2 to ≈ 7, and the 8-row × 7-column iteration table with its
light-green/light-yellow/light-red row fills. `analysis/slide_032_raw.json` claims no external
figure provenance, and none of the banked sources hosts a version of this specific plot. No
hosted original reused ⇒ none saved.

## What the source(s) CONFIRM

Frame facts from `analysis/slide_032_raw.json`: title "Convex Function, Learning Rate =0.4,
Start at X=3"; parameter table `step | 0.4`, `initial X | 3`, `delta | 0.1`; bullets "X = 5",
"f(x) Minimum value is 1.0", "Reach Minimum after 6 Steps"; an 8-row × 7-column table with rows
`x, f(x), x-delta, f(x-delta), x+delta, f(x+delta), slope, next x`.

1. **`f(x) = (x-5)² + 1`, minimum at `X = 5`, `f(x) Minimum value is 1.0`.** CONFIRMED by exact
   computation (`f′(x) = 2(x−5) = 0 ⇒ x = 5`, `f(5) = 1`) and by the banked convex-function
   law (Wikipedia: "Any local minimum of a convex function is also a global minimum…"; Ruder
   §2.1; CS229: "J is a convex quadratic function"). CONFIRMED.
2. **"Reach Minimum after 6 Steps" and the full 8×7 table reproduce exactly under independent
   re-computation** (worker's local NumPy pass, values to 2 dp, `delta = 0.1`):
   `x: 3, 3.4, 3.8, 4.2, 4.6, 5`;
   `f(x): 5, 3.56, 2.44, 1.64, 1.16, 1`;
   `x-delta: 2.9, 3.3, 3.7, 4.1, 4.5, 4.9`;
   `f(x-delta): 5.41, 3.89, 2.69, 1.81, 1.25, 1.01`;
   `x+delta: 3.1, 3.5, 3.9, 4.3, 4.7, 5.1`;
   `f(x+delta): 4.61, 3.25, 2.21, 1.49, 1.09, 1.01`;
   `slope: -8, -6.4, -4.8, -3.2, -1.6, 0`;
   `next x: 3.4, 3.8, 4.2, 4.6, 5, stop`.
   **All 6 data columns match the raw's transcription to 2 decimal places.** CONFIRMED.
   Note the pedagogical fact that makes this slide work: `4.6 + step(0.4) = 5.0` exactly, so
   the walk lands on the minimum and the `slope` in the final column is 0 → `stop`. That is
   the "6 steps" count (the frame's own column count).
3. **The graph's labelled points are arithmetically correct for `f(x) = (x-5)²+1`:** the red
   dot at `(2,10)` satisfies `f(2) = 10`, the green dot at `(5,1)` is the vertex, and the black
   level line at `y = 10` runs from the left root `x = 2` to the right root `x = 7`. CONFIRMED
   (same verification style as slides 030/031).
4. **`step | 0.4` is the learning rate η of the sources' update rule.** CONFIRMED by wording
   (CS229: "Here, α is called the learning rate"; Ruder §2: "The learning rate η determines the
   size of the steps we take to reach a (local) minimum"; deck sibling slide 026: "moving step
   is a hyper parameter, AKA Learning Rate"). CONFIRMED.
5. **The three-slide sweep (0.2 → 11 steps, 0.3 → oscillation, 0.4 → 6 steps, still reaching
   the minimum) is the sourced trade-off, not a contradiction.** CONFIRMED: the sources state
   that the *too large* regime is defined by the loss fluctuating/diverging, not by the step
   being numerically large in the abstract — CS229: "gradient descent always converges
   (assuming the learning rate α is **not too large**)". A step of 0.4 in this 1-D bowl is
   still in the converging regime (the curvature is 2, so the stability limit for the
   magnitude-scaled update is η < 2), and under the course's sign-step scheme 0.4 lands on
   the minimum exactly. CONFIRMED as consistent.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

1. **Slope convention:** the frame's `slope` row is `(f(x+δ) − f(x−δ))/δ` — twice the
   three-point central-difference derivative `(f(x+δ) − f(x−δ))/(2δ)` (Wikipedia *Numerical
   differentiation*). Verified: at `x = 3` the central difference is `−4.00`, the frame prints
   `−8`. Constant factor, sign unchanged, trajectory unchanged. Recorded, not fixed.
2. **Update rule:** `next x = x + step · sgn(−slope/2)` (a learning-rate-sized step in the
   descent direction), not the magnitude-scaled `x − η f′(x)`. Verified numerically across all
   6 columns (independent NumPy pass reproduces the frame's `next x` row exactly, ending
   `5, stop`). Recorded, not fixed.
3. **"Reach Minimum after 6 Steps"** is the course's own count of its sign-step walk's columns
   (under the canonical magnitude update the same minimum is reached in ~2 steps). Recorded as
   course-authored; nothing to "correct".
4. **All presentation chrome is course-authored:** the #C0E0C0/#F0C0C0/#FFFFC0 parameter-cell
   fills, the blue `#0000FF` outer table border with thin inner lines, the pink `#C000C0`
   arrow, the small red cursor dot ("likely a mouse cursor or laser pointer marker" per the
   raw), the multi-colour title segments (dark red `#C00000` / green `#008000` / blue
   `#0000FF`), the bold red "X = 5", bold blue "1.0", purple `#800080` "Minimum value is" and
   "Reach Minimum after 6 Steps", and the #FFFF00 badge. No source counterpart.
5. The asymmetric x tick set (−6, 0, 5, 10, 15) versus the y set (0, 5, 10, 15) and the
   `#F0F0F0` background are course choices.

## [?] Uncertain items

- **No web-resolvable [?] remains** — every numeric claim was re-computed and matched, and
  the qualitative claims are confirmed by the banked live-fetched sources.
- Frame-level items open by design (raw only — no final yet, so no inherited validation
  block; none web-resolvable): exact point sizes (title "~30pt" is the brief's
  recommendation), exact cell fills for the data cells (raw says white), the exact curve colour
  hex (recorded `#0000FF`), whether the (2,10) chord endpoint carries a marker, and the small
  red dot's nature (cursor/laser-pointer artifact). Resolution path = build + zoomed crop judge
  per `shared_patterns/judge_protocol_03.md`.

## Corrections

- **None applied.** Nothing in `analysis/slide_032_raw.json` — no dimension, attribute or
  provenance annotation — is contradicted by the sources or by the re-computation (all 6
  columns match). No `analysis/*.json` was edited by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
