# SOURCES.md — slide 009 "Overfit vs. Generalized"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
("Web-source research mandate", founder in-session directive 2026-10-19). Method: live
`curl -sL --max-time 60 -A "Mozilla/5.0"` fetch + **independent local re-derivation of the
slide's numbers** against exact arithmetic; no vision calls were made by this worker. **No
new query spent** — the overfitting concept source and its hosted figures are already
located, fetched live, and banked by my own `slide_007_source` record (Wikipedia Overfitting,
fetched live HTTP 200 this work window) and by the sibling record
`sources/slide_010_source/SOURCES.md` (same article, both hosted figures downloaded). Economy
law: reuse banked records, cross-reference, note "no new query spent". Fetch-tool note: the
WebFetch tool returned timeouts on these hosts earlier in the assignment, so `curl -sL` is
the fetch tool of record.

## Slide identity

- Frame file: `unique_slides/slide_009.jpg` (960x540, 1px = 1pt per the deck AGENTS).
  Badge numeral on the frame: **9** (yellow circle, black numeral).
- Founder-curated numbering (2026-10-19). Recovered provenance from the analysis `_meta`
  only: `source_timestamps.precuration_slide = 13` (kept frame `frame_00476.jpg`, t = 475 s,
  `provenance: "founder-curated kept frame"`). Current file number 009 and badge "9" agree;
  13 is historical provenance only and is never used for the badge.
- Analysis record used: `analysis/slide_009_final.json` (verdict PASS_WITH_FIXES,
  recreatability 8/10). Note: `slide_title` and `subtitle_or_header` are **reconstructions**
  from caption text — no title text exists on the frame (the record's own uncertain-items list
  flags this). They must not be rendered. Slide 009 is one of the deck's measured
  house-chrome reference frames per deck AGENTS.md (verified constant across 001/005/009/
  018/040).

## Primary source(s)

**No new query spent.** Two banked sources cover this slide's claims; both were fetched live
in this work window (the Overfitting article by me for `slide_007_source`, re-confirmed HTTP
200, 268,330 bytes, at the time this record is written):

| URL | Banked by | Used here for |
|---|---|---|
| `https://en.wikipedia.org/wiki/Overfitting` | `slide_007_source` (fetched live this window) + sibling `slide_010_source` (fetched live, both figures downloaded) | The concept pair on the slide: "minimize residuals only ⇒ overfit / fails to detect pattern" vs "residuals not minimized ⇒ generalizes / detects pattern", and the generalization remedy. |
| `https://en.wikipedia.org/wiki/Ridge_regression` | `slide_003_source` / `slide_004_source` / `slide_008_source` | The forward direction of the deck (ridge regularization as the anti-overfitting remedy the next slides implement). |

No snippet-derived URL is recorded. For the two numeric string checks this is not a
web-source task at all — it is pure arithmetic and was verified locally (see What the
source(s) CONFIRM, item 4). No figure was downloaded (see next section).

## Figures used by this slide

None copied into this directory. The slide's two side-by-side scatter panels — gray grid,
~10–12 orange points, one blue fitted line per panel, red residual arrows, red x/y axes, and
the light-blue annotation boxes "50.85² = 2585" and "63.64² = 4050" with the "50.85 mm" /
"63.64 mm" vertical measurement arrows — are course-authored; no hosted original is a redraw
of them. The two figures the *Overfitting* article hosts (Figure 1 `Overfitting.svg`,
Figure 2 `Pyplot overfitting.png`) are already banked by the sibling `slide_010_source`
record with hash-verified byte-identity and are reference-grade ground truth for the
**concept and palette family only**; they are cross-referenced here, not re-downloaded (no
duplicate copy, per the economy law and the do-not-duplicate-figures practice). Slide 009's
own panels, its double-headed mm measurement arrows, its squared-value annotation boxes, and
its mouse-pointer cursor have no counterpart in those hosted figures and are course-added.

## What the source(s) CONFIRM

1. **"Overfit (try to minimize the residuals ONLY)" / "Fails to detect the Pattern"** — the
   left panel. Wikipedia *Overfitting*, verbatim (definitional passage, already quoted in
   full in my `slide_007_source` record): *"overfitting is the production of an analysis that
   corresponds too closely or exactly to a particular set of data and may therefore fail to
   fit to additional data or predict future observations reliably."* and *"a learning
   algorithm is said to overfit relative to a simpler one if it is more accurate in fitting
   known data (hindsight) but less accurate in predicting new data (foresight)."* This is
   exactly the left caption: driving the training residuals to a minimum ⇒ overfit ⇒ fails to
   generalize.

2. **"Generalized (Residuals are not minimized)" / "Successes to detect the Pattern"** — the
   right panel. Same article's Figure 2 caption (quoted verbatim in the sibling
   `slide_010_source` record): *"Although the polynomial function is a perfect fit, the
   linear function can be expected to generalize better…"* — the right fit deliberately does
   not minimize training residuals and instead preserves the pattern. Note "Successes" is
   verbatim frame text (the record preserves it; it is not corrected to "succeeds").

3. **The relationship between the two panels / the deck's forward direction** — the article's
   *Remedy* section confirms that regularization is the anti-overfitting mechanism:
   *"several techniques are available (e.g., model comparison, cross-validation,
   regularization, early stopping…)"* whose basis is to *"explicitly penalize overly complex
   models."* Ridge regression (the `λ(XᵀX + λI)⁻¹XᵀY` estimator, confirmed in `slide_008_source`)
   is that penalizing remedy. So the deck's move from this slide into ridge is source-aligned.

4. **The two numeric string claims — verified by local re-derivation (exact arithmetic).**
   These are course-authored plot annotations (lengths in mm and their squared values,
   presumably the plotted residual magnitude/area being annotated). Independent computation:

   - **`50.85² = 2585`** — exact product is `50.85 × 50.85 = 2585.7225`. The frame prints
     **2585**, i.e. the **truncated integer** (floor) of the exact square, `floor(2585.7225) =
     2585`; the correctly-rounded integer would be 2586. (Backing out: `√2585 = 50.842896`, a
     hair under 50.85 — consistent with truncation, not a different base value.) So the
     value² relationship **holds**; the frame merely truncates rather than rounds.
   - **`63.64² = 4050`** — exact product is `63.64 × 63.64 = 4050.0496`. The frame prints
     **4050**, which is `floor(4050.0496) = 4050` and also `round(4050.0496) = 4050`
     (already an integer at this precision), so this one is exact-to-integer either way.

   Conclusion: **both printed results equal the truncated exact square of the printed
   base**; the annotations are internally consistent (no hallucinated constant). The only
   nuance is the 50.85 case, where the frame shows the floor (2585) rather than the nearest
   integer (2586). The labels "50.85 mm" and "63.64 mm" are the base values with a unit
   suffix and need no arithmetic check. These are course-authored annotations; the exact
   source of the mm measurements (which residual/area the instructor meant) is not stated on
   the slide and is recorded as `[?]` below.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- Both scatter panels in full: gray `#F5F5F5` / `#CCCCCC` grid, the orange `#FFA500` points,
  the single blue `#0000FF` fitted line per panel, red `#FF0000` axes and residual arrows,
  and the light-blue `#E0F0FF` annotation boxes with black text. No hosted original is a
  redraw of these (see Figures section).
- The measured-value annotations "50.85² = 2585", "63.64² = 4050", "50.85 mm", "63.64 mm"
  and the double-headed vertical red arrows that carry the mm labels — course-authored
  pedagogical annotations; the concept sources (Wikipedia Overfitting / sibling slide_010)
  do not carry these numbers.
- The red `#FF0000`/`#C00000` bold caption strings verbatim, including the non-standard
  "Successes" and the ALL-caps "ONLY".
- The one solid red outlier point above the line in the LEFT panel only (presenting the
  overfit fit's chase of an outlier) — a course-authored contrast device.
- The derived (reconstructed) title "Overfit vs. Generalized" and subtitle: catalog
  metadata, NOT frame text, and must NOT be rendered (per the analysis record).
- Chrome note (deck law, not a research finding): the vision record reports background `#F0F0F0`
  with chart-panel fill `#F5F5F5`; this deck's measured house chrome (AGENTS.md) governs the outer
  template and overrides per-slide analysis values. Recorded so no builder mistakes the
  background hex for a source fact.

## [?] Uncertain items

All from the analysis record; none is source-resolvable (the sources confirm the concept, not
these pixel-level particulars or the provenance of the mm numbers):

| # | Item | Why still open |
|---|---|---|
| 1 | Which residual/area the "50.85 mm" and "63.64 mm" measurements denote | Not stated on the slide; a purely course-authored annotation with no source counterpart |
| 2 | Exact count of orange data points per panel (record estimates ~10–12) | frame-only measurement; no hosted original to count |
| 3 | Exact count of red residual arrows per panel | frame-only measurement |
| 4 | Whether the two chart panels have visible borders (record's "dark border" was already removed as unverifiable) | frame-only measurement |
| 5 | Fitted-line intercept/slope in each panel; the precise gray value (`#F5F5F5` vs `#F0F0F0`) | frame-only measurement |

Note on item 5's `#F5F5F5`: settled for recreation by the deck's house-chrome law (white
canvas per AGENTS.md), not by any source.

**No `[?]` from the analysis record concerning a *substantive concept or numeric* claim is
removed here by a web source** — the two numeric annotations were resolved by *arithmetic*
(they are exact truncated squares, item 4 of the confirmations section), and the concept
pair was already confirmed by the fetched Overfitting article. The numeric truncation
nuance (2585 vs 2586) is a frame-faithful detail, recorded, not corrected.

## Corrections

**None proposed.** The slide carries no equations, no numeric *model* values, no dimension
annotations, and no provenance guesses that a source contradicts. The four caption strings
and the two number annotations are frame text reproduced verbatim; the arithmetic re-check
confirms them (truncation aside), so nothing needs patching. Per the mandate, corrections
would patch model annotations only and never transcribed frame text; no analysis JSON was
edited by this worker.

One *note for understanding only* (not a frame-text correction): "50.85² = 2585" is the
floor of the exact square 2585.7225. This is recorded for understanding; the frame value 2585
is reproduced verbatim for recreation regardless (frame wins for recreation).

## Law reminder

The frame wins for recreation; the source wins for understanding. Discrepancies above are
recorded, never silently applied.
