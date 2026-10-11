# Worker report — slide 006 "Traditional RNN  Seq2Seq model"

Video: `videos/deep-learning/001_transformers_part1` · Worker: per-slide build worker (subagent)
Date: 2026-10-11 · FINAL VERDICT: **PASS** (judge attempt 2, real comparison transcript)

## Deliverable

- `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_006_recreated.pptx`
  (single-version law — no suffixes; no equations → no OMML pass; no advanced graphs → no graphgen pass)
- Build script: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_006.js`
- **Shared components (certified, for children 7/8/9/10):**
  - `videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_006.js`
    — exports `renderBase(pptx, slide, opts)` at BLOCK granularity (27 blocks: dec_*, enc_*,
    ctx_arc, leader, callout, captions, title) plus `opts.skip` / `opts.only` selectors and
    exported `BLOCKS` / `C` (palette) / `GEO` (geometry). Children must require() it — never
    re-derive geometry.
  - `videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/house_chrome.js`
    — DELEGATES to the playlist-certified shared pattern
    `videos/deep-learning/shared_patterns/house_chrome.js` (CHROME constants +
    `drawHouseChrome(pptx, slide, {numeral})`), per the 2026-10-11 playlist chrome law
    (founder directive received mid-build and applied: white canvas, E9E9E7 panel
    x42..918 y45..bottom with C00000 border, badge d36px @ (893,71) FDFD96/6A5ACD + numeral 6).
  - Curve assets (600dpi transparent PNGs, exact-size embeds):
    `recreated_pptx/build/assets/curve_a.png`, `curve_b.png` (decoder recurrent sweeps,
    measured quadratic beziers), `ctx_arc.png` (red context-vector arc + arrowhead wedge).

## Geometry provenance

All content geometry PIL-measured from `unique_slides/slide_006.jpg` (960×540, 1px=1pt,
in=px/72): exact color modes per region, scanline run-length structure (4 cells per bar,
divider positions at quarter marks), ink-component bboxes for every label/arrow, and
quadratic-bezier fits for the three curved strokes. Measurers banked in
`scratch/slide006/measure*.py` (7 scripts) + `gen_curves.py`.

## Attempts

- **Attempt 1** — build + render + self-checks: 3 font-size calibration iterations
  (math labels 13→17pt w/ 12pt subscripts, captions 18→20.5pt, callout 14→15.5pt —
  driven by ink-width ratio vs original), then judge comparison
  (`qa/slide006/judge_attempt_1.txt`): coherent body, recreation judged better with all
  deviations MINOR, but the model omitted the mandated literal `FINAL VERDICT:` line →
  not certifiable by itself; re-ran as attempt 2.
  Pre-probe: gateway window initially HangError'd twice (fleet busy with sibling
  workers); per judge procedure slept 300s and re-probed once → window opened
  (`probe_1.txt`, full valid body).
- **Attempt 2** — same render (no rebuild; banked `judge_prompt_2.txt` instructs the
  literal verdict line in --view), comparison
  (`qa/slide006/judge_attempt_2.txt`): **FINAL VERDICT: PASS**.

## Judge findings (attempt 2) and dispositions

| # | Finding | Severity | Disposition |
|---|---|---|---|
| 1 | Panel body: uniform E9E9E7 in render vs gray-band/white-body look in frame | minor | Playlist chrome law (founder 2026-10-11) fixes the panel; frame's mid-body whiteness is projector vignette (measured: #fff0e7 mid-rows vs #e6e6e8 edges). OVERRIDDEN BY LAW — not a fix trigger. |
| 2 | Decoder feedback-curve direction (arcs above vs "dip below") | minor | Judge variance on 1px-stroke features: the ∩ sweeps above the green bars ARE measured in the frame (dome apex y≈188, land on next hidden-bar top edge) AND the below-bar tails are drawn too (diag strokes at 653,276→669,291 / 784,276→800,291). Both features present in both images. |
| 3 | Callout text bold-upright vs italic | minor | Validated spec says bold sans-serif (typography_notes + brief step 22); numeric stem-slant probe inconclusive ('C' has no straight stem). Spec stands. |
| 4 | x-label up-arrows "faint/absent" in original | — | Mine draws them per spec brief step 20 (present in original, JPEG-washed). Faithful. |
| 5 | Panel scale/proportions eyeball note | minor | Geometry is pixel-matched (containers within 1-2px of measured bboxes); judge eyeball variance. |
| 6 | Green tick marks near s1/s2 | — | Those are the measured below-bar diagonal tails — present in frame; faithful. |

## Pre-judge self-checks (all PASS, banked)

- `house_chrome_check.py` → PASS (panel x 89-1913, y 95-bottom; badge center (1860,148) d=70, tol 8)
- `qa/slide006/selfcheck_attempt_1.py` + `selfcheck_attempt_1_out.txt` → ALL PASS:
  7 fill-color samples exact vs frame; 2 red dots reddish; 12 text ink bboxes within
  ±4px of frame positions AND 10 ink widths within ±8px; 15 arrow/curve/divider ink
  presence points; no content bleed outside the panel.

## Evidence files

- `qa/slide006/render_1.png` (150dpi render), `build_attempt_1.js`, `build_attempt_2.js`,
  `build_attempt_1_components_slide_006.js`, `build_attempt_2_components_slide_006.js`
- `qa/slide006/judge_prompt_1.txt`, `judge_prompt_2.txt`
- `qa/slide006/probe_1.txt` (probe body), `qa/slide006/judge_attempt_1.txt` (attempt-1 body),
  **`qa/slide006/judge_attempt_2.txt` (certifying comparison — FINAL VERDICT: PASS)**
- DB: gen_status=passed, visual_check=PASS, visual_attempts=2,
  visual_transcript=videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide006/judge_attempt_2.txt

## Notes for the orchestrator

- Children 7/8/9/10 are UNBLOCKED as of this certification (verified via
  `15_progress.py deps`). They should `require('./components/slide_006')` and draw only
  their deltas; house chrome comes from `components/house_chrome.js` (do NOT re-draw).
- Judge procedure executed by the worker via Bash (no Agent/Task spawn tool in this
  environment) — orchestrator-approved fallback, noted per 17 §7.
- Verbatim-text laws honored: double space in title ("Traditional RNN  Seq2Seq model")
  and in "Encoder  (RNN)"; true subscripts via 12pt subscript runs; mouse-cursor artifact
  omitted per spec.
