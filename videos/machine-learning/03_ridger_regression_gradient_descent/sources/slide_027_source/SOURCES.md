# SOURCES.md — slide 027 "Follow Negative Direction of Gradient with Selected Learning Rate"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
("Web-source research mandate", founder in-session directive 2026-10-19). Method = live fetch with
`curl -sL` of every URL recorded below in THIS work window, each verified by a re-fetch + byte
compare (the tool of record was curl; no search tool was needed, and no snippet-only record was
kept). Frame facts come from `analysis/slide_027_raw.json` / `analysis/slide_027_final.json`; the
frame facts that govern the certified recreation (measured curve, dot centres, connectors) come
from the controlling record `recreated_pptx/qa/slide027/adjudication_attempt_9.md` and the shipped
`build_attempt_10.js` (== `build/slide_027.js`) — the founder's three findings recorded there are
binding and are NOT re-litigated here. **No vision call was made by this worker** (web +
local-file work only; the slide's judge legs are banked separately under
`recreated_pptx/qa/slide027/`). **Query budget for this worker: 0 searches spent.** The three URLs
below are the canonical English-Wikipedia pages already used by sibling research records
(`sources/slide_019_source/`, `024`, `026`, `028`, `030`, `035` — cross-referenced per the economy
law), so no search was re-spent to find them: 1 banked HTML parsed + 2 live curl fetches + 2
re-fetch byte-compares, all in this window.

## Slide identity

- File: `unique_slides/slide_027.jpg` (960×540, 1px = 1pt), badge numeral **27** (#FFFF00-family
  yellow circle with purple ring, black bold numeral — deck house chrome).
- Numbering: founder-curated numbering 2026-10-19. Pre-curation provenance **unrecoverable** — the
  raw's `_meta.source_timestamps` (`kept_frame frame_01080.jpg`, `start_sec 1079.0`,
  `frame_count 1`) carries no `precuration_slide` field, and slide 27 is one of the 16 slides the
  deck's AGENTS.md honestly marks unrecoverable (1,2,3,13,24–29,33,35,36,43,44,47). Per the deck
  law this gap is expected and is not an error; no new2old remap applies.
- Deck namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`.
- Analysis record: `analysis/slide_027_final.json`, verdict **PASS_WITH_FIXES**, recreatability
  8/10. The frame's verbatim labels (transcribed, never edited by research): `27`, `Cost`,
  `Learning step`, `Minimum`, `Random initial value`, `+`, `θ`, `θ̂`; no bullets, no equations.
- Build/certification state (for the record only — no DB write was made by this worker):
  `gen_status='passed'`, `visual_check='PASS'` on visual attempt 10, controlling record
  `adjudication_attempt_9.md` (full-slide Template A PASS + crop legs, `axis_top` FAIL
  PIL-adjudicated).
- Slide 027 is the deck's generic "how a gradient step is taken" diagram: a convex quadratic cost
  bowl in a single parameter θ, a random start, iterates stepping downhill with a (decreasing)
  learning-step size, and the minimum. Its siblings are 024–026 (GD basics / learning-rate
  definition) and 028–036 (learning-rate effects, convex/non-convex worked examples).

## Primary source(s)

All three URLs were fetched live in this work window and quoted from the fetched bytes. Nothing
below is recorded from an unfetched search snippet. Byte-exact copies are banked in this
directory as provenance evidence (layout law: originals saved as downloaded, never renamed).

| # | URL | What it is | Fetched-live status |
|---|---|---|---|
| 1 | `https://en.wikipedia.org/wiki/Convex_function` | English Wikipedia, article **"Convex function"** — § *Definition* (one-variable convexity test) and § *Strong convexity* (sublevel sets / minimisers). | **CONFIRMED** — banked HTML in this dir, parsed here: **568,136 B**, sha256 `a2e375e6c304eb60f36d2cbdda96bc22ba0d9095cf3101e8a0ca311aeb0cf81f`, revision `1380599970`. Byte-identical to the copy banked at `sources/slide_026_source/convex_function_wikipedia.html` (`cmp` clean; `sha256sum` equal) — same page, unchanged between windows. |
| 2 | `https://en.wikipedia.org/wiki/Gradient_descent` | English Wikipedia, article **"Gradient descent"** — § *Description → "Choosing the step size and descent direction"*. | **CONFIRMED** — fetched live this window: `curl -sL --max-time 90 -A "Mozilla/5.0"` → HTTP 200, **610,963 B**, final URL identical (no redirect), revision `1373673523`. Re-fetched in the same window and **byte-compared: identical** (sha256 `68850dd6a699508f5f9f91f5e4029de8bbcdda0202c4f85ccaadfc4f504d00d7`). |
| 3 | `https://en.wikipedia.org/wiki/Linear_least_squares` | English Wikipedia, article **"Linear least squares"** — § *Introduction* / *Motivating example* (objective function) and § *Discussion*. | **CONFIRMED** — fetched live this window: HTTP 200, **468,414 B**, revision `1374199323`. Re-fetched in the same window and **byte-compared: identical** (sha256 `ed1286f34d767ab8fca4009f620ff108b079cc99285811b298d79d140428dea5`). |

Cross-referenced, **not re-fetched** (economy law — already fetched live and quoted in sibling
records in this fleet; their quotes are cited as such):

- **CS229 lecture notes** (`cs229.stanford.edu/notes2020spring/cs229-notes1.pdf`) — the convex
  quadratic cost and the update `θj := θj − α ∂J(θ)/∂θj`, live-fetched by
  `sources/slide_028_source/SOURCES.md` and `sources/slide_030_source/SOURCES.md`.
- **Ruder, arXiv:1609.04747** §3 — learning-rate trade-offs, live-fetched by
  `sources/slide_028_source/SOURCES.md`.

Note on byte-identity honesty: this window's live *Gradient descent* bytes (`68850dd6…`) are NOT
byte-identical to the older copies banked at `sources/slide_024_source/gradient_descent_wikipedia.html`
and `sources/slide_026_source/gradient_descent_wikipedia.html` (`c7dcfce5…`), nor is
*Linear least squares* identical to 026's copy (`2465c437…`) — Wikipedia page bytes changed between
windows. The URLs of record for this slide are the bytes fetched HERE, and the two live fetches
were re-fetched and byte-compared in-window, which is the contract's verification.

## Figures used by this slide

**None downloaded — no hosted original exists for this slide's illustration.** The source pages
host figures, but none is the figure this slide reuses or redraws; the slide's diagram is an
original course schematic, so per contract step 3 nothing was saved and the reason is stated.
Every candidate was checked:

- **Convex function** hosts 5 figures: "Convex function on an interval" (`ConvexFunction.svg`);
  "A function (in black) is convex if and only if the region above its graph (in green) is a
  convex set" (`Epigraph_convex.svg`); the bivariate 3-D graph of `x² + xy + y²`; "Convex vs. not
  convex"; and a `Convex_01.ogv` visualisation of Jensen's inequality. None carries axes labelled
  Cost / θ, no descent iterates, no minimum marker.
- **Gradient descent** hosts 8 figures: a `Gradient_Descent_in_2D.webm`, "Illustration of gradient
  descent on a series of level sets" (`Gradient_descent.svg`), "Negative gradient in direction of
  steepest descent" (an MIT lecture-photo), the "Fog in the mountains" analogy photo, two steepest-
  descent convergence plots, an 83-iteration animation on a non-linear system of equations, and
  `Max_paraboloid.svg` ("Optimization computes maxima and minima"). The 1-D scalar-θ walk on a
  cost curve that slide 027 draws is not any of these (they are 2-D contour / non-linear-system
  pictures).
- **Linear least squares** hosts 3 figures: least-square approximation with linear, quadratic and
  cubic polynomials, the red-data/blue-line/green-residual plot, and the quadratic-fit result.
  None is a cost-vs-parameter bowl.

`analysis/slide_027_final.json` claims no external figure provenance for any visual element either
(its single `visual_elements.graph` entry is a course-drawn "Conceptual gradient descent plot").
Same conclusion as the sibling records for 028 and 030.

## What the source(s) CONFIRM

Frame facts from `analysis/slide_027_raw.json` / the controlling record's measurements: a
red-bordered graph box; a y-axis arrow labelled **Cost**; an x-axis arrow labelled **θ**; a black
U-shaped (quadratic) cost curve; a chain of descent iterates (nine, per the certified build)
walking downhill with shrinking spacing; one yellow **Minimum** dot with **θ̂** below it; "+" on
the x-axis; and the labels **Learning step** and **Random initial value** (the latter under a
dashed drop-line from the first iterate). Equations on the frame: none.

1. **"Follow Negative Direction of Gradient" — the descent direction.** CONFIRMED. Wikipedia
   *Gradient descent*:
   > "The idea is to take repeated steps in the opposite direction of the gradient (or approximate
   > gradient) of the function at the current point, because this is the direction of steepest
   > descent. Conversely, stepping in the direction of the gradient will lead to a trajectory that
   > maximizes that function; the procedure is then known as gradient ascent."

   The frame draws exactly that: each successive iterate is placed downhill (against the slope of
   the bowl) from the previous one, i.e. along −∇Cost. Wikipedia also gives the update the frame
   illustrates (transcribed from the page's rendered math):
   > "a_(n+1) = a_n − η ∇f(a_n) … for a small enough step size or learning rate η ∈ R_+, then
   > f(a_(n+1)) ≤ f(a_n) ≤ f(a_n) … so the sequence (x_n) converges to the desired local minimum."

   CS229's canonical form (same update, quoted from the live-fetched notes via
   `sources/slide_028_source/SOURCES.md`): "θj := θj − α ∂J(θ)/∂θj … Here, α is called the
   learning rate." The frame's **"Learning step"** annotation is that η (α) factor — the size of
   the step taken along the negative-gradient direction.
2. **"with Selected Learning Rate" — the learning rate is a selected quantity whose value sets the
   trajectory.** CONFIRMED. Wikipedia:
   > "Since using a step size η that is too small would slow convergence, and a η too large would
   > lead to overshoot and divergence, finding a good setting of η is an important practical
   > problem."

   and "Note that the value of the step size η is allowed to change at every iteration." The
   frame's shrinking iterate spacing (see 5) is consistent with a chosen η held fixed on a
   quadratic bowl — and the deck's sibling slide 028 is the direct source statement of the two
   η regimes (cross-referenced there; no new fetch). CS229: gradient descent "always converges
   (assuming the learning rate α is not too large) to the global minimum. Indeed, J is a convex
   quadratic function."
3. **The bowl is a convex quadratic with ONE minimum — "Minimum" + θ̂.** CONFIRMED by Wikipedia
   *Convex function*:
   > "A twice-differentiable function of a single variable is convex if and only if its second
   > derivative is nonnegative on its entire domain."

   > "Well-known examples of convex functions of a single variable include linear functions …
   > quadratic functions (a as a nonnegative real number) and exponential functions…"

   > "A twice differentiable function of one variable is convex on an interval if and only if its
   > second derivative is non-negative there … Visually, a twice differentiable convex function
   > 'curves up', without any bends the other way (inflection points)."

   > "Any local minimum of a convex function is also a global minimum. A strictly convex function
   > will have at most one global minimum."

   The frame's single yellow "Minimum" dot with θ̂ underneath is precisely that unique global
   minimiser, and the drawn U is precisely a smooth upward-curving convex curve — the certified
   build's analytic quadratic `y = -0.00395282*(x-450.41)² + 407.25` has constant second
   difference `2a = -0.0079` fpx (image-space y down ⇒ the display-space cost is
   `C(x) = 0.00395282*(x-450.41)²`, i.e. second derivative `+0.0079 fpx⁻¹ > 0`, strictly convex).
   *Convex function* also ties the two together: "a strongly-convex function is a function that
   grows as fast as a quadratic function."
4. **Why the object being minimised is a "Cost" at all, and that this bowl is the deck's loss.**
   CONFIRMED. Wikipedia *Gradient descent*: "Gradient descent is particularly useful in machine
   learning and artificial intelligence for minimizing the cost or loss function." Wikipedia
   *Linear least squares*: "The OLS method minimizes the sum of squared residuals, and leads to a
   closed-form expression for the estimated value of the unknown parameter vector β" and "Linear
   least squares problems are convex and have a closed-form solution that is unique, provided that
   the number of data points used for fitting equals or exceeds the number of unknown parameters,
   except in small degenerate situations." That is the objective of the regression/ridge problems
   this deck studies (the convex quadratic cost J(θ) of sibling slides 024/035 — cross-referenced):
   a bowl-shaped scalar objective whose minimiser is unique, exactly the picture slide 027 draws.
   *Linear least squares* also records the deck's topic anchor: "Various regularization techniques
   can be applied in such cases, the most common of which is called ridge regression."
5. **Decreasing step sizes near the bottom of the bowl.** CONFIRMED qualitatively by the sources
   and verified locally against the certified fit (this worker's NumPy computation, not a web
   claim): on a convex quadratic the gradient magnitude decays linearly toward the vertex, so a
   fixed-η walk's cost drop per step shrinks geometrically. Against the certified quadratic the
   frame's chain gives cost steps of 28.72, 28.47, 25.72, 19.21, 13.41, 9.83, 7.09, 4.26 fpx and
   iterate vertical spacing of 46.47, 31.91, 24.57, 14.64, 9.45, 6.29, 5.01, 4.15 fpx — monotone
   decreasing in both, with no overshoot across the minimum. Wikipedia's "slow convergence … for a
   small and constant step size" and "converges linearly with a fixed step size" for a strongly
   convex objective are the qualitative statements this matches.
6. **"Random initial value" — GD starts wherever you start it.** CONFIRMED structurally: the
   sources' update is iterated "at the current point", with no assumption about where the
   iteration begins; and because the frame's objective is convex ("Any local minimum of a convex
   function is also a global minimum"), the point the walk converges to is the global minimum
   independent of the start. The frame's dashed drop-line marks that arbitrary starting abscissa.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

Per the binding founder ruling (the founder visually rejected an earlier attempt): the attempt-10
build implements all three findings, and the controlling record is
`recreated_pptx/qa/slide027/adjudication_attempt_9.md`. This research record does not contradict
the frame or that ruling — **the frame wins for recreation**.

- **The black cost curve is ONE SMOOTH quadratic** — founder finding A ("identify it as a
  quadratic curve and draw ONE SMOOTH mathematical curve … a quadratic cost function of the
  iterate position"). Shipped as the analytic quadratic `y = -0.00395282*(x-450.41)² + 407.25`,
  420 samples at 1 frame px, extent x = 239..658, vertex pinned to the yellow minimum at
  (444.49, 407.25) — a course/founder-mandated stylization measured from the frame, not a redraw
  of any source figure.
- **The grey step connectors are ARC ARROWS WITH ARROWHEADS, aligned to the purple dot centres** —
  founder findings B and C (each connector runs between CONSECUTIVE purple dot CENTRES and carries
  a REAL arrowhead at its terminating end). Shipped as nine cubic-Bezier arcs anchored
  dot-centre→dot-centre on the nine measured halo-excluded centroids, each terminated by a filled
  grey triangle head (length 5.4 fpx, half-width 2.7 fpx, tangent along the arc's terminal
  direction, tip 6.32–6.58 fpx from the target centre), drawn in the order curve → connectors →
  heads → discs → yellow minimum so each shaft's overrun is covered by its own head and then by
  its disc. Course/founder-mandated stylization.
- **One adjudicated nuance, recorded (not re-litigated).** The founder's description says "dashed";
  the controlling record §1 measured the ORIGINAL FRAME's connectors as **solid** (95–100 %
  on-density over their ink spans; no dash cadence measurable anywhere in the chain), so the build
  draws them as solid `CHAIN_GRAY` (#ACACAD) arcs at ~2 fpx. The dashed elements that DO exist on
  the frame are the two dash **leaders** — the x = 262.5 vertical drop-line under the first
  iterate (→ "Random initial value") and the short x = 444.5 collar near the minimum — which the
  build draws dash-by-dash from the measured dash rows. The substance of the ruling (arc arrows
  with arrowheads, centre-to-centre anchoring) is implemented exactly as mandated; only the
  dash adjective is a description-vs-frame difference already adjudicated there.
- **Palette.** The diagram's ink is the course's own soft-grey/purple/yellow set (axis core mean
  RGB (80,81,79), curve 61, chain 162, labels 112; iterates (97,70,187); minimum yellow) — the
  fetched source figures are entirely grayscale, which proves the coloured containers are course
  recolouring, not source data. Do not "fix" toward a source palette.
- **Everything else is course-authored presentation:** the house chrome (grey panel, three red
  strokes, yellow badge with purple ring), the title wording, the eight labels, the schematic
  two-arrow axis pair, the number of iterates (nine), the non-overshooting trajectory that stops
  just short of the minimum, and the frame's plot-frame geometry.
- **Honest note on the trajectory's numerics (so no later worker "corrects" it):** the nine
  iterates are **not** a computed constant-η GD walk on the fitted quadratic. A least-squares
  η = 20.45 (the diagram's own frame-px units) reproduces the measured x-chain only to ±23.5 fpx
  max, and the per-interval implied η ranges 13.9 → 55.7. The frame never states a numeric η. The
  chain is a schematic illustration of "step downhill with a decreasing step size" — consistent
  with every qualitative statement the sources make (CONFIRM 1, 2, 5) but not a plotted numeric
  run, and not to be replaced by one.

## [?] Uncertain items

- **No web-resolvable [?] remains for this slide.** Every claim the frame makes — negative-gradient
  step direction, the learning-rate step size, a convex quadratic bowl with one minimum, a
  "Cost" objective — is CONFIRMED above with live-fetched quotes.
- Frame-level [?]s that stay open by design, carried from `analysis/slide_027_final.json` and
  resolved by the build/judge legs, **not** by web research:
  - descent-dot count ("approximately 8" in the analysis record vs the **nine** measured dot
    centres in the controlling record) — resolved by the certified build, which draws nine;
    resolution path = the banked `probe_adj9_geometry_output.txt` / `adj9_geometry.json`;
  - dot hue (`#0000CD` "medium blue" in the analysis record vs the measured frame purple
    (97,70,187)) — resolved at build time against the frame;
  - title font family/size (the analysis record's 32–36 pt estimate) and the exact graph-box
    bounds (the analysis record's 15%–85% / 25%–90% estimates) — resolved by the measured inner
    plot frame (vertical red strokes at cols 193–194 / 715–717, horizontal at rows 166–168 /
    506–508) and the house-chrome/measure bank;
  - the exact wording/typography of the eight labels' font sizes.
  Resolution path for all of the above = the slide's own build + zoomed crop judge per
  `shared_patterns/judge_protocol_03.md` (banked under `recreated_pptx/qa/slide027/`), never web
  research.
- Whether the lecturer had a specific figure on screen when filming (Wikipedia's level-set
  illustration, CS229's contour trajectory, another): unresolvable without the video's audio, and
  the content is course-authored either way. Not web-resolvable.
- Whether the drawn trajectory corresponds to a specific numeric learning rate (e.g. the η = 0.2
  of sibling slide 030): the frame states none, and no constant η fits the chain (above).
  Resolution path = the video's audio; not needed for the recreation.

## Corrections

- **None applied.** No `analysis/*.json` was edited by this worker: no dimension, attribute or
  provenance guess in `analysis/slide_027_final.json` is contradicted by the three sources in a
  way that requires a patch (the sources describe the general method; the frame's annotations are
  position/hue/count estimates that only the banked build measurements can settle).
- Recorded discrepancies with an evidence trail, for the owning worker to apply if it chooses
  (annotation-level only; **no verbatim frame text was touched**):
  1. `analysis/slide_027_final.json` "approximately 8" descent dots vs **nine** measured dot
     centres — evidence: `recreated_pptx/qa/slide027/adjudication_attempt_9.md` §1
     (`probe_adj9_geometry_output.txt`, `adj9_geometry.json`); the certified build draws nine.
  2. dot hue `#0000CD` vs measured frame purple (97,70,187) — evidence: `adjudication_attempt_9.md`
     §4e (purple matches "within a few units: original (97,70,187)").
  3. graph-box bounds "15%–85% width, 25%–90% height" vs the measured inner plot frame (cols
     193–194 / 715–717; rows 166–168 / 506–508) — evidence: `adjudication_attempt_9.md` §4c.
  4. The frame's connectors, measured SOLID while the founder's ruling describes them as "dashed" —
     evidence: `adjudication_attempt_9.md` §1 ("Dashes: the founder's description says 'dashed';
     the frame's connectors are SOLID"); reconciled in Course-authored elements above.
- Nothing in this record re-opens the certified build: the founder's three findings and the
  attempt-10 ship stand, and per the founder ruling the frame wins for recreation.

## Law reminder

The frame wins for recreation; the source wins for understanding.
