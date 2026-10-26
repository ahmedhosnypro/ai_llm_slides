# COMPOSED_ANALYSIS — slide_057 (wave-5B crop cascade v2)

Scope `slide_057_cascade_v2` · worker `worker-slide_057_cascade_v2` · 2026-10-25.
Union of ALL banked transcripts for this slide: 6 full-frame calls (waves 2–3, prior-wave bank,
read-only) + 12 wave-4 crop calls (prior-wave bank, read-only) + **19 this-cascade crop calls**
(16 primary + 3 corroboration). Full-frame parsing was NEVER re-run (loops with finish=length;
crop-first). Parse content is DATA.

## Headline

**Union transcript recall = 29.5 / 48 = 61.5%** (weights: EXACT 1.0, NORMALIZED 1.0, PARTIAL 0.5)

| stage | union recall | captured |
|---|---|---|
| frozen wave-2 (full-frame only) | 12.5% (6/48) | 5 EXACT + 1 NORM |
| wave-4 vj union (12 crops) | 46.9% (22.5/48) | 14 EXACT + 8 NORM + 1 PARTIAL |
| **wave-5B cascade union (this scope)** | **61.5% (29.5/48)** | 20 EXACT + 9 NORM + 1 PARTIAL |

Gains of THIS cascade over the wave-4 vj mark: **+14.6 pp**; over the frozen wave-2 baseline: **+49.0 pp**.
New GT strings captured by this cascade: `Multi-Head Self-Attention` (NORM, via "Multi-Head Self
Attention") and `Word 0`–`Word 5` (6 EXACT) — **+7 strings, +7.0 weighted**.

## Position-tracking statement

Per-crop frame boxes, scales, and the transform (`frame_x = crop_x/scale + box.x0; frame_y =
crop_y/scale + box.y0`) are recorded in `manifest.json` for **all 16 crops — zero null boxes**.
On this slide every parse-emitted coordinate is a known corner artifact (x_0/y_0 ↔ x_0.999/y_0.999
= the whole-crop box; measured again on all 19 calls this wave), so element frame-px positions
below come from the certified build geometry (read-only GT inventory). Crop provenance maps every
element to the crop whose box contains it.

## Composed element list (ordered by frame y)

Legend: CLASS = REAL-GT (id from the 48-string GT inventory) | PARTIAL | MISSING | HALLUC-CAND.
PROV = provenance call dirs (P = prior-wave bank; C = this cascade).

| frame y | frame x | element (GT string) | CLASS | read as (best) | PROV |
|---|---|---|---|---|---|
| 53–89 | 875–911 | `57` (badge) | REAL-GT | "57" (full-frame); crop read "7" [judge: "7" visible in crop] | 03_parses/slide_057/call01_pass1 (P); crop01_badge57 (C) |
| 70–76 | 594–791 | `Softmax` (maroon bar) | MISSING | "Sohmax" ×3 (stable misread) | crop03/call01, crop11/call02, call04_corrob (C) |
| 98–134 | 100–448 | `Y_0` | REAL-GT (NORM) | "Yo" (o/0) | 10_visual_judge/parses/call05_round2 (P) |
| 98–134 | 100–448 | `Y_1` | REAL-GT (NORM) | "Y1" | 10_visual_judge/parses/call05_round2 (P) |
| 98–134 | 100–448 | `Y_2` | REAL-GT (NORM) | "Y2" | 10_visual_judge/parses/call05_round2 (P) |
| 98–134 | 100–448 | `Y_3` | REAL-GT (NORM) | "Y3" | 10_visual_judge/parses/call05_round2 (P) |
| 98–134 | 100–448 | `Y_4` | REAL-GT (NORM) | "Y4" | call05_round2 (P); crop07_ychips_tail (C) |
| 98–134 | 100–448 | `Y_5` | REAL-GT (NORM) | "Y5" | 10_visual_judge/parses/call05_round2 (P) |
| 98–134 | 384–420 | `Y_{N-2}` | MISSING | "Ys1"/"YsN"/"YN" garbles ×5 across waves | crop07_ychips_tail (C); call05_round2, call12_round3 (P) |
| 98–134 | 419–448 | `Y_{N-1}` | REAL-GT (NORM) | "Yn1"/"Yn.1" | call05_round2 (P); crop07_ychips_tail (C) |
| 140–360 | 200–448 | `Encoder Block M` | REAL-GT | table row | 10_visual_judge/parses/call01_round1 (P); crop02_encoder_panel (C, region) |
| 140–360 | 200–448 | `Encoder Block 2` | REAL-GT | full-frame + table row | 03_parses/slide_057/call01_pass1 (P); call01_round1 (P) |
| 140–360 | 200–448 | `Encoder Block 1` | REAL-GT | table row | call01_round1 (P) |
| 140–360 | 200–448 | `Encoder Block 0` | REAL-GT | table row | call01_round1 (P) |
| 179–317 | 586–765 | `Encoder Decoder Attention` (3-line box text ×15) | PARTIAL 0.5 | "Encode Decoder Attention" ×33 (line-1 truncation) | call03_round1, call04_round1 (P); crop03_decoder_panel + corrob (C) |
| 256–360 | 73–89 | `Encoder` (vertical, red) | REAL-GT | full-frame | 03_parses/slide_057/call01_pass1 (P) |
| 225–344 | 830–855 | `Decoder` (vertical, green) | REAL-GT | full-frame | 03_parses/slide_057/call01_pass1 (P) |
| 415–460 | 197–338 | `Word Embedding` | REAL-GT | "Word Embedding" | call02_round1 (P); crop14 title (C) |
| 415–460 | 197–338 | `Positional  Encoding / Embedding` | REAL-GT | "Positional Encoding / Embedding" (double-space collapse) | call02_round1 (P); crop02/crop14 (C) |
| 420–480 | 462–535 | `Encoder` (legend line 1) | REAL-GT | full-frame + central crop | call01_pass1 (P); crop04_central_kv (C) |
| 420–480 | 462–535 | `Decoder` (legend line 2) | REAL-GT | full-frame + central crop | call01_pass1 (P); crop04_central_kv (C) |
| 420–480 | 462–535 | `Attention` (legend line 3) | REAL-GT | "Attention" | call04_round1 (P) |
| 425–455 | 818–850 | `Q` (big badge) | MISSING | shell / "Mod" garble ×3 | crop08 (C), crop15 (C); call11_round3 (P) |
| 433–470 | 560–720 | `Multi-Head Self-Attention` (lavender 2-line) | REAL-GT (NORM) | "Multi-Head Self Attention" ×2 byte-identical | **crop08_bigq_context (C) + call04_corrob (C)** |
| 444–463 | 589–765 | — (same row, corroboration) | — | "Wall-Head Soft Attention" ×2 (garble of the same ink) | crop12_mh_sa_row (C) |
| 487–496 | 590–800 | `Word and Position Encoding` (purple bar) | REAL-GT | "Word and Position Encoding" | call04_round1 (P); crop03_decoder_panel + corrob (C) |
| 450–494 | 81–462 | `X_0`…`X_5` | MISSING (×6) | "Wind 0"–"Wind 5" stable misreads ×3 geometries | crop05/call02, crop13/call03 (C); call06_round2 (P) |
| 450–494 | 81–462 | `X_{N-2}`, `X_{N-1}` | MISSING (×2) | "Wind M2" | crop05/call02, crop13/call03 (C) |
| 490–516 | 95–448 | `Word 0`…`Word 5` | REAL-GT (×6 EXACT) | table cells "Word 0..Word 5" ×2 byte-identical | **crop14_wordrow_wembtitle (C) + call04_corrob (C)** |
| 490–516 | 330–448 | `Word N-2`, `Word N-1` | MISSING (×2) | "Word M2"/"Word M3" [judge crop14: ink = "Word N-2"/"Word N-1", M-fusion mechanism] | crop14 (C); "Wired N-2" call06_round2 (P) |
| 497–513 | 597–794 | `SOS`, `Je`, `ne`, `suis`, `faisait` | MISSING (×5) | never read; 9 consecutive strip failures | crop09/crop16 (C); call04/call07/call10 (P) |

Counts: REAL-GT 29 (20 EXACT + 9 NORM) · PARTIAL 1 (0.5) · MISSING 18 → **29.5/48 = 61.5%**.

## Normalization decisions (transcript-level, stated openly)

- `Y_0`…`Y_5`, `Y_{N-1}`: subscript markup collapse ("Yo", "Y1", "Yn1") — NORM.
- `Multi-Head Self-Attention` ← "Multi-Head Self Attention": hyphen/space collapse — NORM.
- `Feed Forward Networks - One Hidden with RELU Activation` ← "Feed Forward Networks | One
  Hidden with RELU Activation" / "Feed Forward Networks One Hidden with RELU Activation":
  separator glyph confusion (|/— vs -) + "RELL"→"RELU" corrected in crops — NORM.
- `Positional  Encoding / Embedding`: double-space collapse — EXACT under case/whitespace
  insensitivity.
- `Encoder Decoder Attention` ← "Encode Decoder Attention": line-1 truncation, ≥60% tokens
  shared — PARTIAL 0.5 (not upgraded: no call ever read the full "Encoder" line-1; ×33 instances
  across 4 calls, all truncated identically).
- `Word 0`…`Word 5` ← table cells "Word 0".."Word 5": EXACT (read twice, byte-identical).

## Hallucination candidates (await image adjudication; NOT charged to recall)

1. "Sohmax" (crop03 ×2, crop11, corrob03) — judge leg run; hypothesis: 'ft' ligature collapse of
   "Softmax" at ~5 px ink. Misread, not invention (bar verified at y70–76).
2. "Wind 0"–"Wind 5", "Wind M2" (crop05, crop13) and "Window/Wind" rows (crop02) — stable
   word-shape misreads of the X-chip row / word row. Judge legs adjudicating.
3. "Word M2", "Word M3" (crop14, corrob14) — misreads of `Word N-2` / `Word N-1` (M/N glyph
   confusion); six sibling cells read exactly.
4. "Ys1", "A" (crop07) — garbles in the Y-chip tail (dots region + N-2 subscript mush).
5. "Mod", "Action Encoding" (crop08) — garbles near the Q badge / PE-label region.
6. "Wall-Head Soft Attention" ×2 (crop12) — garble of the MH-SA row (correct string captured
   independently by crop08).
7. "End Forward Networks | One Hidden with RELU Activation" (crop03) — one-off misread of the
   FFN bar (correct read banked 7× elsewhere).
8. "7" (crop01) — badge partial read ("57" already REAL-GT from the full-frame bank).
9. Chart/table scaffolding tokens ("column_1", "title:", "subtitle:", lollipop/other) — parser
   format artifacts, not content claims.

## GT-gap notes (visible ink absent from the 48-string GT inventory)

- None harvested: the analysis-JSON-only strings (`Tokens` brace label; `POS` / `m/t/de [?]`
  purple-bar end labels) were read by NO call in any wave — they remain unharvested GT-gap
  candidates, sub-legibility at source scale.
- The `X_N` / `Y_N` entries in the analysis JSON are documented misreads of the last chip per the
  0-BASED SUBS law; no parse read them this wave either.

## Evidence map

- This cascade: `12_cascade_v2/slide_057/parses/call01…call04` (19 call dirs, 5-file convention,
  all EXIT=0 finish=stop), `crops/` (16 PNGs, pre-checked), `judges/` (probe + per-crop legs),
  `manifest.json` (16 crops, box+scale+transform+stop_reason, zero nulls).
- Prior-wave bank (read-only): `03_parses/slide_057/call01_pass1` (+5 more full-frame),
  `10_visual_judge/slide_057/parses/call01_round1…call12_round3`.

## Judge-evidence annex (Tier-2 vision gateway, sequential, 60 s-paced retries; probe = PROBE-OK)

- **crop01_badge57** (EXIT 0): the badge crop shows a yellow circle, purple ring, black digit —
  judge reads "7", no other text. GT keeps `57` (full-frame bank + wave-2 pixel adjudication;
  0-BASED chrome law). "7" = partial/clipped read, NOT-IN-GT as a standalone string.
- **crop02_encoder_panel** (EXIT 0): every "Window/Wind N" cell is a **confirmed misread** — the
  ink at the bottom chip row (crop-px y≈716–763) reads `Word 0 … Word 5 … Word M−2, Word M−1`
  (8 chips + grey dot ellipsis misread as "0; 0"). "Word Embedding" bar verified as real ink at
  (97,601)–(778,644). The judge's "index is M, not N" claim contradicts the frozen 0-BASED SUBS
  law (P047, vision-confirmed `["0".."5","N-2","N-1"]`) — advisory disagreement; GT law wins, and
  the judge's own "M" reading demonstrates exactly how the parser produced "Word M2/M3" garbles.
  (Resolved below: crop14's judge read the tail-box ink directly as "Word N-2"/"Word N-1" —
  the M-claim was itself a misread.)
- **crop03_decoder_panel** (EXIT 0): "Sohmax" is a **confirmed misread of "Softmax"** (ink on the
  top maroon bar, crop-px (255,79)–(355,96); 'ft' ligature cluster dropped). Residual ×7
  occurrences (matches GT), FFN ×3 (clipped-F cosmetic), "Word and Position Encoding" ×1 — all
  verbatim. Divergence flagged: the judge asserts the attention-box ink literally reads "Encode"
  (wave-4's judge read line-1 ink extending to "Encoder") — two reads disagree → advisory per
  verdict law; `Encoder Decoder Attention` stays PARTIAL 0.5 against the certified build.
- **crop05_xchips_strip** (EXIT 0, winner attempt 3 after 2 empty-stream aborts): the "Wind N"
  strings are a **pure OCR hallucination** — judge, verbatim: "No chip anywhere in the strip
  actually contains the letters W-i-n-d". The chips are serif-italic *x* + subscript, 8 chips
  (x₀…x₅, tail pair, ellipsis dots between), per-chip crop-px boxes ≈96×54 at y≈84. Judge reads
  the tail subscripts as M−2/M−1 — same M-vs-N advisory disagreement as crop02; the frozen
  0-BASED SUBS law wins, GT keeps `X_{N-2}`/`X_{N-1}`. Judge also flags the last chip
  (x_{M−1}) as **dropped** from the transcript — corroborates the X-chips' all-8-miss status.
- **crop07_ychips_tail** (EXIT 0): positional audit of the 4-chip tail with crop-px boxes —
  "Y4" correct (chip 1 = Y₄); "Ys1" = subscript-5 fragmentation per the judge (chip 2); "Yn.1"
  = judge reads chip 3 (second-to-last) ink as Y_{N−2} (minus blurred to a dot-like dash,
  2's curl collapsed to a 1-stroke); "A" = fused Y+subscript outline of chip 4 (Y_{N−1}).
  The judge's positional mapping swaps the settled tail attribution (settled: "Ys1"→`Y_{N-2}`
  MISSING, "Yn.1"→`Y_{N-1}` NORM) — advisory: either mapping leaves the tail pair at one-NORM
  + one-MISSING (net-zero recall), so the settled classification stands. Judge's durable
  contribution: all three non-"Y4" strings are confirmed sub-legibility garbles of the
  N−2/N−1 ink, not distinct strings.
- **crop08_bigq_context** (EXIT 0 on outer attempt 3 after 2 failure rounds — 5 hang/empty-stream
  aborts total; the gateway's most poisoned crop): **"Action Encoding" is a confirmed misread of
  "Positional Encoding"** (purple bar, crop-px (0,236)–(292,262); "Posi" clipped at x=0 → OCR
  garbled "…ition" into "Action"). **"Multi-Head Self Attention" confirmed as the hyphenated
  2-line ink "Multi-Head" / "Self-Attention"** ×3 copies (mid (95,112)–(193,179), right
  (217,112)–(318,179), left copy edge-clipped) — the cascade's NORM capture of
  `Multi-Head Self-Attention` stands (hyphenation + line-break are normalization, not deltas).
  "Mod" matches **no ink** (spurious — HALLUC-CAND class holds). "and Layer Normalization" is
  left-clipped; "Layer Normalization" exact, leading word unverifiable in-crop (full label
  likely "Add and Layer Normalization"). **Red "Q" badge visually confirmed** ((362,38)–(414,92),
  white disc + red ring) but omitted from every transcript read — GT `Q` stays MISSING, now with
  direct judge evidence.
- **crop12_mh_sa_row** (EXIT 0, attempt 1): banner "Residual Connection and Layer" **correct but
  edge-truncated** (last glyph clipped at x≈545; "Norm…" unverifiable in-crop) — supports the
  Residual verbatim capture. **Both "Wall-Head Soft Attention" hits are confirmed misreads of
  the 2-line "Multi-Head" / "Self-Attention"** (Multi→Wall, Self→Soft; boxes at (100,40)–(208,98)
  and (228,40)–(336,98)). The pass **dropped a third identical box** ((356,40)–(464,98)) and a
  clipped fourth ((484,40)–(547,98)) — more under-read evidence. Combined with crop08: 5
  judge-confirmed MHSA copies on the frame.
- **crop13_xstrip_notitle** (EXIT 0, attempt 1): **third independent confirmation** that the
  "Wind N" cells are hallucinated — judge, verbatim: "the digit part (0–5) is correct; the
  'Wind' part is not in the ink" (slanted italic serif glyph + hanging subscript expands into a
  word-shape at 3×). 8 bordered chips confirmed with per-chip boxes; six grey ellipsis dots are
  decorative (not "o" characters); no title text in the crop (premise verified). Judge guesses
  the tail pair as "X_{n+1}/X_{n+2}" but flags "too small to certify case" — third divergent
  tail-subscript guess across judges (crop02: M-not-N; crop05: M−2/M−1; crop13: n+1/n+2), all
  subordinate to the frozen 0-BASED SUBS law; GT keeps `X_{N-2}`/`X_{N-1}`. The pattern itself
  is the finding: the tail-pair subscripts are sub-legible even at 3×, which is why every
  parser garbles them.
- **crop14_wordrow_wembtitle** (EXIT 0, winner attempt 2 after one 330 s hang): the capstone
  verdict. **"Word M2"/"Word M3" are confirmed misreads — the ink literally reads "Word N-2"
  [580,118,648,158] and "Word N-1" [652,118,722,158]** (italic *N* + hyphen fuses into an
  M-like blob at low res; the flagged italic "1" smears toward "3"). This **resolves the
  crop02 M-vs-N advisory in GT's favor with direct ink evidence**: the frozen 0-BASED SUBS law
  (P047) is exactly what the pixels show. `Word N-2`/`Word N-1` stay MISSING (no parse ever
  emitted them), but the failure mechanism is now visually characterized. **"Word 0"…"
  Word 5" all match ink verbatim** (per-box coords) — locks the cascade's 6 EXACT captures;
  **"Word Embedding" and "Positional Encoding / Embedding" both match ink** (extra gap after
  "Positional" is kerning, not a second space — advisory on GT's double-space form). The
  ellipsis is six gray circles (not text); in this crop's band the chip row reads as eight
  blue arrows only ("not text") — the X-chip ink lives in crop05/crop13's bands, no conflict.
- Judge program complete: all 9 legs + probe banked under `judges/` (9 OK legs, 0 exhausted; 6
  gateway aborts recorded in the banked logs — hang/empty-stream — all absorbed by retries;
  overwritten failed-attempt stdouts not counted).
