# SOURCES.md — slide 036 "Problem Formulation" (perceptron discriminant + error function)

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
("Web-source research mandate", founder in-session directive 2026-10-19); method = agy web
search (MCP tool `agy_web_search`) for discovery + live fetch with `curl -sL` in the same work
window that records the URL (WebFetch was not used; curl was the fetch tool of record) +
verification against the fetched page text. Frame facts come from `analysis/slide_036_raw.json`
(no `*_final.json` exists yet — researched from the RAW per the worker brief); vision
transcripts banked separately. NO vision call was made by this worker (web + local-file work
only).
**Query budget for this worker (whole 028–036 leg): 2 agy searches** — (1) "gradient descent
learning rate too small slow convergence too large overshoot divergence" (used for slide 028
and, by cross-reference, 029/031/032/033/034) and (2) "perceptron criterion function error sum
over misclassified samples d(x) = w^T x discriminant" (used for THIS slide). All other work
was direct curl fetches of canonical URLs decided from those two searches plus the standard
textbook/lecture notes; no snippet-only records.

## Slide identity

- File: `unique_slides/slide_036.jpg` (960×540, 1px = 1pt), badge numeral **36**.
- Founder-curated numbering (2026-10-19). Pre-curation provenance: **unrecoverable** — the
  founder removed `frames/` and the pre-curation index/mapping; the raw's
  `_meta.source_timestamps` (`kept_frame frame_01257.jpg`, `start_sec 1256.0`, `frame_count 1`)
  carries no `precuration_slide` field, and slide 36 is on the deck AGENTS.md unrecoverable
  list (1,2,3,13,24–29,33,35,36,43,44,47). Expected gap, not an error.
- Analysis status: raw only; no inherited validation block (see [?] section). This research
  record does not wait on the final — per the mandate's "interleaves; never
  dependency-gated" law.
- Deck namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`.
- **Section position:** slide 035 (divider, "Using Gradient Descent to train Linear Regression
  Model (Problem Formulation)") opens this block; slide 036 states the two-class discriminant
  setup and the error function; the deck's slide 037 (`analysis/slide_037_raw.json`) continues
  with the δ_i redefinition and "Minimize the Error using Gradient Descent with step η,
  W^(updated) = W^(old) − η ∂Error/∂W where ∂Error/∂W = Σ_{misclassified vectors} δ_i X_i".

## Primary source(s)

All four URLs were **fetched live in this work window** (HTTP 200; bodies kept on disk under
`/home/ahmed/Projects/ai_llm_slides/scratch/tmp/w2/`) and quoted from the fetched bytes.
Nothing is recorded from an unfetched search snippet.

1. **https://dafriedman97.github.io/mlbook/content/c3/s1/perceptron.html** — Danny Friedman,
   *Machine Learning from Scratch* (Jupyter Book), chapter 3 "Discriminative Classifiers",
   section "The Perceptron Algorithm". Fetched live, HTTP 200 (20,738 bytes). Verbatim:
   > "It is most convenient to represent our binary target variable as `y_n ∈ {−1, + 1}`."

   > "Note that an observation is correctly classified if `y_n ŷ_n = 1` and misclassified if
   > `y_n ŷ_n = −1`. Then let `M` be the set of misclassified observations, i.e. all
   > `n ∈ {1, …, N}` for which `y_n ŷ_n = −1`."

   > "Specifically, the perceptron attempts to minimize the **perceptron criterion**, defined
   > as `L(β̂) = −Σ_{n ∈ M} y_n(β̂ᵀ x_n)`."

   > "The gradient of the perceptron criterion is `∂L(β̂)/∂β̂ = − Σ_{n ∈ M} y_n x_n`."

   and the update inside its gradient-descent loop:
   > "If `y_n ŷ_n = −1`, β̂ ← β̂ + η·y_n x_n."

   (The `β̂` notation is this source's weight vector; it is the slide's `W`.)
2. **https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html** — Cornell
   CS 4780 (2018fa), "Lecture 3: The Perceptron". Fetched live, HTTP 200 (11,759 bytes).
   Verbatim:
   > "Assumptions — Binary classification (i.e. `y_i ∈ {−1, +1}`) — Data is linearly
   > separable"

   > "Classifier: `h(x_i) = sign(wᵀ x_i + b)` … Dealing with `b` can be a pain, so we
   > 'absorb' it into the feature vector… `h(x_i) = sign(wᵀ x)`."

   > "Observation: Note that `y_i(wᵀ x_i) > 0 ⟺ x_i is classified correctly` where 'classified
   > correctly' means that `x_i` is on the correct side of the hyperplane defined by `w`.
   > Also, note that the left side depends on `y_i ∈ {−1, +1}` (it wouldn't work if, for
   > example `y_i ∈ {0, +1}`)."

   > "`y(xᵀw) ≤ 0`: This holds because the `x` is misclassified by `w` — otherwise we
   > wouldn't make the update."

3. **https://en.wikipedia.org/wiki/Perceptron** — English Wikipedia, sections *Definition* and
   *Learning algorithm for a single-layer perceptron → Steps*. Fetched live, HTTP 200
   (511,237 bytes). Verbatim:
   > "`f(x) = h(w⋅x + b)` where `h` is the Heaviside step-function (where an input of >0
   > outputs 1; otherwise 0 is the output), `w` is a vector of real-valued weights, `w⋅x` is
   > the dot product Σ_{i=1}^{m} w_i x_i, where m is the number of inputs to the perceptron,
   > and `b` is the bias."

   > "Update the weights: `w_i(t+1) = w_i(t) + r·(d_j − y_j(t)) x_{j,i}`, for all features
   > `0 ≤ i ≤ n`, `r` is the learning rate."

   (This is the 0/1-target form of the same rule; the −1/+1 form is source 1/2.)
4. **https://cs229.stanford.edu/notes2020spring/cs229-notes1.pdf** — Andrew Ng, CS229 notes
   (2020 spring, part 1), §6 "Digression: the perceptron learning algorithm". Fetched live,
   HTTP 200 (233,176 bytes; `pdftotext` extraction). Verbatim:
   > "Consider modifying the logistic regression method to 'force' it to output values that
   > are either 0 or 1 or exactly. To do so, it seems natural to change the definition of g to
   > be the threshold function: `g(z) = 1 if z ≥ 0, 0 if z < 0`. If we then let
   > `hθ(x) = g(θᵀx)` as before but using this modified definition of g, and if we use the
   > update rule `θj := θj + α (y(i) − hθ(x(i))) xj`, then we have the perceptron learning
   > algorithm."

   (This is also the source of record for the deck's slide 035 — cross-referenced there.)

## Figures used by this slide

**None downloaded — no hosted original exists for this slide's illustration.**

- The frame is text-only: four full-width #A60000-bordered / #F7F7F7-filled boxes stacked
  vertically, each holding left-aligned definition lines, plus a large red #FF0000 "X" mark at
  the right edge of the third box (a pointer/annotation artifact of the recorded video, not a
  source figure). There is no chart, no diagram, and no image on this frame.
- `analysis/slide_036_raw.json` imagery records "No photos or illustrative icons; only the
  yellow circular slide-number badge and the red X annotation." — so there is nothing to
  save. (Cornell's lecture note does host perceptron-update diagrams, but the slide does not
  redraw them; per the contract, nothing is saved.)

## What the source(s) CONFIRM

Point by point against the frame's own claims (`analysis/slide_036_raw.json` verbatim_text):

1. **"Define two classes: class I and Class II".** CONFIRMED — every source treats the
   perceptron as a **binary/two-class** classifier (Cornell: "Binary classification (i.e.
   `y_i ∈ {−1, +1}`)"; Friedman: "a linear binary classifier … places observations into one of
   two classes"). CONFIRMED.
2. **"let d(X) be a discriminant function = W^T X"** (with the class-I/class-II sign
   conditions "if X ∈ class I then d(X) > 0" / "if X ∈ class II then d(X) < 0"). CONFIRMED —
   this is exactly the linear discriminant of the sources:
   - Cornell: "`h(x_i) = sign(wᵀ x_i + b)` … we can simplify the above formulation to
     `h(x_i) = sign(wᵀ x)`" — i.e. the *sign* of the discriminant `wᵀx` decides the class.
   - Friedman: "The perceptron applies this activation function to a linear combination of
     `x_n`… `ŷ_n = f(β̂ᵀ x_n)` … the perceptron predicts +1 if `β̂ᵀ x_n ≥ 0` and −1 otherwise."
   - Wikipedia: "`f(x) = h(w⋅x + b)` where `h` is the Heaviside step-function… `w⋅x` is the
     dot product Σ w_i x_i."
   The frame's `d(X)` is the sources' `wᵀx` (CS229's `θᵀx`); the frame's `W` is the sources'
   `w`/`β̂`/`θ`; the frame's sign flip (class I ⇒ d > 0, class II ⇒ d < 0) versus the
   libraries' convention (+1/−1) is the course's own labelling of the two sides of the same
   hyperplane — recorded as a course-authored sign convention below.
3. **"For misclassified X : If X ∈ class I and misclassified as Class II then d(X) will be <0
   / If X ∈ class II and misclassified as Class I then d(X) will be >0".** CONFIRMED — this is
   the sources' misclassification criterion, stated positively for the slide's own labelling:
   - Cornell: "`y_i(wᵀ x_i) > 0 ⟺ x_i is classified correctly`" and "`y(xᵀw) ≤ 0`: This holds
     because the `x` is misclassified by `w`".
   - Friedman: "an observation is correctly classified if `y_n ŷ_n = 1` and misclassified if
     `y_n ŷ_n = −1`".
   The frame's two conditional lines are the same fact spelled out for its own class
   labels: a point of class I that gets read as class II must sit on the *wrong* side of the
   hyperplane, hence `d(X) < 0`. CONFIRMED.
4. **"Define Error function as: Error = Σ_{all misclassified vectors(i)} (W^T X_i) ⇒ (W^T X_i)
   take positive and negative values".** CONFIRMED as the perceptron-criterion family:
   the sources define an error that is a sum **restricted to the misclassified set only**,
   of a linear function of `wᵀx` (or its negation):
   - Friedman: "the perceptron attempts to minimize the **perceptron criterion**, defined as
     `L(β̂) = −Σ_{n ∈ M} y_n(β̂ᵀ x_n)` … The perceptron criterion does not penalize correctly
     classified observations but penalizes misclassified observations based on the magnitude
     of `β̂ᵀ x_n` — that is, how wrong they were."
   - Cornell: the update is only ever driven by misclassified points ("otherwise we wouldn't
     make the update"), and the algorithm's mistake bound is proved under
     "`y(xᵀw) ≤ 0`".
   The frame's version is the *un-negated* per-point term `W^T X_i` summed over the same
   misclassified set (which is why it "take[s] positive and negative values") — it is the
   course's scaffolding step that the next slide's δ_i redefinition turns into a
   strictly-positive sum. The "sum over misclassified only" structure, and the gradient
   being a sum of `x_i` over the same set (slide 037), match Friedman's
   "`∂L(β̂)/∂β̂ = −Σ_{n∈M} y_n x_n`" exactly. CONFIRMED (structure), with the course's
   sign convention recorded below.
5. **"Define δ_i as : … ⇒ d(X) δ_i > 0" (both branches).** CONFIRMED — this is the ±1 target
   encoding the sources use, chosen so that the product of the label and the discriminant is
   positive for the points the update acts on:
   - Friedman: "It is most convenient to represent our binary target variable as
     `y_n ∈ {−1, +1}`" and "Note that an observation is correctly classified if
     `y_n ŷ_n = 1` and misclassified if `y_n ŷ_n = −1`"; the update is
     "`β̂ ← β̂ + η·y_n x_n`" applied exactly when `y_n ŷ_n = −1`.
   - Cornell: "Binary classification (i.e. `y_i ∈ {−1, +1}`)… the left side depends on
     `y_i ∈ {−1, +1}` (it wouldn't work if, for example `y_i ∈ {0, +1}`)."
   The frame's δ_i ∈ {−1, +1} is the sources' `y_n`/`y_i`; the frame's "d(X)δ_i > 0" is the
   same ±1-times-discriminant product the sources use. CONFIRMED.
6. **The training objective of the whole block ("Minimize the Error using Gradient Descent
   with step η", slide 037) is the sources' gradient descent on the perceptron criterion.**
   CONFIRMED: Friedman's loop "Randomly instantiate β̂ / Until convergence or some stopping
   rule is reached / For n ∈ {1, …, N}: `ŷ_n = f(β̂ᵀx_n)` / If `y_n ŷ_n = −1`,
   `β̂ ← β̂ + η·y_n x_n`"; Cornell's update "`w` becomes `w + yx`"; CS229's
   "`θj := θj + α (y(i) − hθ(x(i))) xj`". CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- **The class-label sign convention is course-authored.** The frame assigns `d(X) > 0 ⇒ class
  I` and `d(X) < 0 ⇒ class II` and then `δ_i = −1` for a misclassified class-I point and
  `δ_i = +1` for a misclassified class-II point. The sources use the mirror-image
  convention (`y ∈ {−1, +1}`, correct classification ⇔ `y(wᵀx) > 0`), which for the same
  hyperplane amounts to relabelling which side is +. Because δ_i is only ever defined here
  *for the misclassified points*, the frame's product `d(X)δ_i > 0` plays the role the
  sources give to `−y_n(wᵀx_n) > 0` in the negated criterion `L(β̂) = −Σ y_n(β̂ᵀx_n)`.
  Recorded, not fixed: **recreate the frame's lines verbatim, including its sign
  convention.**
- **The four stacked #A60000-bordered / #F7F7F7-filled boxes, the colour coding (class I in
  green #008000, Class II in blue #0000FF, d(X) in red #C00000, inequality results in blue
  #0000FF), the underlined words ("misclassified", "Error", "δ_i"), the #FFFF00 badge and
  the large red #FF0000 "X" annotation** at the right edge of the Error box are all
  course-authored presentation. No source counterpart; nothing to "fix" toward a source.
- **No numeric value, dataset, or figure is used on this frame**, so no value-by-value
  verification applies beyond the structural confirmations above.

## [?] Uncertain items

- **No web-resolvable [?] remains** — every structural claim on the frame is confirmed with
  live-fetched, verbatim quotes above.
- Frame-level [?]s that stay open by design (raw only — no final yet, so no inherited
  validation block; none web-resolvable): exact font family/point sizes (the raw gives only
  relative hierarchy), the exact position/size of the large red "X" mark (raw records only
  that it sits "at the far right" of the third box), whether the "⇒" arrows are printed glyph
  or a symbol font, the exact colors of the class-I/class-II runs, and the meaning of the red
  X (pointer/annotation artifact vs deliberate content). Resolution path = build + zoomed
  crop judge per `shared_patterns/judge_protocol_03.md`, not web research.
- **No debt records** for this slide: all four candidate URLs fetched live on the first
  attempt (HTTP 200). One *do-not-reuse* entry is nonetheless recorded for the fleet: the
  URL `https://lcnwww.epfl.ch/gerstner/PUBLICATIONS/01Lecture02Perceptron.pdf` (EPFL
  lecture-02 perceptron PDF) **failed to connect from this host** (curl exit code, 000 bytes)
  and is therefore NOT recorded as a source here; a future worker may retry it, but nothing
  was taken from it.

## Corrections

- **None applied.** No dimension, attribute, or provenance guess in `analysis/slide_036_raw.json`
  is contradicted by the sources or by the re-computation of the sign logic:
  `d(X)δ_i > 0` holds in both of the frame's branches exactly as printed (class-I branch:
  `d < 0`, `δ = −1` ⇒ product > 0; class-II branch: `d > 0`, `δ = +1` ⇒ product > 0), which is
  what the δ_i construction is for. No `analysis/*.json` was edited by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
