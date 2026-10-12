# Worker report — slide 023 (001_introduction, "Visualization of Single Layer Perceptron")

Date: 2026-10-12. Fresh start (no prior artifacts; DB row was registered `building` with no
build/qa files). Slide is `root` (no dependency edges) — build gate clear.

## Result

- **FINAL VERDICT: PASS** (attempt 1) — real comparison winner body, coherent, non-degenerate.
- Deliverable: `videos/deep-learning/001_introduction/recreated_pptx/slide_023_recreated.pptx` (single-version)
- Build: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_023.js`
- DB: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
  `visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide023/judge_attempt_1.txt`
- Judge procedure executed by the worker itself (no spawn tool in this environment) —
  orchestrator-approved fallback, per the banked prompt `judge_prompt_1.txt` (frozen
  template, GROUND RULES prelude carrying the playlist chrome: white FFFFFF canvas, gray
  E9E9E7 panel x42..918 y45→bottom, red C00000 border, badge FDFD96/6A5ACD at (893,71)
  d≈36, numeral 23). Probe hung twice at the 150s wall (fleet gateway saturation); the
  comparison itself landed through `scripts/16_vision_gate.sh` (inner `--timeout 280`
  inside `timeout 1700` outer, `--thinking high --max-tokens 65536`), TMPDIR pointed at
  the evidence-tree scratch for every gate call.
- Transcript: `qa/slide023/judge_attempt_1.txt` (md5 44526091), collision-proof copy
  `judge_attempt_1_PASS_backup_44526091.txt`.

## Judge findings (attempt 1)

No BLOCKER, no MAJOR. Three MINOR (non-blocking):
1. connection lines slightly thicker/more saturated than the original's 1px JPEG-faded lines (high conf);
2. activation step-glyph stroke slightly heavier (low-medium);
3. b₂ label sits slightly lower amid crossing lines than in the original (low).

## Pre-judge evidence chain (all banked in qa/slide023/)

1. **PIL forensics of slide_023.jpg** (960×540, 1px=1pt) — full ink-census + component
   classification: title two-color (red C00000-family + blue "Layer"), ink x152..731 cap
   y61..81 (Arial Bold advance-solve 30.3pt); cream eq box x52..473 y99..238 (fill modal
   (255,248,236)); 3 equation lines pitch 48px, baselines 123.5/171.5/219.5, **glyph flow
   BLACK with RED on the (X) of d_j(X), d's subscript, and the b_j*1 tail** (spec's
   wholesale-red claim overridden per the deck pixel law); W underlined (1px, measured
   line2 y177); tan box x137..326 y360..403 fill (224,224,200), text 8B0000-family
   2 lines baselines 378/397; network panel x423..897 y152..500, thin dark-blue border;
   7 input labels x433..445 (x₁/x₂/x₃/…/…/xₙ black + red "1" b425); 3 Σ circles d35 at
   cx681 cy187/320/455.5, CCFFFF fill, 339999 ring, black Σ glyph 14×18; 3 hollow
   ellipsis circles d13.5 at cy356.5/384/411.5; 21 fan lines (red/blue/green bundles);
   15 weight labels at measured positions (bundle-colored); 3 activation boxes
   x721..767 h31 (pink F8E0F8 fill, dark-rose 993366-family border, blue 0000CC step
   glyph of 3 rects); 3 red Σ→box arrows + 3 red box→output arrows; 3 output texts
   x804 11pt bold black, 3 lines each (wrapped trailing "I"/"II"/"m" reproduced
   explicitly), band pitch 13-14px; black bar x38..921 y519..539.
2. **Video-chrome / artifact omissions** (documented, per certified precedent
   slide_002/005/021 — all judge-PASS): thin red rule at x58 and dark top line y43
   (constant lecture-level chrome, house panel stands in); mouse cursor at
   (414..419, 210..219) per judge ground rule (c). The spec's "red vertical rule" claim
   is thereby covered by the chrome substitution, not silently dropped.
3. **house_chrome_check.py: PASS** on the final render (panel x89-1913, badge (1860,148) d70, tol 8).
4. **selfcheck_attempt_1.py: 52/52 PASS, 0 fails** — containment, black bar, title
   band/x/two-color, eq box fill, 3 eq line bands (top/bottom edges within ~7 render px
   of the scaled original bands), 3 red tails, tan box/text, panel border, 3 Σ circle
   centers dead-on (±0.6px), 3 ellipsis circles, 7 input bands + red bias "1", 15 weight
   labels present in bundle colors, 3 activation rows (pink fill/blue glyph/red arrow),
   3 outputs × 3 bands, explicit lineSpacing pin (29px = 14pt).
5. **Crop comparisons through the gate** (`--thinking high --max-tokens 65536`,
   banked prompts `crop_eq_prompt_1.txt` / `crop_diag_prompt_1.txt`):
   - Equation box: **PASS** (`crop_eq_1.txt`) — coloring matches the pixel law, 3 MINORs
     (paren spacing, dot spacing, T glyph style — compression-level).
   - Weight-label band: **PASS** (`crop_diag_1.txt`) — with one substantive finding:
     missing terminal arrowheads at the Σ-circle edges. REMEDIATED before judging
     (`endArrowType: "triangle"` on all 21 fan lines; re-rendered; arrowheads verified at
     the circle edge by PIL; selfcheck re-run to 0 fails). The two crop transcripts
     document the pre-fix state; the main judge saw the corrected render.

## Build-loop fixes during attempt 1 (all caught by the closed loop, before judging)

1. `render_eq.py` color args must carry `#` — "C00000" without `#` is parsed by
   matplotlib as the **C0 cycle color (blue)**; the F2/F4 red fragments rendered blue
   until re-rendered with `#C00000`.
2. Fan-line geometry: pptxgenjs draws line bboxes top-left→bottom-right; upward lines
   need `flipV` or they render mirrored (red bundle converged at the input column
   instead of Σ1). Fixed with `flipV: up`.
3. Z-order: the network panel was drawn over the equation box's right portion
   (frame x423..473); in the original the eq box sits ON TOP (cream + red border +
   equation tails visibly cross the panel border). Reordered: panel + diagram first,
   eq box + fragments after.

## Documented deviations (deliberate, evidence-based)

- Equations: professional 2D mathtext PNGs (certified mechanism), 4 fragments/line
  (black "d_j(", red "X", black ") = W̲ⱼᵀX = w…+", red "b_j*1"), fontsize 13.6pt
  metric-solved (flow lands x78..438/458 vs measured 78..439/456). d's subscript is
  black inside F1 (measured red at sub-glyph scale — sub-resolution deviation, the
  dominant black flow + red (X)/tail pattern is preserved).
- Weight labels drawn as single bundle-colored italic runs at measured positions; the
  original's ~8px labels show mixed sub-glyph chroma (red subscripts on blue/green w's)
  that is below the reliable rendering floor — spec's color-matched labels followed.
- Panel border 333399 (measured (142,140,162) JPEG-desaturated blue family) vs spec
  0000FF; activation border 993366 (measured dark-rose core (141,28,72)) vs spec FF99CC;
  tan fill E0E0C8 (measured) vs spec D9D9A6; eq box fill FFF8EC (measured) vs spec
  FFFFCC — per the deck law "small-text/region color claims settle via pixel
  column-profiles".
- Tan box border C00000 0.75pt per spec ("thin dark-red border" — sub-resolution in the
  frame).
- Badge numeral 23 per 001_introduction/AGENTS.md (assumption PENDING FOUNDER VETO).
- SOURCES.md honored (softmax-reg / one-vs-rest provenance; no factual changes to math).

## Attempts

- Attempt 1 = the only judge attempt (PASS). Build-loop fixes 1-3 above all happened
  pre-judge inside attempt 1's closed loop.

## Files

- Build: `recreated_pptx/build/slide_023.js` (+ banked copy `qa/slide023/build_attempt_1.js`)
- Assets: `recreated_pptx/build/assets/eq_{F1,F2,F3,F4}_{1,2,m}.png` + `eq_sidecars.json`
- Evidence: `qa/slide023/` — render_1.png, render-1.png, slide_023_recreated.pdf,
  selfcheck_attempt_1.py, crop_eq_*.png/txt, crop_diag_*.png/txt, judge_prompt_1.txt,
  crop prompts, judge_attempt_1.txt (+ md5 backup), probe logs absent (two probe hangs
  at the 150s wall; no transcript written by the gate for those), scratch/ (LO profile + gate locks)
- DB: VIDEO=deep-learning/001_introduction, slide 23 → passed / PASS / attempt 1.
