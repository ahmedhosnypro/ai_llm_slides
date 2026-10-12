# Worker report — slide 021 (001_introduction, Deep Learning DSAI 308)

## Summary

- Slide: 21 — "[3] Quick revision of Neural Netwok (NN)" (section-divider slide)
- Attempts used: 1 of 6 (judge PASS on first attempt)
- Final verdict: **PASS** — backed by a real comparison transcript through the vision gate
- Deliverable (single version): `videos/deep-learning/001_introduction/recreated_pptx/slide_021_recreated.pptx`
- Build script: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_021.js`
- DB row: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
  `visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide021/judge_attempt_1.txt`

## Dispatch-facts correction (important)

The dispatch's "SLIDE FACTS" described slide 021 as "The Complete Deep Learning Model"
annotated backprop state (green dashed feedback + red block arrows). That is **slide 20's**
content (DB title row 20). The actual ground-truth frame `unique_slides/slide_021.jpg` was
PIL-verified before building: **zero green pixels**, two large red title bands
(y 197–248, y 323–375), black bottom bar — i.e. the section divider described by
`analysis/slide_021_final.json` (PASSED content gate), the DB row title, and
`slide_021_source/SOURCES.md`. The build follows the spec JSON + the actual frame; the
spec's `validation.fixes` were applied (verbatim_text law, "Netwok" typo preserved).

## Measured geometry (PIL, 960x540, 1px = 1pt)

- Title line 1 `[3] Quick revision of`: ink x 211..751 (center 481), cap-top 196, baseline 238
- Title line 2 `Neural Netwok (NN)` (typo verbatim): ink x 219..740 (center 479.5), cap-top 322,
  baseline 364, paren ink to 375
- Font: **Arial Bold 56.5pt** C00000 — metric-solved against the real Arial Bold TTF
  (T1 advance 541 px vs measured 540; T2 522 vs 521; cap ~40.8 vs ~42 incl. JPEG bleed).
  Spec range 54–60 pt, midpoint 57 — 56.5 is the metric-exact value inside the range.
- Black bar: x 38..921, y 518..539 in the original; drawn y 518..537.5 (chrome bottom stroke
  kept visible — same documented 2-frame-px deviation as certified slide_002/slide_005).
- Constant video chrome (omitted per certified precedent + judge ground rules):
  thin red inset strokes (top y 42–44, left x 57–60, NO right stroke, soft fade at x≈903)
  present on EVERY frame of this lecture (measured on slides 1/2/5/21/22/49); mouse-cursor
  artifact at (49–54, 236–245). The pre-declared playlist house chrome
  (`shared_patterns/house_chrome.js`, badge numeral 21) stands in for the frame element.

## Closed-loop verification (pre-judge, mandatory)

- `house_chrome_check.py` on the 150dpi render: **PASS** (panel x 89–1913, y 95→bottom;
  badge center (1860,148) d=70; tol 8).
- `selfcheck_attempt_1.py` (banked + output banked): **PASS** — title cap/baseline/tail
  within 1.0 frame-px of the original (l1 195.7/237.5/248.0 vs 196/238/249; l2
  322.4/363.7/375.2 vs 322/364/375); ink advances within 1.4 px; colors exact
  (canvas FFFFFF, panel E9E9E7, bar 000000, title C00000); containment OK;
  lineSpacing 68 (exact pt) on both title boxes; one pre-loop correction applied
  (initial render sat ~6 frame-px low; empirical per-line shift −6.2/−5.4 px; the
  pre-loop render + build are preserved in `scratch/slide021/`).
- Patterns library consulted: house-chrome (used), explicit-line-spacing (used);
  equations/delimiters/tables patterns N/A (none on this slide); dense-region crop
  comparison N/A (no dense/small regions — title is 56.5pt).

## Judge (attempt 1)

- Procedure executed by the worker via Bash (no Agent/Task spawn tool in this environment —
  orchestrator-approved fallback, per scripts/17_worker_instructions.md §7). Banked prompt:
  `qa/slide021/judge_prompt_1.txt`; frozen template with the playlist-chrome GROUND RULES
  prelude (white FFFFFF canvas, gray E9E9E7 panel x42..918/y45→bottom, red C00000 border,
  badge FDFD96/6A5ACD at (893,71) d≈36, numeral 21).
- Probe: `qa/slide021/probe_1.txt` (valid winner body, window opened).
- Comparison: `--thinking high --max-tokens 65536`, inner `--timeout 280` inside 1700s outer
  wall through `scripts/16_vision_gate.sh` (TMPDIR redirected to namespace scratch — /tmp
  quota blocked). Transcript: `qa/slide021/judge_attempt_1.txt` — real winner body, no
  degenerate events.
- Verdict (verbatim from winner body): "**FINAL VERDICT: PASS** for 'faithful, usable
  recreation'." Discrepancy list: **None found** (no BLOCKER/MAJOR/MINOR). Ground rules
  (a)/(c) settled the chrome and the omitted cursor; verbatim text matched including the
  preserved "Netwok" typo.

## Evidence files

- `qa/slide021/render_1.png` — the judged 150dpi render
- `qa/slide021/judge_prompt_1.txt`, `qa/slide021/probe_1.txt`, `qa/slide021/judge_attempt_1.txt`
- `qa/slide021/build_attempt_1.js` — build provenance for the judged attempt
- `qa/slide021/selfcheck_attempt_1.py` + `selfcheck_attempt_1.txt`
- `scratch/slide021/render_1_preloop2.png`, `scratch/slide021/build_preloop1.js` — pre-loop
  correction evidence

## Deviations / notes

1. Dispatch slide-facts text mismatch (see above) — built per spec JSON + actual frame.
2. Constant video chrome (inset strokes, cursor) omitted — certified-precedent-consistent,
   pre-declared to the judge, accepted.
3. No component banking obligation: slide 21 has no dependents in
   `slide_dependencies.json` (edges: 16←9, 17←16, 18←9, 19←9, 25←24, 37←36, 41←35).
4. OMML wrap / graph-gen passes: N/A (no equations, no advanced graphs).
5. Spec's recreation_brief steps 4–5 (bar + cursor) — bar drawn (part of the captured
   ground-truth frame, per spec + precedent); cursor omitted (ground rule c).
