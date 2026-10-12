# Worker report — slide 046 "POOLING" (001_introduction, Deep Learning DSAI 308)

Date: 2026-10-12. Fresh start (no prior artifacts; DB row pre-set `gen_status=building`
with no pptx/build/qa evidence). Judge procedure executed by the worker itself via Bash
(no Agent/Task spawn tool in this environment — orchestrator-approved fallback, noted per
17_worker_instructions.md step 7).

## Dispatch-fact deviation (noted up front)

The dispatch described slide 046 as "Standard Neural Network (NN) vs Convolutional Neural
Net (CNN)". Ground truth disagrees: `unique_slides/slide_046.jpg`, `analysis/slide_046_final.json`
and `slide_046_source/SOURCES.md` all say **POOLING** (the NN-vs-CNN slide is 001's slide 50).
The frame is law — the build recreates POOLING. Badge numeral 46 per dispatch + playlist law
(001_introduction originals carry no printed numbers — assumption pending founder veto).

## Result

- **Verdict: PASS** — judge attempt 1 of max 6 (single attempt; coherent winner body,
  `FINAL VERDICT: PASS for 'faithful, usable recreation'`, no BLOCKER/MAJOR findings).
- Deliverable (SINGLE-VERSION): `videos/deep-learning/001_introduction/recreated_pptx/slide_046_recreated.pptx`
- Build script: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_046.js`
  (banked copy: `qa/slide046/build_attempt_1.js`)
- Comparison transcript: `qa/slide046/judge_attempt_1.txt`
- DB: gen_status=passed, visual_check=PASS, visual_attempts=1, pptx_path/build_script set.

## Build summary (all geometry PIL-measured, banked in measure_original{,2,3,4,5}_out.txt)

- Chrome: `shared_patterns/house_chrome.js` imported (never re-drawn), numeral 46.
  `house_chrome_check.py` PASS on every render (attempt1/2/3/4 outputs banked).
  Interpretation: the original's red top/left L-lines + gray field are this frame's own
  chrome (gray measured x 38..921, y 43..517 ≈ canonical x 42..918, y 45→bottom) — chrome
  drawn at canonical values; slide_040 precedent, covered by judge ground rule (a).
- White content panel (fill FFFFFF measured) with C00000 1.5pt border, stroke-center
  x 57.5..877.5, y 133..456.5 — drawn as CONTENT at the measured position.
- Title POOLING: Arial Bold 34.9pt C00000, ink center 483, baseline 105 (render-corrected
  param 102.5 after closed loop).
- Bullets: main 20.4pt + 3 subs 17.95pt, color 5E5E5E (measured core smear-corrected;
  spec 3B3B3B reads darker than the JPEG), hollow-circle markers at measured positions.
- Option boxes: 333399 borders (stroke modal reconciled; spec 3333CC washed by JPEG),
  white fill, text 20.6pt at measured baselines 268/302.5.
- Diagram: 2x2 green 0CC850 matrix (cells 35x31.5, black 1pt borders, letters a/b/c/d/z
  Arial Bold 18pt), hollow right-arrow (white fill, black 1pt, ink x 256..321 y 351..383,
  tip over z's left edge as in the original), "Pool (" and ")" Times New Roman Italic 20pt
  (normal-size parens — measured h 17, NOT tall delimiters), "==" Arial 24pt gray 4E4E4E
  (LO baseline calibrated by probe: bars_mid = param − 11.8 → param 379.3), tiger photos
  CROPPED from the original frame (187x89 at (424,325); 98x48 at (670,342)) into
  `build/assets/`, caption "Size is reduced" Arial Bold Italic 13.4pt 333399 underlined
  (italic per the zoom crop-compare's direct observation).
- Deliberately omitted (spec + ground rule c): black video-player strip y 518..539, mouse
  cursor near "Average pooling".

## Pre-judge checks (all banked in qa/slide046/)

- `house_chrome_check.py`: PASS (attempts 1–4).
- Closed-loop PIL self-checks (`selfcheck_attempt_{1,2,3,4}.py` + outputs): 24 element
  checks vs the original's measured bboxes at ≤2.0–2.5 frame-px tolerance (~4px @150dpi).
  Iterations: attempt 1 → subs +3.5 low, title +2.5 low, caption low; attempt 2 → '=='
  bars high (LO baseline model wrong for '=') → LO probe calibration; attempt 3 → single
  residual; attempt 4 (italic caption) → same single residual:
  **sub2 right edge +2.6 frame-px** (760.6 vs 758 on a 632px line = 0.4% — renderer kerning
  drift; sub1/sub3 fit within 1.7 at the same 17.95pt; accepted as measurement noise, not a
  defect; the full judge did not flag sub-bullet width).
- Dense-region crop comparison (pattern law): diagram band cropped from BOTH images at
  identical effective scale (2710x416; ink spans match within 2px at zoom) →
  `cropcmp_diagram.txt`: **PASS**, 5 MINOR (border weight reading, arrow boldness, z-border
  weight, ')' adjacency, caption italic). The caption-italic finding was applied; the rest
  are measured-matched cosmetics (original ink bboxes match within tolerance; the ')'
  adjacency: original ')' x 611..617 vs photo right edge 610.5 — same adjacency in the
  render, 611.0..614.8 measured).

## Judge attempt 1 — findings (all MINOR, none fix triggers)

1. Arrow larger/wider than original (confidence high) — arrow drawn at measured ink bbox
   256..321 x 351..383; the original's stroke is thinner (JPEG hairline). Accepted cosmetic.
2. Caption italic non-bold in original vs bold italic in recreation — partially addressed
   pre-judge (italic added); boldness retained per spec ("blue, bold, underlined").
3. ')' photo adjacency — rebutted by measurement (same adjacency in both).
4. Sub-bullet marker-to-text gap marginally tighter — markers placed at measured cx 132.5,
   text at measured ink left 140; within ~1 frame-px of the original.

## Evidence index (qa/slide046/)

- measure_original.py..measure_original5.py + *_out.txt (5 forensics passes)
- selfcheck_attempt_1..4.py + outputs; house_chrome_check_attempt{1,2,3,4}_out.txt
- crops/crop_render.png, crops/crop_original.png, cropcmp_diagram.txt
- probe_1.txt, judge_p_payload_1.txt, judge_prompt_1.txt, judge_attempt_1.txt
- build_attempt_1.js; render_1..4.png
- LO baseline probe: scratch/slide046_render/probe_eq.{js,pptx,png}

## Notes

- No component-banking obligation: no slide in any video's dependency graph references
  `deep-learning/001_introduction:46` (002's `"46": [45]` is 002's own same-video edge).
- No OMML wrap (no equations); no graphgen (photographic imagery, cropped from ground truth).
- Attempts used: 1 of 6 judge attempts (renders 1–4 were pre-judge closed-loop iterations).

## Verification addendum — collision-protocol reader (2026-10-12 ~08:05)

A second worker was dispatched on slide 046 and independently reached the build stage
(own PIL forensics in `scratch/slide046/`) before detecting the live peer and standing
down READ-ONLY per the collision protocol. It verified the banked certification without
mutating any evidence:

- DB row current: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
  `visual_transcript=qa/slide046/judge_attempt_1.txt` (updated 07:57:24).
- Judge evidence is a real, coherent comparison winner body: GROUND RULES dispositions
  (a)/(b)/(c)/(e), element-by-element table, frame-containment + vertical-centering
  audits, 4 MINOR findings, zero BLOCKER/MAJOR, explicit
  `FINAL VERDICT: PASS for 'faithful, usable recreation'`.
- Certificate binds to the JUDGED artifact: `judge_prompt_1.txt` and
  `judge_p_payload_1.txt` name `qa/slide046/render_4.png` explicitly; `render_4.png`,
  `build/slide_046.js`, and `slide_046_recreated.pptx` are all mtime 07:51, and
  `build_attempt_1.js` is byte-identical to the live build script (diff verified).
- Independent re-run (read-only) of `shared_patterns/house_chrome_check.py` on
  `render_4.png`: **PASS** (panel + badge within tolerance 8).
- Single-version law holds: deliverable is the plain-named `slide_046_recreated.pptx`;
  no `_graphed`/`_omml` variants (none applicable: no OMML equations, no graphgen slides).
- Banking obligation re-confirmed independently: 001_introduction's
  `slide_dependencies.json` contains no edge touching 46 (edges: 16←9, 17←16, 18←9,
  19←9, 25←24, 37←36, 41←35); no component bank required.

Conclusion: certification accepted as-is from the banked judge PASS. No rebuild, no
re-judge, no further mutation performed by the verifying worker.

### Asset-chain repair note (same verifying worker, 08:08)

During the overlap window the verifying worker's own pre-detection photo crops
(186x90 @ (426,325) / 102x49 @ (672,341), written ~07:49 into `build/assets/` under the
same natural filenames) ended up shadowing the certified build's referenced assets.
The certified pptx embeds ITS OWN crops (187x89 / 98x48 = `ppt/media/image-1-1.png`,
`image-1-2.png`), and the build script references `assets/tiger_large.png` /
`tiger_small.png`. To keep any future rebuild byte-consistent with the certified
artifact, the verifying worker restored both asset files from the certified pptx's
embedded media (extracted to /tmp/pptx46_inspect, copied over the shadowing files).
No banked evidence deleted; the certified pptx itself was never touched.
