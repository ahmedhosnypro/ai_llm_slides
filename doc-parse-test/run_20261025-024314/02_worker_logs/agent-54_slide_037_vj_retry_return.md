All contract items are satisfied — both fresh hangs banked with EXIT codes, evidence appended everywhere, and scope-fail re-run and verified. Final hand-off:

## RETRY session result: round-2 judge still did NOT land — scope-failed again with updated evidence

**Close command (exact):**
```
"$DBCTL" scope-fail "$DB" slide_037_vj "round1 FAIL; round2 judge leg blocked AGAIN in retry session: resumed attempts D+E both hung RC=124@420s empty-body (E stderr: EmptyStreamError abort+retry 1/3) — 4/4 heavy-call hangs across 2 sessions vs probe4 green (PROBE-OK 32s); prompt v2 frozen+submitted but untested by any model output; crop channel stands GT union 29/29=100% (Decoder EXACT via call05); ledger row 2-retry + report R2.7 banked; frozen-rerun path exhausted, next levers: different load window / gateway streaming check / founder-approved prompt reduction"
```
**Output:** `1` (= `SELECT changes()`: 1 row updated). Verified in DB: `slide_037_vj | failed | 2026-10-25 18:07:03` (UTC = 21:07:03 EEST), note matches verbatim.

**Summary (what happened this session):**
1. Resume path executed verbatim: prompt v2 byte-identical (10,826 B), frozen attempt-C command rerun exactly; no scope-claim (row was `failed` throughout).
2. Gateway was idle ~14 min → probe4 permitted and green (EXIT 0, 32 s, PROBE-OK, 0 degenerate events) — banked as `judge/probe4_*.log`.
3. **Attempt D** (20:47:28→20:54:28): hang, RC=124 @420 s wall, transcript 0 bytes, stderr silent — banked (`resumed_attemptD.meta`, `round2_attemptD_hang_stderr.log`).
4. 60 s wait, then **attempt E** (single retry, 20:56:36→21:03:36): hang again, RC=124, empty body; stderr finally captured `ABORT EmptyStreamError: empty content: no deltas — abort+retry 1/3` then silence — banked (`resumed_attemptE.meta`, `round2_attemptE_hang_stderr.log`).
5. Second hang in session → stop per hang discipline. Cumulative evidence: 4/4 heavy full-frame 10.8 KB-prompt calls hung (B, C, D, E across 2 sessions) vs 4/4 tiny-prompt probe greens on the same route/image.
6. Ledger updated: new `2-retry` row (no verdict, +0.0 pts, union stays 100.0%) — original rows untouched. `VJ_IMPROVEMENT_REPORT.md` gained append-only `## R2.7` (verdict line, DROPPED-TEXT SWEEP untestable with zero model output, prompt-v2 delta statement). `round2_call.log` carries full D+E chronology + superseding resume note. One self-inflicted log defect (attempt-E launch Edit clobbered the D-RESULT line) was caught in the final verification sweep and restored verbatim.
7. Writes stayed inside `$S/10_visual_judge/slide_037/` + the commands log; video namespace read-only; no image bytes in context; no git, no deletions.

**Scope remains `failed` — scope-done was correctly NOT run.** Recommended next levers (recorded in the resume note): retry in a different gateway-load window (all hangs cluster 20:0x–21:0x EEST), check whether the `images` route streams deltas for large-vision-token requests, or a founder-approved prompt-size reduction.