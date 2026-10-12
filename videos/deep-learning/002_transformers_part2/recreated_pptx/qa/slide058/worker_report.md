# Worker report — slide 058 "Transformer Encoder as a Classifier" (002_transformers_part2)

## Summary

- Slide: 58 (NNN=058), video 002_transformers_part2, ROOT slide (no dependencies,
  no pattern group). No dependents in any video's graph (checked
  `slide_dependencies.json`) → no component-banking obligation.
- Attempts used: 1 of 6. Final verdict: **PASS** (real vision comparison, attempt 1).
- Deliverable (single version): `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_058_recreated.pptx`
- Build script: `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_058.js`
  (attempt-1 copy banked: `qa/slide058/build_attempt_1.js`)
- Comparison transcript: `qa/slide058/judge_attempt_1.txt` (probe: `qa/slide058/probe_1.txt`)
- DB: gen_status=passed, visual_check=PASS, visual_attempts=1, visual_transcript set,
  build_script/pptx_path set. VIDEO=deep-learning/002_transformers_part2.

## What the slide is

Section divider: two-line red bold title "Transformer Encoder" / "as a Classifier",
house chrome (gray E9E9E7 panel + C00000 border, badge numeral 58), nothing else.
Provenance was BANKED pre-dispatch (`slide_058_source/SOURCES.md`): course-authored
divider, BERT topic anchor only, cursor + letterbox flagged as artifacts.

## Build decisions (measured, documented in the build header)

- **Mapping**: capture geometry identical to the certified slide-002 frame (top
  stroke row 42/750px; badge yellow bbox center 875.5,70.5 in both) → adopted the
  certified slide-002 fit verbatim: `frame_x = 18.63 + 0.96123·slide_x`,
  `frame_y = 0.95556·slide_y`. Badge cross-check: →(891.4, 73.8) vs house
  (893, 71) = d(−1.6, +2.8) px, within ~3px. An independent 4-landmark least-squares
  fit (left 58.5 / right 902 / top 42 / bottom 516) agrees within ≤1 slide pt.
- **Title**: two SINGLE-LINE center-aligned boxes (Arial Bold 48.5pt, C00000) pinned
  to each line's MEASURED ink center/top: L1 cx 459.69pt ink-top 239.65pt; L2 cx
  474.26pt ink-top 295.11pt. The two lines' ink centers are NOT coincident (Δ14.6pt)
  and neither is at slide center — reproduced as measured (slide-002 L3 precedent).
  em fitted from real `/usr/share/fonts/TTF/Arialbd.TTF` PIL ink bboxes (word-level
  46.9–48.7, mean ~48.2; closed loop confirmed 48.5 lands inside tolerance).
- **Title color**: C00000 — frame core census (158,13,28) matches the certified
  C00000 slide-002 title read under the identical census (163,13,29); luma analysis
  (Y=60 vs C00000's 57; B22222 would be 77) rules out the spec's #B22222 estimate [?]
  (JPEG chroma desaturation on thin strokes; luma preserved under 4:2:0).
- **Omitted as capture artifacts** (ground rule (c); spec imagery/animation_state
  and SOURCES.md agree): presenter cursor at frame ~(650..660, 270..281); black
  letterbox strip rows 518..539 (maps to slide y ≥ 542.3, below the 540pt bottom).
- **Chrome**: `shared_patterns/house_chrome.js` `drawHouseChrome(pptx, s, {numeral: 58})`
  — badge/chrome values are house-locked (spec's #8B1A1A border / #F5F27D+6C5CE7
  badge estimates superseded; validation.uncertain_items flags them as estimates).

## Pre-judge self-check (mandatory, attempt-1 render `qa/slide058/render_1.png`)

- `house_chrome_check.py`: **PASS** (panel x 89–1913, badge (1860,148) d=70, tol 8).
- `selfcheck_attempt_1.py` / `selfcheck_attempt_2.py` (row-run separated, mask-to-mask,
  same thresholds both images): L1 d(L/R/T/B) +2.7/−3.0/+1.5/−0.9 px; L2
  +1.8/+0.1/+0.9/−1.5 px — all within ~4px @150dpi → **PASS**. Containment inside
  panel interior ✓; badge numeral ink present ✓; no black strip ✓; no cursor blob ✓.
- Patterns index read first: house-chrome applies (used); equations/delimiters/
  tables/multi-line-box patterns n/a (divider has none; no explicit lineSpacing
  needed — two single-line boxes).
- (First check script had overlapping measurement bands producing false L2 FAIL;
  fixed with row-run separation — measurement bug, not a build defect.)

## Judge (attempt 1)

- Banked prompt: `qa/slide058/judge_prompt_1.txt` (frozen `-p` template with ground
  rules, verbatim). Executed by the worker via Bash (no spawn tool in this
  environment — orchestrator-approved fallback).
- Probe: valid body (window open). Note: the template's script path
  `.agents/image-analysis/scripts/analyze_image.py` is stale in this workspace; the
  real path per SKILL.md is `.agents/skills/image-analysis/scripts/analyze_image.py`
  — used for both probe and comparison.
- Comparison (`--thinking high --max-tokens 65536`, W4 wall 540s, timeout 420):
  real winner body, element-by-element, "None found" discrepancies, cursor +
  letterbox handled under ground rules (b)/(c).
  **FINAL VERDICT: PASS** for "faithful, usable recreation".
- Transcript: `qa/slide058/judge_attempt_1.txt`.

## Notes

- OMML wrap: n/a (no equations). Graph generation: n/a (no advanced graphs).
- Storm events: none encountered (no provider errors, no retries needed).
- Scratch: `scratch/slide058/` (measurement scripts, render_a1, LO profile);
  TMPDIR redirected for soffice + vision gate (/tmp blocked per contract).
