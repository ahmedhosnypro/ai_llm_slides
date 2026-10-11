# Worker report — slide 014 "Encoder – Decoder Transformer"

Video: `videos/deep-learning/001_transformers_part1` · Worker: per-slide build worker
Date: 2026-10-11 · Attempts used: **1 of 6** · Final verdict: **PASS**

## Deliverable

- PPTX (single-version law): `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_014_recreated.pptx`
- Build script: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_014.js`
  (thin wrapper; composition in the component below)
- **Dependency component (child 15 imports this)**:
  `videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_014.js`
  — `renderBase(pptx, slide, opts)` with `opts.skip` / `opts.only` / `opts.chrome` /
  `opts.numeral`, block granularity: `title, left_panel, left_figure, arc,
  right_panel, right_figure, red_caption, blue_takeaway` (chrome via
  `components/house_chrome.js`, which delegates to the playlist shared pattern).
  Child 15 (REPLACES the right half) should skip
  `right_panel, right_figure, arc, red_caption, blue_takeaway` and draw its own right
  half. DB now shows **15 unblocked**.
- Assets (banked under `recreated_pptx/build/assets/`): `slide014_fig1.png` (byte-copy
  of the founder-downloaded paper Figure 1, arXiv 1706.03762v7, from
  `../001_transformers_part1/slide_18_source/` — never modified there),
  `slide014_fig1_cw.png` (same image pre-rotated 90° CW via PIL ROTATE_270),
  `slide014_arc_cw.png` (600 dpi transparent rotation arrow, 750×750 px → exactly 1.25 in).

## Attempt 1 — build + evidence chain

- **Frame measurement** (`scratch/slide014/measure1–5.py`, `fontcal.py`, `arc_opt.py`):
  - White panels (course-drawn, thin black border): left x[93.5,411.5] y[106,522.5];
    right x[476.5,892.5] y[152,470.5] (exact 90°-CW transposes).
  - Figure placement by mask-correlation fit (scale 0.182, natural aspect):
    left rect x[117,394] y[115,522] (IoU 0.761); right = same image rotated 90° CW,
    rect x[478,885] y[176,453] (IoU 0.781); margins are exact rotated transposes
    (L22 T7 R17 B0 → L0 T22 R7 B17) — proves the frame shows one rigidly rotated copy.
  - Rotation arrow: circle center (450.4,307.6), annulus r 12.75..30.75, sweep 90°..285°
    (y-up), triangular head (base r 6.5..40 at 90°, tip r 27.5 at 52°) pointing CW into
    the east gap — grid-search IoU 0.851 vs the frame red mask; core color #CC0000
    (measured #CC0404). Text: title 35.5 pt / caption 20 pt / takeaway 24.5 pt Arial Bold,
    calibrated with real Arial metrics against frame ink (skirt-inclusive); reds #A0000E
    (certified slide-006 precedent family, measured cores #9F101F..#AD1A29), blue #00008B
    (measured cores #04047C..#040484).
- **Pre-judge self-checks** (`selfcheck_attempt_1.py` + `selfcheck_attempt_1_output.txt`,
  all banked): `house_chrome_check.py` **PASS**; containment (all elements inside house
  frame; arc fully inside the gutter between panel borders) PASS; text ink bboxes vs
  frame (skirt-inclusive targets; blue/width fixed by 24.5 pt, title by 35.5 pt) PASS;
  no-wrap bands PASS; figure IoU left 0.756 / right 0.799 (≥0.60) PASS; arc IoU 0.867
  PASS; panel borders 24/24 probes PASS; panel whiteness PASS.
- **Dense-region crop comparisons** (image-analysis default route, `--thinking high
  --max-tokens 65536`, W4 wall; crops banked under `qa/slide014/crops/`):
  - `crop_left_attempt_1.txt` — **PASS** (labels, stacking, junctions, icons match;
    original's pen/cursor artifact correctly omitted per ground rule (c)).
  - `crop_right_attempt_1.txt` — **PASS** (rotated labels verbatim, correct reading
    direction, strip order correct; zero BLOCKER/MAJOR).
  - `crop_arc_attempt_1.txt` — **PASS** ("C-shaped ~270° arc, gap facing right, thick
    ring, solid triangular head at top pointing right — faithfully reproduced"; 3
    sub-minor rotational nuances).
- **Full-slide judge** (attempt 1): `judge_prompt_1.txt` (banked verbatim template +
  worker view-context noting the founder figure-image mandate and root status) →
  `judge_attempt_1.txt` (4430 bytes, single coherent winner body, no
  truncation/garbage markers). **FINAL VERDICT: PASS** for 'faithful, usable
  recreation'. Findings: 3 MINOR polish-level margin-tightness notes (rotated
  "Output Probabilities" near the right border; "Outputs (shifted right)" closer to
  the left panel's bottom border; right-panel internal margins slightly tighter) —
  all are internal proportions of the founder-mandated paper-figure embed vs the
  course redraw, explicitly judged "polish-level, not fidelity failures". No
  BLOCKER, no MAJOR, no missing elements, no containment breach.

## Certificate

Single-read, default route (images, no `--models`), glm leg DEFERRED/BLOCKED.
**Judge procedure executed by the worker; no spawn tool available** (documented
17 §7 fallback, orchestrator-approved) — all five vision transcripts banked as `.txt`
under `qa/slide014/` and read from disk, never from PNG bytes.

## DB state (end of run)

`gen_status=passed` · `visual_check=PASS` · `visual_attempts=1` ·
`visual_transcript=videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide014/judge_attempt_1.txt`
· `build_script=videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_014.js`
· `pptx_path=videos/deep-learning/001_transformers_part1/recreated_pptx/slide_014_recreated.pptx`
