# Worker report — slide 017 "The Complete ML Classification Process" (001_introduction, Deep Learning DSAI 308) — GRANDCHILD 17←16←9

## Verdict chain

1. **Collision protocol (dispatch mandate)**: pre-mutation sweep found a LIVE PEER —
   `qa/slide017/` measurement forensics written up to 08:08:36 (delta_diff.py,
   measure_title/apply*.py, delta crops), DB row `gen_status=building` (07:57:33), no
   build script / pptx / scratch. Stood down READ-ONLY; did independent in-memory PIL
   delta measurements while waiting. Took over after **43 min peer silence + zero
   artifact movement + mid-state row** (08:51). The prior worker's banked forensics in
   `qa/slide017/` (measure_*.py, delta_diff.py, crop_*.png) were preserved untouched.
2. **Dep gate**: `15_progress.py deps` → slide 17 `unblocked`; parents CERTIFIED in this
   video's DB — 16 (gen_status=passed, visual_check=PASS, banked component) and
   transitively 9 (passed/PASS, banked component).
3. **Component chain verification (throwaway)**: `scratch/slide017/chainverify/verify.js`
   requires `components/slide_016.js` (which itself requires `components/slide_009.js`)
   by absolute path, calls `renderBase` with the documented opts contract (numeral 17 +
   delta skips) → pptx written (`chain_verify.pptx`). Chain loads.
4. **Build (attempt 1)**: `recreated_pptx/build/slide_017.js` — IMPORTS the certified
   components; never re-derives/copy-pastes parent geometry:
   - `P9.renderBase(skip:[title, training_ellipse, box_pre, box_post, arrow1, curve1,
     curve2, final_ellipse, label_*], numeral:"17")` → chrome (numeral 17) + panel +
     blackbar + box_extraction/selection/classification + arrows 2-4;
   - `P16.DELTA_BLOCKS` inherited pixel-identical: training_ellipse_016, box_pre_016,
     arrow1_016, curve1_016, box_classifier_output_016 (pixel-diff 017 vs 016 outside
     the delta zones <6 stray px proves these regions identical);
   - measured 017 delta only: title_017 ('ML' navy 000080, ink-core darkest-20%
     (0,0,115); spec #0000CC loses to ink), callout_inspection_017 (85,355,194,39),
     callout_handcrafted_017 (281,400,152,58), callout_decision_017 (435,346,140,58),
     callout_apply_017 (613,283,86,39, single-line "Apply Model"),
     star_trained_model_017 (star16 at 709,265,166,74; fill FAFEDB modal (250,254,219);
     text 11pt bold red pitch 13), divider_017 (dashType 'dash' w1 at y334, x77..858),
     star_human_experience_017 (star16 at 624,358,200,57; fill FFFFFF; text 12pt bold
     navy pitch 13.5). Divider drawn LAST (crosses the starburst's bottom spike tips —
     measured red dash px inside the star's x-range in the original).
   - Font metrics calibrated with PIL/Liberation-Sans-Bold (Arial metrics): "Trained
     Model!" @11pt = 77.6px vs measured 79; "Human Experience" @12pt = 108.0 vs 108;
     "Apply Model" @14pt = 83.2 vs ~80 (certified callout size).
5. **Render**: soffice headless (private profile `-env:UserInstallation`, TMPDIR=
   `scratch/slide017/tmp` — /tmp quota workaround) → pdftoppm 150dpi →
   `qa/slide017/render_1.png` (2001x1125).
6. **Pre-judge self-checks (attempt 1, ALL PASS)**:
   - `shared_patterns/house_chrome_check.py`: **PASS** (panel x 89-1913, y 95-bottom;
     badge center (1860,148) d=70; tol 8).
   - `qa/slide017/selfcheck_attempt_1.py` (+ banked output): **ALL PASS** — title
     red/navy ink bboxes, callouts A-D stroke geometry + text bands, starburst outline/
     fill/text bands, divider band/edges/duty (render duty 0.55 vs original 0.57),
     frame containment of every delta element, and **inherited regions pixel-equal to
     the certified slide-016 render (0 stray diff px outside delta+badge zones)**.
     One DOCUMENTED ACCEPTED ARTIFACT: star16 spike-tip fill sliver (fill-left 712 vs
     JPEG-thresholded 722; outline geometry exact — ground rule (d) medium difference).
     Build-fix history: divider originally sysDash w2 measured dash 13px/gap 4px duty
     0.74 vs original 8.3/4.2 duty 0.57 → switched to 'dash' w1 (dash 8.3/gap 6.25,
     duty 0.55) — one closed-loop iteration; all other initial check failures were
     checker-window contamination (panel border cols, badge ring, Classifier-Output
     box bottom, neighboring callout strokes) diagnosed against actual pixels and
     fixed in the CHECKER only.
   - **Dense-region crop comparison** (mandatory item 6; annotation band x60..890,
     y255..470, 2x upscale): `cropcmp_attempt_1.txt` — **FINAL VERDICT: PASS** (no
     overflow/clipping/wrapping; vertical centering, callout stagger, divider-to-
     starburst crossing all reproduced).
7. **Judge attempt 1** (executed by worker via Bash per the banked prompt in
   `judge_prompt_1.txt`; no spawn tool in this environment — orchestrator-approved
   fallback, 17_worker_instructions.md §7):
   - Probe: `probe_1.txt` (valid analysis body; gateway window open).
   - Comparison: `judge_attempt_1.txt` — real, coherent winner body, `--thinking high
     --max-tokens 65536`, `--timeout 420` inside W4 540s wall (outer `timeout 1700`
     per dispatch), frozen ground rules banked in `judge_p_payload_1.txt` (numeral 17,
     dependency-inheritance rule (f) with the five delta facts, cursor/letterbox
     artifact rule, star16/dash medium-difference coverage), sourced via
     `-p "$(cat judge_p_payload_1.txt)"`. Streaming default route (no --models flag).
   - **FINAL VERDICT: PASS** — zero BLOCKER/MAJOR; no missing elements (rule 6 clean),
     arrow geometry clean (rule 7), flowchart data clean (rule 8), frame containment
     clean. 3 MINOR, all rule-covered: (1) preset dash vs hand-drawn dashes (rule d-ii),
     (2) star16 vs irregular hand-drawn spikes (rule d-i), (3) observation that both
     images show the black bottom strip (rule (c) note; not a fidelity mismatch).
   - Certificate label: single-read, default route (images), glm leg DEFERRED/BLOCKED.

## Final state

- **Final verdict: PASS on attempt 1 of 6** (plus a rule-covered MINOR-only ledger).
- Deliverable (single version, plain name): `videos/deep-learning/001_introduction/recreated_pptx/slide_017_recreated.pptx`
- Build script: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_017.js`
  (provenance copy: `qa/slide017/build_attempt_1.js`)
- **No component banked**: slide 17 has no children in `slide_dependencies.json`
  (edges: 16←9, 17←16, 18←9, 19←9, 25←24, 37←36, 41←35) — banking obligation not
  triggered; the dependency graph is unchanged.
- DB (VIDEO=deep-learning/001_introduction, slide 17): gen_status=passed,
  visual_check=PASS, visual_attempts=1, visual_transcript=judge_attempt_1.txt,
  build_script + pptx_path set. Slide 17 has no dependents — no cascade.
- Transcripts: `probe_1.txt`, `cropcmp_attempt_1.txt`, `judge_attempt_1.txt`; prompt
  banked as `judge_prompt_1.txt` + `judge_p_payload_1.txt`; self-check
  `selfcheck_attempt_1.py` + `selfcheck_attempt_1_out.txt`; chain-load verification
  `../../scratch/slide017/chainverify/`.
- Prior worker's forensics preserved untouched in this dir: `delta_diff.py`,
  `measure_title.py`, `measure_apply.py`, `measure_apply2.py`, `crop_*.png`
  (written 08:02-08:08 before the takeover).

## Documented delta vs parent 16 (all PIL-measured on slide_017.jpg; scripts in qa/ + scratch/)

| # | Element | Parent 16 (certified) | Slide 017 (measured) | Mechanism |
|---|---|---|---|---|
| 1 | title | all-red 26pt (certified 9 geometry) | same geometry; 'ML' NAVY 000080 (ink core (0,0,115)) | own block, parent metrics, 3 runs |
| 2 | callout inspection | (85,291,194,41) | (85,355,194,39) — shifted DOWN +64 | own block, parent style |
| 3 | callout handcrafted | (280,336,154,60) | (281,400,152,58) — moved down +64, 2px narrower | own block, parent style |
| 4 | callout decision | (435,282,140,60) | (435,346,140,58) — shifted DOWN +64 | own block, parent style |
| 5 | callout apply | (612,282,89,41) 2-line | (613,283,86,39) SINGLE-line "Apply Model" | own block, parent style |
| 6 | starburst Trained Model | — | star16 (709,265,166,74), FAFEDB + C2C4C2 w1, red 11pt text | new block (deck star16 mechanism) |
| 7 | dashed divider | — | y≈334, x77..858, C00000 'dash' w1, OVER starburst spikes | new block |
| 8 | starburst Human Experience | — | star16 (624,358,200,57), FFFFFF + C2C4C2 w1, navy 12pt text | new block (deck star16 mechanism) |
| 9 | chrome numeral | 16 | 17 | opts.numeral |
| — | chain (ellipse, boxes, arrows, curve) | pixel-identical to 016 | inherited via P16.DELTA_BLOCKS | import |
