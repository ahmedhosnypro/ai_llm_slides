# REJUDGE_SUMMARY_r35 — FINAL census of the 2026-10-27 rejudge wave, 2026-11-01T23:0xZ

Census worker for NS=`videos/machine-learning/03_ridger_regression_gradient_descent`,
RJ=`recreated_pptx/qa/rejudge_20261027`. Read-mostly: no slide rebuilt/recertified, no
pptx/DB/deck edits, no git, no vision legs launched. Slide 025 is owned by another worker
and is reported **OPEN** (its raw newest-clean transcripts exist but are not adjudicated here).

## 0. Method note (ordering evidence)

All transcript file mtimes were reset to 2026-11-01 19:16 by a bulk restore, so "newest"
was determined from in-content ordering evidence instead of mtime: per-slide `result.txt`
harvest/keyed lines carrying transcript timestamps (e.g. `R19_FULL=PASS … 2026-10-31T09:02:39Z`)
plus the append-only chronological `REJUDGE_REGISTER.md`; fallback naive-mtime scan where no
result.txt record existed (marked `naive-mtime`). Clean = transcript contains
`FINAL VERDICT` (bold tolerated), zero `429` lines, and not `.bak/.bank/.log/.out/_bak*/.clean*/.stale*/.preW02*/.W02bank*`.
Scan scripts/outputs: `scratch/tmp/r35_scan.py`, `r35_census.py`, `r35_census.json/txt`.

## 1. DB state (read-only query)

- 51 rows; `passed|PASS` = **50**, `building|''` = **1** — the only open row is
  **slide 25** (`Types of Loss function shapes`, worker S27_019_025, updated 2026-10-26T16:44:42).

## 2. Final census — newest clean FULL + CROP verdicts, slides 001–051

Census (slide 025 excluded as OPEN): **FULL PASS=29 / FAIL=21 / OPEN=1 / missing=0;
CROP PASS=41 / FAIL=9 / OPEN=1 / missing=0.**

| slide | newest clean FULL | newest clean CROP |
|---|---|---|
| 001 | FAIL `judge_full_r18.txt` | PASS `crop_dense_judge_r16.txt` |
| 002 | FAIL `judge_full_r19.txt` | PASS `crop_dense_judge_r16.txt` |
| 003 | FAIL `judge_full_r17.txt` | FAIL `crop_dense_judge.txt` |
| 004 | PASS `judge_full_r15.txt` | PASS `crop_dense_judge_r15.txt` |
| 005 | PASS `judge_full_r16.txt` | PASS `crop_dense_judge_r19.txt` |
| 006 | PASS `judge_full_r19.txt` | PASS `crop_dense_judge_r17.txt` |
| 007 | PASS `judge_full_r20.txt` | PASS `crop_dense_judge_retry.txt` |
| 008 | PASS `judge_full_r20.txt` | FAIL `crop_dense_judge_r19.txt` |
| 009 | PASS `judge_full_r20.txt` | PASS `crop_dense_judge_r21.txt` |
| 010 | PASS `judge_full_retry.txt` | FAIL `crop_dense_judge_retry.txt` |
| 011 | PASS `judge_full_r16.txt` | PASS `crop_dense_judge_r15.txt` |
| 012 | PASS `judge_full_fresh.txt` | PASS `crop_dense_judge.txt` |
| 013 | FAIL `judge_full_r18.txt` | PASS `crop_dense_judge_r16.txt` |
| 014 | FAIL `judge_full_fix2.txt` | PASS `crop_dense_judge_fix3.txt` |
| 015 | FAIL `judge_full_fresh3.txt` | FAIL `crop_dense_judge_r20.txt` |
| 016 | FAIL `judge_full_r21.txt` | PASS `crop_dense_judge_r17.txt` |
| 017 | PASS `judge_full_r19.txt` | FAIL `crop_dense_judge_r17.txt` |
| 018 | PASS `judge_full_r19.txt` | FAIL `crop_dense_judge_r20.txt` |
| 019 | FAIL `judge_full_wfix.txt` | FAIL `crop_dense_judge_wfix.txt` |
| 020 | PASS `judge_full_r21.txt` | PASS `crop_dense_judge_r21.txt` |
| 021 | PASS `judge_full_r18.txt` | PASS `crop_dense_judge_r16.txt` |
| 022 | FAIL `judge_full_r20.txt` | FAIL `crop_dense_judge_r17.txt` |
| 023 | PASS `judge_full_r20.txt` | PASS `crop_dense_judge_r16.txt` |
| 024 | PASS `judge_full_r19_r22.txt` | PASS `crop_dense_judge_r16.txt` |
| 025 | **OPEN** (owned by another worker; raw newest clean: FULL `judge_full_k17z3.txt` FAIL, CROP `crop_dense_judge_k17q.txt` FAIL per sweep_r35; earlier k17n PASS legs superseded) | **OPEN** |
| 026 | FAIL `judge_full_r16.txt` | PASS `crop_dense_judge_r21.txt` |
| 027 | FAIL `judge_full_r20.txt` | PASS `crop_dense_judge_r21.txt` |
| 028 | PASS `judge_full_r16.txt` | PASS `crop_dense_judge_r20.txt` |
| 029 | PASS `judge_full_r17.txt` | PASS `crop_dense_judge_r17.txt` |
| 030 | PASS `judge_full_r17.txt` | PASS `crop_dense_judge_w03.txt` |
| 031 | PASS `judge_full_r19.txt` | FAIL `crop_dense_judge_r17.txt` |
| 032 | PASS `judge_full_r17.txt` | PASS `crop_dense_judge_w03.txt` |
| 033 | FAIL `judge_full_w03_snap.txt` | PASS `crop_dense_judge_w03_snap.txt` |
| 034 | PASS `judge_full_r19.txt` | PASS `crop_dense_judge_w03.txt` |
| 035 | PASS `judge_full_r20.txt` | PASS `crop_dense_judge_r20.txt` |
| 036 | PASS `judge_full_r19.txt` | PASS `crop_dense_judge_r20.txt` |
| 037 | FAIL `judge_full_r20.txt` | PASS `crop_dense_judge_fresh3.txt` |
| 038 | PASS `judge_full_r20.txt` | PASS `crop_dense_judge_r21.txt` |
| 039 | FAIL `judge_full_retry.txt` | PASS `crop_dense_judge_r20.txt` |
| 040 | PASS `judge_full_r19.txt` | PASS `crop_dense_judge_fresh3.txt` |
| 041 | PASS `judge_full_r20.txt` | PASS `crop_dense_judge_r20.txt` |
| 042 | PASS `judge_full_w10.txt` | PASS `crop_dense_judge.txt` |
| 043 | FAIL `judge_full_r20.txt` | PASS `crop_dense_judge_r16.txt` |
| 044 | FAIL `judge_full_r21.txt` | PASS `crop_dense_judge_r20.txt` |
| 045 | PASS `judge_full_r19.txt` | PASS `crop_dense_judge_r19.txt` |
| 046 | FAIL `judge_full_fresh2.txt` | PASS `crop_dense_judge_r22.txt` |
| 047 | PASS `judge_full_r19.txt` | PASS `crop_dense_judge_r19.txt` |
| 048 | FAIL `judge_full_r20.txt` | PASS `crop_dense_judge_r20.txt` |
| 049 | FAIL `judge_full_r16.txt` | PASS `crop_dense_judge_r22.txt` |
| 050 | FAIL `judge_full_r20.txt` | PASS `crop_dense_judge_r16.txt` |
| 051 | FAIL `judge_full_w2.txt` | PASS `crop_dense_judge_r19.txt` |

## 3. FAIL-leg adjudication status (PIL against banked transcripts)

Render PNGs were cleaned up after the wave, so no fresh `rejudge_adjudicate.py` pixel runs
were possible; adjudication is taken from the banked `adjudicate_*`/`adjudication.*` files,
per-slide `result.txt` dispositions, and the register rulings:

- **All 30 newest-FAIL legs (21 FULL + 9 CROP) carry banked PIL adjudications; 29 are
  DISMISSED / REFUTED (diffuse pixel census or targeted refutation) — i.e. clean per the
  wave rule "all-refuted = clean".**
- **One leg STANDS as a real defect: slide 013 FULL** (`judge_full_r18.txt` FAIL,
  `R18_FULL_DISPOSITION=FAIL STANDS` — missing row-label column in the TEST tables,
  PIL-confirmed localized; fix dispatch owned by the orchestrator).
- Fresh vision legs needed: **none** — every in-scope slide has a clean (zero-429) transcript
  for both legs, so the "fresh leg only if no clean transcript exists" condition never fired.
  Gateway occupancy at scan: `pgrep -c -f analyze_image.py` = 4 (< 8).

## 4. Open items / follow-ups

- **Slide 025 — OPEN** (owned by another worker; DB row `building`/blank; newest completed
  k17z3 legs FULL+CROP both FAIL per sweep_r35; no clean PASS exists).
- **Slide 013 — newest FULL FAIL stands (PIL-confirmed missing label column); rebuild/fix
  is orchestrator-owned, not done here.**
- 29 FAIL legs are adjudicated-dismissed (clean), listed in §2; census-only, not re-open orders.

## Files changed this spawn

- Created `REJUDGE_SUMMARY_r35.md` and `census_worker_report.md` in `$RJ`; appended one dated
  pointer line to `REJUDGE_REGISTER.md` (append-only).
- Scratch only: `scratch/tmp/r35_scan*.py/json`, `r35_census.py/json/txt`, `r35_final_scan.txt`.
- No git; no vision legs launched; no DB/pptx/deck/build files modified; no evidence deleted.
