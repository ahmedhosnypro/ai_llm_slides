# Ground-truth inventory — slide_057 (002_transformers_part2)

## Frozen GT files (this dir)

| file | role |
|---|---|
| `slide_057.js` | certified builder (the slide's composition) |
| `slide_049.js` | require() — composition provenance (049 stacked-encoder restyled) |
| `slide_047.js` | require() — founder edge 57←47; 0-BASED SUBS label law `["0".."5","N-2","N-1"]` |
| `slide_026.js` | require() — certified frame→slide mapping helpers (MX=18.628 SX=0.96123 SY=0.95556; `x/y/w/h`) |
| `house_chrome.js` | require() — playlist chrome (panel + badge) |
| `slide_057_final.json` | certified vision analysis JSON |

No further require() chains: `slide_049.js`→`slide_026.js`→`house_chrome.js`; `slide_047.js`→`house_chrome.js` — all frozen. The builder uses P026 only for the `x/y/w/h` helpers and P047 only for `SUBS`; it draws its own encoder/central/decoder (049's delta blocks are NOT called).

## Slide identity

- No on-slide title/subtitle (analysis `slide_title` is explicitly descriptive-only). A single full-bleed encoder-decoder schematic.
- House chrome: white canvas `FFFFFF`; gray panel `E9E9E7` x 42..918, y 45→bottom, red `C00000` border; badge circle d≈36px center (893,71), fill `FDFD96`, ring `6A5ACD`, numeral **57** bold Arial 18pt `333333` (= printed number on slide_057.jpg).
- Frame 960×540, 1px ≈ 1pt; all build coordinates are frame px.

## Deduplicated GT text strings

### Primary (certified build, slide_057.js) — 48 strings

Badge/chrome: `57`

Bars (encoder, 4): `Encoder Block M` · `Encoder Block 2` · `Encoder Block 1` · `Encoder Block 0`

Token chips (serif italic letter + subscript, 16): `Y_0 Y_1 Y_2 Y_3 Y_4 Y_5 Y_{N-2} Y_{N-1}` · `X_0 X_1 X_2 X_3 X_4 X_5 X_{N-2} X_{N-1}`

Word row (8): `Word 0 Word 1 Word 2 Word 3 Word 4 Word 5 Word N-2 Word N-1`

Embedding box (2): `Word Embedding` · `Positional  Encoding / Embedding` (double space in build)

Decoder bars: `Residual Connection and Layer Normalization` (×7 red bars) · `Feed Forward Networks - One Hidden with RELU Activation` (×3 green bars) · `Softmax` (×1 maroon bar)

Attention boxes: `Encoder Decoder Attention` (3 stacked lines in each of 15 blue boxes) · `Multi-Head Self-Attention` (masked row, 5 boxes)

Feed badges (3): `K` · `V` · `Q` (Q ×4 instances: 2 tiny mid-column, 1 bottom-right, plus feeds K/V)

Panel/legend labels: `Encoder` (vertical 270° red + legend line 1 red) · `Decoder` (vertical 270° green + legend line 2 green) · `Attention` (legend line 3 blue) · `Word and Position Encoding` (decoder purple bar)

Bottom token row (5): `SOS` · `Je` · `ne` · `suis` · `faisait`

### Analysis-JSON-only strings (8) — NOT in the certified build; build-vs-analysis divergences

- `Tokens` — analysis reads a red brace label over the decoder circle rows; build OMITS it per GROUND RULES(c) (brace left unlabeled, banked v_A_dec_top/v_A2/v_blk4).
- `POS` and `m/t/de [?]` — analysis reads tiny end-labels on the decoder purple bar; build OMITS (p3 census: solid ends; v_blk4/v_K2 not-resolvable).
- `X_N` / `Y_N` — analysis lists an N-th chip; certified 0-BASED SUBS law (P047, vision-confirmed "no tildes or prime marks", last chip = `N-1`) says the analysis misread the last chip.
- `Masked Multi-Headed Attention` (analysis) vs build `Multi-Head Self-Attention` — wording divergence, needs image adjudication.
- `Word and Position Embedding` (analysis) vs build `Word and Position Encoding` — wording divergence, needs image adjudication.
- `Multi-Head [?]` — analysis's uncertain tiny sub-label inside the blue boxes; build renders the 3-line `Encoder / Decoder / Attention`.

## Layout regions & shapes

Analysis layout regions (6): Encoder panel (left ~4–48%) · central encoder-output column + K/V arrows (~48–57%) · tri-color caption (bottom-center) · Decoder panel (right ~56–90%) · slide-number badge (top-right) · bottom black player-strip artifact (omitted from build per GROUND RULES).

Build composition (static census of slide_057.js draw calls): **113 helper-call sites** — drawEncoder 32, drawCentral 28, drawDecoder 53 — plus 3 chrome items. Static loop expansion ≈ **820 drawn primitives** (e.g. 8-column grids ×5–6 cells/chip, 17-circle row, 16×5 fan lines, 20 attention boxes with 3-D shadows, 7 red bars + 3 FFN bars). Z-order is load-bearing: chrome → decoder → central → encoder.

Key frame-px geometry: encoder container (65,131)–(448,510); 8-col grid centers x [114.5,150,185.5,221,256.5,292,384.5,419.5]; decoder panel (555,49)–(854,516); decoder col centers x [603,645.5,690.5,739,781], box lefts x [586,629,674,722,765]; central striped column (470.5,100)–(502.5,418); legend text block x466 y426–480; vertical labels x73 (Encoder, y256..360) and x838 (Decoder, y232..332); badge box x875..911 y53..89.

## Palette (build hexes)

Chrome: `FFFFFF` canvas · `E9E9E7` panel · `C00000` border · `FDFD96` badge fill · `6A5ACD` ring · `333333` numeral.
Encoder: `CCC1B3`/`7A2318` container · `584592` bars · `00008B`/`04048C` navy/dots · `F2C9D6` pink arrows · `D8EFC8`/`2E8B57` green arrows · chips `FDF3DC F2C4CC F6D8E0 6A1A1A` · warm chip stripes `FFF3C8 FFE0A8 FFAD7A FF8D6A F8B8B0 F8D0D0` · `8E1A1A` label red · `F4CEA4`/`E07018` word-emb · `DFF5D0`/`2838A0` PE · `FBE0CC`/`C04030` word boxes · `8A8A8A` gray dots.
Central: `B4AEE6`/`E0E0FA`/`1A1160` column · `8D8AB5` fan · `FFF8E0`/`B02020`/`8E2E31` K/V badges · `C8C4F0`/`333399` hatch.
Decoder: `C0EBD0`/`2E8E38` panel · `7A1F1F` red bars · `1E9028` FFN · `001878`/`3078C0`/`58A8C8` attn boxes · `D6EEDC`/`8A9070` blocks · `A8C0A8`/`789878` sage · `888878` segs · `FFF8E0`/`8A8A60`/`D2C088`/`8A7A40` strips · `CFC1E2`/`C893C4` lavender · `5C186E` purple bar · `C8E8C8`/`5A9A6A`/`A03020`/`E0F4DC` tokens · `E8E0F8`/`5A2E98` hollow · `3AA8A8`/`B400C8`/`2E8E8E` circles · `A5EFC0`/`1E8E3E`/`9FE8AC` green box · `1E8E3E`/`2038C8` legend greens/blues · `C04040`/`3050C0`/`E0C040`/`E08030`/`40A060` multicolor squares · `DFF5C8`/`8A9A70` band-6.

## Fonts

Arial (sans; bar labels 5–11pt bold, vertical labels 15/20pt bold, legend 15.5pt bold italic) + Times New Roman (serif italic: chip labels 8.5pt, word labels 6.5pt, K/V/Q badges 5–11pt, red label ink `8E1A1A`).

## Charts / tables / equations

NONE — `analysis.verbatim_text.equations = []`; the build encodes no chart, table, or equation (pure labeled schematic). A parse claiming equations/charts would be hallucination; a parse omitting them is correct here.

## Omissions by law (not parse failures to expect, but build-side deliberate)

Per banked GROUND RULES(c) the build omits: the cursor artifact on the central column, the bottom player strip, the "Tokens" brace label, and the purple-bar end labels; sketched (unresolvable <5px): right-margin dark marks x822..837 y263..298.
