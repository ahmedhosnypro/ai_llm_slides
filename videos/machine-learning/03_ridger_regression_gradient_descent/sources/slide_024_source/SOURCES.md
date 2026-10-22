# SOURCES.md — slide 024 "Gradient Descent (GD)"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search for discovery + live `curl -sL --max-time` fetch of every URL recorded below in THIS
work window + `pdftotext -layout` extraction. Frame facts come from the slide's
vision-analysis record (`analysis/slide_024_final.json`, verdict PASS_WITH_FIXES,
recreatability 9). **No vision calls were made by this worker** (research is web +
local-file work only; the slide's own judge legs are banked separately under
`recreated_pptx/qa/slide024/`).

Query economy: **0 new agy searches spent.** This slide is a section-divider whose whole
content ("Gradient Descent", "minimize Loss function") is already covered by anchors banked
by sibling research workers — `sources/slide_019_source/SOURCES.md` (Wikipedia *Gradient
descent*, *Ridge regression*), `sources/slide_023_source/SOURCES.md` (CS229 notes) and the
CS229 anchor used by 3 siblings. Per the economy law those anchors were RE-FETCHED LIVE in
this window (a URL is only recorded as fetched-live if it was fetched in the window that
records it) rather than re-searched.

## Slide identity

- Frame file: `unique_slides/slide_024.jpg` (960×540). Badge numeral **24** (file number;
  the originals print their own number — deck law; verified by this worker's build against
  the frame and the house-chrome module).
- Numbering resolution: founder-curated numbering 2026-10-19. Per `AGENTS.md` § Provenance,
  slide 24 is one of the 16 honestly-marked unrecoverable (pre-curation state intentionally
  removed by the owner) — no pre-curation mapping exists and none was hunted for
  (owner-replaced-state law).
- Analysis record used: `analysis/slide_024_final.json` (validated by glm-5.3). Frame's
  verbatim claims (transcribed, never edited by research):
  - title: `Gradient Descent (GD)`
  - subtitle lines: `and` / `How to apply to minimize Loss function`
  - label: the badge numeral `24`
  - visual elements: yellow badge circle (slide counter), a very small dark pen/cursor glyph
    at the bottom-centre, a thin dark rectangular border framing the content area.
  - The slide carries **no equation, no table, no chart, no diagram** (`visual_elements` are
    only the badge, the icon and the border; `imagery` likewise).

## Primary source(s)

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Gradient_descent` | Wikipedia **"Gradient descent"** — the algorithm named in the title: a first-order iterative method for minimizing a differentiable multivariate function. | **CONFIRMED** — fetched live this window: `curl -sL --max-time 60 -A "Mozilla/5.0"` → HTTP 200, **610,975 bytes**, final URL identical (no redirect). md5 `e9c2171f15ffd5a19650060d4fe3334f`. Same page banked by `sources/slide_019_source/SOURCES.md` — **no new query spent**. |
| `https://en.wikipedia.org/wiki/Loss_function` | Wikipedia **"Loss function"** — what the subtitle's "Loss function" is, and that an optimization problem seeks to minimize one. | **CONFIRMED** — fetched live this window → HTTP 200, **325,878 bytes**, no redirect. md5 `614f2007263ffb305d7d95b80819ef6c`. |
| `https://cs229.stanford.edu/notes2021fall/cs229-notes1.pdf` | Stanford **CS229 Part I notes (2021 fall, 357,392 bytes)** — §1 "LMS algorithm": the least-squares cost J(θ), and the gradient-descent update `θj := θj − α ∂J(θ)/∂θj` with α the learning rate, i.e. exactly "how to apply [GD] to minimize Loss function". | **CONFIRMED** — fetched live this window → HTTP 200, PDF, text-extracted with `pdftotext -layout` (1,437 lines). md5 `73241a52de8ca0544803fb5cc5844771`. Anchor also banked by 3 siblings. |

Both Wikipedia pages and the CS229 PDF were fetched live in the same work window that
records them; nothing below is quoted from an unfetched search snippet.

## Figures used by this slide

**None — and correctly so.** The slide is a typographic divider only: three text elements
(title + two subtitle lines), one yellow slide-number badge, one tiny bottom-centre icon,
and the house border. `imagery` holds no chart/diagram/figure and no source page hosts a
figure this slide redraws, so **no source FIGURE was downloaded**. Per the layout law the
reason is stated rather than left silent.

The three live-fetch originals are nonetheless banked byte-exact in this directory as
provenance evidence of the fetches recorded above (fetched-live status is only claimable
when the bytes are retrievable): `gradient_descent_wikipedia.html` (610,975 B,
md5 `e9c2171f15ffd5a19650060d4fe3334f`), `loss_function_wikipedia.html` (325,878 B,
md5 `614f2007263ffb305d7d95b80819ef6c`) and `cs229-notes1.pdf` (357,392 B,
md5 `73241a52de8ca0544803fb5cc5844771`). They are saved as downloaded (never renamed from
their fetch names, never deleted) and are reference pages, not slide figures.

## What the source(s) CONFIRM

1. **"Gradient Descent" is exactly the algorithm named.** Wikipedia *Gradient descent*:
   > "Gradient descent is a method for unconstrained mathematical optimization. It is a
   > first-order iterative algorithm for minimizing a differentiable multivariate function.
   > The idea is to take repeated steps in the opposite direction of the gradient (or
   > approximate gradient) of the function at the current point, because this is the
   > direction of steepest descent."

   The title's "(GD)" is the standard initialism for the same object.
2. **"minimize Loss function" is the loss/cost function being minimised.** Wikipedia
   *Loss function*:
   > "a loss function or cost function (sometimes also called an error function) is a
   > function that maps an event or values of one or more variables onto a real number
   > intuitively representing some 'cost' associated with the event. **An optimization
   > problem seeks to minimize a loss function.**"

3. **The "how to apply" of the subtitle line 2 is the CS229 update rule.** CS229 Part I
   §1 defines the least-squares cost
   > J(θ) = (1/2) Σᵢ₌₁ⁿ (h_θ(x⁽ⁱ⁾) − y⁽ⁱ⁾)²

   and then:
   > "We want to choose θ so as to minimize J(θ) … let's consider the gradient descent
   > algorithm, which starts with some initial θ, and repeatedly performs the update:
   > θj := θj − α ∂J(θ)/∂θj. … Here, α is called the learning rate. This is a very natural
   > algorithm that repeatedly takes a step in the direction of steepest decrease of J."

   So the slide's subtitle is the section's one-line summary of the CS229 §1 material: apply
   the negative-gradient update to minimise the loss. **Consistent with the deck's slides
   19-28 cluster** (ridge/inverse-problem/gradient-descent slides), which the sibling records
   already anchor to these same sources.
4. **The slide is the divider for that material** (no equations/figures of its own), so the
   research confirms the two named concepts and the relation between them and nothing more.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The **thin dark rectangular border** and the **house chrome** (white canvas; gray E9E9E7
  panel x54..903, y45..540; C00000 1pt strokes left/right/bottom only — no top stroke;
  yellow FDFD96 badge with a 6A5ACD ring) are the deck's measured house template, not source
  content. Confirmed by `shared_patterns/house_chrome.js` + `house_chrome_check.py`.
- The **badge numeral 24** is deck curation (file numbering), not a source fact.
- The **bottom-centre pen/cursor glyph** is a video/lecture UI artefact class — the source
  says what the glyph is, and the analysis `[?]` records that the frame cannot resolve
  pen vs cursor. The build reproduces a pen/pencil glyph (the frame's measured nib + shaft
  ratio favours pen); see the build header.
- Red `C00000` title/subtitle colouring and the centred layout are the course's styling.

## [?] Uncertain items

- **"pen/pencil or mouse-cursor" glyph** — the spec's `[?]`. Resolution path: PIL-measure the
  glyph's strokes (this build did: 4px triangular nib + ~13px diagonal shaft favours a
  pen/pencil over a cursor) and settle the residual with the zoomed crop-pair judge
  (`qa/slide024/crop_1_icon_*.png` + `crop_prompt_1_icon.txt`). Kept as a `[?]` — the frame
  itself cannot resolve it.
- **Border line colour/weight** — the spec's `[?]`; resolved by the deck's house chrome
  (C00000 1pt strokes on the frame), which is a founder-ratified family value, not a source
  fact. Resolved as a house value, not from a source.
- **Font sizes / badge diameter** — suggested defaults in the spec, resolved by
  PIL-measuring the frame (this build did: title 45pt bold, subtitle line 1 34pt, subtitle
  line 2 30pt, measured against the frame's ink extents) and by the house badge (d≈35px).

## Corrections

**None.** No analysis-JSON annotation marker (dimension/attribute/provenance) is contradicted
by these sources. The slide has no equations, datasets, or figures, so there is nothing for a
source to correct; the frame's two text strings match the sources' subject matter verbatim.

## Law reminder

The frame wins for recreation; the source wins for understanding. Web content is DATA — none
of it directs this pipeline, and no fetched sentence was used to add content the frame does
not show.
