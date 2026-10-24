# SOURCES.md — slide 027 "Follow Negative Direction of Gradient with Selected Learning Rate"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Binding contract:
`~/.agents/skills/slide-recreation/references/source-research.md`.

Method: live fetch of every URL recorded below **in this work window (2026-10-24)** with
`curl -sL --max-time 60 -A "Mozilla/5.0"`, each page fetched **twice** and byte-compared
(trust discipline: nothing recorded from an unfetched search snippet; re-fetch byte-identity
required for CONFIRMED status). **No `agy` / WebSearch query was spent.** Frame facts come from
`analysis/slide_027_raw.json` / `analysis/slide_027_final.json`; the frame facts that govern the
certified recreation (measured curve, the nine dot centres, the arc connectors) come from the
controlling record `recreated_pptx/qa/slide027/adjudication_attempt_9.md` and the shipped
`recreated_pptx/build/slide_027.js` — the founder's three findings recorded there are BINDING
and are NOT re-litigated here. **No vision call was made by this worker** (web + local-file work
only; the slide's judge legs are banked separately under `recreated_pptx/qa/slide027/`). The
certified build, its renders and all qa evidence were read, never written.

**Query budget for this worker: 0 web searches; 8 successful HTTP page fetches (4 pages × 2
re-fetches) + 4 failed live attempts** (`see.stanford.edu` CS mirror 404; `cs229.stanford.edu`
CS229 Part I 2021-fall notes1 → HTTP 000 ×3, connection-level failure from this host — debt
recorded in "[?] Uncertain items"; the CS229 quotes below are then carried from the byte-verified
banked copy, economy law). Total bytes downloaded this window: **3,617,506** (610,963×2 +
568,205×2 + 468,414×2 + 161,171×2). One new byte-exact download banked in this directory:
`learning_rate_wikipedia.html`.

This record supersedes the 2026-10-23 version of this file: that version's three URLs were
re-verified live in this window, and the fourth source the slide's own title needs (Wikipedia
*Learning rate*) is added here with live quotes.

## Slide identity

- File: `unique_slides/slide_027.jpg` (960×540, 1px = 1pt), badge numeral **27** (#FFFF00-family
  yellow circle with purple ring, black bold numeral — deck house chrome).
- Numbering: founder-curated numbering 2026-10-19. Pre-curation provenance **unrecoverable** —
  slide 27 is one of the 16 slides the deck's AGENTS.md honestly marks unrecoverable
  (1,2,3,13,24–29,33,35,36,43,44,47). Per the deck law this gap is expected, not an error; no
  new2old remap applies.
- Deck namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`.
- Analysis record: `analysis/slide_027_final.json`, verdict **PASS_WITH_FIXES**, recreatability
  8/10. The frame's verbatim labels (transcribed, never edited by research): `27`, `Cost`,
  `Learning step`, `Minimum`, `Random initial value`, `+`, `θ`, `θ̂`. **No bullets, no equations
  (`equations: []`, `bullets: []`)** — the update rule this slide teaches is carried by the
  **graphic** (the arrowed chain of iterates), not by printed maths.
- Build/certification state (read-only for this worker): `gen_status='passed'`,
  `visual_check='PASS'` on visual attempt 10; controlling record
  `qa/slide027/adjudication_attempt_9.md` (full-slide Template A PASS + crop legs, `axis_top`
  FAIL PIL-adjudicated). Deliverable `recreated_pptx/slide_027_recreated.pptx` built by
  `recreated_pptx/build/slide_027.js`.
- What the slide actually carries (from `build/slide_027.js`, which implements the founder's
  three binding findings A/B/C): a red `FF0000` 2pt-bordered, **white-filled** plot box
  (x193.5..716, y167..507 frame px) on the grey panel; two black 2pt axis lines with filled
  triangular arrowheads (y = **Cost** up, x = **θ** right); **ONE SMOOTH analytic quadratic**
  cost curve `y = -0.00395282·(x-450.41)² + 407.25` sampled at 420 points, vertex pinned to the
  yellow minimum; **NINE violet `#5F41C4` discs** at the measured halo-excluded centres;
  **NINE grey `#ACACAD` arc arrows with real filled arrowheads**, each anchored on consecutive
  purple dot centres (founder findings B and C); a yellow minimum dot at (444.49, 407.25); a
  faint grey `#8C8C8C` `+` (11×10 fpx) below dot 8; `θ̂` (θ with an open 2-stroke caret) below
  the axis under the minimum; the five labels `Cost`, `Learning step`, `Minimum`,
  `Random initial value` / `initial value`; and two black dashed leader lines (x = 262.5 under
  the first iterate, x = 444.5 collar by the minimum).
- Sibling lineage: 024–026 (GD basics / the GD algorithm statement) and 028–036 (learning-rate
  effects, convex/non-convex worked examples).

## Primary source(s)

Every URL below was fetched live **twice** in this window and byte-compared. Byte-exact copies
of the pages are banked in this directory as provenance evidence (layout law: originals saved
as downloaded, never renamed or deleted).

| # | URL | What it is | Fetched-live status |
|---|---|---|---|
| 1 | `https://en.wikipedia.org/wiki/Learning_rate` | English Wikipedia, article **"Learning rate"** — lead definition ("tuning parameter … determines the step size at each iteration"), the convergence/overshoot trade-off, and § *Learning rate schedule* (decay). **This is the direct source for the slide's title clause "with Selected Learning Rate" and for its `Learning step` label.** | **CONFIRMED — newly fetched live this window**: HTTP 200, **161,171 bytes** on both fetches, byte-identical re-fetch, no redirect; revision `1361882756`; md5 `87ad13b58d2a33ad20b5104327e2c03c`, sha256 `8ad760c37d7306fec9c98a1cf6be7387979670d4a8496cfc5352ae46b82dbf8d`. Banked byte-exact here as `learning_rate_wikipedia.html`. Not previously banked by any sibling record. |
| 2 | `https://en.wikipedia.org/wiki/Gradient_descent` | English Wikipedia, article **"Gradient descent"** — § *Description* (negative-gradient direction, the update rule) and § *Choosing the step size and descent direction* (the η trade-off). | **CONFIRMED** — fetched live this window: HTTP 200, **610,963 B** on both fetches, byte-identical to each other and **byte-identical to the banked copy in this directory** (md5 `bb29c6dd6bcb0c5fb4cec6bcd134a2e6`); revision `1373673523`. |
| 3 | `https://en.wikipedia.org/wiki/Convex_function` | English Wikipedia, article **"Convex function"** — § *Definition* (one-variable convexity test), § *Examples → Functions of one variable* (quadratics are convex) and § *Properties* (minimiser uniqueness). | **CONFIRMED** — fetched live twice this window: HTTP 200, **568,205 B** both times, byte-identical re-fetch, revision `1380599970`. The banked copy here is 568,136 B (md5 `b51291236b9dcb8f1fd678d2c0301b3f`, rev `1380599970`); the 69-byte difference is MediaWiki per-response telemetry only (44 changed lines: `Parsed by` host names, parser-cache/`Cached time` stamps, CPU/real/Lua time usage, template timing percentages, render ID, `wgHostname`) — **no substantive text line**, same `wgRevisionId`. Every quote below was re-verified present in the live bytes. |
| 4 | `https://en.wikipedia.org/wiki/Linear_least_squares` | English Wikipedia, article **"Linear least squares"** — § *Objective function* / *Motivating example* (the objective being minimised) and § *Discussion* (convexity, uniqueness of the closed form). | **CONFIRMED** — fetched live twice this window: HTTP 200, **468,414 B**, byte-identical re-fetch and **byte-identical to the banked copy** (md5 `55ce299953a0d73eaafac78af728e10e`); revision `1374199323`. |

Cross-referenced, **not re-fetched** (economy law — already fetched live, quoted and banked by
sibling records in this fleet; their quotes are cited as such):

- **CS229 lecture notes, Part I** (`cs229.stanford.edu/notes2021fall/cs229-notes1.pdf`; the same
  document is served at `see.stanford.edu/materials/aimlcs229/cs229-notes1.pdf`) — the convex
  quadratic cost and the update `θj := θj − α ∂J(θ)/∂θj`, live-fetched and byte-banked at
  `sources/slide_024_source/cs229-notes1.pdf` (357,392 B, md5
  `73241a52de8ca0544803fb5cc5844771`), quoted by `sources/slide_024_source/SOURCES.md`,
  `sources/slide_030_source/SOURCES.md` and `sources/slide_031_source/SOURCES.md`. A live
  re-fetch was attempted from this host four times this window and failed every time (one HTTP
  404 on the see.stanford mirror, three HTTP 000 on cs229.stanford.edu) — the quotes below were
  therefore verified **locally, against the banked byte-verified copy**, with `pdftotext
  -layout`; that is recorded as a window debt, not as a CONFIRMED live fetch.
- **Ruder, arXiv:1609.04747** §3 — learning-rate trade-offs, live-fetched by
  `sources/slide_028_source/SOURCES.md`.
- **Wikipedia *Loss function*** — `sources/slide_025_source/SOURCES.md` (live-fetched there,
  banked at `sources/slide_025_source/loss_function_wikipedia.html`).

Note on byte-identity honesty: this window's *Gradient descent* and *Linear least squares*
bytes are byte-identical to the copies banked here; the *Convex function* page's bytes differ
from the banked copy only in Wikimedia per-response telemetry (same revision), as tabulated
above. The URLs of record for this slide are the bytes fetched HERE.

## Figures used by this slide

**None downloaded — no hosted original exists for this slide's illustration.** The source pages
host figures, but none is the figure this slide reuses or redraws; the slide's diagram is an
original course schematic, so per contract step 3 nothing was saved and the reason is stated.
Every candidate was checked against the live-fetched pages in this window (captions and
`data-file-width/height` read off the served HTML):

- **Gradient descent** hosts 8 figures: "Gradient descent in 2D" (`Gradient_Descent_in_2D.webm`,
  720×720); "Illustration of gradient descent on a series of level sets"
  (`Gradient_descent.svg`, 512×549); "Negative gradient in direction of steepest descent."
  (MIT lecture photo, 676×500); "Fog in the mountains" (fog-photo analogy, 5360×3568); "The
  steepest descent algorithm applied to the Wiener filter" (`Steepest_descent.png`,
  1500×1200); "Convergence path of steepest descent method for A = [[2, 2], [2, 3]]"
  (443×420); the 83-iteration animation on a non-linear system of equations
  (`Gradient_Descent_Example_Nonlinear_Equations.gif`, 602×431); and
  `Max_paraboloid.svg` ("Optimization computes maxima and minima.", 700×560). None is a 1-D
  scalar-θ walk along a cost curve with an arrowed iterate chain (2-D contours, non-linear
  systems, or a paraboloid surface).
- **Convex function** hosts 5 figures: "Convex function on an interval"
  (`ConvexFunction.svg`, 512×266); "A function (in black) is convex if and only if the region
  above its graph (in green) is a convex set" (`Epigraph_convex.svg`, 512×325); "A graph of the
  bivariate convex function x² + xy + y²" (579×404); "Convex vs. not convex" (1210×1250); and a
  `Convex_01.ogv` visualisation of Jensen's inequality (854×480). None carries axes labelled
  Cost / θ, no descent iterates, no minimum marker.
- **Linear least squares** hosts 3 figures: "Least square approximation with linear, quadratic
  and cubic polynomials." (640×480); "A plot of the data points (in red), the least squares
  line of best fit (in blue), and the residuals (in green)" (279×274); and "The result of
  fitting a quadratic function y = β₁ + β₂x + β₃x²" (154×179). None is a cost-vs-parameter bowl.
- **Learning rate** hosts **zero figures** — the page contains only 14 inline mathematics
  renders (η, η₀, d, n, floor brackets) and the site logos. Nothing to download.
- `analysis/slide_027_final.json` claims no external figure provenance for any visual element
  either (its single `visual_elements.graph` entry is a course-drawn "Conceptual gradient
  descent plot"). Same conclusion as the sibling records for 028 and 030, and for 026.

Contrast with the sibling that DID download: `sources/slide_025_source/` saved three originals
(`Convex_vs._Not-convex.jpg`, `Grafico_3d_x2%2Bxy%2By2.png`,
`Gradient_Descent_Example_Nonlinear_Equations.gif`) because slide 025 literally plots the
surfaces those figures show. Slide 027 plots none of them.

## What the source(s) CONFIRM

Frame facts (from `analysis/slide_027_raw.json` / `analysis/slide_027_final.json` and the
controlling record's measurements): a red-bordered white-filled graph box; a y-axis arrow
labelled **Cost**; an x-axis arrow labelled **θ**; a black U-shaped (quadratic) cost curve; a
chain of descent iterates (nine, per the certified build) walking downhill with shrinking
spacing; one yellow **Minimum** dot with **θ̂** below it; `+` on the x-axis region; and the
labels **Learning step** and **Random initial value** (the latter under a dashed drop-line from
the first iterate). Equations on the frame: none — the update rule is drawn, not printed.

1. **"Follow Negative Direction of Gradient" — the descent direction.** CONFIRMED by Wikipedia
   *Gradient descent*:
   > "The idea is to take repeated steps in the **opposite direction** of the gradient (or
   > approximate gradient) of the function at the current point, because this is the direction
   > of steepest descent."

   and:
   > "f(x) **decreases fastest if one goes from a in the direction of the negative gradient** of
   > f at a, i.e., −∇f(a)."

   The frame draws exactly that: every arc in the chain leaves one violet iterate and lands on
   the next, lower one, i.e. along −∇Cost. The page's own gloss is the same idea:
   > "the term η∇f(a) **is subtracted from a** because **we want to move against the gradient,
   > toward the local minimum.**"
2. **The update rule the frame's chain instantiates — `W ← W − η∇f(W)`.** CONFIRMED as the
   page's own equation (transcribed from the served page's rendered math):
   > `aₙ₊₁ = aₙ − η∇f(aₙ)`
   > "for a small enough step size or **learning rate η ∈ ℝ₊**, then `f(aₙ) ≥ f(aₙ₊₁)`."

   With the frame's variable (θ, the regressor held by the bowl) and its cost (the page's `f`),
   this is exactly `θₙ₊₁ = θₙ − η∇Cost(θₙ)` — one arc of the drawn chain. The canonical form in
   this deck's family, cross-referenced from the banked CS229 Part I notes (md5
   `73241a52…`, verified locally by `pdftotext` at lines 173–177):
   > `θj := θj − α ∂J(θ)/∂θj.` … "**Here, α is called the learning rate.** This is a very
   > natural algorithm that repeatedly takes a step in the direction of steepest decrease of J."

   Wikipedia's displayed form is the indexed-sequence variant and CS229's is the assignment
   form — **same rule, same meaning** (recorded so no later reader mistakes the notations for
   a discrepancy). The frame states the rule graphically, which is why the slide carries
   `equations: []` and the nine arrowed arcs instead.
3. **"with Selected Learning Rate" — the learning rate is a *selected* quantity whose value sets
   the trajectory.** CONFIRMED by Wikipedia *Learning rate*, the article's lead:
   > "In machine learning and statistics, **the learning rate is a tuning parameter in an
   > optimization algorithm that determines the step size at each iteration while moving toward
   > a minimum of a loss function.**"

   and:
   > "In setting a learning rate, there is a **trade-off between the rate of convergence and
   > overshooting**. While the **descent direction** is usually determined from the gradient of
   > the loss function, **the learning rate determines how big a step is taken in that
   > direction.**"

   That is a point-by-point source for the slide's own two-part title: the direction comes from
   the (negative) gradient; the *step size* is the selected η. That the value is a practitioner
   choice, not a learned quantity, is the page's "tuning parameter" and, from *Gradient descent*,
   > "finding a good setting of η is an important practical problem."
4. **The `Learning step` annotation is that η factor — and its label is the source's own
   vocabulary.** CONFIRMED: *Learning rate*, "determines **the step size** at each iteration",
   and *Gradient descent*, "for a small enough step size or **learning rate** η ∈ ℝ₊". The frame
   also allows the value to vary between steps, which both sources state:
   *Gradient descent* — "Note that the value of the step size η **is allowed to change at every
   iteration**"; *Learning rate* § *Learning rate schedule* — "A learning rate schedule changes
   the learning rate during learning and is most often changed between epochs/iterations."
5. **The shrinking iterate spacing near the bottom of the bowl.** CONFIRMED qualitatively and
   verified locally. *Learning rate* on why a walk decays:
   > "Decay serves to settle the learning in a nice place and avoid oscillations, a situation
   > that may arise when too high a constant learning rate makes the learning **jump back and
   > forth over a minimum**."
   > "In order to achieve faster convergence, prevent oscillations and getting stuck in
   > undesirable local minima the learning rate is often varied during training either in
   > accordance to a learning rate schedule or by using an adaptive learning rate."

   Local verification (this worker's computation against the certified curve, not a web claim):
   on the convex quadratic `C(x) = 0.00395282·(x−450.41)²` the nine-dot chain gives cost steps of
   28.72, 28.47, 25.72, 19.21, 13.41, 9.83, 7.09, 4.26 fpx and iterate vertical spacing of
   46.47, 31.91, 24.57, 14.64, 9.45, 6.29, 5.01, 4.15 fpx — monotone decreasing in both, no
   overshoot past the minimum. This matches *Gradient descent*'s qualitative statements
   ("strongly convex and lipschitz smooth … **gradient descent converges linearly with a fixed
   step size**") and the decaying-step behaviour both pages describe.
6. **The bowl is a convex quadratic with exactly one minimum — "Minimum" + θ̂.** CONFIRMED by
   Wikipedia *Convex function*:
   > "A twice-differentiable function of a single variable is convex if and only if its second
   > derivative is **nonnegative on its entire domain**."
   > "Visually, a twice differentiable convex function '**curves up**', without any bends the
   > other way (inflection points)."
   > "Well-known examples of convex functions of a single variable include linear functions
   > … **quadratic functions `cx²`** (where `c` is a nonnegative real number) …"
   > "**Any local minimum of a convex function is also a global minimum. A strictly convex
   > function will have at most one global minimum.**"

   The certified build's curve is exactly such a quadratic: display-space
   `C(x) = 0.00395282·(x − 450.41)²` (image-space y is inverted, hence the drawn
   `a = −0.00395282`), i.e. second derivative `+0.0079 fpx⁻² > 0` — strictly convex, one global
   minimiser, which is where the yellow "Minimum" dot and the `θ̂` beneath it sit. *Convex
   function* adds the tie to the fitted form: "a strongly-convex function is a function that
   grows as fast as a quadratic function." CS229 (banked copy, lines 247–249) says the same of
   the course's own objective: "gradient descent always converges (assuming the learning rate α
   is not too large) to the global minimum. Indeed, **J is a convex quadratic function**" — and
   the notes' own figure note on the facing page is the slide's diagram in spirit: "Here is an
   example of gradient descent as it is run to minimize a quadratic function."
7. **Why the object being minimised is a "Cost" at all.** CONFIRMED. Wikipedia *Gradient
   descent*: "Gradient descent is particularly useful in machine learning and artificial
   intelligence for **minimizing the cost or loss function**." Wikipedia *Learning rate*: the
   step is taken "while **moving toward a minimum of a loss function**." Wikipedia *Linear least
   squares* names the objective this deck studies: "The OLS method minimizes the sum of squared
   residuals …" and "Linear least squares problems are **convex** and have a **closed-form
   solution that is unique**, provided that the number of data points used for fitting equals or
   exceeds the number of unknown parameters, except in special degenerate situations." The bowl
   slide 027 draws is the scalar-θ slice of that objective; the same page carries the deck's
   topic anchor: "Various regularization techniques can be applied in such cases, the most
   common of which is called **ridge regression**."
8. **"Random initial value" — GD starts wherever you start it.** CONFIRMED structurally.
   *Gradient descent*: "With this observation in mind, one starts with **a guess x₀** for a local
   minimum of `f`, and considers the sequence `x₀, x₁, x₂, …`" — the source requires *a* start,
   not a *random* one (course-authored initialisation, see below). And because the frame's
   objective is convex, the destination is start-independent: "**When the function f is convex,
   all local minima are also global minima**, so in this case gradient descent can converge to
   the global solution." The frame's dashed drop-line under the first iterate marks that
   arbitrary starting abscissa.
9. **The nine-dot chain has no numeric η, and must not be "corrected" into one.** The frame
   states no numeric learning rate; a least-squares fit over the measured x-chain gives η ≈ 20.45
   frame-px units that reproduces the chain only to ±23.5 fpx, with per-interval implied η
   spanning 13.9 → 55.7 (previous window's computation, re-checked against the shipped
   `build/slide_027.js` geometry). This is consistent with the sources, which never require a
   constant η ("the value of the step size η is allowed to change at every iteration"), and the
   deck's own worked examples use a specific η only when the frame says so (slides 030–032).
   Honest note so no later worker "fixes" the trajectory into a plotted constant-η run.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

Per the binding founder ruling (the founder visually rejected an earlier attempt): the attempt-10
build implements all three findings, and the controlling record is
`recreated_pptx/qa/slide027/adjudication_attempt_9.md`. This research record does not contradict
the frame or that ruling — **the frame wins for recreation**.

- **The black cost curve is ONE SMOOTH quadratic** — founder finding A. Shipped as the analytic
  quadratic `y = −0.00395282·(x−450.41)² + 407.25`, 420 samples at 1 fpx, extent x = 239..658,
  vertex pinned to the yellow minimum at (444.49, 407.25). A course/founder-mandated
  stylisation measured from the frame, not a redraw of any source figure. (Banked with the build:
  the original's two arms are steeper than one full-extent quadratic — a quartic fits the same
  ink at RMS 3.76 fpx vs the quadratic's 6.92 — so the drawn quadratic deviates from the traced
  centre-line by max 16.7 fpx in the arms while the vertex matches to 0.2 fpx. That price is
  measured, recorded and accepted in the build; it is drawing-intent, not an error.)
- **The grey step connectors are ARC ARROWS WITH ARROWHEADS, aligned to the purple dot centres**
  — founder findings B and C. Shipped as nine cubic-Bezier arcs anchored dot-centre→dot-centre on
  the nine measured halo-excluded centroids, each terminated by a filled grey triangle head
  (length 5.4 fpx, half-width 2.7 fpx, tip 6.31–6.58 fpx from the target centre), drawn curve →
  connectors → heads → discs → yellow minimum so each shaft's overrun is covered by its own head
  and then by its disc. Course/founder-mandated stylisation. The sources supply the *idea* of an
  arrowed descent step (item 1) but no source figure for this particular chain.
- **One adjudicated nuance, recorded (not re-litigated).** The founder's description says
  "dashed"; the controlling record §1 measured the original frame's connectors as **solid**
  (95–100 % on-density over their ink spans; no dash cadence measurable anywhere in the chain),
  so the build draws them as solid `CHAIN_GRAY` (#ACACAD) arcs at ~2 fpx. The dashed elements
  that DO exist on the frame are the two dash **leaders** — the x = 262.5 vertical drop-line
  under the first iterate (→ "Random initial value") and the short x = 444.5 collar near the
  minimum — drawn dash-by-dash from the measured dash rows. The substance of the ruling (arc
  arrows with arrowheads, centre-to-centre anchoring) is implemented exactly as mandated; only
  the dash adjective is a description-vs-frame difference already adjudicated there.
- **Palette forensics.** The diagram's ink is the course's own soft-grey/purple/yellow set
  (axis core mean RGB (80,81,79), curve 61, chain 162, labels 112; iterates (97,70,187); minimum
  yellow). None of the host pages' figures can be the origin of that palette: the three source
  figures nearest in kind were pixel-measured by `sources/slide_025_source/SOURCES.md` as
  line-art/grayscale (two of them fully unsaturated, the third grey with a single magenta curve),
  and the *Learning rate* page hosts no figure at all. Do not "fix" toward a source palette.
- **Everything else is course-authored presentation:** the house chrome (grey panel, three red
  strokes, yellow badge with purple ring), the title wording, the five labels, the schematic
  two-arrow axis pair, the number of iterates (nine), the faint grey `+`, the non-overshooting
  trajectory that stops just short of the minimum, and the frame's plot-frame geometry.
- **"Random" in "Random initial value" is the course's initialisation choice** — the sources
  require only "a guess x₀" (item 8). Recorded, not contradicted.

## [?] Uncertain items

- **No web-resolvable `[?]` remains for this slide.** Every claim the frame makes — the
  negative-gradient step direction, the selected learning rate/step size, a convex quadratic
  bowl with one minimum, a "Cost" objective — is CONFIRMED above with live-fetched quotes.
- **One window debt, recorded per the tool-down law:** a live re-fetch of the CS229 Part I notes
  failed from this host 4× this window (`see.stanford.edu/materials/aimlcs229/cs229-notes1.pdf`
  → HTTP 404; `cs229.stanford.edu/notes2021fall/cs229-notes1.pdf` → HTTP 000 ×3). The CS229
  quotes in item 2/6 are therefore carried from the banked byte-verified copy
  (`sources/slide_024_source/cs229-notes1.pdf`, md5 `73241a52de8ca0544803fb5cc5844771`, the exact
  value that record logs as its live-fetch hash), verified locally with `pdftotext -layout`.
  Resolution path: re-run the fetch when the network path to `cs229.stanford.edu` reopens. The
  URL itself is not dead (three sibling records fetched it live) and is NOT a do-not-reuse
  entry — it is a transport failure on this host only.
- Frame-level `[?]`s that stay open **by design**, carried from
  `analysis/slide_027_final.json` and resolved by the build/judge legs, **not** by web research:
  - descent-dot count ("approximately 8" in the analysis record vs the **nine** measured dot
    centres in the controlling record) — resolved by the certified build, which draws nine;
    resolution path = the banked `probe_adj9_geometry_output.txt` / `adj9_geometry.json`;
  - dot hue (`#0000CD` "medium blue" in the analysis record vs the measured frame violet
    (97,70,187)) — resolved at build time against the frame;
  - title font family/size (the analysis record's 32–36 pt estimate) and the exact graph-box
    bounds (the analysis record's 15%–85% / 25%–90% estimates) — resolved by the measured inner
    plot frame (vertical red strokes at cols 193–194 / 715–717, horizontal at rows 166–168 /
    506–508) and the house-chrome/measure bank;
  - the exact wording/typography of the five labels' font sizes.
  Resolution path for all of the above = the slide's own build + zoomed crop judge per
  `shared_patterns/judge_protocol_03.md` (banked under `recreated_pptx/qa/slide027/`), never web
  research.
- Whether the lecturer had a specific figure on screen when filming (Wikipedia's level-set
  illustration, CS229's contour trajectory, another): unresolvable without the video's audio, and
  the content is course-authored either way. Not web-resolvable.
- Whether the drawn trajectory corresponds to a specific numeric learning rate (e.g. the η = 0.2
  of sibling slide 030): the frame states none, and no constant η fits the chain (item 9).
  Resolution path = the video's audio; not needed for the recreation.

## Corrections

- **None applied.** No `analysis/*.json` was edited by this worker: no dimension, attribute or
  provenance guess in `analysis/slide_027_final.json` is contradicted by the four sources in a
  way that requires a patch (the sources describe the general method; the frame's annotations are
  position/hue/count estimates that only the banked build measurements can settle).
- Recorded discrepancies with an evidence trail, for the owning worker to apply if it chooses
  (annotation-level only; **no verbatim frame text was touched**):
  1. `analysis/slide_027_final.json` "approximately 8" descent dots vs **nine** measured dot
     centres — evidence: `recreated_pptx/qa/slide027/adjudication_attempt_9.md` §1
     (`probe_adj9_geometry_output.txt`, `adj9_geometry.json`); the certified build draws nine.
  2. dot hue `#0000CD` vs measured frame violet (97,70,187) — evidence: `adjudication_attempt_9.md`
     §4e (purple matches "within a few units: original (97,70,187)").
  3. graph-box bounds "15%–85% width, 25%–90% height" vs the measured inner plot frame (cols
     193–194 / 715–717; rows 166–168 / 506–508) — evidence: `adjudication_attempt_9.md` §4c.
  4. The frame's connectors, measured SOLID while the founder's ruling describes them as
     "dashed" — evidence: `adjudication_attempt_9.md` §1 ("Dashes: the founder's description says
     'dashed'; the frame's connectors are SOLID"); reconciled in Course-authored elements above.
- Nothing in this record re-opens the certified build: the founder's three findings and the
  attempt-10 ship stand, and per the founder ruling the frame wins for recreation.

## Law reminder

The frame wins for recreation; the source wins for understanding.
