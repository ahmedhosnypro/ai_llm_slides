# Worker report — slide 049 "Convnets in practice" (001_introduction, Deep Learning DSAI 308)

Date: 2026-10-12. Fresh start (no prior artifacts). Slide is a dependency-graph ROOT
(no `depends_on`; no slides depend on it → no component-banking obligation).

## Verdict chain

1. Content gate: `analysis/slide_049_final.json` — PASS_WITH_FIXES (validation.fixes applied
   verbatim; verbatim_text is law; `slide_049_source/SOURCES.md` honored — web-verified
   CS231n / d2l.ai corroboration, no content changes needed for the recreation).
2. Pre-judge closed-loop (all banked in this dir):
   - `house_chrome_check.py` on `render_1.png`: **PASS** (panel x 89–1913, y 95→bottom;
     badge center (1860,148) d=70 render-px; within tol 8).
   - `selfcheck_attempt_1.py`: **PASS** — title ink x 253.4..705.1 (orig 252..707), cap-top
     83.3 (84), baseline 116.9 (116.5); box stroke-center 153.5/491.5 × 99.5/860.5 exact;
     8 text bands, tops/bottoms/lefts/rights within ~4 frame-px; underlines
     band1 x 463.0..621.4 (orig 463..621), band4 x 147.4..459.8 (orig 147..458), y +2.5px
     (LO underline offset, inside tolerance); red accents ReLU 331.7..392.2 (334..390),
     max pooling 677.4..805.6 (679..805); 7 black dots within 0.2px; containment strips 0
     stray ink; colors exact (title C00000, body 00008B→renders 000088, border 0000AA).
3. Judge attempt 1 (the only attempt; visual_attempts=1):
   - Banked prompt `judge_prompt_1.txt` = deck-chrome GROUND RULES prelude (white FFFFFF
     canvas, gray E9E9E7 panel x42..918 y45→bottom, red C00000 border, badge FDFD96/6A5ACD
     at (893,71) d≈36 numeral 49, badge-absent-in-original note, black-bar+cursor artifact
     omission) + the FROZEN template from `scripts/17_worker_instructions.md` verbatim.
   - Probe `probe_1.txt`: valid body, window opened.
   - Comparison `judge_attempt_1.txt`: first gate try aborted echo-class GarbageError
     (internal abort+retry 1/3, degenerate events: 1); retry produced a validated winner
     body ending **"FINAL VERDICT: PASS for 'faithful, usable recreation.'"** — verdict
     line `{"page": 1, "verdict": "pass", "issues": []}`. No BLOCKER/MAJOR findings;
     judge explicitly confirmed verbatim text incl. wrap break point, styling
     (bold+underline navy, red ReLU/max pooling, dark-red lead-in), containment, colors,
     and the mandated chrome/artifact handling.
   - Judge procedure executed by the worker (no Agent/Task spawn tool in this environment;
     orchestrator-approved fallback per `scripts/17_worker_instructions.md` §Judge step 7).
     Certificate: single-read, default route (images), glm leg DEFERRED/BLOCKED.
   - Walls per dispatch: `timeout 1700` outer → gate → `--timeout 280 --rounds 1 --tries 1`
     (worker note: the winner's own evidence text narrates the template's W4 line; the
     actual invocation used the dispatch walls).

## Build facts (all PIL-measured from `unique_slides/slide_049.jpg`, 960×540, 1px=1pt)

- Chrome: `shared_patterns/house_chrome.js` imported (numeral 49) — never re-drawn.
  This frame's own panel is x 52..907 (left border x58, washed) vs canonical 42..918 —
  playlist law fixes canonical (slide_040 precedent; judge ground rule (a)).
- Fonts (forensics `font_forensics.py` + ASCII ink crops + underline advance math):
  title **Arial Bold 46.5pt** (word-gap solves self-consistent 46.4/46.6/46.5; Times Bold
  inconsistent 51.0–53.4); body **Times New Roman (Liberation Serif) 25.8pt** (band0 26.1,
  band7 26.05 after closed-loop bump; band4 bold 25.9) — underline constraints dead-on for
  Times (159.1 vs measured 159; 313.4 vs 312), Arial off by 2.4–8px.
- Geometry: box stroke-center x 99.5..860.5, y 153.5..491.5 (fill FFFFFF, border 0000AA 2pt);
  baselines 176.5/216.5/245.5/284.5/325.3/360.5/395.5/431; wrap line of bullet 2 at x 140.7
  (frame shows the wrap 7px LEFT of the text margin — original hanging-indent quirk, frame
  is ground truth); black round dots d 6.75 at measured centers; explicit lineSpacing 30/52.
- Artifacts omitted per spec brief step 15 + ground rule (c): black bottom bar (y 519..539,
  x 38..921), mouse cursor (~893,427).
- No equations (math/OMML laws n/a), no advanced graphs (graphgen n/a), no tables/charts.

## Deliverables & DB

- PPTX (single version): `videos/deep-learning/001_introduction/recreated_pptx/slide_049_recreated.pptx`
- Build script: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_049.js`
- DB: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
  `visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide049/judge_attempt_1.txt`,
  `pptx_path`/`build_script` set, `last_error=null`.

## Deviations / notes

- Underline y sits 2.5 frame-px lower in the LO render than the original (LO underline
  offset ≈0.19em vs PowerPoint ≈0.106em) — renderer-inherent, inside the ~4px tolerance;
  PowerPoint renders the original offset.
- Rendered text widths within ±2px of the original on 6 of 8 lines; band0/band7 needed
  per-line closed-loop size bumps (+0.3pt) to reach exact ink extents.
- No banked evidence was deleted; nothing written outside the video namespace;
  `unique_slides/` and `frames/` untouched.
