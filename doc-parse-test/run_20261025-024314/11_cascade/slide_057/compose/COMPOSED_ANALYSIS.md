# COMPOSED ANALYSIS — slide_057 (wave-5 cascade composition)

Scope `slide_057_cascade` · worker `worker-slide_057_cascade` (resume completion) · 2026-10-25.
Source frame 960×540 (`videos/deep-learning/002_transformers_part2/unique_slides/slide_057.jpg`).
This file merges ALL banked transcripts for the slide: full-frame `03_parses/slide_057/call01_pass1`
+ the 17 cascade crop parse call dirs under `11_cascade/slide_057/parses/`, deduplicated, every
line carrying frame position (manifest transform: `frame_x = crop_x/scale + box.x0`,
`frame_y = crop_y/scale + box.y0`), classification, and provenance.

## Headline

**Union transcript recall 12.5% (frozen wave-2, 6/48) → 49.0% (23.5/48)** — 19 EXACT + 9 NORM.
The full-frame parse loops (`Decoder` ×482, finish=length); crop parses broke the loop and
yielded +18.0 weighted GT over the banked pass1 inventory. Score = transcript-level (what
doc-parse emitted); judge-confirmed ink that no parse emitted (Word N-1, Softmax, token row, Q)
is annotated but NOT scored.

## Merge sources (18 transcripts)

| source | role | strings |
|---|---|---|
| `03_parses/slide_057/call01_pass1` | full-frame (loop-degenerate: 6 unique strings, `Decoder` ×482, finish=length) | 6 |
| `call01..call14, call010, call011` | L1/L2 crop parses (14 crops) | per-crop below |
| `call17, call18` | L3 crop parses (crop15 shell, crop16 garble) | 0 + 3 |
| `call19_corrob_crop05_3000` | corroboration re-parse of crop05 (byte-equivalent strings) | dup |

Judges banked: `judges/crop01/02/05/06_judge.log` (FINAL VERDICT, rc=0). crop08/crop09: both
judge attempts rc=124 (gateway leg exceeded the 340s/420s walls; evidence in
`judges/crop08_judge_call.log` / `judges/crop09_judge_call.log`) — recorded under blockers;
crop08's Y-row garbles are nonetheless adjudicated by the crop01 judge, whose crop contains the
same chip row (true forms Y₀ Y₁ Y₂ Y₃ Y₄ Y₅ Y₍N-2₎ Y₍N-1₎).

## Merged element list (top-to-bottom by frame y)

Legend: class = REAL-GT-EXACT (1.0) · REAL-GT-NORM (0.5) · MISS (garble of real ink, 0.0) ·
NOT-IN-GT (hallucination candidate) · judge = vision-gateway crop judge evidence. Positions are
frame px (960×540); `[region]` = crop box only (no per-string coords in that transcript);
`[GT-geom]` = certified-builder geometry (inventory).

| y (px) | string (verbatim transcript) | frame position | class | GT target | provenance |
|---|---|---|---|---|---|
| 53–89 | `57` | badge (875–911, 53–89) [GT-geom]; parse reported (56,43) — mislocalized `[?]`; judge crop05 saw partial "5" at (856–871, 54–81) | REAL-GT-EXACT | `57` | call01_pass1 |
| 70–76 | `SOHmax` | (679–702, 70–76) judge crop05 read the bar ink as **"Softmax"** | MISS (ligature garble) | `Softmax` (0.0) | call12; judge crop05 |
| 87–433 | `K` | region (443–622, 87–433); K/V badge flank of the central striped column [GT-geom]; no judge transcript (rc=124 ×2) | REAL-GT-EXACT | `K` | call09 |
| 87–433 | `Read Forw`, `Read Forward` ×2 | region (443–622, 87–433) | NOT-IN-GT candidate (see §hallucinations) | — | call09 |
| 87–433 | `Decoder Attention`, `Encode Decoder Attention` | region (443–622, 87–433); central-column reads of the same 3-line boxes | REAL-GT-NORM | `Encoder Decoder Attention` (0.5) | call09 |
| 111–126 | `Yo Y1 Y2 Y3 Y5 ..... Y6 Yx1 Yx1` | chip row (99–437, 111–126); judge crop01 transcribed the same row as **Y₀ Y₁ Y₂ Y₃ Y₄ Y₅ Y₍N-2₎ Y₍N-1₎** | REAL-GT-NORM for Y_0/Y_1/Y_2/Y_3/Y_5 (5×0.5); Y_4/Y_{N-2}/Y_{N-1} MISS | `Y_0..Y_5, Y_{N-2}, Y_{N-1}` | call08; judge crop01 |
| 143–172 | `Residual Connection and Layer Normalization` | bars (587–794, 143–151) & (587–794, 164–172) judge crop05 | REAL-GT-EXACT | same | call01_pass1; call05, call06, call19 |
| 154–162 | `Feed Forward Networks [ One Hidden with RELU Activation` | bar (569–794, 154–162) judge crop05: separator is **"/"** not "[", leading F clipped → true ink **"Feed Forward Networks / One Hidden with RELU Activation"** = GT verbatim | REAL-GT-NORM (0.5; pass1's "RELL" variant same GT target) | `Feed Forward Networks - One Hidden with RELU Activation` | call01_pass1; call05, call19; judge crop05 |
| 157–171 | `Encoder Block M` | (226–313, 157–171) judge crop01 VERIFIED "correct as written" | REAL-GT-EXACT | `Encoder Block M` | call01; judge crop01 |
| 175–199 | `Encode Decoder Attention` ×3 | upper blue boxes (586–621)(629–664)(672–707)(719–756)(766–801), y 175–199; judge crop05: 3-line ink **Encode/Decoder/Attention**, 10 boxes in crop | REAL-GT-NORM (0.5) | `Encoder Decoder Attention` | call05 ×6, call19; judge crop05 |
| 232–360 | `Encoder` / `Decoder` (vertical labels + legend) | vertical Encoder (73, 256–360), vertical Decoder (821–846, 244–336) judge crop05; legend lines y 426–480 [GT-geom] | REAL-GT-EXACT ×2 | `Encoder`, `Decoder` | call01_pass1; call03, call04, call07, call09 |
| 244–401 | `Encoder Block 2 / 1 / 0` | crop03 region (44–464, 244–401); judge crop01 confirmed the bar-label pattern | REAL-GT-EXACT ×3 | `Encoder Block 2/1/0` | call01_pass1 (2); call03 (1, 0) |
| 244–401 | `X1 X2 X3 X4 X5`, `↑` | crop03 table scaffold headers | NOT-IN-GT candidate (scaffold artifact) | — | call03 |
| 300–324 | `Encode Decoder Attention` ×3 (lower row) | lower blue boxes, y 300–324 | REAL-GT-NORM (same GT target, counted once) | `Encoder Decoder Attention` | call05, call19 |
| 397–483 | `T`, `0`, `Attention`, `rmalization`, `Mult-Head Self Attention` | crop14 region (734–906, 397–483); edge partials + dups (`Attention`→crop07 read; `Mult-Head`→crop06 read; `rmalization`→truncated `…rmalization`) | dups: REAL-GT; partials: MISS | — | call14 |
| 401–509 | `Encoder`, `Decoder`, `Attention` (legend 3 lines) | legend block (419–591, 401–509); GT-geom y 426–480 | REAL-GT-EXACT ×3 | `Encoder`, `Decoder`, `Attention` | call07; call04 |
| 423–433 | `Word Embedding` | (234–306, 423–433) judge crop02 VERIFIED | REAL-GT-EXACT | `Word Embedding` | call02; judge crop02 |
| 429 | (big `Q` — no transcript string) | center (833, 429) r≈13; judge crop06: "large red serif letter Q in cream circle" | MISS (transcript never emitted; ink judge-confirmed) | `Q` (0.0) | judge crop06 |
| 432–442 | `Residual Connection and Layer Normalization` (decoder lower) | (594–797, 432–442) judge crop06 | REAL-GT-EXACT | same | call06 |
| 445–455 | `Positional Encoding / Embedding` | (197–339, 445–455) judge crop02 VERIFIED (wide gap "Positional   Encoding" matches build double-space) | REAL-GT-EXACT | `Positional  Encoding / Embedding` | call02; judge crop02 |
| 445–463 | `Multi-Head Self Attention` ×2 | 5 lavender boxes (584–619)(631–666)(676–712)(722–757)(767–802), y 445–463; judge crop06 VERIFIED ink 2-line, no hyphen | REAL-GT-NORM (0.5) | `Multi-Head Self-Attention` | call06, call14; judge crop06 |
| 446–499 | `Wind 4`, `Wind 5`, `Wind M2` | crop16 region (221–459, 446–499) | NOT-IN-GT candidate (X-row garble family, cf. v2 "Wind N") | — | call18 |
| 448–497 | `Wired 0..5`, `Wired M2` | crop10 region (86–459, 448–497) | NOT-IN-GT candidate (X-row garble family) | — | call010 |
| 476–495 | `Word 0`–`Word 5` | boxes (100–129)(135–165)(172–201)(207–237)(242–272)(278–308), y 476–495; judge crop02 VERIFIED each | REAL-GT-EXACT ×6 | `Word 0..Word 5` | call02; judge crop02 |
| 476–495 | `Word N2` | (368–401, 476–495); judge crop02: ink reads **"Word N-2"** (hyphen dropped by parse) | REAL-GT-NORM (0.5) | `Word N-2` | call02; judge crop02 |
| 476–495 | (`Word N-1` — no transcript string) | (405–440, 476–495); judge crop02: "clearly legible" at right edge | MISS (judge-confirmed ink, parse never emitted) | `Word N-1` (0.0) | judge crop02 |
| 486–496 | `Word and Position Encoding` | purple bar (594–797, 486–496) judge crop06 VERIFIED — settles inventory divergence: ink says **Encoding** (build spelling), not "Embedding" | REAL-GT-EXACT | `Word and Position Encoding` | call06, call13; judge crop06 |
| 489–521 | (bottom token row — no transcript strings) | 5 boxes (596–608)(642–653)(687–699)(732–745)(773–799), y 498–507; judge crop06 read ≈"SOS je ne sais résultat" (last tokens low-confidence at 3×) | MISS (ink judge-confirmed; GT = `SOS Je ne suis faisait`) | 5 token strings (0.0) | judge crop06; call13 |

Shell transcripts (no strings): `call011` (crop11 wordrow-tight), `call17` (crop15 ynum-right) —
recorded, nothing to merge.

## NOT-IN-GT hallucination candidates (transcript strings with no GT counterpart)

| string | count | provenance | assessment |
|---|---|---|---|
| `Wired 0/1/2/3/4/5/M2` | 7 | call010 (crop10 X-chips tight) | word-shape garble of the X-chip serif-italic row (`X_N` misread as "Wired N"); same family as v2's "Wind N" — parser prior, not real ink |
| `Wind 4`, `Wind 5`, `Wind M2` | 3 | call18 (crop16) | same family, tighter geometry |
| `Read Forw`, `Read Forward` ×2 | 3 | call09 (crop09 KV column) | region contains striped column + K/V/Q badges only (GT build census); no judge transcript — both judge attempts rc=124 (see blockers in CASCADE_REPORT.md) — treat as unverified ink reading |
| `X1..X5`, `↑` | 6 | call03 (crop03) | table-scaffold headers over arrow glyphs, not slide ink |
| `0 0 0 0` | 2 dirs | call02, call010 | table-cell filler over the ellipsis dot row |
| `T`, `0`, `rmalization` | 3 | call14 (crop14 big-Q) | edge-truncated partials of neighboring GT ink (`Q` badge, `…Normalization`) |
| `Y6`, `Yx1` ×2 | 3 | call08 (crop08) | chip garbles; judge crop01's read of the same row confirms true forms Y₅/Y₍N-2₎/Y₍N-1₎ |
| `SOHmax` | 1 | call12 (crop12) | ligature garble of `Softmax`; judge crop05 read the ink as "Softmax" |

None of these enter GT (0.0); they are parse artifacts over real graphics/ink, banked for the
hallucination audit.

## GT-gaps (real-on-image strings absent from the GT inventory)

**None found.** All judge-confirmed ink maps to an existing GT string or to the inventory's
documented build-vs-analysis divergences (`Tokens` brace label, purple-bar end labels — both
omitted by law per GROUND RULES(c)). The full-frame mislocalization of `57` (parse reported
(56,43) vs badge at (875,53)) is a position error, not a string gap.

## Composition notes

- Dedup rule: a GT target counts once at its best transcript score (EXACT 1.0 / NORM 0.5 /
  PARTIAL 0.5); repeated reads across call dirs are listed as provenance, not extra score.
- The pass1 loop artifact (`Decoder` ×482, finish=length, no coordinates) is collapsed to its
  6 unique strings; loop evidence stays in `03_parses/slide_057/call01_pass1/`.
- Judge legs are evidence annotations; transcript recall is unchanged by them (Word N-1,
  Softmax, token row, Q remain 0.0 — no parse emitted them).
- Position provenance: judge-reported crop-px converted via the per-node transform
  (`frame = crop_px/3 + box.x0|y0`); `[GT-geom]` anchors from `04_ground_truth/slide_057/inventory.md`.
