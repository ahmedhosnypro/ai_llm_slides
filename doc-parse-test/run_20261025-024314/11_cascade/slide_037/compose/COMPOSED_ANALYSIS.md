# COMPOSED_ANALYSIS — slide_037 (worker-slide_037_cascade, wave 5 v1)

**Headline: union recall 100% (29/29 GT labels) vs frozen wave-2 recall 79.3% (23/29).**
Merge of the full-frame pass1 transcript + all 9 banked crop-parse transcripts (3
recursion levels, 8 crops) + the vision-gateway judge transcripts. Deduped at label
level; positions are frame px (960×540) via the manifest transform `frame_x =
crop_x/scale + box.x0; frame_y = crop_y/scale + box.y0`, anchored to the GT inventory's
authoritative positions when REAL-GT. `[?]` marks judge-reported approximations (±15 px).

Provenance keys: **P1** = `03_parses/slide_037/call01_pass1` (full frame, wave-2) ·
**C1..C9** = `11_cascade/slide_037/parses/call01_crop01 … call09_crop05_corroborate`
(crop parses; C9 = 3000-token corroboration re-parse of crop05, string-identical to C5)
· **J2, J4, J5, J6, J7, J8** = `judges/crop02_judge.md, crop04_judge.md, crop05_judge.md,
crop06_judge.md, crop07_judge.md, crop08_judge.md` (vision gateway). GT ids = the 29
inventory ids in `04_ground_truth/slide_037/inventory.md`.

## Merged elements, ordered by frame y

| y (frame px) | Element (verbatim) | Classification (GT id) | Provenance | Notes |
|---|---|---|---|---|
| 50–100 | `Transformer Blocks (stacked over Multi-Head)` | REAL-GT (2) | P1, C1, C8 (fragment `ked over Multi-Head)`) | C1 read exact (block class Page-header); C8 clips the title's right part |
| 53–89 | `37` (badge numeral) | REAL-GT (1) | P1, C1, C8 | exact in C1 and C8 |
| 112 | `Encoder` (red italic panel label) | REAL-GT (16) | P1, C2, C5, C8 | |
| 112 | `Output` (yellow band) | REAL-GT (18) | P1, C2 (merged `Output Decoder`), C5, C8 | J2: pixels show two separate labels Output + Decoder; C2's merge is a segmentation error, not a misread |
| 112 | `Decoder` (green italic panel label) | REAL-GT (17) | **C2, C5, C8** | RECOVERED (absent from P1); C2 inside merged `Output Decoder`; J2 confirms the green italic label |
| 127 | `Probabilities` | REAL-GT (19) | P1, C2, C8 | v1's C2 and C8 both read it; J5 confirms it IS printed in the arch crop (~(630,150)–(802,188) crop-px → ≈(743,125)–(800,138)) — a stable doc-parse blind spot at 3× zoom, not a recall loss |
| 152 | `Softmax` (decoder box) | REAL-GT (20) | P1, C2, C5, C8 | |
| 182–237 | `WE ARE HERE` (3 lines, rotated 342°) | REAL-GT (29) | P1, C2, C8, C5 (case `We ARE HERE`) | case variant = same label; J5 confirms all-caps white-on-red pin at crop-px ~(215,283)–(358,428) |
| 206–343 | `Add & Norm` (4 visible instances: enc 653,277 · dec-steel 753,206 · dec-steel 753,263 · dec-indigo 753,329; 5th occluded under disc) | REAL-GT (21) | **C2, C5 ×2, C8** | RECOVERED (absent from P1); garble variants `Aad & Norm` (C5), `Ad & Norm` (C2) judged REAL misreads; J5 also locates a blue decoder instance at crop-px ~(625,732)–(812,768) |
| 210 | `Multi-Head Attention` (inset-B header, bold italic red) | REAL-GT (4) | P1, C4, C5, C8 | C2 garble `M Multi-Head Attention` and C8 garble `Multi-lead Attention` = same header |
| 227 | `Scaled Dot-Product Attention` (inset-A header + SDPA box in inset-B) | REAL-GT (3) | P1 ×2, C3, C4, C6 (line-2 fragment `Attention`), C7 | P1 garble `Scalar Dot-Product Attention` = same label |
| 177–403 | `Linear` ×5 (decoder 752,177 · inset-B top 364,266 · inset-B bottom 309/359/416,403) | REAL-GT (14) | P1, C2, C4 ×4, C5, C7 ×3, C8 | J4: C4 region carries 4 instances (top + 3 bottom), all exact |
| 292–318 | `Feed Forward` ×2 (enc 654,292 · dec 753,223) | REAL-GT (22) | **C5 ×2, C8** | RECOVERED (absent from P1); garbles `Read Forward` (C2), `Fixed Forward` (C8) |
| 348 | `Masked Multi-Head Attention` (748,348) | REAL-GT (5) | **C5, C8** | RECOVERED (P1 garble `Math-Head Attention` only) |
| 312 | `Concat` (364,312) | REAL-GT (13) | P1 (merged `MatMul Concat`), C2, C4, C7 | |
| 330 | `SoftMax` (inset-A box 80,330) | REAL-GT (12) | P1 (case), C3, C6 | C3/C6 exact case |
| 294–429 | `MatMul` ×2 (76,429 · 105,294) | REAL-GT (9) | P1 (merged `MatMul Concat`), C2, C3 ×2, C6 ×2 | P1 garble `Max` = same label |
| 357 | `h` (brace label, italic, 484.5,357.5) | REAL-GT (15) | **C4, C7** | RECOVERED (absent from P1); J4 CONFIRMED: label right of the attention box on the curved brace of the stacked layers, crop-px (643,524)–(665,556) → frame ≈(493,357)–(500,367), matches GT |
| 363 | `Mask (opt.)` (77,363) | REAL-GT (11) | P1, C3, C6 | |
| 397 | `Scale` (93,397) | REAL-GT (10) | P1, C3, C6 | |
| 416–447 | `Positional Encoding` ×2 (594,416 · 836,419) | REAL-GT (24) | P1 ×2, C2 ×2, C5 ×2, C8 ×2 | |
| 446–471 | `Input Embedding` (653,446) | REAL-GT (25) | P1, C2, C5, C8 | |
| 446–471 | `Output Embedding` (756,446) | REAL-GT (26) | **C5, C9** | RECOVERED (absent from P1); C2 and C8 miss it — C9 (3000-token re-parse) confirms C5 |
| 494 | `Inputs` (664,494) | REAL-GT (27) | P1, C2, C5, C8 | |
| 492–522 | `Outputs` + `(shifted right)` (761,492 · 748,508) | REAL-GT (28) | P1 (2 lines), C2, C5, C8 (composed single line) | |
| 311–494 | `Q`/`K`/`V` circle letters, 5 sets (15 circles) | REAL-GT (6/7/8) | P1 `Q K V`, C2 `V K Q`+`Q K V`, C3, C4, C6, C7, C8; C5 `V K O` | C5's `O` = misread of a Q circle (J5); C7's `9` = misread of the inset-B bottom-right Q circle (J7) |
| 300–330 | `N x` ×2 (597.5,329.5 · 845.5,300.5) | REAL-GT (23) | P1 `Nx`, C2, C5, C8 | J5/J8: the left encoder Nx is mostly occluded (only `N` reads clearly) — matches the GT occlusion note |

## Hallucination candidates (parsed strings with nothing printed on the slide)

| String | Provenance | Judge verdict | Position |
|---|---|---|---|
| (none) | — | — | — |

No doc-parse hallucination survived judging in the v1 cascade: every novel parsed string
mapped to a real GT label as an OCR misread or segmentation artifact (see garble ledger).
The v2 prior-art run caught 2 hallucinations (`Create`, `October 1 March`) on different
crop boundaries; the v1 crop set simply never produced them.

## GT-gaps (real-on-image strings absent from the inventory)

**None found.** All 29 GT ids are recovered by the union and the crop judges found no
printed string the inventory lacks. The bottom video-player UI strip (frame y > 516) is
excluded from crops by design (GT: video UI, not slide content) and carries no text claims.

## Garble ledger (novel parsed strings that are OCR misreads of real GT text)

| Garble | Maps to GT | Where read | Judge |
|---|---|---|---|
| `Scalar Dot-Product Attention` | 3 | P1 | — (obvious) |
| `Mult-Head Attention` / `Math-Head Attention` | 4 / 5 | P1 | — (obvious) |
| `Max` | 9 | P1 | — (obvious) |
| `Output Decoder` (two labels merged) | 18 + 17 | C2 | J2: separate labels Output + Decoder |
| `Add & Norm` as `Ad & Norm` | 21 | C2 | J2: REAL misread |
| `Read Forward` | 22 | C2 | J2: REAL misread of `Feed Forward` |
| `M Multi-Head Attention` | 4 | C2 | J2: `M ` prefix artifact; header is `Multi-Head Attention` |
| `V K Q` (segmentation) | 6/7/8 | C2 | J2: three separate circle labels read as one line |
| `We ARE HERE` (case) | 29 | C5 | J5: REAL |
| `Aad & Norm` | 21 | C5 | J5: REAL misread |
| `O` | 6 (Q circle) | C5 | J5: misread of the decoder-cross Q circle ~(803,304) `[?]` |
| `Attention` (header line-2 fragment) | 3 | C6 | J6: REAL — lower ~60% of the clipped bold-italic red inset-A header at crop-px x 95–280, y 0–20 |
| `9` | 6 (Q circle) | C7 | J7: NOT visible as `9` — misread of the bottom-right dark-red Q circle, crop-px (504,732)–(558,786) |
| `ked over Multi-Head)` (title fragment) | 2 | C8 | J8: REAL — the clipped red title banner at crop-px (0,5)–(985,85) → frame ≈(518,59)–(846,85), inside the GT title box |
| `Multi-lead Attention` | 4 | C8 | J8: REAL misread of the decoder's Multi-Head Attention box, crop-px (668,645)–(862,718) → frame ≈(741,272)–(805,296) |
| `Fixed Forward` | 22 | C8 | J8: REAL misread of the decoder-top Feed Forward box, crop-px (670,473)–(855,548) → frame ≈(741,215)–(803,240) |

## Recovery accounting (79.3% → 100%)

Wave-2 pass1 alone covers 23/29; missing were GT-5 (Masked Multi-Head Attention),
GT-15 (h), GT-17 (Decoder), GT-21 (Add & Norm), GT-22 (Feed Forward), GT-26 (Output
Embedding). v1 cascade recoveries: GT-17 + GT-21 (C2), GT-15 (C4), GT-5 + GT-22 + GT-26
(C5, C9 corroborates GT-26). C8 confirms GT-17/21/22/5 but adds no new label. Net:
**29/29 labels, union recall 100%** (+20.7 pts vs frozen 79.3%).
