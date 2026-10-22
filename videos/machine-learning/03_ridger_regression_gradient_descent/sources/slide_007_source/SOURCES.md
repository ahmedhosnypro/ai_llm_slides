# SOURCES.md — slide 007 "Problems of Linear Regression"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
("Web-source research mandate", founder in-session directive 2026-10-19). Method: agy web
search (MCP `agy_web_search`) for discovery + live `curl -sL --max-time 60 -A "Mozilla/5.0"`
fetch of each recorded URL in the same work window that records it. Fetch-tool note: the
WebFetch tool returned timeouts on these hosts earlier in the assignment, so `curl -sL` is
the fetch tool of record (same as the other records in this deck). Frame facts come from
`analysis/slide_007_final.json`; **no vision calls were made by this worker** — no
`scripts/16_vision_gate.sh`, no vision model. Query disclosure: this slide's four problem
claims each had their own academic anchor located by search this window; the
normal-equations / ridge / least-squares points are **no new query spent** because they were
already banked by my own `slide_003_source` and `slide_005_source` records (economy law).

## Slide identity

- Frame file: `unique_slides/slide_007.jpg` (960x540, 1px = 1pt per the deck AGENTS).
  Badge numeral on the frame: **7** (yellow circle, black numeral).
- Founder-curated numbering (2026-10-19). Recovered provenance from the analysis `_meta`
  only: `source_timestamps.precuration_slide = 8` (kept frame `frame_00372.jpg`, t = 371 s,
  `provenance: "founder-curated kept frame"`). Current file number 007 and badge "7" agree;
  8 is historical provenance only and is never used for the badge.
- Analysis record used: `analysis/slide_007_final.json` (verdict PASS_WITH_FIXES,
  recreatability 8/10).

## Primary source(s)

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Multicollinearity` | Wikipedia article **"Multicollinearity"** — *Perfect multicollinearity* (the exact-linear-relationship ⇒ `XᵀX` non-invertible result) and *Numerical issues* (ill-conditioning of `XᵀX`). | **CONFIRMED** — fetched live 2026-10-20 in this work window, HTTP 200, 212,205 bytes. |
| `https://en.wikipedia.org/wiki/Overfitting` | Wikipedia article **"Overfitting"** — definitional passage (*Statistical inference*), *Machine learning* section, and *Consequences*. | **CONFIRMED** — fetched live 2026-10-20, same window, HTTP 200, 268,330 bytes. |
| `https://psquare-lab.github.io/assets/pdf/EEC351/notes/PLA.pdf` | Course notes on the **Perceptron Learning Algorithm / linear separability** (Sasha Pshenychnyi / Berkeley EEC 151-style notes). Supplies the "many separating hyperplanes ⇒ select the best (max-margin)" argument. | **CONFIRMED** — fetched live 2026-10-20, same window, HTTP 200, `application/pdf`, 193,758 bytes (`pdftotext -layout` for quotes below). |

Origin-level cross-references (**no new query spent** — already located, fetched live, and
banked by my own earlier records; re-quoted here against this slide's specific claims):

| URL | Banked by | Used here for |
|---|---|---|
| `https://see.stanford.edu/materials/aimlcs229/cs229-notes1.pdf` (§2.2 normal equations; batch vs stochastic GD) | `slide_005_source` | The closed form `W = (XᵀX)⁻¹XᵀY` that a singular `XᵀX` blocks; and CS229's own statement that for large training sets an iterative (GD) method is preferred over the explicit inverse. |
| `https://en.wikipedia.org/wiki/Numerical_methods_for_linear_least_squares` (section *Inverting the matrix of the normal equations*) | `slide_003_source` | That solving/inverting the normal-equations matrix is the recognized cost and that the Gramian must be full-rank/well-conditioned. |
| `https://en.wikipedia.org/wiki/Ridge_regression` | `slide_003_source` / `slide_004_source` | The remedy the deck reaches for at slide 008 onward (L2 term makes the moment matrix full-rank); confirming *why* the singular-matrix problem motivates ridge. |

No snippet-derived URL is recorded; nothing above was banked from an unfetched search
snippet. No figure was downloaded (see next section).

## Figures used by this slide

None. The slide is a text box with an arrow-bulleted list (intro line + underlined section
header + four `➢` bullets) inside a white/blue-bordered rectangle. There are no charts,
diagrams, plots, or imagery. The source articles contain figures (e.g. the Multicollinearity
and Overfitting articles carry geometric illustrations), but none is a figure this slide
reuses or redraws, so nothing was copied into this directory. All layout particulars —
white `#FFFFFF` box, `#0000FF` border, `#0000FF` bold bullets with `#C00000` italic
parentheticals, the `➢` arrow glyph, the yellow `#FFFF00` badge — are course-authored chrome
and are recorded, not "sourced".

## What the source(s) CONFIRM

The slide lists **FOUR problems** of linear regression and one framing line. Each maps to a
fetched source:

1. **"Assume the Dataset is linearly separable (suitable to apply Linear regression
   model)"** (intro line) — CONFIRMED as a standard, well-defined notion. The PLA notes,
   verbatim (Figure 2 discussion): *"The data set on the left is linearly separable, whereas
   the data set on the right is not. [For the figure] on the left, we may draw a line such
   that all the points labeled [one class] lie to one side of the line, and all the points
   labeled [the other class] lie to the other side."* This is exactly the slide's stated
   premise.

2. **➢ "Overfitting Problem"** — CONFIRMED. Wikipedia *Overfitting*, verbatim:
   > "in mathematical modeling, overfitting is the production of an analysis that
   > corresponds too closely or exactly to a particular set of data and may therefore fail
   > to fit to additional data or predict future observations reliably."
   and, from the *Machine learning* section:
   > "overfitting occurs when a model begins to 'memorize' training data rather than
   > 'learning' to generalize from a trend."
   and *Consequences*: "The most obvious consequence of overfitting is poor performance on
   the validation dataset." The problem named on the slide is a recognized first-class
   failure mode of an unregularized fit.

3. **➢ "Matrix Inversion Problem [1] (Singular Matrix)"** — CONFIRMED, and in the source's
   own matrix notation. Wikipedia *Multicollinearity*, verbatim:
   > "If there is an exact linear relationship among the independent variables, then at
   > least one of the columns of X is a linear combination of the others, and so the rank of
   > X (and therefore of XᵀX) is less than k + 1, and the matrix XᵀX will not be
   > invertible."
   The same article writes the design matrix exactly as the deck does: an "N × (k+1) matrix,
   where N is the number of observations, k is the number of explanatory variables". Because
   slide 005 established the closed form `W = (XᵀX)⁻¹XᵀY`, a singular `XᵀX` (perfect
   multicollinearity) is precisely what breaks the solution — the source names the exact
   condition. The numerical-least-squares article corroborates the full-rank requirement:
   the normal equations are solvable in closed form only "with a full-rank matrix XᵀX".

4. **➢ "Matrix Inversion Problem [2] (Large Matrix dimension)"** — CONFIRMED as the cost of
   explicitly inverting the normal-equations matrix. Wikipedia *Numerical methods for linear
   least squares*, verbatim: *"this equation is correct and can work in many applications,
   it is not computationally efficient to invert the normal-equations matrix (the Gramian
   matrix)."* CS229 §2 likewise separates the explicit/closed-form ("normal equations")
   method from iterative minimization and notes "particularly when the training set is
   large, stochastic gradient descent is often preferred over batch gradient descent" — the
   documented reason the lecture turns to gradient descent next. The Multicollinearity
   article's *Numerical issues* section adds the stability half of the problem: for
   near-collinear columns "the matrix XᵀX has an inverse, but it is ill-conditioned … even
   if [an approximate inverse] can [be computed], the resulting inverse may have large
   rounding errors." (Frame note: the slide labels this "[2] Large Matrix dimension"; the
   sources frame the same inversion bottleneck as a computational-efficiency + numerical
   -stability concern as the Gramian grows. The mapping is faithful in substance; the exact
   `O(n³)` figure for a p×p inverse is a standard arithmetic fact and is not asserted here
   as if a fetched source stated it.)

5. **➢ "Different Hyperplanes can solve the problems (Selection of Best Hyperplane)"** —
   CONFIRMED. This is the payoff of the intro's "linearly separable" premise: when the data
   admits a separating hyperplane, there are many of them, so one must be chosen. The PLA
   notes, verbatim:
   > "we need not be satisfied with merely a separating hyperplane, but require one that
   > leaves a maximal gap with the training data points. Such 'maximum margin' classifiers
   > (for example, Support Vector Machines) can also be learned efficiently from data."
   (The extraction shows "train- ing"; the PDF line-break hyphenation was joined to "training"
   for the quote. No words were changed.) This confirms both halves of the bullet: that
   *different* hyperplanes can satisfy separability, and that the *selection* criterion is
   the maximum-margin / "best hyperplane" choice.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The entire layout: white `#FFFFFF` content box with a `#0000FF` border, intro + underlined
  header + four `➢`-bulleted lines, title "Problems of Linear Regression" in `#C00000`,
  yellow `#FFFF00` badge.
- The exact wording scheme: numbering the problems "[1]"/"[2]", the red `#C00000` italic
  parentheticals "(Singular Matrix)" / "(Large Matrix dimension)" / "(Selection of Best
  Hyperplane)", and the bare "Overfitting Problem" (no parenthetical).
- The slide's specific grouping of the failure modes into exactly **"FOUR problems"** and the
  ordering. The sources present overfitting, singular/ill-conditioned `XᵀX`, and hyperplane
  selection as related-but-distinct topics; bundling them as "the four problems of linear
  regression" under a linear-separability premise is the instructor's pedagogical framing,
  not a claim any single source makes verbatim.
- The concatenation under problem [2]: the sources discuss inversion *cost* and inversion
  *instability* separately; the slide's "Large Matrix dimension" folds both into one label.
- Chrome note (deck law, not a research finding): the vision record reports background
  `#F0F0F0`; this deck's measured house chrome (AGENTS.md) applies to the outer template and
  overrides per-slide analysis values. Recorded so no builder mistakes `#F0F0F0` for a source
  fact.

## [?] Uncertain items

| # | Item | Why still open |
|---|---|---|
| 1 | Exact hex of the intro line's "dark red/maroon" color (record suggests closest `#C00000`) | Frame-local typography detail; no source counterpart. Carried from the analysis record. |
| 2 | Exact underlined spans in the intro line ("linearly separable", "Linear regression model") | The analysis record itself marks this `[?]`; typography note only says "underlined key phrases". Frame-only. |
| 3 | Font family / point sizes / content-box border width | Frame-only measurements; not source-resolvable. |

None of the four *substantive* problem claims is `[?]` — all four are confirmed by the
fetched sources above. No `[?]` marker was removed here (this slide's analysis record carries
no `[?]` on the problem claims).

## Corrections

**None proposed.** The slide carries no equations, no numeric model values, no dimension
annotations, and no provenance guesses that a fetched source contradicts. The four problem
statements are conceptual labels, and each is corroborated (not corrected) by its source.
Per the mandate, corrections would patch model annotations only and never transcribed frame
text; nothing in the sources contradicts any frame text here, so no patch is made and no
analysis JSON was edited by this worker.

One *note for understanding only* (not a frame-text correction): the slide's problem "[2]
Large Matrix dimension" is best read through the sources as the general inversion bottleneck
of the normal equations (efficiency + numerical stability), which is why the lecture proceeds
to gradient descent. This is interpretive framing, recorded for understanding; the frame text
is reproduced verbatim for recreation regardless.

## Law reminder

The frame wins for recreation; the source wins for understanding. Discrepancies above are
recorded, never silently applied.
