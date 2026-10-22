# SOURCES.md — slide 046 (perceptron worked example — Iteration 4 terminal state, Step η = 2, final W = (14, −4, 0))

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19); binding contract
`~/.zcode/skills/slide-recreation/references/source-research.md` (read before this work).
Method: agy web search (MCP `agy_web_search`) for discovery + **live fetch of every recorded URL
in this same work window** (`curl -sL`; WebFetch returned timeouts on this host) + verification
against the fetched text. Frame facts come from the slide's vision-analysis record
`analysis/slide_046_raw.json` (no `_final.json` yet — research is not dependency-gated).
NO vision calls were made by this worker (no `scripts/16_vision_gate.sh`, no vision model, no
local frame view — web + local-file work only, per the mandate).

## Slide identity

- Frame file: `unique_slides/slide_046.jpg` (960×540, 1px = 1pt per the deck AGENTS.md).
  Badge numeral on the frame: **46** (yellow circle; `labels` contains "46"). Deck rule:
  badge numeral = file number N, no zero-padding.
- Numbering resolution: founder-curated set (51 files, 2026-10-19). `_meta.source_timestamps`:
  `precuration_slide = 157`, kept frame `frame_05595.jpg`, t = 5594 s,
  `provenance: "founder-curated 2026-10-19 (frame swap from group)"`, md5 snapshot
  `0b355cbc667845d46001d7001ada241d`. File number 046 and badge "46" agree; pre-curation 157
  is historical only (pre-curation index intentionally removed by the founder).
- Analysis record used: `analysis/slide_046_raw.json` — no `_final.json` exists at write time.

## Primary source(s)

All URLs **fetched live in this work window (HTTP 200)**, hashes recorded; none recorded from
an unfetched snippet. Query budget: **0 new queries for this slide** — the cluster's single agy
search and all fetches were spent and verified under `sources/slide_045_source/SOURCES.md`,
which this record cross-references (ECONOMY LAW: no redundant re-spend on covered ground).

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html` | Cornell CS 4780 Lecture 3 "The Perceptron" — decision function sign(wᵀx+b), bias absorption via the appended constant dimension, misclassification criterion, finite-updates convergence. | **CONFIRMED (origin-level)** — fetched live this window under slide 045; HTTP 200, 11,759 bytes, sha256 `016a9af244c34f3870f11f00e85996f699c723ef9ae147b8bbdec794af74011d`. |
| `https://deeplearning.cs.cmu.edu/S26/documents/readings/Perceptron_Learning_Algorithm_and_Convergence.pdf` | CMU "The Perceptron Learning Algorithm and its Convergence" (Kalyanakrishnan 2017, after Collins) — PLA pseudocode, ≤ 0 update trigger, sign(0) discussion, convergence bound R²/γ². | **CONFIRMED (origin-level)** — fetched live this window under slide 045; HTTP 200, 193,758 bytes, sha256 `de8b549f66d9f9c9627826628ec0bba0b7e4cb6595651698576be6c228605688`. |
| `https://en.wikipedia.org/wiki/Perceptron` | Wikipedia "Perceptron" — update `w_i(t+1)=w_i(t)+r·(d_j−y_j(t))·x_{j,i}`, `x_{j,0}=1`, learning-rate r, no-update-on-correct, separable-data convergence, Rosenblatt (1958). | **CONFIRMED (origin-level)** — fetched live this window under slides 045/048; HTTP 200, 511,237 bytes, sha256 `ab8b324c8e78c181f50078b5ed0fa7886e5380f9e434f1367491dec38fafa9a3`. |
| `https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf` | UPenn CIS 5190 "Linear Classification: The Perceptron" — h(x)=sign(wᵀx), "If x(i) is misclassified, do w ← w + y(i)x(i)", online loop with the ≤ 0 branch. | **CONFIRMED (origin-level)** — fetched live this window under slide 045; HTTP 200, 3,126,847 bytes, sha256 `a045390ab90326904197323e7bf26d5d4e09df6eefb04af713549906793489e4`. |
| `https://www.geeksforgeeks.org/deep-learning/perceptron-convergence-theorem-in-neural-networks/` | GfG "Perceptron Convergence Theorem in Neural Networks" — C1/C2 update rule verbatim, no-update-if-correct, convergence for linearly separable data. | **CONFIRMED (origin-level)** — fetched live this window under slide 045; HTTP 200, 321,706 bytes, sha256 `b6acf2e8fbde41aaaffb2143b44a621166fdccc7d6b820e2363612db7a663e7d`. |

Sibling origin-level cross-references (no re-fetch): `sources/slide_045_source/SOURCES.md`
(the same worked example's iteration-4 panel and its source-side recomputation),
`sources/slide_037_source/` (banked Duda–Hart–Stock Ch. 5 PDF, md5
`47235972a70be5152744c50b8a64f77d`), `sources/slide_039_source/SOURCES.md`
(course update rule W(updated)=W(old)−ηδᵢXᵢ against DHS/Wikipedia). Sibling records 041–044
(worked-example start frames) were still in progress at write time; this record does not
depend on them.

## Figures used by this slide

**None — and correctly so.** The frame's only non-text marks are the yellow slide-number
circle, the pale-yellow final-W box, the red-outlined "Iteration 4" callout, the pink stop
callout, and the red-bordered scatter plot — all course-built. The plot redraws the lecture's
own data with the lecture's own colors; no source-published figure is reused or redrawn.
(The canonical algorithm figures exist — Cornell's `PerceptronUpdate.png`, CMU's Figure 1 — and
are banked at `sources/slide_048_source/` with hashes and byte-identity results; none is
reproduced on this frame.) Reason stated per the layout law.

## What the source(s) CONFIRM

Frame facts (from `analysis/slide_046_raw.json` verbatim_text/equations): "Initial W =
(4, −2, −2)ᵀ", "Step η = 2", "Check classes of" Z₁ matrix (0 0 7)/(0 6 2), the augmented
matrix, the pale-yellow box "W = (14, −4, 0)ᵀ", "Iteration 4", "No change in W / Stop
Iterations", and the red-bordered scatter plot (x-axis 0–8, y-axis 0–7, a vertical red
decision line near x = 3, blue squares at (1,1)/(1,2)/(2,1), red triangles at (3,2)/(7,6),
magenta diamonds at (5,4)/(6,5)/(6,6), a '+ve' label with a left-pointing arrow).

1. **Final weight W = (14, −4, 0)ᵀ as the converged result of the iteration-4 example.**
   CONFIRMED by source-side recomputation with the canonical rule (slide 045's record, §item 8):
   the η = 2 run from W₀ = (4,−2,−2) reaches exactly W = (14,−4,0) after three updating passes,
   and the fourth pass updates nothing. The canonical loop exits precisely when a full pass
   makes no update — Cornell: "If a data set is linearly separable, the Perceptron will find a
   separating hyperplane in a finite number of updates"; CMU: "While there exists i such that
   y_i(w_k·x_i) ≤ 0 … Return w_k". CONFIRMED.
2. **The decision boundary is a straight line produced by that W, here a vertical line
   x = 3.5.** With the bias carried in W₀ (Cornell: "[x_i; 1]ᵀ[w; b] = wᵀx_i + b"; Wikipedia:
   "x_{j,0} = 1"), the frame's weights give the boundary 14 − 4x + 0·y = 0 ⟹ x = 3.5, i.e. a
   vertical line matching the frame's plotted vertical red line. CONFIRMED as the standard
   construction (the frame's rendered tick position is its own pixel fact — see [?] below).
3. **The positive-class side is the side where d > 0 — the frame's '+ve' arrow points to the
   side containing the blue Class-I squares (left of the line).** With W = (14,−4,0), d > 0 ⟺
   x < 3.5, and the three C₁ points (1,1),(1,2),(2,1) all lie left of the line; the three C₂
   points (5,4),(6,5),(6,6) lie right, d < 0. CONFIRMED — exactly the "C1 positive, C2
   negative" legend carried from the slide family (Cornell "y_i(wᵀx_i) > 0 ⟺ x_i is classified
   correctly"; UPenn "w^Tx > 0 ⟹ y = +1").
4. **The red triangle markers at (7,6) and (3,2) are the "Check classes of" test points
   Z₂ = (7,6)ᵀ, Z₃ = (3,2)ᵀ** plotted on the same axes (the frame's own Z matrix rows
   (0 0 7)/(0 6 2) and (7 6)/(3 2)). Source-side: plotting held-out test points against a
   learned boundary is the standard evaluation step after training converges; no source
   figure is implicated (course-authored overlay). CONFIRMED as a standard practice; the
   plotting itself is course-authored.
5. **"No change in W / Stop Iterations" as the terminal state.** CONFIRMED — CMU's loop
   terminates exactly when no point satisfies y_i(w·x_i) ≤ 0; Wikipedia "The algorithm updates
   the weights after every training sample in step 2b, though one may note that the weights
   remain unchanged whenever d_j = y_j(t)"; GfG "If a sample is correctly classified, no
   update is made: w(n+1) = w(n)". CONFIRMED.
6. **"Step η = 2" as the run's learning rate.** CONFIRMED as the standard η/r/α hyperparameter
   (Wikipedia "r is the learning rate … a positive number usually chosen to be less than 1";
   UPenn "Can eliminate α … its only effect is to scale w by a constant, which doesn't affect
   performance"). The value 2 is course-authored (exceeds the "usually < 1" convention;
   recorded, not corrected).

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The dataset, W₀ = (4,−2,−2), η = 2, the "Check classes of" Z precomputation, and the whole
  six-frame worked example: course-authored (no textbook counterpart).
- The scatter plot styling: white panel + red border, blue squares for C₁, magenta diamonds
  for C₂, red triangles for the Z test points, the '+ve' arrow annotation — course-authored
  rendering choices (sources describe the algorithm, not this figure).
- The pale-yellow final-W box, red-outlined "Iteration 4" callout, pink stop callout, yellow
  badge, and the frame's table colors (C₁ blue / C₂ red in the table, differing from the
  plot's series colors): deck chrome/course styling.
- Frame spelling "Ugmented Vectors (From Top)" preserved verbatim (no correction toward
  "Augmented").

## [?] Uncertain items

- **The plotted vertical decision line reads "at x = 3" in the analysis record while the
  canonical boundary for W = (14,−4,0) is x = 3.5.** Vision reads tick positions
  approximately (the record's own words: "vertical red decision line at x = 3", plus chart
  annotation "vertical red decision line at x=3"); a half-tick offset is within that
  tolerance but unresolved from the JSON alone. Resolution path: build-time pixel check against
  `unique_slides/slide_046.jpg`. Frame wins for recreation; the source-side value (x = 3.5
  for the displayed W) is recorded for understanding.
- **The top table's x₆ column reads (4)(6)(6) on this frame** (sibling frames 048/049/051 read
  x₆ = (6)(6)(6) for features / the same column), a cross-frame variance consistent with
  vision noise on a small cell; the worked example's arithmetic and the plot both use the
  standard column. Resolution path: build-time pixel check. Not web-resolvable.
- **The Z₁ matrix's column labels read "Z₁ Z₁ Z₁" on this frame** (sibling frames 048/050 show
  Z₁ Z₂ Z₃) — same coordinate top row (0 0 7)/(0 6 2). Recorded as a frame-level uncertainty;
  resolution path: build-time pixel check.
- Exact marker sizes, line weight of the red boundary, axis tick font sizes: frame-only
  measurements, not web facts.

## Corrections

**None applied.** No dimension annotation, attribute guess, or provenance guess in
`analysis/slide_046_raw.json` is contradicted by the fetched sources; transcribed frame text
stays verbatim. This worker made **no edit** to `analysis/*.json`. The anomalies above are
frame-transcription items (not annotations), recorded under [?] with build-time resolution
paths, per the corrections clause (corrections patch model annotations only, never transcribed
frame text).

## Law reminder

The frame wins for recreation; the source wins for understanding.
