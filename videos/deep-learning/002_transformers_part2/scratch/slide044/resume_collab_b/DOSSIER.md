# Collab-resume worker dossier (dispatched ~16:22, standby from ~16:47)

Second resumed worker on slide 044. On arrival the slide showed: certified PASS chain
(builder-A, judge_attempt_2.txt on build c93f1d26 / render_1) + an UNJUDGED takeover
(builder-7, build 25e85f33 at 14:44, renders 2/3, died ~15:51 pre-judge). This worker
independently established the timeline, then observed live peer builder-9 restoring the
certified chain (DB last_error 16:47) and went STANDBY per the collision protocol
(builder-8 precedent). No shared file edited by this worker after 16:40 (the 16:39
deliverable rebuild + 16:40 render happened BEFORE this worker read builder-9's note;
they turned out to be an independent reproduction of the certified chain).

## Independent corroborations (this dossier)

1. takeover_diff.txt — full diff c93f1d26 (certified) vs 25e85f33 (takeover): title
   em 35.75->30.5 (older 160..849 advance was rect-border contamination), LEFT cube 4th
   dark-green band, GN/INST front-band bright-orange splits, RT dark magenta band
   restored, pitch 31.x->30, washed D2B9B4 borders, oval x734..886, FV x663.
2. pptx_inspect/ — XML proof: a build run at 16:39 against the RESTORED script produced
   sz="3575" title (certified content) — confirms build/slide_044.js is c93f1d26 and
   reproducible; no library/environment drift (pptxgenjs 4.0.1 unchanged since Oct 9,
   LibreOffice 26.8.1.1 both eras).
3. render4/slide-1.png md5 cc3c38debba10c0e9f162255476c6b76 — this worker's independent
   render of the restored build; BYTE-IDENTICAL to builder-9's
   qa/slide044/render_attempt2_restored.png (two independent builds -> same raster).
4. selfcheck_attempt_3_fresh.py — selfcheck variant (was prepared pre-standby; render4
   == restored render, so qa/slide044/selfcheck outputs for render_2 lineage do NOT
   apply to the restored render; builder-9's selfcheck_restore_out.txt (41 checks,
   13 flagged, all known orig-wash/cursor classes + the DIFF94 title width that judge-2
   accepted) is the valid selfcheck for the certified chain).

## Why standby (not takeover)

builder-9 demonstrably live (writes 16:32->16:55), plan sound and nearly done, judge-2
PASS binds to the restored build exactly. Racing it would duplicate vision-gate calls
and thrash the DB. Take-over trigger: no builder-9 write for >10 min with
gen_status still 'building'.

## FINAL RESOLUTION (17:05)

builder-9 finalized: DB gen_status=passed @16:59:16, worker_report.md resume appendix
@16:56. Its appendix referenced qa/slide044/restore_verification.txt but did not
persist the file; THIS worker banked it (clearly labeled) from its own independent
verification — md5 triple-identity render_1 == render4 == render_attempt2_restored
(cc3c38de), build md5 c93f1d26 both copies, XML sz=3575 proof, chrome PASS. Slide 44
CLOSED: certified, consistent, evidence intact.
