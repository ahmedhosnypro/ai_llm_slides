# SOURCES.md — slide 022 "[3] Inverse of High Dimension (non-singular) Matrix"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search (MCP `agy_web_search`) for discovery + live `curl -sL` fetch of every URL recorded below
in this same work window. Frame facts come from the slide's vision-analysis record
(`analysis/slide_022_final.json`, verdict PASS_WITH_FIXES, recreatability 9). **No vision calls
were made by this worker.** (Local image read of `unique_slides/slide_022.jpg` was attempted;
image rendering is unavailable to this worker, so all frame facts are from the analysis record.)
Query economy: **no new query spent on this slide** — all claims are covered by the cluster's
anchor sources fetched live and banked in `sources/slide_019_source/SOURCES.md`,
`sources/slide_020_source/SOURCES.md` and `sources/slide_021_source/SOURCES.md` (this worker,
same work window).

## Slide identity

- Frame file: `unique_slides/slide_022.jpg` (960×540). Badge numeral **22** (yellow #FFFF00
  circle, black numeral, ~45 px diameter per the record).
- Numbering resolution: founder-curated numbering 2026-10-19; pre-curation state
  intentionally unrecoverable. `_meta` records `precuration_slide = 104` (kept frame
  `frame_02420.jpg`, t = 2419 s, `provenance: "founder-curated kept frame"`). File number 022
  and badge "22" agree; pre-curation 104 is historical only.
- Analysis record used: `analysis/slide_022_final.json` (validated by glm-5.3, 698.5 s). The
  frame is a **title-only section divider**: "[3] Inverse of High Dimension" / "(non-singular)
  Matrix", badge, mouse-cursor recording artifact (excluded from recreation by the brief), no
  body text.

## Primary source(s)

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Invertible_matrix` | **"Invertible matrix"** — invertibility of a (large) square matrix: full rank / non-zero determinant; the "(non-singular) Matrix" qualifier on the divider. | **CONFIRMED** — fetched live this window, HTTP 200, 440,221 bytes, no redirect. Banked in `sources/slide_020_source/SOURCES.md` (this worker). **No new query spent.** |
| `https://en.wikipedia.org/wiki/Gaussian_elimination` | **"Gaussian elimination"** — the cost of actually computing that inverse at high dimension, which is the transition this divider sets up (its cost claim is stated on slide 023). | **CONFIRMED** — fetched live this window, HTTP 200, 368,265 bytes, no redirect. |
| `https://cs229.stanford.edu/notes2021fall/cs229-notes1.pdf` | Stanford **CS229 Part I notes (2021 fall)** — the high-dimensional case of the inverse problem: fewer linearly independent examples than features ⇒ XᵀX not invertible. | **CONFIRMED** — fetched live this window, HTTP 200, 357,392 bytes. Banked in `sources/slide_020_source/SOURCES.md` (this worker). **No new query spent.** |

No URL above was recorded from an unfetched snippet; all were re-fetched live in this work
window.

## Figures used by this slide

**None — and correctly so.** Title-only divider: no chart, diagram, image or reused figure
(`imagery: []`; `visual_elements` holds only the badge and the cursor artifact). Nothing was
downloaded. Per the layout law the reason is stated rather than left silent.

## What the source(s) CONFIRM

1. **"(non-singular) Matrix" — the divider's parenthetical is the correct technical qualifier.**
   Verbatim (*Invertible matrix*): "In linear algebra, an **invertible matrix** (*non-singular*,
   non-degenerate or regular) is a square matrix that has an inverse." So the section the
   divider announces — inverting a high-dimensional matrix that *is* non-singular — is a
   well-posed (in principle) linear-algebra operation, and the deck's next section (slide 023)
   is about when it is impractical even when well-posed.
2. **The rank criterion is dimension-sensitive, which is the "high dimension" hook.** Verbatim
   (*Invertible matrix*): "Equivalently, an n × n matrix is invertible if its rank is n, by the
   rank-nullity theorem. Such a matrix is said to be of full rank." At high dimension the
   matrix must reach full rank n for its inverse to exist, and the CS229 notes spell out the
   regression-side failure mode verbatim: "If either the number of linearly independent
   examples is fewer than the number of features, or if the features are not linearly
   independent, then XᵀX will not be invertible." — i.e. the high-dimensional feature count d
   grows the (d+1)×(d+1) moment matrix toward exactly the singularity case slide 021 just
   demonstrated with a 3×3 example.
3. **"High dimension" ⇒ the algorithm's cost, not its well-posedness, becomes the binding
   problem.** The standard algorithm's cost at size n is confirmed verbatim (*Gaussian
   elimination*, *Computational efficiency*):
   > "Computationally, for an n × n matrix, this method needs only O(n³) arithmetic
   > operations, while using Leibniz formula for determinants requires (n n!) operations …"

   and (same section) "to solve a system of n equations for n unknowns by performing row
   operations on the matrix until it is in echelon form … for a total of approximately 2n³/3
   operations." This is the cost that slide 023 then multiplies out; the divider's
   "high dimension" framing is exactly the case where this cost bites.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The section numbering "[3]", the deck's divider format, and the exact two-line break
  "[3] Inverse of High Dimension" / "(non-singular) Matrix".
- The "(non-singular) Matrix" qualifier as a *precondition* on the section — the sources use
  the word, but the course has chosen to make non-singularity a stated assumption of the
  section rather than discuss the singular case again.
- Arial 48 pt bold #C00000 centred title; yellow #FFFF00 badge ~45 px with no outline; #F0F0F0
  background measured on the frame vs the deck's mandated white canvas (house-chrome law
  governs).
- The mouse-cursor artifact — a live-presentation capture item, explicitly excluded from
  recreation by the brief's step 9.

## [?] Uncertain items

| # | Item | Status / resolution path |
|---|---|---|
| 1 | Exact title font size (48 pt is the record's pinned midpoint of a 44–54 pt estimate) | Frame-only; no source supplies a course slide's pt size. Carried by the build stage. |
| 2 | Whether the badge circle has an outline | Frame-only; the record selected "no outline" because the source describes only fill + text. |
| 3 | Which specific high-dimensional method the section will cover (the frame announces; it does not show) | The section's actual content lands on slide 023 (inversion cost) — resolved there, not here. |

## Corrections

**None.** No dimension, attribute or provenance guess in `analysis/slide_022_final.json` is
contradicted by any source; the sources *confirm* the divider's terminology and set up its
subject. No `analysis/*.json` file was edited by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
