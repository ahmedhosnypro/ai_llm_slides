# Verification Addendum — resume worker (cross-check), slide 040 — 2026-10-12 ~07:40 EEST

Distinctly-named addendum (worker_report.md belongs to the certified-chain builder;
a sibling verification worker's addendum lives in `verification_addendum_2026-10-12.md`).
Three workers were active on this slide after the provider outage; this worker detected
the live builder at 06:22 (build-file mtime advanced between reads) and stood down
READ-ONLY for all build/render/judge/DB artifacts. Builder's chain certified the slide:
**DB gen_status=passed, visual_check=PASS (judge_attempt_5.txt), 07:30:42.**

## Timeline (three dispatches, one certified chain)

- 04:18–05:09 — original build worker (renders 1–3, crops, judge_base_prompt) — killed by outage.
- 06:05–07:31 — the builder resumed: probes m26_remeasure/m27_stems_rects/m28_rects →
  build v4 (06:22) → render_4 (06:24) → build v5 (06:33) → render_5 (06:34) → checks 5 →
  crops2 (06:36–06:43: intro PASS, panelbot FAIL 5 MAJOR) → m33/m34/m35 eq3 regen sweep →
  build v6 (07:07) → render_6 → build v7 (07:14) → render_7 → m40–m42 → crops3 panelbot
  PASS (07:21) → full-slide judge attempt 4 FAIL (letterbox-artifact MAJOR) → judge
  attempt 5 re-dispatch (07:24) → **PASS (07:27)** → DB closed (07:30:42).
- 06:17–06:36 — THIS worker: independent PIL census (scratch m26_settle, m27_strokes,
  m28 inline, m30_disputes, m31 inline + out_*.txt).
- 06:20–06:53 — third (verification) worker: w1–w5 probes + worker_report.md addendum
  (later moved to verification_addendum_2026-10-12.md).

## THIS worker's independent census — outcomes

Confirmed against the frame (and convergent with the builder and the third worker):

1. **eq3 annotation is a closed thin lavender-blue rect** frame[164,399,287,446] — top
   rows 399–400, bottom row 446 (dark core 144,142,171), left col 164–165, right col 287;
   NOT a floating underline. The builder's earlier "underline-only" read was a threshold
   artifact (light strokes missed); m27 contiguity scan settled it.
2. **eq4 annotation is a closed thin pink rect** frame[164,451,371,475] (top rows 451–452,
   bottom row 475 core (196,156,163), left col 164–165, right col 371).
3. **y_i ellipse is tan-FILLED**: interior median (236,179,118) ≈ #ECB376 (builder used
   mode (240,184,128) #F0B880 — same family).
4. **γ and β are RED in the intro** (hue census x530..600: R/G/R column pattern; cores
   (169,82,93)/(170,80,92)); "and" between them green. Two crop-judge reads of "green γ/β"
   are low-res misreads — the final full-slide judge accepted the red rendering.
5. **L2 red run IS underlined** (row 157 continuous x664..828, core (152,91,99)) and
   **'learn parameters' IS green-underlined** (row 157 continuous x390..530, (97,165,94))
   — this worker's first "no underline" rebuttals were WRONG (scan band started at 158;
   green cutoff g<160 vs stroke g=162; red mask g<95 vs text g≈118). Corrected masks in
   m30 settled it; the builder had it right.
6. **L3 red IS underlined** (row 181 continuous x105..435) AND the intro box's own bottom
   border sits at rows 184–186 full-width (88..892) — two distinct strokes; both in the build.
7. Blue-word italics were NOT resolvable by pixel forensics at 9px x-height (controls fail:
   m30 correlation shows 'strictly'==+'Zero' at the noise floor; m31 left-edge fits garbage
   on multi-letter windows). Deferred to visual judging; the final judge accepted the build.

## Final state verification (this worker, read-only)

- Chain integrity: deliverable `recreated_pptx/slide_040_recreated.pptx` (07:14) ==
  `build/slide_040.js` (07:14) == judged `qa/slide040/render_7.png` (07:14). ✓
- Judge attempt 5 (`qa/slide040/judge_attempt_5.txt`): real comparison body, geometry
  settling via chrome landmarks (explicitly corrects attempt-4's letterbox-artifact MAJOR),
  no BLOCKER/MAJOR, 3 MINORs (inter-equation whitespace within tolerance; slightly heavier
  equation strokes — medium difference; capture-artifact space before "Minimizes" noted,
  not a defect). **FINAL VERDICT: PASS.**
- DB row 40: gen_status=passed, visual_check=PASS, visual_attempts=5,
  visual_transcript=judge_attempt_5.txt. ✓
- Slide 40 has NO dependents (same-video or cross-video) → no component-banking obligation.
- Observation: equations are 600-dpi mathtext PNGs; the OMML dual-representation post-pass
  (`scripts/18_omml_wrapper.py`) is NOT applied — consistent with certified siblings 039/041
  (0 oMath occurrences) — i.e. deferred batch-wide, not a slide-040 omission.

Evidence banked by this worker: `scratch/slide040/{m26_settle,m27_strokes,m30_disputes}.py`
+ `out_m26.txt, out_m27.txt, out_m28.txt, out_m30.txt, out_m31.txt`.
