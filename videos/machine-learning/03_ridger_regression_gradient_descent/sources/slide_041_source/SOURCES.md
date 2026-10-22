# SOURCES.md — slide 041 "Training of Linear Regression Model using SGD — Solved Example (setup)"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search + live `curl -sL` fetch of every recorded URL in the same work window that records it +
verification against the fetched page text. **This slide spent 0 new search queries**: every
claim it makes is an instance of the perceptron/SGD mechanics already covered by the cluster's
fetched sources (cross-referenced below; ECONOMY LAW honored). Worker query disclosure:
`sources/slide_038_source/SOURCES.md` (3 searches for slides 037–044). Frame facts come from
`analysis/slide_041_raw.json`; NO vision calls were made by this worker.

## Slide identity

- Frame file: `unique_slides/slide_041.jpg` (960×540, 1px = 1pt per the deck AGENTS.md).
- Badge number on the frame: **41** (yellow circle, black numeral; `labels` include "41").
- Numbering resolution: founder-curated set (51 files). Recovered pre-curation provenance in
  `_meta`: `source_timestamps.precuration_slide = 140`, kept frame `frame_04894.jpg`,
  t = 4893 s, `provenance: "founder-curated 2026-10-19 (frame swap from group)"` — note this
  slide's kept frame came from a dedup-group swap, which is a second reason the frame (not any
  banked record) is ground truth for its content. Current file number 041 and badge "41"
  agree; pre-curation 140 is historical only.
- Analysis record used: `analysis/slide_041_raw.json` (no `_final.json` yet).

## Primary source(s)

All URLs were fetched live in this work window (HTTP 200); hashes below. None recorded from an
unfetched snippet. All are origin-level carry-overs of the slides 037/039 fetches — no new
query spent on this slide.

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html` | Cornell CS 4780 **"Lecture 3: The Perceptron"** — the two-category sign classifier, the ±1 labels, the bias-absorption augmentation, and the correctness criterion. | **CONFIRMED (origin-level)** — fetched live this window, 11,759 bytes, md5 `d5fa439fe07ebef324b60ede92adcd4f`; quotes banked in `sources/slide_037_source/SOURCES.md`. |
| `https://en.wikipedia.org/wiki/Perceptron` | Wikipedia **"Perceptron"** — `x_{j,0} = 1` bias convention, the per-sample update, convergence. | **CONFIRMED (origin-level)** — fetched live this window, 51,936 bytes wikitext, md5 `4bf47c89c5e97c46cbb0215a59cb9052`; quotes banked in `sources/slide_037_source/SOURCES.md`. |
| `https://www.ccs.neu.edu/home/vip/teach/MLcourse/2_GD_REG_pton_NN/materials/DHS_liniar_disc_intro_perceptron.pdf` | DHS Ch. 5 teaching PDF — the two-category decision rule incl. the g(x)=0 treatment, augmented feature space, single-sample correction rule. | **CONFIRMED (origin-level)** — banked byte-identical at `sources/slide_037_source/DHS_liniar_disc_intro_perceptron.pdf` (md5 `47235972a70be5152744c50b8a64f77d`), fetched live this window. |
| `https://en.wikipedia.org/wiki/Stochastic_gradient_descent` | Wikipedia **"Stochastic gradient descent"** — learning rate and per-sample update context. | **CONFIRMED (origin-level)** — fetched live this window, 58,106 bytes wikitext, md5 `a0179f74b0046c7c9a1e65d9de51c7d3`; quotes banked in `sources/slide_039_source/SOURCES.md`. |

## Figures used by this slide

**None — and correctly so, with one caveat recorded.** The slide's scatter plot (blue squares,
red triangles, magenta diamonds on a gray-grid white plot with a red border) is the course's
own visualization of its worked example — no hosted source figure matches it, and none is
reused or redrawn. The nearest concept-figures in the sources are DHS Figure 5.13 ("Samples
from two categories, ω₁ (black) and ω₂ (red) are shown in augmented feature space, along with
an augmented weight vector a.") and Wikipedia's `Perceptron_example.svg` ("A diagram showing a
perceptron updating its linear boundary as more training examples are added") — neither is
this slide's plot (different data, markers, and geometry), so nothing was downloaded; the
reason is stated per the layout law. The DHS/Wikipedia figures are concept-level background
only.

## What the source(s) CONFIRM

1. **The data-matrix-with-class-row setup** (input vectors x₁…x₆ as matrix columns, a class
   row C₁/C₂ underneath): the standard supervised two-category formulation. Cornell CS 4780,
   verbatim: "Binary classification (i.e. y_i ∈ {−1, +1})"; DHS §5.2.1: "A two-category linear
   classifier implements the following decision rule: Decide ω₁ if g(x) > 0 and ω₂ if g(x) < 0."
   CONFIRMED at the setup level.
2. **"C₁ positive C₂ negative"** — the class-to-side mapping of the discriminant d(X) = W^T X
   (C₁ = positive side, C₂ = negative side). This is exactly DHS's decision rule quoted above
   (ω₁ on the positive side, ω₂ on the negative side). CONFIRMED.
3. **"Zero is unaccepted"** (a discriminant value d(X) = 0 is not a valid class assignment —
   the example treats it as a mistake and updates). Two confirmations: (a) Cornell CS 4780's
   correctness criterion is a STRICT inequality — verbatim: "y_i(w^T x_i) > 0 ⟺ x_i is
   classified correctly" — so y_i(w^T x_i) = 0 fails the criterion and the perceptron update
   fires; (b) DHS §5.2.1, verbatim: "If g(x) = 0, x can ordinarily be assigned to either
   class, but in this chapter we shall leave the assignment undefined." The slide's "unaccepted"
   is the course's phrasing of exactly this boundary case. CONFIRMED — and this is why the
   worked example updates the weight on d(x₁) = 0 (slide 042, row 1).
4. **Augmented-vector mechanics** (the example's vectors carry a constant 1 component so the
   bias rides inside W): Wikipedia, verbatim: "x_{j,0} = 1 ... Because x_{j,0} = 1, the w_0 is
   effectively a bias that we use instead of the bias constant b"; Cornell: "we 'absorb' it
   into the feature vector w by adding one additional constant dimension". CONFIRMED — the
   slides 041–044 "from Top"/"Augmented Vectors" tables (a top row of 1s prepended) are this
   convention.
5. **"Step η = 2" as a positive learning rate** — Wikipedia, verbatim: "r is the learning rate
   of the perceptron. Learning rate is a positive number usually chosen to be less than 1. The
   larger the value, the greater the chance for volatility in the weight changes." η = 2 is
   positive (valid) but larger than the "usually less than 1" convention; the sources'
   volatility caveat applies as an understanding-level note. The course's choice stands
   (frame wins); the example's arithmetic is internally consistent with η = 2 throughout
   slides 042–044. CONFIRMED as a valid choice; the deviation from the usual < 1 is recorded,
   not corrected.
6. **"Initial W = (4, −2, −2)^T"** (a specific starting weight vector) — Wikipedia's
   algorithm: "Initialize the weights. Weights may be initialized to 0 or to a small random
   value." The course's nonzero start is a course-authored choice for the worked example; the
   mechanics (it is just the initial a(0)/w(0) of the update rules) are standard. CONFIRMED at
   the mechanics level.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- **All the worked example's data**: the exact matrix entries, the class row, the initial W
  values, η = 2, the "Check classes of" Z-matrix, and every computed number — there is no
  hosted source for this instructor-authored example. Recorded so no builder substitutes a
  "textbook" dataset.
- The scatter plot's construction (marker shapes/colors, grid, red-bordered white plot area,
  marker placement) — course-authored visualization of the example's data.
- The pale-yellow/blue-bordered header panel, the legend colors (C₁/C₂/Zero color coding),
  the badge, and the mouse-pointer artifacts — course chrome / recording artifacts.

## [?] Uncertain items

| # | Item | Resolution path |
|---|---|---|
| 1 | The transcribed matrix vs. the plotted points do not obviously correspond (the raw records 5 matrix columns x₁x₂x₄x₅x₆ but 9 plotted markers at 4 distinct styles) — a transcription-level ambiguity, not a source question | frame-level re-measurement (build-time zoom judge per the deck's mandate); the vision transcript is the current truth for recreation and is NOT patched |
| 2 | Exact meaning/derivation of the "Check classes of [Z₁ Z₁ Z₁; (0)(7)(3); (0)(6)(2)]" matrix as transcribed (its columns are labeled Z₁ three times) | frame-level re-measurement; arithmetic re-derivation is the builder's job from the frame |
| 3 | Whether Initial W is [4;−2;−2] (3D, as this slide's transcription shows) or the 2D [4;−2] seen on slides 042–044 (slide 042's raw shows `\begin{pmatrix}4\\-2\end{pmatrix}`) — an internally inconsistent transcription across frames | frame-level re-measurement of each frame; no source resolution exists (course-authored values) |
| 4 | Marker-color → class mapping on the plot (blue squares vs red triangles vs magenta diamonds) | frame-level re-measurement (no hosted counterpart) |

## Corrections

**None.** No dimension annotation, attribute guess, or provenance guess in
`analysis/slide_041_raw.json` is contradicted by the fetched sources; transcribed frame text
stays verbatim. No edit to `analysis/*.json` was made by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
