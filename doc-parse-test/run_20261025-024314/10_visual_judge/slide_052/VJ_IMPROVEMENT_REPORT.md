# VJ improvement report — slide_052 (doc-parse wave-4)

Scope `slide_052_vj` · worker `worker-slide_052_vj` · 2026-10-25 · run `doc-parse-test/run_20261025-024314`
Source frame: `videos/deep-learning/002_transformers_part2/unique_slides/slide_052.jpg` (960×540; Transformer encoder-decoder attention block schematic, no title bar).

## Headline

**Union text recall 75.0% → 97.7% (+22.7 pp)** over the judged rounds, verdict arc **round 1 FAIL → round 2 PASS**, on 12 crop-parse calls (4/4/4 across rounds 1-3). Every one of the 12 crop calls finished EXIT 0. The judged-arc improvement (round 1 → round 2) is **+13.6 pp (84.1% → 97.7%)**, driven entirely by the round-2 prompt redesign that converted the judge from a coverage auditor into a tight-crop targeting instrument.

**Prompt-v2 delta headline:** round 1's prompt asked *"what does the transcript miss?"* (full-frame audit, 5 confirm/refute facts, active hunt, broad defect list); round 2's prompt asked *"where exactly are the remaining glyphs, and give me the crop boxes"* (per-glyph bbox + fill/border verification, 1-2 TIGHT crop proposals per still-missing string, 3x-LANCZOS ≤1664×2048 sizing constraint, verdict reframed to crop-targeted coverage). The judge's round-2 crop proposals directly defined the two crops that recovered K and V — the strings round 1's wider crops had missed.

**Doctrine finding (headline corroboration of the cascade-wave result):** the 15-22 px K/V/Q/Y glyphs are invisible to doc-parse at full-frame input at ANY token budget (1024/3000/9000-token passes byte-identical, md5 `bdb0e649…`: K/V/Y fully absent, Q only 2/5 instances) — while the judge leg reads every one of them cleanly from the same frame. Doc-parse's blindness is input-form-dependent, not resolution-fated.

Honesty note (per addendum): doc-parse's prompt was never editable (wire contract carries `decoding` only). Every gain came from **input-form engineering** (judged-defect-targeted PIL crops, LANCZOS 3x, ≤1664×2048) + **judge-driven targeting** (round 2's per-glyph crop-box proposals).

## Recall trajectory

| stage | union recall (22-unit GT) | detail |
|---|---|---|
| wave-2 frozen baseline (full-frame passes) | 75.0% (16 EXACT / 0 NORM / 1 PARTIAL / 5 MISSING) | 3 passes byte-identical (`bdb0e649…`); K, V, Y, SOS-legend, badge 52 missing; Q 2/5; 5×3 stacked grids shredded |
| round 1 (+4 crops: leftpanel, kv_arrows, badge, q_row) | 84.1% (18 EXACT / 1 PARTIAL / 3 MISSING) | +2 units: GT9 `SOS = Start Of Sentence` (leftpanel), GT22 `52` (badge); I/feel/Sick restored as separate lines. K, V, Y still MISSING. Judge verdict: **FAIL** ('full-frame parse transcripts cover the frame text content') |
| round 2 (+4 crops: kv_tight, v_only, y_row, q_strip) | 97.7% (21 EXACT / 1 PARTIAL / 0 MISSING) | +2 units: GT18 `K` (kv_tight 295,165-340,260 @3x), GT19 `V` (v_only 298,218-342,262 @3x); GT5 `Encode Decoder Attention` upgraded PARTIAL→EXACT. Y detected but digit-hallucinated (`Y0`/`Y2`, 2/3 instances → GT21 stays PARTIAL); bare Q-strip EMPTY. Judge verdict: **PASS** ('crop-targeted transcripts cover the remaining missed strings') |
| round 3 (+4 crops: y_band, y_single, q_context, y_row2x — crops only, no judged round) | 97.7% (unchanged) | +0 units: pure-Y crops (band 62,243-268,257 @3x; single 70,240-103,268 @3x) both EMPTY; 2x Y-row retry reproduced `Y0`/`Y2`; stem-context Q crop (580,230-840,290 @3x) added 2 more `Q` instances + 2 `Attention` lines (Q instances 2/5 → 4/5) |

Final composition: **21 EXACT + 1 PARTIAL (GT21 `Y` via `Y0`/`Y2`)** = 21 + 0.5-weighted evidence; the sole non-EXACT unit is Y.

## Judge round design — what each round's prompt demanded and why it changed

- **Round 1 (template `vj-comparison-r1`, v1.0) — full-frame coverage audit.** The judge received the full-frame parse transcript (3 byte-identical passes) and 5 prior FACTS (F1-F5) to CONFIRM/REFUTE on the image, plus an active-hunt clause (F5: find ANY text the transcript lacks) and a broad defect list with `REAL | NOT-IN-GT` tagging against the certified 22-unit GT. Purpose: an unanchored inventory of everything the full-frame parser misses. Outcome: all F-facts CONFIRMED with pixel regions; 15-row defect list; verdict FAIL. Quality note: 4 MED rows (word boxes SOS/Je/me/sens/malade, I/feel/Sick) were judge over-flags — the strings ARE in the full-frame parse (dismissed by transcript inspection; the merges are wave-2 structure defects, not unit misses).
- **Round 2 (template `vj-comparison-rN`, v1.0) — residual targeting.** Scope narrowed to "ONLY the regions round 1 left uncovered"; the round-1 arbitration (recovered strings, still-missing strings, and the round-1 crop failure on K/V) was banked into the preamble so no judge attention was re-spent on covered ground. New demands: (a) per-glyph verification — K bbox + circle fill/border, V same, Y×3 same, Q×5 bboxes, each CONFIRMED VISIBLE or unreadable-at-this-resolution; (b) CROP-BOX PROPOSALS — 1-2 TIGHT crop boxes per still-missing string, isolating the glyph from line art, sized for a 3x LANCZOS upscale ≤1664×2048; (c) verdict reframed to crop-targeted coverage. Why it changed: round 1 established WHAT is missing; round 2 needed the judge to act as a targeting instrument. Its proposals (K `(302,170)-(335,203)`, V `(300,222)-(334,255)`, Y band, per-circle Q boxes) are the direct source of the round-2 crop set — and unlike round 1's 140×140 kv_arrows crop (which contained K+V+line art and returned only a merged attention label), the near-single-glyph crops succeeded.
- **Final leg (template `vj-comparison-final`, v1.0) — attempted, not completed** (see disposition below). Would have closed the campaign over the union of ALL banked transcripts (full-frame + 12 crops), with the rounds 1-3 arbitration ledger as prior: Y-suffix hallucination check, which 5th Q circle remains missed, and spot-checks of the recovered strings.

## Round-2 improvement statement (what round 2 recovered that round 1 missed)

Round 1 ended with union 84.1% and three units MISSING (K, V, Y) plus the Q instance gap (2/5). Round 2's prompt-driven crops recovered:

- **GT18 `K`** — crop05_kv_tight (295,165,340,260 @3x, the judge's proposed box), EXACT. Spurious `2` token in the same output — edge-of-reliability marker on a 19×24 px source glyph.
- **GT19 `V`** — crop08_v_only (298,218,342,262 @3x), EXACT.
- **GT5 `Encode Decoder Attention`** upgraded PARTIAL→EXACT (crop02/crop04 emit the complete merged line; the 5×3 stacked-grid STRUCTURE defect persists — string complete, structure still lost).
- **GT21 `Y`** — detected for the first time (crop06_y_row: `Y0`/`Y2`, 2/3 instances) but with hallucinated digit suffixes; evidence improves to PARTIAL, unit not recovered.
- **GT20 `Q`** — no instance progress in round 2 itself (crop07_q_strip, a bare circle strip, returned EMPTY); round 3's stem-context crop later added 2 instances → 4/5.

Net: MISSING 3→0, EXACT 18→21, union 84.1%→97.7% (**+13.6 pp round-over-round; +22.7 pp over baseline**). Instance-level residual: Q 4/5, Y 2/3-garbled.

## The K/V 15-px glyph doctrine (corroborated and refined)

The cascade-wave doctrine holds and sharpens on this slide:

- **Full-frame, any budget:** K, V, Y entirely absent; Q 2/5 — the 1024/3000/9000-token passes are byte-identical, so budget cannot buy these glyphs.
- **Multi-element crops don't rescue them:** round 1's kv_arrows crop (140×140 source @3x, containing K and V) returned only the merged `Encode Decoder Attention` line — nearby line art and labels crowd the glyphs out.
- **Only near-single-glyph crops partially escape:** round 2's tight crops (glyph ≈ the whole frame) extracted K and V (K with a spurious `2`), while anchor-less circle/strip crops stayed empty (q_strip) and pure-Y crops returned EMPTY at 3x and reproduced `Y0`/`Y2` at 2x.
- **The judge reads them all cleanly from the same 960×540 frame** — every glyph CONFIRMED VISIBLE with pixel bboxes and fill/border descriptions: K `(309,176)-(327,199)` red ring, V `(307,228)-(328,250)` green ring, Y×3 `~(83,247)-(249,263)` red tags, Q×5 `(373,251)-(865,271)` blue circles. The glyphs are legible pixels; the deficit is doc-parse's, not the image's.
- **Q is the cleanest corroboration:** five 15-22 px blue circles with no in-crop text anchor resisted every doc-parse input form tried across rounds 2-3 (bare strip EMPTY, stem-context only partial at 4/5), while the judge read all five with bboxes.

Advisory (banked in ledger): the round-2 judge's K/V fill-border color descriptions conflict with the wave-2 pixel measurements — noted, does not affect the coverage verdict.

## Final-round disposition (honest labeling)

A final closing judge leg was **attempted but never completed**: `judge/final_prompt.txt` (vj-comparison-final v1.0) is banked and the gateway leg launched (`judge/final_stderr.log`: mode analysis, pid 24397), but `judge/final_stdout.log` is **0 bytes** — no judge body, no FINAL VERDICT. Per scope instructions it is recorded INCOMPLETE and NOT banked as a transcript; no re-run was made (the two judged rounds already satisfy the ≥2-round gate). The round-3 crop results it would have arbitrated (Y stays the sole PARTIAL; Q 4/5; recovered strings K/V/SOS-legend/52 all EXACT) live in the final prompt's arbitration ledger and in the parses/ transcripts themselves.

## Remaining misses (0.5 weighted / 22) — parked with labels

- GT21 `Y` ×3 — detected only as `Y0`/`Y2` (hallucinated digit suffixes), 2/3 instances; pure-Y crops empty at 3x, 2x retry reproduces the garble. Never read as plain `Y` by doc-parse; judge confirms the tags are plain `Y`.
- GT20 `Q` instance 5/5 — 4 of 5 circles captured (2 from full-frame + 2 via stem-context crop); the bare-circle form is unreadable to doc-parse in every crop tried.
- Structure (not unit-level): the two 5×3 stacked attention-label grids remain shredded in all transcripts (strings complete, line structure lost) — a wave-2 structure defect outside unit recall.

## Artifacts (all under `$RUN/10_visual_judge/slide_052/`)

- `judge/`: `probe_transcript.txt` (gateway PROBE-OK), `round1_prompt.txt` + `round1_transcript.md` (FAIL, 15-row defect list), `round2_prompt.txt` + `round2_transcript.md` (PASS, per-glyph confirmations + crop proposals), `final_prompt.txt` (banked, v1.0) + `final_stderr.log` (startup only) + `final_stdout.log` (0 bytes — final leg incomplete)
- `crops/round1/` (crop01-04), `crops/round2/` (crop05-08), `crops/round3/` (crop09-12) — 12 PNGs, pre-checked (dims + nonzero mean)
- `parses/call01_round1 … call12_round3/` — 12 call dirs, 5-file convention, all EXIT 0, all nonempty transcripts (2 deliberately content-EMPTY: crop07_q_strip, crop09/crop10 — banked as parser-blind-spot evidence; the call transcripts themselves are nonempty class/coordinate output)
- `ledger.md` — append-only rounds 1-2 + final-attempt + close rows
- Crop-parse latency: round 1 avg 7.9 s/call, round 2 avg 6.5 s/call, round 3 avg 4.0 s/call (2/3/4/7 s)
