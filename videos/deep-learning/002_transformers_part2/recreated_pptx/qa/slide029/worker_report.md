# Worker report — slide 029 (002_transformers_part2) — PASS on attempt 1

Slide: N=29, NNN=029 — "Sequence of 12 words / Positions are defined / as angles"
Video: `deep-learning/002_transformers_part2` · Dependency-gated child of slide 28
(edge `29 ← 28`, certified 2026-10-12). Founder HARD STOP for this frame set was
already satisfied (002 curation record).

## Result

- **Final verdict: PASS** (attempt 1 of 6 allowed).
- Judge: full frozen `-p` template WITH GROUND RULES; worker context in `--view`
  carried the shared-base fact ("base composition = slide 28's certified component,
  imported; expected difference = the 12-word delta + callout only") plus the two
  PIL-settled facts (no arc 11 on the frame; family arrowhead convention).
- Certificate: single-read, default route (images), glm leg DEFERRED/BLOCKED.
- Deliverable (single-version): `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_029_recreated.pptx`
- Build: `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_029.js`
  (requires the certified `components/slide_028.js` by ABSOLUTE path and calls
  `renderBase(pptx, slide, { numeral: 29, wordCount: 12, skip: ["arcs","title"] })`;
  the composition is imported, never re-drawn — arcs 0-3 via P27.drawArc, 4-6 via
  P28.drawArcDelta, 7/8-10 as this slide's measured delta, title/callout as delta).

## Attempts

| K | verdict | evidence |
|---|---------|----------|
| 1 | PASS | `qa/slide029/judge_attempt_1.txt` (comparison winner body, round 1, 0 degenerate events) |

Pre-judge gates (all banked under `qa/slide029/` + `scratch/slide029/`):
- `house_chrome_check.py` PASS (panel/badge within tol; numeral 29).
- `selfcheck_attempt_1.py` → **ALL PASS** (34 checks): title-1 ink bbox, callout
  border cores/white fill/text ink bands + widths (≤4 render px), yellow highlight
  band, red-ω-in-L1, heads 8-10 bbox centers, label k7m/8/9/10 centers, old-k7 spot
  empty, chips 9-11, arcs 8-10 present / arc 11 absent, containment, house-frame
  containment. Two build fixes were applied during self-check (both pre-judge):
  1. callout font 14pt (spec guess) → **16.75pt** (closed-loop ink-width fit; L2
     rendered 277.8pt vs measured 278.8pt at 16.5, all three bands ≤4px at 16.75).
  2. the "double left edge" reading was corrected to a SINGLE callout rect
     (x 48.24, y 409.7, w 311.0, h 124.3, C00000 2pt): the frame's cols 57-59 stroke
     is the PANEL border (present on 028 too; the 28v29 diff blob starts at col 64).
     Caught after the probe render flagged a spurious stroke left of the panel border.
- Dense-region crop comparisons (all PASS, banked): `crop_callout_1.txt` (2 MINOR:
  content block ~2.5-4 slide-pt high in box — within the ≤4px closed-loop tolerance;
  background dotted lines out of crop scope), `crop_bottomsector_1.txt` (1 MAJOR
  OVERRIDDEN + 2 MINOR — see overrides), `crop_title1_1.txt` (2 MINOR, ≤4px edges).

## Judge findings (main comparison) and disposition

1. MINOR — arrowhead rotation convention (unrotated down-triangles vs tangent-
   rotated appearance in the original): certified house style (027 convention law,
   judge-PASSed on 27 and 28); PIL row-width profiles of 029's new heads 8/9/10 are
   indistinguishable from the certified 028 heads (both read ambiguously at ~7-9px
   size). Not a fix trigger. The bottom-sector crop's MAJOR "arrowheads reversed"
   was settled the same way: measurement beats a ~75%-confidence tiny-crop reading;
   the convention is family-certified.
2. MINOR (crop) — arc stroke "solid vs faintly dashed": the family law pins the arc
   stroke SOLID F0C9B0 0.75pt ("do NOT thicken or dash it" — the original's stroke
   is below the JPEG noise floor). Certified; not a fix trigger.

## Measured delta (all PIL on `unique_slides/slide_029.jpg` vs `slide_028.jpg`;
masks calibrated against 028's certified constants — label method bias 0.0, head
masks ≤1.5pt; full campaign in `scratch/slide029/measure1-5.py` + outputs)

- Frame→slide mapping verified from THIS frame's chrome landmarks: pixel-identical
  to 028's (L col 58, T row 43, letterbox rows 519-539) → parent mapping
  `fx = 18.63 + 0.96123·sx ; fy = 0.95556·sy` lands 1:1.
- Title line 1: ink CENTER-aligned at slide cx 177.0 on BOTH frames (28:
  56.6..296.9; 29: 51.4..303.1) — drawn center-aligned; lines 2-3 inherited
  byte-identical (no diff rows).
- Chips 9/10/11: component polar rule verified ≤1.1pt (k=8 control identical
  between frames) — no overrides.
- 11 arcs (k=0..10), NO arc 11: pale-stroke census empty at 342-358.5° beyond the
  axis baseline (22 px vs 21 px on 028), head-11 window n=0, no label. The spec's
  "12 arcs / Word 11→Word 0" is frame-overridden (SOURCES.md had flagged it `[?]`).
- Arrowheads 8/9/10 (slide pt): (576.2,522.7) (689.1,493.4) (777.0,408.7) —
  hand-placed vs polar up to 4.8pt, same law as 028's k=5/k=6.
- `+ω` labels: k=7 MOVED to (414.2,479.6) — 028's (372.7,489.2) spot is GRAY on
  this frame (pixel-probed; only the panel border column there); k=8 (530.3,523.7),
  k=9 (642.8,527.0), k=10 (749.4,489.2). Labels 0-6 unchanged (no diff rows).
- NEW callout (bottom-left): white rect, C00000 2pt border, slide
  (48.24, 409.7, w 311.0, h 124.3); text Arial bold 16.75pt centered at cx 203.2:
  L1 "Using smaller ω value, allow" (blue 0000CC; "smaller" over a yellow FFFF00
  band slide (141.9,416.5,57.2,17.8); the ω glyph RED CC0000 — measured frame cols
  216-228), L2 "representation of longer sequences" (blue), L3
  "(practically use  ω = 1/10000)" (red CC0000, verbatim double space). Ink bands
  slide y 419.6/438.5/476.2 (pitch 18.9pt; one blank pitch before L3).
- Badge numeral 29 via the certified chrome chain; mouse cursor at Word 2 (frame
  ~(677,156)) omitted per GROUND RULES (c); 028's cursor absent (base has none).

## Deviations from the frozen procedure (documented)

- `--thinking high` could not be passed: the installed analyze_image.py (skill v1.6,
  owner amendment 2026-10-11) REMOVED the flag and bakes reasoning at effort LOW.
  `--max-tokens 65536` was passed as mandated. The same script version certified
  slides 027/028. Noted in `judge_prompt_1.txt`.
- Judge procedure executed by the worker via Bash (no Agent/Task spawn tool in this
  environment) — orchestrator-approved fallback per 17_worker_instructions §7.
- The probe found the spurious left stroke (see self-check fix 2) — fixed BEFORE
  the crop comparisons and the judge ran; all vision evidence is on the final build.

## Dependency obligations

- `slide_dependencies.json`: nothing depends on 29 (only edge `29 ← 28`), so the
  component-banking trigger (rule 2) does NOT fire. The build is component-ready on
  demand: its draw is already `renderBase(...)`-shaped with per-block functions.
- No certified component was edited (cascade law honored).

## Evidence inventory (qa/slide029/)

`render_1.png` · `build_attempt_1.js` · `judge_prompt_1.txt` · `probe_1.txt` ·
`selfcheck_attempt_1.py` / `.txt` · `crop_callout_{render,orig}_1.png` +
`crop_callout_1.txt` · `crop_bottomsector_{render,orig}_1.png` +
`crop_bottomsector_1.txt` · `crop_title1_{render,orig}_1.png` + `crop_title1_1.txt`
· `judge_attempt_1.txt` · this report. Measurement campaign under
`scratch/slide029/` (measure1-5.py + outputs, head_orientation.py, make_crops.py,
render/, lo_profile/, crops/).

## DB state (final)

gen_status=passed · visual_check=PASS · visual_attempts=1 ·
visual_transcript=videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide029/judge_attempt_1.txt ·
pptx_path=videos/deep-learning/002_transformers_part2/recreated_pptx/slide_029_recreated.pptx ·
build_script=videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_029.js
