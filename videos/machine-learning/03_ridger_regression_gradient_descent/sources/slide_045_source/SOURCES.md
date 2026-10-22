# SOURCES.md — slide 045 "Iteration 4" (perceptron worked example, Step η = 2)

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19); the binding contract is
`~/.zcode/skills/slide-recreation/references/source-research.md` (read before this work).
Method: agy web search (MCP `agy_web_search`) for discovery + **live fetch of every recorded URL
in this same work window** (`curl -sL`, WebFetch fallback returned timeouts on this host) +
verification against the fetched page/pdf text. Frame facts come from the slide's
vision-analysis record `analysis/slide_045_raw.json` (no `_final.json` yet — research is not
dependency-gated). NO vision calls were made by this worker (no `scripts/16_vision_gate.sh`,
no vision model; no frame image viewed even locally, per the mandate's web-only rule).

## Slide identity

- Frame file: `unique_slides/slide_045.jpg` (960×540, 1px = 1pt per the deck AGENTS.md).
  Badge numeral on the frame: **45** (yellow circle; `labels` contains "45"). Deck rule:
  badge numeral = the file number N, no zero-padding.
- Numbering resolution: founder-curated set (51 files, 2026-10-19). `_meta.source_timestamps`:
  `precuration_slide = 156`, kept frame `frame_05591.jpg`, t = 5590 s,
  `provenance: "founder-curated kept frame"`, md5 snapshot
  `1407eaad7723e802e40baeec2e7b1689`. File number 045 and badge "45" agree; pre-curation
  156 is historical only (the pre-curation index was intentionally removed by the founder).
- Analysis record used: `analysis/slide_045_raw.json` — no `_final.json` exists at write time.
- Deck namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`.

## Primary source(s)

All URLs below were **fetched live in this work window (HTTP 200)**; sizes and hashes recorded.
None recorded from an unfetched snippet. Query budget: this worker spent **1** agy search (the
perceptron-PLA cluster query); every other recorded URL was reached directly from the canonical
location after that one search surfaced the cluster (no additional queries spent — ECONOMY LAW).

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html` | Cornell **CS 4780 (2018fa) Lecture 3: The Perceptron** — classifier `h(x)=sign(w^Tx+b)`; bias absorbed by the appended constant dimension; update geometry; the convergence theorem with margin and the 1/γ² mistake bound. | **CONFIRMED** — fetched live this window, HTTP 200, HTML 11,759 bytes, sha256 `016a9af244c34f3870f11f00e85996f699c723ef9ae147b8bbdec794af74011d` (local text extract quote-verified). |
| `https://deeplearning.cs.cmu.edu/S26/documents/readings/Perceptron_Learning_Algorithm_and_Convergence.pdf` | CMU reading **"The Perceptron Learning Algorithm and its Convergence"** (Shivaram Kalyanakrishnan, 2017; based on a note by Michael Collins) — the canonical PLA pseudocode with the `y_i(w_k·x_i) ≤ 0` loop condition, Theorem 3 (R²/γ² updates), the sign(0)-convention discussion, Rosenblatt citation [2]. | **CONFIRMED** — fetched live this window, HTTP 200, PDF 193,758 bytes, sha256 `de8b549f66d9f9c9627826628ec0bba0b7e4cb6595651698576be6c228605688`. pdftotext-extracted; quotes below. |
| `https://en.wikipedia.org/wiki/Perceptron` | Wikipedia **"Perceptron"** — §4 "Learning algorithm for a single-layer perceptron": update `w_i(t+1) = w_i(t) + r·(d_j − y_j(t))·x_{j,i}`, `x_{j,0} = 1` augmentation, learning rate `r`, "weights remain unchanged whenever d_j = y_j(t)", and the linearly-separable convergence statement + Rosenblatt (1958) reference. | **CONFIRMED** — fetched live this window, HTTP 200, HTML 511,237 bytes, sha256 `ab8b324c8e78c181f50078b5ed0fa7886e5380f9e434f1367491dec38fafa9a3`. **No new query spent** (canonical URL reached directly). |
| `https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf` | UPenn **CIS 5190 "Linear Classification: The Perceptron"** (Eaton/Rai lecture deck) — `h(x)=sign(w^Tx)`, "If x(i) is misclassified, do w ← w + y(i)x(i)", the online/batch pseudocode with the `y(i)x(i)ᵀw ≤ 0 // prediction is incorrect` branch, and the α-scaling remark. | **CONFIRMED** — fetched live this window, HTTP 200, PDF 3,126,847 bytes, sha256 `a045390ab90326904197323e7bf26d5d4e09df6eefb04af713549906793489e4`. Text layer quote-verified via pdftotext. **No new query spent.** |
| `https://www.geeksforgeeks.org/deep-learning/perceptron-convergence-theorem-in-neural-networks/` | GeeksforGeeks **"Perceptron Convergence Theorem in Neural Networks"** — the C1/C2-classified update rule verbatim ("if a sample is correctly classified, no update is made: w(n+1) = w(n) … w(n+1) = w(n) + ηx(n), if w^T(n)x(n) ≤ 0 and x(n) ∈ C1"), the linearly-separable convergence statement, and the `z = w^T x + b` procedure. | **CONFIRMED** — fetched live this window, HTTP 200, HTML 321,706 bytes, sha256 `b6acf2e8fbde41aaaffb2143b44a621166fdccc7d6b820e2363612db7a663e7d`. **No new query spent.** |

Origin-level cross-references (sibling banked records, no re-fetch by this worker):
- `sources/slide_037_source/SOURCES.md` + banked `DHS_liniar_disc_intro_perceptron.pdf`
  (Duda, Hart & Stork, *Pattern Classification* 2nd ed., Ch. 5, md5
  `47235972a70be5152744c50b8a64f77d`) — the fixed-increment batch/single-sample perceptron rules
  and Algorithm 4; the δ_i definition. Origin-level CONFIRMED.
- `sources/slide_039_source/SOURCES.md` — the course's `W^(updated) = W^(old) − η δ_i X_i`
  single-sample update and the "Repeat for ALL misclassified Samples" loop, confirmed against
  DHS + Wikipedia. Origin-level CONFIRMED.
- Sibling records for the worked-example start slides 041–044 were still in progress at write
  time (dirs exist, records pending); this record therefore rests on the freshly fetched
  canonical sources above, and the orchestrator may add the origin-level cross-link when they
  land. No claim of this record depends on them.

## Figures used by this slide

**None — and correctly so.** This slide is a hand-built worked-example panel (data table,
"check classes of" matrix, legend, augmented-vectors table, red iteration badge, red-bordered
stop box, six-row calculation panel). No source-published figure is reused or redrawn; every
element is course-authored layout over course-chosen numbers. The canonical sources' own
figures (e.g. Cornell's `images/perceptron/PerceptronUpdate.png` "Illustration of a Perceptron
update", CMU's Figure 1) depict the generic algorithm and are banked for the record at
`sources/slide_048_source/` with hashes — see that record; nothing on THIS frame reuses them.
Reason stated per the layout law rather than left silent.

## What the source(s) CONFIRM

Frame facts (from `analysis/slide_045_raw.json` verbatim_text/equations): "Initial W =
[4; -2; -2]", "Step η = 2", "Check classes of [0 7 3; 0 6 2] with column labels Z₁ Z₁ Z₁",
legend "C1 positive, C2 negative, Zero is unaccepted", six calculation rows
`d(xᵢ) = [<augmented xᵢ>; -4; 0] = <scalar> ⇒ Keep same Weight W = [14; -4; 0]`, and the
terminal box "No change in W / Stop Iterations".

1. **The decision function form `d(x) = xᵀW` (dot product of the augmented sample with the
   weight vector).** The frame's brackets pair each augmented sample vector `(1, f₁, f₂)` with
   the weight components and yield a scalar — i.e. `d(x) = W^Tx` with the bias carried as the
   leading `1` component. CONFIRMED by every fetched source: Wikipedia "Linear combiner output:
   v(n) = Σ w_i(n)x_i(n) = w^T(n)x(n)" and "x_{j,0} = 1"; Cornell "we 'absorb' [the bias] into
   the feature vector w by adding one additional constant dimension … [x_i; 1]ᵀ[w; b] =
   wᵀx_i + b"; UPenn "we incorporated bias term w₀ into it by x₀ = 1"; CMU "it can easily be
   implemented by transforming the d-dimensional input into a (d+1)-dimensional one".
   CONFIRMED.
2. **The class convention "C1 positive, C2 negative" (i.e. d(x) > 0 ⇒ Class I, d(x) < 0 ⇒
   Class II).** CONFIRMED: Cornell "y_i(w^ᵀx_i) > 0 ⟺ x_i is classified correctly" with
   y ∈ {−1,+1}; UPenn "w^Tx > 0 ⟹ y = +1 / w^Tx < 0 ⟹ y = −1"; CMU "the points labeled ` must
   lie on the side of the hyperplane to which its normal points" with `↦+1, ´↦−1. The course's
   C1/C2 naming is course-authored notation (sibling slide 036/037 define it); the underlying
   sign convention is standard. CONFIRMED.
3. **"Zero is unaccepted" — a zero decision value is treated as unclassified (and, in the
   training loop, as misclassified).** This is the course's shorthand for the canonical
   *strict* inequality. CONFIRMED: Cornell requires `y_i(w^ᵀx_i) > 0` (strict) for "classified
   correctly"; CMU's loop runs "While there exists i … such that y_i(w_k·x_i) ≤ 0" (zero
   included) and explicitly discusses the ambiguity: "the Perceptron's predictions for these
   points would depend on whether we assign sign(0) to be 0 or 1—which seems an arbitrary
   choice"; UPenn's online algorithm marks "if y(i)x(i)ᵀw ≤ 0 // prediction is incorrect"
   (a zero score fires the update). CONFIRMED as standard treatment.
4. **The update-on-misclassification rule W ← W + η·x (equivalently W + y·x, y = ±1).** The
   frame's worked example continues this rule (its "Update Weight"/"Keep same Weight" phrasing).
   CONFIRMED: Wikipedia "w_i(t+1) = w_i(t) + r·(d_j − y_j(t))·x_{j,i}, … r is the learning
   rate"; UPenn "The perceptron uses the following update rule … Perceptron update rule: If
   x(i) is misclassified, do w ← w + y(i)x(i)" and "Can eliminate α … since its only effect is
   to scale w by a constant, which doesn't affect performance" (α/η as pure scaling); CMU
   pseudocode "w_{k+1} ← w_k + y_j x_j"; GfG verbatim: "if w^T(n)x(n) ≤ 0 and x(n) ∈ C1.
   w(n+1) = w(n) + ηx(n)" — the course's exact case. CONFIRMED.
5. **"Keep same Weight" when the point is correctly classified.** CONFIRMED: Wikipedia "the
   weights remain unchanged whenever d_j = y_j(t)"; GfG "If a sample is correctly classified,
   no update is made: w(n+1) = w(n)"; UPenn "If the prediction matches the label, make no
   change". CONFIRMED.
6. **"No change in W ⇒ Stop Iterations" — one full pass with zero updates terminates the
   algorithm.** CONFIRMED: CMU's loop is "While there exists i such that y_i(w_k·x_i) ≤ 0 …
   Return w_k" (exit exactly when no misclassified point remains); Wikipedia "If the training
   set is linearly separable, then the perceptron is guaranteed to converge after making
   finitely many mistakes"; Cornell "If a data set is linearly separable, the Perceptron will
   find a separating hyperplane in a finite number of updates." The course's stop condition is
   the canonical termination condition. CONFIRMED.
7. **The step size η (frame prints "Step η = 2") is the standard learning rate.** CONFIRMED:
   Wikipedia "r is the learning rate of the perceptron. Learning rate is a positive number
   usually chosen to be less than 1"; UPenn's α is "eliminated … since its only effect is to
   scale w by a constant, which doesn't affect performance". The course's choice η = 2 exceeds
   the "usually < 1" convention — a course-authored example parameter, recorded, not corrected
   (see below). CONFIRMED as a valid hyperparameter; its value is course-authored.
8. **Worked-example arithmetic (source-side recomputation — the source wins for
   understanding).** With augmented samples x₁=[1;1;1], x₂=[1;2;1], x₃=[1;1;2] (Class I/C₁) and
   x₄=[1;5;4], x₅=[1;6;5], x₆=[1;6;6] (Class II/C₂) and the canonical rule, the η = 2 run from
   W₀=[4;−2;−2] reaches **exactly the frame's final W = [14; −4; 0] after 3 updating passes**,
   and pass 4 makes no update (all six d(xᵢ) correctly signed: +10, +6, +10, −6, −10, −10 with
   C₁ positive & C₂ negative) — reproducing the frame's terminal state "No change in W / Stop
   Iterations" at "Iteration 4". CONFIRMED (canonical algorithm reproduces the frame's
   trajectory and endpoint).

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- **The specific dataset** — the six 2-D points: Class I (C₁) = feature pairs (1,2), (2,1),
  (1,1); Class II (C₂) = (5,4), (6,5), (6,6) (consistent with the augmented matrices and
  scatter plots on sibling frames 046/048/049/050/051), the initial W=[4;−2;−2], and Step η = 2.
  This is the lecture's own worked example — no textbook uses it.
- **The "Check classes of" Z₁ Z₁ Z₁ precomputation panel** (rows (0 7 3)/(0 6 2)) and the
  legend phrasing "C1 positive, C2 negative, Zero is unaccepted" — course-authored pedagogy
  framing (the underlying ≤0/misclassified and sign(0) conventions are standard, §items 3–4).
- **The bracket notation d(xᵢ) = [<xᵢ row>; <W₂ W₃ row>] = scalar** — the frame interleaves the
  sample vector and the trailing weight components in one tall bracket. Course-authored display
  convention; the mathematics is the standard dot product.
- **Color coding** (red C₁/Step η/badge, blue C₂/headers, yellow number circle, gray rule
  lines) and the panel/badge geometry: deck chrome per the deck's house template. No web
  counterpart.
- **"Ugmented Vectors (from Top)"** (sic — truncated spelling preserved across the deck):
  frame text, kept verbatim (corrections patch annotations only, never transcribed text).

## [?] Uncertain items

- **Slide 045's printed scalar results `d(x₂) = -4` and `d(x₆) = -112`** do not match the
  canonical recomputation with W=[14;−4;0]: d(x₂) = (1,2,1)·(14,−4,0) = **+6** and
  d(x₆) = (1,6,6)·(14,−4,0) = **−10**. The other four rows (+10, +10, −6, −10) recompute
  exactly, and all six rows carry the same action ("Keep same Weight"), so the algorithm
  reads consistently; the two outliers look like on-slide/video transcription artifacts
  (e.g. "-112" plausibly "-10" with bracket glyphs merged; "-4" plausibly a sign/merge
  artifact). Resolution path: pixel-verify the two cells against `unique_slides/slide_045.jpg`
  at build time (builder-side; not a vision call by this worker). **The frame wins for
  recreation — the build prints the frame's values as written; the canonical values above are
  recorded for understanding only.**
- **Slide 045's top table carries a third data row (1)(1)(1)(4)(5)(6)** and the augmented
  table four rows, where the sibling frames (046/048/049/051) consistently show a bias row of
  all ones plus two feature rows. Cross-slide comparison (frame-level fact from the analysis
  records, no vision call) suggests the extra row is a vision misread of the duplicated row
  seen on slide 049; recorded as a frame-level uncertainty, resolution path = build-time pixel
  check. Not web-resolvable.
- Font sizes, exact panel geometry, stroke weights: frame-only measurements, not web facts.

## Corrections

**None applied.** No dimension annotation, attribute guess, or provenance guess in
`analysis/slide_045_raw.json` is contradicted by the fetched sources. The analysis record's
model annotations (region descriptions, color readings, the bracket-notation description)
stand as measured. Per the corrections clause, this worker made **no edit** to
`analysis/slide_045_raw.json` (or any analysis JSON); the annotations-vs-source check produced
no patch. The two printed-scalar anomalies above are transcribed frame text — NOT patchable —
and are recorded under [?] instead.

## Law reminder

The frame wins for recreation; the source wins for understanding.
