# Ground-truth inventory — slide_037 (002_transformers_part2, Deep Learning DSAI 308)

Scope: `slide_037` · worker: `worker-slide_037` · wave 1 (report-only vs project; all
paths below are read-only inputs; frozen copies + this inventory live under
`doc-parse-test/run_20261025-024314/04_ground_truth/slide_037/`).

## Provenance / frozen inputs

| Frozen copy (md5) | Source (read-only) |
|---|---|
| `slide_037.js` 9a25d4956574337754d22ffe6bfad3f5 | `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_037.js` |
| `slide_019.js` ae79ac207a53e5281a007d1f3c3872f8 | `videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_019.js` |
| `slide_018.js` 02a4a344ae05a49fe9ac59c032e50d6b | `videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_018.js` |
| `slide_017.js` 63b0708c90787608007edd5be875bc76 | `videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_017.js` |
| `house_chrome_001_component.js` f729966cc177a7b6f5e79b841fcd13cc | `.../001_transformers_part1/recreated_pptx/build/components/house_chrome.js` |
| `house_chrome_shared_patterns.js` cf357ccadbded846196a823ae9d1e2d0 | `videos/deep-learning/shared_patterns/house_chrome.js` |
| `slide_037_final.json` b2e1462bd29d94d9e48077b608275c74 | `videos/deep-learning/002_transformers_part2/analysis/slide_037_final.json` |

Require chain (followed read-only): `slide_037.js` → `001/components/{slide_019,
slide_017, slide_018, house_chrome}`; `slide_019 → slide_018 → slide_017`;
`house_chrome` (001) → `shared_patterns/house_chrome.js`. Cross-video dependency edge
`37 ← 001:19` (recorded in `002_transformers_part2/slide_dependencies.json`; the child
imports 001's certified slide-019 component and draws only its measured delta).

**How the numbers below were produced:** the frozen `slide_037.js` was executed under a
stubbed `pptxgenjs` recorder (`_sim/node_modules/pptxgenjs` — `addShape`/`addText`
record calls, `writeFile` is a no-op; nothing written to the project — verified: the
deliverable pptx's mtime is unchanged, 2026-10-12). Record: `_sim/draw_record.json`
(268 draw calls: 202 shapes + 66 text boxes; all geometry already in frame px,
1 px = 1 pt = 1/72 in on the 960×540 frame).

**Parse-input capture context:** `unique_slides/slide_037.jpg`, 960×540 baseline JPEG
(1 px on the frame ≈ 1 pt on the 960×540 slide; the px geometry below uses the same
frame). 960×540 < the parser's 1664×2048 max input resolution → no downscale. The
image itself was never opened in this lane (no image bytes in context).

## Deduplicated GT text strings (label level; instance counts = drawn / final-visible)

Drawn = text boxes in the build's z-stack (66 boxes, 84 rendered lines); visible =
survives later repaint patches / overlay boxes. The build draws the 001:17/18/19
certified chain, then repaints/patches parts of it; hidden-under-patch strings are
listed for completeness because a parser sees the RENDERED frame, not the z-stack.

| # | GT string | Drawn inst. | Visible inst. | Position(s) of visible inst. (px box) |
|---|---|---|---|---|
| 1 | `37` (badge numeral) | 1 | 1 | 875,53 36×36 (badge circle, top-right) |
| 2 | `Transformer Blocks (stacked over Multi-Head)` (title) | 1 | 1 | 96,50 800×50, 35.5 pt bold #C00000, top-LEFT |
| 3 | `Scaled Dot-Product Attention` | 2 | 2 | inset-A header 54,227 148×40 (2 lines, 15 pt bold italic red); SDPA box in inset-B 309,360 161×32 (2 lines, 8 pt) |
| 4 | `Multi-Head Attention` | 4 | 3 | inset-B header 294,210 200×24 (15 pt bold italic red); encoder box 650,355 72×32 (9 pt); decoder box 748,277 73×33 (8.5 pt) — a 4th drawn inst. (017's enc-stack text 630,356) sits behind the salmon box |
| 5 | `Masked Multi-Head Attention` | 1 | 1 | 748,348 69×35 (3 lines, 8.5 pt) |
| 6–8 | `Q` / `K` / `V` (circle letters) | 5 sets (15 circles) | 15 | inset-A Q84,466/K119.5,464.5/V157.5,464; inset-B V321,489/K378.5,489/Q437,490.5; encoder V657.5,394.5/K689.5,395/Q712,395; decoder-masked V745.5,385/K787.5,384/Q816,386; decoder-cross V743.5,311/K768.5,312/Q815,311.5 |
| 9 | `MatMul` | 2 | 2 | 76,429 88×16; 105,294 68×18 |
| 10 | `Scale` | 1 | 1 | 93,397 38×12 |
| 11 | `Mask (opt.)` | 1 | 1 | 77,363 69×14 |
| 12 | `SoftMax` (inset-A box) | 1 | 1 | 80,330 62×15 |
| 13 | `Concat` | 1 | 1 | 364,312 46×14 |
| 14 | `Linear` | 5 | 5 | inset-B 309,403 / 359,403 / 416,403 / 364,266; decoder 752,177 67×14 |
| 15 | `h` (brace label, italic) | 1 | 1 | 484.5,357.5 19×19 |
| 16 | `Encoder` (panel label, red italic) | 1 | 1 | 581,112 84×20 |
| 17 | `Decoder` (panel label, green italic #0E7D10) | 1 | 1 | 818,112 72×20 |
| 18 | `Output` (yellow band) | 1 | 1 | 761,112 51×16 |
| 19 | `Probabilities` | 1 | 1 | 756,127 60×14 |
| 20 | `Softmax` (decoder box) | 1 | 1 | 752,152 67×14 |
| 21 | `Add & Norm` | 10 | 4 + 1 occluded | visible: 653,277 (enc, 7.5 pt); 753,206.5 (dec steel #327389); 753,263.5 (dec steel); 753,329.5 (dec indigo #4863BE); occluded: 653,342 — under the solid red disc (672,331.5 d≈23.5). The other 5 drawn inst. (017 chain) are hidden under repaint patches/boxes |
| 22 | `Feed Forward` | 4 | 2 | 654,292 59×26.5 (enc, 2 lines); 753,223.5 64×26.5 (dec, 2 lines); 017's two inst. hidden under repaints |
| 23 | `N x` (repeat glyph, spaced — analysis JSON writes it `Nx`) | 2 | 2 | 597.5,329.5 25×25 (enc); 845.5,300.5 21×21 (dec) |
| 24 | `Positional Encoding` | 2 | 2 | 594,416 56×28 (enc, 2 lines); 836,419 48×28 (dec, 2 lines) |
| 25 | `Input Embedding` | 1 | 1 | 653,446 68×25 (2 lines) |
| 26 | `Output Embedding` | 1 | 1 | 756,446 63×25 (2 lines) |
| 27 | `Inputs` | 1 | 1 | 664,494 44×16 |
| 28 | `Outputs (shifted right)` (build lines: `Outputs` + `(shifted right)`) | 1+1 | 1+1 | 761,492 51×19; 748,508 76×14 (green #3C8C3C) |
| 29 | `WE ARE HERE` (build: 3 lines `WE`/`ARE`/`HERE`, white bold, rotated 342°) | 1 | 1 | 601.6,182.4 60×55 (on the red map-pin head) |

**29 unique GT labels** (36 unique rendered line-strings; 84 rendered lines; 66 text
boxes). Bullets: none (diagram-only slide — 0 bullet lines, per the certified
analysis). Equations: none. No `[No ...` meta entries exist in the analysis JSON.

## Layout regions / shapes

- Analysis JSON `layout.regions`: **7** — Title; Slide-number badge; Scaled Dot-Product
  Attention diagram (~6–23% w, 38–90% h); Multi-Head Attention diagram (~30–54% w,
  36–93% h); Transformer architecture diagram (~57–93% w, 17–96% h); Connector funnel;
  Video progress bar (bottom ~96–100% h — video-player UI, not slide content, and NOT
  drawn by the build).
- Build drawn primitives (recorder): **202 shapes** — 61 rect, 92 line, 26 ellipse,
  13 triangle, 10 roundRect — plus **66 text boxes** = 268 draw calls, composed in
  z-order: house chrome → 017 blocks (21, minus title/callouts/leaders/PE) → 018 delta
  (15, minus banners) → 019 delta (6, minus legends/leaders/enc-repaints/dec-green) →
  037 own delta (10 blocks: gap shafts, dec green w/ zone-3 chevrons, warm encoder
  interior, dashed box, funnel, pin, disc, enc PE clock, dec PE clock, title).

## Palette (75 hexes on the final render)

Chrome: `FFFFFF` canvas · `E9E9E7` panel · `C00000` border/badge-ring-adjacent red ·
`FDFD96` badge fill · `6A5ACD` badge ring · `333333` numeral.
Full set (from the recorder): 0000A1, 00A000, 05008F, 0E7D10, 1A1A1A, 1B723F, 2A26A0,
2E2318, 2E2E2E, 2F2F2F, 2F6476, 327389, 331111, 333333, 3A3630, 3A4A2C, 3A5697,
3C8C3C, 3E3A28, 3E7150, 3F3F3F, 404040, 4863BE, 4A4A4A, 4A7360, 562366, 5C9CB7,
6A5ACD, 6B2A28, 6E4423, 6E7E62, 6E87E0, 753029, 7B4B2A, 808080, 81C124, 857F73,
8A6A48, 8A8A8A, 8C4423, 8CC62E, 990000, 997343, A6A6A6, A8ECBC, ABABAB, B01515,
B08058, B0B070, B0E4CE, B28659, B5BB97, B8706C, BB93AE, C00000, C0B9DA, C3B744,
C87E57, C8965A, C8A888, C8E9CE, C8F8E0, CE8ADC, D4BCA0, DC1A20, E4E4E4, E9E9E7,
E9EDEA, EEC3D7, F8FBC6, FBECDB, FCFBC5, FDFD96, FFFF00, FFFFFF.

## Fonts / typography

Single font family: **Arial** (every text box carries an explicit `fontFace: Arial`).
Sizes 6.5 pt (cross-attention circle letters) → 35.5 pt (title); numeral 18 pt bold.
Title/headers bold; the 4 diagram headers (inset-A, inset-B, Encoder, Decoder) are
bold **italic** red/green; block labels bold 7–9.5 pt; `Output`/`Probabilities` 8 pt
regular; pin text 12.5 pt bold white rotated 342°.

## Charts / tables / equations the build encodes

**None.** The slide is 3 vector diagrams (2 flowchart insets + 1 encoder–decoder
architecture) drawn natively from shapes/lines. No chart data series, no table, no
math/equation objects (no mathtext PNGs, no OMML) — the equation pipeline does not
apply to this slide. Diagram semantics (arrows, dashes, z-order, occlusion, stacked
shadow copies, clock icons, chevrons) are shape geometry, not text.

## Build facts a parse transcript cannot carry

Colors (75 hexes), exact px geometry of 202 shapes, fonts/sizes/bold/italic,
z-order & occlusion (the hidden `Add & Norm` under the disc; 017-chain strings under
repaint patches), dash patterns (dashed rounded box, funnel dashes, dashed decoder
MHA border, dashDot feedback curve), rotation (342° pin text), stacked-card shadow
copies, the yellow L-shaped cross-attention band, clock icons, navy chevrons, badge
ring geometry, and the fact that the bottom black strip is video UI (absent from the
build by design).
