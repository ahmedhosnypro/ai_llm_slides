# Worker report — slide 054 (002_transformers_part2, P4 pattern-group HEAD)

**Verdict: PASS** (visual judge, single-read, default route `images`, glm leg
DEFERRED/BLOCKED). Judge procedure executed by the worker; no spawn tool
available in this environment (orchestrator-approved fallback, per
`scripts/17_worker_instructions.md` §7).

## Deliverable

- `recreated_pptx/slide_054_recreated.pptx` (single-version law — plain name)
- Build: `recreated_pptx/build/slide_054.js` (banked per attempt as
  `qa/slide054/build_attempt_{1..7}.js`)
- DB row: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=7`,
  `visual_transcript=videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide054/judge_attempt_7.txt`

## Resume context

Dispatched fresh; found a prior worker's banked attempt 1 (build + render +
self-check, last artifact 05:09, >2h silent, DB row `gen_status=pending`, no
judge transcript — a mid-diagnosis crash, not a live peer). Resumed per the
resume rule; continued render/build numbering from attempt 2; never deleted
banked evidence.

## Attempt history (build/render numbering; judge dispatches marked)

| # | What changed | Evidence |
|---|---|---|
| 1 | (prior worker) initial build; closed-loop self-check: title −9.2px; rotated labels never checked | `build_attempt_1.js`, `selfcheck_attempt_1.py` |
| 2 | Resume: title em 19.5→19.6 + ink-left 81.5pt; **fixed nested-IN unit bug** on all 3 rotated labels (`IN(SM_CX - IN(70))` placed box top-left at intended center → strip displaced +w/2,+h/2); added rot_* strip checks. Chrome PASS, self-check PASS (3 known strict-mask CHECKs) | `render_2.png`, `rotlabel_centers_2.txt` |
| — | Crop C1 (attempt-2 render): FAIL — comma-vs-dot, Scaling label, arrow claims | `crop_eq_frac_2.txt` |
| 3 | Frame-measure sweep: K·q (middle dot, per C4+SOURCES+judge), re-rendered fraction as `\dfrac{K\cdot q}{\sqrt{d}}`, mask-cell khaki borders 8C8250 + U+2212, red cell text, label sizes (Scaling 21→23, Mask 14, Softmax 8.5), ς anchor, **arrow-language rewrite** (heads-only in box gaps, B/K2 removed) | `render_3.png`, `c1_followup_measure.txt` |
| — | Crop C1 (attempt-4 render): FAIL — claims: fraction 2.5× (CROP SCALE BUG: unequal zoom), F direction "reversed", Scaling top glyph "S" vs my "√d" | `crop_eq_frac_4.txt` |
| 4 | Equal-scale insight + redness forensics: F head points RIGHT (steep falloff tip-side), faint shafts real (A/F/G), Scaling reads TOP-TO-BOTTOM (rotate 90) | `f_head_forensics.txt`, `shaft_redness_scan.txt` |
| 5 | F flipped right + faint shafts, Scaling rotate 90, equal-scale crops. C1 FAIL: mask cell "−∞" too small; shaft/head misaligned ~10px | `crop_eq_frac_5.txt`, `c5_followup.txt` |
| 6 | **Second unit bug**: new seg() calls passed FRAME px where slide-pt expected → all new shafts ~10px high (this was the judge's "misaligned shaft"); unified seg/head to frame coords; mask cell text 12pt dark red; chip −∞ red. All closed-loop checks PASS (0 fails) | `render_6.png`, `selfcheck6_output.txt` |
| — | Crop C1: FAIL solely on Scaling strip anchor (~13px high; my band-scan had over-included fill-noise rows) | `crop_eq_frac_6.txt` |
| 7 | Scaling anchor re-measured by redness profile (text ink starts y=229): SC_CY sy(294), em 21 → strip 230.3..356.8 vs original 229..358; fraction center 213.0 | `render_7.png`, `scaling_strip_top.txt` |
| **JUDGE** | **PASS** — 3 MINOR findings, no MAJOR/BLOCKER | `judge_attempt_7.txt` |

## Judge findings (attempt 7, verbatim severity)

1. MINOR — V₁ label near-collision with the fourth ⊗ node (the original shows the same
   adjacency; measured node4 right edge 656 = V4 label left edge 656).
2. MINOR — recreation slightly larger/looser globally; containment not violated.
3. MINOR — typed-vs-handwritten stroke difference (ground rule d, inherent).

## Pre-judge self-check banked (all PASS on render_7 evidence chain)

- `house_chrome_check.py`: PASS (every render from 2 onward)
- `selfcheck_attempt_2.py` (v3, with rot_* checks) + `selfcheck4_output.txt` /
  `selfcheck6_output.txt`: title/chips/fraction/rot-strips/mask-cell text all
  within tolerance; arrowheads present; B/K2 gaps empty; containment 0 stray px
- Frame-truth verifier: `frame_truth_2.py`
- Dense-region crop comparisons (equal-scale, through the gate):
  `crop_eq_frac_2/4/5/6.txt` (iterative FAILs → fixes), C2/C3 superseded by the
  full-frame judge run under gateway load; the full-frame judge covered those
  regions (softmax/nodes, legend) with no findings beyond the MINORs above.

## Deviations from the letter of the template (documented)

- Probe step: the gateway window was already open from the immediately preceding
  gate call; the redundant probe was skipped to conserve fleet gate slots under
  load (16-slot fleet was saturated earlier; probes at 150s timed out twice,
  resolved after a 300s wait per the hang law).
- The crop comparisons used the frozen GROUND RULES verbatim plus an added
  crop-context paragraph (allowed: "same judge template").

## Provenance

- SOURCES: `slide_054_source/SOURCES.md` (banked by the web-verification worker;
  not re-run — analysis/validation were pre-validated PASS_WITH_FIXES).
- P4 pattern bank for slide 055: `qa/slide054/PATTERN_GROUP_P4.md` (conventions,
  traps, evidence index). Slide 54 is NOT a content-dependency parent in
  `slide_dependencies.json` (verified), so no `build/components/slide_054.js`
  export is owed; the pattern file + build script are the reuse surface for P4#2.
