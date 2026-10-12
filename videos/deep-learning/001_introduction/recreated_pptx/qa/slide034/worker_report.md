# Worker report — slide 034, videos/deep-learning/001_introduction ("What would a k-D filter looks like?")

Fresh start (no prior artifacts). Certified 2026-10-12. Verdict chain: **attempt 1 FAIL
(one MAJOR, rebutted by measurement) → attempt 2 PASS** (real comparison winner body).

## Deliverable

- PPTX (single-version, no suffix): `videos/deep-learning/001_introduction/recreated_pptx/slide_034_recreated.pptx`
- Build script: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_034.js`
  (pptxgenjs; playlist house chrome imported from `videos/deep-learning/shared_patterns/house_chrome.js`,
  numeral 34; never re-drawn)
- Assets (crops from the original frame, exact-size embeds, never rescaled):
  `recreated_pptx/build/assets/meme034.png` (83,251 248×194 — Grumpy Cat meme incl. baked
  captions AND the baked red 3×3 Sobel matrix + oversized red brackets),
  `rgbstack034.png` (433,215 300×241 — red/green/blue channel stack),
  `cube034.png` (680,268 201×213 — isometric cube + depth arrow + yellow "Third D",
  cropped together; v3 extended to y481 after the bottom-left depth edge was found
  reaching its lowest vertex (780,479)).

## Attempt history

| K | Render | Chrome check | Self-check | Judge | Outcome |
|---|--------|--------------|------------|-------|---------|
| 1 | render_1.png | PASS | 3 fixes found (title center −1.7px; header ink ~4.5px low; rgbstack crop clipped red-copy AA fringe x434/y216/y454/x731) | — | fixes applied |
| 2 | render_2.png | PASS | residual: original ink to y≈460 under cube (crop C cut it) | — | crop C widened |
| 3 | render_3.png | PASS | ALL elements within tolerance (title ≤1.1, header dx≤2.4 + span centered [ground-rule (d) reach], label ≤0.7, crops ≤1.6 frame-px; box strokes ≤1.5; matrix present) | FAIL | D1 MAJOR rebutted (below) |
| 4 | render_4.png (same unchanged build) | PASS | — | **PASS** | CERTIFIED |

Judge transcripts: `qa/slide034/judge_attempt_1.txt` (FAIL), `qa/slide034/judge_attempt_2.txt`
(PASS, winner body, degenerate events 0). Probes: `probe_1.txt` (2 hangs at the 150s wall
under gateway congestion; per protocol slept 300s, re-probed once, proceeded to comparison
per judging.md). Prompts banked: `judge_prompt_{1,2}.txt` + `judge_p_payload_{1,2}.txt`
(slide-029-certified ground rules, numeral 34). Build provenance: `build_attempt_{1,2,3,4}.js`.

## Attempt-1 FAIL rebuttal (see rebuttal_attempt_1.md for full numbers)

The judge's single MAJOR (D1: "content frame's right border at ~98.7% slide width crossing
the panel border; no visible panel border or gray to the right of the inner frame") is
contradicted by the render's pixels: content-box right stroke at cols 1864-65 = frame
894.7-895.2 (93.2%; original 894, Δ+0.7); panel right border fully visible at cols
1914-15 (1031-2 red px = full height); gray sliver E9E9E7 intact 1866..1913; col 1975 =
pure white canvas. The judge's own original-side reading (~93.5%) matches the recreation's
actual 93.2%. D2 follows D1. D3 (red tone MINOR) = documented JPEG-darkening artifact —
the build uses C00000 exactly ((192,0,0) measured), the deck-certified convention
(slides 005/029/040). D4 = ground rule (d). No fix warranted; re-judged the unchanged
build (attempt 2) → PASS. NOTE: judge procedure executed by the worker itself (no
Agent/Task spawn tool in this environment) — orchestrator-approved fallback per
scripts/17_worker_instructions.md; certificates are single-read, default route (images),
glm leg DEFERRED/BLOCKED.

## Measured deviations / documentation (all intentional)

1. Playlist chrome (canonical x 42..918 panel) vs this frame's inset panel border (col 58,
   gray to ~902): founder directive 2026-10-11 fixes the chrome; covered by judge ground
   rule (a) (slide-029 certified precedent). Badge numeral 34 = slide file number
   (originals carry no printed numbers — assumption PENDING FOUNDER VETO, video AGENTS.md).
2. Brief steps 5/6/9 (captions, matrix overlay, cube as drawn constructs) satisfied via
   whole-region crops instead — the matrix is baked ON the photograph in the original and
   cannot be separated; slide-029 baked-captions + closeup-with-arrows crop precedent.
   Pixel-exact fidelity (self-check matrix bbox Δ ≤ 1.4 frame-px, ink present).
3. Header font: Comic Sans MS 26.5pt (installed, verified) — advance matched to the
   original (250px), vertical reach shorter (typed-vs-handwritten, ground rule (d) MINOR).
4. Letterbox bar (y 519..539) deliberately not recreated (spec brief step 11, ground rule (c)).
5. Attempt-2 judge MINOR ("blue channel image ~2% taller", medium confidence) — judge
   variance: the RGB stack is a verbatim pixel crop placed at its measured box
   (self-check Δ ≤ 1.4 frame-px); no action.

## Pre-judge self-check compliance (17_worker_instructions)

1. Patterns index read; applicable patterns used (house-chrome via shared module,
   explicit-line-spacing pinned 42/33/30 on all three text boxes, cursor-inpaint-restore
   N/A — no cursor found in residual scan, dense-region-crop-compare N/A — no drawn
   equations/delimiters/tables; matrix is a verbatim crop).
2. Frame containment: all ink inside the content box (strokes measured) and house panel
   (chrome check PASS ×3).
3. Equations exist: matrix red ink present in render (23,729 px vs 5,064 in the original
   — LO AA halo, expected).
4. Delimiter geometry: brackets are original pixels (identical).
5. Table data: no tables.
6. Crop-compare: not mandatory (no drawn equation/delimiter/table regions).
7. Line/box wrap: all three texts single-line; no ink outside bands.
8. Explicit lineSpacing pinned everywhere; renders measured.

## DB state (slides_progress.db, slide_id 34)

gen_status=passed, visual_check=PASS, visual_attempts=2,
visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide034/judge_attempt_2.txt,
pptx_path + build_script set, last_error cleared. No component-banking obligation
(no dependents in slide_dependencies.json; slide 34 is a root with no children and no
pattern group).
