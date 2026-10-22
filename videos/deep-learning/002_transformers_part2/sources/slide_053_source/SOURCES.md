# SOURCES.md — 002 slide 053 "Self Attention Look Ahead Mask (Used in Decoder first Block)"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Machine-verified 2026-10-11 by the Part II
web-verification worker: vision transcript banked
(`transcripts/slide_053_vision_2026-10-11.txt`, default `images` route, one
probe, `--thinking high --max-tokens 65536`, via `scripts/16_vision_gate.sh`),
web research via `agy` + live fetches.

## Slide identity

- Video-2 (002_transformers_part2) curated slide **053** ← old extraction
  slide **133** (`unique_slides/new2old_mapping.json`), frame
  `unique_slides/slide_053.jpg` (kept from t≈4681 s; shown 4555–4680 s = 126
  frames, heavily taught), badge numeral 53.
- Content (banked vision transcript): title verbatim **"Self Attention Look
  Ahead Mask (Used in  Decoder first Block )"** (double space after "in",
  space before ")" — slide's own spacing). A 5×5 look-ahead-mask matrix over
  the SAME running French example as slide 052 — row labels (left, top→bottom)
  and rotated column headers: **SOS / Je / me / sens / malade**. Cell values:
  **0** on and below the diagonal (15 cells, light-green lower triangle),
  **−∞** above the diagonal (10 cells, brown/tan upper triangle). Right
  panel: red "Softmax" label over the boxed equation
  **σ(x_j) = e^(x_j) / Σ_i e^(x_i)**. Bottom callout (verbatim): "Mask Values
  are ADDED to Masked (Scaled) Values" / "Addition of "0" does not change the
  original values, consequently no effect on Softmax output" / "Addition of
  "-inf" gets "Zero" output of Softmax, leaving zero attention scores for
  future Words." A blue block-arrow points left→right into the row labels.

## Primary source — CONFIRMED (mechanism), paper verbatim

- **Paper**: "Attention Is All You Need" — Vaswani et al. 2017,
  arXiv:1706.03762v7. Both masking sentences verified live 2026-10-11 from
  https://arxiv.org/html/1706.03762v7 (HTML banked at `../scratch/paper_v7.html`):
  - §3.2.1: "We implement this inside of scaled dot-product attention by
    **masking out (setting to −∞) all values in the input of the softmax
    which correspond to illegal connections**." — exactly the slide's
    "ADDED … −∞ → Zero output of Softmax" callout and the −∞ cells.
  - §3.2.3.1 (decoder): "masking, combined with fact that the output
    embeddings are offset by one position, ensures that the **predictions
    for position i can depend only on the known outputs at positions less
    than i**." — exactly the slide's lower-triangular pattern (row i may
    attend to columns ≤ i; "future Words" get zero attention) and the title's
    "Used in Decoder first Block" (first decoder sub-layer = masked MHA,
    cf. slide 052 and §3.1).
  - §3.2.1 formula (also verified live): Attention(Q,K,V) =
    softmax(QKᵀ/√d_k)V — the mask matrix is ADDED inside the softmax input,
    matching the callout's "Mask Values are ADDED to Masked (Scaled) Values".
- **Softmax equation**: the boxed σ(x_j) = e^{x_j} / Σ_i e^{x_i} is the
  standard softmax definition — confirmed live against
  https://en.wikipedia.org/wiki/Softmax_function ("normalized exponential…
  converts a tuple of K real numbers into a probability distribution").
- No discrepancy between slide and paper. The slide's 0/−∞ matrix is the
  standard pedagogical rendering of the paper's mask matrix M.

## Figure identity — course-authored; nearest mechanism explainer identified

- The exact matrix cartoon (green token tiles, 0/−∞ chips, boxed softmax,
  callout box) is **course-authored in the deck's own style** — it continues
  slide 052's running example and styling ("SOS Je me sens malade" tokens;
  same green label tiles). No published figure matches the slide's own
  pixels/wording.
- **Nearest published explainer (agy-identified, verified via Wayback)**:
  Greg Mongaras, **"How Do Self-Attention Masks Work?"** (Medium, 2021),
  https://gmongaras.medium.com/how-do-self-attention-masks-work-72ed9382510f
  — live-verified 2026-10-11 via Wayback snapshot
  http://web.archive.org/web/20260227063434/https://gmongaras.medium.com/how-do-self-attention-masks-work-72ed9382510f
  (live site Cloudflare-blocks bots; snapshot archived 2026-02-27). It
  teaches the identical mechanism — "The look-ahead mask was originally used
  in the Attention is All You Need paper for the original transformer";
  mask matrix ADDED to the query-key matrix; "Softmax of the result from
  adding the query-key matrix to the mask matrix … is now all 0s and
  essentially doesn't affect the weights". **Its example sentence differs
  ("cómo estás <END>…")** — so it is a mechanism counterpart, NOT the slide's
  figure source. agy's first attempt on this query timed out (300 s proxy
  timeout); the retry surfaced this article and the link was independently
  resolved (302) and archived before citation.
- No figures downloaded for this slide: the slide does not reuse any
  published figure's pixels (course-authored rendering; the paper has no
  mask-matrix figure, and Mongaras' figures differ in example/labels).
  Reference URLs above serve as the ground-truth mechanism record.

## What the source CONFIRMS / CORRECTS

- CONFIRMED: −∞ masking added to the softmax input (§3.2.1); lower-triangular
  allowed pattern with position i attending only to ≤ i (§3.2.3.1); "0 added
  → no change" and "−∞ added → softmax zero" arithmetic; the softmax
  equation's standard form; the mask living in the DECODER's first
  (masked-MHA) sub-layer (§3.1/§3.2.3.1, and slide 052's stack).
- CORRECTED: nothing — no slide-vs-source disagreement found.
- Continuity note for the build: the row/column token order (SOS first) and
  the 5×5 size match slide 052's decoder column exactly — the two slides form
  one running example.

## [?] Open questions

1. Exact origin of the cartoon rendering: course-authored `[?]` (consistent
   with 052's finding; no confirming external figure). If the P4 pair
   (slides 054/055, verified next) continues this series, the same
   course-authored conclusion likely applies — recorded there when verified.
2. The tiny gray arrow near the matrix's upper-right (reads as a presenter
   cursor, not content) — intent `[?]` per the transcript.
3. Whether the instructor's "(Scaled) Values" refers to QKᵀ/√d_k (the
   paper's scaling) — almost certainly yes, but the slide does not draw the
   QKᵀ/√d_k step itself `[?]` (frame ground truth: only "Masked (Scaled)
   Values" wording).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what each slide shows; web
sources confirm/correct data and provenance, never license inventing content.
`[?]` markers are removed only with a confirming URL recorded here.

## Script-12 raw cross-check (2026-10-11, web-research verification worker)

Cross-checked against `analysis/slide_053_raw.json` (script-12 raw landed after
this record was written from the banked vision transcript).

- CONFIRMED by raw: title + subtitle verbatim ("Self Attention Look Ahead
  Mask" / "(Used in  Decoder first Block )" — raw preserves the double space
  after "in" and space before ")"); 5×5 matrix over SOS/Je/me/sens/malade
  (rows = query words, columns = key words) with 0 on/below the diagonal
  (15 cells) and −∞ above (10 cells), rows exactly SOS [0,−∞,−∞,−∞,−∞] …
  malade [0,0,0,0,0]; boxed softmax σ(x_j) = e^{x_j} / Σ_i e^{x_i} under a red
  "Softmax" label top-right; bottom statement box "Mask Values are ADDED to
  Masked (Scaled) Values" with ADDED underlined, plus both explanatory lines
  verbatim; blue block arrow pointing into the row labels; badge numeral 53;
  identity metadata (old extraction slide 133, kept frame_04681, shown
  4555–4680 s, 126 frames) — all match this record's Slide-identity and
  Primary-source sections. No source claims in this record are contradicted.
- STRENGTHENED: open question 2 (tiny gray arrow near the matrix's
  upper-right) — the raw independently reads it as "a mouse-cursor arrow
  (white with black outline, screen-recording overlay)" sitting on the
  matrix's right edge (~70% width / 52% height), i.e. frame ground truth
  itself classifies it as a recording artifact, not slide content. Treating
  it as non-content in the build is supported by the frame analysis; the
  formal `[?]` removal rule (confirming URL) does not apply to a
  frame-ground-truth artifact, so the marker is downgraded to
  "resolved-by-frame-ground-truth" for build purposes.
- New raw detail (no conflict, useful for the build): value colors —
  mint-green (#DCF5DC) lower triangle with dark-navy "0" chips, mauve
  (#A87C7C) upper triangle with red "−∞" chips, chips on light-yellow
  (#FFFFCC), badge yellow #FFFF99 with red "53"; softmax equation in italic
  serif (equation-editor style).
- No new published-figure claim appears in the raw (it describes a
  course-authored diagram; consistent with open question 1's course-authored
  finding — remains `[?]` with no external candidate to fetch).
- New `[?]` items: none. Corrections needed: none.

## Build-time frame corrections (2026-10-12, slide-053 recreation worker)

PIL pixel forensics during the recreation (scratch/slide053/measure*.py) corrected
several vision-extraction readings. Frame ground truth wins per the fidelity law;
recorded here per the disagreement rule:

1. **Subtitle color split** — the frame's line 2 is RED "(Used in  Decoder " + BLUE
   "first Block " + RED ")". The red/blue ink boundary sits at frame x 455|463, and an
   Arial-Bold advance fit (em 24.3) puts it exactly after "Decoder" (8.502 em).
   The earlier reading "blue = Decoder first Block" was a vision-model error.
2. **Statement box extent** — ONE blue-bordered box (frame x 64..878, y 417..507)
   contains ALL THREE text lines (left/right borders run continuously between the
   lines; bottom border rows 506..507). The extraction's "box + separate explanatory
   band" split was a layout error; the build draws one box.
3. **Upper-triangle mask cells** — each of the 10 masked cells is a SALMON chip
   (fill measured (227,170,138) = #E3AA8A; border + value (126,64,39) = #7E4027,
   chip ~23.0x17.8 pt) DISPLAYING a dark-red "−∞" value. Two earlier readings were
   both wrong at different levels: the extraction's "mauve field with red −∞ glyphs"
   (close, but the chip structure/fill color was not resolved) and the build worker's
   first-pass "solid red rectangles" (a red>55 mask read salmon fill + dark border +
   dark glyph as one solid red region; a full RGB dump showed the chip structure).
   The certified build renders chip + border + "−∞" per cell.
4. **Upper-triangle field color** — the mauve field between/around chips measures
   (196,172,160) = #C4ACA0 in wide inter-cell gaps (not the extraction's #A87C7C).
5. **Diagonal** — the green/mauve boundary (thin dark line) runs from frame
   (472, 201.5) to (676.5, 397.5): it starts ~27 px RIGHT of the matrix's top-left
   corner, NOT corner-to-corner as the extraction phrased it (green fills the
   top-left corner region).
6. **Title size** — advance fits give ~24.3 pt bold (extraction estimated ~28 pt);
   L1 ink 367.7 pt wide, L2 345.9 pt wide, both matching at 24.3 pt.
7. **Equation placement** — the softmax equation ink sits HIGH in its black box
   (top gap ~10 pt, bottom ~19 pt of the 75 pt box) in the frame itself; the
   recreation reproduces that measured placement (first crop-judge PASS run
   misread the original as centered; the PIL-facts retry PASSed).

Open questions 1 (course-authored cartoon) and 3 ("(Scaled)" wording) remain as
recorded above; open question 2 (cursor) was already resolved by frame ground truth.
No new source claims were needed for these corrections — they are frame-internal
measurements, not web-verifiable facts.
