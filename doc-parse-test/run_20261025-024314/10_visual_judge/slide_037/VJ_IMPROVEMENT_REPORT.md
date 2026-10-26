skel

---

# Round 2 — slide_037_vj (wave-4 visual-judge loop, 2026-10-25 evening session)

## R2.1 State at round-2 start

Round 1 ended FAIL for 'call01_pass1 transcript fidelity to the slide image' with 9 defect
lines (6 HIGH / 2 MEDIUM / 1 LOW) and a crop channel that lifted union recall 79.3% → 96.6%
(5 strings: `Add & Norm`, `Feed Forward`, `Output Embedding`, `Masked Multi-Head Attention`
(normalized), `h`), leaving `Decoder` as the sole GT holdout.

## R2.2 Round-2 crop channel — the GT union closes (100%)

Four tight crops (LANCZOS 3x, `crops/round2/`), four parses (`parses/call05..08_round2/`,
all EXIT 0, 4-9 s each). Named-string results:

- **`Decoder` — EXACT, captured by call05 only** (crop05, a dedicated ~52x24 frame-px label
  crop upscaled 6x). This was the string round 1's crops failed to read even though crop01
  covered its region — the lesson banked: a holdout label gets its own minimal crop, not a
  shared column crop. Union recall: **29/29 = 100.0%** (measure_union.py re-run: EXACT=28,
  NORMALIZED=1 (`N x`), MISSING=0; +3.4 pts over round 1's 96.6%).
- Verbatim upgrades: `Feed Forward` EXACT (call06, superseding round-1's `Fixed Forward`
  garble), `Masked Multi-Head Attention` EXACT-with-hyphens (call06, superseding round-1's
  normalized hyphenless read), `Positional Encoding` / `Output Embedding` /
  `Outputs (shifted right)` re-read EXACT (call08).
- Crop-size law confirmed: the tightest crops read cleanest (call05: 58 chars, zero garbles);
  wider stack crops (call06/07) produced fresh garbles (`AUT Morm`, `Multi-lead Attention`,
  `Mid & Hem`, `Fred Howard`) — the same garble families round 1 saw at full-frame scale.
  call07 (encoder stack) was a total garble loss; its strings were already banked elsewhere.

## R2.3 Round-2 judge prompt (template v2) — defect-to-demand mapping

`judge/round2_prompt.txt` (10 826 bytes, frozen 2026-10-25 20:06; transcript under test
unchanged = call01_pass1, so any verdict is directly comparable to round 1). Each round-1
defect class is converted into a mandatory, output-shaped task:

| Round-1 defect (verdict FAIL) | v2 demand |
|---|---|
| 6 GT strings dropped while fully visible (`Add & Norm` ×4, `Feed Forward` ×2, `Output Embedding`, `Decoder`, `h`, `Masked Multi-Head Attention`) | Task 4 DROPPED-TEXT SWEEP: region-by-region census (title band, badge, inset-A, inset-B, map-pin, encoder column, decoder column, bottom bands), every visible string marked PRESENT/ABSENT/PARTIAL vs transcript, ending in a consolidated "VISIBLE IN IMAGE, ABSENT FROM TRANSCRIPT:" list; plus the 6-string WATCHLIST (W1-W6) with letter-by-letter reads and px anchors |
| Instance coverage ~26/56 (`Linear` 2/5, `MatMul` 1/2, `Multi-Head Attention` 2/3, `N x` 1/2, `Q/K/V` 3/15) | Task 5 INSTANCE-COVERAGE TABLE: 29 rows × (visible count, transcript count, FULL/PARTIAL/MISS verdict), with the five known shortfalls to confirm/refute by independent count |
| Line merges (`MatMul Concat` cross-inset; `Q K V` per group; title+badge "**…Multi-Head)** 37") | Task 7 MERGE AUDIT: three named merge sites M1-M3 + open-ended "any other fused line" |
| Structure failures: all text anchored at empty (60, 98.7); reading-order inversion; badge zone mis-tokened `class_Section-header`; Picture-box mis-bounds; `WE ARE HERE` rotation unrepresented | Task 8 STRUCTURE AUDIT S1-S4 (anchor-window check, reading-order naming, class-token audit, rotation/placement check) |
| 4 hallucinated strings (`Scalar Dot-Product Attention`, `Mult-Head Attention`, `Math-Head Attention`, `Max`) | Task 6 kept from v1 (exact-string image search + garble attribution) |
| Judge px estimates ran 20-30 px off; one region-label slip (upper `MatMul` called "inset-B top") | G4 revised: ±30 px advisory, region identity + instance counts weighted over exact numbers; task 2 requires the two MatMul boxes labeled by region |

## R2.4 Round-2 judge call — BLOCKED (no verdict this session)

The v2 prompt is designed and frozen but **untested by the gateway**: both judge attempts
hung past the 7-minute wall and were killed with empty bodies (hang discipline: hang → 60 s
wait → single retry → 2nd hang → blocker, per the wave-4 protocol).

| attempt | started | outcome |
|---|---|---|
| B (call 1) | 20:08:57 | RC=124 @420 s, empty body. Gateway stderr: `EmptyStreamError` → HTTP 502 upstream_unreachable → HTTP 504 upstream_timeout → race restart → silence. Banked `judge/round2_attemptB_hang_stderr.log` |
| C (single post-hang retry) | 20:22:30 | RC=124 @420 s, empty body. Internal attempt 1 `EmptyStreamError`, then silence. Banked `judge/round2_attemptC_hang_stderr.log` |
| diagnostic probe | 20:31 | tiny prompt, same image: EXIT 0 in 9.1 s, PROBE-OK — **route alive**; degradation isolated to heavy full-frame 10.8 KB-prompt vision calls (Nvidia upstream streaming). Banked `judge/probe3_*.log` |

Round-2 verdict therefore DOES NOT EXIST and must not be inferred; the round-2 row in
`ledger.md` records "NO VERDICT — judge leg BLOCKED". The mandate's one-retry limit was
reached exactly; a third call was out of protocol.

## R2.5 Prompt-v2 delta statement

Design-level delta only (no verdict evidence this session): v1 asked the judge to check
dropped strings among 6+ other charges and the round-1 report shows omissions still passed
unlisted; v2 makes omission detection a structural, output-shaped obligation (the sweep's
consolidated absence list + the 29-row coverage table cannot both be empty while the
transcript misses 6 GT regions and ~30 instances). Prediction on banked evidence: a v2 run
should return FAIL again (the transcript under test is unchanged and its HIGH defects are
unfixed), but with the defect list mechanically complete — every W1-W6 string and every
coverage shortfall named — which is the improvement the loop is testing.

## R2.6 Resume note (next session)

Rerun the frozen attempt-C command from `judge/round2_call.log` (prompt unchanged — do NOT
redesign v2; do NOT re-probe unless idle >10 min). On land: score the transcript per the
v2 tasks, append the round-2 verdict to the ledger row and a verdict subsection here, then
scope-close. The crop channel needs no further work — GT union is already 100%.

## R2.7 Resumed verdict — STILL NO VERDICT (retry session, 2026-10-25 ~20:43–21:05 EEST)

Verdict line: **NO VERDICT — round-2 judge leg blocked a second time.** The resume path
executed exactly as banked: probe4 (tiny prompt, same image, gateway idle ~14 min) returned
EXIT 0 in 32 s with PROBE-OK and 0 degenerate events; the frozen attempt-D command (prompt v2
byte-identical, 10 826 B, transcript under test call01_pass1 unchanged) hung and was wall-killed
at RC=124 with an empty transcript; after the mandated 60 s wait the single retry (attempt E)
hung identically — RC=124 @420 s, empty body, its stderr finally capturing the failure mode on
record: `ABORT EmptyStreamError: empty content: no deltas — abort+retry 1/3`, then silence to
the wall. Two fresh hangs banked (round2_attemptD/E_hang_stderr.log, resumed_attemptD/E.meta);
second hang in this session → stop per hang discipline.

What the DROPPED-TEXT SWEEP caught or did not catch: untestable this session — the sweep
lives inside prompt v2's demanded output shape, and v2 has now been submitted to the gateway
4 times (B, C, D, E) without a single byte of model output returning. No judgment can be made
about the sweep's catching power from zero responses; the claim in R2.5 ("a v2 run should
return FAIL again, with the defect list mechanically complete") remains a prediction, not a
result. The only new transcript-side evidence this session is negative: the gateway emits no
deltas at all for this call shape, so nothing downstream (sweep, coverage table, merge audit,
structure audit) ever begins.

Prompt-v2 delta statement: v2 is confirmed SUBMITTED (the gateway accepted and held the
connection for the full 420 s twice, with pid-level startup evidence in stderr) but still
UNTESTED by any model response — 4 consecutive heavy-call hangs across 2 sessions ~2 h apart
(20:0x–21:0x EEST), against 4/4 tiny-prompt probe greens (probe2, probe3, probe4, prior
diagnostic) on the same route and image. The isolation of the failure to the heavy
full-frame 10.8 KB-prompt vision call is now established with cross-session evidence; the
frozen-command rerun path is exhausted. Next-session levers, in order: (1) retry in a
different gateway-load window (all hangs cluster 20:0x–21:0x EEST); (2) ask the gateway owner
whether the `images` route streams deltas for large-vision-token requests (probe4 proves
streaming works for small ones); (3) founder-sanctioned prompt-size reduction (breaks the
do-not-redesign freeze, so requires explicit approval). Crop-channel result stands untouched:
GT union 29/29 = 100.0% (`Decoder` EXACT via call05_round2).

## R2.8 prompt-split attempt — STILL NO VERDICT (split session, 2026-10-25 ~21:45-22:23 EEST)

Verdict line: **NO VERDICT — the prompt-split path executed clean and blocked identically.**
Per the split mandate, frozen v2's content was redistributed (no new tasks) into two
sequential sub-calls, each under the 3,500-byte cap, both labeled template v2.1 (prompt-split
adaptation of frozen v2; size-correlated hang mitigation), both stating the transcript under
test (call01_pass1) and the image (slide_037.jpg, 960x540):

- **round2a DROPPED-TEXT SWEEP** (`judge/round2a_prompt.txt`, 3,496 B): v2's six-string
  watchlist (W1 `Add & Norm`, W2 `Feed Forward`, W3 `Output Embedding`, W4 `Decoder`,
  W5 `h`, W6 `Masked Multi-Head Attention`) with per-string positions + v2 task 4's
  region-by-region census + the consolidated "VISIBLE IN IMAGE, ABSENT FROM TRANSCRIPT:"
  list + terminal verdict. Both gateway attempts hung: RC=124 @420 s (21:50:37→21:57:37)
  and the mandated single post-60 s retry (21:59:54→22:06:54), 0-byte transcripts, stderr
  each time only the startup line + `ABORT EmptyStreamError: empty content: no deltas —
  abort+retry 1/3`, then silence. Second hang → sub-call stopped per discipline (stderrs
  archived as round2a_attempt1_hang_stderr.log / round2a_attempt2retry_hang_stderr.log).
- **round2b COVERAGE + STRUCTURE** (`judge/round2b_prompt.txt`, 3,495 B): v2 task 5's
  29-row table compressed to its top under-covered rows (Linear 2/5, MatMul 1/2,
  Multi-Head Attention 2/3, N x 1/2, Q/K/V 3/15 — labels + expected counts + region hints)
  + the 4-string hallucination check + merge audit M1-M3 + structure audit S1-S4 (v2's
  Picture-box mis-bounds sub-check was the one item dropped at the byte cap) + compact
  defect list + terminal verdict. Identical outcome: RC=124 @420 s (22:08:07→~22:15:07)
  and its single retry (22:16:23→~22:23:23), 0 bytes both times, same EmptyStreamError
  signature. Second hang → sub-call stopped (stderrs archived as round2b_attempt1_hang_
  stderr.log / round2b_attempt2retry_hang_stderr.log).

What each sub-call caught or did not catch: untestable — as with v2, the gateway emitted no
deltas at all, so neither the sweep (2a) nor the coverage/merge/structure audit (2b) ever
produced a first token; nothing downstream exists to score, and no catching-power claim is
made. The calls were strictly sequential (2b launched only after 2a's budget was exhausted),
after the gateway-serialization gate: slide_059_vj (agent-53) held the gateway until
21:34:58 (5 polls @120 s), and no concurrent full-frame judge ran against this session's
four calls.

Template v2.1 delta vs v2 (design intent vs evidence): v2.1 kept every v2 defect-to-demand
mapping except the Picture-box sub-check, halved the prompt, and split the charge so no
single call carried all ten v2 tasks. The size-correlation hypothesis it encoded is now
REFUTED as the sole discriminator: v2 (10.8 KB) hung 4/4 and the v2.1 halves (3.5 KB) hung
4/4 with the byte-identical EmptyStream signature, while tiny-prompt probes on the same
route and image return in seconds (4/4 green historically). Prompt text size alone does not
separate hang from land. Strongest remaining correlate: the load window — the only
heavy-call land on record is round-1's 7.1 KB v1 judge at 08:2x EEST; all 8 heavy-call
hangs sit in 20:0x-22:2x EEST. Next-session levers, re-ordered: (1) re-run the banked,
byte-frozen v2.1 sub-calls in a different-load window (no redesign needed); (2) the
gateway-owner streaming question for large-prompt vision requests; (3) image-side
mitigation (downscaled-frame judge pass) — untested and founder-sanction-gated since it
changes the judge's input.

Honest note: template v2 remains banked-untested (unchanged from R2.7), and v2.1 now joins
it — 8 consecutive heavy-call hangs across 3 sessions, 0 bytes of judge output beyond
round-1's landed v1 verdict. The round-2/2.1 judge channel carries NO verdict of any kind;
round-1 FAIL (9 defects, 6 HIGH) + the crop-channel GT union 29/29 = 100.0% remain the
standing evidence. Scope closed failed per the mandate's exhausted-budget branch, with the
split evidence banked here, in `ledger.md` (2.1-split row), and in
`judge/round2_call.log` (COMMAND/PROMPT/STARTED/EXIT/FINISHED for all four calls).
