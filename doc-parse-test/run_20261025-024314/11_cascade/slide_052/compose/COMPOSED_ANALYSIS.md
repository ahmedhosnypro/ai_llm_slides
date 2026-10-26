# COMPOSED ANALYSIS — slide 052 (wave-5 v1 crop cascade)

Scope `slide_052_cascade` · frame 960×540 · source `videos/deep-learning/002_transformers_part2/unique_slides/slide_052.jpg`
Region source: full-frame `03_parses/slide_052/call05_t9k/slide_052.parse.md` (md5 `bdb0e649…`, byte-identical to call01_pass1/call02_pass2 — one transcript, read-only input).
Merged evidence: full-frame transcript + 12 crop-parse call dirs (`parses/`, this tree) + 8 judge transcripts (3 inherited: crop01 empty/killed, crop02, crop03 empty/killed; 6 produced this session: crop05/07/08/09/10/11) + 2 probes.
Transform contract (manifest.json, per crop): `frame_x = crop_x/scale + box.x0; frame_y = crop_y/scale + box.y0`.

## Headline

**Union recall 75.0% → 86.4% transcript-level** (19 EXACT + 0 NORMALIZED + 0 PARTIAL + 3 MISSING of 22 GT units; wave-2 basis and matching rule) — **judge-corroborated coverage 22/22 = 100.0%** (the 3 transcript misses, K, V, Y, are REAL on image per this cascade's judges: K and V each confirmed by 2 independent judges with positions matching the certified build; doc-parse cannot read the 15–22 px glyphs at any compliant crop scale, 3× or 6×). 12 crops (cap 16) · 12 parse calls (cap 24) · parallel parse speedup ~2.7×.

Trajectory: wave-2 full-frame 75.0% (16 EXACT + GT5 PARTIAL) → cascade level-1 recovers GT9 (`SOS = Start Of Sentence`, crop05), GT22 (`52`, crop07) and upgrades GT5 to EXACT (crop02: 5 complete instances + 5/5 `Q`) → 86.4% transcript. Levels 2–3 (K/V zone at 3× and 6×, Y row) recovered **zero** new doc-parse strings — the residual 3 misses are the glyph-limitation documented below.

## Composed elements — ordered by frame y

Positions: `[parse]` = coordinate token carried by a transcript (×960/×540); `[box]` = localized by the crop's manifest box; `[judge]` = judge crop-px position mapped through the transform (judge-estimated, ±). Classification: REAL-GT / GT-gap / hallucination-candidate / garble (judge-explained NOT-IN-GT fragment).

| y (frame px) | element | classification | GT id | provenance | evidence |
|---|---|---|---|---|---|
| 41.7 | `F2` | hallucination-candidate | — | full-frame t9k `[parse]` | single-read; no GT match; callout-1 zone; carried from wave-2/3 as candidate |
| 56–84 | `52` (badge numeral) | REAL-GT | GT22 | `call07_crop07_badge` `[box]` + judges/crop07_judge.md `[judge]` | **recovered by cascade** (MISSING in all full-frame passes); judge: reads exactly "52", digits frame ≈(865,60)–(882,76), center ≈(873,68) vs build (875.5,69.5); purple-ringed yellow badge |
| 62–107 | `Multi-head Encoder-Decoder Attention Block` (callout 1) | REAL-GT | GT1 | full-frame t9k `[box]` | EXACT |
| 84 | `Residual Connection and Layer Normalization` (upper bar 1) | REAL-GT | GT3 | full-frame t9k `[box]` | instance 1/3 |
| 116 | `Feed Forward Networks [ One Hidden with RELU Activation]` | REAL-GT | GT4 | full-frame t9k `[box]` | EXACT (whitespace-insensitive; verbatim double space before `RELU` collapsed by parser — known wave-2 defect) |
| 113–124 | `er!` (judge-only observation) | [?] unresolvable clip | — | judges/crop07_judge.md `[judge]` frame ≈(797,113)–(820,124) | dark-red bold letters on a green band, bottom-clipped at crop07's edge; unreadable, no GT unit at that location; flagged, no recall impact |
| 127–178 | `Masked Multi-head Self Attention Block` (callout 2) | REAL-GT | GT2 | full-frame t9k `[box]` + `call04_crop04_left_kv_y` `[box]` (tail inside box y145–295) | EXACT |
| 146–164 | `Residual Connection and Layer Normalization` (upper bar 2) | REAL-GT | GT3 | full-frame t9k `[box]` + `call02` judge (top-clipped bar text frame y155–164) | instance 2/3 |
| 151.7–163.7 | `Res` (fragment) | garble — clip of GT3 instance 2 | — | `call8_crop08_kv_q_zone` `[judge]` | judge: white bold text on the dark-red banner, right-truncated at crop edge, "likely the start of 'Residual'"; not a phantom string |
| 178–243 | `Encode`/`Decoder`/`Attention` ×5 stacks | REAL-GT | GT5 | `call02_crop02_upper_boxes` 5 complete lines + full-frame fragments + `call8` instance 1 + judges/crop02_judge.md, crop08_judge.md `[judge]` | **EXACT (upgraded from wave-2 PARTIAL)**; crop02 parse = 5× "Encode Decoder Attention" lines; judges confirm stack line 1 is "Encode" (no "r") |
| 178–243 | `Encoder` ×3 (standalone) | hallucination-candidate (register-confirmed) | — | full-frame t9k | frozen wave-2 register adjudicated standalone "Encoder" as hallucination (original reads `Encode`); re-appeared unchanged; crop02 judge: 5× "Encode", 0× "Encoder" |
| 180.7–196 | `K` (red circle) | REAL-GT — **doc-parse MISSING at transcript level** | GT18 | judges/crop08_judge.md + crop11_judge.md `[judge]` | **two independent v1 judges**; frame centers ≈(315.7,188.7)/(316.7,188.3) vs build (316.5,187.5); both parses of the zone (3× and 6×) returned no K |
| 194.3–238.7 | `Enc`/`Deco`/`Atten` (right-truncated) | garble — truncation of GT5 instance 1 | — | `call11_crop11_kv_tight` + judges/crop11_judge.md `[judge]` | 6× crop's right edge (frame x370) cuts the label mid-word; judge: "cut-off Encoder/Decoder/Attention"; the completion to "Encoder" is the judge's speculation, contradicted by the certified build and crop02 judge ("Encode") |
| 230.7–246 | `V` (green circle) | REAL-GT — **doc-parse MISSING at transcript level** | GT19 | judges/crop08_judge.md + crop11_judge.md `[judge]` | **two independent v1 judges**; frame centers ≈(315.7,238)/(316.9,238.3) vs build (317.5,238.5) |
| 246–294 | `Q` ×5 (blue circles) | REAL-GT | GT20 | `call02_crop02_upper_boxes` 5 lines + full-frame t9k 2 lines + judges/crop02_judge.md, crop08_judge.md `[judge]` | unit EXACT; **instance coverage 5/5 via crop02** (v1 improvement over full-frame's 2/5); judge positions frame ≈(382–815, 253–256) match build x≈385/489/601/715/813 |
| 247–282 | `Ya`/`Y2` → judges read **Y₀, Y₁, Y₂** ×3 (red tags) | REAL-GT (tags) with `[?]` wording conflict — **doc-parse MISSING at unit level** | GT21 | `call9_crop09_y_tags_row` + judges/crop09_judge.md `[judge]` | parse garbled the row ("Ya"/"Y2"); judge: three red Y tags at frame x≈102–114/173–186/246–258, y≈267–282 (build: x≈85/163/239, fy≈247–263), reading **Y₀/Y₁/Y₂ with bottom-clipped subscripts**; conflicts with the certified build's plain `Y` — same subscript observation as the v2 cascade's judges, now a 2nd independent read; flagged for pixel adjudication, kept out of recall arithmetic |
| 299–419 | `Transformer Encoder` | REAL-GT | GT8 | full-frame t9k `[box]` + `call05_crop05_encoder_inputs` + judges/crop05_judge.md `[judge]` (text frame ≈(84–277, 356–375)) | EXACT |
| ~312 | `Residual Connection and Layer Normalization` (lower bar) | REAL-GT | GT3 | full-frame t9k `[box]` | instance 3/3 |
| 332–428 | `Masked`/`Multi-Head`/`Self Attention` ×5 stacks | REAL-GT | GT6 | full-frame t9k ×4 + `call03_crop03_lower_boxes` ×4 + `call10_crop10_box5_right` (5th box) + judges/crop10_judge.md `[judge]` | EXACT; **5/5 instances** (full-frame had 4 + one `Self Attention` fragment); crop10 judge verifies the 5th stack verbatim, incl. yellow `Masked` |
| 352–385 | `Ml-Head`, left-stack clips `sked`/`ttention` | garble — edge clips of GT6 instance 4 | — | `call10_crop10_box5_right` + judges/crop10_judge.md `[judge]` | judge: "Ml-Head" is a misread of the edge-clipped left "Multi-Head" (OCR hallucinated the leading "M"); "sked"/"ttention" are the same stack's clipped tails |
| 373.3–385.3 | `S` (right-edge clip, judge-only) | garble — GT6 zone fragment | — | judges/crop05_judge.md `[judge]` frame ≈(331.7–340.7, 373.3–385.3) | clipped start of a masked-stack label entering crop05's right edge; maps to GT6 zone, no new unit |
| 443.7–472.7 | `I` / `feel` / `Sick` (3 input boxes) | REAL-GT | GT10/11/12 | full-frame t9k merged line + `call05_crop05_encoder_inputs` merged line + judges/crop05_judge.md `[judge]` | judges: 3 separate boxes, tokens I / feel / Sick at frame x≈74–136/150–213/225.7–288.7, y≈444–473; line-merge = structure-only defect |
| 444–470 | `SOS` `Je` `me` `sens` `malade` (word boxes) | REAL-GT | GT13–17 | full-frame t9k + `call06_crop06_word_boxes` `[box]` | all 5 EXACT |
| 454 | `Word and Position Encoding` | REAL-GT | GT7 | full-frame t9k + `call06_crop06_word_boxes` `[box]` | EXACT |
| 492–504.3 | `SOS = Start Of Sentence` | REAL-GT | GT9 | `call05_crop05_encoder_inputs` `[box]` + judges/crop05_judge.md `[judge]` | **recovered by cascade** (MISSING in all full-frame passes); judge: verbatim, S/O/S initials underlined, wide "=" spacing, frame ≈(82–226, 492–504) |
| 517.6 | trailing `class_Picture` region claim | hallucination-candidate (register-confirmed) | — | full-frame t9k `[parse]` (906.5,517.6) + `call01_crop01_picture` re-read (full-span block, zero text) | wave-2-confirmed hallucination region; its dedicated crop parse added zero content |

GT-gaps (real-on-image, absent from the inventory): **none found.** Every judge-confirmed real string maps to a GT unit. One wording conflict is flagged instead: the Y-row subscripts (Y₀/Y₁/Y₂ per judges vs plain `Y` in the certified build) — kept `[?]` for pixel adjudication, consistent with the v2 cascade's treatment.

## Hallucination candidates (own section)

1. `F2` — full-frame t9k at (34.7,41.7); no GT match; single-read candidate (also carried by v2).
2. `Encoder` ×3 standalone — full-frame t9k (all three passes byte-identical); wave-2 register-confirmed hallucination; crop02 judge re-confirms the stacks read "Encode".
3. Trailing `class_Picture` block at (906.5,517.6) — region claim; register-confirmed; its cascade crop (crop01) re-read returned only a full-span block with zero text — no picture payload.
4. `Ml-Head` — crop10 parse; judge-confirmed misread of edge-clipped left "Multi-Head" (OCR hallucinated the leading "M"). Not phantom slide content.
5. `Ya` — crop09 parse; judge-confirmed misread of Y₀ (bottom-clipped subscript resembling "a"). `Y2` is the visible Y₂ (the `[?]` subscript question above, not a hallucination).
6. `Res`, `Enc`, `Deco`, `Atten`, `sked`, `ttention`, `S` — NOT-IN-GT as parsed; all edge-clip/truncation fragments of GT strings, judge-explained; no phantom content.
7. `er!` — crop07 judge-only observation at ≈(797,113)–(820,124): bottom-clipped, unreadable, no GT unit at that location; `[?]` unresolvable from this crop; no recall impact.

## Parser blind spots (findings for the audit)

1. **15–22 px glyph circles (K, V) are unreadable to doc-parse at ANY compliant crop scale.** This cascade tried the K/V zone twice: 3× (crop08, 516×369) read only `Res` + the blue-box label; 6× (crop11, 540×732, a documented scale deviation for exactly this reason) read only the truncated box label — zero K/V. Vision-gateway judges read K and V cleanly in both crops (positions match the certified build to ~1–2 px). The loss is the parser's, not the image's; the judge leg is the compliant recovery route.
2. **Q circles under the 3D boxes: full-frame 2/5 → 2.8× wide crop 5/5.** crop02's chart-style read captured all five `Q` instances the full-frame parse dropped.
3. **Y-tag row (16 px glyphs): doc-parse garbles subscripts** (`Ya`/`Y2` at 3×, zero text at 6×); judges resolve the row (3 tags, subscripts `[?]`).
4. **Edge clipping drives most NOT-IN-GT garble** (`Res`, `Enc`/`Deco`/`Atten`, `sked`/`ttention`, `Ml-Head`, `er!`): the 4% crop margin reduces but does not eliminate it, and judge-only crops (badge corner) can introduce new clips.
5. **Trailing full-span class blocks** (`class_Picture`/`class_Chart` spanning (0,0)–(0.999,0.999)) carry no sub-coordinates → parse-driven recursion terminates immediately on those branches; all real recursion here was judge-defect-driven.

## Provenance index

- Full-frame: `03_parses/slide_052/call05_t9k/` (read-only input; md5 `bdb0e649…`)
- Crop parses: `parses/call01…call12` (12 dirs; box/scale/transform per crop in `manifest.json`)
- Crops: `crops/crop01_picture … crop12_y_tight/crop.png` (12)
- Judges: `judges/probe_call.log` + `probe2_call.log` (gateway probes, EXIT 0) + nonempty transcripts `crop02_judge.md` (inherited), `crop05/07/08/09/10/11_judge.md` (this session); `crop01_judge.md` and `crop03_judge.md` are empty (previous worker's runs killed mid-flight — neither crop carried novel strings, so no rerun was required; files preserved)
- Classification basis: wave-2/3 frozen artifacts (`04_ground_truth/slide_052/inventory.md`, `05_comparison/slide_052_t9k_delta.md`, `08_final/scores_slide_052.csv`) — read-only
