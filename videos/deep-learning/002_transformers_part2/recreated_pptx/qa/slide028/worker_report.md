# Worker report — slide 028 (002_transformers_part2, Deep Learning DSAI 308)

Dispatch: build worker, sole owner. Ground truth `unique_slides/slide_028.jpg`
(960x540, founder frame-swap mid-group — frame on disk canonical). Spec FINAL
`analysis/slide_028_final.json` (PASS_WITH_FIXES, score 9). Deps 28 ← [27, 26], both
certified in this deck's DB at dispatch time.

## RESULT

- **gen_status=passed, visual_check=PASS, visual_attempts=1** (single judge attempt).
- Deliverable (single-version law): `recreated_pptx/slide_028_recreated.pptx`
- Build: `recreated_pptx/build/slide_028.js`
- Judge transcript of record: `recreated_pptx/qa/slide028/judge_attempt_1.txt`
  (FINAL VERDICT: **PASS** for 'faithful, usable recreation'; no BLOCKER/MAJOR;
  3 MINOR findings, all on INHERITED certified regions — see "Judge findings").
- Component banked (dependents 29 ← 28, 45 ← 28):
  `recreated_pptx/build/components/slide_028.js` — renderBase(pptx, slide, opts)
  (opts: numeral/wordCount/skip), **0-pixel-diff verified** vs the certified render
  (0 of 2,251,225 pixels differ; `qa/slide028/verify_component_0diff.txt`).

## DUPLICATE-WORKER INCIDENT (orchestrator-coordinated)

A second builder for slide 028 from the pre-interruption fleet was ALIVE during this
run (foreign measurement files in `scratch/slide028/`: probes 04:49–05:09, measure1–4
06:08–06:18, measure5 06:35:50; idempotent DB touch 06:46:41; no build/pptx/qa/DB
field writes). Per the orchestrator's directive I stood down READ-ONLY for ~65 min
and took over only on the dual condition (peer quiet ≥40 min on both clocks AND zero
new artifacts AND DB mid-state; met 07:29). The peer's banked measurements were
independently cross-verified and used as corroborating evidence (never deleted):
heads k=4..7, labels k=4..7 (its measure4/measure5.json are the source of the delta
label values; my re-measurements agree within 1.5pt). My own measurements:
`scratch/slide028/measure5_mine -> measure6_mine.py/.json` (chips, diff bands),
`measure_28_vs_27.py`, `sample_colors.py`, crops `lr_*.png`, `bl_028.png`.
Judge procedure executed by worker; no spawn tool available (orchestrator-approved
fallback); the verdict is taken verbatim from the banked comparison winner body.

## Build (dependency law)

- `require`s slide 027's CERTIFIED component (composition base: chrome + circle +
  spokes + chips 0..4 certified measured centers + eqbox) and slide 026's CERTIFIED
  component (founder edge 28←26: zero of its blocks appear on this frame — expressed
  as `renderBase(pptx, slide, { only: [], chrome: false })`, the full-removal delta).
- Chips 5..8: parent's polar rule verified ≤1.7pt against this frame → no overrides.
- Delta: title line 1 "Sequence of 9 words" (5→9, same certified boxes — drawn by
  `drawTitleDelta` because `renderBase`'s `opts.titleLines` is a dead option in the
  certified 027 component, never forwarded to `drawTitle`; measured diff band confined
  to the digit glyph, frame cols 225–228); arcs 4..7 (family polyline rule arcR 224 /
  pads 12,1.5 / 14 segs / F0C9B0 0.75pt) with MEASURED arrowheads (k=4,7 on the polar
  rule; k=5,6 hand-placed 4.5–5.2pt above it) and MEASURED '+ω' label centroids
  (deviations from the polar auto-rule up to 24pt — labelsMeasuredDelta); badge 28.
- Mouse cursor near Word 1 (this frame) and at circle center (frame 27) = capture
  artifacts, correctly omitted (GROUND RULES (b)/(c)).
- No equations needing professional-format rendering (the Sin(ω t)/Cos(ω t) box is
  linear text in the ORIGINAL — professional format == this text, per 027 precedent).
- Fixed during attempt 1 (caught by render inspection + pptx XML audit before any
  judge call): (1) delta geometry multiplied by the IN *function* instead of its value
  → NaN → pptxgenjs 1in/0in defaults (giant triangle + stray giant "+ω"); (2) the
  dead `titleLines` option (above).

## Pre-judge verification (all banked in qa/slide028/)

- `house_chrome_check.py` on render_1.png: **PASS** (panel x 89–1913, badge center
  (1860,148) d=70, tol 8).
- `selfcheck_attempt_1.py` + `.txt`: **PASS, 25/25** — frame containment (ink bbox
  inside panel), eqbox ink present, heads k=4..7 d ≤1.3px, chips k=5..8 d ≤1.0px,
  labels 0..7 apples-to-apples orig-vs-render ink d ≤4.2px (certified 0..3 show the
  same 2.6–4.2px behavior as delta 4..7 at 1.2–3.4px), title 3 lines + line-1 ink
  match (d ≤2.6px), arcs 4..7 present, title/eqbox wrap clean. Two self-check
  artifacts were diagnosed and fixed method-wise (centroid-vs-bbox mismatch; panel
  border contaminating tall search windows) — both documented in the script.
- Dense-region crop comparisons through the gate (item 6): `crop_eqbox_1.txt` PASS
  (1 MINOR: box padding fractionally tighter, sub-pixel at 1x, inherited certified
  geometry); `crop_bottomleft_1.txt` PASS (3 MINOR: faint delta arc extent — the
  family's certified "stroke below JPEG noise floor, do NOT thicken" convention;
  circle-ring stroke slightly heavier — inherited; ω glyph width — font rendering).

## Judge (attempt 1)

- Probe: HungError ×2 (150s / 270s walls; gateway congestion, other workers in
  flight) — proceeded to the comparison per the evidence law (the comparison IS the
  evidence; probe only opens the window).
- Comparison: `judge_attempt_1.txt` — coherent element-by-element body, GROUND RULES
  honored (artifacts omitted per (b)/(c)), FINAL VERDICT: **PASS**.

### Judge findings and dispositions

1. MINOR (~65%) "Sin(ω t) ink color dark red vs blue" — INHERITED: the eqbox is
   slide 027's certified block with PIL-verified per-glyph colors ("Sin(" blue, "ω"
   red, " t" green, ")" blue) and pixel-identical geometry here (no diff band at the
   eqbox in the 27↔28 frame census) → judge variance, overridden per the
   inheritance law.
2. MINOR (~80%) spokes pale pink vs more visible red — INHERITED: certified 027
   spoke constants (993333 @ 75% transparency), judge-verified on 027 → judge variance.
3. MINOR (~50%) vertical axis faint pink — INHERITED, same disposition.
4. Crop MINORs (above) — same dispositions; the delta-arc faintness is the certified
   family convention (founder law: do NOT thicken or dash the arc stroke).

No findings on this slide's delta (title digit, chips 5..8, arcs 4..7, heads/labels,
badge). No fix triggers. Cert label: single-read, default route (images), glm leg
DEFERRED/BLOCKED.

## Evidence inventory (qa/slide028/)

render_1.png · build_attempt_1.js · judge_prompt_1.txt · probe (none banked — both
probe calls HangErrored without transcript) · selfcheck_attempt_1.py/.txt ·
crop_eqbox_1.txt · crop_bottomleft_1.txt · judge_attempt_1.txt ·
verify_component_0diff.txt · this report. Scratch evidence under
`scratch/slide028/` (measurements, crops, component verify pptx/pdf/png, LO profile).

## Handoff

- Slides 29 and 45 are unblocked by this certification: import
  `videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_028.js`
  (absolute path), call `renderBase(pptx, slide, { numeral: <printed number>,
  wordCount/skip per their frames })`, draw only their measured delta. NEVER edit the
  certified component (cascade law).
