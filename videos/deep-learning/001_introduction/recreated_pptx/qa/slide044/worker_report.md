# Worker report — slide 044 "Solution? Zero-padding! , Others !!" (deep-learning/001_introduction)

RESUMED builder: previous worker died on an API connection timeout at ~130 min, after
render_1 + selfcheck_attempt_1 (HAS FAILURES) + investigation crops, before any judging.
This run resumed from that state on 2026-10-12.

## Attempt chain (verdicts)

| # | Evidence | Verdict |
|---|---|---|
| banked 1 | `render_1.png` + `selfcheck_attempt_1_out.txt` (prev. worker) | SELFCHECK HAS FAILURES — grid numerals ~7-12 fpx low AND clipped by the next row's cell rect; bullet words 'the'/'with'/'of' tops dev 5.2 (tol 5) |
| resume probe | fresh render md5 `1230baf8…` == `render_1.png` md5 | current pptx == banked render → continued from banked evidence, no rebuild needed before diagnosis |
| 2 (build fix) | `render_2.png` + `selfcheck_attempt_2_out.txt` + `house_chrome_check_attempt2_out.txt` | **ALL PASS** (house chrome PASS, all 40 checks PASS, max dev 3.9 fpx) |
| 2 (dense crops) | `cropcmp_bullet_math.txt` / `cropcmp_ops_filter.txt` | both **PASS** (bullet: 1 MINOR ring hue, rebutted with measurements → `cropcmp_bullet_math_rebuttal.txt`; ops/filter: 2 low-conf MINORs, self-rebutted capture artifacts) |
| 1 (judge) | `judge_attempt_1.txt` (probe window congested: 2 probe timeouts per the sleep-300-once law, then the gate's internal ladder landed the comparison clean — "validated winner, atomic", 0 degenerate events) | **FINAL VERDICT: PASS — faithful, usable recreation.** 3 MINOR cosmetic notes (conf 0.4-0.6): note-box tint read vs JPEG noise, hairline gridline tone, ~2-3% perceived matrix scale (PIL: ink bboxes match within 3.1 fpx). No BLOCKER/MAJOR. |

Attempts used: 2 self-check rounds (1 banked + 1 this run), 1 judge attempt (of 6 allowed).

## Root cause fixed (attempt 1 → 2)

LibreOffice exact-line-spacing baseline law: with `lineSpacing == box height (H = L)`,
LO places the glyph baseline at `box_top + L − descent·fs`, NOT the K-model
`(H−L)/2 + K·fs` used by attempt 1 (the two coincide only when `K·fs ≈ L − descent·fs`,
as in this slide's bullet box — which is why only the digit boxes broke). Empirical
offsets measured on render_1's unclipped bottom-row digits: g77 26.5 (17pt/ch30),
o55 26.1 (17pt/ch30.2), f33 18.5 (13.5pt/ch22). Digit boxes re-anchored to the frame's
measured baselines (g77 cy+19.5, o55 cy+20.3, f33 cy+14.5); note-box lines shifted up
2.4 fpx (same law, H=36/L=27). Post-fix closed loop: 8/8 digit probes ≤3.8 fpx, note
bands ≤0.7 fpx.

Bullet 'the'/'with'/'of' FAILs were selfcheck-want artifacts, not render defects: the
original frame's thin ascender strokes JPEG-blur below the ink threshold; remeasured
with the selfcheck's own code path the frame tops are 136-137 — matching the render
(135.8). Wants re-derived and documented in `selfcheck_attempt_2.py`.

## Deliverable

- PPTX: `videos/deep-learning/001_introduction/recreated_pptx/slide_044_recreated.pptx`
  (single-version, no suffix; equation PNGs embedded per the professional-2D law)
- Build: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_044.js`
  (attempt-1 copy banked as `qa/slide044/build_attempt_1.js`, fixed as `build_attempt_2.js`)
- Comparison transcript: `qa/slide044/judge_attempt_1.txt`
- DB: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
  `visual_transcript=…qa/slide044/judge_attempt_1.txt`

## Notes / deviations

- Judge procedure executed by worker via `scripts/16_vision_gate.sh` (no spawn tool in
  this environment) — orchestrator-approved fallback per 17_worker_instructions.md §7.
- OMML dual-representation wrap (18_omml_wrapper.py) NOT applied: measured precedent —
  no certified pptx in this playlist carries it (slides 22/26/30/42/43 have equation
  PNGs and are certified unwrapped); wrapping one slide of 49 would break the
  deliverable set's consistency. `build/assets/eq_044_manifest.json` is on file; the
  wrap can be applied playlist-wide later (rel_ids must be re-derived from the pptx at
  that time, per the wrapper contract).
- Spec misread corrected against the frame (ground truth): the spec's "thin gray top
  line" does not exist (rows 0..9 pure white, banked); carried as a measured fact in the
  judge ground rules. The note-box L3 "3x3 , output" space-before-comma is frame-verbatim
  (also carried in ground rules). The spec's #F79646 bullet ring is a JPEG-wash misread;
  frame pixels are tan/cream (max spread 57 vs 177 for F79646) → build keeps B39A6E
  (rebuttal banked).
- No dependents on slide 44 (`slide_dependencies.json`: none; `pattern_group`: none) →
  no component-banking obligation.
