# Register — slide_059 (doc-parse accuracy audit, wave 2)

Scope: `slide_059` · agent `worker-slide_059` · wave-2 banked 2026-10-25.
Inputs: `03_parses/slide_059/{call01_pass1,call02_pass2}/` · `04_ground_truth/slide_059/{inventory.md,slide_059.js,house_chrome.js,slide_059_final.json}` · `05_comparison/slide_059_comparison.md` (claims 1–12) · `06_vision_checks/slide_059_vision.md` (adjudication items 1–15).

Read labels: every parse-side observation is **single-read (degenerate: pass2 byte-identical to pass1)**; frame-side facts are **corroborated** only by the adjudicator's pixel/OCR measurements. Coordinates: frame px `(fx, fy)` from the adjudication; build values are slide-pt (pt-as-px convention, ≤~20 px displacement near the slide bottom — adjudication item 15).

## BLOCKER

**B1 — coordinate-misalignment + class-token-mismatch: 2 positioned items for a 240-shape diagram; 0/2 within tolerance. REAL · confidence HIGH · corroborated (degenerate pass2 + adjudication items 9, 12, 15).**
The parse carries exactly two `<x_…><y_…>` tokens — `call01_pass1/slide_059.parse.md:1,25` → (37.5, 41.7) and (906.5, 517.6) px. The only text-bearing one lands 107.2 px from the nearest GT text box (`05_comparison/slide_059_comparison.md` §2); the other carries only `<class_Picture>` (whole-frame region; nothing textual at the bottom-right corner — adjudication item 12). GT build renders **240** measured items in 14 logical groups (`04_ground_truth/slide_059/inventory.md`). With this output a builder can place nothing. Item-15 caveat (pt-as-px displacement) does not change the 0/2 verdict.

**B2 — math-normalization-loss + hallucinated-content: the subscript/symbol token family destroyed. REAL (DEBATABLE split on 5 of 8 fragments) · confidence HIGH · corroborated (adjudication items 2, 3, 4, 6).**
All 16 X/Y subscript labels (inventory #12–#27) MISSING — emitted as 8 fragments `Yd Xd Xx XN Xt Yk YNz YNd` (`slide_059.parse.md:9–16`); `Σ` ×3 absent in any form though the frame shows white-on-navy Σ in all three circles (adjudication item 4: cx 440/513/585, fy 104–113); subscripts flattened to linear `VectorP0…VectorPn-1` (`slide_059.parse.md:24`). Adjudication item 3 splits the fragments: `XN/YNz/YNd` = real mangles of X_{N-2}/X_{N-1}/Y_{N-2}/Y_{N-1} (fx 760–777, 836–853); `Xd/Xx/Xt/Yk/Yd` match nothing on the slide → invented fragments (HALLUCINATED, advisory). No 2D math survived; even the linear form lost subscript semantics.

## MAJOR

**M1 — hallucinated-content: stray leading "1" in `1C1`/`1C2`; C₃ dropped. HALLUCINATED · confidence HIGH · corroborated (adjudication item 1).**
`slide_059.parse.md:2–3`. The frame shows three clean serif "C"+subscript labels at fx 438–455 / 512–528 / 583–599 with clean background at fx 412–436 — no glyph precedes the band; the "1" is the parser's own subscript misordered in front of the C. C₃ (inventory #11) appears nowhere in the parse.

**M2 — dropped-region: "Softmax" undercount 4→1. REAL · confidence HIGH · corroborated (adjudication item 5).**
`slide_059.parse.md:5` emits only `Softmax Layer`. The frame carries 4 visible "Softmax" strings: yellow in-circle text at fy 92–101 in all 3 circles (blobs poke past circle edges at fx 420–423/458–461) + the orange bar label at fx 182–262 (build `slide_059.js:249–268`). The 3 in-circle strings (inventory #5, ×3) are absent.

**M3 — dropped-region: pooled 20-cell vector row wholly unreported. REAL · confidence HIGH · corroborated (adjudication item 7).**
No parse line describes the row (fy 149–164, fx 389–631); adjudication counts 21 uniform separators at 12.0–12.5 px pitch = exactly 20 cells — build (`slide_059.js:223–229`, POOL_COLORS ×20) wins over the analysis's "~30". The parse missed the row entirely (its only trace is the whole-frame `class_Picture`).

**M4 — table-structure-loss: every stacked label merged to one line. REAL · confidence MEDIUM-HIGH · corroborated (adjudication item 11, psm6 line splits).**
`slide_059.parse.md:6` (`Single vector representing the whole sequence`), `:8` (`Output Sequence`), `:22` (`Word Embedding Vectors`), `:25` (`Position Information Vectors`) merge GT 2–3-line stacks (inventory #36–#45) into single lines; psm6 confirms 3/3/2/2 splits on the frame. Annotation-column line structure is lost.

**M5 — reliability: degenerate corroboration — pass2 byte-identical to pass1. REAL · confidence HIGH · corroborated (empty diff of both `.parse.md`; identical `.parse.json`).**
Raising `--max-output-tokens` 1024→3000 changed nothing (119 < 1024; `finish_reason=stop` voluntary). The second read adds zero independent evidence; every error is double-counted. Jaccard 1.00 is nominal, not probative.

**M6 — hallucinated-content (partial, DEBATABLE split): invented fragments among the 8 garbage tokens — `Xd/Xx/Xt/Yk/Yd`. confidence MEDIUM (7 px glyphs) · DEBATABLE → split REAL-mangles / HALLUCINATED-advisory.**
See B2 and adjudication item 3.

## MINOR

**m1 — Vector_{PN-1} case: parse `VectorPn-1` vs GT capital-N. REAL (build wins) · confidence MEDIUM · corroborated (adjudication item 6: subscript ink fy 490–496; tail widths w≈14 "PN-2" vs w≈11 "PN-1"; 7 px glyph caveat).**
Case-insensitive EXACT stands per the wave-1 scoring contract, but the lowercase n is a real normalization slip.

**m2 — "Transformer Block" captured 3/3 — NOT a miss. REAL · confidence HIGH · corroborated (adjudication item 13(a): upscaled masked OCR reads "Transformer Block" on all three bars, fy 279–297/300–318/352–370).**
`slide_059.parse.md:17,18,20` = GT multiplicity (inventory #2). The wave-2 resume prompt listed "3 Transformer Block labels missed" among adjudication inputs; parse transcript and adjudication both contradict it — recorded here as a resume-prompt transcription slip, not a parse defect.

**m3 — analysis-vs-build settlements banked (GT corrections). REAL · HIGH (item-6 caveat: 7 px glyphs).**
Head subscripts are **0–5** (adjudication item 2: head-1 hollow-oval "0" at fx 217–221/fy 430–434; head-6 solid "5" at fx 583–586) → build code (`slide_059.js:95` `X_SUBS`) right; the build's "X_1..X_6" header comment and the analysis JSON (`X₁..X₅`) wrong. Capital-N Vector tails (item 6) → build `V_SUBS` (`slide_059.js:145`) right. Pooled row **20 cells** (item 7). Ellipsis dot cores dark red (127–157, 0, 15–21), not white (item 8) → build `BARRED` (`slide_059.js:197–204`) right, analysis "white vertical-ellipsis dots" wrong.

**m4 — no reading-order inversion detected. REAL · HIGH · corroborated (degenerate pass2).**
Parse band order (`slide_059.parse.md:1–25`) runs top→bottom consistently with the frame's physical order (adjudication item 9: lilac input fy 385–512 → bars 276–371 → Output/Sequence 226–259 → GAP 184–207 → pooled 149–164 → softmax 91–111 → circles → classes 55–71). The defect vocabulary's reading-order-inversion is unused: the parse flattens rather than inverts.

**m5 — inherent omissions (detail, not a discrete defect): zero color, font, z-order, shape-type, dash or multiplicity information anywhere in the parse; badge numeral `59` captured as bare text (`slide_059.parse.md:4`; adjudication item 10: badge fill bbox fx 859–892/fy 57–85, FDFD96 + 6A5ACD ring, letterform + OCR "59", no other digits). MINOR · HIGH.**

## Resume-prompt reconciliation note

The wave-2 resume prompt lists two adjudication inputs absent from this scope's record: (a) "3 Transformer Block labels missed" — contradicted by `slide_059.parse.md:17,18,20` and adjudication item 13(a) (see m2); (b) "bottom tokens labeled SOS/Je/ne/suis/faisait per build" — no such strings exist in this scope's build, analysis, parse, or adjudication file; apparent cross-scope contamination from another slide's claims. Neither was acted on; this register is grounded solely in `06_vision_checks/slide_059_vision.md`.

## Scores (0–10)

- **accuracy: 4/10** — the big prose labels are verbatim (Output Classes, Global Average Pooling, Input Sequence, Transformer Encoder, 3× Transformer Block, Softmax Layer, 59), but 23 math/subscript-family strings (16 X/Y + Σ×3 + in-circle Softmax×3 + C₃) are garbled or absent, one hallucination group is confirmed, and coverage is ~40–55% of the adjudicator's 43 visible strings.
- **reliability: 5/10** — mechanically flawless (both calls EXIT=0, finish=stop, 0 stderr lines, deterministic), but degenerate: the identical 119-token output at both token budgets shows one rigid mode, no corroboration value, and no recovery path from its subscript weakness.
- **detail: 2/10** — 2 coordinate tokens for 240 shapes, 1 whole-frame region class, no colors/fonts/counts/structure; every multi-line label stack flattened.
- **recreation_power: 2/10** — a builder could recover only the flat prose strings; positions (2 unusable points), the pooled row, circles/Σ, the whole subscript label family, colors and multiplicities are absent vs the certified build's 240 measured items.
