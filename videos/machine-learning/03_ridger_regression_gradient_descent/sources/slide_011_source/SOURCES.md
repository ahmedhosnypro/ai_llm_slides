# SOURCES.md — slide 011 "Example of Overfitting due to outlier in data"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search (MCP `agy_web_search`) + live `curl -sL` fetch of each URL in the same work window
that records it + independent local re-derivation of the deck's numbers. Frame facts come
from the slide's vision-analysis record (`analysis/slide_011_final.json`); NO vision calls
were made by this worker. **Query economy: 0 new queries spent on this slide** — every
claim it makes is covered by the cluster's shared primary sources, already fetched live
and banked for slides 010/012 (see cross-references below). The deck's second cluster
query ("overfitting caused by an outlier in regression data distorts the fitted model
parameters") was spent for this slide's topic area and its leads are evaluated below.

## Slide identity

- Frame file: `unique_slides/slide_011.jpg` (960×540, 1px = 1pt per the deck AGENTS).
- Badge number on the frame: **11** (yellow circle, black numeral). Deck rule: badge
  numeral = the file number N, no zero-padding.
- Numbering resolution: 51 founder-curated files numbered by the founder 2026-10-19; the
  pre-curation state is intentionally unrecoverable. A recovered pre-curation provenance
  value IS present in `_meta`: `source_timestamps.precuration_slide = 17` (kept frame
  `frame_00598.jpg`, t = 597 s, `provenance: "founder-curated kept frame"`). So this slide
  is one of the 35 with recovered provenance and is NOT in the 16-slide unrecoverable
  list. File number 011 and badge "11" agree; pre-curation 17 is historical only.
- Analysis record used: `analysis/slide_011_final.json` (verdict PASS_WITH_FIXES,
  recreatability 9). Raw not needed.

## Primary source(s)

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://en.wikipedia.org/wiki/Robust_regression` | Wikipedia article **"Robust regression"** — the canonical statement that ordinary least squares is highly sensitive to outliers and is dragged toward them. This is the source behind this slide's title claim. | **CONFIRMED** — fetched live 2026-10-20 in this work window: `curl -sL --max-time 60 -A "Mozilla/5.0" "https://en.wikipedia.org/w/index.php?title=Robust_regression&action=raw"` (22,500 bytes of wikitext). Quotes verbatim below. |
| `https://en.wikipedia.org/wiki/Overfitting` | Wikipedia article **"Overfitting"** — the definition of overfitting and the remedy list. | **CONFIRMED (origin-level)** — fetched live 2026-10-20 and banked with quotes in `sources/slide_010_source/SOURCES.md`. Same work window, same evidence trail; **no new query spent**. |
| `https://en.wikipedia.org/wiki/Outlier` | Wikipedia article **"Outlier"** — outlier detection/influence in regression, leverage and Cook's distance. | **CONFIRMED (origin-level)** — fetched live 2026-10-20 in this work window (`action=raw`, 28,734 bytes) and quoted in `sources/slide_012_source/SOURCES.md`. **No new query spent.** |

Nothing above was recorded from an unfetched search snippet. One on-topic lead from the
cluster's second search query was attempted and **NOT recorded as a source** because it
could not be fetched: `https://stats.stackexchange.com/questions/475517/relationship-between-overfitting-and-robustness-to-outliers`
returned a Cloudflare interstitial ("Just a moment…", 5,448 bytes of bot-challenge HTML,
no article content) on two fetch attempts. It is a LIVE page, not a dead or hallucinated
URL — recorded here as an attempt log / debt record so the orchestrator can decide
whether to bank it in the fleet map's do-not-reuse section (fetch-blocked, not
source-confirmed). No claim in this record depends on it.

## Figures used by this slide

**None — and correctly so.** This slide is a title-only slide (title + subtitle + badge);
it hosts no figure at all. The analysis record confirms: `imagery: []`,
`visual_elements` holds only the badge, and the recreation brief's step 6 forbids any
chart/imagery. The nearest hosted originals for the topic are the two "Overfitting"
article figures banked at `sources/slide_010_source/` (`Overfitting.svg`,
`Pyplot overfitting.png`) — reference-grade for the concept, and NOT this slide's content.
No download was made into this directory because there is no figure to download; per the
layout law the reason is stated here rather than left silent.

## What the source(s) CONFIRM

1. **The slide's headline claim — overfitting can be *caused by* an outlier in the data.**
   Source, verbatim (*Robust regression*, "Presence of outliers"):
   > "Another common situation in which robust estimation is used occurs when the data
   > contain outliers. In the presence of outliers that do not come from the same
   > data-generating process as the rest of the data, least squares estimation is
   > inefficient and can be biased. Because the least squares predictions are dragged
   > towards the outliers, and because the variance of the estimates is artificially
   > inflated, the result is that outliers can be masked."
   This is the source's own statement of the causal mechanism the slide announces.
2. **Why a single outlier distorts the fit (the squared-error amplification).** Verbatim
   (*Robust regression*, introduction):
   > "For example, least squares estimates for regression models are highly sensitive to
   > outliers: an outlier with twice the error magnitude of a typical observation
   > contributes four (two squared) times as much to the squared error loss, and therefore
   > has more leverage over the regression estimates."
   Confirms that the distortion comes from the L2/squared-error loss the deck has been
   building (slide 014's Loss Term `||Y − Ŷ||²`), and that it is a *leverage* effect on
   the estimate.
3. **The mechanism is a distortion of the model's parameters, not merely its residuals.**
   Verbatim (*Robust regression*): "…least squares estimation is inefficient and can be
   biased" and "the least squares predictions are dragged towards the outliers". This
   supports the deck's follow-on slide 012/013, whose numeric tables show the parameter
   vector W moving as the outlier grows — and this worker's independent re-derivation
   quantifies it exactly (see slide 013's SOURCES.md, "What the source(s) CONFIRM" §3).
4. **The parenthetical "and how to minimize overfitting" — the remedy direction.** Verbatim
   (*Overfitting*, *Remedy*):
   > "To lessen the chance or amount of overfitting, several techniques are available
   > (e.g., model comparison, cross-validation, regularization, early stopping, pruning,
   > Bayesian priors, or dropout)."
   The deck's answer to this slide's own question is regularization (slides 014 onwards), whose
   closed form is confirmed verbatim by the Ridge-regression article (slide 015's record).
5. **The outlier's special status as a data-point, not a feature.** Verbatim (*Outlier*):
   > "Mahalanobis distance and leverage are often used to detect outliers, especially in
   > the development of linear regression models."
   Confirms the deck's usage "x8 is Outlier" (a flagged training sample).

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The slide is a title-only divider: title "Example of Overfitting due to outlier in
  data" with the single word "outlier" underlined, and the italic blue parenthetical
  "(and how to minimize overfitting )" — including the space before the closing
  parenthesis, which the analysis record's own uncertain-items list flags as possibly an
  extraction artifact. It is kept verbatim either way (transcribed frame text).
- The red `#C00000` title color, blue `#0000FF` italic subtitle, yellow badge, and the
  empty top ~35% / lower ~45% bands (a deliberately sparse lecture divider layout).
- The mouse cursor near the bottom-left — a live-presentation capture artifact; the
  analysis record's recreation brief step 6 explicitly forbids reproducing it.
- The specific framing "due to outlier in data" + "(and how to minimize overfitting)" as
  a single lecture-divider slide: a course pedagogical choice, not a source's phrasing.
  Note the source's framing is broader (regularization/robust estimation against outliers
  AND against model complexity); the slide narrows it to the outlier case. The slide's
  narrowing is course-authored pedagogy — recorded, not "fixed" toward the source.
- The `#F0F0F0` background the vision record reports versus the deck's mandated white
  `FFFFFF` canvas: deck house-chrome law governs the recreation (see slide 010's record,
  course-authored section). Recorded only so the value is not mistaken for a source fact.

## [?] Uncertain items

| # | Item | Resolution path |
|---|---|---|
| 1 | Exact font point sizes (title ~36–40 pt, subtitle ~22–26 pt, badge ~14–18 pt) — builder estimates from the stated hierarchy | frame-only measurement; no source could supply a course slide's pt sizes |
| 2 | Exact badge diameter and its margin from the top/right edges (~0.4–0.5 in estimate) | frame-only measurement |
| 3 | Slide aspect ratio not stated in the JSON | resolved by deck law: `LAYOUT_WIDE` 13.33 × 7.5 in (AGENTS.md house chrome) — resolved by the deck's own binding rule, not a guess |
| 4 | Whether the badge circle has an outline/stroke | frame-only measurement (record assumes none) |
| 5 | Whether the space before `)` in "(and how to minimize overfitting )" is intended or an extraction artifact | frame-only; kept verbatim regardless (transcribed text is never "corrected") |

## Corrections

**None.** This slide carries no equations, no numeric values beyond the badge "11", no
matrix/dimension annotations and no provenance guesses. Nothing in the sources contradicts
any transcribed frame text. No analysis JSON was edited by this worker.

## Law reminder

The frame wins for recreation; the source wins for understanding. Discrepancies above are
recorded, never silently applied.
