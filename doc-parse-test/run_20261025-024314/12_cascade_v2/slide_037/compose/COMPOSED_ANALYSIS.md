# COMPOSED_ANALYSIS — slide_037 (worker-slide_037_cascade_v2, wave 5B)

**Headline: union recall 100% (29/29 GT labels) vs frozen wave-2 recall 79.3% (23/29).**
Merge of the full-frame pass1 transcript + 7 crop parses (2 levels of recursion) + 5
vision-gateway judge transcripts. Deduped at label level; positions are frame px
(960×540) via the manifest transform `frame_x = crop_x/scale + box.x0; frame_y =
crop_y/scale + box.y0`, anchored to the GT inventory's authoritative positions when
REAL-GT. `[?]` marks judge-reported approximations (±15 px).

Provenance keys: **P1** = `03_parses/slide_037/call01_pass1` (full frame) ·
**C1..C7** = `parses/call_crop01..call_crop07` · **J2,J4..J7** =
`judges/judge_crop02,04,05,06,07.md` (vision gateway). GT ids = the 29 inventory ids in
`04_ground_truth/slide_037/inventory.md`.

## Merged elements, ordered by frame y

| y (frame px) | Element (verbatim) | Classification (GT id) | Provenance | Notes |
|---|---|---|---|---|
| 50–100 | `Transformer Blocks (stacked over Multi-Head)` | REAL-GT (2) | P1, C1 | C1 read exact; block (75,53)–(921,91) class Page-header |
| 53–89 | `37` (badge numeral) | REAL-GT (1) | P1, C1 | exact in C1 |
| 112 | `Encoder` (red italic panel label) | REAL-GT (16) | P1, C2, C5, C6 | J6 ~30%,10% of C6 → ≈(588,132) `[?]` |
| 112 | `Output` (yellow band) | REAL-GT (18) | P1, C5, C7 | |
| 112 | `Decoder` (green italic panel label) | REAL-GT (17) | **C2, C5, C7** | RECOVERED by cascade (absent from P1); J5 ~82%,10% |
| 127 | `Probabilities` | REAL-GT (19) | P1 (+J5) | P1 is the only doc-parse read that caught it; J5 confirms printed in C5 region ~(63%,13%) → ≈(769,132) |
| 152 | `Softmax` (decoder box) | REAL-GT (20) | P1, C5, C7 | C5/C7 give clean case; J5/J7 confirm |
| 177–206 | `WE ARE HERE` (3 lines, rotated 342°) | REAL-GT (29) | P1, C2, C5, C6 | case variants `We ARE HERE`/`We Are HERE` in C5/C6 = same label; J2 ~66%/22–30% of C2 → ≈(611,178) |
| 206–342 | `Add & Norm` (4 visible instances: enc 653,277 · dec-steel 753,206 · dec-steel 753,263 · dec-indigo 753,329; 5th occluded under disc) | REAL-GT (21) | **C2 ×3, C5 ×3, C7 ×3** | RECOVERED (absent from P1); garble variants `Aad & Norm` (C5), `And & Home` (C6), `Add A Norm`/`Ass & Norm` (C7) all judged REAL misreads of GT-21; J7: all 3 decoder boxes present |
| 210 | `Multi-Head Attention` (inset-B header, bold italic red) | REAL-GT (4) | P1, C4 | C4 Section-header exact (320,191)–(454,209); encoder box inst. C5/C6; decoder box inst. C2 garble `Must-Head Attention` → J2 REAL misread ~83%/44% of C2 → ≈(762,274) |
| 227 | `Scaled Dot-Product Attention` (inset-A header + SDPA box in inset-B) | REAL-GT (3) | P1 ×2, C3, C4 | P1 garble `Scalar Dot-Product Attention` = same label |
| 266–403 | `Linear` ×5 (inset-B ×3 bottom + top 364,266 + decoder 752,177; inset-B 309/359/416,403) | REAL-GT (14) | P1, C4 ×3, C5, C7 | C4 reads all 3 inset-B bottom instances |
| 292–318 | `Feed Forward` ×2 (enc 654,292 · dec 753,223) | REAL-GT (22) | **C5 ×2, C6, C7** | RECOVERED (absent from P1); J5 confirms both |
| 348 | `Masked Multi-Head Attention` (748,348) | REAL-GT (5) | **C5** | RECOVERED (P1 garble `Math-Head Attention` only); C7 garble `Masked Murti Head Attention` judged REAL misread |
| 312 | `Concat` (364,312) | REAL-GT (13) | P1, C4 | J4 confirms yellow box |
| 330 | `SoftMax` (inset-A box 80,330) | REAL-GT (12) | P1, C3 | C3 exact case |
| 294–429 | `MatMul` ×2 (76,429 · 105,294) | REAL-GT (9) | P1, C2, C3 ×2 | P1 garble `Max` = same label |
| 357 | `h` (brace label, italic, 484.5,357.5) | REAL-GT (15) | **C4** | RECOVERED (absent from P1); J4 CONFIRMED: italic h labeling the brace of the h-head stack, ~88–90% left/54% top of C4 → ≈(500,362) `[?]` |
| 363 | `Mask (opt.)` (77,363) | REAL-GT (11) | P1, C2, C3 | |
| 397 | `Scale` (93,397) | REAL-GT (10) | P1, C3 | |
| 416–447 | `Positional Encoding` ×2 (594,416 · 836,419) | REAL-GT (24) | P1 ×2, C2 ×2, C5 ×2, C6, C7 | |
| 446–471 | `Input Embedding` (653,446) | REAL-GT (25) | P1, C2, C5, C6 | |
| 446–471 | `Output Embedding` (756,446) | REAL-GT (26) | **C2, C5, C7** | RECOVERED (absent from P1); J2 confirms two-line label |
| 494 | `Inputs` (664,494) | REAL-GT (27) | P1, C2, C5, C6 | |
| 492–522 | `Outputs` + `(shifted right)` (761,492 · 748,508) | REAL-GT (28) | P1, C2, C5, C7 | C5/C7 read the composed single line |
| 311–494 | `Q`/`K`/`V` circle letters, 5 sets (15 circles) | REAL-GT (6) | P1 `Q K V`, C2, C3, C4, C6 `V K Q` | C5 `V K O` — J5: `O` = misread of the decoder-cross **Q** circle; C7 `V`+`Y` — J7: `Y` = misread of the decoder-masked **V** circle |
| 300–330 | `N x` ×2 (597.5,329.5 · 845.5,300.5) | REAL-GT (23) | P1 `Nx`, C2, C5, C6 (partial `N`), C7 | J5: left Nx occluded (only `N` shows) — matches GT occlusion note |

## Hallucination candidates (parsed strings with nothing printed on the slide)

| String | Provenance | Judge verdict | Position |
|---|---|---|---|
| `Create` | C2 (`parses/call_crop02`) | J2: **NOT-IN-GT** — "Nothing resembling 'Create' is printed anywhere in the crop" | n/a (hallucinated) |
| `October 1 March` | C6 (`parses/call_crop06`) | J6: **NOT-IN-GT** — "No such printed text; hallucinated/OCR garbage" | n/a (hallucinated) |

Both strings are excluded from the union count; they are doc-parse hallucinations at
zoom, caught and quarantined by the judge step.

## GT-gaps (real-on-image strings absent from the inventory)

**None found.** All 29 GT ids are recovered by the union; the 5 vision judges found no
printed string on any crop that the inventory lacks. The bottom video-player UI strip
(frame y > 516) is excluded from crops by design (GT: video UI, not slide content) and
carries no text claims.

## Garble ledger (novel parsed strings that are OCR misreads of real GT text)

| Garble | Maps to GT | Where read | Judge |
|---|---|---|---|
| `Scalar Dot-Product Attention` | 3 | P1 | — (obvious) |
| `Mult-Head Attention` / `Math-Head Attention` | 4 / 5 | P1 | — (obvious) |
| `Max` | 9 | P1 | — (obvious) |
| `Must-Head Attention` | 4 (dec box) / 5 | C2, C6 | J2/J6: REAL misread |
| `Aad & Norm` | 21 | C5 | J5: REAL misread |
| `And & Home` | 21 | C6 | J6: REAL misread |
| `Add A Norm` / `Ass & Norm` | 21 | C7 | J7: REAL misreads (2 of 3 decoder boxes, dimmed under overlays) |
| `Murti-I lead Attention` | 4 | C7 | J7: REAL misread |
| `Masked Murti Head Attention` | 5 | C7 | J7: REAL misread |
| `O` | 6 (Q circle) | C5 | J5: misread of Q circle ~(803,304) `[?]` |
| `Y` | 6 (V circle) | C7 | J7: misread of V circle ~(741,383) `[?]` |
| `We ARE HERE` / `We Are HERE` (case) | 29 | C2, C5, C6 | J2/J5/J6: REAL |

## Recovery accounting (79.3% → 100%)

Wave-2 pass1 alone covers 23/29; missing were GT-5, 15, 17, 21, 22, 26. Cascade
recoveries: GT-17 + GT-21 + GT-26 (C2), GT-15 (C4), GT-5 + GT-22 (C5). Net: **29/29
labels, union recall 100%** (+20.7 pts vs frozen 79.3%).
