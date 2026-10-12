# Worker report — slide 018 "Adding Position Information" (002_transformers_part2)

Date: 2026-10-12. Worker: slide-recreation build worker (root slide, no dependency
edge, no pattern group; badge numeral 18).

## Result

- **Final verdict: PASS** (visual judge attempt 1, real comparison winner body).
- Deliverable: `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_018_recreated.pptx`
  (single-version law — no suffixes; no equations -> no OMML wrap; no advanced
  graphs -> no graphgen).
- Build script: `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_018.js`
- Comparison transcript: `videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide018/judge_attempt_1.txt`
- Probe transcript: `videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide018/probe_1.txt`
- DB: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
  `visual_transcript` set, `last_error` clear.

## Attempts used

- **Judge attempts: 1 / 6 max.** Judge prompt banked verbatim at
  `qa/slide018/judge_prompt_1.txt`; per-attempt build copy at `qa/slide018/build_attempt_1.js`.
  No Agent/Task spawn tool available in this environment -> judge procedure executed
  by the worker via Bash, byte-for-byte per the banked prompt (orchestrator-approved
  fallback, 17_worker_instructions.md §7). Comparison ran at `--thinking high
  --max-tokens 65536`, gate timeout 540 / script timeout 420 (W4 wall from the start).
  One script-recovered `EmptyStreamError` (abort+retry 1/3) then a validated winner;
  degenerate-garbage events: 0.
- **Pre-judge closed-loop renders: 3** (no judge dispatched until the PIL loop
  passed). Renders banked as `qa/slide018/render_1.png` (initial), `render_2.png`
  (size/cx/lead corrections), `render_3.png` (charSpacing 0.15 + shadow 0.05) —
  render_3 is the judged render. Self-check: `scratch/slide018/selfcheck_attempt_1.py`
  + `selfcheck_attempt_2_output.txt` + `selfcheck_attempt_3_output.txt`;
  `house_chrome_check.py: PASS` on every render.

## Frame->slide mapping (video-002 zoomed-out capture)

Fitted from THIS frame's chrome landmarks (panel left 58.04 / right 900.95 / top
43.02 / bottom 516.41 <-> slide 42 / 919 / 45 / 540):
`frame_x = 17.674 + 0.96113*slide_x; frame_y = -0.013 + 0.95633*slide_y`.
Badge cross-check: frame badge center (875.5, 71.0) -> slide (892.5, 74.3) vs house
(893, 71) — dx 0.5 / dy 3.3 px, same accepted JPEG-bbox delta as certified slide_002.
Omitted as capture artifacts (ground rule c): presenter cursor at frame (392..401,
239..249); black letterbox strip rows 519..539.

## Closed-loop verification (render 3 vs mapped targets, tolerance ~4px @150dpi)

| Element | deltas (px @150dpi) |
|---|---|
| Title ink | x0 -0.7, y0 -0.1, x1 +0.1, y1 -2.5, cx -0.3 |
| Line 1 ink | x0 -0.4, y0 +0.5, x1 +2.9, y1 -0.3 (blue seg x1 -1.1, red seg x0 -1.4 / x1 +2.9) |
| Line 2 ink | x0 -0.4, y0 +0.8, x1 +0.2, y1 -1.2 (blue x1 -1.1, mag x0 +0.7 / x1 +0.2) |
| White box | rows +0.7 / -0.9, cols +0.6 / -1.0 |
| Shadow just-below-band | render 220.2 vs original 221.8 (panel 232 both) |
| Letterbox absent | True |

Key build parameters converged: title 39.6pt, body 31.1pt Arial Bold (spec's ~28pt
estimate was low; advance-fit + closed-loop decided), body lead 0.274em, blue runs
charSpacing 0.15pt (Liberation-vs-original advance micro-fit for the color-run
boundary), shadow outer blur 3 / offset 2 / opacity 0.05 (matches the original's
~10-unit band within 1.6 units). Colors: spec hexes win (CC0000 / 0000A0 / CC00CC /
D9D9D9) — PIL cores sat uniformly ~0.83-0.92x below spec (video/JPEG darkening of
saturated dark inks; light badge yellow measures undarkened), matching the certified
slide_002 precedent. Lines are LEFT-aligned at a common ink edge (265.65pt) per the
frame — the spec's validation had resolved this to "centered" and flagged it
uncertain; frame wins (both lines' left ink edges identical at frame x=273).

## Judge findings (verbatim summary)

- Ground rules settled: house chrome, cursor omission, letterbox omission — all
  explicitly accepted as non-discrepancies.
- Element-by-element table: all MATCH (title text/color, panel geometry, line
  splits and colors, inter-line spacing, alignment, containment, badge).
- Two MINOR notes (both "visually negligible / imperceptible", confidence high):
  white panel bottom edge ~2-3% lower; title baseline ~2-3% lower. These are the
  judge's eyeball percentages; the PIL closed-loop measured the box within 1px and
  the title ink top within 0.1px of the frame-mapped targets, so they are judge
  variance, not fix triggers. No BLOCKER/MAJOR findings, no missing elements.
- `FINAL VERDICT: PASS for 'faithful, usable recreation'.`

## Self-check law compliance

Patterns read pre-build (project + playlist indexes): used house-chrome (shared
module, never hand-drawn), highlight-box (measured box, wrap budget), explicit-line-
spacing reasoning (single-line boxes placed at measured bands -> pitch 69.0pt
reproduced by placement; no multi-line box, no empty runs). Frame containment PASS
(all ink inside panel border; no letterbox). Equations/delimiters/tables: none on
this slide (crop-compare tier not mandatory). No [?] markers in the spec; none
dropped. Web provenance: `slide_018_source/SOURCES.md` was BANKED (Vaswani §3.5
"learned and fixed"); no figure download needed (course-authored agenda).

## Dependents

None reference `002_transformers_part2:18` (checked `slide_dependencies.json` and
the DB deps view) -> no component-banking obligation.
