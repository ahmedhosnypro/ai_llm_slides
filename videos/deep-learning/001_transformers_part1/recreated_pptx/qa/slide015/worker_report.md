# Worker report — slide 015 (deep-learning/001_transformers_part1)

**Final verdict: PASS** (attempt 1 of 6). Deliverable:
`videos/deep-learning/001_transformers_part1/recreated_pptx/slide_015_recreated.pptx`
(single-version law; no equations on this slide, so no OMML pass applies).

## Dependency status

- Edge 15 ← 14 (`slide_dependencies.json`). Parent 14 certified (`gen_status=passed`,
  `visual_check=PASS`); `15_progress.py deps` reported 15 **unblocked** before the build.
- Slide 15 has NO dependents (no edge lists 15 as a parent), so no
  `build/components/slide_015.js` export is required.

## Build (attempt 1)

`recreated_pptx/build/slide_015.js` — requires the certified parent component
`components/slide_014.js` and calls
`renderBase(pptx, slide, { numeral: 15, skip: ["arc","right_panel","right_figure","red_caption","blue_takeaway"] })`
(title, left panel, left figure, chrome inherited — never re-derived). Delta drawn at
this frame's own PIL-measured geometry (scripts in `scratch/slide015/measure1-4.py`,
`recolor2.py`, `verify_asset.py`):

- **Right panel**: white card, 2pt `00B050` border (stroke centerline rect
  573,105 → 894,524 pt; measured strokes cols 572–574 / 893–895, rows 104–106 / 523–525).
- **Recolored Figure 1** (founder mandate: the downloaded arXiv image, recolored per the
  frame): `build/assets/slide015_fig1_color.png` (600 dpi, 2650×3467, embedded at exact
  size 318×416 pt at (575,107)). Asset construction (`recolor2.py`):
  - background fields (peach `FDEDDD` encoder column / mint `CEFFE1` decoder column,
    measured flat cores; NOT the spec's guesses) traced from the frame via a per-pixel
    class map (white/peach/green, 3×3-majority + inpaint under ink) — class agreement
    vs frame 0.999;
  - the paper figure alpha-composited on top at frame-measured rect x[598,874] y[115,522]
    (277×408 pt; IoU-optimal paste, dark-ink IoU vs frame 0.579 — same deviation class as
    the certified left panel's 0.609, i.e. course-redraw vs paper-image internals);
  - **per-box tint remaps measured from the frame** (mode of mapped fill pixels): the
    course retinted MORE boxes than the spec recorded — decoder Add & Norm ×3 →
    greenish (≈ CAFEBC), decoder FF → cyan-green (≈ A2EEDA), decoder MHA + masked MHA →
    pale yellow-green (≈ CAE6AE), decoder Output Embedding → green (≈ CAE6CE), decoder
    Linear → greenish-lavender, decoder Softmax → green; encoder MHA → tan (F6D6AA),
    encoder FF → gray-blue (CEDE D2 band), encoder Add & Norm → warmer yellow (F6EABA);
    encoder embedding stays pink. Position-restricted classification (padded-bbox)
    prevents cross-column misassignment between same-colored paper boxes.
- **Red gutter block arrow**: exact measured polygon (shaft x[458,512] y[300,313] +
  head base x512 y[295,318], tip (525,306.5)), 600 dpi PNG at exact size 68×24 pt at
  (458,295), core `CC0000` (measured (204,0,0)).
- **Two small red up-arrows** (600 dpi PNGs, background-relative redness alpha):
  up1 x[654,666] y[487,513] (beside "Inputs"), up2 x[740,750] y[116,140]
  (top of decoder region, beside "Output Probabilities").
- **Headers**: "Encoder" `C00000` / "Decoder" `00A651`, Arial bold italic 16 pt
  (frame ink widths 66/67 px confirm the size), closed-loop positioned
  (Encoder box (583,112); Decoder box (769,111) after a 2.5 pt nudge).

## Pre-judge self-checks (ALL PASS; banked)

- `house_chrome_check.py` on `qa/slide015/render_1.png`: **PASS**
  (panel x 89–1913, badge center (1860,148) d=70, tol 8).
- `scratch/slide015/selfcheck_attempt_1.py` (+ `_output.txt`): 24/24 PASS —
  - inheritance diff vs parent certified render `qa/slide014/render_1.png` fully
    confined to the badge numeral (14→15), the removed-arc strip, and the right half;
    stray diff px = 0; **left figure mean|diff| = 0.00** (pixel-identical inheritance);
  - containment: no delta ink outside the playlist chrome panel; strip between title
    and panel clean; gutter clean outside the block arrow;
  - green border cols/rows within 4 px of measured; shading field cores exact
    ((253,237,221)/(206,255,225)) and spans within 8 px;
  - block arrow bbox within 5 px, shape IoU vs frame 0.916, core (204,0,1);
  - up-arrow IoUs 0.779 / 0.840; header ink bboxes within 4–5 px of frame;
  - asset verification: class agreement 0.999, 11/14 box fills exact, remaining 3 are
    the verify rect's own border contamination (comp targets match interior point samples).
- Zoomed crop vision pass NOT run: the mandatory trigger (equations / multi-line
  delimiters / tables) does not apply to this slide; the full-slide judge + PIL
  structural checks are the evidence.

## Judge (attempt 1)

- **Judge procedure executed by the worker; no spawn tool available** (documented 17 §7
  fallback). Banked verbatim prompt: `qa/slide015/judge_prompt_1.txt` (frozen `-p`
  template; shared-base fact carried in `--view`; path corrected to
  `.agents/skills/image-analysis/scripts/analyze_image.py` — the 17 template's path is
  stale). Build copy: `qa/slide015/build_attempt_1.js`. Render: `qa/slide015/render_1.png`.
- Probe: 2 outer-wall timeouts (150 s) — first a pure hang, then the gateway responded
  with an upstream GarbageError (window proven open); no probe transcript landed.
  Comparison run directly at the W4 wall (540 s) and landed on the first try.
- `qa/slide015/judge_attempt_1.txt` (3470 B): single coherent winner body —
  element-by-element table; **all three removals verified executed**; all text verbatim;
  line breaks/centering match; containment clean including the tightest items;
  "no missing elements, no overflow, no delimiter/centering/spacing defects".
  Findings: (1) block arrow "slightly narrower" — MINOR, medium confidence: judge
  estimate vs this build's PIL-measured polygon (bbox within 5 px, IoU 0.916 vs frame)
  — measured ground truth wins, no fix; (2) right-panel tints "slightly more muted" —
  MINOR, explicitly judged "within the mandated delta" (tints are the frame-measured
  cores). **FINAL VERDICT: PASS for 'faithful, usable recreation'.**

## Certificate

Single-read, default route (images, no `--models`), `--thinking high --max-tokens 65536`,
glm leg DEFERRED/BLOCKED. Judge procedure executed by worker (no Agent/Task tool in this
environment — orchestrator-approved 17 §7 fallback).

## DB state (end of run)

`gen_status=passed` · `visual_check=PASS` · `visual_attempts=1` ·
`visual_transcript=videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide015/judge_attempt_1.txt` ·
`build_script=videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_015.js` ·
`pptx_path=videos/deep-learning/001_transformers_part1/recreated_pptx/slide_015_recreated.pptx`
