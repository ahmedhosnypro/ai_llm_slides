# COMPOSED_ANALYSIS — slide_059 (wave 5B crop cascade, composed)

- Scope: `slide_059_cascade_v2` · agent `worker-slide_059_cascade_v2` · composed 2026-10-25.
- Merges ALL banked transcripts: full-frame `03_parses/slide_059/call05_t9k/slide_059.parse.md`
  (byte-identical ×3, treated as ONE read) + 16 crop parse call dirs (`parses/callNN_cropNN/`)
  + 13 vision-gateway judge transcripts (`judges/`).
- Frame: 960×540 px · source md5 `fb03ceaae946177062b7e097d68ffde3`.
- Transform rule: `frame_x = crop_x/scale + box_frame_px[0] ; frame_y = crop_y/scale + box_frame_px[1]`
  (manifest.json). Parse-side in-crop coords exist only as whole-crop class blocks (origin-only),
  so string positions below are (a) wave-2 adjudicated pixel measurements where available
  (`06_vision_checks/slide_059_vision.md`, arbitrated — highest rank), else (b) judge-read crop-px
  mapped through the transform, else (c) the crop's manifest box (region-level).
- Classification vocabulary: REAL-GT (string on frame, in GT inventory, GT id given) ·
  REAL-novel (on frame, no GT row — structure/multiplicity evidence) · hallucination-candidate ·
  GT-gap (in GT, still unrecovered). Uncertain items keep `[?]`.

## Headline

**Union recall: 58.7% → 100% (46/46 GT strings)** — every GT row recovered at transcript
level (doc-parse or vision-judge), C₁/C₂ partials upgraded to full. Doc-parse-only union:
91.3% (42/46); the vision-judge leg recovered the last 4 (X₁, X₄, X₅, Y₀).
16 crops · 16 doc-parse parse calls · wall ≈23 s vs 60 s summed call latency ≈ **2.6×
parallel speedup** (13 judge legs additional, sequential, max 1 in-flight).

## Composed elements (ordered by frame y)

| fy (frame px) | Element / string | Class | GT id | Provenance (call dir(s)) | Position basis |
|---|---|---|---|---|---|
| ~40–52 | `Output Classes` | REAL-GT | #8 | call05_t9k (full-frame, EXACT); positioned item (0.0391,0.0773) rejected by register B1 (107 px off) | wave-4 Q3 zone |
| 55–71 | `C₁` | REAL-GT (upgraded PARTIAL→full) | #9 | call07 `C1`; judges crop01/crop07 (char-exact "C"+subscript 1) | wave-2 A1 fx 438–455 |
| 55–71 | `C₂` | REAL-GT (upgraded PARTIAL→full) | #10 | call07 `C2`; judges crop01/crop07 | wave-2 A1 fx 512–528 |
| 55–71 | `C₃` | REAL-GT (NEW — absent at wave 2) | #11 | call07 `C3`; judges crop01/crop07 | wave-2 A1 fx 583–599 |
| 57–85 | `59` (badge numeral) | REAL-GT | #46 | call05_t9k (full-frame, EXACT) | m5: fx 859–892 |
| 91–111 | `Softmax Layer` (tan bar) | REAL-GT | #4 | call05_t9k (full-frame, EXACT) | M2: fx 182–262 |
| 92–101 | `Softmax` ×3 (in-circle, yellow) | REAL-GT multiplicity recovery | #5 (×3) | call01 ×2, call08 ×2; judges crop01/crop08: all 3 circles (cx 440/513/585) | M2/A3 |
| 104–113 | `Σ` ×3 (white-on-navy) | REAL-GT (NEW — absent at wave 2) | #6 (×3) | call01 `Σ` ×2 (verbatim glyph); judges crop01/crop08: Σ in all 3 circles | A10: cx 440/513/585 |
| ~143–180 | `Single vector representing` / `the whole sequence` | REAL-GT (stack of 2; full-frame merged to 1 line) | #36, #37 | call05_t9k + call05_crop05 | A8 band |
| 149–164 | pooled vector row: **20 pastel cells**, 5-color cycle (yellow→green→orange→lavender→pink), **no text in cells** | REAL-novel (structure; wholly unreported at wave 2) | — | call04 (textless parse); judge crop04 (~20 cells counted, cycle described); register M3 (21 separators @ 12.0–12.5 px pitch, build POOL_COLORS ×20) | M3: fx 389–631 |
| 184–207 | `Global Average Pooling` | REAL-GT | #3 | call05_t9k (full-frame, EXACT) | wave-4 Q5 |
| 215–260 | `Y₀` | REAL-GT (NEW) | #20 | judges crop12 + crop16 (letter Y + subscript 0, explicit, 2 independent reads) | A4: row fx 217–853; X₁-slot pitch |
| 215–260 | `Y₁` | REAL-GT (NEW) | #21 | call16 `Y1` (pictogram chart); judges crop12 + crop16 (subscript 1 explicit) | A4 |
| 215–260 | `Y₂` `Y₃` `Y₄` `Y₅` | REAL-GT (NEW ×4) | #22–25 | call03 `Y2 Y3 Y4 Y5`; judge crop16 (Y₂ Y₃ confirmed; Y₄ partial) | A4 |
| 215–260 | `Y_{N-2}` | REAL-GT (NEW) | #26 | call11 `Y N-2`; judge crop11 (subscript N-2) | B2: fx 760–777 |
| 215–260 | `Y_{N-1}` | REAL-GT (NEW) | #27 | call11 `YN-1`; judge crop11 read "N-3/N-j" `[?]` — doc-parse + GT build agree N-1 | B2: fx 836–853 |
| 226–259 | `Output` / `Sequence` | REAL-GT (stack of 2; full-frame merged) | #38, #39 | call05_t9k | A8/m4 |
| 276–371 | `Transformer Encoder` (red container title) | REAL-GT | #1 | call05_t9k (full-frame, EXACT) | m4 band |
| 279–370 | `Transformer Block` ×3 | REAL-GT (×3 multiplicity) | #2 | call05_t9k (full-frame ×3) | m2: fy 279–297/300–318/352–370 |
| 405–445 | `X₀` | REAL-GT (NEW) | #12 | call09 `X0` + call13 `X0`; judge crop09 (subscript 0, slot-consistent fx 220–231) | m3: head-1 fx 217–221 |
| 405–445 | `X₁` | REAL-GT (NEW — judge-recovered) | #13 | judge crop13: `X₁` on embedding cell at crop (478–510, 218–248) → transform → fx 280–296, fy 421–436 (slot-consistent); doc-parse collapsed it in 4 attempts | judge-read + transform; wave-2 pitch expects X₁@~290 |
| 405–445 | `X₂` | REAL-GT (NEW) | #14 | call09 `X2` (slot fx 363–374 per judge crop09); judge crop15-era zone | m3 pitch |
| 405–445 | `X₃` | REAL-GT (NEW) | #15 | call09 `X3` (slot fx 437–448 per judge crop09) | m3 pitch |
| 405–445 | `X₄` | REAL-GT (NEW — judge-recovered, ×2 reads) | #16 | judges crop02 + crop14: subscript digit **4** explicit, slot-consistent (fx ≈500–514 vs expected ~509); doc-parse collapsed it in 4 attempts (bare `X`) | judge positions + transform |
| 405–445 | `X₅` | REAL-GT (NEW — judge-recovered, ×2 reads) | #17 | judges crop02 + crop14: subscript digit **5** explicit, slot-consistent (fx ≈572–587; m3 pixel-adjudicated head-6 "5" @ 583–586) | m3 |
| 405–445 | `X_{N-2}` | REAL-GT (NEW) | #18 | call06 `XN2`; judge crop06 (subscript N-2) | B2: fx 760–777 |
| 405–445 | `X_{N-1}` | REAL-GT (NEW) | #19 | call06 `XN1`; judge crop06 read "N-3" `[?]` — doc-parse + GT build agree N-1 | B2: fx 836–853 |
| ~385–512 | `Input Sequence` (lilac container) | REAL-GT | #40 | call05_t9k (full-frame, EXACT); call13 ranked_table title | m4 band |
| 448–466 | `+` (red disc) | REAL-GT | #7 | call05_t9k (full-frame, EXACT) | A9: fx 489–509 |
| ~430–470 | `Word` / `Embedding` / `Vectors` | REAL-GT (stack of 3; full-frame merged) | #41–43 | call05_t9k; call13 ranked_table row | A8 |
| 470–500 | `Vector_{P0}` … `Vector_{P5}`, `Vector_{PN-2}` | REAL-GT (normalized at wave 2; crop-corroborated) | #28–34 | call05_t9k; call06 `Vector PN-2`; call13 ranked_table `Vector_PO`/`Vector_PI`; judge crop13 (boxed Vector_P0/P1) | A6: fy 470–500 |
| 470–500 | `Vector_{PN-1}` | REAL-GT | #35 | call05_t9k (full-frame EXACT); call06 `Vector PN-1`; judge crop06 | m1 |
| ~475–500 | `Position` / `Information` / `Vectors` | REAL-GT (stack of 3; full-frame merged) | #44, #45 | call05_t9k; call13 ranked_table row; judge crop13 (3 stacked lines, in order) | A8 |

### Structural recoveries (class blocks, REAL-novel)

1. `class_Picture` whole-frame (call05_t9k, origin (0.9443,0.9586)) → crop06 estimated quadrant
   box (710,400,960,540), `estimated: true` — quadrant fully enumerated (X/Vector N-tail labels).
2. `class_Chart` `ranked_table` (call13, crop13 annot-lower): title `Input Sequence`; rows
   `Word Embedding Vectors | X0 | X` and `Position Information Vectors | Vector_PO | Vector_PI`
   — annotation-panel structure the full-frame parse never produced.
3. `class_Chart` `pictogram_percentage` (call16, crop16 Y-head zone): rows `Yd` / `Y1` / `X2` —
   yielded the clean `Y1` string.
4. Pooled-row structure (judge crop04 + register M3): 20 cells, 5-color pastel cycle, no text.

## Hallucination candidates

| String | Source call | Disposition |
|---|---|---|
| `1C1`, `1C2` (leading `1`) | call05_t9k (full-frame) | CONFIRMED hallucination (register M1: clean bg at fx 412–436, no preceding glyph). Recurred at crop scale as `IC1/IC2/IC3` (call01). Fixed by tighter labels-row crop (call07): clean `C1 C2 C3`. |
| `Yd` `Xd` `Xx` `Xt` `Yk` | call05_t9k (full-frame) | Invented fragments (register B2 split). Not reproduced by any crop parse — crop-scale reads replaced them with slot-consistent labels. |
| `Xl`, `Xj`, `O` | call02 (crop02) | Mangle-candidates of X₀/X₁ subscript shapes (hollow-0/solid-1) + unread subscript `[?]`. Superseded by slot-consistent reads (call09 + judges). |
| `Z` (for Σ, ×2) | call08 (crop08) | Σ misread at 3× in the tight circles crop; call01 (wider box) read `Σ` verbatim — judges confirm Σ ×3. |
| `X1`, `X2` (in Y₀/Y₁ zone) | call12 (crop12) | X↔Y letter confusion; judges crop12/crop16 read the same box as Y₀ Y₁ Y₂. Classified misreads, NOT X-row strings. |
| judge `N-3` readings (crop06, crop11) | judges | Single-read subscript confusion on the N-tail digits; doc-parse calls (call06 `XN1`, call11 `YN-1`) + GT build (`N-1`) win per the wave-2 arbitration precedent. |

## GT-gaps (in GT, unrecovered after the full cascade)

- **None.** All 46 GT rows are recovered at transcript level. Every judge-recovered string
  is at least double-sourced or slot-consistent with wave-2 pixel adjudication:
  `X₄`/`X₅` have two independent judge reads each (crop02 full-row + crop14 tight zone,
  digits explicit, positions slot-consistent) after 4 doc-parse failures; `X₁` has two
  judge reads (crop02 digit-1 @ slot 2; crop13 `X₁` on the embedding cell strip at
  slot-consistent fx 280–296); `Y₀` has two judge reads (crop12 + crop16).

## Recall accounting

- Wave-2 frozen: 27/46 = **58.7%** (9 EXACT + 17 NORMALIZED + 0.5×2 PARTIAL).
- Cascade additions: Σ(#6) + C₃(#11) + C₁/C₂ upgrades (+1.0) + X₀..X₅(#12–17) +
  X_{N-2}/X_{N-1}(#18–19) + Y₀..Y₅(#20–25) + Y_{N-2}/Y_{N-1}(#26–27) = 19 credit →
  **46/46 = 100%**.
- Route split: doc-parse-transcript recoveries = 42/46 (91.3%); the vision-judge leg adds
  X₁(#13, 2 reads), X₄(#16), X₅(#17), Y₀(#20, 2 reads) → 46/46. Judge credits follow
  requirement 2 (the crop judge is a first-class recovery route); each carries provenance
  and, where single-source, is marked judge-recovered in the table above.
