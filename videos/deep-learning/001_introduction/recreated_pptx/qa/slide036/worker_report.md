# Slide 036 worker report — "How many Parameters are  in the  RGB / Image filter  ( K=3 )"

**VERDICT: PASS (judge attempt 1).** Certified 2026-10-12. Slide 37 (dependent) unblocked.

## Resume context

The previous builder died on an API connection timeout after ~94 min. It left 3+ PIL
measurement passes in this dir (`measure_original{,2,3,4}.py` + `_out.txt`) and the
`crops/` exploration set — no build script, no renders, no pptx. This worker RE-VERIFIED
the banked passes against the frame (all consistent), added `measure5.py` (content-box
border, =/+/neuron/arrow geometry, color-separated question/equation bands, crop-edge
safety) and `fit_fonts.py` (Arial/Comic metric fits), then built the full chain fresh.
Judge attempt numbering starts at 1 (no banked judge transcripts existed); renders
1–3 are this worker's closed-loop iterations.

## Deliverable

- **PPTX (single version):** `videos/deep-learning/001_introduction/recreated_pptx/slide_036_recreated.pptx`
- **Build:** `recreated_pptx/build/slide_036.js` (thin runner) → composition in
  `recreated_pptx/build/components/slide_036.js`
- **BANKED COMPONENT (mandatory — slide 37 imports it):**
  `recreated_pptx/build/components/slide_036.js` — `renderBase(pptx, slide, opts)` with
  per-block functions (content_box, title, slab_top, slab_body, filter_unit, equals, plus,
  neuron, arrow_neuron, question, equation), geometry as parameters (`GEOM`, per-block
  `opts.geom` overrides, `opts.skip`/`opts.only`/`opts.numeral`). Slide 37's crowding fix:
  skip `filter_unit, equals, plus, neuron, arrow_neuron, question, equation` and draw its
  own; reuse `slab_top`+`slab_body` TOGETHER (A/B tile, seamless).
- **0-PIXEL-DIFF PROOF:** `scratch_component_proof/proof_build.js` requires the certified
  component by absolute path and renders md5-IDENTICAL to the certified render:
  `proof-1.png = 6c27c19144fe8e3fea35827e41258570 = render_3.png` (see
  `scratch_component_proof/proof_md5.txt`). Zip-level pptx md5s differ (pptxgenjs embeds
  timestamps) — the law's proof is render-level pixel identity, which holds exactly.
- **Assets (cropped from the frame, exact boxes, no rescale):** `build/assets/slabtop036.png`
  (158,160 245x61), `slabbody036.png` (158,219 223x176), `filterunit036.png` (378,240
  122x170), `eq_147_036.png` (mathtext 32pt #D42A2A; sidecar `eq_147_036_sidecar.json`).

## Verdict chain (evidence)

| Step | Result | Evidence |
|---|---|---|
| PIL closed-loop self-check (attempt 2 render) | 2 real fixes found: equation `padIn` unit bug (0.96in shift), title 3px low | `selfcheck_attempt_2_out.txt` |
| PIL closed-loop self-check (attempt 3 render) | **ALL PASS** (title/box/tiles/=/+/neuron/arrow/question/equation extents + containment) | `selfcheck_attempt_3.py` + `_out.txt` |
| house_chrome_check | **PASS** (attempt 1 and 3) | `house_chrome_check_attempt{1,3}_out.txt` |
| Crop check 1 — equation region | **PASS**, MINOR-only (font rendering detail) | `crop_eq_check_1.txt` |
| Crop check 2 — =/+/neuron/arrow cluster | **PASS**, MINOR-only (neuron ~5-10% relative, plus shade) | `crop_result_check_1.txt` |
| **Judge attempt 1** | **PASS** — `[winner] images (round 1, attempt 1)`, validated winner, degenerate events 0; findings: 3 MINOR, no BLOCKER/MAJOR | `judge_attempt_1.txt` (transcript), procedure per `judge_prompt_1.txt` + `-p` from `judge_p_payload_1.txt` |

Judge MINOR findings and dispositions (documented, none are fix triggers):
1. "Diagram ~8-10% larger relative to panel" — judge variance: the diagram tiles are
   BAKED ORIGINAL PIXELS at PIL-measured positions (tile probes maxd<=3; selfcheck
   extents PASS); pixel identity overrides the impression.
2. "Equation closer to bottom border" — PIL: eq ink bottom 481.9 vs original 479
   (Δ2.9px @150dpi), inside the 4px tolerance; containment clean.
3. Typed-vs-handwritten — ground rule (d) medium difference, at most MINOR.

## Deviations from the spec JSON (frame is truth; spec PASSED gate but its geometry
## estimates were explicitly unmeasured)

1. **'=' sign color:** spec says "dark equals sign" — the frame shows CYAN bars (PIL
   modal 3EAEC6). Drawn cyan per frame.
2. **Neuron center:** spec 29ABE2 → measured flat-fill modal 11BDEB (deck law: ink wins
   on flat fills).
3. **Dashed-line count:** spec "fixed at 7" (two vision estimates) — the frame has 5 dash
   bands (two independent banked PIL passes agree). Moot in the render: all dashes are
   baked original pixels.
4. **Point sizes:** spec ~32/24/28pt (marked unmeasured) → PIL-fitted 35pt Arial Bold
   title (adv 648 vs 643), 39pt Comic Sans MS question (adv 638 vs 638), 32pt mathtext
   equation (ink 253.4 vs 254).
5. **Arrow direction:** spec "up-right to the neuron icon" — the frame's arrow points
   UP-LEFT (tail 660,408 → tip 611,325). Drawn per frame.
6. **Title color:** C00000 per this deck's certified precedent (034/005/029/040 — measured
   modal AC0E1D reads as JPEG-darkened C00000); spec said A61C1C.
7. **Imagery law:** hand-drawn 3D slabs + intertwined ink (labels/arrows crossing them,
   dashes over the slab face) are CROPS from the frame (slide-034 certified precedent),
   3 tiles with verified edge safety (A/B tile at y=219/220, C overlaps B at x 378..380 —
   identical source pixels, seamless). Everything cleanly separable is drawn/rendered.
8. **Equation professional-format law:** `7 · 7 · 3 = 147` rendered as matplotlib
   mathtext PNG (32pt, \; spacing matches the original's wide marker spacing), per
   founder directive 2026-10-09; judge ground rule (e) covers the format upgrade.
9. **Badge numeral "36"** (file number; 001_introduction originals carry no printed
   numbers — assumption PENDING FOUNDER VETO per video AGENTS.md).
10. **Black strip rows 519..539 excluded** (video-player artifact; ground rule (c);
    certified slide-034/040 precedent).
11. Sources honored: `slide_036_source/SOURCES.md` (CS231n depth-column, 7·7·3=147
    confirmed); the gray '+' (bias-term annotation) kept verbatim per its [?] note.

## DB state (final)

`gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
`visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide036/judge_attempt_1.txt`,
`build_script` + `pptx_path` set. Slide 37: `unblocked`.

## Notes for slide 37's builder

- `require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_036.js")`
  (NEVER edit it — copy-then-modify if needed; cascade law).
- `renderBase(pptx, slide, { numeral: "37", skip: ["filter_unit","equals","plus","neuron",
  "arrow_neuron","question","equation"] })` then draw your own right side + your question/
  equation at YOUR measured geometry; pass `opts.geom` overrides if the header band
  compresses the diagram (the founder-noted crowding).
- `slab_top` + `slab_body` are one seamless unit (tile pair) — move/skip them together.
