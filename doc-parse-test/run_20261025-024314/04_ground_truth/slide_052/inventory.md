# Ground-truth inventory — slide_052

Scope: `slide_052` · source frame `videos/deep-learning/002_transformers_part2/unique_slides/slide_052.jpg` (960×540 baseline JPEG, 1 frame px ≈ 1 pt; build uses frame→slide transform `slide_x=(fx−18.63)/0.96123`, `slide_y=fy/0.95556`).

Frozen GT copies (this dir): `slide_052.js` (certified builder, md5 `9425cf73853b97d1ec98eea0c1e41bcf`), `house_chrome.js` (required by the builder, md5 `cf357ccadbded846196a823ae9d1e2d0`), `slide_052_final.json` (vision analysis, md5 `c785be71d1e80cb46a878a6dcd2d1953`).

## 1. Deduplicated GT text strings (22 units)

Composed text units the certified build places (run arrays joined; loop expansions deduplicated). Order = reading order of the build.

| # | GT string | Instances on slide | Build source |
|---|---|---|---|
| 1 | `Multi-head Encoder-Decoder Attention Block` | 1 | callout 1, 3 runs, "Encoder-Decoder" italic+underlined (slide_052.js:257-262) |
| 2 | `Masked Multi-head Self Attention Block` | 1 | callout 2, 3 runs, "Self" italic+underlined (slide_052.js:263-268) |
| 3 | `Residual Connection and Layer Normalization` | 3 | dark-red bars: upper fx(338,84), upper fx(338,146), lower fx(338,312) |
| 4 | `Feed Forward Networks [ One Hidden with  RELU Activation]` | 1 | green bar fx(338,116); VERBATIM double space before `RELU`; `RELU` in Courier New, rest Arial (slide_052.js:90-94) |
| 5 | `Encode Decoder Attention` | 5 | upper blue 3D boxes, 3 stacked lines `Encode`/`Decoder`/`Attention` — verbatim "Encode" (no "r") (slide_052.js:117-121) |
| 6 | `Masked Multi-Head Self Attention` | 5 | lower masked boxes, 3 stacked lines, `Masked` in #FFFF00 yellow (slide_052.js:152-156) |
| 7 | `Word and Position Encoding` | 1 | purple bar fx(344,454) |
| 8 | `Transformer Encoder` | 1 | large blue box fx(77,305) 19pt |
| 9 | `SOS = Start Of Sentence` | 1 | pale-green legend fx(64,485); analysis files it under `equations` too |
| 10 | `I` | 1 | white red-bordered input box 1 |
| 11 | `feel` | 1 | input box 2 |
| 12 | `Sick` | 1 | input box 3 |
| 13 | `SOS` | 1 | pale-green word box 1 |
| 14 | `Je` | 1 | word box 2 |
| 15 | `me` | 1 | word box 3 |
| 16 | `sens` | 1 | word box 4 |
| 17 | `malade` | 1 | word box 5 |
| 18 | `K` | 1 | red circle, upper container left edge fx(309,180) d≈15 |
| 19 | `V` | 1 | green circle fx(310,231) |
| 20 | `Q` | 5 | blue circles under the five upper boxes, fx x≈385/489/601/715/813, fy≈253 |
| 21 | `Y` | 3 | red tags above left token groups, fx x≈85/163/239, fy≈247 |
| 22 | `52` | 1 | badge numeral, house chrome (center ≈(893,71) house / measured (875.5,69.5) this frame), #333333 bold 18pt Arial |

No bullets, no title bar (analysis `slide_title` is a reconstruction; the frame carries no title text). Analysis `verbatim_text.bullets` is empty; all 38 raw label instances deduplicate to the 22 units above.

## 2. Layout regions / shapes

- **Drawable elements (authoritative, from an instrumented run of the frozen builder with a recording pptxgenjs stub — `build_probe/out/probe.json`): 256** = 218 shapes (137 rect, 82 line, 15 triangle, 8 ellipse) + 38 text elements (14 of them plain text boxes, 24 shape-bound).
- **Structural regions (analysis `layout.regions`): 9** — outer frame, callout 1, callout 2, badge, top container, bottom container, left encoder panel, connectors, mouse cursor (recording artifact, excluded from recreation per build header).
- Major geometry (frame px): upper beige container (318,72,552,195) + 5 cream strips; lower pink container (313,294,555,222) + 5 strips; 5 upper blue boxes (fy 178-243), 5 lower masked boxes (fy 344.5-384); K/V long arrows fy 202/223; 5 Q stems fy 246-294; 3 input boxes fy 444; encoder box (83,299,210,120); 2 callouts fx(64,62,232,45)/(64,127,232,51); 13 token-square groups (5 upper fy54, 5 lower fy277, 3 left fy265 inside enclosure (57,257,238,22.5)); 15 causal-mask tips (per-box counts 1,2,3,4,5; colors magenta/red/blue/orange/dark-red) + 15 hairline stems; 5 token-cell grids (2 tan h-rules + 6 v-rules + 2 rails each, #C2B498).

## 3. Palette (build constants + house chrome)

`FFFFFF` canvas · `E9E9E7` gray panel · `C00000` chrome border · `FDFD96` badge fill · `6A5ACD` badge ring · `333333` badge numeral · `990000` residual bars · `0A9A08` FFN bar · `0010B4` blue boxes · `3C3CD0`/`0A1A6E`/`3A50CC`/`0A1878`/`14247E`/`000080` 3D box detail · `7A0080` purple bar · `F4F8D2` cream strips · `D6C6B4` upper container · `F2DDF6` lower container · `A89878`/`C24AC2` container borders · `CC0000` callouts/Y/arrows · `8A1420` input words · `7A2A24` legend/word-box text · `C05055` K · `3E8A3C` V · `23209E` Q · `D98A8E`/`9CCDA8` K/V arrow bands · `999999`/`808080`/`ACA398`/`85806E`/`C2B498`/`B8CCAA` connectors/grids/box borders · `EAFBDC` word boxes/legend · `EAF0F6` top strips · `B040B0`/`D03030`/`3040C0`/`E08030`/`902828` mask tips.

## 4. Fonts

Arial everywhere (bold for all captions/labels); `RELU` run in **Courier New** (deliberate monospace contrast, verbatim double space preserved); badge numeral Arial 18 bold; box labels 13pt/9.5pt with measured lineSpacing 16/12; encoder 19pt; callouts 14.5pt lineSpacing 18.

## 5. Charts / tables / equations / quantitative diagram data

- No charts, no tables, no bullets. One equation-class item: the legend equality `SOS = Start Of Sentence`.
- Quantitative diagram data the build encodes: causal-mask tip counts per box `[1,2,3,4,5]` (15 tips, 5 colors); 13 token-square groups × 3 cells; 7 K/V/Q circles (1+1+5); 10 attention boxes (5+5); 15-arrow Q/K/V flow description in the analysis (build renders the upper Q stems ×5, lower rising arrows as measured stems).

## 6. Build-only facts (a parse transcript cannot carry these)

20+ accent hexes; exact px geometry of all 256 elements; z-order (K/V long arrows pass BEHIND the blue boxes); arrowhead types (`endArrowType`/`beginArrowType` triangle) and directions; italic+underline emphasis inside callouts; `Masked` yellow vs white runs; 3D slab construction (stripe y-positions, side slivers); flipV/flipH on connectors; token-cell grid pitch (12 px) and rail extents; the measured frame→slide capture transform; mouse-cursor omission ruling.
