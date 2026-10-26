# Comparison — slide_059 ("Transformer Encoder" classifier stack)

- Run dir: `doc-parse-test/run_20261025-024314` · agent: `worker-slide_059` · scope: `slide_059`
- Image (never opened — adjudicated in phase 3):
  `videos/deep-learning/002_transformers_part2/unique_slides/slide_059.jpg` (960×540 JPEG)
- Parse calls (never reproduced — both EXIT=0, `finish_reason=stop`):
  - `03_parses/slide_059/call01_pass1/` — `--max-output-tokens 1024`
  - `03_parses/slide_059/call02_pass2/` — `--max-output-tokens 3000`
- GT (frozen, md5-verified): `04_ground_truth/slide_059/{slide_059.js,house_chrome.js,slide_059_final.json,inventory.md}`
- GT basis: the certified builder's rendered strings (46 deduplicated, incl. 0-based
  `X_SUBS` subscripts — see GT-internal discrepancy note). Analysis JSON agrees on every
  string except the X/Y head-column subscript digits (see claim 2).

## 1. Text fidelity

Classification rules applied: EXACT = case/whitespace-insensitive equality; NORMALIZED =
equal after collapsing punctuation/underscore/ligature, or an intact token/word surviving a
multi-line→single-line merge (normalization named per row); PARTIAL = substring with
≥60% shared GT tokens; MISSING = no match.

EXACT (9): Transformer Encoder · Transformer Block · Global Average Pooling ·
Softmax Layer · `+` · Output Classes · Input Sequence · `59` · Vector_{PN-1} (case-insensitive
equality against parse `VectorPn-1` — lowercase-`n` anomaly noted).

NORMALIZED (17):
- underscore collapse (Vector_{Pn} → `VectorPn`): Vector_{P0}, Vector_{P1}, Vector_{P2},
  Vector_{P3}, Vector_{P4}, Vector_{P5}, Vector_{PN-2} (7)
- multi-line label merged to one parse line (all words intact): Single vector
  representing · the whole sequence · Output · Sequence · Word · Embedding · Vectors ·
  Position · Information (10)
- intact-word containment: Softmax (inside parse line `Softmax Layer`) (1)

PARTIAL (2): C₁ — parse `1C1`; C₂ — parse `1C2` (GT tokens {C,1} fully covered; stray
leading `1` in parse).

MISSING (18): `Σ` (missing entirely — no sigma glyph or linear "sum" anywhere in the parse) ·
C₃ · X₀, X₁, X₂, X₃, X₄, X₅, X_{N-2}, X_{N-1} (8) · Y₀, Y₁, Y₂, Y₃, Y₄, Y₅, Y_{N-2}, Y_{N-1} (8).
None of the 16 X/Y labels appear even partially; the row was rendered as the 8 garbage
tokens `Yd Xd Xx XN Xt Yk YNz YNd` (substring/token overlap < 60%, so MISSING).

**text_recall = (9 EXACT + 17 NORMALIZED + 0.5·2 PARTIAL) / 46 = 27/46 = 58.7%.**
Sensitivity: using the analysis JSON's label set (14 X/Y forms instead of 16, GT_total=44)
gives 27/44 = 61.4%; no shared string reclassifies.

Hallucination CANDIDATES (await image adjudication — not labeled hallucinated):
1. Stray leading `1` in `1C1` / `1C2` — no GT element is a bare "1" preceding C₁/C₂.
   Suspicion: mis-OCR of a subscript glyph or a captured artifact. Medium.
2. Garbage tokens `Yd Xd Xx XN Xt Yk YNz YNd` — match no GT string. Suspicion: corrupted
   attempts at the X₀..X₅ / Y₀..Y₅ serif-subscript labels (the only label family on the slide
   that could produce 8 ~2-char fragments). Medium-high that they are corruptions of real
   labels rather than invented content.
No other unmatched content strings: every remaining parse line maps to a GT string (the
3× `Transformer Block` occurrences match GT's 3 bars at the correct multiplicity).

## 2. Layout & coordinates

- Parse items carrying `<x_…><y_…>` tokens: **2** (of ~25 content lines).
  - Item 1 `<x_0.0391><y_0.0773>` → (37.5, 41.7) px; carries the ENTIRE 24-line text dump.
  - Item 2 `<x_0.9443><y_0.9586>` → (906.5, 517.6) px; carries only `<class_Picture>`.
- Both points land inside the 960×540 frame.
- Matchable same-text pairs: **0** — the only positioned text is an unstructured 24-line
  block, so no per-element px distance can be computed.
- Distance to nearest GT element: item 1 → 107.2 px (GT note "Single vector representing /
  the whole sequence", box 70.1,143.9..270.1,175.9) — OUTSIDE the ~80 px band. Item 2 →
  0 px (inside the lilac Input-Sequence container's bottom-right corner), 5.1 px to the
  last V-tail cell, 39.1 px to the Vector_{PN-1} label box — but it carries no text.
- Fraction of parse items within ~80 px of the nearest GT element: **0/2 text-bearing
  items (0%)**; 1/2 if the textless region point is counted.
- Shape/region counts: build renders **240 items** (193 shape primitives + 47 text boxes)
  in 14 logical groups; the analysis defines 11 layout regions. Parse detected regions:
  **1** — a single whole-frame `<class_Picture>`. Ratio 1 : 240/11.

Reading order (only ordering signal present) roughly follows the GT's top→bottom bands:
Output Classes / C-labels / badge 59 → Softmax band → left notes → GAP → Output Sequence →
(encoder) → Input Sequence → position row. The encoder, pooled row, arrows, fan lines and
dots carry no text and no position, so band separation exists but no within-band geometry.

## 3. Structure fidelity

- Parse class tokens: `<class_Picture>` ×1 only. No section-header / list / table / chart /
  equation classes were emitted.
- Section headers: GT's 3 header-level texts (Output Classes, Transformer Encoder title,
  Softmax Layer) are all present as plain lines but with no structural marking.
- Lists: none in GT, none in parse. Tables/charts: none in GT (n/a); the parse extracted no
  data values — correctly, since there is nothing numeric beyond token labels.
- Equations: GT math = `Σ` ×3 + subscripted serif labels (X_i, Y_i, Vector_{Pi}, C_i) + "+"
  node. The parse kept **no** math: Σ is absent in both 2D and linear form; subscripts were
  flattened (`VectorP0…`, linear but lossy) or garbled (`1C1`, `Xd`, `YNz`). The only
  readable math-adjacent output is the flat `VectorP0…VectorPn-1` run (linear, not 2D).
- What the build encodes that the parse CANNOT carry: all 34 palette hexes; the exact
  frame-px geometry of 240 shapes; fonts (Arial vs Times New Roman bold-italic); dashed
  borders on 3 bands; z-order (red rim circle behind each navy circle); shape types
  (roundRect / upArrow / ellipse / line); multiplicity semantics (3 identical Transformer
  Block bars, 3 Softmax circles, 20-cell pooled row, 5-dot ellipses ×3, 6 ellipsis
  columns, 18 fan lines); which pooled cells feed which softmax circle; badge ring
  color/width; near-white arrow fill.

## 4. Reliability

| Call | EXIT | finish_reason | output_tokens | content chars | latency | stderr lines |
|---|---|---|---|---|---|---|
| call01_pass1 | 0 | stop | 119 | 424 | 28.5 s | 0 |
| call02_pass2 | 0 | stop | 119 | 424 | 122.5 s | 0 |

- Avg latency 75.5 s; avg output tokens 119; both `.parse.md` files byte-identical (diff
  empty).
- Corroboration (pass1 vs pass2): Jaccard overlap of detected GT strings = **1.00**
  (28/28 each); strings found in only one pass: **none**.
- Critical caveat: the two passes are NOT independent reads. Raising the output cap
  1024 → 3000 changed nothing (119 < 1024), the same 119 tokens were emitted verbatim —
  `finish_reason=stop` was reached voluntarily, not capped. Every error in pass1 is present
  in pass2, so corroboration cannot rescue single-read errors here; findings stand as a
  duplicated single read. `finish_all_stop` = 1/1 (wave-2 metric, recorded not scored).

## Claims for image adjudication

1. C₁/C₂/C₃ rendering — verify whether the three class labels are exactly "C₁ C₂ C₃" and
   whether any stray glyph precedes the first two (parse emitted `1C1`, `1C2`) or whether a
   `1`-like element really sits left of the class band.
2. Head-column subscript digits — the build code renders X₀..X₅ / Y₀..Y₅ while the build's
   header comment and the analysis JSON say X₁..X₆ / X₁..X₅: verify the printed digits of
   the six head columns on both token rows (this settles what the 8 garbage tokens
   corrupted).
3. Garbage tokens `Yd Xd Xx XN Xt Yk YNz YNd` — check the image's X/Y row labels: are they
   serif bold italic with subscripts (which could break a parser into such fragments)? Do
   any of these fragments correspond to actual glyphs on the slide, or are they invented?
4. Σ visibility — GT draws a Σ inside each of the 3 navy softmax circles; the parse has no
   sigma at all: confirm Σ is printed in the circles (total miss vs genuine absence).
5. "Softmax" multiplicity — GT has per-circle "Softmax" ×3 plus "Softmax Layer" on the tan
   bar; the parse emitted only "Softmax Layer": count the visible "Softmax" strings.
6. Vector_{PN-1} case — GT renders capital N (`Vector_{PN-1}`); parse wrote lowercase
   (`VectorPn-1`): verify the subscript case of the last position-vector label.
7. Pooled-vector row — GT build draws 20 pastel cells, the analysis says ~30, the parse
   describes no row: count the squares in the pooled row (settles GT's 20-vs-30 split).
8. Transformer Block count — parse matched 3/3 bars; verify the bar count on the image and
   that the 6 white-3-dot ellipsis columns sit between bars 2–3 (nothing in the parse
   mentions them).
9. Vertical layout order — the parse gives only 2 coordinate tokens; verify the
   bottom→top flow on the image (Input Sequence at bottom → encoder → Output Sequence →
   GAP → pooled row → softmax band → Output Classes at top) to confirm the parse's reading
   order is the true arrangement.
10. Badge — verify the top-right badge circle shows `59` with the purple ring (playlist
    chrome) and no other digits, i.e. the parse's "59" is the badge, not stray content.
11. Line-structure loss — verify "Word / Embedding / Vectors", "Position / Information /
    Vectors" and "Single vector representing / the whole sequence" are 3-/2-line stacked
    labels on the image (parse merged them to single lines).
12. The textless region point at (906.5, 517.6) px — confirm nothing textual sits at the
    frame's bottom-right corner (GT has only the lilac container edge there), i.e. the
    parse's sole region is a whole-frame picture class rather than a missed label.
