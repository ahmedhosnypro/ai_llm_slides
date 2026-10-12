# Monitor report — second dispatch on slide 022 (double-dispatch race, resolved)

**Writer:** the SECOND resume worker dispatched for slide 022 (session started ~11:15).
**Status at close: STOOD DOWN — the slide was certified by the other live worker
(worker 2); this dispatch verified the certification independently and wrote nothing
to any shared artifact except the one disclosed overwrite below.**

## Timeline of the race (all times 2026-10-12 EEST)

- 09:05–10:06 — worker 1 (per worker 2's report; "dead builder" in the dispatch I
  received): measures 1–18, build v1, pptx, render_1, selfchecks 1–3, 4x crops.
- ~11:10 — worker 2 (its own resume note in build_attempt_2.js) resumes.
- ~11:15 — THIS dispatch starts; reads the banked state (17_worker_instructions,
  playlist + video AGENTS, shared_patterns/index.json, selfchecks 1–3, build v1,
  spec, SOURCES.md, P2 pattern assets of 020/021).
- 11:21:37 — THIS worker rebuilt the pptx from the unchanged build v1 and re-rendered
  it over `qa/slide022/render_1.png` — **disclosed overwrite**; pixel comparison before
  any judge existed: 0 of 2,251,225 pixels differ vs the banked render (build v1 is
  deterministic), so no evidence content was lost. `house_chrome_check.py` PASS.
- 11:19–11:21 — worker 2's selfcheck_attempt_4 lands (concurrency detected here).
- 11:39–11:45 — worker 2 banks build_attempt_2 (em calibration), build_attempt_3
  (widths ≤3.5%, row-3 digits → Arial bold), render_3.
- 11:50 — worker 2 banks judge_prompt_1, sets gen_status=judging.
- 12:09–12:16 — worker 2 rides out a probe hang (sleep 300 + re-probe, per protocol;
  gateway congested — slide 055's judge in flight simultaneously).
- 12:19 — judge_attempt_1: coherent FAIL, 1 MAJOR (missing dashed container on strip 3).
- 12:24 — worker 2 fixes (re-adds the accidentally dropped lane3 `drawLane`),
  render_4 + build_attempt_4 banked; pptx rebuilt 12:24:04.
- 12:30 — judge_attempt_2: coherent **PASS** (4 MINORs, no BLOCKER/MAJOR).
- 12:32 — worker_report.md banked; DB: gen_status=passed, visual_check=PASS,
  visual_attempts=2, visual_transcript=judge_attempt_2.txt.
- 12:24+ — worker 2 banks p2_member_notes_022.js; slide 034 (P2#4) becomes unblocked.

## THIS dispatch's independent verifications (read-only)

1. **Attempt-1 MAJOR was REAL:** PIL census on render_3 — lane3 top dash 0 dark
   columns (original: 176 spanning x 171–877), left side 0 vs 33, fill 31 px — the
   row-3 container was genuinely absent (worker-2's edit had dropped the drawLane).
   Judge attempt 1 correctly blocked it.
2. **Attempt-2 fix verified:** render_4 lane3 top dash 1163 cols (span 321–1872),
   bottom 1115, left 15, fill 76,852 px — matches lanes 1/2 rendering class.
3. `house_chrome_check.py` on render_4: **PASS** (panel x 89–1913, badge (1860,148)).
4. Provenance: `build/slide_022.js` byte-identical to `build_attempt_4.js`; pptx
   (12:24:04) matches the judged render_4 (12:24:06); single-version deliverable,
   no equations/graphs (no OMML wrap or graphgen needed).
5. Judge attempt 2 transcript: real comparison body, coherent verdict line,
   4 MINORs (+δ size/weight, arrow anchor, digit weight, dot size) — no BLOCKER/MAJOR.
6. DB end state confirmed via `15_progress.py get 22`; `deps` shows slide 034
   unblocked (pattern gate P2#3 satisfied).

## Lessons for the orchestrator

- The fleet dispatched TWO resume workers on the same slide simultaneously
  (this one and worker 2). Both executed the protocol correctly and detected the
  overlap through artifact mtimes; zero evidence was lost. But double dispatches
  risk judge double-spend — dedupe on the DB row's `updated_at`/gen_status before
  dispatching a resume.
- Worker numbering here: "worker 1" = the 09:05 builder, "worker 2" = the ~11:10
  resumer (its numbering is used in all banked artifacts), THIS dispatch = monitor.
