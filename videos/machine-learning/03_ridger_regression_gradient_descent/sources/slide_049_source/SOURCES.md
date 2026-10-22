# SOURCES.md — slide 049 (perceptron worked example — Iteration 2, no change, stop; the η = 1 second pass)

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19); binding contract
`~/.zcode/skills/slide-recreation/references/source-research.md` (read before this work).
Method: agy web search (MCP `agy_web_search`) for discovery + **live fetch of every recorded URL
in this same work window** (`curl -sL`; WebFetch returned timeouts on this host) + verification
against the fetched text. Frame facts come from the slide's vision-analysis record
`analysis/slide_049_raw.json` (no `_final.json` yet — research is not dependency-gated).
NO vision calls were made by this worker (no `scripts/16_vision_gate.sh`, no vision model, no
local frame view — web + local-file work only, per the mandate).

## Slide identity

- Frame file: `unique_slides/slide_049.jpg` (960×540, 1px = 1pt per the deck AGENTS.md).
  Badge numeral on the frame: **49** (yellow circle; `labels` contains "49"). Deck rule:
  badge numeral = file number N, no zero-padding.
- Numbering resolution: founder-curated set (51 files, 2026-10-19). `_meta.source_timestamps`:
  `precuration_slide = 164`, kept frame `frame_05712.jpg`, t = 5711 s,
  `provenance: "founder-curated 2026-10-19 (frame swap from group)"`, md5 snapshot
  `449ad2054cc8268b17a91fd1b29c6619`. File number 049 and badge "49" agree; pre-curation 164
  is historical only (the pre-curation index was intentionally removed by the founder; note the
  same pre-curation id 164 also appears on slide 050 — a frame-swap pair from one group).
- Analysis record used: `analysis/slide_049_raw.json` — no `_final.json` exists at write time.

## Primary source(s)

All URLs **fetched live in this work window (HTTP 200)**, full hashes recorded; none recorded
from an unfetched snippet. Query budget: **0 new queries for this slide** — the cluster's
single agy search plus all fetches were spent and verified under
`sources/slide_045_source/SOURCES.md` (and, for the PLA pseudocode, under
`sources/slide_048_source/SOURCES.md`), cross-referenced here per the ECONOMY LAW.

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://deeplearning.cs.cmu.edu/S26/documents/readings/Perceptron_Learning_Algorithm_and_Convergence.pdf` | CMU "The Perceptron Learning Algorithm and its Convergence" — the loop "While there exists i … such that y_i(w_k·x_i) ≤ 0" (i.e. terminate exactly when a full pass makes no update) and the theorem's finite-updates guarantee. Banked byte-identical at `sources/slide_048_source/cmu_perceptron_pla.pdf`. | **CONFIRMED (origin-level)** — fetched live this window (slide 045/048 legs); HTTP 200, 193,758 bytes, sha256 `de8b549f66d9f9c9627826628ec0bba0b7e4cb6595651698576be6c228605688`. |
| `https://en.wikipedia.org/wiki/Perceptron` | Wikipedia "Perceptron" §4 — "the weights remain unchanged whenever d_j = y_j(t)" (the frame's Keep-same-Weight rows) and "the perceptron is guaranteed to converge after making finitely many mistakes". | **CONFIRMED (origin-level)** — fetched live this window; HTTP 200, 511,237 bytes, sha256 `ab8b324c8e78c181f50078b5ed0fa7886e5380f9e434f1367491dec38fafa9a3`. |
| `https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf` | UPenn CIS 5190 "Linear Classification: The Perceptron" — "If the prediction matches the label, make no change"; the online loop "if y(i)x(i)ᵀw ≤ 0 // prediction is incorrect". | **CONFIRMED (origin-level)** — fetched live this window; HTTP 200, 3,126,847 bytes, sha256 `a045390ab90326904197323e7bf26d5d4e09df6eefb04af713549906793489e4`. |
| `https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html` | Cornell CS 4780 Lecture 3 — finite-updates convergence for linearly separable data ("the Perceptron will find a separating hyperplane in a finite number of updates. (If the data is not linearly separable, it will loop forever.)"). | **CONFIRMED (origin-level)** — fetched live this window; HTTP 200, 11,759 bytes, sha256 `016a9af244c34f3870f11f00e85996f699c723ef9ae147b8bbdec794af74011d`. |
| `https://www.geeksforgeeks.org/deep-learning/perceptron-convergence-theorem-in-neural-networks/` | GfG "Perceptron Convergence Theorem in Neural Networks" — "If a sample is correctly classified, no update is made: w(n+1) = w(n)" and "Repeat Until Convergence". | **CONFIRMED (origin-level)** — fetched live this window; HTTP 200, 321,706 bytes, sha256 `b6acf2e8fbde41aaaffb2143b44a621166fdccc7d6b820e2363612db7a663e7d`. |

Sibling origin-level cross-references (no re-fetch): `sources/slide_045_source/SOURCES.md`,
`sources/slide_048_source/SOURCES.md` (the Iteration-1 pass of this same η = 1 example),
`sources/slide_037_source/` (banked Duda–Hart–Stock Ch. 5 PDF, md5
`47235972a70be5152744c50b8a64f77d` — Algorithm 4's fixed-increment rule revisited until no
misclassified sample remains), `sources/slide_039_source/SOURCES.md`. Sister records 041–044
were still in progress at write time; nothing here depends on them.

## Figures used by this slide

**None — and correctly so.** The frame is tables + one red callout + six calculation bands, all
course-built; no source-published figure is reused or redrawn. (Canonical algorithm figures are
banked at `sources/slide_048_source/` with hashes and byte-identity results; none is reproduced
on this frame.) Reason stated per the layout law.

## What the source(s) CONFIRM

Frame facts (from `analysis/slide_049_raw.json` verbatim_text/equations): "Initial W = [4, −2]"
(placed in the top table's "Initial" column), red "REPEAT using Step η = 1", "Check classes of"
grid (Z₁ Z₁ Z₁ / (0)(7)(3) / (0)(6)(2)), the legend, the red callout "Iteration 2 / No change in
W / Stop Iterations", and six calculation rows each ending "Keep same Weight, W = [[5],
[−1], [−1]]" with printed results 3, 2, 2, −4, −6, −7.

1. **The six printed results 3, 2, 2, −4, −6, −7 all recompute exactly** with the canonical
   decision function d(x) = Wᵀx and the Iteration-1 result W = (5, −1, −1) carried forward:
   x₁ = (1,1,1) ⇒ 5−1−1 = **3** ✓; x₂ = (1,2,1) ⇒ 5−2−1 = **2** ✓; x₃ = (1,1,2) ⇒ 5−1−2 = **2** ✓;
   x₄ = (1,5,4) ⇒ 5−5−4 = **−4** ✓; x₅ = (1,6,5) ⇒ 5−6−5 = **−6** ✓; x₆ = (1,6,6) ⇒ 5−6−6 = **−7** ✓.
   The decision function's form (dot product, bias carried as the leading 1) is standard —
   CONFIRMED (Wikipedia "v(n) = Σ w_i(n)x_i(n) = w^T(n)x(n)", "x_{j,0} = 1"; Cornell
   "[x_i; 1]ᵀ[w; b] = wᵀx_i + b"; UPenn "x₀ = 1").
2. **"Keep same Weight" on every row** — when d(x) is already on the correct side (C₁ > 0, C₂ <
   0), the update does not fire and the weight vector carries forward unchanged. CONFIRMED:
   Wikipedia "the weights remain unchanged whenever d_j = y_j(t)"; GfG "If a sample is
   correctly classified, no update is made: w(n+1) = w(n)"; UPenn "If the prediction matches
   the label, make no change". CONFIRMED.
3. **"No change in W / Stop Iterations" as the termination rule** — the algorithm stops after a
   full pass in which no sample triggered an update. CONFIRMED: CMU's loop is "While there
   exists i ∈ {1..n} such that y_i(w_k·x_i) ≤ 0 … Return w_k" — the exit condition is exactly
   "no misclassified (or zero-scored) point remains"; Cornell: "If a data set is linearly
   separable, the Perceptron will find a separating hyperplane in a finite number of updates.
   (If the data is not linearly separable, it will loop forever.)"; Wikipedia: "the perceptron
   is guaranteed to converge after making finitely many mistakes"; GfG: "Repeat Until
   Convergence". CONFIRMED.
4. **"Iteration 2" as the second pass of the SAME η = 1 run** (the first pass is sibling slide
   048's "Iteration 1"). CONFIRMED structure: single-sample updates swept per pass
   (Wikipedia's step 2 "For each example j in our training set D"; UPenn's online learning
   "the model update is performed each time a single observation is received"). Source-side
   recomputation of the full run: pass 1 makes exactly one update (at x₁, whose score is
   0 — the "Zero is unaccepted" case), pass 2 changes nothing ⇒ stop. CONFIRMED.
5. **The class legend "C1 positive C2 negative Zero is unaccepted"** and the check-classes grid:
   same standard conventions as the sibling records (Cornell's strict correctness criterion;
   CMU's ≤ 0 trigger and sign(0)-arbitrariness paragraph; UPenn's sign convention) —
   CONFIRMED at the algorithm level; the course's wording and the Z precomputation grid are
   course-authored.
6. **Step η = 1** as the run's learning rate — standard hyperparameter (Wikipedia "Learning
   rate is a positive number usually chosen to be less than 1"); value course-authored.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The dataset, W₀ = (4,−2,−2), η = 1, the Z test points, and the entire worked example:
  course-authored.
- "REPEAT using Step η = 1", "Keep same Weight", "No change in W / Stop Iterations",
  "Iteration 2", the legend, "Check classes of" grid: course pedagogy wording.
- The red filled callout (white bold text), the yellow badge, table borders/colors, and the
  band-separated calculation rows: deck chrome.
- The frame's row-vector rendering "Initial W = [4, −2]" (2 entries) sits beside a 3-component
  weight usage [(5),(−1),(−1)] — the frame mixes its 2-D and 3-D sub-examples (frame-arrangement
  fact, recorded; no source counterpart).
- Frame spelling "Ugmented Vectors (from Top)" preserved verbatim (no correction).

## [?] Uncertain items

- **The top table's row 3 duplicates row 2 `(1)(1)(2)(4)(5)(6)`** (and the augmented table
  likewise carries the feature row twice). Sibling frames show the same duplication artifact in
  places; all equations use exactly two features. Resolution path: build-time pixel check
  against `unique_slides/slide_049.jpg`; frame wins for recreation if the duplicate is real.
- **The calculation bands' bracket form `d(xᵢ) = [[1, f₁, f₂, 5], [−1, result]]`** (the trailing
  "5" and the [−1, result] pair) is a compressed course notation whose exact glyph layout is a
  frame-level measurement; the six RESULTS recompute exactly (above), which is the
  source-relevant part. Resolution path: build-time pixel check for the bracket layout.
- Exact band geometry, font sizes, stroke weights: frame-only measurements, not web facts.

## Corrections

**None applied.** No dimension annotation, attribute guess, or provenance guess in
`analysis/slide_049_raw.json` is contradicted by the fetched sources. This worker made **no
edit** to any analysis JSON. The duplicated-row anomaly is transcribed frame text — NOT
patchable — and is recorded under [?] with its resolution path, per the corrections clause.

## Law reminder

The frame wins for recreation; the source wins for understanding.
