# SOURCES.md — slide 030 "Convex Function, Learning Rate =0.2, Start at X=3"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
("Web-source research mandate", founder in-session directive 2026-10-19); method = agy web
search (MCP tool `agy_web_search`) for discovery + live fetch with `curl -sL` in the same work
window that records the URL (WebFetch was not used; curl was the fetch tool of record) +
verification against the fetched page text, plus exact numeric re-computation of every
table value on the frame with NumPy/SciPy (local computation, not a web claim). Frame facts
come from `analysis/slide_030_raw.json` / `analysis/slide_030_final.json`; vision transcripts
banked separately. NO vision call was made by this worker (web + local-file work only).
Query budget for this worker (whole 028–036 leg): 2 agy searches (listed per record) + direct
curl fetches of canonical URLs. For this slide: 0 new agy searches (covered by the slide-028
query set); 4 live curls, all listed below.

## Slide identity

- File: `unique_slides/slide_030.jpg` (960×540, 1px = 1pt), badge numeral **30**.
- Pre-curation provenance **recovered**: `_meta.source_timestamps.precuration_slide = 122`,
  `provenance "founder-curated kept frame"`, `kept_frame frame_03501.jpg`, `start_sec 3500`,
  with the md5 snapshot `34535ed01742a71fa2d8f386a05b3e6b` recorded in the raw's `_meta`. The
  pre-curation numbering is otherwise unrecoverable (the founder removed `frames/` and the
  pre-curation index) and is not needed here — the curated file number is authoritative for
  this deck and the badge numeral is exactly 30.
- `analysis/slide_030_final.json` verdict **PASS_WITH_FIXES**, recreatability 9/10.
- Deck namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`.
- **Slide 030 is the reference worked example of the deck's "gradient descent on a convex
  function" block (030/031/032 = η = 0.2/0.3/0.4, 033/034 = non-convex).** Its sources and
  its numeric verification are re-used by 031/032 by cross-reference, so no sibling re-spends
  fetches.

## Primary source(s)

All URLs below were **fetched live in this work window** (HTTP 200; bodies kept on disk under
`/home/ahmed/Projects/ai_llm_slides/scratch/tmp/w2/`) and quoted from the fetched bytes.
Nothing is recorded from an unfetched search snippet.

1. **https://en.wikipedia.org/wiki/Numerical_differentiation** — English Wikipedia, section
   *Finite differences* (incl. the derivation of the three-point formulas). Fetched live,
   HTTP 200 (466,585 bytes). Verbatim:
   > "f′(x) = (f(x+h) − f(x−h)) / (2h) + O(h²) … which is called the three-point central
   > difference formula"

   and, for the two-point secant slope,
   > "The slope of this line is (f(x+h) − f(x)) / h. This expression is Newton's difference
   > quotient (also known as a first-order divided difference)."

   This is the source of record for the slide's `x ± delta` table columns and for the exact
   form of the numerical slope — see the discrepancy note below.
2. **https://cs229.stanford.edu/notes2020spring/cs229-notes1.pdf** — Andrew Ng, CS229 lecture
   notes (2020 spring part 1: Linear Regression and Classification), §1 "LMS algorithm".
   Fetched live, HTTP 200 (233,176 bytes; `pdftotext` extraction). Verbatim:
   > "θj := θj − α ∂J(θ)/∂θj … Here, α is called the learning rate."

   > "…the optimization problem we have posed here for linear regression has only one global,
   > and no other local, optima; thus gradient descent always converges (assuming the learning
   > rate α is not too large) to the global minimum. Indeed, J is a convex quadratic
   > function."

   (Also the source of record for the deck's slide 035 — cross-referenced there.)
3. **https://en.wikipedia.org/wiki/Convex_function** — English Wikipedia, section *Convex
   function calculus* (sublevel sets / minimisers). Fetched live, HTTP 200 (568,136 bytes).
   Verbatim:
   > "Any local minimum of a convex function is also a global minimum. A strictly convex
   > function will have at most one global minimum."

4. **https://arxiv.org/abs/1609.04747** + **https://arxiv.org/pdf/1609.04747** — Sebastian
   Ruder, "An overview of gradient descent optimization algorithms", arXiv:1609.04747v2.
   Fetched live, HTTP 200 (41,246 bytes abs; 659,026 bytes PDF). Verbatim §2.1:
   > "Batch gradient descent is guaranteed to converge to the global minimum for convex error
   > surfaces and to a local minimum for non-convex surfaces."

   (Full record, with the §3 learning-rate quotes, is banked in
   `sources/slide_028_source/SOURCES.md` — cross-referenced here; the PDF was not re-fetched
   for this slide, the banked fetch covers it.)

## Figures used by this slide

**None downloaded — no hosted original exists for this slide's illustration.**

- Every graphic on the frame is course-authored: the blue (#0000FF) parabola plot with light
  gray grid, the red (#FF0000) dashed vertical at x = 5, the red dot at (2,10), the green
  (#008000) dot at (5,1), the black #y=10 chord from (2,10) to (7,1), and the 8×12 iteration
  table. None is a redraw of a figure hosted by the sources above: CS229's notes host GD
  trajectories on quadratic contours, but those are the housing-data example's own plots, not
  this slide's `f(x)=(x-5)²+1` plot.
- `analysis/slide_030_final.json` claims no external figure provenance for any visual element
  either.
- No hosted original is reused ⇒ none saved (contract step 3 satisfied with a reason).

## What the source(s) CONFIRM

Frame facts taken from `analysis/slide_030_raw.json`: title "Convex Function, Learning Rate
=0.2, Start at X=3"; parameter table `step | 0.2`, `initial X | 3`, `delta | 0.1`; equation
block `f(x)=(x-5)^2+1`, `X = 5`, `f(x) Minimum value is 1.0`; callout "Reach Minimum after 11
Steps"; an 8-row × 12-column iteration table with rows `x, f(x), x-delta, f(x-delta), x+delta,
f(x+delta), slope, next x`.

1. **`f(x) = (x-5)² + 1` is a convex (strictly convex) function whose minimum is `X = 5`
   with `f(x) Minimum value is 1.0`.** CONFIRMED both by the sources and by exact
   computation: `f′(x) = 2(x−5) = 0 ⇒ x = 5`, `f(5) = 1`. Wikipedia *Convex function* confirms
   the *general* law ("Any local minimum of a convex function is also a global minimum. A
   strictly convex function will have at most one global minimum.") — the frame's "X = 5" /
   "1.0" is the instance of that law for this quadratic; Ruder §2.1 confirms batch GD "is
   guaranteed to converge to the global minimum for convex error surfaces"; CS229 says "J is a
   convex quadratic function" and GD converges to its single global optimum.
2. **The x/z-slope column structure (`x-delta`, `f(x-delta)`, `x+delta`, `f(x+delta)`) is the
   standard finite-difference construction of a slope.** CONFIRMED by Wikipedia *Numerical
   differentiation*: the slope of a nearby secant `(f(x+h) − f(x))/h` is Newton's difference
   quotient, and the symmetric three-point construct is the named "three-point central
   difference formula" `f′(x) = (f(x+h) − f(x−h))/(2h) + O(h²)`. The slide's `delta = 0.1`
   column pair is exactly that construction with `h = delta = 0.1`.
3. **The complete iteration table reproduces exactly under independent re-computation** —
   every cell of the frame's table is reproduced by evaluating `f(x) = (x-5)²+1` at the
   stated `x` and at `x ± 0.1` (this worker's local NumPy computation; values to 2 dp):
   `x: 3 … 5` (step 0.2);
   `f(x): 5, 4.24, 3.56, 2.96, 2.44, 2, 1.64, 1.36, 1.16, 1.04, 1`;
   `x-delta: 2.9 … 4.9`;
   `f(x-delta): 5.41, 4.61, 3.89, 3.25, 2.69, 2.21, 1.81, 1.49, 1.25, 1.09, 1.01`;
   `x+delta: 3.1 … 5.1`;
   `f(x+delta): 4.61, 3.89, 3.25, 2.69, 2.21, 1.81, 1.49, 1.25, 1.09, 1.01, 1.01`;
   `slope: -8, -7.2, -6.4, -5.6, -4.8, -4, -3.2, -2.4, -1.6, -0.8, 0`;
   `next x: 3.2, 3.4, 3.6, 3.8, 4, 4.2, 4.4, 4.6, 4.8, 5, stop`.
   **All 11 columns match the frame's transcription to 2 decimal places** (source of record:
   `analysis/slide_030_final.json` visual_elements table description). CONFIRMED.
4. **"Reach Minimum after 11 Steps":** the table's 11 columns run `x = 3 → 5.0` (11 positions,
   the last carrying `stop` in `next x`), and the minimum `f(5) = 1` is reached at that last
   column. The frame's step count is its own column count; CONFIRMED as internally consistent
   (see the update-rule note below — under the magnitude-scaled GD update the same minimum
   would be reached in fewer steps, which is why the count is course-authored).
5. **The "stop" cell:** the last `slope` is 0 at `x = 5`, so the descent stops at the
   minimum. CONFIRMED as consistent with the sources' stopping condition — CS229's
   "Repeat until convergence", and the standard rule that the gradient vanishes at a minimum
   (also the subject of this deck's sibling slide 026, "Stop when the gradient is almost zero").
6. **The `step | 0.2` parameter is the learning rate η** of the sources' update
   `θ := θ − α∇J(θ)`. CONFIRMED by wording: CS229 "Here, α is called the learning rate";
   Ruder §2 "The learning rate η determines the size of the steps we take to reach a (local)
   minimum." The slide labels it `step`, and the deck's sibling slide 026 states the same
   thing ("moving step is a hyper parameter, AKA Learning Rate").

## Course-authored elements (no source counterpart — do NOT "fix" to source)

Two conventions on this frame are course-authored and differ from the canonical source form.
Both are recorded here so no builder "fixes" them toward the source; **the frame's numbers
stay verbatim for recreation** — the exception being the annotation-level corrections clause,
which this worker did not need to invoke (see Corrections).

1. **Slope convention: the frame's `slope` row is `(f(x+delta) − f(x−delta)) / delta`, i.e.
   twice the three-point central-difference derivative.** Verified numerically: at `x = 3`
   the central difference is `(4.61 − 5.41)/(2·0.1) = −4.00` while the frame prints `−8`;
   the frame's value equals `(4.61 − 5.41)/0.1`. The factor 2 is a constant and does not
   change the sign of the slope, so it does not change the trajectory.
2. **Update rule: the frame advances `next x = x + step · sgn(−slope/2)` — a fixed-size step
   in the descent direction — not the magnitude-scaled update `x − η·f′(x)`.** Verified
   numerically over all 11 columns (independent NumPy computation): with
   `next_x = x + 0.2·sgn(−(f(x+0.1)−f(x−0.1))/0.2)` the sequence reproduces the frame's
   `next x` row exactly (`3.2 … 5, stop`). Under the canonical update the first step would
   already land at `3 − 0.2·(−4) = 3.8` (true `f′(3) = −4`), so the frame deliberately teaches
   "walk a learning-rate-sized step downhill, re-check the slope each time" — a coherent
   pedagogical scheme that the sources' qualitative statements (Ruder §2, CS229 §1) do not
   forbid; it is a course-authored simplification, not an error.
3. **Everything else on the frame is course-authored presentation:** the green/red/yellow
   parameter-table cell fills (#C6E0B4/#F0C0C0/#FFFFC0 family), the magenta #FF00FF formula
   box, the purple #7030A0 "Reach Minimum after 11 Steps" callout with magenta underline, the
   blue #0070C0 8×12 table with pink arrows, the red block arrow, and the white mouse-pointer
   cursor (a video-capture artifact, excluded from the build by the final's brief).
- No equation, number, axis label or table caption on this frame comes from a hosted source
  figure; the chosen test function `f(x)=(x-5)²+1` and its start point `X=3` are the course's
  own worked example.

## [?] Uncertain items

- No web-resolvable [?] remains: every numeric claim on the frame was independently
  re-computed and matched, and every structural claim is confirmed by the fetched sources.
- **Recorded for understanding (not a frame discrepancy to fix):** under the canonical
  fixed-form magnitude update `x ← x − η f′(x)` this problem converges to `x = 5` in fewer
  iterations (e.g. from `x=3`: 3.8, 4.94, 5.00 — 2 iterations for η = 0.2, and it *oscillates*
  for η > 1.0 because the curvature is 2). The frame's "11 Steps" therefore counts its own
  sign-step walk, not the canonical GD walk. Resolution path = already resolved here (recorded
  in Course-authored elements); the recreation keeps the frame's table and count verbatim.
- Frame-level [?]s that stay open by design (carried from `analysis/slide_030_final.json`,
  none web-resolvable): exact yellow shade / digit colour of the badge, exact coordinates of
  the unlabelled red graph point ((6.2, 2.44) is computed from stated geometry), whether the
  (7,1) chord endpoint carries a marker, cell-level usage of #DDEBF7/#7030A0 inside the
  iteration table, approximate graph axis extents (…x from −5 to 15, y from −5 to 15), and
  the cursor artifact. Resolution path = build + zoomed crop judge per
  `shared_patterns/judge_protocol_03.md`, not web research.

## Corrections

- **None applied.** No dimension, attribute, or provenance guess in
  `analysis/slide_030_final.json` is contradicted by these sources or by the re-computation.
  The model's table transcription was verified cell-by-cell and is correct; the model's
  "(6.2, 2.44)" placement of the unlabelled red point is consistent with the plotted geometry
  (the right intersection of the black y=10 chord with the parabola is at `x = 7`, and the
  red dot near x ≈ 6.2 matches the second chord/parabola intersection shown on the frame).
  No verbatim frame text was touched and no `analysis/*.json` was edited by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
