# Worker report — slide 023 (deep-learning/002_transformers_part2)

**Final verdict: PASS** (real visual-judge comparison, default `images` route, `--thinking high
--max-tokens 65536`, winner round 1, 0 degenerate events). Single-read certificate; glm leg
DEFERRED/BLOCKED per standard.

## Deliverables (single-version law)

- PPTX: `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_023_recreated.pptx`
- Build script: `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_023.js`
  (requires the banked component `build/components/slide_023.js` — `renderBase(pptx, slide,
  {numeral})` — which is the composition source of truth; slide 024 depends on 023, so the
  banked component obligation is satisfied by construction: the deliverable build IS the
  component call.)
- House chrome: shared `videos/deep-learning/shared_patterns/house_chrome.js`,
  `drawHouseChrome(pptx, slide, {numeral: 23})`; `house_chrome_check.py` PASS on every render.

## Attempts (4 renders, 1 judge dispatch)

| K | Build delta | Result |
|---|---|---|
| 1 | First build from frame measurements | closed-loop found hl-text +6px low, sizes off |
| 2 | title 25→24.5, subtitle 23→22.5, box text 12.5→13, hl text 16.5→17 with y=cap−7.8, heads widened | caps within 2px; widths within 1%; structural checks pass |
| 3 | crop-driven: hl text → italic (measured stem lean + crop model), b1 underlines "small for long seq"/"large for short sequence" (pixel runs 397..530 / 563..751), b2L1 underline extended through "in short seq" (pixel run 369..566), arrows → up-pointing triangles (apex at destination-box bottom), gray dots 9.4→8.0pt, bullet dots 10.9→9.5pt | row12 + hlbox crops MATCH |
| 4 | blue ellipsis dots 3333CC→#6B8BB4 (measured disc core (107,139,180)), d 10.4→9.8 | row12 crop MATCH; **judge PASS** |

## Evidence (all under `recreated_pptx/qa/slide023/`)

- `judge_prompt_4.txt` (banked frozen template), `build_attempt_4.js`, `probe_4.txt`,
  `judge_attempt_4.txt` — **FINAL VERDICT: PASS**; 4 MINOR issues (bullet-marker size,
  triangle size/position, omitted hairline arcs, +δ label nudges); no BLOCKER/MAJOR.
- Crop comparisons (mandatory dense-region check): `crop_row3_arrows*.txt`,
  `crop_hlbox_text*.txt`, `crop_row12_boxes*.txt` (a1/a3/a4 generations).
- Renders `render_1..4.png`; render 4 is the judged/certified one.
- Measurement scripts in `scratch/slide023/` (chrome landmark fit, badge cross-check,
  band/box/dot/label segmentation, arrow pixel trace, selfcheck_1..6).

## Notable findings

1. **Frame→slide mapping** (this frame, from its own chrome landmarks): left stroke ctr 58↔42,
   right 901↔919, top 43↔45, bottom 516.5↔540 → `slide_x=(fx−17.628)/0.961230`,
   `slide_y=(fy+0.045)/0.956566`. Badge cross-check: yellow bbox center (875.5, 70.5) → slide
   (892.4, 73.7) vs house (893, 71) ✓. Letterbox rows 519–539 and mouse cursor omitted.
2. **Title/subtitle are genuinely right-of-center** in the original (ink centers 516.4/522.6pt
   vs slide center 480) — reproduced as measured (slide-002 precedent).
3. **Arrows are NOT long arcs**: pixel scan of all inter-box gaps found only container-border
   dashes; each arrow is a small orange mark at the DESTINATION box's bottom-center — thin at
   top (apex at the box edge), wide at bottom (below the container border) → up-pointing
   triangle. Two crop runs initially over-read these 15×11px JPEG blobs as "curved arcs";
   the full-slide judge later rated the triangle rendition MINOR-only and PASSED the slide.
4. **Measured-vs-spec deltas honored (frame wins)**: hlbox fill #E8FCFA (not D6EAF8);
   "Problems:" red (not blue); lead line mixed red/blue segments; bullet-1 red δ; bullet-2
   wrap line fully magenta; hl text italic; underlines on b1 phrases and b2 "in short seq".
5. Crop-run a1 was invalidated by a worker-side crop-mapping bug (y1 mapped through the
   x-mapper → squashed crops); detected via file pixel census, regenerated, re-run (a3/a4).

## Judge issues (all MINOR, accepted)

1. Bullet markers slightly larger in recreation (d 9.5pt vs original ~10px blurred).
2. Orange triangles slightly larger/centered vs original's smaller tucked marks.
3. Faint hairline arc traces between triangles and +δ labels omitted (below JPEG visibility;
   gap pixel scan shows no measurable arc ink).
4. +δ label horizontal nudges ±2px.

DB row: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=4`,
`visual_transcript=videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide023/judge_attempt_4.txt`.
No `last_error`.
