# Iteration ledger — slide_037_vj (wave-4 visual-judge loop, append-only)

Baseline (wave-2 frozen): label-level text_recall **79.3%** (23/29 GT strings,
call01_pass1; call02_pass2/call05_t9k/call06_t9k_retry are 2/29 minimal reads).
Instance baseline: ~26/56 legible instances (46%). Hallucinations confirmed: 3
groups / 4 strings. GT string list: `04_ground_truth/slide_037/inventory.md` (29).

| round | verdict (transcript) | new GT strings | union recall | delta | calls spent (crop-parse + judge) | avg latency |
|---|---|---|---|---|---|---|
| 1 | FAIL for 'call01_pass1 transcript fidelity to the slide image' | 5 — Add & Norm, Feed Forward, Output Embedding, Masked Multi-Head Attention (normalized), h | 96.6% (28/29) | +17.3 pts | 4 crop parses (all stop, 3-9s) + 2 judge calls (1 wall-hit RC=124 no body, 1 landed ~25s) | 6.4s/crop parse |

| 2 | NO VERDICT — judge leg BLOCKED: 2 consecutive hangs (RC=124 @420 s wall both, empty body; gateway `images` route returned EmptyStreamError → HTTP 502 → HTTP 504 inside attempt B, EmptyStreamError inside attempt C; tiny-prompt probes green ×3 — route alive, degradation isolated to heavy full-frame 10.8 KB-prompt vision calls) | 1 — `Decoder` (EXACT, call05_round2, tight 6x decoder-label crop crop05 (x≈792-844,y≈100-124)) | 100.0% (29/29; measure_union.py: EXACT=28 NORMALIZED=1 PARTIAL=0 MISSING=0) | +3.4 pts (96.6 → 100.0) | 4 crop parses (call05-08_round2, all EXIT 0, 4-9 s each) + 2 judge calls (both wall-killed hangs, 0 body) + 3 probes (6.4 s, 9.1 s, diagnostic — all PROBE-OK) | 420 s/judge attempt (killed); 6.4 s/crop parse |

| 2-retry | NO VERDICT (again) — resumed attempt D hang (RC=124 @420 s, 20:47:28→20:54:28, empty body, stderr silent) then attempt E hang (RC=124 @420 s, 20:56:36→21:03:36, empty body, stderr shows `ABORT EmptyStreamError: empty content: no deltas — abort+retry 1/3` then silence); 60 s wait + probe4 green between them (EXIT 0, 32 s, PROBE-OK, degenerate 0); prompt v2 byte-identical throughout — cumulative 4/4 heavy-call hangs vs 4/4 probe greens across 2 sessions ~2 h apart | 0 — none (crop channel already closed; no new parses this session) | 100.0% (29/29, unchanged) | +0.0 pts | 2 judge calls (both wall-killed hangs, 0 body) + 1 probe (probe4, 32 s, PROBE-OK) | 420 s/judge attempt (killed); 32 s/probe |

**Round-2 prompt design rationale (template v2, `judge/round2_prompt.txt`, 10 826 bytes, frozen
2026-10-25 20:06):** every round-1 HIGH/MEDIUM defect is encoded as a mandatory demand —
(a) dropped-string failure mode → task 4 DROPPED-TEXT SWEEP (region-by-region census with a
consolidated "VISIBLE IN IMAGE, ABSENT FROM TRANSCRIPT" list) + a 6-string watchlist
(W1 `Add & Norm` ×4, W2 `Feed Forward` ×2, W3 `Output Embedding`, W4 `Decoder`, W5 `h`,
W6 `Masked Multi-Head Attention`) demanding letter-by-letter reads; (b) instance-coverage
loss → task 5 coverage table (29 rows, visible-count vs transcript-count, confirm/refute
Linear 2/5, MatMul 1/2, Multi-Head Attention 2/3, N x 1/2, Q/K/V 3/15); (c) line merges →
task 7 MERGE AUDIT (title/badge "…Multi-Head)** 37" fusion, MatMul Concat cross-inset
fusion, Q K V fusion, plus open-ended "any other fused line"); (d) structure failures →
task 8 STRUCTURE AUDIT (empty-anchor check at (60, 98.7), reading-order inversion, badge
`class_Section-header` token, Picture-box mis-bounds, WE ARE HERE rotation); (e) hallucinations →
task 6 kept (Scalar/Mult-Head/Math-Head/Max); (f) round-1 px-estimate noise → G4 revised
(±30 px advisory; region identity + counts weighted over exact numbers). Transcript under
test unchanged (call01_pass1) so a round-2 verdict is directly comparable to round 1.

**Round-2 vs round-1 deltas:** crop channel completed the GT union (round 1 ended 28/29;
`Decoder` was the sole holdout — round-1's crop01 covered its region but the parser still
dropped it; round-2's dedicated 6x label crop read it EXACT). Garble-residue class confirmed
crop-size-dependent: tight crops (call05, 58 chars) read clean; wider stack crops (call06/07)
produced fresh garbles (`AUT Morm`, `Mid & Hem`, `Fred Howard`) while still upgrading `Feed
Forward` and `Masked Multi-Head Attention` to EXACT. Judge channel: no verdict — prompt v2
is banked and frozen, UNTESTED by the gateway this session; first landable run resumes from
the attempt-C command in `judge/round2_call.log`.

| 2.1-split | NO VERDICT (third session, prompt-split mandate) — frozen v2's content redistributed into two ≤3.5 KB sequential sub-calls, 2a DROPPED-TEXT SWEEP (judge/round2a_prompt.txt, 3,496 B) and 2b COVERAGE+STRUCTURE (judge/round2b_prompt.txt, 3,495 B), transcript under test unchanged (call01_pass1); each sub-call hung twice: RC=124 @420 s + 60 s wait + single retry + 2nd hang RC=124 @420 s, all empty-body EmptyStreamError (2a 21:50:37/21:59:54, 2b 22:08:07/22:16:23 EEST) — 0 bytes of model output ever returned; both sub-call budgets exhausted per hang discipline | 0 — none (crop channel untouched; no parses this session) | 100.0% (29/29, unchanged) | +0.0 pts | 4 judge calls (all wall-killed hangs, 0 body) + 0 probes (gateway answered nothing this session; own-call rule) | 420 s/judge attempt (killed) |

**Prompt-split rationale and outcome (template v2.1, banked 21:45, executed 21:50-22:23):**
the split mandate tested the size-correlation hypothesis (v2 10.8 KB hung 4/4 vs tiny-probe
greens) by redistributing v2's content — no new tasks — into two half-size sequential judge
calls: 2a = v2 watchlist + task-4 sweep + terminal verdict; 2b = v2 tasks 5-9 compact
(coverage on the five top under-covered labels Linear 2/5, MatMul 1/2, Multi-Head Attention
2/3, N x 1/2, Q/K/V 3/15, the 4-string hallucination check, merges M1-M3, structure S1-S4,
defect list, verdict; v2's Picture-box mis-bounds sub-check was the one item dropped at the
byte cap). RESULT: hypothesis REFUTED as the sole discriminator — 3.5 KB hung byte-identically
(4/4 RC=124 empty-body EmptyStreamError). Prompt text size alone does not separate hang from
land: the only heavy-call land on record remains round-1's 7.1 KB v1 judge at 08:2x EEST,
while all 8 heavy hangs sit in the 20:0x-22:2x EEST window. Top next-session lever:
re-run the banked, byte-frozen v2.1 sub-calls in a different-load window (no redesign
needed), then the gateway-owner streaming question. v2.1 joins v2 as banked-untested; crop
channel GT union 29/29 = 100.0% stands.
