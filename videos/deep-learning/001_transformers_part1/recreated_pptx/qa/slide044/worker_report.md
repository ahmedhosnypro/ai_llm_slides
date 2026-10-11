# Worker report — slide 044 (videos/deep-learning/001_transformers_part1)

**Deliverable:** `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_044_recreated.pptx`
(single-version law: ONE plain-named pptx, built by `recreated_pptx/build/slide_044.js`)
**Child of 44←43** (founder dependency graph): `require`s the certified frozen parent
component `recreated_pptx/build/components/slide_043.js` — `renderBase(pptx, slide,
{ numeral: 44, skip: ["title"] })` — and draws ONLY this slide's delta. No component
banked for 44 (it has no dependents; the subtree root component is slide_043.js).

## Result

- **Final verdict: PASS** (visual judge attempt 2), backed by a real comparison
  transcript with `--thinking high --max-tokens 65536`:
  `qa/slide044/judge_attempt_2.txt` ("No fix-trigger defects found. The inset is
  correctly imported/composited, the title block shift and all three occlusions
  reproduce the original exactly." — remaining findings MINOR, all in inherited
  regions = judge variance per the inheritance law).
- Dense-region (inset crop) comparison attempt 2 also a validated winner body:
  `qa/slide044/cmp_inset_attempt_2.txt` — "IMG1 (the attempt-2 render) is BETTER";
  all attempt-1 inset findings confirmed fixed; one cosmetic residual (h-slash
  slightly detached from the stack corner).
- Attempts used: 2 (attempt 1: full judge PASS but the mandatory inset CROP
  comparison FAILed with 1 BLOCKER + 2 MAJOR on the delta → fix round → attempt 2).
- DB: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=2`,
  `visual_transcript=videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide044/judge_attempt_2.txt`.
- Judge procedure executed BY THE WORKER (no Agent/Task spawn tool in this
  environment) via `scripts/16_vision_gate.sh` + `analyze_image.py`, per the
  documented §7 fallback. Gateway congestion early in the run: 6 hard-wall
  HangErrors on analysis calls before the window stabilized (probe → sleep 300 →
  re-probe once recovered it; per skill amendment W4 the judge comparisons landed
  first try on both attempts).

## Delta implemented (all geometry PIL-measured on unique_slides/slide_044.jpg,
960×540, 1px=1pt; scripts scratch/slide044/m1..m19 + s1..s3)

1. **Title replaced at the child-measured position** — the frame carries slide 43's
   title runs drawn 9px LEFT of the parent's box (word-cluster scan m13: every
   line-1 word shifted −9px with identical widths; IoU 0.753 @ dx=−9 vs 0.194 @ 0,
   line2 IoU 0.755 @ −9; m14). Per 17 §3 the child's frame is ground truth for
   inherited elements, so the parent title block is skipped (`opts.skip:["title"]`)
   and re-drawn with the parent's exact runs at x=491 (center 691) instead of 500.
   This is a measured frame fact, NOT a shift of the diagram blocks — those are
   untouched, and the occlusion is done purely by z-order (dispatch note).
2. **The Figure-2-right inset** (the pure addition), drawn LAST (on top):
   - Green-framed white panel, centerline x740..906 / y82..296, 3.5pt `1F8A1C`
     (measured border bands 738-741 / 904-908 / 80-83 / 294-298, core (28,139,21)).
   - Bottom-up course-style topology: `V,K,Q` labels (y281..288) → 3 thin up-arrows
     (x763/x809/x855, y240..278, heads at top) → three `Linear` boxes
     (x745/x791/x837, y220..239, fill E9EDE9, 1.75pt black border) EACH with TWO
     grey outlined duplicate boxes fanned behind it (tops y209/y214, right slivers
     poking right — measured strips + corner arcs s3) → three hollow grey
     connectors with solid dark tips (y201..219) → lavender stack: front box
     x746..875 y170..200 fill `BEB4D4` 1.75pt black border with the 2-line label
     "Scaled Dot-Product" / "Attention" (8pt, lineSpacing 10) + TWO grey fanned
     behind layers (tops y157/y163, right edges poking x≈881/x≈889) → THREE thin
     arrows rising into Concat (x805/x810/x815, heads at top, middle strong) + a
     thin diagonal arrow entering the stack from upper-left ((790,155)→(800,168))
     → `Concat` box x786..832 y128..149 fill `F5FEC7` → `Linear` box x790..831
     y96..116 → up output arrow (x810, y85..96).
   - `h` annotation right of the stack: bracket-like diagonal stroke down the
     stack's right edge + short horizontal tick + upright `h` (frame-measured).
3. **Occlusions reproduced by z-order** (inset drawn after renderBase; inherited
   blocks NOT shifted): panel covers the title line-2 right tail (visible
   '"Wide" Architec'), the bottom-left arc of the yellow 44 badge, the h=5 tag
   (747..777, 198..212), the h=5 card's top-right corner and the h=5 dashed X-box
   above y298 (below it the frame shows it again — measured identical, inherited).

## Frame-vs-spec reconciliations (frame wins; recorded)

- Spec labels list carries `Y₁` for the output vector: the frame shows NO delta vs
  slide 43 in the vecbox region (m9) → the certified `Y₂` rendering is inherited.
- Spec's "4 color groups of 3 cells" concat bar: the frame is identical to 43's
  certified 5-segment bar in that zone (diff = 2px noise) → inherited as certified.
- Spec's "4 overlapping purple boxes" for the stack: the frame shows the front box
  + 2 visible grey behind layers → drawn as measured (front + 2).
- Both reconciliations stay within the coordinator's "verified pure addition" for
  everything outside the title-position fact above.

## Pre-judge self-checks (banked)

- `qa/slide044/selfcheck_attempt_1.py` (v2, used for both attempts; attempt-2 run
  output in `qa/slide044/selfcheck_attempt_2_out.txt`) — PASS on render_1 and
  render_2: panel border bands, stack lavender fill + top border, Concat yellow,
  bottom boxes (fill/borders), V/K/Q ink, all six arrow shafts, title line1/line2
  alignment vs the original (center within 3.3 frame px), panel inner-ink bbox vs
  original (≤2.8px), house-frame containment (content ink x91.6..912), h=5-tag
  zone MAD 38.2 vs the original, badge yellow cut 79.7 vs original 80.0.
- **Chrome check** (`shared_patterns/house_chrome_check.py`): FAIL on the badge
  center — the DOCUMENTED occlusion effect (dispatch: run it "understanding the
  occlusion"). Verified against the frame: the original slide_044.jpg's badge
  yellow extent is cut at y80 by the inset exactly like the render (yellow
  y-extent render 54.2..79.7 vs orig 57..80 frame px; slide_043's unoccluded
  badge extends to y86). All other chrome checks (panel, red strokes, purple ring)
  PASS. Evidence: `scratch/slide044/s1_chrome_occl.py`.
- **Inheritance diff** (`scratch/slide044/s2_inherit_diff.py`): probe render of the
  bare base (`qa/slide044/probe_base_render.png`, numeral 44, no delta) vs the full
  render — ALL delta pixels inside the title + inset zones; 0 outside, on both
  attempts (70,876 / 70,992 px).
- **Dense-region crop comparison**: `qa/slide044/cmp_inset_render.png` /
  `cmp_inset_original.png` (identical crop frame x726..916 y70..308, 4x).

## Judge loop

- **Attempt 1** — full judge PASS (`judge_attempt_1.txt`, MINOR-only, all
  inherited-region variance); inset crop comparison **FAIL**
  (`cmp_inset_attempt_1.txt`): BLOCKER — grey duplicate-box stacks behind the three
  bottom Linear boxes omitted; MAJOR — stack fan-out reduced to one shadow layer;
  MAJOR — arrows into Concat reduced from three to one; MINOR — h-annotation
  styling, connector styling, bottom-Linear fill tint.
- Fixes (frame-verified, not just model-quoted): fanned duplicate boxes added
  behind each bottom Linear (measured tops y209/y214 + right slivers x785-795);
  stack rebuilt as front + 2 grey behind layers (tops y157/y163, right edges
  x881/x889); three arrows into Concat (x805/x810/x815, middle strong per the
  frame's highlighted centre shaft) + the upper-left diagonal arrow (790,155)→
  (800,168); h restyled as bracket-stroke + tick + upright h; bottom-Linear fill
  tinted E9EDE9; connector tips made solid dark triangles over hollow outlines;
  panel border centerline moved to x740/y82 so the stroke lands exactly on the
  measured bands; inset box borders bumped to 1.75pt (measured 2px strokes).
- **Attempt 2 — PASS** (both comparisons; details above).

## Evidence index

- qa/slide044/: render_1.png, render_2.png, probe_base_render.png,
  judge_prompt_1.txt, judge_prompt_2.txt, judge_ground_rules.txt,
  judge_attempt_1.txt (full-judge PASS, attempt 1), judge_attempt_2.txt (PASS),
  cmp_inset_attempt_1.txt (crop FAIL), cmp_inset_attempt_2.txt (crop: IMG1 better,
  all findings fixed), build_attempt_1.js, build_attempt_2.js,
  selfcheck_attempt_1.py, selfcheck_attempt_2_out.txt, cmp_inset_render.png,
  cmp_inset_original.png
- scratch/slide044/: measurement scripts m1..m19, s1..s3, mk_crops/mk_cmp_crops,
  probe_base.js, vision transcripts an_title44.txt, an_badge44 attempts,
  an_inset44.txt attempts (hung), reprobe_1.txt
