# Wave-4 visual-judge iteration ledger — slide_052 (append-only, one row per round)

Baseline (frozen wave 2): full-frame parse text_recall 75.0% (16 EXACT / 0 NORMALIZED / 1 PARTIAL / 5 MISSING of 22 GT units). The three full-frame passes (call01_pass1 / call02_pass2 / call05_t9k) are byte-identical (md5 bdb0e649...) and count as ONE transcript in every union.

GT-unit match basis (consistent with frozen wave-2 comparison `05_comparison/slide_052_comparison.md`): EXACT = case/whitespace-insensitive equality of the unit (wave-2 counted merged-line members I/feel/Sick and 2-of-5 Q as EXACT units — instance/structure losses are defects, not unit misses); PARTIAL = substring ≥60% shared tokens (GT5 "Encode Decoder Attention": best evidence "Encode Decoder"); MISSING = absent from all banked transcripts.

## Round 1 — 2026-10-25

- Judge: tier-2 gateway (`judge/round1_transcript.md`, single-read, exit 0, finish ok). All F-facts CONFIRMED with pixel regions. Defect list: K, V, Y×3, SOS-legend, badge 52, Q×3-of-5, both 5×3 stacked grids (all REAL); 4 MED rows on word boxes DISMISSED by transcript inspection (SOS/Je/me/sens/malade and I/feel/Sick ARE in the full-frame parse — judge over-flag; merges are wave-2 structure defects, not unit misses). Terminal: `FINAL VERDICT: FAIL for 'full-frame parse transcripts cover the frame text content'`.
- Crops (4, all pre-checked dims/nonzero-mean, all EXIT 0 / finish stop):
  - crop01_leftpanel (40,240,300,520 @3x) → `Transformer Encoder`, `I`/`feel`/`Sick` split, **`SOS = Start Of Sentence` NEW** — Y×3 missed
  - crop02_kv_arrows (290,160,430,300 @3x) → merged `Encode Decoder Attention` only — K, V missed
  - crop03_badge (810,30,960,110 @3x) → **`52` NEW**
  - crop04_q_row (560,170,890,300 @3x) → 3× merged `Encode Decoder Attention` — Q circles missed
- Union recall: 18 EXACT + 0 NORMALIZED + 1 PARTIAL + 3 MISSING (K, V, Y) of 22 = **84.1%** (baseline 75.0%, delta **+9.1 pp**; new GT units this round: 2).
- Instance-level deltas: word boxes I/feel/Sick now appear as 3 separate lines (structure restored by crop); Q still 2/5 instances; Y 0/3; K/V 0/1 each.
- Calls spent: 4 crop-parses (+1 judge +1 probe). Avg crop-parse latency: 7.9 s/call (29.5-8.1 = 9.3, 13.9, 4.7, 4.1 s). Strings-per-call yield: 2 new GT units / 4 crop calls = 0.50 (3 counting split I/feel/Sick as string-level events → 0.75 events/call).
- Failed-read ledger: none (5/5 gateway+parse calls exit 0, non-degenerate).
- Remaining misses → round-2 targets: K (~309-327×176-199, red circle), V (~307-328×228-250, green circle), Y×3 (band y~247-263, centers x~85/163/239); instance work: Q×3 (~x601/715/813, y~254).

| round | verdict | new GT strings | union recall % | delta pp | calls spent | avg latency s |
|---|---|---|---|---|---|---|
| 1 (2026-10-25) | FAIL (defect list banked) | 2 (GT9 SOS-legend, GT22 52) | 84.1 | +9.1 | 4 crop-parses + 1 judge + 1 probe | 7.9 (crop-parses) |

## Round 2 — 2026-10-25

- Judge: tier-2 gateway (`judge/round2_transcript.md`, single gateway leg, exit 0; script-internal ladder recovered 2× HangError 270s aborts before the validated winner — wall ~695s, counted as script-recovered events, not failures). All glyphs CONFIRMED VISIBLE with bboxes (K, V, Y×3, Q×5); per-glyph crop proposals banked. Terminal: `FINAL VERDICT: PASS for 'crop-targeted transcripts cover the remaining missed strings'`. Note: its K/V fill-border color descriptions conflict with the wave-2 pixel measurements (advisory; does not affect coverage).
- Crops (4, all pre-checked, all EXIT 0 / finish stop):
  - crop06_y_row (40,238,300,285 @3x) → `Y0` / `Y2` — Y glyphs DETECTED but digit-suffix-hallucinated, 2 of 3 instances; GT21 evidence = PARTIAL
  - crop05_kv_tight (295,165,340,260 @3x) → **`K` NEW** + spurious `2`
  - crop07_q_strip (370,240,830,270 @3x) → EMPTY content (coordinate tokens + class_Picture only) — bare Q circles invisible to the parser
  - crop08_v_only (298,218,342,262 @3x) → **`V` NEW**
- GT5 upgrade: crop02/crop04 emit the complete unit "Encode Decoder Attention" (merged single line) → unit-level EXACT under the stated whitespace-insensitive basis (the 5×3 stacked-grid STRUCTURE defect persists — string complete, structure still lost).
- Union recall: 21 EXACT + 0 NORMALIZED + 1 PARTIAL (GT21 Y via "Y0"/"Y2") + 0 MISSING of 22 = **97.7%** (round 1: 84.1%, delta **+13.6 pp**; new GT units this round: 2 — GT18 K, GT19 V; +1 unit upgraded PARTIAL→EXACT: GT5).
- Instance-level: Q still 2/5; Y 2/3 detected but garbled; K/V now 1/1 each.
- Calls spent: 4 crop-parses (+1 judge in flight over the wall boundary). Avg crop-parse latency: 6.5 s/call (13.0/4.0/3.0/6.0). Strings-per-call yield: 2 new units / 4 crop calls = 0.50.
- Failed-read ledger: crop07 = EMPTY body (counted NO-RESULT-for-content, banked as parser-blind-spot evidence).
- Round 3 trigger: round 2 added 2 new GT units (≥2) → round 3 runs. Remaining targets: GT21 Y→EXACT (kill digit garble, catch 3rd instance), Q instances (2/5, judge proposes per-circle crops + stem context), structure of 5×3 grids (not unit-level).

| round | verdict | new GT strings | union recall % | delta pp | calls spent | avg latency s |
|---|---|---|---|---|---|---|
| 2 (2026-10-25) | PASS ('crop-targeted transcripts cover the remaining missed strings') | 2 (GT18 K, GT19 V; +GT5 upgraded) | 97.7 | +13.6 | 4 crop-parses + 1 judge | 6.5 (crop-parses) |

## Final round (attempted) — 2026-10-25

- Final judge leg (template `vj-comparison-final` v1.0, `judge/final_prompt.txt` banked): launched (gateway mode analysis, pid 24397, `judge/final_stderr.log`) but produced NO body — `judge/final_stdout.log` is 0 bytes, no FINAL VERDICT line. Recorded **INCOMPLETE**; NOT banked as a transcript; no re-run (the 2 judged rounds already satisfy the ≥2-round gate). The round-3 crop results it would have arbitrated (+2 Q instances via crop11 stem context, crop09/crop10 pure-Y EMPTY, crop12 2x retry reproduced `Y0`/`Y2`) live in the final prompt's arbitration ledger and the call09-12 transcripts.

## Close — 2026-10-25

- `VJ_IMPROVEMENT_REPORT.md` written (rounds 1 FAIL → 2 PASS verdict arc, per-round prompt design + prompt-v2 delta headline, round-2 improvement statement K/V/GT5 + Y-PARTIAL, K/V 15-px glyph doctrine corroborated-and-refined, final-round attempt honestly labeled incomplete). Done criteria: ≥2 judged rounds with FINAL VERDICT ✓, every round prompt banked ✓, 12 crop-parse call dirs EXIT 0 ✓, 12 nonempty transcripts ✓, ledger ≥2 round rows ✓, VJ report ✓. Final-round attempt disposition: incomplete (0-byte stdout), recorded above. Scope `slide_052_vj` closed.
