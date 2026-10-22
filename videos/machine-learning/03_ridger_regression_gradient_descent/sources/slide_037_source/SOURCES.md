# SOURCES.md — slide 037 "Problem Formulation"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web search
(MCP `agy_web_search` ×2 + agy CLI `agy -p` ×1, see query-budget note) for discovery + live
`curl -sL` fetch of every recorded URL in the same work window that records it + verification
against the fetched text (the Duda-Hart-Stork lecture PDF is a scanned image PDF, so its pages
were rendered at 200 dpi and OCR'd with tesseract locally to extract the verbatim quotes below;
the original PDF bytes are banked unmodified). Frame facts come from the slide's
vision-analysis record `analysis/slide_037_raw.json`; NO vision calls were made by this worker
(no `scripts/16_vision_gate.sh`, no vision model). Query budget: 3 searches total for this
worker's whole 037–044 range (see slide 038's record for the disclosure); slide 037 itself
spent 2 of them (both perceptron-criterion searches).

## Slide identity

- Frame file: `unique_slides/slide_037.jpg` (960×540, 1px = 1pt per the deck AGENTS.md).
- Badge number on the frame: **37** (yellow circle, black numeral; `labels` in the raw record
  include "37"). Deck rule (AGENTS.md, "House chrome — THIS deck"): badge numeral = the file
  number N, no zero-padding.
- Numbering resolution: 51 founder-curated files numbered by the founder 2026-10-19. This
  slide carries recovered pre-curation provenance in the analysis `_meta`:
  `source_timestamps.precuration_slide = 132`, kept frame `frame_04686.jpg`, t = 4685 s,
  `provenance: "founder-curated kept frame"`. Current file number 037 and badge "37" agree;
  pre-curation 132 is historical provenance only and must not be used for the badge.
- Analysis record used: `analysis/slide_037_raw.json` (no `_final.json` exists yet; research
  does not wait on validation — mandate law).

## Primary source(s)

All five URLs were fetched live in this work window (HTTP 200). None was recorded from an
unfetched search snippet.

1. **https://www.ccs.neu.edu/home/vip/teach/MLcourse/2_GD_REG_pton_NN/materials/DHS_liniar_disc_intro_perceptron.pdf**
   — Virgil Pavlu's teaching PDF reproducing **Duda, Hart & Stork, *Pattern Classification*
   (2nd ed.), Chapter 5** (§5.2 linear discriminants, §5.5 "Minimizing the Perceptron
   Criterion Function", incl. Algorithms 1–4 and Theorem 5.1). 2,229,117 bytes, 12 pages,
   scanned image PDF (Creator: Mac OS X Quartz). md5 `47235972a70be5152744c50b8a64f77d`,
   sha256 `7e134dfb51cfc75ef2410239362d373d0e26d4a11a55edb1817c0b4586a2879e`. Downloaded and
   banked as-served (never renamed) in this directory as `DHS_liniar_disc_intro_perceptron.pdf`;
   the OCR working copy `DHS_liniar_disc_intro_perceptron_OCR.txt` (tesseract, 200 dpi pages)
   is a derived file kept for the quote trail. **This is the source of record for the slide's
   Error-function formulation** — slides 039 and 041–044 cross-reference this same banked copy
   (no re-download; byte-identical by hash).
2. **https://courses.grainger.illinois.edu/cs440/fa2019/Lectures/lect26.html** — UIUC CS 440/ECE
   448 (Margaret Fleck), **"Lecture 26: Linear Classifiers 2"** — the perceptron learning rule,
   epochs, and convergence conditions. 10,582 bytes, md5 `e5422bc0791ac0bf26d932e08bad6ee5`.
3. **https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html** — Cornell
   CS 4780 (Kilian Weinberger et al.), **"Lecture 3: The Perceptron"** — sign() classifier,
   bias absorption into the augmented vector, the correctness criterion
   `y_i(w^T x_i) > 0 ⟺ classified correctly`, and the Novikoff/Cover-style convergence
   argument. 11,759 bytes, md5 `d5fa439fe07ebef324b60ede92adcd4f`.
4. **https://en.wikipedia.org/w/index.php?title=Perceptron&action=raw** — Wikipedia
   **"Perceptron"** (algorithm section + convergence theorem section), wikitext as served,
   51,936 bytes, md5 `4bf47c89c5e97c46cbb0215a59cb9052`. Also fetched as rendered HTML
   (`en.wikipedia.org/wiki/Perceptron`) in the same window.
5. **https://en.wikipedia.org/w/index.php?title=Gradient_descent&action=raw** — Wikipedia
   **"Gradient descent"** (definitional lead), wikitext as served, 40,753 bytes, md5
   `7ccec322feaf8d35ed83b689bc2ab29a`.

## Figures used by this slide

**None — and correctly so.** The frame is a text-only slide: the analysis record's
`visual_elements` holds only highlight-boxes and the badge; `imagery` lists only the badge.
No source figure is reused or redrawn. For provenance awareness the DHS source does host
original figures — **its Figure 5.11** ("Four learning criteria as a function of weights in a
linear classifier. At the upper left is the total number of patterns misclassified, which is
piecewise constant and hence unacceptable for gradient descent procedures. At the upper right
is the Perceptron criterion (Eq. 16), which is piecewise linear and acceptable for gradient
descent."), Figure 5.12 (the criterion plotted in weight space with the batch-update
trajectory) and Figure 5.13 (samples in augmented feature space with a fixed-increment
correction sequence) — but slide 037 shows none of them; they are concept-level background
only. Per the layout law the reason is stated here rather than left silent. The banked PDF
pages are reference-grade ground truth for the criterion's shape (4-panel learning-criteria
family) should any later slide need them.

## What the source(s) CONFIRM

1. **"Redefine Error function as: Error = Σ_{all misclassified vectors (i)} δ_i W^T X_i" and
   "Summation is always positive".** The canonical perceptron criterion function of DHS §5.5.1
   is exactly this sum (DHS book, Eq. 16, quoted verbatim from the fetched/OCR'd PDF):
   > "Consider now the problem of constructing a criterion function for solving the linear
   > inequalities a^T y_i > 0. The most obvious choice is to let J(a; y_1,...,y_n) be the number
   > of samples misclassified by a. However, because this function is piecewise constant, it is
   > obviously a poor candidate for a gradient search. A better choice is the Perceptron
   > criterion function
   > J_p(a) = Σ_{y∈Y} (−a^T y), (16)"

   Written in the slide's notation the terms coincide: for a misclassified vector the slide's
   δ_i equals the sign of d(X) = W^T X_i (the slide itself says "δ_i has the same sign" as
   (W^T X_i)), hence δ_i W^T X_i = |W^T X_i| = −(W^T X_i) for that term — identical to each
   term of J_p, and therefore **always ≥ 0 ("Summation is always positive")**. CONFIRMED.
2. **"Minimize the Error using Gradient Descent with step η" / "W^(updated) = W^(old) − η
   ∂Error/∂W".** DHS §5.5 is literally titled *"Minimizing the Perceptron Criterion Function"*
   and its Algorithm 1 is "Basic gradient descent" (`a ← a − η(k) ∇J(a)`); the section text
   explains why the criterion must be differentiable-friendly: the misclassified-count error is
   "a poor candidate for a gradient search", whereas the perceptron criterion is "piecewise
   linear and acceptable for gradient descent" (verbatim, Figure 5.11 caption). The update
   form W_new = W_old − η ∂Error/∂W is the standard descent step; Wikipedia (*Gradient
   descent*): "The idea is to take repeated steps in the opposite direction of the gradient
   ... because this is the direction of steepest descent." CONFIRMED.
3. **"∂Error/∂W = Σ_{misclassified vectors} δ_i X_i" and the final rule "W^(updated) =
   W^(old) − η Σ_{misclassified vectors ONLY (i)} δ_i X_i".** DHS states the batch form
   verbatim:
   > "Thus, the batch Perceptron algorithm for finding a solution vector can be stated very
   > simply: the next weight vector is obtained by adding some multiple of the sum of the
   > misclassified samples to the present weight vector."

   Since for every misclassified sample δ_i = −y_i (y_i = the desired ±1 class sign), the
   slide's `W − η Σ δ_i X_i` is algebraically the same step as DHS's `W + η Σ y_i X_i` and the
   canonical rule; Illinois CS 440 gives the canonical rule verbatim:
   > "If y' = y, do nothing. Otherwise w_i = w_i + α * y * x_i"

   and Wikipedia (*Perceptron*, algorithm step 2b) gives the equivalent
   > "w_i(t+1) = w_i(t) + r·(d_j − y_j(t)) x_{j,i}, for all features 0 ≤ i ≤ n"

   CONFIRMED — the slide's derivation is the standard perceptron rule in an equivalent
   δ_i-disguise.
4. **The two "Define δ_i as:" implication lines ("d(X) will be <0 ⇒ δ_i = −1 ⇒ d(X)δ_i > 0" /
   "d(X) will be >0 ⇒ δ_i = +1 ⇒ d(X)δ_i > 0").** Both are the misclassification condition of
   the linear classifier, confirmed verbatim by Cornell CS 4780:
   > "y_i(w^T x_i) > 0 ⟺ x_i is classified correctly"
   > (with the classifier `h(x_i) = sign(w^T x_i + b)`)

   and by DHS §5.2's decision rule "Decide ω_1 if g(x) > 0 and ω_2 if g(x) < 0". The slide's
   d(X)δ_i > 0 products are positive precisely because the samples are misclassified (their
   true class sign is flipped relative to d(X)'s sign). CONFIRMED.
5. **Context for the coming worked examples (why "misclassified vectors ONLY" matters):**
   Wikipedia (*Perceptron*): "The algorithm updates the weights after every training sample in
   step 2b, though one may note that the weights remain unchanged whenever d_j = y_j(t)";
   Illinois: "If y' = y, do nothing." The slide's red "misclassified vectors ONLY (i)"
   subscript is exactly this restriction. CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- **The δ_i notation itself** (δ_i := the sign matching d(X), so that each misclassified term
  is positive). Canonical sources carry ±1 class labels y_i (Cornell/Wikipedia) or normalize
  samples by reflection through the origin (DHS §5.4: "If y_i ∈ ω_2, replace y_i with −y_i").
  The slide's δ_i device is a course-authored presentation of the same criterion — recorded
  here so no builder "corrects" the slide toward y_i notation.
- The phrase "Summation is always positive" (a true property of J_p, but the course's own
  emphasis) and the two implication lines' exact wording.
- The three-panel layout, the pale-yellow/tan panel fills, the red implication arrows, the
  green rounded highlight boxes on the update rules, and all deck chrome (badge, border) —
  no source counterpart.
- The slide's Error uses the plain sum; DHS/Wikipedia state the criterion per-epoch over the
  current misclassified set (equivalent); no averaging constant appears on the slide and none
  is added.

## [?] Uncertain items

- Reading of "δ_i has the same sign" — resolved **with trail**: δ_i = sign(d(X)) (i.e. of
  W^T X_i) is the only reading under which "Summation is always positive" holds, and it makes
  the slide's Error an exact instance of DHS Eq. 16 (verified algebraically above). Closed by
  this record's confirming sources; no open item remains.
- Whether the gradient of a piecewise-linear criterion needs the "locally fixed misclassified
  set" convention — resolved: DHS derives its gradient step on exactly this criterion (§5.5,
  Algorithm 1), so the slide's ∂Error/∂W = Σ δ_i X_i follows the source's treatment. Closed.
- No dimension/attribute/provenance annotation in `analysis/slide_037_raw.json` is
  source-contradicted, so nothing is carried as an open `[?]` from the analysis record.

## Corrections

**None.** No dimension annotation, attribute guess, or provenance guess in
`analysis/slide_037_raw.json` is contradicted by the fetched sources. The transcribed frame
text (equations, bullets) is recreation-verbatim and stays untouched. No edit to
`analysis/*.json` was made by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
