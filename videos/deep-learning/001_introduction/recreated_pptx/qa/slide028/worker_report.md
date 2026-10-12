# Worker report — slide 028 (001_introduction, Deep Learning DSAI 308)

## Summary

- Slide: 28 — "Introduction to Convolutional Neural Network (CNN)" (section-title slide)
- Attempts used: 1 of 6 (judge PASS on first attempt)
- Final verdict: **PASS** — backed by a real comparison transcript through the vision gate
  (`judge_attempt_1.txt`, validated winner, atomic, degenerate events 0)
- Deliverable (single version): `videos/deep-learning/001_introduction/recreated_pptx/slide_028_recreated.pptx`
- Build script: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_028.js`
- DB row: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
  `visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide028/judge_attempt_1.txt`

## Dispatch-facts correction (important)

The dispatch's "SLIDE FACTS" described slide 028 as "Visualization of Single_Layer
Perceptron (equation rows + network diagram with 2-Class / Multi-Class Σ nodes)".
That is slide 22/23's content (DB titles rows 22/23). The actual ground-truth frame
`unique_slides/slide_028.jpg` was PIL-verified before building: three red title bands
(y 119–158 / 235–274 / 293–342), small two-line gray attribution bottom-left, black bar
y 519..539, cursor artifact — i.e. the CNN section-title slide described by
`analysis/slide_028_final.json` (PASSED content gate), the DB row title, and
`slide_028_source/SOURCES.md` (UvA provenance confirmed). No equations exist on the
slide (spec `verbatim_text.equations = []`) → equations/OMML laws N/A. The build follows
the spec JSON + the actual frame; the spec's `validation.fixes` were applied.

## Measured geometry (PIL, 960x540, 1px = 1pt)

- Title line 1 `Introduction to`: ink x 301..660 (center 480.5), ink 119..158, baseline 158
- Title line 2 `Convolutional Neural Network`: ink x 112..847 (center 479.5), ink 235..274, baseline 274
- Title line 3 `(CNN)`: ink x 409..550 (center 479.5), ink 293..342, baseline 331.5
  (paren tail 342 = 331.5 + 0.212em×51.5 — exact; paren top 293 = 331.5 − 0.748em×51.5)
- Attribution line 1 `Some of Slides are picked from`: ink x 99.., rows 467..481, baseline ≈477
- Attribution line 2 `UVA Deep Learning Course   EFSTRATIOS GAVVES`: ink x 93..426,
  rows 485..499, baseline ≈495; Course→EFSTRATIOS gap measured x 265..278 (the spec's
  3-space wide gap, preserved verbatim)
- Black bar: x 38..921, y 519..539 in the original; drawn y 519..537.5 (chrome bottom
  stroke kept visible — same documented 2-frame-px deviation as certified
  slide_002/slide_005/slide_021)
- Constant video chrome (omitted per certified precedent + judge ground rules):
  thin red inset strokes (top y 42, left x 57–59, NO right stroke) — same constant
  lecture-level chrome measured on slides 1/2/5/21/22/49; mouse-cursor artifact at
  x 241..295, y 446..479. The pre-declared playlist house chrome
  (`shared_patterns/house_chrome.js`, badge numeral 28) stands in for the frame element.

## Forensics-driven decisions (ink over spec estimates, per deck AGENTS.md pixel law)

1. **All three title lines Arial Bold 51.5pt** — metric-solved against the real
   Arial Bold TTF: t1 ink 359 vs measured 360, t2 734 vs 736, t3 142 vs 142. Equal cap
   heights (39/39/paren-49) kill the spec's "line 1 ~40pt, lines 2–3 ~48pt" estimates
   (spec uncertain_items concede sizes are estimates); "Introduction to" only LOOKS
   smaller (shorter line).
2. **Title color C00000** — measured modal (176..180, 0, 8..12) is JPEG-darkened C00000
   (G=B≈0 rules out the spec's #A6191E guess); same reasoning as certified slide_005/
   slide_021.
3. **Attribution Arial Italic 14pt #3A3A3A** — metric-solved vs Ariali.TTF (UVA line ink
   331 vs measured 334; the spec's ~12pt would give 284, 50px off). Color 3A3A3A per
   spec (measured thin-stroke lum p05=60 ≈ lightened 3A3A3A).
4. **Attribution as TWO single-line boxes** at the measured left edges (99 / 93) — a
   single left-aligned box would place both lines' ink at the same x, contradicting the
   measured 6px offset. Verticals dead-on at empirical 0 (477.5/496.0 rendered vs
   477/495 target).

## Closed-loop verification (pre-judge, mandatory)

- `house_chrome_check.py` on the 150dpi render: **PASS** (panel x 89–1913, y 95→bottom;
  badge center (1860,148) d=70; tol 8).
- `selfcheck_attempt_1.py` (banked + output banked): **PASS** — title baselines
  158.0/274.0/331.5 EXACT vs targets; ink advances within 5.3 frame-px over 736 (0.7%);
  attribution rows/left edges within 1px; colors exact (canvas FFFFFF, panel E9E9E7,
  bar 000000, title modal exactly C00000=(192,0,0)); containment OK; no stray/wrapped
  ink. Two pre-loop corrections applied (both documented in the build comments):
  (a) initial render wrapped t2 at box w=10in (720px < 734px advance) → boxes widened
  to 12.4in (893px, 1.217× longest advance, wrap-budget law); (b) title baseline landed
  +4.8px low (model error) → empirical 4.8 on all three title lines.
- Dense-region crop comparison (mandate #6; attribution = small text):
  `cropcompare_attempt_1.txt` — **PASS** ("attribution region faithful"), 2 MINOR
  findings: (1) "line-1 indent larger in IMG1 (~15px vs ~6px)" — REBUTTED with PIL
  numbers: rendered left edges 99.9/93.2 vs original 99/93 → indent delta 6.7px vs 6px,
  within 0.7px (the model misjudged at 2x upscale); (2) slight glyph-shape rendering
  differences — inherent typed-vs-source medium difference, at most MINOR per rule (c).
- Probe: `probe_1.txt` — valid body, window opened. The probe's "thin red vertical
  segment through the bar" suspicion was PIL-refuted: zero red pixels in the bar band
  rows 519..537.5; the only red below the bar is row 539.3 = the certified half-visible
  chrome bottom stroke.

## Judge (attempt 1)

- Procedure executed by the worker via Bash (no Agent/Task spawn tool in this
  environment — orchestrator-approved fallback, per scripts/17_worker_instructions.md §7).
- Banked prompt: `qa/slide028/judge_prompt_1.txt`; frozen template with the
  playlist-chrome GROUND RULES prelude (white FFFFFF canvas, gray E9E9E7 panel
  x42..918/y45→bottom, red C00000 border, badge FDFD96/6A5ACD at (893,71) d≈36,
  numeral 28). The `-p` payload was sourced byte-for-byte from the banked file.
- Comparison: `--thinking high --max-tokens 65536`, inner `--timeout 280` inside 1700s
  outer wall through `scripts/16_vision_gate.sh` (TMPDIR redirected to namespace
  scratch — dispatch /tmp-quota directive). Transcript:
  `qa/slide028/judge_attempt_1.txt` — real winner body, no degenerate events.
- Verdict (verbatim from winner body): "**FINAL VERDICT: PASS** for 'faithful, usable
  recreation'." Discrepancies: 2 MINOR, no MAJOR/BLOCKER, no missing elements, no
  containment violations: (1) "faint horizontal gray line at ~68% height in IMG2" —
  REBUTTED with PIL: no such line exists in the original (rows 350–460 show no row
  darker than panel-median−6; the dark rows 443–453 are the cursor, pre-declared
  omitted per rule (c)); (2) title glyphs "very slightly heavier/larger, within
  tolerance" — PIL: advance within 0.7%, baselines exact. Judge ground rules (a)/(c)
  settled the chrome and the omitted cursor; verbatim text matched including the
  3-space gap.

## Evidence files

- `qa/slide028/render_1.png` — the judged 150dpi render
- `qa/slide028/judge_prompt_1.txt`, `qa/slide028/probe_1.txt`, `qa/slide028/judge_attempt_1.txt`
- `qa/slide028/crop_attr_render_1.png`, `qa/slide028/crop_attr_orig_1.png`,
  `qa/slide028/cropcompare_attempt_1.txt` — dense-region crop comparison
- `qa/slide028/build_attempt_1.js` — build provenance for the judged attempt
- `qa/slide028/selfcheck_attempt_1.py` + `selfcheck_attempt_1.txt`
- `scratch/forensics_028_p1.py`, `scratch/forensics_028_p2.py`,
  `scratch/eq_solve_028_fonts.py`, `scratch/measure_028_r1.py` — forensics chain
- `scratch/lo028/` — render scratch (soffice profile at `scratch/lo028_profile`)

## Deviations / notes

1. Dispatch slide-facts text mismatch (see above) — built per spec JSON + actual frame.
2. Spec's recreation_brief step 6 says "do not reproduce the solid black strip" —
   the strip IS part of the captured ground-truth frame and certified precedent
   (slide_002/005/021) draws it; the judge ground rule (6) treats an omitted original
   element as BLOCKER. Drawn (with the documented 2-frame-px bottom deviation);
   documented as a deliberate ink-over-brief decision.
3. Spec's recreation_brief step 3 says one title text box with "paragraph spacing";
   built as three single-line boxes (measured pitches 116/57.5 are non-uniform —
   impossible in one uniformly-spaced box). Spec's recreation_brief step 4 says one
   attribution text box; built as two (measured 6px left-edge offset). Both are layout
   mechanism choices; rendered ink positions match the original within tolerance.
4. Constant video chrome (inset strokes, cursor) omitted — certified-precedent-
   consistent, pre-declared to the judge, accepted.
5. No component banking obligation: slide 28 has no dependents in
   `slide_dependencies.json` (edges: 16←9, 17←16, 18←9, 19←9, 25←24, 37←36, 41←35)
   and no pattern group.
6. OMML wrap / graph-gen passes: N/A (no equations, no advanced graphs).
