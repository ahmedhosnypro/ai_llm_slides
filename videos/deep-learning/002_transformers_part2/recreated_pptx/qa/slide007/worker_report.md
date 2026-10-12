# Worker report — slide 007 (video 002_transformers_part2), 2026-10-11

Slide: N=7, NNN=007 — section header "Parallelization / Implementation Issues".
Worker owned the slide end-to-end. Final verdict: **PASS** (attempt 2, real
comparison transcript). No prior worker progress existed (fresh start).

## Deliverables (single-version law)

- PPTX: `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_007_recreated.pptx`
- Build: `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_007.js`
- Evidence dir: `videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide007/`

## What was built

Playlist house chrome via the shared module
`videos/deep-learning/shared_patterns/house_chrome.js` (`drawHouseChrome(pptx, slide,
{numeral: 7})` — white canvas, gray E9E9E7 panel, C00000 border, FDFD96/6A5ACD badge,
bold 333333 numeral "7") + the two-line red (C00000) Arial bold title as two
single-line centered text boxes at measured ink positions:

- L1 "Parallelization" — 48.5pt, target ink cx 467.5pt, top 237.7pt
- L2 "Implementation Issues" — 48.5pt, target ink cx 474.7pt, top 292.0pt

Omitted as video-capture artifacts (judge GROUND RULES (c), spec-flagged): the mouse
cursor below "Parallelization" and the black bottom letterbox strip.

## Geometry work

002 frames are ~0.958-zoomed captures with a black letterbox strip below (slide_002
precedent). This frame's own mapping was fitted from its four chrome border stroke
centers (left 58.5, right 901.5, top 42.5, bottom 516.5 frame px ↔ slide chrome
42/919/45/540): `frame_x = 18.13 + 0.96123·slide_x`, `frame_y = −0.591 + 0.95758·slide_y`.
Badge cross-check: yellow-bbox center (875.5, 71.0) frame → slide (891.5, 74.9) vs house
(893, 71) — same ~3px JPEG-bbox jitter slide_002 accepted (same playlist template).
Title color census mode (184..193, 13..16, 29..35) = C00000 + JPEG noise (canvas
(254,255,253) and panel (231,233,230) identical to slide_002's certified frame — frame
NOT dimmed). Title em re-fit from ink widths: 319.4/6.725em and 517.1/10.781em → 48.5pt
(spec's "40–44pt" was a zoomed-frame estimate; PIL measurement wins). Measured line ink
centers are genuinely off slide center (467.5/474.7 vs 480) — reproduced as measured.

## Attempts

- **Attempt 1 (pre-judge iteration, no judge dispatched):** built at 48pt; closed-loop
  PIL check FAILED (ink width −8.4/−12.3px @150dpi; centers −1.5/−0.5px). Fixed:
  fontSize 48→48.5, box centers +1.5/+0.5pt, y-lead trim. Evidence:
  `scratch/slide007/closed_loop_attempt1.txt`, `selfcheck_attempt_1.py`.
- **Attempt 2:** render_2.png — house_chrome_check.py **PASS**; closed-loop ink check
  **PASS** (all ink-edge errors within ~4px @150dpi: L1 x0 +2.7, x1 +1.3, y0 +0.8,
  y1 −3.2; L2 x0 +1.6, x1 −0.7, y0 +0.7, y1 −4.0; color mode exactly (192,0,0)).
  Evidence: `scratch/slide007/closed_loop_attempt2.txt`, `selfcheck_attempt_2.py`,
  `qa/slide007/render_2.png`.

## Judge (attempt 2)

- Judge prompt banked verbatim: `qa/slide007/judge_prompt_2.txt`; build copy banked:
  `qa/slide007/build_attempt_2.js`.
- **No Agent/Task tool available in this environment → judge procedure executed by the
  worker itself via Bash, byte-for-byte per the banked prompt (orchestrator-approved
  fallback); verdict taken verbatim from the comparison winner body.**
- Probe: `qa/slide007/probe_2.txt` — valid body, window open.
  (Path note: the template's `.agents/image-analysis/scripts/analyze_image.py` is
  stale; per the skill's 2026-10-11 amendment the script lives at
  `.agents/skills/image-analysis/scripts/analyze_image.py` — used that.)
- Comparison: `qa/slide007/judge_attempt_2.txt` — `[winner] images (round 1,
  attempt 1)`, degenerate events 0, `--thinking high --max-tokens 65536`, W4 wall
  (timeout 420 wrapped in 540), through `scripts/16_vision_gate.sh` with TMPDIR
  redirected off /tmp. Certificate label: **single-read, default route (images),
  glm leg DEFERRED/BLOCKED.**
- Findings: no discrepancies ("None found" table); title verbatim + line break +
  spacing match; frame containment OK; contentlessness matches (rule (b)); cursor +
  letterbox omissions mandated (rule (c)); colors match. Minor non-counted note:
  badge ring slightly more saturated purple — house chrome, excluded per rule (a).
- **FINAL VERDICT: PASS for 'faithful, usable recreation'.**

## Pre-judge self-check coverage (mandatory checklist)

1. Patterns index read (shared_patterns/index.json — house_chrome used).
2. Frame containment: title ink x 452..1527 / y 496..704 px inside panel x 89..1913 /
   y 95..1125 @150dpi — PASS.
3. Equations: none on slide — N/A. 4. Delimiters: none — N/A. 5. Tables: none — N/A.
6. Zoomed crop vision: N/A (no equations/delimiters/tables — title only).
7. Line/box wrap: single-line boxes, ink bands match targets, no stray ink — PASS.
8. Line spacing: no multi-line text box — N/A (two single-line boxes).

## DB

`gen_status=passed`, `visual_check=PASS`, `visual_attempts=2`,
`visual_transcript=videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide007/judge_attempt_2.txt`,
`pptx_path`, `build_script` set. Row verified: slide 7 passed/PASS.

## Component banking

No slide in any video's dependency graph references 002:7 (checked
`slide_dependencies.json`) — no banking obligation.

## Provenance

`slide_007_source/SOURCES.md` was already banked by the web-verification worker
(course-authored header; Vaswani §3.2 + Table 1 recorded as background for following
slides only). No sourced content enters the recreation (frame is ground truth).
