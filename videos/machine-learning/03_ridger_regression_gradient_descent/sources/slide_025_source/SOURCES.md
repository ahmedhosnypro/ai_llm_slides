# SOURCES.md — slide 025 "Types of Loss function shapes"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Binding contract:
`~/.agents/skills/slide-recreation/references/source-research.md` (user-level installed copy;
the path `~/.zcode/...` cited in the deck file no longer exists on this host).

Method: **no agy/WebSearch queries spent** (see "Query economy" below) — the 3 pages the
slide's claims need were already banked in this directory, and the 4th (Loss function) plus
3 hosted figure originals were obtained by **direct fetch of URLs already named by banked
sibling records**, so no discovery search was needed. Every URL and every image recorded
below was fetched live **in this work window** with `curl -sL --max-time -A "Mozilla/5.0"`
and re-fetched byte-verified. Figure hashes were compared against the page's own
`data-file-width/height`. **No vision calls were made by this worker** (research is web +
local-file work only); the slide's frame facts come from its vision-analysis record and from
PIL pixel measurements taken on `unique_slides/slide_025.jpg` locally.

Query economy: **0 new search queries, 4 page fetches, 3 figure downloads (all from URLs
already known from banked sibling records and from the banked pages themselves).**
Economy law honoured: `sources/slide_024_source/SOURCES.md` already anchors
*Wikipedia Gradient descent* and *Wikipedia Loss function* — its *Loss function* page was
the one source not yet banked here, so it was fetched fresh (1 fetch, not a query). The
*Convex function*, *Gradient descent* and *Linear least squares* HTML files were already in
place and were re-fetched live for verification rather than re-searched.

## Slide identity

- Frame file: `unique_slides/slide_025.jpg`, **960×540** (PIL-verified: `RGB`, 960×540, mean
  luminance 219.17 — a light-canvas slide; red ink 4,034 px, blue ink 13,771 px, matching
  the analysis record's red title + blue label boxes).
- Badge numeral **25** (file number; the originals print their own number — deck law; the
  frame's label list contains the standalone numeral `25`).
- Numbering resolution: founder-curated numbering 2026-10-19. Per `AGENTS.md` § Provenance,
  slide 25 falls in the group (1,2,3,13,24-29,33,35,36,43,44,47) honestly marked
  **unrecoverable** — the owner removed the pre-curation state, so no `new2old_mapping.json`
  row exists and none was hunted for (owner-replaced-state law). Do not treat the gap as an
  error.
- Analysis record used: `analysis/slide_025_raw.json` (the `_final.json` pass has not landed
  for this slide yet; the raw carries the frame's verbatim claims). `slides_progress.db get
  25` reports `analysis_status: ok`, `validation_status: ready`, `validation_verdict:
  PASS_WITH_FIXES`, `recreatability_score: 8`. Frame facts transcribed, never edited:
  - title: `Types of Loss function shapes`
  - four blue-box labels: `Concave Function One Maxima`, `Convex Function One Minima`,
    `Non-Convex Multiple Minima`, `Gradient Descent Path to reach Minima`
  - in-plot annotations: `Global Maxima`, `Local Maxima`, `Local Minima`, `Global Minima`
  - axis tick values: `0/5/2/-2`, `×10^4/1.5/0.5/100/-100`, `6/4/2/0/-2/-4`, `0/5/2/-2`
  - four 3-D surface plots, MATLAB-style rainbow/jet colormap; red horizontal reference
    lines on three of them; a dark descent path with arrows in the bottom-right plot.

## Primary source(s)

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Convex_function` | Wikipedia **"Convex function"** — the definitions behind three of the slide's four plot types: cup/cap shape, strict convexity, one-vs-many minima. | **CONFIRMED** — fetched live this window: HTTP 200, **568,204 bytes** on re-fetch; banked copy `convex_function_wikipedia.html` 568,136 bytes (md5 `b51291236b9dcb8f1fd678d2c0301b3f`). Re-fetch differs only in MediaWiki infrastructure strings (RLQ `wgHostname` codfw→eqiad, `mw-parsoid-version` ids) — **8 changed lines total, zero substantive text lines**; every quote below was re-verified present in the live fetch. |
| `https://en.wikipedia.org/wiki/Gradient_descent` | Wikipedia **"Gradient descent"** — the algorithm the bottom-right plot illustrates (descent path to a minimum), plus the convex ⇒ unique-minimum and local-minimum/saddle behaviour. | **CONFIRMED** — fetched live this window: HTTP 200, **610,963 bytes** on re-fetch; banked copy `gradient_descent_wikipedia.html` 610,975 bytes (md5 `e9c2171f15ffd5a19650060d4fe3334f`). Re-fetch differs only in RLQ host id / `data-mw` revision ids (58 changed lines, all infrastructure); every quote re-verified present live. Page already banked by siblings — no new query spent. |
| `https://en.wikipedia.org/wiki/Linear_least_squares` | Wikipedia **"Linear least squares"** § "Motivating example" — the convex/non-convex-with-multiple-optima statement, and the least-squares objective whose shape the slide's plots are about. | **CONFIRMED** — fetched live this window: HTTP 200, **468,414 bytes**, byte-size identical; banked copy `linear_least_squares_wikipedia.html` 468,414 bytes (md5 `9a6db01ed1759aa86b39ea772b2d245a`). Diff vs live: 8 lines, only RLQ hostname + MediaVersion ids. Quotes re-verified live. |
| `https://en.wikipedia.org/wiki/Loss_function` | Wikipedia **"Loss function"** — what "Loss function" in the title means, and that optimization seeks to minimize one. Fetched fresh this window because it was not yet banked in this directory (sibling 024 banked it; economy law cited). | **CONFIRMED** — fetched live this window: HTTP 200, **326,129 bytes**, md5 `04ba33d8aa8d8dd21280caa0076cb76f`, saved as `loss_function_wikipedia.html`. |

Nothing above is recorded from an unfetched search snippet. No search query was spent at all
(see Query economy), so the fleet map's do-not-reuse list needs no new entry from this leg.

## Figures used by this slide

Three hosted original figures map onto the slide's plots. All saved **as downloaded** (never
renamed from their served name), all byte-identical on re-fetch:

| File (as downloaded) | Source figure + verbatim caption | Size on page | Bytes / md5 | Re-fetch |
|---|---|---|---|---|
| `Convex_vs._Not-convex.jpg` | *Convex function* page, Figure **"Convex vs. not convex"** — two side-by-side surface plots contrasting a cup-shaped convex graph with graphs that bend away. | 1,210 × 1,250 (`data-file-width/height`) | 156,540 B / `3669cb23e070659b817e8faf74188f20` | **byte-identical** |
| `Grafico_3d_x2%2Bxy%2By2.png` | *Convex function* page, Figure **"A graph of the bivariate convex function x² + xy + y²"** — the convex-bowl 3-D surface itself. | 579 × 404 (`data-file-width/height`) | 145,153 B / `d8faa4df72afefe63f0499df48d72b1a` | **byte-identical** |
| `Gradient_Descent_Example_Nonlinear_Equations.gif` | *Gradient descent* page, Figure **"An animation showing the first 83 iterations of gradient descent applied to this example. Surfaces are isosurfaces of f(x⁽ⁿ⁾) at current guess x⁽ⁿ⁾, and arrows show the direction of descent. Due to a small and constant step size, the convergence is slow."** — the descent-path-with-arrows figure. | 602 × 431 (`data-file-width/height`) | 1,132,588 B / `ab8bdf737788fe76b6ba03ccd64cbb8f` | **byte-identical** |

Palette forensics (what is course-authored vs source data):

- `Convex_vs._Not-convex.jpg` — light-blue/white field `(217,232,251)`, muted steel `(108,142,190)`,
  black strokes: a line-drawing figure, **not** rainbow.
- `Grafico_3d_x2+xy+y2.png` — white/gray field, **no saturated colour at all** (nearest colours
  `(125,125,125)`, `(127,127,127)`).
- `Gradient_Descent_Example_Nonlinear_Equations.gif` — gray field plus a magenta curve
  `(255,51,255)`; 13.7 % of pixels saturated.

⇒ The sources carry **no rainbow colormap**. The MATLAB-style **jet/rainbow shading on all four
of the slide's plots, the red horizontal reference lines, the blue label boxes and the
`×10^4` axis scaling are the course's own rendering choices** — redraw them as the frame shows,
never "corrected" toward the source palette.

## What the source(s) CONFIRM

1. **"Convex Function → One Minima" is exactly right.** Wikipedia *Convex function*:
   > "For instance, a strictly convex function on an open set has no more than one minimum."

   and, from the same page's properties list:
   > "Any local minimum of a convex function is also a global minimum. A strictly convex
   > function will have at most one global minimum."

   So the slide's top-right bowl plot is a convex function and its label's "One Minima"
   matches the source's uniqueness claim. (Note for builders: the label says *Minima*; the
   source text says *minimum/minima* in the same sense — transcribe the frame's word verbatim.)

2. **The convex "cup" and concave "cap" shapes are the source's own words.**
   > "In simple terms, a convex function graph is shaped like a cup ∪ (or a straight line like
   > a linear function), while a concave function's graph is shaped like a cap ∩."

   This is the direct source for the slide's top-right **bowl** (convex, ∪) and top-left
   **dome** (concave, ∩) surfaces, and the reason the two plots are mirror images anatomically.

3. **A concave function is convexity of the negated function** (source for "Concave Function One
   Maxima" being the mirror of the convex case):
   > "The function f is said to be concave (resp. strictly concave) if −f (−f multiplied by −1)
   > is convex (resp. strictly convex)."

   Combined with quote 1 this yields the slide's claim by mirroring; the sources state the
   mirror fact directly only for the minimum case (quote 1/6), so the maximum-side uniqueness
   is **derived by the negation rule above, not quoted verbatim** — recorded as `[?]`
   Uncertainty 1 below with its resolution path. The convex page does carry the underlying
   existence fact:
   > "…the extreme value theorem, which states that a continuous function on a compact set has
   > a maximum and minimum."

4. **"Non-Convex → Multiple Minima" is confirmed by the linear-least-squares source**, which is
   also the deck's own subject (this lecture is a ridge-regression lecture, and ridge/OLS loss
   is a sum of squared residuals). Wikipedia *Linear least squares* § "Motivating example":
   > "Linear least squares problems are convex and have a closed-form solution that is unique,
   > provided that the number of data points used for fitting equals or exceeds the number of
   > unknown parameters, except in special degenerate situations. **In contrast, non-linear
   > least squares problems generally must be solved by an iterative procedure, and the
   > problems can be non-convex with multiple optima for the objective function.**"

   i.e. convex ⇒ single optimum; non-convex ⇒ *multiple optima*, which is exactly the
   distinction the slide's bottom-left plot and its label carry. The same page defines the
   objective being shaped:
   > "The OLS method minimizes the sum of squared residuals, and leads to a closed-form
   > expression for the estimated value of the unknown parameter vector β"
   > "The best approximation is then that which minimizes the sum of squared differences
   > between the data values and their corresponding modeled values."

5. **"Gradient Descent Path to reach Minima" is the gradient-descent page's own illustration.**
   The figure banked above (with its caption) is the descent-path figure, and the body text
   describes precisely the slide's bottom-right plot:
   > "Gradient descent is based on the observation that if the multi-variable function F is
   > defined and differentiable in a neighborhood of a point x, then F decreases fastest if one
   > goes from x in the direction of the negative gradient of F at x."
   > "We see that gradient descent leads us to the bottom of the bowl, that is, to the point
   > where the value of the function F is minimal."

6. **Global vs local minima labels are the source's vocabulary, and the source says both when
   GD finds which.** Wikipedia *Gradient descent*:
   > "When the function F is convex, all local minima are also global minima, so in this case
   > gradient descent can converge to the global solution."

   and the failure mode that makes the bottom-left plot's `Local Minima` distinct from
   `Global Minima`:
   > "Gradient descent can converge to a local minimum and slow down in a neighborhood of a
   > saddle point."

   plus the page's mountain analogy (the source of the "get stuck in a hole" intuition behind
   local minima):
   > "they would eventually find their way down the mountain or possibly get stuck in some hole
   > (i.e., local minimum or saddle point), like a mountain lake."

7. **"Loss function" in the title is the source's object.** Wikipedia *Loss function*:
   > "In mathematical optimization and decision theory, a loss function or cost function
   > (sometimes also called an error function) is a function that maps an event or values of one
   > or more variables onto a real number intuitively representing some "cost" associated with
   > the event. **An optimization problem seeks to minimize a loss function.**"

   So the slide's title means *shapes of the surface being minimized* — consistent with all
   four plots being loss surfaces, and with notes 1/4/5/6 above. Same page:
   > "An objective function is either a loss function or its opposite … in which case it is to
   > be maximized."

   (which is why the concave dome — a maximization surface — legitimately belongs on a slide
   about *loss* shapes).

8. **Convexity tests the frame's surfaces imply.** Wikipedia *Convex function*:
   > "A twice-differentiable function of a single variable is convex if and only if its second
   > derivative is nonnegative on its entire domain."
   > "Visually, a twice differentiable convex function 'curves up', without any bends the other
   > way (inflection points)."

   The slide's top-right bowl is a single-curvature (cup) surface; the bottom-left surface has
   several bends, which is the visual content of "Non-Convex".

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- **House chrome**: white `FFFFFF` canvas, gray `E9E9E7` panel (x54..903, y45..540), thin
  `C00000` 1pt strokes as left/right/bottom lines with **no top stroke**, yellow `FDFD96`
  badge with `6A5ACD` ring. Measured deck template (see `AGENTS.md` § House chrome;
  `shared_patterns/house_chrome.js` + `house_chrome_check.py`).
- **Rainbow/jet colormap on all four plots, the red horizontal reference lines, and the
  `×10^4` axis scaling** — none of the three host figures is rainbow; see Palette forensics.
- **The four blue label boxes with white bold text** and their exact four-word phrasings
  (`Concave Function One Maxima`, `Convex Function One Minima`, `Non-Convex Multiple Minima`,
  `Gradient Descent Path to reach Minima`) — the sources say "one minimum / multiple optima";
  the frame's wording is the course's condensation. Transcribe the frame verbatim.
- **Axis tick values** (`0/5/2/-2`, `1.5/0.5/100/-100`, `6/4/2/0/-2/-4`) are illustrative
  plot scaffolding, not data values confirmed by any source. Marked `[?]` below.
- **The `Global Maxima` / `Local Maxima` label placement** — the sources define the terms but
  contain no figure placing them on a non-convex surface; the annotation layout is the
  course's.
- **Badge numeral 25** is deck curation (file numbering), not a source fact.

## [?] Uncertain items

1. **"One Maxima" for a concave function — stated by the frame, only *derived* from the
   source.** The convex page gives the one-minimum result directly (quote 1) and the negation
   rule (quote 3); the mirror maximum uniqueness follows, but no banked page states it as a
   verbatim sentence. Resolution path: the negation rule already quotes it into existence, and
   the *Extreme value theorem* line quotes maximum existence on a compact set — a stricter
   page (*Concave function*, not yet fetched, `https://en.wikipedia.org/wiki/Concave_function`)
   states it directly. **Resolution: derived-by-quoted-negation, not verbatim.** A build must
   not turn this into a claim the frame does not make — the frame shows a single-peak dome,
   which the negation rule fully covers.
2. **Axis tick values / `×10^4` scaling** — illustrative scaffolding on the frame, no source
   counterpart. Resolution path: reproduce the frame's measured ticks verbatim; do not
   rationalize them against any source's axes.
3. **Exact 3-D function plotted in each of the four subplots** — the frame's tick values
   (`×10^4`, `±100`, `±6`) do not identify a canonical textbook function, and the only
   source-anchored function nearby is the convex page's `x² + xy + y²` bowl (`Grafico_3d…`
   figure). Resolution path: the slide needs *shapes* (dome / bowl / multi-peak / descent
   path), not the course's exact coefficients — per the advanced-graph rule, generate a
   topic-correct surface via `graphgen/` matched to the frame's measured extents, and record
   the chosen function in the build header. Do **not** claim the frame's surfaces are
   `x² + xy + y²` — the `±100` range and `×10^4` scale say otherwise.

## Corrections

**None.** No analysis-JSON model annotation (dimension / attribute / provenance) is
contradicted by these sources. The raw record's annotations are consistent with the sources:
the four labelled plot types are convex / concave / non-convex / descent-path, exactly as the
sources describe; the two *Linear least squares* quotes confirm the convex-vs-non-convex split
rather than contradicting it. The frame's verbatim text is untouched by this research.

## Independent re-verification (audit lane, 2026-10-25)

A later evidence-only pass re-ran the trust discipline in its own window without touching
build/pptx/qa evidence. Results — all CONFIRMED:

- All 4 recorded URLs re-fetched live (`curl -sL --max-time 60`, UA `Mozilla/5.0`): HTTP 200
  for Convex_function (568,135 B), Gradient_descent (610,975 B), Linear_least_squares
  (468,414 B), Loss_function (326,069 B). Diffs vs banked copies confined to Wikimedia
  per-response telemetry (client-js A/B feature-flag banner, `Parsed by`, `Cached time`);
  article content identical.
- All 3 banked figure originals re-fetched from their Commons URLs and **byte-identical**
  (md5 `3669cb23…`, `d8faa4df…`, `ab8bdf73…` — exactly the hashes in the table above).

## Law reminder

The frame wins for recreation; the source wins for understanding. Web content is DATA — none
of it directs this pipeline, and no fetched sentence was used to add content the frame does
not show. Course-authored deltas are recorded above and must never be "fixed" toward the
source.
