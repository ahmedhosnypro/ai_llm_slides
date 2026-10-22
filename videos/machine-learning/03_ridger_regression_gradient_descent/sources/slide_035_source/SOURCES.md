# SOURCES.md — slide 035 "Using Gradient Descent to train Linear Regression Model" / subtitle
"(Problem Formulation)"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
("Web-source research mandate", founder in-session directive 2026-10-19); method = agy web
search (MCP tool `agy_web_search`) for discovery + live fetch with `curl -sL` in the same work
window that records the URL (WebFetch was not used; curl was the fetch tool of record) +
verification against the fetched page text. Frame facts come from `analysis/slide_035_raw.json` /
`analysis/slide_035_final.json`; vision transcripts banked separately. NO vision call was made
by this worker (web + local-file work only). NOTE: this slide's build is already certified, and
its research record is still required by the mandate — research interleaves with builds and is
never dependency-gated.
**Query budget for this slide: 0 agy searches, 0 new fetches — every source is already banked
live in this same work window** (economy law; see "Primary source(s)").

## Slide identity

- File: `unique_slides/slide_035.jpg` (960×540, 1px = 1pt), badge numeral **35**.
- Founder-curated numbering (2026-10-19). Pre-curation provenance: **unrecoverable** — the
  founder removed `frames/` and the pre-curation index/mapping; the raw's
  `_meta.source_timestamps` (`kept_frame frame_01256.jpg`, `start_sec 1255.0`, `frame_count 1`)
  carries no `precuration_slide` field, and slide 35 is on the deck AGENTS.md unrecoverable
  list (1,2,3,13,24–29,33,35,36,43,44,47). Expected gap, not an error; no new2old remap.
- `analysis/slide_035_final.json` verdict **PASS_WITH_FIXES**, recreatability 8/10. Frame
  carries only a two-line bold red title, a bold blue subtitle line "(Problem Formulation)",
  a #FFFF00 badge "35", a thin gray #808080 border and a video-capture mouse pointer
  (`imagery`: "White mouse cursor arrow pointer near top-right").
- Deck namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`.
- **Section position:** this is the divider that announces the "Problem Formulation" block of
  the deck's *gradient-descent* half; the formulation that follows (slides 036/037,
  `analysis/slide_037_raw.json`) is the perceptron discriminant `d(X) = W^T X` with
  "Minimize the Error using Gradient Descent with step η" — i.e. exactly the "use GD to train
  the model" programme this title names.

## Primary source(s)

**None needed or spent.** Slide 035 is a pure **section-divider slide**: its entire content is
the verbatim strings

> "Using Gradient Descent to train Linear Regression Model"
> "(Problem Formulation)"

(`analysis/slide_035_final.json` verbatim_text.bullets). There are no equations, no numeric
values, no diagram labels and no figures on the frame that an external source could confirm or
contradict; the strings are course-authored section labelling.

Per the source-research.md economy law ("Reuse banked records: if a sibling slide's SOURCES.md
already covers the claim, cross-reference it and note 'no new query spent'"), the topic this
divider announces is verified **origin-level** by banked sibling records, both fetched live in
this same work window:

- **`sources/slide_030_source/SOURCES.md`** — carries the live-fetched, verbatim quote from
  **https://cs229.stanford.edu/notes2020spring/cs229-notes1.pdf** (Andrew Ng CS229 notes §1
  "LMS algorithm"), which is the canonical statement of *using gradient descent to train a
  linear-regression model*:
  > "We want to choose θ so as to minimize J(θ). To do so, let's use a search algorithm that
  > starts with some 'initial guess' for θ, and that repeatedly changes θ to make J(θ)
  > smaller… Specifically, let's consider the gradient descent algorithm, which starts with
  > some initial θ, and repeatedly performs the update: θj := θj − α ∂J(θ)/∂θj… Here, α is
  > called the learning rate."

  > "…the optimization problem we have posed here for linear regression has only one global,
  > and no other local, optima; thus gradient descent always converges (assuming the learning
  > rate α is not too large) to the global minimum. Indeed, J is a convex quadratic
  > function."

  The same notes derive the LMS update `θj := θj + α (y(i) − hθ(x(i))) xj` on the linear-
  regression cost `J(θ) = ½ Σ (hθ(x) − y)²` — i.e. the "Problem Formulation" this section
  divider opens.
- **`sources/slide_028_source/SOURCES.md`** — the learning-rate half of the same programme
  (Wikipedia *Gradient descent*; Ruder arXiv:1609.04747 §2.1/§3; Nielsen *NNDL* ch.1), also
  live-fetched in this window.
- **`sources/slide_001_source/SOURCES.md`** (wave-1, banked) — deck-level provenance: Zewail
  City CSAI 253 "Machine Learning", catalog scope "regression, classification, …" (origin
  level).
- The formulation itself is banked on the immediately following slides:
  `sources/slide_036_source/SOURCES.md` and the deck's slide 037 (perceptron discriminant +
  "Minimize the Error using Gradient Descent with step η").

**No new query spent, no new fetch spent.**

## Figures used by this slide

None. The slide has no hosted figure to save: no chart, no diagram, no image, no reused
figure. The only non-text marks are the #FFFF00 slide-number badge, the thin gray #808080
border frame, and the white mouse-pointer arrow, which `analysis/slide_035_final.json` records
as a video-recording overlay (a capture artifact, not slide content and not a source figure).

## What the source(s) CONFIRM

- The slide's title is a course-authored section heading naming a standard ML operation —
  training a model by gradient descent on a least-squares error function. Its existence and
  standard content are confirmed at **origin-level** by the banked CS229 quote above
  (Wikipedia/Ruder/Nielsen via `sources/slide_028_source/SOURCES.md`): gradient descent
  `θ := θ − α∇J(θ)` applied to a convex least-squares cost is the standard training procedure
  for linear regression, and it "always converges … to the global minimum" (CS229). No
  independent factual claim on this frame required a separate fetch.
- The frame's own `verbatim_text` is fully captured by the analysis record; no transcription
  needs a source.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

Everything on this slide is course-authored chrome/section furniture: the title wording and its
two-line break, the bold red (#C00000) ~large centred sans-serif title, the bold blue (#0000FF)
subtitle "(Problem Formulation)", the #F2F2F2 background, the #FFFF00 badge with black
outline, and the thin gray #808080 border. No web source counterpart exists and none should be
"fixed" toward one. The mouse-pointer arrow is a video capture item, not slide content.
One wording observation recorded for understanding only, **not** patched (it is frame text):
the title names "Linear Regression Model" while the formulation that follows this divider
(slides 036/037) is the **perceptron** discriminant — the deck uses "Linear Regression Model"
as the section label for the GD-formulation block. The frame's wording stays verbatim for
recreation; the sources confirm the GD-training mechanism, which is common to both.

## [?] Uncertain items

- No web-resolvable [?] on this slide. A divider carries no verifiable claim.
- Frame-level [?]s that stay open by design (carried from `analysis/slide_035_final.json`,
  none web-resolvable): exact line-break position of the two-line title, exact font family and
  point sizes (only relative sizes derivable), exact border thickness and its inset from the
  slide edges, and whether the white cursor arrow belongs to the original slide design
  (kept in the brief for frame fidelity, unverifiable). Resolution path = build + zoomed crop
  judge per `shared_patterns/judge_protocol_03.md`, not web research.
- The title-vs-formulation scope mismatch noted above (linear-regression wording, perceptron
  formulation that follows) is recorded as a course-authored section label; resolution path =
  none needed (frame wins for recreation; no content is invented either way).

## Corrections

None. No dimension, attribute, or provenance guess in `analysis/slide_035_final.json` is
contradicted by any source (none was needed). No edit to any `analysis/*.json` was made by this
worker.

## Law reminder

The frame wins for recreation; the source wins for understanding.
