# COMPOSED ANALYSIS — slide 052 (wave 5B requirement-compliant crop cascade)

Scope `slide_052_cascade_v2` · frame 960×540 · source `videos/deep-learning/002_transformers_part2/unique_slides/slide_052.jpg`
Region source: full-frame `03_parses/slide_052/call05_t9k/slide_052.parse.md` (md5 `bdb0e649…`, byte-identical to call01_pass1/call02_pass2 — one transcript).
Merged evidence: full-frame transcript + 17 crop-parse call dirs (this tree `parses/`) + 12 vision-gateway judge transcripts (`judges/`).
Transform contract (manifest.json, per crop): `frame_x = crop_x/scale + box.x0; frame_y = crop_y/scale + box.y0`.

## Headline

**Union recall 75.0% → 90.9% transcript-level** (20 EXACT + 0 NORMALIZED + 0 PARTIAL + 2 MISSING of 22 GT units; wave-2 basis) — **judge-corroborated coverage 22/22 = 100.0%** (the 2 transcript misses, K and V, are REAL on image per 3 independent gateway judges each; doc-parse cannot read them at compliant crop scales). 16 crops (cap 16), 17 parse calls (cap 24), parallel speedup ~2.5×.

Trajectory: wave-2 full-frame 75.0% → cascade level-1 +2 units (GT9, GT22) & GT5 PARTIAL→EXACT → level-2/3 +GT21 (clean `Y`) → 90.9% transcript / 100% judge-corroborated.

## Composed elements — ordered by frame y

Positions: `[parse]` = coordinate token carried by a transcript (×960/×540); `[box]` = localized by the crop's manifest box; `[judge]` = crop-px position from a judge transcript mapped through the transform (judge-estimated, ±). Classification per brief: REAL-GT / GT-gap / hallucination-candidate.

| y (frame px) | element | classification | GT id | provenance | evidence |
|---|---|---|---|---|---|
| 41.7 | `F2` | hallucination-candidate | — | full-frame t9k L1 `[parse]` | single-read; no GT match; callout-1 zone; no judge run (unit-count impact zero) |
| 56–84 | `52` badge | REAL-GT | GT22 | `call06_crop06_badge` `[box]` + judges/crop06_judge.md `[judge]` | judge: "the yellow circular badge clearly prints the number 52" |
| 62–107 | `Multi-head Encoder-Decoder Attention Block` (callout 1) | REAL-GT | GT1 | full-frame t9k L2 `[box]` | EXACT |
| 84 | `Residual Connection and Layer Normalization` (upper bar 1) | REAL-GT | GT3 | full-frame t9k L3 `[box]` | instance 1/3 |
| 116 | `Feed Forward Networks [ One Hidden with RELU Activation]` | REAL-GT | GT4 | full-frame t9k L4 `[box]` | EXACT (whitespace-insensitive) |
| 127–178 | `Masked Multi-head Self Attention Block` (callout 2) | REAL-GT | GT2 | full-frame t9k L5 `[box]`; tail fragments read by crop09/crop14 judges | EXACT; its right tail entering crop09/crop14 produced the garbles below |
| 146 | `Residual Connection and Layer Normalization` (upper bar 2) | REAL-GT | GT3 | full-frame t9k L6 `[box]` | instance 2/3 |
| ~150–165 | `October 1` | **hallucination-candidate → judge-confirmed ABSENT** | — | `call02` + `call14` (byte-identical md5 `ec11ed28…`) | judges/crop02_judge.md: "no 'October 1' anywhere… OCR hallucination"; corroboration stable ×2 |
| 178–243 | `Encode`/`Decoder`/`Attention` ×5 stacks | REAL-GT | GT5 | full-frame fragments (L7–L15 shredded) + `call02` 4 complete lines + `call07` ×1 + `call12` ×3; judges/crop02_judge.md `[judge]` | **EXACT (upgraded from wave-2 PARTIAL)**; 5/5 stacks REAL; judge: "exact first label line of every stack is 'Encode' — 5× 'Encode', 0× 'Ende', 0× 'Encoder'" |
| 178–243 | `Ende Decoder Attention` | NOT-IN-GT garble | — | `call02` + `call14` | judge: all stacks read "Encode" — misread of stack line 1 |
| 178–243 | `Encoder` ×3 (standalone) | **hallucination-candidate (register-confirmed)** | — | full-frame t9k L8/L9/L12 | frozen wave-2 register lists standalone "Encoder" as confirmed hallucination; re-appearance treated as candidate, not gain |
| ~187 | `K` (red circle, white K) | REAL-GT — **doc-parse MISSING at transcript level** | GT18 | judges/crop02, crop09, crop14 `[judge]` | three judge convergences: frame ≈(316,187)/(316,188); GT build center (316.5,187.5). 4 compliant crop parses read everything except K |
| ~239 | `V` (green circle, white V) | REAL-GT — **doc-parse MISSING at transcript level** | GT19 | judges/crop02, crop09, crop15 `[judge]` | frame ≈(317,239); GT build center (317.5,238.5) |
| ~253 | `Q` ×5 (blue circles) | REAL-GT | GT20 | full-frame ×2 (L16/L17) + `call07` ×1 + judges/crop02, crop12 `[judge]` | unit EXACT; transcript instances 3/5; judge: 5 circles, centers frame ≈(382/487/596/714/813, 253) — matches build x≈385/489/601/715/813 |
| 247–263 | `Y` ×3 (red tags) | REAL-GT | GT21 | full-frame: none; `call10` clean `Y` line + `call08` `Ya`/`Y2` + judges/crop08, crop10 | **EXACT (clean single-token line)**; judges: 3 tags exist (parse caught 2); tag x pitch ≈78px matches build (85/163/239). Suffix readings `Ya`/`Y1`/`Y2` on-image are a 2-judge single-read observation conflicting with the certified build's plain `Y` — kept `[?]`, flagged for pixel adjudication |
| 299–419 | `Transformer Encoder` | REAL-GT | GT8 | full-frame L19 + `call05` `[box]` | EXACT |
| ~312 | `Residual Connection and Layer Normalization` (lower bar) | REAL-GT | GT3 | full-frame L18 + `call03` `[box]` | instance 3/3 |
| 344–384 | `Masked`/`Multi-Head`/`Self Attention` ×5 stacks | REAL-GT | GT6 | full-frame ×4 (L20–L23) + `call03` ×4 + `call13` 5th fragments + judges/crop13_judge.md | EXACT; 5/5 instances covered (5th garbled but judge-verified: "exactly Masked (yellow) / Multi-Head / Self Attention") |
| 443–473 | `I` / `feel` / `Sick` (3 input boxes) | REAL-GT | GT10/11/12 | full-frame merged line L25 (wave-2 basis: merged members EXACT) + `call05` `feel`/`Sick` split + `call17` `feel` + judges/crop05, crop16 | judges: 3 boxes read I / feel / S(ick, clipped); "I" parser-omitted in split reads, visible on image |
| 454 | `Word and Position Encoding` | REAL-GT | GT7 | full-frame L26 + `call04` `[box]` | EXACT |
| 444–470 | `SOS` `Je` `me` `sens` `malade` (word boxes) | REAL-GT | GT13–17 | full-frame L27–L31 + `call04` (merged 2-per-line) | all 5 EXACT; line-merge = structure-only defect |
| 485 | `SOS = Start Of Sentence` | REAL-GT | GT9 | `call05_crop05_leftpanel` `[box]` + judges/crop05_judge.md | **recovered by cascade** (MISSING in all full-frame passes); judge: text exact, S/O/S initials underlined |
| 490–499 | `nalade` | NOT-IN-GT garble | — | `call01` `[judge]` frame (796–830, 490–499) | judges/crop01_judge.md: left-clipped tail of `malade` (GT17); glyphs real, string not |
| 517.6 | `class_Picture` region claim | **hallucination-candidate (register-confirmed location)** | — | full-frame t9k trailing block `[parse]` (906.5,517.6); `call01` re-read | judges/crop01_judge.md: the point lands in a flat black rectangle — "no photographic detail… not a genuine standalone picture" |

GT-gaps (real-on-image, absent from inventory): none — every judge-confirmed real string maps to a GT unit. (crop05 judge's clipped `Se…` at the right edge = `Self Attention` stack tail, GT6 zone.)

## Hallucination candidates (own section)

1. `October 1` — call02/call14, judge-confirmed absent on image (OCR distortion of "Encode"). Stable across 2 independent calls (byte-identical transcripts). **Confirmed hallucination.**
2. `Encoder` ×3 standalone — full-frame t9k (all three passes); frozen wave-2 register already adjudicated this as hallucinated; re-appeared unchanged in the region source.
3. `F2` — full-frame t9k L1 at (34.7,41.7); no GT match; single-read candidate.
4. Trailing `class_Picture` block at (906.5,517.6) — region claim; judge inspection found a flat black rectangle, no picture content. Register-confirmed location; the crop-parse (call01) re-read also produced only a clipped text fragment (`nalade`), no image payload.
5. `Ende Decoder Attention`, `nalade`, `M-Head`, `Int-head Sell on Block`, `Ya`/`Y1`/`Y2` — NOT-IN-GT as parsed; all garbles explained by judges (misread / clip / callout-tail artifacts) — no phantom slide content except the `[?]` Y-tag subscripts noted above.

## Parser blind spots (findings for the audit)

1. **15-px glyph circles (K, V) are unreadable to doc-parse at compliant crop scales.** Wave-4 read them only from 44–45px-wide crops (violates the ≥480px-wide@2–3× prep rule). This cascade's compliant attempts: 172px context (crop07: label dominates), 162px band (crop09: glyphs misclassified as `Y1/Y2`), 162px K-only band (crop14: callout tail dominates), 162px V-only band (crop15: empty). Vision-gateway judges read K/V without difficulty → the loss is doc-parse's, not the image's.
2. **Q circles invisible to doc-parse below 3D-box stacks** (full-frame: 2/5; 2×-scale crop02: 0/5; 3×-scale crop12: 0/5) while judges count 5/5 with positions.
3. **Line-merging** in wide 2× crops (word boxes 2-per-line in call04) vs clean splits in 3× left-side crops (call05).
4. **Clipped-edge garble**: any string touching a crop edge reads as a fragment (`nalade`, `M-Head`, `Int-head Sell on Block`) — crop prep margin (4%) reduces but does not eliminate this.
5. **Trailing full-span class blocks** (`class_Picture`/`class_Chart` at (0.999,0.999)) carry no usable sub-coordinates → parse-driven recursion terminates immediately; all real recursion here was judge-defect-driven.

## Provenance index

- Full-frame: `03_parses/slide_052/call05_t9k/` (read-only input)
- Crop parses: `parses/call01…call17` (17 dirs; manifest.json `source_call_dir` per crop; call14 = corroboration re-parse of crop02 at `--max-output-tokens 3000`)
- Crops: `crops/cropNN_<class>/crop.png` (16; boxes/scales/transforms in manifest.json — no null boxes)
- Judges: `judges/probe_transcript.txt` + 12 × `judges/cropNN_judge.md` (crop03/04/07/11 carry no novel strings → primary judge = their doc-parse re-parse, per brief)
- Classification basis: wave-2 (`05_comparison/slide_052_comparison.md` + `04_ground_truth/slide_052/inventory.md`, read-only)
