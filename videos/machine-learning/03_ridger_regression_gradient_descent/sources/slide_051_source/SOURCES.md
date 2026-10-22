# SOURCES.md — slide 051 (perceptron worked example — "Check Classes" on the Z test points; the zero-score "Undefined Class")

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19); binding contract
`~/.zcode/skills/slide-recreation/references/source-research.md` (read before this work).
Method: agy web search (MCP `agy_web_search`) for discovery + **live fetch of every recorded URL
in this same work window** (`curl -sL`; WebFetch returned timeouts on this host) + verification
against the fetched text. Frame facts come from the slide's vision-analysis record
`analysis/slide_051_raw.json` (no `_final.json` yet — research is not dependency-gated).
NO vision calls were made by this worker (no `scripts/16_vision_gate.sh`, no vision model, no
local frame view — web + local-file work only, per the mandate).

## Slide identity

- Frame file: `unique_slides/slide_051.jpg` (960×540, 1px = 1pt per the deck AGENTS.md).
  Badge numeral on the frame: **51** (yellow circle; `labels` contains "51"). Deck rule:
  badge numeral = file number N, no zero-padding.
- Numbering resolution: founder-curated set (51 files, 2026-10-19). `_meta.source_timestamps`:
  `precuration_slide = 165`, kept frame `frame_05748.jpg`, t = 5747 s,
  `provenance: "founder-curated kept frame"`, md5 snapshot
  `17149feb2a99a330a8d98ab1df78fd06`. File number 051 and badge "51" agree; pre-curation 165
  is historical only (pre-curation index intentionally removed by the founder).
- Analysis record used: `analysis/slide_051_raw.json` — no `_final.json` exists at write time.

## Primary source(s)

All URLs **fetched live in this work window (HTTP 200)**, full hashes recorded; none recorded
from an unfetched snippet. Query budget: **0 new queries for this slide** — the cluster's single
agy search plus all fetches were spent and verified under
`sources/slide_045_source/SOURCES.md` / `sources/slide_048_source/SOURCES.md`, cross-referenced
here per the ECONOMY LAW.

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://deeplearning.cs.cmu.edu/S26/documents/readings/Perceptron_Learning_Algorithm_and_Convergence.pdf` | CMU "The Perceptron Learning Algorithm and its Convergence" — the sign(α) = 1 if α ≥ 0 / 0 if α < 0 convention AND the explicit paragraph that zero-on-the-boundary makes the prediction depend on an "arbitrary choice" — the canonical statement of exactly the ambiguity this slide resolves as "Undefined Class". Banked byte-identical at `sources/slide_048_source/cmu_perceptron_pla.pdf`. | **CONFIRMED (origin-level)** — fetched live this window; HTTP 200, 193,758 bytes, sha256 `de8b549f66d9f9c9627826628ec0bba0b7e4cb6595651698576be6c228605688`. |
| `https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html` | Cornell CS 4780 Lecture 3 — the STRICT correctness criterion "y_i(wᵀx_i) > 0 ⟺ x_i is classified correctly" (a zero score is not "classified correctly") and the `h(x)=sign(wᵀx)` classifier. | **CONFIRMED (origin-level)** — fetched live this window; HTTP 200, 11,759 bytes, sha256 `016a9af244c34f3870f11f00e85996f699c723ef9ae147b8bbdec794af74011d`. |
| `https://en.wikipedia.org/wiki/Perceptron` | Wikipedia "Perceptron" — ±1 labels, sign(wᵀx) prediction, "The decision boundary is defined by w^Tx = 0" (via the GfG-class sources' shared convention; Wikipedia's own section states the prediction/decision setup and the update rule). | **CONFIRMED (origin-level)** — fetched live this window; HTTP 200, 511,237 bytes, sha256 `ab8b324c8e78c181f50078b5ed0fa7886e5380f9e434f1367491dec38fafa9a3`. |
| `https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf` | UPenn CIS 5190 "Linear Classification: The Perceptron" — "h(x) = sign(wᵀx) where sign(z) = +1 if z ≥ 0, −1 if z < 0" and the strict training trigger "if y(i)x(i)ᵀw ≤ 0 // prediction is incorrect". | **CONFIRMED (origin-level)** — fetched live this window; HTTP 200, 3,126,847 bytes, sha256 `a045390ab90326904197323e7bf26d5d4e09df6eefb04af713549906793489e4`. |
| `https://www.geeksforgeeks.org/deep-learning/perceptron-convergence-theorem-in-neural-networks/` | GfG "Perceptron Convergence Theorem in Neural Networks" — "The decision boundary is defined by w^Tx = 0 which represents a hyperplane separating the two classes" and the C1/C2 update procedure. | **CONFIRMED (origin-level)** — fetched live this window; HTTP 200, 321,706 bytes, sha256 `b6acf2e8fbde41aaaffb2143b44a621166fdccc7d6b820e2363612db7a663e7d`. |

Sibling origin-level cross-references (no re-fetch): `sources/slide_045_source/SOURCES.md`,
`sources/slide_047_source/SOURCES.md` (the same d(Z) evaluation idiom and the "Zero is
unaccepted" clause), `sources/slide_048_source/SOURCES.md` (the η = 1 run that produced
W = (5,−1,−1), the weights used here), `sources/slide_049_source/SOURCES.md`,
`sources/slide_050_source/SOURCES.md`, `sources/slide_037_source/` (banked DHS Ch. 5 PDF, md5
`47235972a70be5152744c50b8a64f77d`), `sources/slide_039_source/SOURCES.md`. Sister records
041–044 were still in progress at write time; nothing here depends on them.

## Figures used by this slide

**None — and correctly so.** The frame is matrices + three boxed decision computations + a red
"Check Classes" button, all course-built; no source-published figure is reused or redrawn.
(Canonical algorithm figures are banked at `sources/slide_048_source/` with hashes and
byte-identity results; none is reproduced on this frame.) Reason stated per the layout law.

## What the source(s) CONFIRM

Frame facts (from `analysis/slide_051_raw.json` verbatim_text/equations): "Initial W =
[4; −2; −2]", red italic "Step η = 1", legend "C₁ positive C₂ negative Zero is unaccepted",
"Check classes of" test matrix headed Z₁ Z₁ Z₁, the augmented matrix, red "Check Classes" button,
and three decision rows: `d(Z₁) = [1 0 0; 5; −1] = 5 ⇒ Positive > 0 ⇒ Class I`,
`d(Z₂) = [1 7 6; 5; −1] = −8 ⇒ Negative < 0 ⇒ Class II`,
`d(Z₃) = [1 3 2; 5; −1] = 0 ⇒ "Not > 0 , Not < 0" ⇒ Undefined Class`.

1. **All three printed decision values recompute exactly** with the canonical decision
   function d(Z) = WᵀZ and the converged W = (5, −1, −1) of this η = 1 example:
   Z₁ = (0,0) ⇒ (1,0,0)·(5,−1,−1) = **5** ✓; Z₂ = (7,6) ⇒ 5−7−6 = **−8** ✓;
   Z₃ = (3,2) ⇒ 5−3−2 = **0** ✓. The dot-product form (bias carried as the leading 1; test
   points augmented identically to training points) is standard — CONFIRMED (Wikipedia
   "v(n) = Σ w_i(n)x_i(n) = w^T(n)x(n)", "x_{j,0} = 1"; Cornell "[x_i; 1]ᵀ[w; b] =
   wᵀx_i + b"; UPenn "we incorporated bias term w₀ into it by x₀ = 1"; CMU "(d+1)-dimensional"
   bias transformation). CONFIRMED.
2. **The sign rule d(Z) > 0 ⇒ Class I, d(Z) < 0 ⇒ Class II.** CONFIRMED: UPenn "w^Tx > 0 ⟹
   y = +1 / w^Tx < 0 ⟹ y = −1"; Cornell "y_i(wᵀx_i) > 0 ⟺ x_i is classified correctly" with
   y ∈ {−1,+1}; the GfG decision boundary "w^Tx = 0". CONFIRMED.
3. **The zero case `d(Z₃) = 0 ⇒ "Not > 0 , Not < 0" ⇒ Undefined Class`** — the slide's
   explicit three-way classification. The canonical sources acknowledge this exact boundary
   situation: Cornell's correctness criterion is STRICT (y_i(wᵀx_i) > 0), so a zero score is
   "not correctly classified" under any label; CMU devotes a paragraph to the ambiguity ("the
   Perceptron's predictions for these points would depend on whether we assign sign(0) to be 0
   or 1—which seems an arbitrary choice") and its own sign(α) convention picks ≥ 0 ⇒ +1, while
   UPenn's deck likewise picks sign(0) = +1 — the sources DISAGREE at zero by convention, which
   is precisely why the course states it explicitly. The course's training-time clause "Zero is
   unaccepted" (update fires: CMU/UPenn loops use ≤ 0) and its classification-time outcome
   "Undefined Class" are the two consistent resolutions of that ambiguity. CONFIRMED as the
   textbook boundary case; the "Undefined Class" NAME is course-authored.
4. **The weights used (W = (5,−1,−1), shown in the frame's brackets as the trailing (5; −1)
   components) are the converged result of this example's η = 1 run** (sibling frames 048/049;
   source-side trace recorded in those records). CONFIRMED.
5. **"Check Classes" / "Check classes of" — evaluating the trained perceptron on held-out
   points after convergence.** Standard post-training evaluation; no source figure implicated
   (course-authored overlay and button). CONFIRMED as standard practice.
6. **"Step η = 1"** — standard learning-rate hyperparameter (Wikipedia "Learning rate is a
   positive number usually chosen to be less than 1"); value course-authored.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The dataset, initial W, η = 1, the Z test points (0,0), (7,6), (3,2), and the worked example:
  course-authored.
- The three-way outcome naming ("Class I" / "Class II" / "Undefined Class"), the captions
  "Positive > 0" / "Negative < 0" / "Not > 0 , Not < 0", the legend, and the red "Check
  Classes" button: course pedagogy wording (the underlying conventions are standard — above).
- The bracket display d(Z) = [<Z row>; <w₀ w₁ tail>] and the red/blue class-tag coloring:
  course-authored presentation.
- The mouse-pointer cursor beside "Undefined Class" (live-demo capture artifact): retained for
  frame fidelity only.
- Frame spelling "Augmented Vectors (from Top)" preserved verbatim (no correction).

## [?] Uncertain items

- **The test-matrix read on this frame is three rows — (0)(0)(0), (7)(6)(2), (3)(2)(2) — under
  headers Z₁ Z₁ Z₁**, whereas the frame's own equations (and sibling frames 046/047/048/050)
  use the two-row matrix (0)(7)(3) over (0)(6)(2), i.e. columns Z₁ = (0,0), Z₂ = (7,6),
  Z₃ = (3,2). The three-row read is most plausibly a vision artifact (the equations are
  internally consistent with the 2-row form). Resolution path: build-time pixel check against
  `unique_slides/slide_051.jpg`; frame wins for recreation if the extra row is real. Not
  web-resolvable.
- **The decision rows' exact bracket layout** ([vector; tail components] stacked) and the class
  tag colors (Class I red; Class II and Undefined blue): frame-level measurements.
- The top-center "Initial W = [4; −2; −2]" beside test points evaluated against the converged
  W = (5,−1,−1): the frame interleaves the run's initialization with its result (course
  arrangement); no web resolution path.
- Exact box geometry, font sizes, stroke weights: frame-only measurements, not web facts.

## Corrections

**None applied.** No dimension annotation, attribute guess, or provenance guess in
`analysis/slide_051_raw.json` is contradicted by the fetched sources. This worker made **no
edit** to any analysis JSON. The three-row matrix read is transcribed frame text — NOT
patchable — and is recorded under [?] with its build-time resolution path, per the corrections
clause.

## Law reminder

The frame wins for recreation; the source wins for understanding.
