# Round-2 judge transcript — slide_057_vj (doc-parse wave-4)

- Judge: comparison mode, Tier-2 gateway leg (default route `images`, `--timeout 300 --rounds 1 --tries 1`), prompt = `judge/round2_prompt.txt` (frozen vj-r2), transcript = `judge/round2_gateway_transcript.txt` (4890 bytes, coherent body, terminal verdict line). Single attempt, no retries.
- Round-2 crop parses banked (all finish=stop): `parses/call05_round2` (crop05_ychips_row, 26 tok), `call06_round2` (crop06_xchips_wordrow, 74 tok), `call07_round2` (crop07_dec_tokens, 10 tok), `call08_round2` (crop08_kv_central, 9 tok).

## Observations

1. Judge verified every still-missed group present on-image with tight re-crop boxes; realistic ceiling ~38–41/48 (~80–85%) — Softmax (~4 px ink), tiny mid-column Q's, and lavender 2-line text judged below source legibility (upscaling cannot recover unrendered information).
2. crop05 (Y-chip row strip, 1167×138): read "Yo Y1 Y2 Y3 Y4 Y5 ..... YsN Yn1" — **7 of 8 Y-chips matched** (Y_1..Y_5 literal after subscript-collapse; Y_0 via o/0 glyph confusion; Y_{N-1} via "Yn1"); Y_{N-2} garbled as "YsN" (below the ≥60% token threshold — stays MISSING, near-miss documented).
3. crop06 (X-chips+word row, 1167×210): parser latched onto the embedding title inside the crop's top edge and emitted a "lollipop chart" scaffold: title "Positional Encoding / Embedding" (already matched) + rows "Wired 0..5, Wired N-2, Wired N-2" — "Wired" is a word-shape misread of "Word" (2-char insertion; below the PARTIAL threshold → the 8 word-row strings stay MISSING, near-miss documented); X-chip labels skipped entirely.
4. crop07 (decoder token strip, 897×99): emitted only "Word and Position Encoding" (the purple bar, already matched); the 5 token labels (~5–6 px glyphs) skipped again.
5. crop08 (K/V central, 345×495): "K" + "V" — both EXACT, 2 new GT strings.
6. Judge-charged round-1 read errors, adjudicated: "Encode"→"Encoder" truncation MEDIUM (real; line-1 ink to x608); FFN "[" separator LOW — **two reads disagree** (wave-2 ink-map measured a slash-like diagonal at x≈670–672; round-2 judge says no bracket glyph) → advisory only, never a charged defect (verdict law).

## Defect list (post-round-2 state)

- [HIGH] X-chip row (y455..490, x100..440) — 8 strings present, never read in any call; crop06 wrapped the region in chart scaffold — evidence: crop06 output has no X labels.
- [HIGH] word row (y492..513, x100..440) — 8 strings misread "Wired N" (word-shape error), 0 matched — evidence: crop06 table rows vs GT "Word N"; wave-2 OCR read red ink in all boxes.
- [HIGH] bottom token row (x597..794, y497..513) — "SOS/Je/ne/suis/faisait" skipped in crop04 and crop07 despite in-crop — evidence: glyph blobs y498..504, runs 3/2/2/4/7.
- [HIGH] Y_{N-2} (chip 7, ~(384,120)) — garbled "YsN" in crop05 — near-miss, single-read.
- [MEDIUM] big "Q" badge (x818..850, y425..455) — judge-verified fully legible, never crop-targeted — evidence: 48 dark-red ink px.
- [MEDIUM] "Softmax" (x681..705, y71..75) — in-crop miss in crop03; judge assesses below source legibility (~4 px ink) — park-never-drop.
- [MEDIUM] lavender "Multi-Head / Self-Attention" (y444..463) — line ink ~4–5 px, below source legibility per judge — park-never-drop.
- [LOW] tiny mid-column Q's (x~500..530) — below legibility — park-never-drop.
- [LOW] coordinate tokens — all crop calls emit corner artifacts (x_0/y_0 → x_0.999/y_0.9992); region-targeted parsing still yields no usable geometry on this slide.

## FINAL VERDICT: FAIL for 'parse captures the slide's renderable text'
