# Worker report — slide 043 (videos/deep-learning/001_transformers_part1)

**Deliverable:** `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_043_recreated.pptx`
(single-version law: ONE plain-named pptx, built by `recreated_pptx/build/slide_043.js`)
**Component (banked for children 44/45):** `recreated_pptx/build/components/slide_043.js`
— `renderBase(pptx, slide, opts)` with `opts.skip`/`opts.only`, chrome via
`components/house_chrome.js` (delegates to `videos/deep-learning/shared_patterns/house_chrome.js`),
numeral 43.

## Result

- **Final verdict: PASS** (visual judge attempt 2), backed by a real comparison
  transcript with `--thinking high --max-tokens 65536`:
  `qa/slide043/judge_attempt_2.txt`.
- Attempts used: 2 (attempt 1 FAIL → fixes → attempt 2 PASS).
- DB: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=2`,
  `visual_transcript=videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide043/judge_attempt_2.txt`.
- Children 44 and 45 are now **unblocked** (confirmed via `15_progress.py deps`).
- Judge procedure executed BY THE WORKER (no Agent/Task spawn tool in this
  environment) via `scripts/16_vision_gate.sh` + `analyze_image.py`, per the
  documented §7 fallback.

## Provenance / analysis inputs

- Spec: `analysis/slide_043_final.json` (gate-passed PASS_WITH_FIXES, score 9;
  `_meta` notes the raw was recovered via the fallback model — per dispatch, the
  spec was trusted for CONTENT but every geometry/color claim was re-verified
  against the frame by PIL and/or crop vision).
- 13 banked vision-crop transcripts under `scratch/slide043/` (an_title,
  probe_pipeline, an_micro (LT box + vecbox + 1×d), an_staircase, an_frontmid,
  an_right, an_bottom, an_legend, an_tanbox, an_leftcol, an_kqzone + 2 failed
  probe logs). PIL measurement scripts `scratch/slide043/m1..m20`.
- SOURCES.md consulted (Wide = concat → dH×d linear ≡ paper MultiHead; course
  h=5 vs paper h=8 kept as course illustration; Bloem notation source).

## Geometry highlights (frame px, 1px = 1pt)

- Cards h1..h5: (56,274)/(104,252)/(152,232)/(189,208)/(234,192), 548 wide,
  fills EF8C96 / C5C1F4 / F8FF9A / D4FFE5 / F7E2CD (measured, overrides the
  spec's approximate palette).
- Title: line1 ink x 527..867 y 54..76, line2 x 606..797 y 78..99, both
  centered at cx≈700; "Wide" NAVY bold (not black — measured #140E3C) on yellow
  highlight x 616..662; X₂ red with true subscript.
- Pipeline (flows UPWARD): vecbox (400,50,70×22, blue border, 5 cells, green Y₂)
  + red "1×d" → arrow → LT box (314,90,240×24.5, fill F6FAD5, ORANGE border,
  "Linear Transformation    [ T ]" + sub d(red) H(blue) ×(red) d(red)) → arrow →
  concat stadium bar (185,128,499×23.5) with label zone + 5 measured segments
  BB4F07 / 777C5C / F2F208 / AAFF71 / F3DEBC.
- Head-1 internals: dashed input container (92,318) with X₁..X₄ cells → 4 green
  W_k^(0..3) boxes → striped K bars + red K₁..K₄ → tan Dot Product box
  (195,301,58×140) with 4 target circles + red fan from bottom-center → K,q and
  a professional-2D K,q/√d fraction (mathtext 600dpi PNG, exact size) → pale-pink
  "Scaling by √d" pill + lavender "Soft max" pill (rotated mathtext PNGs) → Σ
  box → 4 dashed row lines → ⊗ nodes → V₁..V₄ + strips → W_v^(0..3) → dashed
  X-cells box. Query row: q₁ red bar + W_q^(0) box + dashed token container with
  4 word strips (X₂ magenta) + red arrow into X₂.
- Right: climbing dashed Y-chips (lavender/orange/dark-gray/yellow/green gap
  chip), per-head dashed X-panels + 12 W-chips in 4 staggered columns (heads
  2..5, red/green/blue outlines, red labels), dark-red swoosh (600dpi bezier PNG
  from (592,464) to head (738,336), ~8.5pt) + rotated blue italic "H^th Heads".
- Legend (736,468,170×64): 8-cell vector icon + 1×d, W square, red =, d×d grid,
  blue bold "d: Embedding Length" (blue confirmed by 2 crop reads + pixel
  sampling #5050C8; overrides spec's "red").

## Judge loop

- **Attempt 1 — FAIL** (`judge_attempt_1.txt`): MAJOR title X₂/badge collision +
  missing subscript; MAJOR W-chip label mismatch (orig reads W_q⁽⁰⁾); MAJOR
  missing dashed climbing Y-chips between stack and bar; MINOR stadium bar
  shape, unlabeled input cells, Y-segment sub order.
- Fixes applied (all in `components/slide_043.js`): title line1 23pt→20pt
  (render ink now 525..869, clear of badge, subscript visible); W labels
  W_q^(0)/W_k^(0..3)/W_v^(0..3) with larger sub/sup runs; dashed-green Y-chips
  with red Y labels along the measured diagonal + the green gap chip (486,177);
  concat bar made a stadium; X labels added to input cells; sub/superscript
  legibility bumped.
- **Attempt 2 — PASS** (`judge_attempt_2.txt`): all majors resolved; remaining
  findings MINOR only (bar Y-label order legibility 0.7; climbing-chip
  arrangement approximation 0.8; input cells without sub-cell strips 0.8; 1×d
  beside q₁ placement 0.6). No overflow/clipping/collisions; equations centered.

## Pre-judge self-checks (banked)

- `qa/slide043/selfcheck_attempt_1.py` / `selfcheck_attempt_2.py` — PASS on both
  renders (containment, equation ink presence, LT/title/wrap, highlight,
  card/segment/swoosh/legend color samples).
- `house_chrome_check.py` — PASS on render_1 and render_2 (badge center
  (1860,148) d=70 at 150dpi, panel extent within tol 8).
- Containment note: the content-ink bbox scan (x 41.3..919.2, y 44.6..539.5)
  includes the chrome's own border strokes; chrome itself is verified by
  house_chrome_check.py. Content drawn by this slide sits clear of the chrome.
- Dense-region crop comparisons: the K,q/√d fraction, rotated pill labels and
  micro-labels were measured from 4x crops of the ORIGINAL during the build
  phase (13 transcripts); the attempt-2 full judge additionally confirmed
  equations "vertically centered", labels "legible at 150dpi", no empty
  equation regions.

## Notes for children (44, 45)

- Import `recreated_pptx/build/components/slide_043.js`; call
  `renderBase(pptx, slide, { numeral: 44|45 })` or cherry-pick via
  `opts.skip`/`opts.only`. Block names: title, vecbox, pipearrows, ltbox,
  concatbar, headarrows, cards, headannots, ff_left, ff_mid, ff_right,
  queryrow, bottomcurve, headpanels, wochips, swoosh, hlabel, legend.
- Child 44 (Figure-2-right inset ON TOP, occluding the title tail and the h=5
  badge in the ORIGINAL): draw the inset after renderBase; the occlusion of the
  title's right end and the badge area reproduces the original.
- Child 45 (Narrow variant): drop the pipeline blocks
  (`skip:['ltbox','concatbar','pipearrows','vecbox']` as measured against its
  own frame) and add the input-sequence/chunk/To-Head legend elements.
- OMML wrap NOT applied: this deck's directives scope equations to the
  mathtext-PNG mechanism (dispatch + playlist AGENTS.md never mandate the
  wrapper), and children rebuild from the component — a wrap of this pptx would
  not propagate. Revisit if the founder requests editable equations deck-wide.

## Evidence index

- qa/slide043/: render_1.png, render_2.png, judge_prompt_1.txt, judge_prompt_2.txt,
  judge_attempt_1.txt (FAIL), judge_attempt_2.txt (PASS), build_attempt_1.js,
  build_attempt_1_component.js, build_attempt_2.js, build_attempt_2_component.js,
  selfcheck_attempt_1.py, selfcheck_attempt_2.py
- scratch/slide043/: measurement scripts m1..m20, crops crop_*.png, 13 transcripts
  (an_*.txt, probe_pipeline.txt, probe_1 attempt logs), regions.json
