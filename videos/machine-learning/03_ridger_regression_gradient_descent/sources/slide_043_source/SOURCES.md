# SOURCES.md — slide 043 "Iteration 2"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search + live `curl -sL` fetch of every recorded URL in the same work window that records it +
verification against the fetched text, plus **independent local re-derivation of the slide's
arithmetic** against the standard update rule. **This slide spent 0 new search queries**
(economy law: all claims covered by the cluster's fetched sources, cross-referenced below;
worker query disclosure in `sources/slide_038_source/SOURCES.md`). Frame facts come from
`analysis/slide_043_raw.json`; NO vision calls were made by this worker.

## Slide identity

- Frame file: `unique_slides/slide_043.jpg` (960×540, 1px = 1pt per the deck AGENTS.md).
- Badge number on the frame: **43** (yellow circle, black numeral; `labels` include "43").
- Numbering resolution: per the deck AGENTS.md "Deck-specific notes", slide 43 is one of the
  **16 slides with honestly-unrecoverable pre-curation provenance** (the founder removed the
  pre-curation state; the analysis `_meta` confirms: `provenance: "analysis pending;
  precuration id unrecoverable (owner removed frames/ + pre-curation state)"`). The founder-
  curated file number 043 and the badge "43" are the only authoritative numbering.
- Analysis record used: `analysis/slide_043_raw.json` (no `_final.json` yet).

## Primary source(s)

All URLs were fetched live in this work window (HTTP 200); hashes below. None recorded from an
unfetched snippet; all are origin-level carry-overs of the slides 037/039 fetches — no new
query spent on this slide.

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html` | Cornell CS 4780 **"Lecture 3: The Perceptron"** — ±1 labels, augmented bias vector, strict-inequality correctness criterion (why d = 0 counts as a mistake). | **CONFIRMED (origin-level)** — fetched live this window (11,759 bytes, md5 `d5fa439fe07ebef324b60ede92adcd4f`); quotes banked in `sources/slide_037_source/SOURCES.md`. |
| `https://en.wikipedia.org/wiki/Perceptron` | Wikipedia **"Perceptron"** — per-sample update; no-change when correct. | **CONFIRMED (origin-level)** — fetched live this window (wikitext 51,936 bytes, md5 `4bf47c89c5e97c46cbb0215a59cb9052`); quotes banked in `sources/slide_037_source/SOURCES.md`. |
| `https://www.ccs.neu.edu/home/vip/teach/MLcourse/2_GD_REG_pton_NN/materials/DHS_liniar_disc_intro_perceptron.pdf` | DHS Ch. 5 teaching PDF — Algorithm 4 single-sample correction rule. | **CONFIRMED (origin-level)** — banked byte-identical at `sources/slide_037_source/DHS_liniar_disc_intro_perceptron.pdf` (md5 `47235972a70be5152744c50b8a64f77d`), fetched live this window. |
| `https://courses.grainger.illinois.edu/cs440/fa2019/Lectures/lect26.html` | UIUC CS 440 Lecture 26 — the no-op-vs-correct rule. | **CONFIRMED (origin-level)** — fetched live this window (10,582 bytes, md5 `e5422bc0791ac0bf26d932e08bad6ee5`); quotes banked in `sources/slide_037_source/SOURCES.md`. |

## Figures used by this slide

**None — and correctly so.** The slide is a computation stack (two tables + six calculation
bands + badges + pointer icon); no source figure is reused or redrawn, and no hosted original
corresponds to this instructor-authored worked example. Reason stated per the layout law.

## What the source(s) CONFIRM

1. **The six-band structure (d(x_i) → decision → W equation) is the canonical single-sample
   iteration** — DHS Algorithm 4 (banked OCR): "if y_i is misclassified by a then a ← a + y_i
   ... until all patterns properly classified"; Illinois: "If y' = y, do nothing. Otherwise
   w_i = w_i + α * y * x_i"; Wikipedia: "the weights remain unchanged whenever d_j = y_j(t)".
   The slide's "Update Weight" bands are the correction case; its "Keep same Weight" bands are
   the no-op case. CONFIRMED.
2. **The +/− sign pattern** — C₁ points that fail get `W + 2·x`, C₂ points that fail get
   `W − 2·x` (the slide shows the + form three times and the plain keep for the C₂ rows it
   counts as correct). With labels y ∈ {−1,+1} (Cornell) this is the single rule
   `W ← W + η·y_i·x_i`. CONFIRMED.
3. **"d(x₄) = 0 ⇒ Keep same Weight" is NOT a source-confirmed behavior — flagged, not
   fixed.** The slide's row 4 shows d(x₄) = 0 with the decision "Keep same Weight", whereas
   the slide's own legend (and the sources' strict criterion) treat zero as a failure
   (Cornell: "y_i(w^T x_i) > 0 ⟺ classified correctly"; DHS: g(x)=0 "undefined"; the example's
   own "Zero is unaccepted" rule fired an update on d(x₁)=0 in iteration 1). This is an
   internal inconsistency of the course's worked example at transcription level — recorded in
   `[?]` #3 with a frame re-measurement path. The frame wins for recreation; no patch is
   applied.
4. **Independent re-derivation of the arithmetic (understanding-level):**
   - **Iteration-2 start state is cross-consistent with iteration 1's end:** the slide's
     d(x₁) = −14 re-derives exactly from W = [4;−10;−8] (which slide 042's last rows imply,
     re-derived there: d(x₅) = −96 = 4·1 + (−10)·6 + (−8)·5 ✓) with x₁ = [1;1;1]:
     4 − 10 − 8 = −14. CONFIRMED re-derivable — the iteration chain carries state correctly.
   - **First update re-derives exactly:** x₁ ∈ C₁ with d(x₁) = −14 < 0 ⇒
     W ← [4;−10;−8] + 2·[1;1;1] = [6;−8;−6] ✓ (matches the slide's W equation and its update
     vector being x₁ itself, as the standard rule requires).
   - **Rows 2–6:** every printed W-equation is arithmetically self-consistent (the vector
     additions check out, e.g. [6;−8;−6] + 2·[1;2;−2] = [8;−4;−10]), but at transcription
     level some printed d(x) results do not equal W·x with the printed x's (e.g. d(x₂) = −14
     prints where W=[6;−8;−6]·[1;2;1] = −16), and some printed update vectors are not the
     printed x's (e.g. x₂ = [1;2;1] but update vector [1;2;−2]). The transcription of these
     dense matrix displays is partially garbled. Recorded in `[?]` #1/#2 — frame re-
     measurement decides; nothing is patched.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- **Every number in the example** — both tables (original + augmented), Initial W, Step η = 2,
  the Z-check matrix, all six bands — instructor-authored; no hosted counterpart.
- The red-bordered "Iteration 2" box and pointer icon, the blue left-pointing arrows on the
  first four bands, the red/blue class-label colors, the yellow badge "43", and the white
  canvas — course styling / chrome.
- The course's own sign/zero conventions as printed on this slide (including any inconsistent
  decisions, above) are the frame's content and stay as transcribed.

## [?] Uncertain items

| # | Item | Resolution path |
|---|---|---|
| 1 | d(x) results in rows 2–6 that do not equal W·x under the printed state (−14 vs −16, etc.) | frame-level re-measurement (build-time zoom judge); transcribed values stay as recreation truth until then |
| 2 | Printed update vectors that differ from the printed x's (e.g. [1;2;−2] vs x₂ = [1;2;1]) — transcription-garbled or instructor slip | frame-level re-measurement; no source resolution (course-authored numbers) |
| 3 | Row 4's "d(x₄) = 0 ⇒ Keep same Weight" decision vs the deck's own "Zero is unaccepted" rule | frame-level re-measurement; understanding-level note recorded above |
| 4 | The bracket layout of the d(x) displays ("[1 1 1; −10; −8]") — exact rows/columns of the printed matrix | frame-level re-measurement; builders transcribe from the frame |

## Corrections

**None.** The sources confirm only the algorithm mechanics; the slide's numbers are
course-authored and its annotations frame-local. Nothing in `analysis/slide_043_raw.json`'s
model annotations is contradicted by the sources; transcribed frame text stays verbatim. No
edit to `analysis/*.json` was made by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
