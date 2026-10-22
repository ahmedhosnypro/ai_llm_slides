# SOURCES.md — slide 047 (perceptron worked example — "Check Classes" decision boxes, Initial W = [4; −2])

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19); binding contract
`~/.zcode/skills/slide-recreation/references/source-research.md` (read before this work).
Method: agy web search (MCP `agy_web_search`) for discovery + **live fetch of every recorded URL
in this same work window** (`curl -sL`; WebFetch returned timeouts on this host) + verification
against the fetched text. Frame facts come from the slide's vision-analysis record
`analysis/slide_047_raw.json` (no `_final.json` yet — research is not dependency-gated).
NO vision calls were made by this worker (no `scripts/16_vision_gate.sh`, no vision model, no
local frame view — web + local-file work only, per the mandate).

## Slide identity

- Frame file: `unique_slides/slide_047.jpg` (960×540, 1px = 1pt per the deck AGENTS.md).
  Badge numeral on the frame: **47** (yellow circle; `labels` contains "47"). Deck rule:
  badge numeral = file number N, no zero-padding.
- Numbering resolution: founder-curated set (51 files, 2026-10-19). `_meta.source_timestamps`:
  kept frame `frame_01516.jpg`, t = 1511 s, 5-frame group. **No recovered pre-curation slide
  number** for this frame (see deck AGENTS.md "Deck-specific notes": slide 47 is among the 16
  honestly-unrecoverable provenances — the owner removed the pre-curation state; the gap is
  not an error). File number 047 and badge "47" agree.
- Analysis record used: `analysis/slide_047_raw.json` — no `_final.json` exists at write time.

## Primary source(s)

All URLs **fetched live in this work window (HTTP 200)**, hashes recorded; none recorded from
an unfetched snippet. Query budget: **0 new queries for this slide** — the cluster's single agy
search plus all fetches were spent and verified under `sources/slide_045_source/SOURCES.md`,
cross-referenced here per the ECONOMY LAW (covered ground is not re-spent).

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html` | Cornell CS 4780 Lecture 3 "The Perceptron" — sign(wᵀx+b) classifier, bias absorbed by the appended constant dimension, the STRICT "classified correctly iff y_i(wᵀx_i) > 0" criterion. | **CONFIRMED (origin-level)** — fetched live this window under slide 045; HTTP 200, 11,759 bytes, sha256 `016a9af244c34f3870f11f00e85996f699c723ef9ae147b8bbdec794af74011d`. |
| `https://deeplearning.cs.cmu.edu/S26/documents/readings/Perceptron_Learning_Algorithm_and_Convergence.pdf` | CMU "The Perceptron Learning Algorithm and its Convergence" — sign(α) convention discussion ("whether we assign sign(0) to be 0 or 1—which seems an arbitrary choice"), the ≤ 0 update trigger, convergence bound. | **CONFIRMED (origin-level)** — fetched live this window under slide 045; HTTP 200, 193,758 bytes, sha256 `de8b549f66d9f9c9627826628ec0bba0b7e4cb6595651698576be6c228605688`. |
| `https://en.wikipedia.org/wiki/Perceptron` | Wikipedia "Perceptron" — decision via wᵀx with x₀ = 1 augmentation; ±1 labels; convergence statement. | **CONFIRMED (origin-level)** — fetched live this window under slides 045/048; HTTP 200, 511,237 bytes, sha256 `ab8b324c8e78c181f50078b5ed0fa7886e5380f9e434f1367491dec38fafa9a3`. |
| `https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf` | UPenn CIS 5190 "Linear Classification: The Perceptron" — "w^Tx > 0 ⟹ y = +1 / w^Tx < 0 ⟹ y = −1" (and the variant sign(z)=+1 if z ≥ 0), bias via x₀ = 1. | **CONFIRMED (origin-level)** — fetched live this window under slide 045; HTTP 200, 3,126,847 bytes, sha256 `a045390ab90326904197323e7bf26d5d4e09df6eefb04af713549906793489e4`. |
| `https://www.geeksforgeeks.org/deep-learning/perceptron-convergence-theorem-in-neural-networks/` | GfG "Perceptron Convergence Theorem in Neural Networks" — the C1/C2 update rule and decision procedure. | **CONFIRMED (origin-level)** — fetched live this window under slide 045; HTTP 200, 321,706 bytes, sha256 `b6acf2e8fbde41aaaffb2143b44a621166fdccc7d6b820e2363612db7a663e7d`. |

Sibling origin-level cross-references (no re-fetch): `sources/slide_045_source/SOURCES.md`
(the same cluster's fetched evidence), `sources/slide_046_source/SOURCES.md` (terminal-state
plot), `sources/slide_037_source/` (banked Duda–Hart–Stock Ch. 5 PDF, md5
`47235972a70be5152744c50b8a64f77d`), `sources/slide_039_source/SOURCES.md`. Sibling records
041–044 (worked-example start frames) were still in progress at write time; this record does
not depend on them.

## Figures used by this slide

**None — and correctly so.** The frame is matrices + three boxed decision computations + a red
"Check Classes" button, all course-built. No source-published figure is reused or redrawn.
(Canonical algorithm figures are banked at `sources/slide_048_source/` with hashes and
byte-identity results; none is reproduced on this frame.) Reason stated per the layout law.

## What the source(s) CONFIRM

Frame facts (from `analysis/slide_047_raw.json` verbatim_text/equations): "Initial W = [4; −2]",
"Step η = 2", legend "C₁ positive C₂ negative Zero is unaccepted", "Check classes of" matrix
with headers Z₁ Z₁ Z₁ and rows (0)(7)(3) / (0)(6)(2), and three decision boxes:
`d(Z₁) = [1 0 0; −4 0; 14] = 14 ⇒ Positive > 0 ⇒ Class I` (red),
`d(Z₁) = [1 7 6; −4 0; 14] = −14 ⇒ Negative < 0 ⇒ Class II` (blue),
`d(Z₁) = [1 3 2; −4 0; −2] = −2 ⇒ Negative < 0 ⇒ Class II` (blue).

1. **Evaluating a trained perceptron on new points Z via the dot product d(Z) = WᵀZ with the
   Z vectors augmented by the leading 1.** The frame's brackets pair each Z row (1, z₁, z₂)
   with the weight column; the arithmetic is the standard inner product with the bias carried
   as the leading 1 component. CONFIRMED: Cornell "[x_i; 1]ᵀ[w; b] = wᵀx_i + b"; Wikipedia
   "x_{j,0} = 1" and "Linear combiner output: v(n) = Σ w_i(n)x_i(n) = w^T(n)x(n)"; UPenn "we
   incorporated bias term w₀ into it by x₀ = 1"; CMU "transforming the d-dimensional input
   into a (d+1)-dimensional one". CONFIRMED.
2. **The decision rule d(Z) > 0 ⇒ Class I (positive), d(Z) < 0 ⇒ Class II (negative).**
   CONFIRMED: Cornell "y_i(w^T x_i) > 0 ⟺ x_i is classified correctly" with y ∈ {−1,+1}; UPenn
   "w^Tx > 0 ⟹ y = +1 / w^Tx < 0 ⟹ y = −1". The course's "Class I"/"Class II" naming is
   course-authored notation (defined on the deck's own problem-formulation frames); the sign
   convention is standard. CONFIRMED.
3. **The "Zero is unaccepted" clause carried into classification.** The frame's two-branch
   rule (Positive > 0 / Negative < 0) leaves d = 0 unassigned — the course's explicit
   resolution of the sign-at-zero ambiguity that canonical sources flag. CONFIRMED as the
   standard *problem*: Cornell's correctness criterion is STRICT (y_i(wᵀx_i) > 0), so zero is
   "not correct"; CMU devotes a paragraph to the arbitrariness ("the Perceptron's predictions
   for these points would depend on whether we assign sign(0) to be 0 or 1—which seems an
   arbitrary choice"). The course's explicit "unaccepted" is one of the canonical resolutions.
   CONFIRMED.
4. **Worked-example arithmetic (source-side recomputation — the source wins for
   understanding).** The d(Z) brackets display the weight column W = (14, −4, 0) (the η = 2
   example's converged final W; sibling frames 045/046). Recomputing the canonical dot
   product: Z₁ = (0,0) ⇒ d = 14 ✓ (frame 14, "Class I"); Z₂ = (7,6) ⇒ d = 14 − 28 = **−14** ✓
   (frame −14, "Class II"); Z₃ = (3,2) ⇒ d = 14 − 12 = **+2** — the frame prints **−2** with
   the outcome "Negative < 0 ⇒ Class II". The first two boxes agree exactly with the standard
   computation; the third disagrees in sign. CONFIRMED (algorithm + two of three values);
   the third value is recorded under [?] below, frame wins.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The dataset, the initial W, the Z test points (0,0), (7,6), (3,2), and Step η = 2:
  course-authored worked-example material.
- The "Check Classes" red button, the boxed decision rows, the red/blue class-tag coloring,
  the "Positive > 0" / "Negative < 0" captions, the legend colors (C₁ red, C₂ blue, Zero
  green), the light-gray background, and the badge: course/deck styling.
- The bracket display convention d(Z) = [<Z row>; <w₂ w₃ row>; <w₁ row>] (weight components
  interleaved under the test vector): course-authored notation.
- Frame spelling "Ugmented Vectors (from Top)" preserved verbatim (no correction).

## [?] Uncertain items

- **The third decision box's printed value:** frame prints `d(Z₃) = −2 ⇒ Negative < 0 ⇒ Class
  II`; the canonical dot product with the displayed W = (14,−4,0) gives **+2** (which would be
  "Positive > 0 ⇒ Class I"). No consistent weight-vector reading reproduces −2 from
  (1, 3, 2)·W while the first two boxes hold. Resolution path: build-time pixel check of the
  box against `unique_slides/slide_047.jpg`; if it truly prints −2/Class II, the build
  reproduces the frame verbatim (frame wins for recreation; the canonical value is recorded
  for understanding). This worker did not view the frame (no vision calls).
- **All three boxes read "d(Z₁)" in the analysis record's verbatim text** (sibling frames
  048/050 label the same three test points Z₁, Z₂, Z₃ with entries (0,0), (7,6), (3,2) in the
  same order). The repeated subscript is most plausibly a vision/OCR limitation on small
  subscripts. Resolution path: build-time pixel check. Recorded, not patched.
- **"Initial W = [4; −2]" (2 entries) sits beside d(Z) computations that use a 3-entry
  W = (14,−4,0).** The frame interleaves two sub-examples (a 2-D initial-W panel belonging to
  the 2-D example family on frames 042/044, and the 3-entry Z-evaluation from the η = 2 run).
  Recorded as a frame-arrangement fact with no web resolution path (course-authored slide
  composition).
- Exact box geometry, font sizes, stroke weights: frame-only measurements, not web facts.

## Corrections

**None applied.** No dimension annotation, attribute guess, or provenance guess in
`analysis/slide_047_raw.json` is contradicted by the fetched sources; transcribed frame text
stays verbatim. This worker made **no edit** to `analysis/*.json`. The −2 anomaly is frame
text (not an annotation) and is therefore recorded under [?] with its resolution path, per the
corrections clause.

## Law reminder

The frame wins for recreation; the source wins for understanding.
