# Round-1 judge transcript — slide_057_vj (doc-parse wave-4)

- Judge: visual-judge comparison mode, Tier-2 gateway leg (`image-analysis/analyze_image/analyze_image.py`, default route `images`, analysis mode, `--timeout 300 --rounds 1 --tries 1`), prompt = `judge/round1_prompt.txt` (frozen vj-r1), transcript = `judge/round1_gateway_transcript.txt` (4091 bytes, coherent body, terminal verdict line present).
- Attempt history: attempt 1 failed (`Response ended prematurely`, no transcript); paced retry after 60 s + successful re-probe. Probe leg: `crop00_probe_legend.png` returned "Encoder/Decoder/Attention" verbatim (matches wave-2 OCR conf 86.1–91.5).
- Measurement legs: wave-2 pixel adjudication `06_vision_checks/slide_057_vision.md` (tesseract native+4x word-TSV, color-mask ink maps, color-cluster censuses — frame px on 960×540) and wave-2 register `07_registers/slide_057_register.md` (frozen inputs, read-only).
- Source image: `videos/deep-learning/002_transformers_part2/unique_slides/slide_057.jpg`, 960×540 RGB, md5 `d785db85444cb3377818caafc05f80a8` (hash recorded before judging; Tier-1 direct Read unavailable in this subagent — model lacks image_in; visual read obtained via Tier-2 gateway leg, disclosed per fallback-ladder law).
- Parse inputs judged: all 6 banked full-frame transcripts (`03_parses/slide_057/call01_pass1`, `call02_pass2`, `call03_retry_pass1`, `call04_retry_pass2`, `call05_t9k`, `call06_t9k_retry`). Wave-3 t9k pair EXISTS and is banked: both calls EXIT=0 (72 s / 75 s) but finish in the SAME 6-unique-line prefix + `Decoder` loop (4490 lines each, 9000-token budget exhausted) — **9000 tokens does NOT break the repetition loop; the failure is budget-independent and content-independent of prompt surface.** Union of all 6 transcripts = the same 6 unique strings.

## Observations

1. The slide is a dense, fully-labeled encoder-decoder Transformer schematic: ~48 distinct text strings at 5–11 pt equivalent, three panels + chrome. Judge-confirmed legible regions include all groups the parse missed (see defects).
2. All 6 parse calls collapsed to a 6-unique-line prefix then a bare `Decoder` loop (×482 @1024, ×1470 @3000, ×4477 @9000); `finish_reason=length` on all 6. The loop word "Decoder" exists on-image only ~17 times; the loop is model degeneration, not invention (`hallucinated_confirmed=0`).
3. The sole coordinate token `<x_0.0586><y_0.0789>57` maps to (56.3, 42.6) — the frame border's top-left corner, ~820 px from the measured badge center (876,70). Anchor artifact, unusable.
4. Gateway judge verified each of the 6 captured strings is genuinely on-image (57, Encoder, Decoder, Encoder Block 2, FFN bar, Residual bar) and that "RELL" is a misread of on-image "RELU" (verified ink at (736,357)); the "/" separator is defensible (on-image separator is a slash-like diagonal, not a flat hyphen).
5. The dense diagram region (all chip rows, word rows, embedding box, decoder bar-stack labels, attention-box text, bottom tokens) is unexplored by the parser in every full-frame call — the loop starves it.

## Defect list

- [HIGH] reliability — deterministic repetition-loop collapse, `finish=length` 6/6 calls, budgets 1024/3000/9000 all identical — (whole frame; loop word "Decoder")
- [HIGH] coverage — 42/48 GT strings lost (12.5% recall); every dropped group re-verified legible on the frame — (frame-wide; wave-2 adjudication verdicts 3–4, 11–13 + judge read)
- [HIGH] encoder bars M/1/0 — only "Encoder Block 2" captured; "Encoder Block M" (~(226,160)), "1" (~(227,299)), "0" (~(225,341)) missed, conf 90–97 on-image — (x~200..448, y~140..360)
- [HIGH] Y-chip row — 8 serif-italic labels Y_0..Y_{N-1} missed — (y~100..130, x~100..440; last chip ~(419,120))
- [HIGH] X-chip row — 8 labels X_0..X_{N-1} missed — (y~455..490, x~100..440)
- [HIGH] word row — "Word 0/1/2/3/4/5/N-2/N-1" missed (red ink, all boxes) — (y~497..513 under encoder panel)
- [HIGH] embedding box — "Word Embedding" (x233..310 y424..431) + "Positional  Encoding / Embedding" (x197..338 y446..454) missed — (x~197..338, y~415..460)
- [HIGH] decoder bar-stack labels — "Softmax" (x594..791 y70..76) missed; 2 of 3 FFN-bar instances uncovered; 7 red-bar instances carry no anchors — (x~594..791, y~70..432)
- [HIGH] attention-box 3-line text — "Encoder / Decoder / Attention" in 15 navy boxes (x586..765, y~179..317) missed — yields GT string `Encoder Decoder Attention` and legend `Attention`
- [HIGH] purple bar — "Word and Position Encoding" (y~487..496) missed — (x~590..800, y~485..500)
- [HIGH] bottom token row — "SOS Je ne suis faisait" (x597..794, y~497..513) missed (glyph blobs verified)
- [MEDIUM] lavender boxes — "Multi-Head / Self-Attention" 5 boxes (y444..463; line-1 ink x589..608) missed — sub-threshold-adjacent but the only label of these boxes
- [MEDIUM] K/V/Q badges — "K=" (~515,160), "V", tiny Qs mid-column, big "Q" (x818..850 y425..455) missed — (central column + decoder bottom-right)
- [MEDIUM] legend "Attention" line — never emitted as a distinct item though on-image at (462,467) conf 86.1 — (x~462..535, y~420..475)
- [MEDIUM] FFN glyph error — "RELL" vs on-image "RELU" — ((736,357), verified ink; misread, not hallucination)
- [MEDIUM] vertical labels unanchored — "Encoder"/"Decoder" strings exist but carry no position; as located content effectively missed — (x73..89 y256..360; x830..855 y225..344)
- [LOW] layout roles 0/6 — zero class tokens, zero regions, one coordinate artifact — (whole frame)
- [LOW] sub-threshold marks — right-margin dark marks x820..840 y263..335, mark at ~(456,486) — correctly skippable (<5 px), not charged

## FINAL VERDICT: FAIL for 'parse captures the slide's renderable text'
