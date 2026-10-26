# Register — slide_052 (doc-parse accuracy audit, wave 2)

Parse: `03_parses/slide_052/call01_pass1/` + `call02_pass2/` (byte-identical, md5 `bdb0e649c4ba8572201ff35d90e80950`)
GT: `04_ground_truth/slide_052/` · Comparison: `05_comparison/slide_052_comparison.md` · Adjudication: `06_vision_checks/slide_052_vision.md` (pixel-grounded: tesseract OCR + thresholded glyph renders + gap/color measurements on the 960×540 frame)

Read labels: every finding below was seen in BOTH passes (byte-identical outputs — the second read is pass2; it cannot falsify pass1) AND adjudicated against the frame by the vision agent's independent pixel inspection — labeled **corroborated (pass2 + pixel adjudication, verdict N)**. No finding rests on a single read.

## BLOCKER

**B1 · No usable layout/structure signal; the one emitted region is hallucinated.** `high` · corroborated (pass2 + pixel adjudication, verdicts 6, 14) · HALLUCINATED (region).
The parse emits exactly 2 positioned items for a 256-element schematic (census: `04_ground_truth/slide_052/build_probe/out/probe.json`), carries exactly one class token — trailing `<class_Picture>` at frame (906.5, 517.6) — and zero structural classes for a pure-diagram slide. Adjudication: nothing pictorial at that point; it lands on the panel's red bottom-border line (y516-517, x58-901) at the black-letterbox junction, ~38 px right of the actual lower-container corner (≈868, 516) → mis-anchored region, not a schematic marker (`05_comparison` claim 6; `06_vision_checks` verdict 6). Defects: **class-token-mismatch** + **hallucinated-content** (region token). A builder gets no container/box/arrow structure at all.

**B2 · Both parse coordinates are mis-anchored — the parser's coordinate frame is systematically offset.** `high` · corroborated (pass2 + pixel adjudication, verdicts 7, 14) · REAL (the mis-alignment is real).
Item 1 (34.7, 41.7) sits in blank white canvas (measured mean 252, std ~1; nearest ink = border-corner AA at x57, y44), ~29 px left / ~20 px up of the callout-1 box corner at (64, 62). Item 2 see B1. Verdict 14: every build-derived coordinate checks out against the image; only the parse's own two anchors mis-measure — "consistent with one systematically offset coordinate frame in the parser". Defect: **coordinate-misalignment**. Consequence: even the 2 coordinates it does emit cannot be trusted without correction.

## MAJOR

**M1 · Five GT string types dropped outright, plus 3 of 5 Q instances.** `high` · corroborated (pass2 + pixel adjudication, verdicts 2, 3, 4, 5, 8) · REAL (the drops).
`K` (red circle 306-327 × 176-199, clear glyph) · `V` (green circle 307-328 × 228-250) · `Y` ×3 (band y247-263, centers x≈85/163/239, OCR "Y Y Y") · `SOS = Start Of Sentence` (legend 64-245 × 485-511, fill ~RGB(233,253,218)) · `52` (yellow badge bbox (858,56)-(893,84), center (875.5, 70.0), glyph render shows "5"/"2") — none appear in the parse; `Q` present only 2× vs 5 circles at x 385/489/601/715/813, y≈254. Defect: **dropped-region**. Wave-1 cites: `05_comparison` §1 MISSING rows; coordinates match `04_ground_truth/slide_052/slide_052.js` (K/V :125-128, Y :214-216, legend :248-249, Q :131-136) and `house_chrome.js` badge (center 893,71 house / 875.5,69.5 measured on this frame).

**M2 · Hallucinated content: standalone "Encoder" ×3.** `high` · corroborated (pass2 + pixel adjudication, verdict 1) · HALLUCINATED (as renderings of the frame).
Parse lines 7/8/11 read `Encoder`; all five upper boxes (y178-244) OCR "Encode" 10/10 across three passes, zero "Encoder". The certified build deliberately preserves the no-"r" spelling (`slide_052.js:117-121`; analysis fix note "verbatim 'Encode', not 'Encoder'"). Defect: **hallucinated-content** (mis-OCR).

**M3 · Both 5×3 stacked box-label grids shredded.** `high` · corroborated (pass2 + pixel adjudication, verdict 9) · REAL (the shredding).
Per-box OCR confirms exactly "Encode | Decoder | Attention" ×5 and "Masked | Multi-Head | Self Attention" ×5 (lower first line yellow-tinted, core ~RGB(178,191,94) rows 356-358). The parse renders the 30 label instances as: 1 merged line `Encode Decoder` + fragments `Encoder`×3/`Decoder`×2/`Attention`×3, 4 whole `Masked Multi-Head Self Attention` lines + 1 fragment `Self Attention`. Defect: **table-structure-loss** (the label grid is a structured 5×3 arrangement reduced to fragment soup). Wave-1: `05_comparison` §1 PARTIAL row + §3 counts.

**M4 · Instance-level coverage ~20-25 of 62 visible text instances cleanly captured.** `med` · corroborated (verdict 13 coverage sweep) · REAL.
Frame carries 29 distinct string types / 62 instances (verdict 13 enumeration); parse misses ≥7 strings outright, drops 3/5 Q, shreds 30 box-label instances, merges I/feel/Sick, degrades the FFN bar. Unit-level text_recall 75.0% (22 dedup units) overstates instance fidelity; the adjudicator's estimate is low-to-medium leaning low. Aggregate defect: **dropped-region**.

## MINOR

**m1 · Verbatim double space before RELU collapsed.** `high` · corroborated (pass2 + pixel adjudication, verdict 10) · REAL.
Image measures a 9.8 px gap before "RELU" vs 3.5-5.5 px for every normal word gap — a genuine double space the certified build preserves verbatim (`slide_052.js:91`); the parse normalizes it to one space and gives no hint of the Courier-New monospace run. Verbatim-whitespace loss (no standard vocabulary term; not math-related, so **math-normalization-loss** does not apply here).

**m2 · "I feel Sick" merged into one line.** `high` · corroborated (pass2 + pixel adjudication, verdict 11) · REAL (the merge is wrong).
Image shows three separate white boxes x72-138 / 148-214 / 224-290, y~444-478 (fill fractions 0.96/0.73/0.71, unfilled gaps between). Parse emits a single line `I feel Sick`. Defect: **table-structure-loss** (box structure flattened).

**m3 · Reading order: no defect charged.** `low` · corroborated (pass2; checked against build fy values) · DEBATABLE.
Parse line order is consistent with a top-to-bottom band sort of the true geometry (callout2 at fy127 correctly falls between the FFN bar fy115 and bar3 fy146); the apparent inversions (`Transformer Encoder` before the masked boxes; `I feel Sick` before the purple bar) involve overlapping y-bands and cannot be proven inversions. No **reading-order-inversion** finding.

**m4 · Checked and cleared:** no **chart-token-pollution** (zero chart tokens; also zero real charts on the slide), no **math-normalization-loss** (no math on the slide beyond the legend equality, whose loss is charged under M1).

## Scores

| Score | Value | Justification |
|---|---|---|
| accuracy | **4/10** | Headline strings verbatim (both callouts, 3 residual bars, FFN bar, purple bar, Transformer Encoder, all 5 word boxes) and passes reproduce exactly — but 5 string types dropped, 3 hallucinated "Encoder" lines, 1 hallucinated region token, both coordinates mis-anchored, instance coverage ~20-25/62. |
| reliability | **8/10** | 2/2 calls EXIT 0 / finish stop / 0 stderr, byte-identical corroboration (J=1.00), no retries — deductions: zero variance means corroboration is blind to the parser's systematic blind spots, and the shared-endpoint latency spread (16.7→52.2 s) shows contention sensitivity. |
| detail | **2/10** | 30 text lines captured but: 2/256 positioned items, 1 class token (hallucinated), no colors/fonts/z-order/counts/geometry; stacked labels shredded; word boxes and input boxes flattened. |
| recreation_power | **1/10** | From this parse alone a builder could typeset ~9 text strings with no positions, sizes, colors or structure; the 256-element schematic — 10 3D boxes, 15 caption bars' styling, 13 token groups, 7 K/V/Q circles, mask-tip counts, grids — is unrecoverable, vs the certified build which encodes all of it. |

## Wave-2 artifact note

`scores_slide_052.csv` (one header + one data line) banked at `08_final/scores_slide_052.csv`; column semantics: `coord_plausible_pct=0` (both anchors adjudicated mis-anchored — raw within-80px fraction was 100% at n=2 pre-adjudication), `layout_roles_detected=0` of 9 analysis `layout.regions` (no parse class token corresponds to any region; the sole region token was adjudicated hallucinated), `hallucinated_confirmed=1`, `finish_all_stop=1`, `corroboration_jaccard=1.00`, `avg_latency_s=34.45`, `avg_out_tokens=145`, `recreation_power_0_10=1`.
