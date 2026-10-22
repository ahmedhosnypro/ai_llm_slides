# SOURCES.md — slide 044 "Iteration 3"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search + live `curl -sL` fetch of every recorded URL in the same work window that records it +
verification against the fetched text, plus **independent local re-derivation of the slide's
arithmetic** against the standard update rule. **This slide spent 0 new search queries**
(economy law: all claims covered by the cluster's fetched sources, cross-referenced below;
worker query disclosure in `sources/slide_038_source/SOURCES.md`). Frame facts come from
`analysis/slide_044_raw.json`; NO vision calls were made by this worker.

## Slide identity

- Frame file: `unique_slides/slide_044.jpg` (960×540, 1px = 1pt per the deck AGENTS.md).
- Badge number on the frame: **44** (yellow circle, black numeral; `labels` include "44").
- Numbering resolution: per the deck AGENTS.md "Deck-specific notes", slide 44 is one of the
  **16 slides with honestly-unrecoverable pre-curation provenance** (the founder removed the
  pre-curation state; the analysis `_meta` confirms: `provenance: "analysis pending;
  precuration id unrecoverable (owner removed frames/ + pre-curation state)"`). The founder-
  curated file number 044 and the badge "44" are the only authoritative numbering.
- Analysis record used: `analysis/slide_044_raw.json` (no `_final.json` yet).

## Primary source(s)

All URLs were fetched live in this work window (HTTP 200); hashes below. None recorded from an
unfetched snippet; all are origin-level carry-overs of the slides 037/039 fetches — no new
query spent on this slide.

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html` | Cornell CS 4780 **"Lecture 3: The Perceptron"** — ±1 labels, augmented bias vector, strict correctness criterion. | **CONFIRMED (origin-level)** — fetched live this window (11,759 bytes, md5 `d5fa439fe07ebef324b60ede92adcd4f`); quotes banked in `sources/slide_037_source/SOURCES.md`. |
| `https://en.wikipedia.org/wiki/Perceptron` | Wikipedia **"Perceptron"** — per-sample update; no-change when correct. | **CONFIRMED (origin-level)** — fetched live this window (wikitext 51,936 bytes, md5 `4bf47c89c5e97c46cbb0215a59cb9052`); quotes banked in `sources/slide_037_source/SOURCES.md`. |
| `https://www.ccs.neu.edu/home/vip/teach/MLcourse/2_GD_REG_pton_NN/materials/DHS_liniar_disc_intro_perceptron.pdf` | DHS Ch. 5 teaching PDF — Algorithm 4 single-sample correction rule + termination condition. | **CONFIRMED (origin-level)** — banked byte-identical at `sources/slide_037_source/DHS_liniar_disc_intro_perceptron.pdf` (md5 `47235972a70be5152744c50b8a64f77d`), fetched live this window. |
| `https://courses.grainger.illinois.edu/cs440/fa2019/Lectures/lect26.html` | UIUC CS 440 Lecture 26 — the no-op-vs-correct rule. | **CONFIRMED (origin-level)** — fetched live this window (10,582 bytes, md5 `e5422bc0791ac0bf26d932e08bad6ee5`); quotes banked in `sources/slide_037_source/SOURCES.md`. |

## Figures used by this slide

**None — and correctly so.** The slide is a computation stack (two tables + six equation rows
+ badges + a cursor icon); no source figure is reused or redrawn, and no hosted original
corresponds to this instructor-authored worked example. Reason stated per the layout law.

## What the source(s) CONFIRM

1. **The six-row structure and the Update/Keep decision pattern are the canonical
   single-sample rule.** DHS Algorithm 4 (banked OCR): "if y_i is misclassified by a then
   a ← a + y_i ... until all patterns properly classified"; Illinois: "If y' = y, do nothing.
   Otherwise w_i = w_i + α * y * x_i"; Wikipedia: "the weights remain unchanged whenever
   d_j = y_j(t)". CONFIRMED.
2. **The slide's decision pattern is source-consistent on its face:** x₁–x₃ (class C₁)
   carry negative printed d values (−12, −16, −4) and are updated; x₄–x₆ (class C₂) carry
   negative printed d values (−6, −10, −4) and are kept. For C₁ (+1 labels) a negative
   discriminant means misclassified → update; for C₂ (−1 labels) a negative discriminant
   means correct → keep. Both branches match the sign test
   `y_i·(w^T x_i) > 0 ⟺ correct` (Cornell, verbatim banked) exactly. CONFIRMED.
3. **Independent re-derivation of the arithmetic (understanding-level):**
   - The printed W track is internally self-consistent: [4;−2] + 2·[3;−2] = [10;−6] ✓;
     [10;−6] + 2·[1;1] = [12;−4] ✓; [12;−4] + 2·[1;0] = [14;−4] ✓. Every printed update
     equation adds up.
   - **But the printed d(x) results do not re-derive under the printed states** (e.g. with
     W = [4;−2] and x₁ = [1;1;1] the dot product is 2, not −12; the printed bottom matrix rows
     such as "−12; −8" / "−10; −6" / "−6; −2" do not sum to the printed results either), and
     the printed update vectors are not the printed x's ([3;−2], [1;1], [1;0] vs x₁=[1;1;1],
     x₂=[1;2;1], x₃=[1,1,2]).
   - **Cross-slide state discontinuity:** slide 043's iteration 2 ends at W = [10;−2;−10]
     (3-D), while this slide re-prints "Initial W = [4; −2]" (2-D) and runs a 2-D track. The
     two transcripts cannot both be exact. Recorded in `[?]` #1/#2 with a frame re-
     measurement path — NOT patched (the frame wins for recreation; the numbers are
     course-authored).
   - What the re-derivation DOES establish: the iteration logics (compute d, sign-test
     against the class, update or keep) are exactly the standard rule confirmed by the
     sources; only the transcription of the dense matrix displays is unreliable.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- **Every number in the example** — both tables, Initial W, Step η = 2, the Z-check matrix,
  all six equation rows — instructor-authored; no hosted counterpart, none substituted.
- The red "Iteration 3" badge, the "Upgraded Vectors (from Top)" caption, the red/blue class
  colors, the left-pointing arrows on the updated rows, the badge "44", and the cursor icon —
  course styling / artifacts.

## [?] Uncertain items

| # | Item | Resolution path |
|---|---|---|
| 1 | The 2-D vs 3-D weight track discontinuity between slides 043 and 044 (and the re-printed "Initial W = [4; −2]") | frame-level re-measurement of slides 041–044; no source resolution (course-authored values) |
| 2 | Printed d(x) results that do not equal W·x under the printed state (−12 vs 2, etc.) and update vectors that are not the printed x's | frame-level re-measurement (build-time zoom judge); transcribed values stay as recreation truth until then |
| 3 | The bracket layout of the d(x) displays ("[1 1 1; −12; −8]") — exact rows/columns of the printed matrix | frame-level re-measurement; builders transcribe from the frame |

## Corrections

**None.** The sources confirm only the algorithm mechanics; the slide's numbers are
course-authored and its annotations frame-local. Nothing in `analysis/slide_044_raw.json`'s
model annotations is contradicted by the sources; transcribed frame text stays verbatim. No
edit to `analysis/*.json` was made by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
