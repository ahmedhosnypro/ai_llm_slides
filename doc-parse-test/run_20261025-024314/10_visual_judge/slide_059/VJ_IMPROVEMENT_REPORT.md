# VJ improvement report — slide_059 (doc-parse wave-4)

Scope `slide_059_vj` · worker `worker-slide_059_vj` · 2026-10-25 · run `doc-parse-test/run_20261025-024314`
Source frame: `videos/deep-learning/002_transformers_part2/unique_slides/slide_059.jpg` (960×540, md5 `fb03ceaae946177062b7e097d68ffde3`, recorded in `probe/frame_md5.txt`).

## Headline

**Round 1 judged: FAIL** (full-frame transcript fidelity vs the original frame) · **Round 2 judged round: NOT ACHIEVED — infrastructure blocker** (Tier-2 gateway vision lane wedges audit-class requests; 8/8 zero-delta hangs across 5 attempts + a dead fallback leg, A/B-proven against a 3/3-passing probe). Nothing was fabricated: no round-2 verdict exists. The round-2 prompt work (v2 + v2.1), the probe-gated retry procedure, and all findings below are banked for the next healthy window. The **parse gate is cleared**: 4 nonempty crop-parse transcripts (call01–03 round-1 + call04 retry4).

Recall trajectory (46-string GT, `measure_recall.py`): **58.7% (wave-2 frozen) → 88.0% (40.5/46; EXACT 14 + NORMALIZED 25 + PARTIAL 3)** — the round-1 crop work (+29.3 pp) is banked in ledger rows 1–2; still missing X₀, X₁, Y₀, Y₁.

## Rounds

| round | judge leg | verdict | outcome |
|---|---|---|---|
| 1 | Tier-2 gateway, route `images`, 13.4 s, single-read unconfirmed | **FAIL** — `FINAL VERDICT: FAIL for 'doc-parse full-frame transcript fidelity vs the original slide_059 frame'` | defect list + 6 verifications + additional misses banked (`judge/round1_transcript.md`); 4 crops parsed (3 OK + 1 infra-failed ×3, later cleared) |
| 2 | **BLOCKED** — see forensics | none (no verdict produced) | prompt v2 (9845 B) + v2.1 compact (6448 B) banked; 8 zero-delta hangs; GLM-5.3 fallback dead; probe-gated retry procedure documented |

## Round-2 prompt design (the exercise's work — banked, unexecuted by the model)

Round-1's transcript failed in three specific modes; template v2 (round 2) targets each with a dedicated section:

1. **TEXTLESS-REGION OMISSION** — round 1 reported only text defects; regions with no text were neither covered nor declared, so transcript silence there was indistinguishable from a miss. v2 adds **Section A: region-by-region coverage table (R1–R14)** with a forced four-way state per region: PRESENT / GARBLED / ABSENT-DEFECT / **TEXTLESS-OK** ("frame shows no text there — transcript silence is the CORRECT state; say so explicitly instead of skipping").
2. **THE 1C1/1C2 HALLUCINATION-MISREAD CLASS** — the transcript emitted `1C1`, `1C2` where the frame shows subscripted `C₁ C₂ C₃` (stray leading glyph + lost subscript; same family as the adjudicated `1C3` in the crop transcripts). v2 adds **Section B: short-token classification** of all 12 suspicious tokens (`1C1 1C2 59 + Yd Xd Xx XN Xt Yk YNz YNd`) → MATCH / MISREAD→actual-string / INVENTED / UNRESOLVED, glyph-by-glyph, positions mandatory — "never accept a token because it is close".
3. **GROUPED INSTEAD OF PER-STRING ACCOUNTING** — round 1 wrote "all X labels absent"; v2 demands every missed/garbled string **named individually** with region fx..fx, fy..fy (rule 6: counts matter, frame count vs transcript count), with a row-per-line allowance that still enumerates every string on that line.
4. Verifications sharpened to the known soft spots: **first two labels of each token row with subscripts digit-by-digit** (the unresolved X₀/X₁, Y₀/Y₁), circle interiors per-circle in order, the pooled row's textless status + visible-cell count (build renders ~20 cells; frame is the authority), badge-circle contents, and frame-vs-transcript counts for all repeated elements.

v2 → v2.1 compaction (9845 → 6448 B) preserved all three devices and bounded the output shape (R1–R9 merged table, Q1–Q5) after the full form hung 6×; the compaction changed nothing about the wedge (see forensics), so both are banked as equally-valid prompts for retry.

## What the banked evidence establishes (independent of the blocked judge leg)

- **Textless-region finding, machine-side**: the thrice-failed crop04 (pooled row) succeeded on its 4th attempt (`call04_round1_retry4`, EXIT 0, finish=stop, 4.1 s) and returned **corner coordinates + `<class_Picture>` and ZERO text tokens** — the correct transcript for a region with no text. The 3 earlier failures were pure infrastructure (`Connection refused`, banked in retry2/retry3 stderr), masking a faithful-empty result. This is exactly the TEXTLESS-OK state the round-2 template forces the judge to declare — and the doc-parse parser already behaves correctly on textless regions.
- **1C1/1C2 class, crop-corroborated**: the full-frame transcript's `1C1`/`1C2` (frame: `C₁ C₂ C₃`) extends into the crop transcripts as `1C3` (ledger row 1, advisory). The pattern is systematic: leading-glyph hallucination + subscript loss on short serif labels — round-2 Section B is built to force per-token adjudication of exactly this class.
- **Recall accounting**: retry4 adds 0 strings (textless row carries no GT text); union stays 88.0% (40.5/46); X₀ X₁ Y₀ Y₁ remain the only misses (subscripts unresolved at crop scale per round-1 crop reads).

## Judge-efficiency & infrastructure forensics (why round 2 did not happen)

- Attempt log (all banked in `judge/round2_call.log` + `round2_stderr.log`): ①20:12 EmptyStreamError + HTTP 502 `upstream_unreachable` · ②20:17 hang >7 min → killed (stderr: EmptyStream ×2 + HTTP 504 `upstream_timeout`) · ③20:34 contract retry (60 s wait honored) 3× HangError 270 s, EXIT 1 · ④20:52 **disclosed fallback `--models GLM-5.3`** (AGENTS.md-documented fallback family, same gateway) read-timeout 240 s — and the GLM **tiny probe** also read-timed-out → GLM serving independently dead · ⑤20:56 probe3 (images route) **PASSED 42 s, `59.`** → recovery declared · ⑥21:00 post-recovery 2× HangError 270 s, killed · ⑦21:10 compact v2.1 + `--timeout 300` HangError 330 s, killed · ⑧21:21 **probe-gated**: gate probe PASSED ~2 s, audit fired in the same serving window → HangError 360 s; retry-2 stopped as predetermined.
- **A/B result**: tiny probe (93 B prompt, same image, same route) served **3/3** (2 s / 42 s / 2 s); audit-shaped requests (6.4–9.8 KB) served **0/8** with zero stream deltas across 270–480 s walls. CLI hardcodes `stream:true` (founder directive) with thinking disabled — no non-streaming path exists to route around a stuck stream.
- Interpretation: the upstream serving layer wedges audit-class requests this evening; the lane was healthy at 08:16 (round-1 audit, 13.4 s) and the doc-parse service (separate) recovered by 20:03 — the vision lane did not within this window. Scope-fail taken per the blocker contract; the ledger row 3 carries the retry recipe (probe gate → v2 full at `--timeout 240`, v2.1 compact fallback).

## Artifacts (all under `$RUN/10_visual_judge/slide_059/`)

- `judge/round1_prompt.txt` (frozen v1), `round1_transcript.md` (+ gateway body banked at run time) — round 1
- `judge/round2_prompt.txt` (v2 full), `round2_prompt_v21_compact.txt`, `round2_prompt_v2_full_hung_variant.txt`, `round2_call.log` (7-attempt disposition chain), `round2_stderr.log` (last attempt) — round 2 design + blocker evidence
- `probe/probe4_gate.txt` (+ probe2/3 stdout+stderr) — gate-probe transcripts for the A/B finding
- `crops/round1/` + `crops/round2/` (8 pre-checked crops, boxes in `precheck.txt`); `parses/call01–03_round1` + `call04_round1{,_retry2,_retry3,_retry4}` (5-file convention; retry4 EXIT 0 finish=stop)
- `ledger.md` — 3 append-only rows (round 1 · crop04 disposition · round-2 BLOCKED); `measure_recall.py` (frozen matcher)
