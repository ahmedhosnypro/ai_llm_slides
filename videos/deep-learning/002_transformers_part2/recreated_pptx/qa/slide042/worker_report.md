# Worker report — slide 042 "Batch Data (Feature Vectors)" — CERTIFIED

Video: `deep-learning/002_transformers_part2` · P3 pattern-group HEAD ([42,43,44]) ·
Fourth dispatch (resumed after a provider-storm death mid-judge).

**FINAL: PASS** (attempt 4, real vision comparison, `judge_attempt_4.txt`) ·
DB: `gen_status='passed'`, `visual_check='PASS'`, `visual_attempts=4`,
`visual_transcript=videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide042/judge_attempt_4.txt`.
Deliverable: `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_042_recreated.pptx`
(single plain-named version; no equations -> no OMML wrap; no advanced graph -> no graphgen).
**Slide 43 (P3#2) is now UNBLOCKED** (`deps`: `pattern P3#1 (slide 42) not certified` cleared).

## Resume state (verified before any action)

- DB row: `gen_status='judging'`, `visual_attempts=2` (both judge attempts SPENT — the
  attempt-2 judge died mid-flight in a provider storm; NO `judge_attempt_2.txt` exists,
  i.e. no vision evidence for attempt 2). Live `build/slide_042.js` byte-identical to
  `qa/slide042/build_attempt_2.js`.
- Re-rendered the live build: pixel-identical to banked `render_2.png`
  (0/2,251,125 px differ) — composition state confirmed; banked as `render_3.png`.
- `SOURCES.md` provenance banked (Wu & He 1803.08494 Fig.2 axis mapping; course's own
  cube-style redraw; frame = ground truth).

## Attempt history (this run)

| Attempt | What | Verdict | Evidence |
|---|---|---|---|
| 3 (pre-judge) | Fresh self-checks on the attempt-2 composition: `house_chrome_check` PASS; closed-loop PIL vs original found real deltas in the h-arrow (orig tips 655..774 vs drawn 651..778) and h-label baselines (~2–3.5 frame px low); everything else flagged was a mask artifact | build fix | `selfcheck_attempt_3*.py/_out.txt`, `house_chrome_check_3.txt`, probes in `scratch/slide042/probe42*_attempt3.py` |
| 3 (crop) | Zoomed crop vision comparison of the whole right diagram (self-check dense-region mechanism): **CROP VERDICT: MATCH** — layer order/staircase/arrows/labels/white arrow all match; 1 MINOR (white-arrow orientation unresolvable through video blur) | corroboration | `crop_diag_attempt3_{orig,render}.png`, `selfcheck_crop_diag_3.txt` |
| 3 (judge) | W4 direct comparison (probes hung twice at the 150 s wall — slept 300 s, re-probed once, still hung while the fleet landed comparisons, so dispatched the comparison per the banked W4 law) | **FAIL** | `judge_attempt_3.txt` |
| 4 (build) | Fixes: h-arrow tips 651/778 -> 655/774 (fresh closed-loop re-measure); h-label baselines 483.5/496 -> 481.8/492.2 (orig ink bottoms 481/495); blue frame 000080 -> 0000CC (attempt-3 judge's "darker navy" was LEGIT: orig border core (65,56,173), and the spec says #0000CC) | rebuild | `build_attempt_4.js`, `render_4.png`, `selfcheck_attempt_4*.txt`, `house_chrome_check_4.txt` (PASS) |
| 4 (judge) | W4 comparison | **PASS** — no BLOCKER/MAJOR; 2 MINOR cosmetics (middle-grid white gaps slightly more pronounced; dark top faces slightly darker; "styling only", counts/extents verified within ~1.5 frame px) | `judge_attempt_4.txt` |

### Attempt-3 judge findings — adjudication record (kept for the pattern members)

- MAJOR #1 "(4 Filters)" touches the blue frame's bottom border (conf 0.6): measured
  FALSE — closed-loop gap 29.6 render px in the render vs 28 frame px in the original
  (identical margins; `judge_attempt_4.txt` re-verified with these numbers). The
  suggested remedy (shift the Channels group up ~15 px) would have collided the
  "(4 Filters)" parens with the h-arrow shaft (485.8..487.2) — not applied.
- MINOR #2 "frame stroke heavier/darker navy": thickness was actually thinner in the
  render (4 render px = 1.92 pt vs orig ~3 frame px blurred), but the COLOR was
  legitimately darker -> fixed to #0000CC.
- MINOR #3 "cubes ~5–8% larger": contradicted by PIL (stack/grid ink extents within
  ~1.5 frame px of the original) — not applied.
- Attempt-3 FAIL recorded honestly in the DB before the attempt-4 rebuild
  (`visual_check=FAIL`, `visual_attempts=3`, transcript banked).

### Mask-artifact lessons for the P3 members (PIL pre-checks on video frames)

- Thin red borders on video frames are chroma-destroyed (4:2:0): a #C00000 1 px border
  reads (204,175,179)/(229,204,210). Use a LOOSE red mask (r>150, r-g>30) for borders,
  and luminance-dip scans for geometry; strict masks only for text/diagram cores.
- A "red-text" mask `(r-g>60)&(r-b>60)&(g<b+35)` separates red text from the orange
  cube faces (FF7F00 has g>>b) — needed anywhere labels sit near the orange layer.
- Magenta needs `(r>150)&(b>150)&(g<80)`: loose magenta masks catch pink AA fringes of
  red arrows/text in BOTH images and manufacture fake extents.
- The right block's staircase slivers are occlusion-sensitive at 1–2 px: bbox deltas
  there are NOT defects by themselves — corroborate with a crop vision comparison
  (this run: CROP MATCH) before touching geometry.
- Converted-bbox prints must add the transform offsets (x+18.63): one d_frame column
  in `selfcheck_attempt_3.py` v1 was offset-shifted (the d_render gate was correct).

## Judge dispatch note

No Agent/Task spawn tool in this environment — the judge procedure was executed by the
worker via Bash, byte-for-byte per the banked prompts (orchestrator-approved fallback).
Frozen `-p` GROUND RULES payload kept verbatim across attempts 2/3/4 (only K/NNN/render
substitutions; verified by round-trip diff). Probes: 2 hangs (150 s wall each, 300 s
sleep + single re-probe) -> comparison dispatched directly per the banked W4 law; no
`probe_3.txt`/`probe_4.txt` exist. Comparison transcripts are real winner bodies with
coherent FINAL VERDICT lines (no degenerate garbage; no GarbageError retries needed).
Certificate: single-read, default route (images), glm leg DEFERRED/BLOCKED.

## P3 pattern conventions for slides 43 & 44 (Batch Normalization family)

P3 = [42,43,44] share the Wu & He "Group Normalization Fig. 2" tensor-cube family: the
SAME cube-ladder engine, label-box style, and dimension-arrow style, recomposed per
frame. 43/44 must NOT clone this composition — reuse the PATTERNS below at THEIR own
PIL-measured geometry (their frames are ground truth). Working code: `build/slide_042.js`
(certified component-quality reference; 43/44 build their own scripts).

1. **Frame->slide mapping.** 002 frames are ~0.958-scale zoomed-out captures. Fit YOUR
   frame's four chrome landmarks (left/right/top/bottom-border) exactly as done here
   (slide 042: left 59, right 902, top 43, bottom 516 <-> 42/919/45/540), then
   `SX(fx)=(fx-x0)/kx`, `SY(fy)=fy/ky` in SLIDE PT (pptxgenjs), never px. Verify the
   badge cross-check (yellow bbox center) lands within ~3 px. Slide 042's constants are
   NOT 43/44's — refit from each frame.
2. **Cube-grid engine** (`cubeGrid(ox,oy,cols,rows,pitchX,pitchY,Wf,Hf,dx,dy,cFront,cTop)`):
   - THREE paint passes per grid: ALL top faces, THEN all right faces, THEN all fronts.
     (The bright seams between columns are right-face slivers surviving the next
     column's front; row n+1's top face shows only as a ~4.7 pt dark sliver.)
   - One cube = front rect + top parallelogram (offset +dx,-dy) + right parallelogram;
     right face SAME color as front (measured: bright-quartile equality).
   - Parallelograms via `custGeom` with ABSOLUTE-inch points; pptxgenjs DROPS the close
     point's x/y — repeat the first vertex as an extra final point (probe-verified).
   - Fronts carry a 0.25 pt line in their own color (crisper edges in LO).
   - 042 values (refit per frame!): middle grid origin (380,269), pitch (30.7,31.5),
     front 27x27, oblique (13.5,14.7); left stack 1x5 origin (170,277), pitch-y 31.4,
     front 30x27, oblique (11.5,14.7).
3. **Multi-layer batch block** (042: five 4x5 layers, back-to-front paint
   bluegray -> yellow -> orange -> green -> magenta):
   - Layer offsets NON-UNIFORM in x is possible — fit each layer's cum offset from the
     RIGHT-staircase transitions scanned at 3 independent rows (042: cum {12,28,49,64},
     uniform layer-dy 18 frame px); fronts+right faces of rear layers peek as
     staircase slivers; top faces DARK (~0.36x luminance of front) painted per layer
     BEFORE its fronts; front layer overlaps everything behind it.
   - 042 layer colors front->back: CC00CC / 7CFC00 / FF7F00 / EDFF1A / 759FC9 with
     dark tops 4E0050 / 2B5E00 / 5C2E00 / 525C00 / 4C5875. For 43/44 (BN family) the
     layering/axis semantics change (Groups) — re-derive from each frame + SOURCES.md.
4. **Dimension arrows** (thin shaft + LARGE separate heads — LO line-arrowheads scale
   with line width and render too heavy, so NEVER use `endArrowType` for these):
   `shaft(x0,y0,x1,y1,w)` = thin rotated rect (w=1.4 pt) + `head(xTip,yTip,deg)` =
   8.4 pt `isocelesTriangle` rotated to aim the apex (deg: 0=up, clockwise); shaft
   trimmed by HEAD*0.7 at each end. 042: vertical x642.5 y326.5..466; horizontal
   y486.5 tips 655..774; diagonal (792,474.5)..(861.5,403) at ~44 deg.
5. **Rotated labels**: single `addText` with `rotate` + `align:center`,
   `valign:middle`, box centered on the measured ink center; v-label 270 deg (reads
   bottom-to-top), diagonal labels 314 deg (=-46) in ONE box of two `breakLine` runs
   with explicit `lineSpacing` (042: 24.5 pt). Baseline placement for horizontal
   labels: `y = baseline_pt - 0.9831*fontSize` (K_AR law), `h = 1.6*fontSize`,
   `valign:top`, `margin:0`.
6. **Label boxes**: white fill + thin red border; multi-color runs via text-run arrays
   (`bold`, `fontFace:"Arial"`, explicit sizes); text ink census (PIL word-stem
   sampling) decides the color mapping — the spec's color guesses were wrong in 3 of 6
   lines (042: 'One Input' GREEN, 'Sample (Using one filter)' GREEN+BLUE, '[4 Channels]'
   MAGENTA — keep per-frame census).
7. **Known frame-internal discrepancy to carry into 43/44 if it recurs** (SOURCES.md):
   the DRAWN column count may disagree with the label text (042: 5 columns drawn, label
   says "4 filters [4 Channels]") — the FRAME wins (fidelity law), record in SOURCES.md.
8. **Self-check kit**: reuse `selfcheck_attempt_4.py` as the template (closed-loop
   orig-vs-render bboxes, artifact-proof masks above, containment bands, ink-presence
   thresholds) + `house_chrome_check.py` + a crop vision comparison of the diagram
   region before the judge (cheap, caught nothing here but would have caught the
   tribug class). Tolerances: ~4-6 render px standard; 8-10 only for occlusion-sliver
   regions, and then ONLY with crop-compare corroboration.

## Evidence inventory (this dir)

- Builds: `build_attempt_{1,2,3,4}.js` (4 = certified) · live `build/slide_042.js`.
- Renders: `render_1.png` (pre-fix PNG-based build), `render_2.png` + `render_2_iter1_tribug.png`
  (attempt-2 native-vector build; the composition that was mid-judge at death),
  `render_3.png` (= render_2 pixel-identical, re-banked this run),
  `render_4.png` (CERTIFIED).
- Prompts: `judge_prompt_{2,3,4}.txt` (frozen template + substitutions).
- Transcripts: `judge_attempt_3.txt` (FAIL, adjudicated), `judge_attempt_4.txt` (PASS,
  DB-registered), `selfcheck_crop_diag_3.txt` (crop MATCH). Probes hung twice -> no
  probe transcripts (documented above).
- Self-checks: `selfcheck_attempt_{3,4}.py` + `_out.txt`, `house_chrome_check_{3,4}.txt`,
  `crop_diag_attempt3_{orig,render}.png`, legacy attempt-1/2 selfchecks.
- Superseded: `slide_042_recreated_attempt1.pptx` (attempt-1 build, kept as evidence).
- Measurement probes: `scratch/slide042/probe42_attempt3.py`, `probe42b_attempt3.py`
  (+ all earlier banked measure scripts/outputs from the previous builders).

## Appendix — builder-2 record (the "second builder" / attempt-1 PNG-based build)

Appended by the second dispatched builder (2026-10-12 ~04:40), which monitored
builders 3–4 read-only after detecting the concurrent resume, per the resume law.

**What this builder did (01:00–01:38):** resumed from the first builder's banked
`scratch/slide042/` measurement corpus (block_map.txt, measure_*.py — all reused and
extended: measure_chrome2/3, measure_content, measure_final, measure_struct,
measure_native, measure_last, measure_cubewalls, gen_diagrams, fit_block2/3,
gen_final — outputs banked alongside). Fitted this frame's chrome mapping
(left 59, right 901, top 43, bottom 516 -> x=18.66+0.96055·sx, y=0.95556·sy),
pixel-decided the contested facts (middle grid 4x5; layer order magenta/green/
orange/yellow/blue; label run colors GREEN count-words / BLUE "(Using …)" /
MAGENTA "[…]" / RED otherwise — all independently re-confirmed by builder-4's
deeper census), built `build_attempt_1.js` (PIL-generated cube-wall PNGs) +
`render_1.png` + `selfcheck_attempt_1/2`, set DB gen_status=building.

**Honest defect ledger for attempt 1** (builder-4's findings, verified true):
gray panel left visible inside the blue frame (interior must be WHITE — orig
(254,255,253)); the white stacking arrow at (803,297)..(814,310) omitted (this
builder's white-pixel scan window x640..800 missed x803-814 and it misread the
background wedge as the whole story — builder-4's crop_top.png proof is right);
h-arrow/labels and right-box overflow defects as listed in the attempt-2 header.
Attempt-1 was superseded; its assets (`s042_left_stack/mid_grid/right_block.png`
+ `*_meta.json` in `build/assets/`) remain banked as measured-reference material.

**Coordination lesson for storm-prone parallel dispatches:** builder 2 went
read-only for ~2.5 h while monitoring builders 3–4 (to avoid clobbering shared
files), which builders 3/4 could only interpret as a death — liveness is
invisible unless signaled through the shared state (DB touch / qa timestamp).
Builders 3 and 4 both applied the resume law correctly (bank superseded work,
never delete, continue numbering) — the handoff chain worked; the only cost was
one redundant build. Recommended: a builder that intentionally stands down should
write a one-line `last_error`/DB note saying "standby, monitoring", and a builder
taking over should still re-check for a live peer before dispatching judges.
