# Wave-1 Recon — Banked Judge Verdict Audit

Run: `run-1793126532` · Recon date: 2026-11-01 · Read-only audit (no evidence modified).

Scope audited: `recreated_pptx/build/slide_*_judge*.txt`, `recreated_pptx/judge_slide_004_merged.txt`,
`pooled_missions/runs/run-1793126532/parked/verdicts_wave*/*.txt` (+ the two parked `misfiled_*.txt`
copies and the two extra slide-004 transcripts in `build/`).

Verdict law applied (REJUDGE_PROTOCOL Step 6): a verdict counts ONLY if the transcript body is
coherent (>=800 bytes, real reasoning) AND the file ends with an explicit `FINAL VERDICT: PASS|FAIL`.

## Audit table

| File (relative to V) | Bytes | Final verdict | Ends with explicit verdict? | Coherent body? | Notes |
|---|---|---|---|---|---|
| recreated_pptx/build/slide_008_judge.txt | 4925 | FAIL | yes (line 39 = last) | yes | hatched class-region shading omitted, cluster colors wrong, title clipped |
| recreated_pptx/build/slide_008_judge_prompt.txt | 4460 | n/a | n/a | n/a | PROMPT TEMPLATE, not a transcript ("PASS | FAIL — <one-sentence summary>"); excluded from verdict counts |
| recreated_pptx/build/slide_009_judge.txt | 1862 | PASS | yes (line 20 = last) | yes | order marker "Image 1 (Recreation) / Image 2 (Original)" = correct order |
| recreated_pptx/build/slide_016_judge.txt | 3341 | FAIL | yes | yes | v1 judge; heading-block placement/type-size deviation |
| recreated_pptx/build/slide_016_judge_v2.txt | 2297 | PASS | yes | yes | v2 re-judge supersedes v1 FAIL |
| recreated_pptx/build/slide_019_judge_pass.txt | 3354 | PASS | yes | yes | |
| recreated_pptx/build/slide_031_judge.txt | 1315 | FAIL | yes | yes | bare FAIL |
| recreated_pptx/build/judge_slide_004_attempt_1.txt | 1031 | PASS | yes (line 3 = last) | yes (small but real body) | |
| recreated_pptx/build/judge_slide_004_omml.txt | 2374 | PASS | yes | yes | OMML-wrapped build, image 1 wins |
| recreated_pptx/judge_slide_004_merged.txt | 1183 | PASS | NO — verdict is line 1, body follows | yes | merged transcript does not END with the verdict line; accepted as PASS content-wise but non-standard placement |
| parked/misfiled_009_copy_in_slide011_dir.txt | 17698 | PASS | yes (line 210 = last) | yes | misfiled slide-009 transcript parked in slide-011 dir |
| parked/misfiled_022_copy_from_026.txt | 4607 | FAIL | yes | yes | identical size to wave3 judge_re_026 FAIL — duplicate |
| parked/verdicts_wave2/judge_re_001_preFAIL.txt | 3932 | FAIL | yes | yes | instructors-block line-spacing MAJOR |
| parked/verdicts_wave3/judge_re_002_relay.wave2fail.025714.txt | 5136 | FAIL | yes | yes | line-spacing/vertical placement |
| parked/verdicts_wave3/judge_re_008_relay.txt | 39412 | FAIL | yes | yes | order marker recreation-first (correct); BLOCKER hatched shading |
| parked/verdicts_wave3/judge_re_012_relay.txt.stale_fail_2026-10-31.txt | 5242 | FAIL | yes | yes | stale pre-fix FAIL |
| parked/verdicts_wave3/judge_re_013_relay.stale_pre_fix.txt | 5647 | FAIL | yes | yes | stale pre-fix FAIL (arc terminations) |
| parked/verdicts_wave3/judge_re_016_relay.txt | 4531 | FAIL | yes | yes | wave-3 relay FAIL (title-block region) |
| parked/verdicts_wave3/judge_re_017_relay_FAIL_superseded_by_rejudge_2026-10-31.txt | 23315 | FAIL | yes | yes | FAIL, filename-marked superseded by later rejudge |
| parked/verdicts_wave3/judge_re_026_relay.wave3fail.2026-10-31.txt | 4607 | FAIL | yes | yes | cream value-box alignment |
| parked/verdicts_wave3/worker_judge_re_013.oldjudge.txt | 32165 | PASS | yes (line 328 = last) | yes | CONFLICTS with stale FAIL for 013 — older worker PASS |
| parked/verdicts_wave3/worker_judge_re_016.oldjudge.txt | 16943 | PASS | yes (line 150 = last) | yes | CONFLICTS with wave-3 relay FAIL for 016 — older worker PASS |
| parked/verdicts_wave3/worker_judge_re_026.oldjudge.txt | 226 | VOID | no | no (226 B error stub: only gate info header, no model output) | not a verdict |
| parked/verdicts_wave3/worker_judge_re_032.oldjudge.txt | 8183 | PASS | yes (line 115 = last) | yes | |

## Tally

- PASS (valid, ends with explicit verdict): 8 — slide_009_judge, slide_016_judge_v2, slide_019_judge_pass,
  judge_slide_004_attempt_1, judge_slide_004_omml, misfiled_009, worker_judge_re_013.oldjudge,
  worker_judge_re_016.oldjudge, worker_judge_re_032.oldjudge (9 if the merged slide-004 file is
  counted despite verdict-on-line-1)
- FAIL: 10 — slide_008_judge, slide_016_judge(v1), slide_031_judge, misfiled_022, judge_re_001,
  judge_re_002, judge_re_008, judge_re_012, judge_re_013, judge_re_016, judge_re_017, judge_re_026
  (12 files; misfiled_022 duplicates judge_re_026)
- VOID / not a verdict: 2 — worker_judge_re_026.oldjudge (226 B stub), slide_008_judge_prompt.txt (prompt)
- judge_slide_004_merged.txt: PASS content but verdict on line 1 instead of last line — flagged.

Machine-readable copy: `recon_wave1_verdict_audit.json` (same dir).
