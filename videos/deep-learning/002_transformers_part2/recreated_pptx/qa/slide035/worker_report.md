# Worker report — slide 035 "Building Transformer Block" (002_transformers_part2)

## Outcome

- **Final verdict: PASS** (visual judge, attempt 1, single-read default route `images`,
  glm leg DEFERRED/BLOCKED per routing law).
- Deliverable: `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_035_recreated.pptx`
- Build script: `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_035.js`
- Comparison transcript: `videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide035/judge_attempt_1.txt`
- Probe transcript: `videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide035/probe_1.txt`
- Banked per-attempt provenance: `judge_prompt_1.txt`, `build_attempt_1.js`, `render_1.png`
- DB row: gen_status=passed, visual_check=PASS, visual_attempts=1.

## Attempts used

1 (PASS on the first judge dispatch; no fix iterations needed).

## Content and construction

- Spec: `analysis/slide_035_final.json` (PASS_WITH_FIXES) — verbatim text:
  title "Building Transformer Block"; "Adding" + "Residual Connections" /
  "Layer Normalization" / "Feed Forward Network". No equations/tables/figures
  (SOURCES.md confirms: text-only transition slide; paper 1706.03762v7 §3.1/§3.3
  names the three constructs).
- Chrome: shared `videos/deep-learning/shared_patterns/house_chrome.js`
  (`drawHouseChrome(pptx, slide, {numeral: 35})`); `house_chrome_check.py` PASS
  (panel x 89–1913, y 95–bottom; badge center (1860,148) d=70; tol 8).
- Frame→slide mapping (derived from THIS frame's chrome landmarks — left border
  col 59, right ~902, top ~43, bottom 516; identical to certified slide_002):
  `frame_x = 18.63 + 0.96123·slide_x`, `frame_y = 0.95556·slide_y`. Badge
  cross-check: frame badge yellow-fill center (875.5, 71.0) → slide (891.4, 74.3)
  vs house (893, 71) — within ~3px (fill bbox excludes the purple ring).
- Measured ink (mapped to slide pts): title cap top 163.8 / baseline 199.1,
  bbox cx 476.3 (genuinely ~3.7pt left of slide center — reproduced as measured);
  "Adding" asc top 306.1 / baseline 332.3, ink L 105.4; list lines cap tops
  356.4 / 397.1 / 436.9, ink L 202.2, baseline pitch 39.7pt. Sizes from Arial
  Bold advance fits: title 48.5pt, list 35pt, "Adding" 34pt.
- Colors: title C00000 (measured core (185,7,24)); body 0000A8 — MEASURED
  CORRECTION of the spec's #1A1AB8: deep-core census (4,0,149)..(5,0,165) with
  R=G=0 rules out R=G=26; per the measured-color law (certified 039 precedent).
  Five single-line text boxes at measured positions (certified slide_002
  pattern; no multi-line auto-pitch anywhere).
- Omitted per judge ground rule (c): mouse cursor at ~frame (365,400) over
  "Layer Normalization"; black letterbox strip (frame rows 519–539, below the
  slide bottom under the mapping).

## Pre-judge self-checks (all banked under scratch/slide035/)

- Patterns index read; house-chrome pattern used; no other pattern applies
  (no equations/delimiters/tables/graphs on this slide).
- `house_chrome_check.py`: PASS.
- Closed-loop PIL (`closed_loop.py`, `closed_loop_attempt1.txt`): PASS — title
  dL +2.7 / dR −3.3 / capTop −1.2 / baseline −1.8; Adding dL −2.6 / base −4.2;
  L1 −1.3/−2.9; L2 −1.3/−0.8; L3 −3.3/−0.5 (all px @150dpi, tol ~4).
- Containment/wrap/badge (`selfcheck_containment.txt`): PASS — no ink outside
  bands, 0 stray px between title and list and below list, badge numeral ink
  present (482 px).
- Equations/delimiters/tables: N/A (none in spec).
- Dense-region crop comparison: N/A (no equations, multi-line delimiters, or
  tables — the mandatory-crop trigger does not fire on this 5-line slide).

## Judge findings (attempt 1)

- 3 × MINOR, 0 MAJOR, 0 BLOCKER:
  1. Body block ~0.02 image-fractions lower/left in IMG1 vs IMG2 (medium conf).
  2. List pitch ~0.075 vs ~0.072 of image height (~4%, low conf).
  3. Body font "marginally larger/bolder" (low conf).
- Assessment: MINOR #1 is the zoomed-out-frame artifact — fractions-of-IMAGE
  between IMG1 (true 960pt slide) and IMG2 (0.958-scale capture with +18.63px
  offset) differ by construction (offset 18.63/960 ≈ 0.019 ≈ the reported
  delta); the physical geometry is the chrome-landmark-fitted mapping,
  closed-loop verified. #2/#3 are within the closed-loop tolerances. Not fix
  triggers; documented here per the variance law.
- Judge note: the probe transcript's observations (bottom border flush, badge
  near border) are house chrome; the comparison settled them under ground rule
  (a). Judge procedure executed by the worker (no spawn tool in this
  environment; orchestrator-approved fallback). Script path corrected to
  `.agents/skills/image-analysis/scripts/analyze_image.py` per the skill's
  2026-10-11 location amendment; template otherwise verbatim.

## Component banking

Slide 35 has no dependents in any video graph (deps view: root, no children) —
no component export obligation.
