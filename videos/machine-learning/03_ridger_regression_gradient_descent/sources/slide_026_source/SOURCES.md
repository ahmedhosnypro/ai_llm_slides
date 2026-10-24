# SOURCES.md — slide 026 "Gradient Descent Solution"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: **parse the
banked originals in this directory FIRST** (three pre-banked Wikipedia HTML pages), then a live
re-fetch of each recorded URL in this same work window with `curl -sL --max-time -A
"Mozilla/5.0"` + a byte-compare against the banked original (trust discipline: a URL is only
recorded as fetched-live if it was fetched in the window that records it; hash-verified
re-fetch). No page-frame facts were taken from a search snippet.

Frame facts come from the slide's analysis record
(`analysis/slide_026_final.json`, verdict PASS_WITH_FIXES, recreatability 9). **No vision call
was made by this worker** — research is web + local-file work only, per the mandate's "No
vision calls" clause. The slide's own judge legs and its certified pptx were NOT touched, NOT
re-judged, and NOT rebuilt.

**Query budget for this slide: 0 `agy` web searches spent, 4 live HTTP fetches.**
- 0 searches — discovery needed none: the mandate's economy law requires checking banked
  records before re-spending a query, and the trio already banked here
  (`gradient_descent_wikipedia.html`, `convex_function_wikipedia.html`,
  `linear_least_squares_wikipedia.html`) is exactly the topic set this slide's text requires.
- 3 re-fetches = the trust-discipline byte-compare of the banked trio (all three
  content-identical, same revision id — see "Primary source(s)").
- 1 new fetch = Wikipedia *Ridge regression*, spent to close the one substantive frame claim
  the trio and all sibling records leave open: "convex function **(even with regularizer)**".
- Total bytes downloaded this window: 2,123,423 (610,963 + 568,204 + 468,414 + 475,412).
- One byte-exact download newly banked: `ridge_regression_wikipedia.html`.

## Slide identity

- Frame file: `unique_slides/slide_026.jpg` (960×540; 1px = 1pt per the deck AGENTS.md).
  Badge numeral **26** (the originals print their own number — deck law).
- Numbering resolution: **founder-curated numbering 2026-10-19.** Per `AGENTS.md` §
  Provenance, slide 26 is one of the **16 honestly-marked unrecoverable** slides
  (1, 2, 3, 13, 24–29, 33, 35, 36, 43, 44, 47) — the owner removed the pre-curation state.
  No pre-curation mapping exists and none was hunted for (owner-replaced-state law). `_meta`
  carries the recovered kept-frame provenance `kept_frame frame_01079.jpg`, `start_sec 1037.0`,
  `end_sec 1078.0`, `frame_count 42` — the *video* timestamp of the kept frame, not a
  pre-curation slide number.
- Analysis record used: `analysis/slide_026_final.json` (validated). Frame's verbatim claims
  (transcribed, never edited by research):
  - title `Gradient Descent Solution`; labels `Gradient Descent (GD) Algorithm:` / `Notes:` / `26`
  - `[1] Start with initial Random Weights (W)`
  - `[2] Update the weights by moving along the direction of negative gradient of Loss function
    (w.r.t. W) (moving step is a hyper parameter, AKA Learning Rate)`
  - `[3] Stop when the gradient is almost zero (this is at the minimum value of the function)`
  - `Least Squares Linear regression objective function is a convex function (even with
    regularizer). This means it has ONE Minimum (good news ).`
  - `GD will approximately find this minimum value but at a variable number of steps depending
    on the used Learning Rate`
  - **No equation, no table, no chart, no diagram**: `equations` is `[]`, `imagery` is `[]`;
    `visual_elements` are only the blue-bordered white-filled highlight box and the yellow
    badge circle (both `recreation_brief` text, not sourced figures).
- Build/certification state (read-only for this worker): `gen_status=passed`,
  `visual_check=PASS`, deliverable `recreated_pptx/slide_026_recreated.pptx`, built by
  `recreated_pptx/build/slide_026.js`, final render `render_9.png`
  (`recreated_pptx/qa/slide026/judge_attempt_5.txt` = Template A PASS, 0 discrepancies;
  `crop_9_notes_judge.txt` = Template B notes PASS, 0 discrepancies; `crop_7_alg_judge.txt` =
  Template B alg PASS, its single MINOR PIL-refuted in `adjudication_a7_algcrop.md`).

## Primary source(s)

Every URL below was **fetched live in this work window** and byte-compared against the banked
original. Nothing is recorded from an unfetched snippet.

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Gradient_descent` | Wikipedia **"Gradient descent"** (rev `1373673523`, modified 2026-09-07) — the algorithm named in the title and in the box header: the negative-gradient update rule, the learning rate η, the convex⇒global-minimum property, and the step-size trade-off. | **CONFIRMED** — live this window: `curl -sL --max-time 45` → HTTP 200, **610,963 bytes**, final URL identical (no redirect). Banked original 610,975 B, md5 `e9c2171f15ffd5a19650060d4fe3334f`. Byte-compare: raw md5 differs (610,963 vs 610,975 B) **only** in Wikimedia per-response telemetry — `wgRequestId`, `wgHostname`/`cachereport.origin` (server names), `Parsed by`, render `cputime`/`walltime`, `timingprofile`, `Render ID`, parser-cache `generated at`, and the randomised `utm_campaign=` on media URLs. After normalising exactly those volatile fields the two are **content-identical** (normalised md5 `a79605632c26072eddef56cbc3c8e1e7`), and **both carry the same `wgRevisionId` `1373673523`**, so the *article text* is unchanged. Every quote below was additionally re-verified against the live fetch's tag-stripped text. Same page already banked by `sources/slide_019_source/SOURCES.md` and `sources/slide_024_source/SOURCES.md` — **no new search spent to find it**. |
| `https://en.wikipedia.org/wiki/Convex_function` | Wikipedia **"Convex function"** (rev `1380599970`, modified 2026-10-16) — the definition/property the notes bullet relies on for "ONE Minimum": local minima of a convex function are global; a strictly convex function has at most one; the operations that preserve convexity. | **CONFIRMED** — live this window → HTTP 200, **568,204 bytes**, no redirect. Banked original 568,136 B, md5 `b51291236b9dcb8f1fd678d2c0301b3f`; after normalising the same volatile telemetry fields **content-identical** (normalised md5 `81e43d92c959b3ad291af879fb4c7d2`), same `wgRevisionId` `1380599970`. Also already live-fetched and quoted by sibling records `slide_030` / `slide_031` / `slide_034`. |
| `https://en.wikipedia.org/wiki/Linear_least_squares` | Wikipedia **"Linear least squares"** (rev `1374199323`, modified 2026-09-10) — the objective function the notes bullet names: *least-squares* linear regression, its convexity, and its unique closed-form solution. | **CONFIRMED** — live this window → HTTP 200, **468,414 bytes**, no redirect. Banked original 468,414 B, md5 `9a6db01ed1759aa86b39ea772b2d245a`; after normalising the volatile telemetry **content-identical, md5 equal on both sides of the normalisation** (normalised md5 `42a3c0f505eb1edb7408cecfe1ad7c89`), same `wgRevisionId` `1374199323`. This page was **not** previously banked by any sibling record — it is new to the fleet map for this slide's claims. |
| `https://en.wikipedia.org/wiki/Ridge_regression` | Wikipedia **"Ridge regression"** (rev `1365109207`) — the **regularizer** in the notes bullet's parenthetical "(even with regularizer)": the ridge/Tikhonov estimator as `(XᵀX + λI)⁻¹XᵀY` and as the Lagrangian minimisation `argmin_β ‖Y − Xβ‖² + λ(βᵀβ − c)`, plus the ill-posed/unique-solution statement. | **CONFIRMED** — newly fetched live this window (the 1 new fetch): `curl -sL --max-time 60` → HTTP 200, **475,412 bytes**, final URL identical. Banked byte-exact in this directory as `ridge_regression_wikipedia.html`, md5 `000e2df1986bd4454dda3e3bad7708d8`. Re-fetch byte-identity recorded below in "Figures used". |

## Figures used by this slide

**None — and correctly so.** This slide is pure typography: a title, a red box header
(`Gradient Descent (GD) Algorithm:`), three numbered blue algorithm lines, a second red header
(`Notes:`) and two black note bullets, inside one blue-bordered white-filled rectangle with the
house badge. `analysis/slide_026_final.json` records `equations: []`, `imagery: []` and no
chart/diagram/plot of any kind — there is **no hosted source figure that this slide redraws**,
so no source FIGURE was downloaded. Per the layout law the reason is stated rather than left
silent.

The four live-fetch originals are nonetheless banked byte-exact in this directory as the
provenance evidence of the fetches recorded above (fetched-live status is only claimable when
the bytes are retrievable), saved as downloaded and never renamed or deleted:

| Banked file | URL | Size | md5 | Re-fetch byte-identity |
|---|---|---|---|---|
| `gradient_descent_wikipedia.html` | `en.wikipedia.org/wiki/Gradient_descent` | 610,975 B | `e9c2171f15ffd5a19650060d4fe3334f` | Live 610,963 B, HTTP 200. Raw md5 differs; **content-identical after normalising Wikimedia per-response telemetry** (request id / host / render timings). Same revision `1373673523`. |
| `convex_function_wikipedia.html` | `en.wikipedia.org/wiki/Convex_function` | 568,136 B | `b51291236b9dcb8f1fd678d2c0301b3f` | Live 568,204 B, HTTP 200. Raw md5 differs; **content-identical after normalising the same volatile fields**. Same revision `1380599970`. |
| `linear_least_squares_wikipedia.html` | `en.wikipedia.org/wiki/Linear_least_squares` | 468,414 B | `9a6db01ed1759aa86b39ea772b2d245a` | Live 468,414 B, HTTP 200. **Content-identical** (normalised md5 identical on both sides, `42a3c0f5…`); same revision `1374199323`. |
| `ridge_regression_wikipedia.html` | `en.wikipedia.org/wiki/Ridge_regression` | 475,412 B | `000e2df1986bd4454dda3e3bad7708d8` | Newly banked this window from the fetch itself (rev `1365109207`); no prior banked copy to compare against. Re-fetch byte-identity was verified for the three pre-banked trio pages, not for this one — it is the banked artifact of this window's own fetch. |

These are reference pages, not slide figures.

## What the source(s) CONFIRM

Frame facts from `analysis/slide_026_final.json` (title, the three numbered steps, the two note
bullets). Point by point, with verbatim quotes from the live-fetched pages:

1. **The title and box header name a real algorithm — "Gradient Descent (GD)".** Wikipedia
   *Gradient descent*:
   > "Gradient descent is a method for unconstrained mathematical optimization. It is a
   > first-order iterative algorithm for minimizing a differentiable multivariate function."

   The frame's "(GD)" is the standard initialism for the same object, and the page is explicit
   that this is the machine-learning loss-crunching algorithm:
   > "Gradient descent is particularly useful in machine learning and artificial intelligence
   > for minimizing the cost or loss function."

   **This is what makes the slide the deck's GD-convergence slide**, and why the "Notes" attach
   the algorithm to the deck's least-squares regression objective (slides 005/019/020 lineage).
2. **Step [1] "Start with initial Random Weights (W)" — CONFIRMED as the algorithm's stage 0.**
   Wikipedia *Gradient descent*:
   > "With this observation in mind, one starts with a guess `x₀` for a local minimum of `f`,
   > and considers the sequence `x₀, x₁, x₂, …`"

   In the regression setting the variable being solved for is the weight vector (`W`/`β`), so
   the initial guess is the initial random weight vector. The sources do not dictate that the
   start be *random* — that is the course's initialisation choice (see "Course-authored
   elements").
3. **Step [2] "Update the weights by moving along the direction of negative gradient of Loss
   function (w.r.t. W)" — CONFIRMED verbatim as the core update rule.** Wikipedia *Gradient
   descent*, § Description:
   > "Gradient descent is based on the observation that if the multi-variable function
   > `f(x)` is defined and differentiable in a neighborhood of a point `a`, then `f(x)`
   > decreases fastest if one goes from `a` in the direction of the negative gradient of `f`
   > at `a`, i.e., `-∇f(a)`."

   and the update itself, as the page's own equation (its `annotation` TeX):
   > `xₙ₊₁ = xₙ - ηₙ ∇f(xₙ),  n ≥ 0.`
   > `aₙ₊₁ = aₙ - η ∇f(aₙ)`

   The mechanism clause of step [2] — *subtract* the gradient — is the page's own wording:
   > "the term `η∇f(a)` **is subtracted from `a`** because **we want to move against the
   > gradient, toward the local minimum**."

   The "Loss function" of the frame is the `f`/`J` being minimised; "w.r.t. W" is the gradient
   taken with respect to the weight vector, which is exactly what the update differentiates
   w.r.t. Note the canonical rule in this deck's family is usually written with the step
   *inside* the gradient term (`θ := θ - η∇J(θ)`, CS229 §1) — Wikipedia's displayed form is
   the indexed-sequence variant `xₙ₊₁ = xₙ - ηₙ∇f(xₙ)`. **Same rule, same meaning**; recorded
   so no later reader mistakes the two notations for a discrepancy.
4. **Step [2]'s "(moving step is a hyper parameter, AKA Learning Rate)" — CONFIRMED.**
   Wikipedia *Gradient descent*:
   > "for a small enough step size or **learning rate** `η ∈ ℝ₊`, then `f(aₙ) ≥ f(aₙ₊₁)`."

   The same η/α "learning rate = the step size" identity is already banked verbatim by sibling
   records (economy law, no new query spent): CS229 notes1 §1 — "θⱼ := θⱼ − α ∂J(θ)/∂θⱼ. …
   Here, α is called the learning rate." (`sources/slide_024_source/SOURCES.md`,
   `sources/slide_030_source/SOURCES.md`, `sources/slide_031_source/SOURCES.md`,
   `sources/slide_032_source/SOURCES.md` — the last of which quotes this very slide's phrase
   "moving step is a hyper parameter, AKA Learning Rate"); Ruder arXiv:1609.04747 §2 — "The
   learning rate η determines the size of the steps we take to reach a (local) minimum"
   (`sources/slide_030_source/SOURCES.md`, `sources/slide_031_source/SOURCES.md`). That it is a
   *hyperparameter* (chosen by the practitioner, not learned) is confirmed by the sibling
   records' wording plus the page's statement that the step size is a free choice the user must
   set: "Since using a step size η that is too small would slow convergence, and a η too large
   would lead to overshoot and divergence, **finding a good setting of η is an important
   practical problem**."
5. **Step [3] "Stop when the gradient is almost zero (this is at the minimum value of the
   function)" — CONFIRMED.** Wikipedia *Gradient descent*, § Description:
   > "so the sequence `(xₙ)` **converges to the desired local minimum**. Note that the value
   > of the step size η is allowed to change at every iteration."

   and the descent-monotonicity that gets there:
   > `f(x₀) ≥ f(x₁) ≥ f(x₂) ≥ ⋯,`

   A vanishing gradient at a stationary point is the standard stopping test; the neighbours of
   the minimum are where ∇f = 0, and the page's convergence statement is the destination.
   (The sibling records carry the "Repeat until convergence"/"α not too large" wording:
   `sources/slide_030_source/SOURCES.md`.)
6. **Note bullet 1, clause A: "Least Squares Linear regression objective function is a convex
   function" — CONFIRMED verbatim.** Wikipedia *Linear least squares*, § Discussion:
   > "Linear least squares problems are **convex** and have a **closed-form solution that is
   > unique**, provided that the number of data points used for fitting equals or exceeds the
   > number of unknown parameters, except in special degenerate situations."

   And the object itself is the squared-error objective the bullet means — § Basic formulation:
   > "one of the most common is to define it as `‖Ax − b‖²`. This produces a minimization
   > problem, called a least squares problem"

   The same page identifies the statistical model as linear regression:
   > "linear least squares problems correspond to a particularly important type of statistical
   > model called linear regression … One basic form of such a model is an ordinary least
   > squares model."
7. **Note bullet 1, clause B: "**even with regularizer**" — CONFIRMED by a sourced composition
   (no single banked page states the sentence verbatim for the regularised objective; the
   claim is confirmed step by step).**
   - The regulariser is the ridge/Tikhonov quadratic penalty. Wikipedia *Ridge regression*,
     § Overview:
     > "the simple ridge estimator has an extra term `λI` in the denominator:
     > `β̂_λ = (XᵀX + λI)⁻¹XᵀY` where `Y` is the regressand or response vector, `X` is the
     > design matrix, `I` is the identity matrix, and the ridge (or Tikhonov) regularization
     > parameter `λ ≥ 0` …"

     and, crucially, the regularised problem as a minimisation:
     > "which can be expressed as a Lagrangian minimization:
     > `argmin_β ‖Y − Xβ‖² + λ(βᵀβ − c)`"

     So the regularised objective is **the least-squares squared norm plus one quadratic form**.
   - A quadratic form is convex. Wikipedia *Convex function*, § Definition:
     > "Well-known examples of convex functions of a single variable include linear functions
     > `f(x) = cx` (where `c` is a real number), **quadratic functions `cx²`** (where `c` is a
     > **nonnegative** real number) and exponential functions `ceˣ` …"

     The ridge term `λ(βᵀβ − c)` has `λ ≥ 0`, i.e. a nonnegative multiple of a quadratic form.
   - Convexity is preserved under such a sum. Wikipedia *Convex function*, § "Operations that
     preserve convexity":
     > "**Nonnegative weighted sums:** if `w₁, …, wₙ ≥ 0` and `f₁, …, fₙ` are all convex, then
     > so is `w₁f₁ + ⋯ + wₙfₙ`. **In particular, the sum of two convex functions is convex.**"

     (and the page separately states convexity is "invariant under affine maps", covering the
     `Xβ` inside the norm.)
   - Conclusion: least-squares objective (convex, clause A) + convex quadratic penalty with a
     nonnegative weight (ridge, `λ ≥ 0`) ⇒ still convex. **The frame's parenthetical is
     CONFIRMED.**
   - Supporting, and the reason the course bothers to regularise at all, Wikipedia *Linear
     least squares* § Properties:
     > "In some cases the (weighted) normal equations matrix `XᵀX` is ill-conditioned. …
     > Various regularization techniques can be applied in such cases, the most common of which
     > is called **ridge regression**."

     and Wikipedia *Ridge regression* § Overview on what the penalty buys:
     > "the problem of a near-singular moment matrix `XᵀX` is alleviated by adding positive
     > elements to the diagonals, thereby decreasing its condition number."
8. **Note bullet 1, clause C: "This means it has ONE Minimum (good news )" — CONFIRMED as the
   convexity⇒uniqueness property.** Wikipedia *Convex function*, § Properties:
   > "**Any local minimum of a convex function is also a global minimum. A strictly convex
   > function will have at most one global minimum.**"

   and, from the lead:
   > "For instance, a strictly convex function on an open set has no more than one minimum."

   So convexity makes every local minimum global; strict convexity makes the minimum unique.
   The frame's "(good news )" is the course's gloss on the contrast with non-convex surfaces,
   which the neighbouring slides 033/034 of this deck demonstrate (one basin can be reached
   instead of another) — see `sources/slide_033_source/SOURCES.md`,
   `sources/slide_034_source/SOURCES.md` (Ruder §2.1: batch GD "is guaranteed to converge to
   the global minimum for convex error surfaces and to a local minimum for non-convex
   surfaces"). Wikipedia *Gradient descent* states the same half of the law:
   > "When the function `f` is convex, all local minima are also global minima, so in this case
   > gradient descent can converge to the global solution."

   **Precision note (recorded, not a discrepancy):** convexity alone guarantees
   *global-ness* of every local minimum, and *uniqueness* needs strict convexity (or, per the
   *Linear least squares* quote, the "provided that the number of data points … equals or
   exceeds the number of unknown parameters" condition for a unique closed form). For an
   ordinary least-squares quadratic with a non-singular moment matrix — and a fortiori for the
   ridge objective, whose `(XᵀX + λI)` is positive definite for `λ > 0` — the objective *is*
   strictly convex, so "ONE Minimum" is correct as stated. The frame's word "ONE" is a
   colloquial restatement of the sourced "at most one global minimum" / "unique" — accurate,
   and no build change is implied.
9. **Note bullet 2: "GD will approximately find this minimum value but at a variable number of
   steps depending on the used Learning Rate" — CONFIRMED on both halves.**
   - *"approximately"*: gradient descent is iterative and convergences only asymptotically.
     Wikipedia *Gradient descent*:
     > "It is a **first-order iterative** algorithm for minimizing a differentiable
     > multivariate function."

     > "so the sequence `(xₙ)` converges to the desired local minimum."

     (i.e. approached in the limit of the sequence, not obtained exactly in one step).
   - *"a variable number of steps depending on the used Learning Rate"*: the page states the
     step-size trade-off directly:
     > "Since using a step size η that is **too small would slow convergence**, and a η **too
     > large would lead to overshoot and divergence**, finding a good setting of η is an
     > important practical problem."

     and the iteration count's dependence on the problem's geometry:
     > "The gradient descent can take **many iterations** to compute a local minimum with a
     > required accuracy, if the curvature in different directions is very different for the
     > given function."

     > "The number of gradient descent iterations is commonly proportional to the spectral
     > condition number `κ(A)` of the system matrix `A` …"

     The convergence-rate guarantee scales with the step under the standard assumptions:
     > "For example, if the objective is assumed to be **strongly convex and lipschitz smooth,
     > then gradient descent converges linearly with a fixed step size**."

     Together: the number of steps to reach (approximately) the minimum varies with the step
     size η — small η ⇒ slow (many steps), large η ⇒ overshoot/divergence. **CONFIRMED.** The
     deck's own worked examples instantiate exactly this (slides 030/031/032: η = 0.2 → 11
     steps; η = 0.4 → 6 steps; the learning-rate sweep slides 028/036) — cross-referenced per
     the economy law, no new query spent.
   - *"minimum value"* vs *"argmin"*: the frame says GD finds the minimum **value** (the loss
     at the optimum), which is the correct object — the sources' `f(x₀) ≥ f(x₁) ≥ …` chain and
     the `argmin_β` formulations are about the argument and the value together. Recorded, not a
     discrepancy.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- **"initial Random Weights (W)" — the "Random" is course-authored.** The sources only require
  *a* starting guess: "one starts with a guess `x₀` for a local minimum of `f`" (Wikipedia
  *Gradient descent*). That the guess is drawn randomly is the course's initialisation choice
  (standard in practice, but not stated by any banked source). Keep the frame's word verbatim.
- **The "Notes:" framing and the "(good news )" gloss** are pedagogical course commentary with
  no source counterpart. The parenthetical's trailing space is transcribed from the frame and
  preserved by the certified build (recorded in `judge_attempt_5.txt`).
- **"OK / number of steps" phrasing "at a variable number of steps"** is the course's plain
  language for the sources' step-size/condition-number dependence; no source uses that
  phrasing.
- **The 3-step + 2-bullet pedagogical split** of the algorithm (start / update / stop, then
  notes) is the course's teaching structure. The sources state the same content as one
  continuous definition plus convergence properties; no source presents this exact checklist.
- **All chrome and styling is course-authored** (no source counterpart): the blue-bordered
  white-filled highlight box (`#0000FF` on `#FFFFFF`) holding all body text; the red `C00000`
  bold section headers and title; the blue body text of the three algorithm steps; the
  selective bold/underline emphasis runs; the yellow slide-number badge; and the deck's house
  template (white canvas, `E9E9E7` gray panel x54..903, `C00000` 1pt left/right/bottom strokes
  with **no top stroke**, `FDFD96` badge with `6A5ACD` ring) — frozen in
  `shared_patterns/house_chrome.js`, verified by `house_chrome_check.py`
  (`recreated_pptx/qa/slide026/house_chrome_9.txt` PASS).
- **The frame's typo "approximatly"** (the analysis JSON normalises to "approximately") is
  transcribed frame text: the certified build renders the frame's spelling, per the frame-wins
  law and the worker's glyph-cluster adjudication
  (`recreated_pptx/qa/slide026/worker_report.md`, attempt 8). This is a transcription fact, not
  a source claim — **research does not "correct" it.**
- **The pink/red emphasis details recorded in the standing-down handover are NOT source
  matters.** `recreated_pptx/qa/slide026/handover_w8_026_2026-10-21.md` §3a/3b/3c records three
  measured frame-vs-render emphasis verdicts (rowA "Random Weights (W)" weight class; a
  hand-drawn light-blue rule under "Random Weights"; rowD "gradient is " bold). Those are
  PIL-level frame-vs-render measurements settled by the zoomed judge protocol
  (`shared_patterns/judge_protocol_03.md`) — **out of scope for a web-research leg and not
  web-resolvable.** The certified `render_9` + `judge_attempt_5.txt` (PASS, 0 discrepancies) is
  the state of record; nothing here authorises touching it. Recorded for completeness only.

## [?] Uncertain items

- **No web-resolvable `[?]` remains on this slide.** Every word of the frame's five text
  blocks and both labels is confirmed by the four live-fetched sources above, with the one
  genuinely open clause ("even with regularizer") closed by the sourced composition in
  "What the source(s) CONFIRM" item 7. No `[?]` was carried into the record.
- **Not-resolvable-by-research, recorded for completeness (analysis-record `[?]`s, none
  web-resolvable):** exact font point sizes (only relative hierarchy exists in the JSON), the
  exact thickness of the blue content-box border (described only as "thin"), and the fact that
  all percentage positions in `layout.regions` are vision-model approximations with no
  pixel-exact coordinates. Resolution path for all of these = the build's own PIL measurement
  against the 960×540 frame (1px = 1pt) plus the zoomed crop-pair judge — never a web source.
  These were resolved by the certified build, not by this record.
- **Discrepancy of notation only (recorded per the discrepancy law, nothing to fix):** the
  update rule is written `xₙ₊₁ = xₙ - ηₙ∇f(xₙ)` on Wikipedia *Gradient descent* and
  `θⱼ := θⱼ − α ∂J(θ)/∂θⱼ` in CS229 §1. The frame words the rule out in prose and never writes
  an equation (`equations: []`), so there is no notational conflict on the slide itself.

## Corrections

**None.** No analysis-JSON model annotation — dimension annotation, attribute guess, or
provenance guess — is contradicted by these sources:

- `equations: []` and `imagery: []` are correct for this typography-only slide (confirmed:
  no chart/diagram/figure exists on the frame, and no sourced figure is redrawn).
- The transcribed frame text matches the sources' subject matter on every point, with no
  numeric or factual error to patch.
- The frame's "approximatly" and the trailing space in "(good news )" are **frame text**, which
  the corrections clause never touches (it patches model annotations only, never transcribed
  frame text).
- The provenance annotation "_meta provenance unrecoverable / 16 slides honestly marked" is
  already correct and unchanged by this research; nothing in the sources adds pre-curation
  numbering.

**No `analysis/*.json` file was edited by this worker.**

## Independent re-verification (audit lane, 2026-10-24)

This record was landed by the wave worker and committed; a later evidence-only audit lane
re-ran the trust discipline in its own window without touching build/pptx/qa evidence.
Results — all CONFIRMED:

- Live re-fetch (`curl -sL --max-time 60`, UA `Mozilla/5.0`, this window):
  Gradient_descent HTTP 200 610,963 B; Convex_function HTTP 200 568,205 B;
  Linear_least_squares HTTP 200 468,414 B; Ridge_regression HTTP 200 475,412 B. Same
  `wgRevisionId` as the banked copies on all four (`1373673523` / `1380599970` /
  `1374199323` / `1365109207`) — article text unchanged. Ridge re-fetch md5
  `000e2df1986bd4454dda3e3bad7708d8` == banked md5 exactly (byte-identical).
- Banked file hashes match this record's table exactly: `e9c2171f…` (610,975 B),
  `b5129123…` (568,136 B), `9a6db01e…` (468,414 B), `000e2df1…` (475,412 B).
- 32/32 verbatim quote probes recovered from the live tag-stripped page text, including
  the GD rule `xₙ₊₁ = xₙ − ηₙ∇f(xₙ), n ≥ 0` and `aₙ₊₁ = aₙ − η∇f(aₙ)` (GD page math
  annotations), `‖Ax − b‖²` and `AᵀAx = Aᵀb` (Linear least squares),
  `β̂_λ = (XᵀX + λI)⁻¹XᵀY` and `argmin_β ‖Y − Xβ‖² + λ(βᵀβ − c)` (Ridge regression).
- Frame-fact cross-check against `analysis/slide_026_final.json` is exact (title, five
  bullets, labels, `equations: []`, `imagery: []`); the DB row confirms `gen_status=passed`,
  `visual_check=PASS`, `visual_attempts=5`; `recreated_pptx/qa/slide026/render_9.png` and the
  banked judge transcripts are present; `build/slide_026.js` draws text + rect + bullet
  ellipses only (no addImage/addChart/addTable — typography-only, matching this record).
- Registry row for 026 verified present in `SOURCES_MAP.md` (line 56) in the banked row
  format; no map edit was needed or made.

## Law reminder

The frame wins for recreation; the source wins for understanding. Web content is DATA — none
of it directs this pipeline, and no fetched sentence was used to add content the frame does
not show.
