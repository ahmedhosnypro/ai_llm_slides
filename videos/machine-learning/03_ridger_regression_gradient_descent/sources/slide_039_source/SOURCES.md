# SOURCES.md — slide 039 "Gradient Descent (GD) – Stochastic Gradient Descent SGD) and Mini-Batch Gradient Descent"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search + live `curl -sL` fetch of every recorded URL in the same work window that records it +
verification against the fetched page text. **This slide spent 0 new search queries**: all of
its claims are covered by the cluster's shared primary sources (fetched live in this window
for slides 037/038), cross-referenced below per the ECONOMY LAW. Query-budget disclosure for
this worker lives in `sources/slide_038_source/SOURCES.md` (3 searches total for 037–044).
Frame facts come from the slide's vision-analysis record `analysis/slide_039_raw.json`; NO
vision calls were made by this worker (no `scripts/16_vision_gate.sh`, no vision model).

## Slide identity

- Frame file: `unique_slides/slide_039.jpg` (960×540, 1px = 1pt per the deck AGENTS.md).
- Badge number on the frame: **39** (yellow rounded badge, black numeral; `labels` include
  "39"). Deck rule: badge numeral = the file number N, no zero-padding.
- Numbering resolution: founder-curated set (51 files). Recovered pre-curation provenance in
  `_meta`: `source_timestamps.precuration_slide = 134`, kept frame `frame_04722.jpg`,
  t = 4721 s, `provenance: "founder-curated kept frame"`. Current file number 039 and badge
  "39" agree; pre-curation 134 is historical only.
- Analysis record used: `analysis/slide_039_raw.json` (no `_final.json` yet; research is not
  dependency-gated).

## Primary source(s)

All URLs were fetched live in this work window (HTTP 200); hashes recorded inline. None
recorded from an unfetched snippet. The two Wikipedia/CS231n/sklearn URLs were fetched
directly from their canonical locations (no search spent) after the cluster's searches
surfaced the topic cluster.

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Stochastic_gradient_descent` | Wikipedia **"Stochastic gradient descent"** — the single-sample update `w := w − η ∇Q_i(w)`, the "sweeps through the training set" loop, the mini-batch compromise, and the mini-batch-vs-SGD relationship. | **CONFIRMED** — fetched live this window, `action=raw` wikitext 58,106 bytes, md5 `a0179f74b0046c7c9a1e65d9de51c7d3`. Quotes below. |
| `https://cs231n.github.io/optimization-1/` | Stanford **CS231n** optimization notes — vanilla GD / mini-batch GD / SGD trichotomy with pseudocode. | **CONFIRMED** — fetched live this window, 47,579 bytes, md5 `cfad649b103495ddcc77732c07930767`. Quotes below. |
| `https://scikit-learn.org/stable/modules/sgd.html` | scikit-learn **"1.5. Stochastic Gradient Descent"** — GD vs SGD distinction, per-example iteration, and the efficiency claim. | **CONFIRMED** — fetched live this window, 96,457 bytes, md5 `f7b236d97a732d6bce3b51d7d4e64128`. Quotes below. |
| `https://www.ccs.neu.edu/home/vip/teach/MLcourse/2_GD_REG_pton_NN/materials/DHS_liniar_disc_intro_perceptron.pdf` | Duda, Hart & Stork Ch. 5 teaching PDF (banked at `sources/slide_037_source/`) — the batch vs single-sample perceptron correction rules and the misclassified-set loop. | **CONFIRMED (origin-level)** — fetched live this window and banked byte-identical at `sources/slide_037_source/DHS_liniar_disc_intro_perceptron.pdf` (md5 `47235972a70be5152744c50b8a64f77d`). **No new query spent.** |
| `https://en.wikipedia.org/wiki/Perceptron` | Wikipedia **"Perceptron"** — single-sample update mechanics. | **CONFIRMED (origin-level)** — fetched live this window; quotes banked in `sources/slide_037_source/SOURCES.md`. **No new query spent.** |

## Figures used by this slide

**None — and correctly so.** The frame is a bullet/equation slide with a green-bordered
equation callout; `imagery` holds only the badge and the (recording-artifact) mouse pointer.
No source figure is reused or redrawn; the slide's green callout box and blue arrow bullets
are course-authored styling. Notable exception check: the deck's worked example on this slide
(`W^(updated)=W^old − η δ_i X_i`) is a course-authored computation continuing the lecture's own
example — not a copy of any hosted figure. Reason stated per the layout law.

## What the source(s) CONFIRM

1. **"Stochastic Gradient Descent (SGD) is a variant of GD which computes the gradient of the
   Error function with respect to a single training example"** — scikit-learn, verbatim:
   > "In contrast to (batch) gradient descent, SGD approximates the true gradient of E(w,b) by
   > considering a single training example at a time."

   Wikipedia, verbatim (the update itself):
   > "In stochastic (or 'on-line') gradient descent, the true gradient of Q(w) is approximated
   > by a gradient at a single sample: w := w − η ∇Q_i(w)."

   CONFIRMED — the slide's sentence is the standard definition almost word for word.
2. **"In other words, it updates the weights using one training sample at a time"** —
   Wikipedia, verbatim:
   > "As the algorithm sweeps through the training set, it performs the above update for each
   > training sample."

   scikit-learn, verbatim:
   > "The algorithm iterates over the training examples and for each example updates the model
   > parameters according to the update rule given by ..."

   CONFIRMED.
3. **"Remember: GD updated the weight vector after passing through ALL training samples"** —
   Wikipedia, verbatim:
   > "... it replaces the actual gradient (calculated from the entire data set) by an estimate
   > thereof ..."

   and cs231n's vanilla-GD pseudocode evaluates `evaluate_gradient(loss_fun, data, weights)`
   over the whole `data`. CONFIRMED — GD = full-batch (the slide's "ALL training samples").
4. **"SGD is usually more efficient than GD"** — scikit-learn, verbatim:
   > "The major advantage of SGD is its efficiency, which is basically linear in the number of
   > training examples."

   Wikipedia, verbatim:
   > "Especially in high-dimensional optimization problems this reduces the very high
   > computational burden, achieving faster iterations in exchange for a lower convergence
   > rate."

   CONFIRMED (note the sources' honest caveat — "in exchange for a lower convergence rate" —
   which does not contradict the slide's comparative claim about per-iteration efficiency).
5. **"SGD converges faster than GD"** — cs231n, verbatim:
   > "... the gradient from a mini-batch is a good approximation of the gradient of the full
   > objective. Therefore, much faster convergence can be achieved in practice by evaluating
   > the mini-batch gradients to perform more frequent parameter updates."

   CONFIRMED as the standard practical claim (the slide's wording "usually"/"faster" matches
   the sources' "in practice" framing). The deck teaches the perceptron progressively with
   single-sample updates, consistent with DHS's Algorithm 4 fixed-increment single-sample rule.
6. **The equation "W^(updated)=W^old − η δ_i X_i" (single-sample update, with the course's
   δ_i)** — the single-sample special case of the slide-037 rule: Wikipedia SGD's
   `w := w − η ∇Q_i(w)`, and DHS Algorithm 4 ("the fixed-increment rule", `a(k+1) = a(k) + y^k`
   with `a^T(k) y^k < 0 for all k`, OCR'd verbatim from the banked PDF). Since the deck's
   δ_i = −y_i for a misclassified sample (slide 037's record), the two are the same step.
   CONFIRMED.
7. **"Repeat for ALL misclassified Samples"** — the loop-until-correct structure: DHS
   Algorithm 4 terminates only "until all patterns properly classified", and its convergence
   proof requires the samples be revisited ("as long as every sample appears in the sequence
   infinitely often"); Illinois CS 440's epochs discussion matches. Wikipedia (*Perceptron*):
   "The algorithm updates the weights after every training sample in step 2b, though one may
   note that the weights remain unchanged whenever d_j = y_j(t)." CONFIRMED.
8. **"Batch GD is a generalization of GD and SGD where weights are updated after passing
   through 'Mini-Batch' of training samples with size n" / "If n=N (it is GD), and if n=1 (it
   is SGD)"** — the standard trichotomy, confirmed endpoint-to-middle: cs231n vanilla GD =
   gradient over the full `data`; "A very common approach ... is to compute the gradient over
   batches of the training data" (mini-batch); "The extreme case of this is a setting where the
   mini-batch contains only a single example. This process is called Stochastic Gradient
   Descent (SGD) ..." Wikipedia: "A compromise between computing the true gradient and the
   gradient at a single sample is to compute the gradient against more than one training sample
   (called a 'mini-batch') at each step." The slide's n=N → GD / n=1 → SGD conditional is the
   same statement in the course's own notation. CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- **The δ_i notation in the update equation** (canonical sources write ±1 class labels y_i or
  normalized samples; the course carries its sign-suffix δ_i from slide 037).
- The title's exact transcription, preserved verbatim including its unbalanced parenthesis
  ("Stochastic Gradient Descent SGD)" — a frame-text typo; recreation keeps it as printed).
- The green-bordered equation callout, the red annotation "Repeat for ALL misclassified
  Samples", the "Why using SGD" subheading, the blue arrow bullets, the red/blue two-line
  title split, and the mouse-pointer artifact (retained for frame fidelity only).
- The slide's "Zero is unaccepted" note on the NEXT slides is course shorthand for d(X)=0
  being treated as unclassifiable; see slide 041's record for the source treatment
  (DHS leaves g(x)=0 "undefined"; the perceptron update fires on y w^T x ≤ 0).

## [?] Uncertain items

- None web-resolvable and none open from the sources. The frame-local font sizes (serif
  ~20–24 pt body, ~32–36 pt title) and exact panel geometry remain frame-only measurements,
  carried as `[?]` into the build's uncertain list per the mandate; they are not web facts and
  are not listed as source uncertainties.

## Corrections

**None.** No dimension annotation, attribute guess, or provenance guess in
`analysis/slide_039_raw.json` is contradicted by the fetched sources; transcribed frame text
stays verbatim. No edit to `analysis/*.json` was made by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
