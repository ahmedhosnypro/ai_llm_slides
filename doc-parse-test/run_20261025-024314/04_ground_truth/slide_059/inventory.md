# Ground-truth inventory — slide_059 ("Transformer Encoder" classifier stack)

Video namespace: `deep-learning/002_transformers_part2` (deck CLOSED 2026-10-13, 60/60 certified).

Frozen sources in this dir (md5-verified identical to the live files):

| File | Source | md5 (head) |
|---|---|---|
| `slide_059.js` | `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_059.js` | 268ee35f89ca912f… |
| `house_chrome.js` | `videos/deep-learning/shared_patterns/house_chrome.js` | cf357ccadbded846… |
| `slide_059_final.json` | `videos/deep-learning/002_transformers_part2/analysis/slide_059_final.json` | 2ba1f0f964f9caef… |

- **Dependency note**: edge 59←38 is PATTERN-level, not compositional — the certified
  builder is STANDALONE and `require()`s nothing from slide_038 (build header comment;
  lecture AGENTS.md: "Slide 49 / 59: pattern-derived dependencies … do NOT clone their
  compositions"). The only require()-pulled build file is the playlist
  `shared_patterns/house_chrome.js`. `slide_038.js`/`components/slide_038.js` were NOT
  used and are NOT frozen.
- **Frame mapping**: 960×540 frame, 1 px = 1 pt = 1/72 in; the build's `pt()` values are
  frame px. House chrome (playlist law): white canvas `FFFFFF`, gray panel `E9E9E7`
  (x 42..918, y 45→bottom), red `C00000` border, badge circle d≈36 px centered (893, 71),
  fill `FDFD96`, ring `6A5ACD`, numeral `333333` Arial 18 bold — numeral **59**.

## GT text strings (deduplicated, 46)

Rendering form: "X₀" = run `X` + subscript run; serif labels are Times New Roman bold italic.

| # | String | Where (build section) | Occurrences |
|---|---|---|---|
| 1 | Transformer Encoder | white 20.5pt bold title on red encoder container | 1 |
| 2 | Transformer Block | white 10.5pt bold on 3 dark-red bars | 3 |
| 3 | Global Average Pooling | black 17pt bold in white GAP box | 1 |
| 4 | Softmax Layer | orange 14pt bold on tan bar | 1 |
| 5 | Softmax | yellow 7.5pt bold inside 3 navy circles | 3 |
| 6 | Σ (U+03A3) | white 13pt bold inside 3 navy circles | 3 |
| 7 | + | white 13pt bold in red circle | 1 |
| 8 | Output Classes | blue 13pt bold, top-left of class band | 1 |
| 9 | C₁ | blue serif bold italic + subscript | 1 |
| 10 | C₂ | 〃 | 1 |
| 11 | C₃ | 〃 | 1 |
| 12 | X₀ | red serif bold italic + subscript, embedding row | 1 |
| 13 | X₁ | 〃 | 1 |
| 14 | X₂ | 〃 | 1 |
| 15 | X₃ | 〃 | 1 |
| 16 | X₄ | 〃 | 1 |
| 17 | X₅ | 〃 | 1 |
| 18 | X_{N-2} | 〃 | 1 |
| 19 | X_{N-1} | 〃 | 1 |
| 20 | Y₀ | red serif bold italic + subscript, output row | 1 |
| 21 | Y₁ | 〃 | 1 |
| 22 | Y₂ | 〃 | 1 |
| 23 | Y₃ | 〃 | 1 |
| 24 | Y₄ | 〃 | 1 |
| 25 | Y₅ | 〃 | 1 |
| 26 | Y_{N-2} | 〃 | 1 |
| 27 | Y_{N-1} | 〃 | 1 |
| 28 | Vector_{P0} | navy serif bold italic + subscript, position row | 1 |
| 29 | Vector_{P1} | 〃 | 1 |
| 30 | Vector_{P2} | 〃 | 1 |
| 31 | Vector_{P3} | 〃 | 1 |
| 32 | Vector_{P4} | 〃 | 1 |
| 33 | Vector_{P5} | 〃 | 1 |
| 34 | Vector_{PN-2} | 〃 | 1 |
| 35 | Vector_{PN-1} | 〃 | 1 |
| 36 | Single vector representing | red italic serif 13.5pt, left annotation line 1 | 1 |
| 37 | the whole sequence | 〃 line 2 | 1 |
| 38 | Output | red bold italic 14pt, left annotation line 1 | 1 |
| 39 | Sequence | 〃 line 2 | 1 |
| 40 | Input Sequence | red bold italic 14pt, left annotation | 1 |
| 41 | Word | green bold italic 13pt, left annotation line 1 | 1 |
| 42 | Embedding | 〃 line 2 | 1 |
| 43 | Vectors | 〃 line 3 (also in #44–45 group — deduplicated once) | 2 |
| 44 | Position | blue bold italic 13pt, left annotation line 1 | 1 |
| 45 | Information | 〃 line 2 | 1 |
| 46 | 59 | badge numeral (chrome) | 1 |

**GT-internal discrepancy (flagged for image adjudication):** the build CODE renders the
six head token columns as `X₀..X₅` / `Y₀..Y₅` (subscript digits 0–5, `X_SUBS` array),
while the build's own header comment says "X_1..X_6" and the analysis JSON lists
`X₁..X₅` / `Y₁..Y₅` + tails (7 labels each). The certified build's rendered strings are
used as GT here; the frame is the arbiter (claim #2 in the comparison file).

## Layout regions / shapes

- **Rendered item count (build)**: 240 total = 193 shape primitives + 47 text boxes.
  Breakdown: chrome 3 · input container 1 · 3 dashed band rects · 2 token rows × (40
  cells + 8 labels + 5 dots) = 106 · V row 16 cells + 8 labels + 5 dots = 29 · "+" node 2
  · encoder container 1 + 3 bars + 3 bar texts + 18 ellipsis dots + 1 title = 26 · GAP
  box 2 · pooled row 20 cells · fan lines 18 · softmax bar 2 + 3 × (rim + circle +
  Softmax + Σ + stem) = 17 · C labels 3 · Output Classes 1 · 4 block arrows · 5 left
  annotation boxes.
- **Logical groups (build comment sections)**: 14 (chrome + 13 content groups).
- **Analysis `layout.regions`**: 11 named regions.
- **Diagram grammar**: vertical bottom→top data flow on centerline x≈511 px: Input
  Sequence container (lilac) → blue up-arrow → red encoder container (3 bars) → arrow →
  Output Sequence row (light blue) → arrow → GAP box → arrow → pooled 20-cell row → fan
  of 18 thin lines → tan Softmax bar with 3 navy circles → C₁..C₃.

## Palette (34 distinct hexes from the build)

Chrome/border: `FFFFFF E9E9E7 C00000 FDFD96 6A5ACD 333333` · fills: `F5DCF6 F0FEE4
FDEBD0 D6EAF8 CD5C5C FBF0D2 F2D8C8 TAN=F5CBA7 EDEFFF` · cell colors: `FCFCD4 F0FEE4
FFB6B6 DCDFF2 F2D9F4` · pool cells: `FEFFC5 E3FFCB EDE4C1 F8DBC1 E2DCF3 F5D6EE` ·
lines/ink: `A00000 00008B C00000 00B050 0000CC 2E64FE E67E22 7F7F7F A6A6A6 9C2020
20208F FFB3B1 FFFFFF 000000 F7DC6F`.

## Fonts

- Arial (sans): all section labels, bar text, GAP, badge numeral, Σ, +.
- Times New Roman bold italic: X/Y/Vector/C symbol labels, with true subscript runs;
  "Single vector representing the whole sequence" is Times italic 13.5.

## Charts / tables / equations

- No charts, no tables, no bullet lists, no OMML/mathtext equations in the build.
- Math-ish content the build encodes: Σ glyph ×3; subscripted symbol labels
  (X_i, Y_i, Vector_{Pi}, C_i) as serif bold italic + subscript runs; a "+" addition
  node. The analysis additionally records the implied equation `Xᵢ + Vector_{Pi}`
  (marked "implied" — not verbatim on the slide).
