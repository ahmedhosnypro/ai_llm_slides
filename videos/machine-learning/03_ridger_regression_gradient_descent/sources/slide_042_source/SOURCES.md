# SOURCES.md — slide 042 "Iteration 1"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search + live `curl -sL` fetch of every recorded URL in the same work window that records it +
verification against the fetched text, plus **independent local re-derivation of the slide's
arithmetic** against the standard update rule. **This slide spent 0 new search queries**
(economy law: all claims covered by the cluster's fetched sources, cross-referenced below;
worker query disclosure in `sources/slide_038_source/SOURCES.md`). Frame facts come from
`analysis/slide_042_raw.json`; NO vision calls were made by this worker.

## Slide identity

- Frame file: `unique_slides/slide_042.jpg` (960×540, 1px = 1pt per the deck AGENTS.md).
- Badge number on the frame: **42** (yellow circle, black numeral; `labels` include "42").
- Numbering resolution: founder-curated set (51 files). Recovered pre-curation provenance in
  `_meta`: `source_timestamps.precuration_slide = 142`, kept frame `frame_04947.jpg`,
  t = 4946 s, `provenance: "founder-curated 2026-10-19 (frame swap from group)"` — the kept
  frame came from a dedup-group swap, reinforcing frame-as-truth for this content. Current
  file number 042 and badge "42" agree; pre-curation 142 is historical only.
- Analysis record used: `analysis/slide_042_raw.json` (no `_final.json` yet).

## Primary source(s)

All URLs were fetched live in this work window (HTTP 200); hashes below. None recorded from an
unfetched snippet; all are origin-level carry-overs of the slides 037/039 fetches — no new
query spent on this slide.

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Perceptron` | Wikipedia **"Perceptron"** — the per-sample update the iteration executes; "weights remain unchanged whenever d_j = y_j(t)". | **CONFIRMED (origin-level)** — fetched live this window (wikitext 51,936 bytes, md5 `4bf47c89c5e97c46cbb0215a59cb9052`); quotes banked in `sources/slide_037_source/SOURCES.md`. |
| `https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html` | Cornell CS 4780 **"Lecture 3: The Perceptron"** — correctness criterion (strict inequality), sign classifier, augmented bias vector. | **CONFIRMED (origin-level)** — fetched live this window (11,759 bytes, md5 `d5fa439fe07ebef324b60ede92adcd4f`); quotes banked in `sources/slide_037_source/SOURCES.md`. |
| `https://www.ccs.neu.edu/home/vip/teach/MLcourse/2_GD_REG_pton_NN/materials/DHS_liniar_disc_intro_perceptron.pdf` | DHS Ch. 5 teaching PDF — Algorithm 4 fixed-increment single-sample rule and its termination condition. | **CONFIRMED (origin-level)** — banked byte-identical at `sources/slide_037_source/DHS_liniar_disc_intro_perceptron.pdf` (md5 `47235972a70be5152744c50b8a64f77d`), fetched live this window. |
| `https://courses.grainger.illinois.edu/cs440/fa2019/Lectures/lect26.html` | UIUC CS 440 Lecture 26 — "If y' = y, do nothing. Otherwise w_i = w_i + α * y * x_i". | **CONFIRMED (origin-level)** — fetched live this window (10,582 bytes, md5 `e5422bc0791ac0bf26d932e08bad6ee5`); quotes banked in `sources/slide_037_source/SOURCES.md`. |

## Figures used by this slide

**None — and correctly so.** The slide is a computation stack (tables, matrices, decision rows,
badges); no source figure is reused or redrawn, and no hosted original corresponds to this
instructor-authored worked example. Reason stated per the layout law.

## What the source(s) CONFIRM

1. **The iteration's step structure — compute d(x_i), decide Update/Keep, write the new W** —
   is the canonical single-sample perceptron rule. DHS Algorithm 4 (OCR'd verbatim from the
   banked PDF): "if y_i is misclassified by a then a ← a + y_i ... until all patterns properly
   classified", with Eq. 20 "a(k+1) = a(k) + y^k ... where a^T(k) y^k < 0 for all k". Illinois
   CS 440, verbatim: "If y' = y, do nothing. Otherwise w_i = w_i + α * y * x_i". Wikipedia,
   verbatim: "The algorithm updates the weights after every training sample in step 2b, though
   one may note that the weights remain unchanged whenever d_j = y_j(t)." The slide's
   "Keep same Weight" rows are the no-op case; the "Update Weight" rows are the correction
   case. CONFIRMED.
2. **The update signs** — for a C₁ (positive-class) point that fails the test the rule adds
   η·x_i to W (slide: W=[4;−2]+2·[1;1]=[6;0]); for a C₂ (negative-class) point it subtracts
   η·x_i (slide: W=[6;0]−2·[1;5]=[4;−10]). With the ±1 label convention this is exactly the
   single rule W ← W + η·y_i·x_i (the minus sign is y₄ = −1). Cornell: classifier
   `h(x_i) = sign(w^T x_i + b)` with labels y_i ∈ {−1,+1}; the update adds yx for a negative
   margin. CONFIRMED.
3. **"d(x_i) = 0 ⇒ Update Weight" (row 1: d(x₁)=0, Zero is unaccepted)** — the strict
   correctness inequality of Cornell ("y_i(w^T x_i) > 0 ⟺ classified correctly") makes zero a
   failure; DHS §5.2.1 leaves g(x)=0 "undefined" (banked quotes, slide 041's record). The
   slide's decision on d(x₁)=0 is the standard treatment. CONFIRMED.
4. **Independent re-derivation of the transcribed arithmetic (understanding-level, not a
   patch):**
   - Reading the class row as C₁ C₁ C₁ C₂ C₂ C₂ and the leading 1's as the bias augmentation
     (Cornell/Wikipedia convention), the values d(x₂)=6, d(x₃)=6, d(x₄)=6 re-derive
     consistently: after the row-1 update the 3-D weight is [6;0;0] (the slide transcribes the
     update as the 2-D-looking "W=[4;−2]+2·[1;1]=[6;0]"), and then x₂=[1;2;1], x₃=[1;1;1],
     x₄=[1;5;1] all give 6 under W=[6;0;0]. CONFIRMED re-derivable.
   - The row-4 update W=[6;0]−2·[1;5]=[4;−10] then extends to [4;−10;−2] in 3-D
     (x₄=[1;5;1]). CONFIRMED re-derivable in structure.
   - **d(x₅) = −96 does NOT re-derive** from the transcribed state: with W=[4;−10;−2] and
     x₅=[1;6;5] the dot product is −66 (with x₅=[1;6;6] it is −68). The transcription is
     internally inconsistent here (possible vision misread of −66 as −96, or an instructor
     slip on the frame). Recorded as `[?]` #1 below with a frame re-measurement path — NOT
     patched, because the frame wins for recreation.
   - The 2-D vs 3-D weight ambiguity (slide 041 transcribes Initial W = [4;−2;−2], this slide
     transcribes [4;−2]) is also a transcription-level inconsistency; the 3-D reading makes
     d(x₁) = 4−2−2 = 0 work (the slide's own value), which is evidence for the 3-D reading at
     understanding level. Recorded as `[?]` #2; frame re-measurement decides recreation.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- **Every number in the example** — the data tables, "Upgraded Vectors (From Top)", the
  Initial W, Step η = 2, the Check-classes Z-matrix, and all five d(x_i)/W rows — is
  instructor-authored. There is no hosted counterpart for any of it; none is substituted or
  "corrected" toward a textbook.
- The red "Iteration 1" badge, the green "⇐" arrows at the far right of update rows, the
  "Update Weight"/"Keep same Weight" phrasing, the black/red color coding, the badge "42",
  and the mouse-pointer artifacts — course styling / recording artifacts.
- The decision-pedagogy order (each d(x_i) paired with its action and resulting W in one
  stacked row) is the course's presentation of the standard rule.

## [?] Uncertain items

| # | Item | Resolution path |
|---|---|---|
| 1 | d(x₅) = −96 as transcribed does not re-derive under the state implied by the preceding rows (−66/−68 expected) | frame-level re-measurement (build-time zoom judge); the transcribed value stays as recreation truth until then |
| 2 | W dimension ambiguity (2-D [4;−2] on this slide vs 3-D [4;−2;−2] on slide 041); the d(x₁)=0 value favors the 3-D reading | frame-level re-measurement of slides 041–044 |
| 3 | The garbled d(x_i) matrix forms (e.g. "d(x₁)=[1 1 1 4; −2 0]") — the transcribed bracket layout cannot be fully parsed | frame-level re-measurement; builders transcribe from the frame, not from this record |

## Corrections

**None.** The sources confirm only the algorithm mechanics; the slide's numbers are
course-authored and its annotations frame-local. No dimension annotation, attribute guess, or
provenance guess in `analysis/slide_042_raw.json` is contradicted by the sources; transcribed
frame text stays verbatim. No edit to `analysis/*.json` was made by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
