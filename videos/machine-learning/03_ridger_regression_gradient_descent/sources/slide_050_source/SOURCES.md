# SOURCES.md — slide 050 "Iteration 2" (perceptron worked example — terminal 2-D view, final W = (5, −1), plotted decision boundary)

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19); binding contract
`~/.zcode/skills/slide-recreation/references/source-research.md` (read before this work).
Method: agy web search (MCP `agy_web_search`) for discovery + **live fetch of every recorded URL
in this same work window** (`curl -sL`; WebFetch returned timeouts on this host) + verification
against the fetched text. Frame facts come from the slide's vision-analysis record
`analysis/slide_050_raw.json` (no `_final.json` yet — research is not dependency-gated).
NO vision calls were made by this worker (no `scripts/16_vision_gate.sh`, no vision model, no
local frame view — web + local-file work only, per the mandate). The `analysis/` ↔
`RECONCILE_NOTE.md` rename (`slide_50_raw.json` → `slide_050_raw.json`, OCR-attribution
verified) is a local-file fact, noted here for the record trail.

## Slide identity

- Frame file: `unique_slides/slide_050.jpg` (960×540, 1px = 1pt per the deck AGENTS.md).
  Badge numeral on the frame: **50** (yellow circle; `labels` contains "50"). Deck rule:
  badge numeral = file number N, no zero-padding.
- Numbering resolution: founder-curated set (51 files, 2026-10-19). `_meta.source_timestamps`:
  `precuration_slide = 164`, kept frame `frame_05734.jpg`, t = 5733 s,
  `provenance: "founder-curated kept frame"`, md5 snapshot
  `0a8ae7bced67a957569a3b4c4ecafa29`. File number 050 and badge "50" agree; pre-curation 164
  is historical only (pre-curation index intentionally removed; the same pre-curation id also
  appears on slide 049 — a frame-swap pair from one group).
- Analysis record used: `analysis/slide_050_raw.json` — no `_final.json` exists at write time.

## Primary source(s)

All URLs **fetched live in this work window (HTTP 200)**, full hashes recorded; none recorded
from an unfetched snippet. Query budget: **0 new queries for this slide** — the cluster's single
agy search plus all fetches were spent and verified under
`sources/slide_045_source/SOURCES.md` / `sources/slide_048_source/SOURCES.md`, cross-referenced
here per the ECONOMY LAW.

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Perceptron` | Wikipedia "Perceptron" — decision rule via sign(wᵀx), the no-update-on-correct-pass behavior, finite-mistakes convergence, learning-rate r. | **CONFIRMED (origin-level)** — fetched live this window; HTTP 200, 511,237 bytes, sha256 `ab8b324c8e78c181f50078b5ed0fa7886e5380f9e434f1367491dec38fafa9a3`. |
| `https://deeplearning.cs.cmu.edu/S26/documents/readings/Perceptron_Learning_Algorithm_and_Convergence.pdf` | CMU "The Perceptron Learning Algorithm and its Convergence" — the hyperplane interpretation (weights = the normal vector to the decision hyperplane) and the termination/convergence statements. Banked byte-identical at `sources/slide_048_source/cmu_perceptron_pla.pdf`. | **CONFIRMED (origin-level)** — fetched live this window; HTTP 200, 193,758 bytes, sha256 `de8b549f66d9f9c9627826628ec0bba0b7e4cb6595651698576be6c228605688`. |
| `https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html` | Cornell CS 4780 Lecture 3 — "The Perceptron was arguably the first algorithm with a strong formal guarantee. If a data set is linearly separable, the Perceptron will find a separating hyperplane in a finite number of updates." | **CONFIRMED (origin-level)** — fetched live this window; HTTP 200, 11,759 bytes, sha256 `016a9af244c34f3870f11f00e85996f699c723ef9ae147b8bbdec794af74011d`. |
| `https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf` | UPenn CIS 5190 "Linear Classification: The Perceptron" — "A hyperplane partitions R^d into two half-spaces … defined by the normal vector w which is orthogonal to any vector lying on the hyperplane"; the sign rule "w^Tx > 0 ⟹ y = +1". | **CONFIRMED (origin-level)** — fetched live this window; HTTP 200, 3,126,847 bytes, sha256 `a045390ab90326904197323e7bf26d5d4e09df6eefb04af713549906793489e4`. |
| `https://www.geeksforgeeks.org/deep-learning/perceptron-convergence-theorem-in-neural-networks/` | GfG "Perceptron Convergence Theorem in Neural Networks" — "The decision boundary is defined by w^Tx = 0 which represents a hyperplane separating the two classes"; repeat-until-convergence loop. | **CONFIRMED (origin-level)** — fetched live this window; HTTP 200, 321,706 bytes, sha256 `b6acf2e8fbde41aaaffb2143b44a621166fdccc7d6b820e2363612db7a663e7d`. |

Sibling origin-level cross-references (no re-fetch): `sources/slide_045_source/SOURCES.md`,
`sources/slide_046_source/SOURCES.md` (the η = 2 example's terminal plot — the same chart idiom),
`sources/slide_048_source/SOURCES.md` (the η = 1 Iteration-1 pass that produced this example's
weights), `sources/slide_049_source/SOURCES.md` (this example's Iteration-2 no-change pass),
`sources/slide_037_source/` (banked DHS Ch. 5 PDF, md5 `47235972a70be5152744c50b8a64f77d`),
`sources/slide_039_source/SOURCES.md`. Sister records 041–044 were still in progress at write
time; nothing here depends on them.

## Figures used by this slide

**None — and correctly so.** The frame's chart is a course-built redraw of the lecture's own
six-point dataset with the learned boundary; no source-published figure is reused or redrawn.
(Canonical algorithm figures — Cornell's hyperplane/perceptron-update illustrations — are
banked at `sources/slide_048_source/` with hashes and byte-identity results; none is
reproduced here, and the slide's red/blue/magenta series coloring has no counterpart in the
grayscale sources.) Reason stated per the layout law.

## What the source(s) CONFIRM

Frame facts (from `analysis/slide_050_raw.json` verbatim_text/equations): "Initial W =
(4; −2)", "REPEAT using Step η = 1", "Check classes of Z₁=(0,0)ᵀ, Z₂=(7,6)ᵀ, Z₃=(3,2)ᵀ", the
pink box with underlined "W = (5; −1)", red "Iteration 2" box, "No change in W / Stop
Iterations", and the chart (axes 0–8 / 0–7, thick red directed line ~through (3,3), '+ve'
annotation, blue squares at the C₁ points, magenta diamonds at the C₂ points, red triangles at
the Z test points).

1. **The chart's red line is the learned decision boundary wᵀx = 0** — the separating
   hyperplane drawn in feature space. CONFIRMED: GfG "The decision boundary is defined by
   w^Tx = 0 which represents a hyperplane separating the two classes"; UPenn "A hyperplane
   partitions R^d into two half-spaces — Defined by the normal vector w which is orthogonal to
   any vector lying on the hyperplane"; CMU "the parameters (or weights) of the Perceptron may
   be interpreted as the components of a normal vector to the hyperplane". CONFIRMED.
2. **The boundary's direction matches the converged weights.** The run's final W (per the
   Iteration-1/2 frames, in bias-absorbed form) is (5, −1, −1), whose hyperplane 5 − x − y = 0
   has normal (−1, −1) — i.e. a line of slope −1 in (x,y), perpendicular to the (1,1)
   direction. The frame's drawn line (through ~(3,3), endpoints ~(0.5,5.5) and ~(7,0.5)) also
   has slope −1 with normal (1,1) — the SAME direction. Direction CONFIRMED; the drawn
   constant (line x+y≈6 vs the displayed W's x+y=5) is recorded under [?] below.
3. **The boundary separates the two classes as required for the run to have stopped.**
   Source-side check with W = (5,−1,−1): C₁ points (1,2),(2,1),(1,1) give d = 2, 2, 3 > 0 ✓ and
   C₂ points (5,4),(6,5),(6,6) give d = −4, −6, −7 < 0 ✓ — every training point strictly
   correctly classified, which is exactly the termination condition (CMU's loop exits when no
   point has y_i(w·x_i) ≤ 0; Cornell "will find a separating hyperplane in a finite number of
   updates"). CONFIRMED.
4. **"No change in W / Stop Iterations"** — the terminal state of a converged run. CONFIRMED
   (same canonical loop condition as the sibling records; Cornell/Wikipedia/CMU/GfG quotes
   recorded under slide 049's and slide 048's records, both fetched live this window).
5. **"Final W = (5; −1)" in the pink box** — the terminus of the η = 1 example (frames 048/049
   carry W = (5,−1,−1) in the full 3-component form; this frame displays the two trailing
   components). Source-side: the (−1,−1) tail is exactly the normal-direction pair of the
   chart's boundary (see item 2). CONFIRMED as the same converged result; the 2-component
   rendering itself is course-authored display.
6. **The Z test points Z₁=(0,0), Z₂=(7,6), Z₃=(3,2) plotted as red triangles (frame marks
   (7,6) and (~3,2/3)):** evaluating the learned classifier on held-out points is the standard
   post-training step (upstream of sibling frame 051's d(Z) decision boxes). No source figure
   implicated; the overlay is course-authored. CONFIRMED as standard practice.
7. **"REPEAT using Step η = 1" / Step η = 1** — standard learning-rate hyperparameter
   (Wikipedia "r is the learning rate … a positive number usually chosen to be less than 1");
   value course-authored.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The dataset, initial W, η = 1, and the entire worked example: course-authored.
- The chart styling: white panel + red border, blue squares (C₁), magenta diamonds (C₂), red
  triangles (Z points), the thick directed red boundary with arrowhead, the '+ve' annotation,
  the y-axis deliberately skipping the "1" tick label, the pink rounded W box, the stray black
  plus sign, the red Iteration-2 box and badge: deck chrome/course rendering.
- The 2-component "Initial W = (4; −2)" display inside a 3-component computation: course
  display shorthand (see [?]).
- Frame spelling "Ugmented Vectors (from Top)" preserved verbatim (no correction).

## [?] Uncertain items

- **The drawn boundary's constant:** the chart's line passes ~through (3,3) (⇒ x + y ≈ 6),
  while the displayed final W = (5,−1,−1) gives x + y = 5. Both are valid separators of the
  same data (direction confirmed; the offset is within vision's "about" tolerance and the exact
  pixel trace is a frame measurement). Resolution path: build-time pixel check of the line's
  intercepts against `unique_slides/slide_050.jpg`. Frame wins for recreation; the
  source-side mapping (W ⇒ boundary line) is recorded for understanding.
- **C₁ marker positions read (1,1),(2,1),(2,2) on this frame** where sibling frame 046 reads
  (1,1),(1,2),(2,1) (and all equations imply C₁ = {(1,2),(2,1),(1,1)}). Cross-frame comparison
  (local-file analysis records only — no vision call) suggests (2,2) is a vision variance of
  (1,2). Resolution path: build-time pixel check. Not web-resolvable.
- **Red triangle Z marker at (~3,2) vs the record's "(3,3)"**: sibling frame 046 plots the Z₃ =
  (3,2) point; this frame's chart reads "(3,3)". Same resolution path: build-time pixel check.
- **"Initial W = (4; −2)" (2 components) beside a 3-component converged W:** the frame's 2-D
  sub-example display; its exact relationship to the 3-component weights is a course-authored
  frame-arrangement fact with no web resolution path.
- Exact line weight, marker sizes, axis tick fonts, box geometry: frame-only measurements,
  not web facts.

## Corrections

**None applied.** No dimension annotation, attribute guess, or provenance guess in
`analysis/slide_050_raw.json` is contradicted by the fetched sources. This worker made **no
edit** to any analysis JSON. The boundary-constant and marker-position items above are
frame measurements (transcribed content), not annotations, and are recorded under [?] with
build-time resolution paths, per the corrections clause.

## Law reminder

The frame wins for recreation; the source wins for understanding.
