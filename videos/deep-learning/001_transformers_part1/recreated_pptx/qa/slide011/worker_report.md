# Worker report — slide 011 "Transformer / Attention is All You Need"

Video: `videos/deep-learning/001_transformers_part1` (Deep Learning DSAI 308, "Transformers — Part I")
Worker: per-slide build worker, 2026-10-11. Dependency status at start: **root** (unblocked).

## Deliverable

- **PPTX:** `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_011_recreated.pptx` (single-version law)
- **Build script:** `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_011.js`
  (banked per-attempt copy: `qa/slide011/build_attempt_1.js`)
- **Render (150 dpi):** `qa/slide011/render_1.png` (2001×1125)
- **Final verdict: PASS** — full-slide visual judge, real comparison winner body,
  `qa/slide011/judge_attempt_1.txt` (banked `judge_prompt_1.txt` = frozen 17 template with
  NNN=011 / K=1 / VIDEO substituted).

## Attempts used: 1 build attempt (1 render), judge comparisons: 2 dispatches (1st = 3
degenerate echo aborts; retry with identical parameters landed PASS). No rebuild needed.

## Judge findings (verbatim summary from the winner body)

FINAL VERDICT: PASS for 'faithful, usable recreation'. Zero MAJOR, zero BLOCKER.
Two MINOR notes: (1) dashed attention-flow curves render slightly heavier/darker than the
original's pale dashes; (2) red connector arrowhead curvature differs slightly. Both are
acceptable-fidelity notes, not fix triggers. The body explicitly verified: title/subtitle/
Decoder/badge chrome, both blocks verbatim, x/o token taps, both lavender panels, the
'attention' sub-box with fan lines, both 'Encoder-Decoder Attention' labels, self-loops,
all three note-box bullets verbatim INCLUDING the quirks ("( Training Mode Only)" spacing,
"Encoder ," trailing comma, double space in "Very Long  Sequence length"), blue underlined
links, 'Encoder' on the bottom band, no missing elements, no containment violations, mouse
cursor correctly omitted.

## Pre-judge self-check (mandatory battery) — `qa/slide011/selfcheck_attempt_1.py` +
`selfcheck_attempt_1_output.txt`: **32 OK / 0 FAIL** on the final render, including:

- Equations closed loop: x1/x2/x3 token ink bands vs original ≤1.1 frame px; o1/o2/o3 ≤3.1
  frame px (the 3 px is the arrowhead tip row inside the compare window, not the token).
  All six tokens render via matplotlib mathtext → 600 dpi PNG → addImage at exact px/600
  size, baseline-law placement (professional-format rule; equations-mathtext-png pattern).
- Geometry: yellow block / orange block / note box bboxes within 1–2 frame px of measured.
- Containment: zero content ink in canvas margins and in the 2 px ring inside each border
  stroke (predicate adapted for this playlist's white margin per dispatch; shared
  `check_containment.py` NOT edited — the ml-intro gray-canvas assumption does not apply).
- Note text pitch: measured render line tops 447/474/499 vs original 446/472/498 (Δ≤2 px).
- Z-order, wrap bands, delimiter geometry, table data: n/a (no tables/delimiters).

### house_chrome_check.py — documented false positive (intrinsic to this slide)

`shared_patterns/house_chrome_check.py` FAILs on my render — and **FAILs identically on
the ORIGINAL ground-truth frame** (banked in `selfcheck_attempt_1_output.txt`): the original
slide carries a WHITE content rectangle (frame px x 40..920, y 114..499, PIL-measured,
reproduced verbatim in the build) that covers the gray panel and its side borders over
those rows, so the checker's exposed-panel/column assumptions cannot hold for either
image. The chrome itself is drawn exclusively by the shared `house_chrome.js` module
(zero re-drawing), and the adapted chrome check passes 7/7 (panel visible above/below the
white box, all four border strokes, badge center/size/purple ring). Also: the spec's
"#BFBFBF footer strip" does not exist in the frame — the bottom band is the exposed panel
itself; "Encoder" sits on it, and the note box overlaps it, exactly as measured.

## Dense-region crop comparisons (pattern: dense-region-crop-compare)

Crops + numeric measurement banked under `qa/slide011/crops/`; raw dispatch logs under
`qa/slide011/logs/`. The gateway route was intermittently serving degenerate bodies this
window (echo-class prompt echoes and orchestration-roleplay fragments):

| region | outcome |
|---|---|
| arrows + o1/o2/o3 tokens | **PASS** (`crops/cropcmp_arrows.txt`, real verdict body; 2 MINOR: 4x-upscale stroke weight, rounder o glyph) |
| note box text | no verdict-bearing body after 4 dispatches (echo ×9 + narration fragment) — logs `crop_notebox*.log` |
| red arc + dashed curves | no verdict-bearing body after 3 dispatches (echo ×9) — logs `crop_arcdash*.log` |
| input lines + x1/x2/x3 | landed winner is an orchestration-roleplay fragment (process-FAIL narration, no image analysis; admits lines/positions correspond) — `crops/cropcmp_xlabels.txt` |

Per the verdict law the slide verdict stands on the full-slide comparison transcript; the
un-landed crop regions are additionally covered by the full-slide judge's explicit
findings (note-box bullets verbatim + quirks; dashes present with correct origin/target;
x-token taps) and the programmatic closed loops (≤1.1 px / ≤3.1 px, pitch Δ≤2 px).

## Documented deviations / judgment calls (frame-is-ground-truth)

1. White content rectangle over the panel (see above) — measured, reproduced.
2. Sub-block fills measured from large uniform interiors: #EFF1FD / #F3F1FC (spec's
   #D6D6F2 matches only the darker 1-px edge AA, not the fill).
3. Dashed cross-attention curves: FOUR dash chains per pixel forensics (spec: "2-3 [?]"),
   pale mauve #B790A5 (measured dash cores (183,144,165)); the spec's #FF9E9E would be
   visibly pinker than the frame. Judge confirmed dashes present, correct origin/target.
4. Spec's [?] items kept: dashed-curve count resolved to 4 by forensics; "Decoder" label
   placed at measured ink center (727.5, 97.5); badge numeral 11 per house law.
5. The fan below the 'attention' box: 3 solid dark lines from a common origin (285.5,277)
   to (190,306)/(288,306)/(385,306) — measured, replacing the spec's "three lines
   converging on the box's bottom center" reading.
6. o-arrows shortened to the measured head tops (y≈143.5) after the first self-check.

## Judge procedure note (17 §7 fallback)

No Agent/Task spawn tool in this environment → the banked judge procedure was executed by
the worker via Bash per 17 §7 (orchestrator-approved fallback). Probe law honored (probe,
sleep-300, re-probe; short walls never landed — three 124s hangs banked — so the
comparison went straight to the W4 wide wall). Banked prompt = the frozen 17 template with
only NNN/K/VIDEO substituted (its `.agents/image-analysis/...` path is stale post the
2026-10-11 skill move; execution used the real path `.agents/skills/image-analysis/...`).
Ordering deviation: the full-slide judge was dispatched before the crop comparisons
because short-wall probes kept hanging; crops then ran as mandatory corroboration.

## Evidence index

- `qa/slide011/judge_prompt_1.txt`, `build_attempt_1.js`, `render_1.png`
- `qa/slide011/judge_attempt_1.txt` — the PASS comparison transcript
- `qa/slide011/selfcheck_attempt_1.py` + `_output.txt` — 32/32 OK incl. original-frame
  chrome-check control run
- `qa/slide011/crops/` — 5 region crop pairs + measurements + landed transcripts
- `qa/slide011/logs/` — all failed-dispatch logs (echo/garbage/roleplay evidence)
- `scratch/slide011/` — measurement scripts (measure_frame.py, scan_frame.py, elements.py,
  regions.py, probe2.py, ascii_map.py), asset generator `gen_assets.py`
- `recreated_pptx/build/assets/` — arc011_red.png/.json, loop011_1/2.png/.json,
  dashes011.png/.json, eq011/eq011_{x1,x2,x3,o1,o2,o3}.png/.json

DB: gen_status=passed, visual_check=PASS, visual_attempts=1, transcript + paths set.
Slide 11 has NO dependents in `slide_dependencies.json` → no component export required.
