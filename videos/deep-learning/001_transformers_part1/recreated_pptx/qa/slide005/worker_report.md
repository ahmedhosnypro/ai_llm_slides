# Worker report — slide 005 "1-D Convolutional Neural Network" (001_transformers_part1)

Date: 2026-10-11. Worker: per-slide BUILD WORKER (subagent). Final verdict: **PASS** (attempt 3).

## Deliverables

- PPTX (single-version law, no suffixes): `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_005_recreated.pptx`
- Build script: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_005.js`
  (pptxgenjs; house chrome drawn ONLY via `videos/deep-learning/shared_patterns/house_chrome.js`,
  `drawHouseChrome(pptx, slide, {numeral: 5})`; no `#` hex; fontFace everywhere; margin:0;
  explicit lineSpacing 14pt on headers, 16pt on kernel label)
- Render: `recreated_pptx/qa/slide005/render_3.png` (150 dpi, private LO profile +
  TMPDIR under the video namespace — /tmp quota avoided)
- Dependency status: ROOT (confirmed via `15_progress.py deps`); no dependents, so no
  component export required.

## Attempts

| K | What happened |
|---|---|
| 1 | Build v1 + render_1. house_chrome_check PASS. Self-check attempt 1: FAIL — mix of my checker's unit bugs (frame-px offsets added to render-px indices) and real issues: banner rect too long/wide vs measured band, hatch PNG alpha-blended white rendered (224,224,224) in LO, title y 2px low. No judge dispatched (pre-judge gate held). |
| 2 | Fixed: banner rect 5.4in→ L 362px/rot 338/center (745,428) (re-measured: midline slope −21.7°, perp width 31.6px, length ~362px); bar text 13→14pt (measured 90px text length); kernel label −1.5px; caption 16→16.5pt; title y −2px. render_2: all checks pass except hatch white-body count (check miscalibrated) + border AA misread as stray ink. |
| 3 | Hatch PNG regenerated: opaque E9E9E7 background (kills alpha-blend dimming) and stripe pitch 5.4px along-x (measured from frame drift, was 4). render_3: **ALL self-checks PASS** (see below). Judge → PASS. |

## Judge (attempt 3 — the only judge dispatch)

- Banked prompt: `qa/slide005/judge_prompt_3.txt`; banked build: `qa/slide005/build_attempt_3.js`
- Probe transcript: `qa/slide005/probe_3.txt` (valid body, window opened)
- Comparison transcript: `qa/slide005/judge_attempt_3.txt` (validated winner body,
  degenerate events 0, single-read default route images, glm leg DEFERRED/BLOCKED)
- **FINAL VERDICT: PASS** — element-by-element table all Match; missing elements: none;
  frame containment: pass (banner tip and arrowhead approach but do not cross the border);
  no overflow/clipping/collisions.
- Judge MINOR findings (documented, non-blocking per verdict law):
  1. caption style — judge reads original as bold italic vs recreation bold upright (spec
     says bold+underlined, no italic; not fixed post-PASS per verdict law).
  2. title typeface family (serif-leaning vs Arial bold) — inherent font substitution.
  3. triangle z-order at 3rd→4th map — very subtle, low confidence; original shows the
     same bar/triangle intersection.
  4. row-count granularity (~13–14 vs ~14, low confidence) — pixel forensics pinned the
     true grid at 18 cells/stack (see below).
- NOTE (17 §7 fallback): no Agent/Task spawn tool in this environment — the banked judge
  procedure was executed by the worker via Bash, byte-for-byte (probe + comparison through
  the vision gate, transcripts banked). Orchestrator-approved fallback.

## Mandatory pre-judge self-check (banked: `qa/slide005/selfcheck_attempt_3*.py/.txt`)

1. Patterns library read first (index.json + patterns.md); no new pattern needed — this
   slide's novel bit (fine diagonal hatch → 8x PNG embedded exact-size) follows the
   certified image-embed discipline.
2. Frame containment: PASS — content ink inside the panel; the checker's two flagged
   clusters decomposed in the banked addendum: 8828/9056 px are the chrome border's own
   C00000 anti-aliasing (within 4px of a border line), the remaining 203 px are the
   banner's right tip at x913–918.2 — the ORIGINAL banner yellow reaches x918 identically.
3. Equations: none on this slide (no equation regions — N/A).
4. Delimiter geometry: no multi-line delimiters on this slide (N/A).
5. Table data: no tables (N/A).
6. Dense-region crop compare: mandatory only for equations/delimiters/tables — none
   present; cell stacks were instead verified cell-by-cell (18 cells × 5 stacks, modal
   fill classification on BOTH render and frame — stronger than a crop compare here).
7. Line/box wrap: no ink outside expected bands (per-element bbox checks all within
   tolerance).
8. Explicit line spacing: pinned 14pt (headers) / 16pt (kernel label); measured render
   line tops 149.6 vs target 149, kernel label top 155.2 vs 155.

## Spec-vs-frame resolutions (frame is ground truth; recorded per SOURCES.md's [?] items)

- **Cell count**: spec estimated 13 cells/stack; the frame's outline grid measures 18
  cells (y178.5→462.5, pitch 15.78px, uniform across all 5 stacks). Built with 18.
- **Highlighted cells** (spec's [?] row assignments, re-verified by modal luma/hue):
  WV FFFFCC cells 1–3; FM1 FFCC99 cells 3, 14, 15, 16; FM2 cyan cells 9, 10, 11, 15;
  FM3 FFCCFF cells 3, 4, 5, 10; FM4 CCFFCC cells 4, 14. (Spec proportions agree; the
  13-cell numbering was the compressed reading.)
- **Funnel triangle 2**: the spec lists 4 funnel triangles; the founder-swapped canonical
  frame (frame_00095) contains only 3 — raw deviation scan of gap1-lower (x246–306,
  y330–460) found 5 noise pixels total. Triangle 2 omitted; frame wins.
- **Gray bars**: fill measured (216,216,216) ≈ D8D8D8 (spec said BFBFBF — measured wins);
  bars at x412/560/702/832, w18, y178–461; blue 0000CC rotated text 14pt, centered.
- **Warning banner**: measured −21.7° (spec said ≈−8°), band length ~362px, perp ~31.6px,
  midline center (745,428) → yellow rect + text rotate 338.
- **Callout fill**: modal (224,248,224) ≈ E0F8E0 (spec said white — measured wins).
- **Non Linearity bar between Words Vectors and 1st FM**: confirmed ABSENT (matches the
  spec's validated fix).
- **Bar 1 column artifact** in early self-checks: the hatch image's alpha-blended white —
  fixed by making the PNG background opaque E9E9E7.
- Mouse-cursor artifact (≈x29%, y21%) NOT recreated (spec step 26 + judge ground rule c).

## Evidence index

- `qa/slide005/render_{1,2,3}.png`, `selfcheck_attempt_{1,2,3}.py/.txt` (+ addendum in 3)
- `qa/slide005/judge_prompt_3.txt`, `probe_3.txt`, `judge_attempt_3.txt`, `build_attempt_3.js`
- Forensics: `scratch/slide005/forensics1..11_out.txt`, `probe1.py` output, `gen_hatch.py`
- Progress DB: gen_status=passed, visual_check=PASS, visual_attempts=3,
  visual_transcript=videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide005/judge_attempt_3.txt
