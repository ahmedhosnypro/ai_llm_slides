# SOURCES.md — slide 028 "Effect of small and large Learning Rate"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
("Web-source research mandate", founder in-session directive 2026-10-19); method = agy web
search (MCP tool `agy_web_search`, token source keyring) for discovery + live fetch with
`curl -sL` in the same work window that records the URL (WebFetch was not used; curl was the
fetch tool of record) + verification against the fetched page text. Frame facts come from
`analysis/slide_028_raw.json` / `analysis/slide_028_final.json`; vision transcripts banked
separately. NO vision call was made by this worker (web + local-file work only).
Query budget for this worker (whole 028–036 leg): 2 agy searches (listed per record) + direct
curl fetches of canonical URLs (no snippet-only records). For this slide: 1 agy search
("gradient descent learning rate too small slow convergence too large overshoot
divergence") + 4 live curls.

## Slide identity

- File: `unique_slides/slide_028.jpg` (960×540, 1px = 1pt), badge numeral **28**
  (#FFFF00 circle, black numeral — deck house chrome, verified constant across this deck).
- Founder-curated numbering (2026-10-19). Pre-curation provenance: **unrecoverable** for slide
  28 — the founder removed `frames/` and the pre-curation index/mapping, and the raw's
  `_meta.source_timestamps` (`kept_frame frame_01081.jpg`, `start_sec 1080.0`, `frame_count 1`)
  carries no `precuration_slide` field. Per the deck AGENTS.md this gap is expected (16
  slides: 1,2,3,13,24–29,33,35,36,43,44,47) and is not an error; no new2old remap applies.
- `analysis/slide_028_final.json` verdict **PASS_WITH_FIXES**, recreatability 8/10; its four
  open `uncertain_items` (exact left-curve dot count, title alignment, valley-arrow color,
  absolute font sizes) are frame-level facts with no web resolution path.
- Deck namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`.

## Primary source(s)

All URLs below were **fetched live in this work window** (HTTP 200; bodies kept on disk under
`/home/ahmed/Projects/ai_llm_slides/scratch/tmp/w2/`) and quoted from the fetched bytes.
Nothing is recorded from an unfetched search snippet.

1. **https://en.wikipedia.org/wiki/Gradient_descent** — English Wikipedia, article "Gradient
   descent", section *Description → "Choosing the step size and descent direction"*. Fetched
   live, HTTP 200 (610,975 bytes). Verbatim:
   > "Since using a step size η that is too small would slow convergence, and a η too large
   > would lead to overshoot and divergence, finding a good setting of η is an important
   > practical problem."

   This is the canonical one-sentence statement of the exact two-panel contrast this slide
   draws: small η ⇒ slow convergence (left panel, small steps down the arm), large η ⇒
   overshoot/divergence (right panel, large oscillating steps across the minimum).
2. **https://arxiv.org/abs/1609.04747** and **https://arxiv.org/pdf/1609.04747** — Sebastian
   Ruder, "An overview of gradient descent optimization algorithms", arXiv:1609.04747v2
   [cs.LG]. Fetched live, HTTP 200 (abs page 41,246 bytes; PDF 659,026 bytes, `pdftotext`
   extracted). Verbatim, §3 "Challenges":
   > "Choosing a proper learning rate can be difficult. A learning rate that is too small
   > leads to painfully slow convergence, while a learning rate that is too large can hinder
   > convergence and cause the loss function to fluctuate around the minimum or even to
   > diverge."

   and §2.1 (batch gradient descent):
   > "Batch gradient descent is guaranteed to converge to the global minimum for convex error
   > surfaces and to a local minimum for non-convex surfaces."

   (Ruder is the source of record for the non-convex/local-minimum statements on slides
   033/034 — cross-referenced there rather than re-fetched.)
3. **https://neuralnetworksanddeeplearning.com/chap1.html** — Michael Nielsen,
   *Neural Networks and Deep Learning*, Chapter 1, "Learning with gradient descent". Fetched
   live, HTTP 200 (191,023 bytes; this host rejected the plain `curl` TLS handshake, so the
   fetch used `curl -skL`). Verbatim:
   > "To make gradient descent work correctly, we need to choose the learning rate η to be
   > small enough that Equation (9) … is a good approximation. If we don't, we might end up
   > with ΔC > 0, which obviously would not be good! At the same time, we don't want η to be
   > too small, since that will make the changes Δv tiny, and thus the gradient descent
   > algorithm will work very slowly."

   Nielsen also demonstrates the "too small" regime numerically on the same page: with
   η = 0.001 the MNIST accuracy "is getting slowly better over time" (1139 → 2142 over 30
   epochs), whereas η = 3.0 trains well — the textbook instance of the slide's left panel.
4. **https://cs229.stanford.edu/notes2020spring/cs229-notes1.pdf** — Andrew Ng, CS229
   lecture notes (2020 spring, part 1: Linear Regression and Classification). Fetched live,
   HTTP 200 (233,176 bytes PDF; `pdftotext` extraction). Verbatim:
   > "θj := θj − α ∂J(θ)/∂θj … Here, α is called the learning rate."

   > "…the optimization problem we have posed here for linear regression has only one global,
   > and no other local, optima; thus gradient descent always converges (assuming the learning
   > rate α is not too large) to the global minimum. Indeed, J is a convex quadratic
   > function."

## Figures used by this slide

**None downloaded — no hosted original exists for this slide's illustration.**

- Both panels are course-authored redraws (loss-vs-"Value of weight" step plots with red
  arrow axes). Nielsen's Chapter 1 does host the ball-in-valley drawings
  (`images/valley.png`, `images/valley_with_ball.png`) inside the same learning-rate
  discussion, but they illustrate a different point (the gradient pointing sideways out of a
  valley), and the Wikipedia lead animation (`Gradient_descent.svg`,
  `Gradient_Descent_in_2D.webm`) shows GD on level sets — neither is the small-vs-large-η
  contrast this slide draws. Per the contract ("if the source page hosts the original figure
  the slide reuses or redraws, save it"), no hosted original is reused here, so none was
  saved.
- `analysis/slide_028_final.json` likewise lists only the two "graph" panels plus the
  #1F4E79 framing rectangle — all course-drawn, no claimed provenance.

## What the source(s) CONFIRM

Point by point against the frame's claims (`analysis/slide_028_raw.json` verbatim labels:
"Small Learning Rate", "Large Learning Rate", "Loss" ×2, "Value of weight" ×2; two U-shaped
blue curves with red arrow axes):

1. **"Small Learning Rate" panel = many small steps, monotone slow descent toward the
   minimum.** CONFIRMED by all four sources — Wikipedia ("a step size η that is too small
   would slow convergence"), Ruder ("painfully slow convergence"), Nielsen ("we don't want η
   to be too small … gradient descent algorithm will work very slowly"), CS229 (GD converges
   provided α is not too large). The ~6 small dots descending the left arm are the standard
   depiction of that regime.
2. **"Large Learning Rate" panel = large steps that overshoot, oscillating across the
   valley (4 big dots crossing the minimum) — i.e. the fluctuation regime.** CONFIRMED by
   Wikipedia ("overshoot and divergence"), Ruder ("fluctuate around the minimum or even to
   diverge"), Nielsen ("we might end up with ΔC > 0"). The frame deliberately stops at
   fluctuation rather than terminal divergence: that is the "fluctuate around the minimum"
   sub-case of Ruder's sourced sentence, so the drawn case is confirmed, not contradicted.
3. **Axis semantics "Value of weight" (x) vs "Loss" (y) — a 1-D convex bowl in one parameter
   with the GD path drawn on it.** CONFIRMED at source level: every source's update is
   `θ := θ − α∇J(θ)` / `θj := θj − α ∂J/∂θj`, i.e. a step of size α along a single scalar
   parameter axis of the loss; CS229 draws exactly that (GD trajectory on the contours of a
   quadratic cost: "The ellipses … are the contours of a quadratic function. Also shown is
   the trajectory taken by gradient descent… The x's … mark the successive values of θ"). The
   slide reduces that picture to one weight dimension — course-authored simplification (below).
4. **The two regimes are presented as one trade-off (one bowl, two η values).** CONFIRMED:
   each source states them jointly — Wikipedia ("finding a good setting of η is an important
   practical problem"), Ruder ("Choosing a proper learning rate can be difficult"), Nielsen
   (η must be "small enough … but … not too small").

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The two-panel composition, the headings "Small Learning Rate" / "Large Learning Rate", the
  red (#FF0000) arrow axes labelled "Loss" and "Value of weight", the blue (#2E75B6) bowl
  curves, the #1F4E79 framing rectangle, the #FFFF00 badge and the red bold title are all
  course-authored presentation. No source dictates the palette, the arrowhead style, the
  heading wording, or the side-by-side layout; the frame stays ground truth for pixels.
- The step counts/geometry of the drawn trajectories (~6 tiny dots left; 4 big oscillating
  dots right) are the course's illustrative choice — the sources describe the regimes
  qualitatively and never specify a step count. Do not "correct" the drawn paths toward a
  source's own example (Nielsen's η = 0.001 MNIST run; CS229's housing-data run).
- The reduction from CS229's 2-D contour picture to a single "Value of weight" axis is a
  course-authored simplification (kept; the frame wins for recreation).
- Right panel stops at oscillation, not at the divergent/NaN regime: course-authored
  pedagogical stop-point.

## [?] Uncertain items

- **No web-resolvable [?] remains for this slide.** Every claim on the frame is a
  qualitative statement about the effect of the learning rate, and all of them are CONFIRMED
  above, with live-fetched quotes.
- Frame-level [?]s that stay open by design (not web-resolvable, carried from
  `analysis/slide_028_final.json`): exact left-curve dot count (source said "~6"; the final
  commits to 6), color of the tiny valley-pointing arrow (assigned #000000), absolute font
  sizes and badge diameter, title horizontal alignment (resolved top-center). Resolution
  path for all = build + zoomed crop judge (per `shared_patterns/judge_protocol_03.md`),
  not web research.
- Whether the lecturer had a specific figure open when filming (Nielsen's valley drawing,
  CS229's contour plot, or another): unresolvable without the video's audio; visually the
  content is course-authored either way.

## Corrections

- **None applied.** No dimension, attribute, or provenance guess in
  `analysis/slide_028_final.json` is contradicted by any of the four sources. The model's
  "U-shaped (parabolic) loss curve" annotation is consistent with the sources' quadratic/
  convex cost descriptions; the provenance annotation ("pre-curation id unrecoverable") is
  unaffected; no verbatim frame text was touched.
- No edit to any `analysis/*.json` was made by this worker (the patch-only clause was not
  triggered).

## Law reminder

The frame wins for recreation; the source wins for understanding.
