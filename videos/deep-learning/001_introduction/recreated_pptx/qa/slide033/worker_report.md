# Worker report — slide 033 (001_introduction) "Where to Get Filters for Recognition"

## Outcome

- **Final verdict: PASS** (visual judge attempt 3, real comparison winner body).
- Deliverable: `videos/deep-learning/001_introduction/recreated_pptx/slide_033_recreated.pptx` (SINGLE-VERSION, no suffix).
- Build script: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_033.js`.
- Comparison transcript: `videos/deep-learning/001_introduction/recreated_pptx/qa/slide033/judge_attempt_3.txt`.
- DB row 33: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=3`, `visual_transcript=.../judge_attempt_3.txt`, `last_error=null`.

## Resume context

Two predecessor workers died on API connection timeouts with no pptx / no build script /
empty qa dir. Their only surviving artifacts were four EXACT pixel crops of the original
frame in `build/assets/` (`s033_plane_upper/lower/rgb_slab/mc_slab` — verified by
pixel-exact correlation, err 0.00, boxes x105..213/y345..432, x105..192/y433..486,
x330..494/y318..491, x570..764/y343..491). This run treated everything else as a fresh
start and REUSED those crops (dispatch-sanctioned: crop non-drawable imagery at measured
boxes). Judge procedure executed by the worker (no spawn tool in this environment) —
orchestrator-approved fallback per 17_worker_instructions.md §7.

## Attempts

| Judge attempt | Render | Verdict | Issues |
|---|---|---|---|
| 1 | render_4.png | FAIL | 3 MAJOR (high conf): "Grayscale"→"Grays…", "Multiple channels"→"Multip…", "Filter" vs "Filters" — label truncation claims |
| 2 | render_5.png | FAIL | same 3 MAJORs ("Graysc", "Multiple" w/o "channels", "Filter") |
| — | render_6.png | (crop comparison, dense-region check) | MAJOR: label glyphs ~2x too heavy — root cause found |
| 3 | render_6.png | **PASS** | 0 BLOCKER/MAJOR; 3 MINORs (marker-font glyph shapes [rule d], <2% title-width/arrow-curvature, 'rd' hue) |

Renders 1-3 were pre-judge closed-loop iterations (geometry fixes only; no judge dispatch).

## Root cause of attempts 1-2 (the interesting failure)

The exposed handwritten labels ("Grayscale", "Multiple channels", "Filters") were first
rendered as Comic-Sans-Bold tight-ink PNGs (slide_032's documented mechanism) baked down
to the exact tiny boxes. Two independent vision reads claimed the labels were TRUNCATED
("Graysc", "Multiple", "Filter") while PIL proved the ink spanned the full measured boxes.
The dense-region crop comparison (law step 6) exposed the real defect: Comic Sans Bold's
stroke weight (~0.3 of cap height) is ~2x the original's thin pen hand (~0.15) — at label
size the adjacent letters MERGED into blobs, so the model read blobs as fewer/fatter
letters ("Multiple" alone filling the label's width). Baking the downscale into the tiny
asset and letting LO upscale made it worse.

Fix (attempt 3): crop the three label words directly from the original frame at their
measured boxes (`s033_crop_word_{grayscale,multichannels,filters}.png` — neighbors
verified clean), same mechanism as the slab crops and the 'rd' superscript crop.
Original pixels = zero font-fidelity risk. Lesson for the skill memory: **at small label
sizes, substituted-font stroke weight must be matched to the original's measured stroke
weight (or the handwriting cropped outright); a bold marker font reads as truncated
text to the vision judge.**

## Measured build summary (frame px, 1px = 1pt; PIL forensics in git history of this dir)

- Chrome: playlist house chrome imported (`shared_patterns/house_chrome.js`), numeral 33
  (this lecture's frames carry no printed numbers — assumption PENDING FOUNDER VETO,
  001_introduction/AGENTS.md).
- Title: Arial Bold 35pt C00000, ink x175..773 (center 474), cap top 80, baseline 105
  (advance-center 476.4 closed-loop, same +2.4 correction as certified sibling 032).
- Text panel: border center-line x78.5..877.5 y140..266, white fill, 9999CC 1.5pt
  (modal (160,157,188) — chroma-reconstruction identical to certified slide_031; the
  spec's "0000CC border" guess loses to ink per deck law).
- Body: Times New Roman Bold 21pt (width-solve mean +1.2px over 13 words; cap height 14px
  exact), navy 000080 (darkest cores (0,0,82..102) match certified slide_031's navy; the
  spec's 0000CC guess loses). Baselines 163/210/233/256; ink lefts 94/88/88/88.
- COLOR RUNS (ink wins over the spec's coloring claims): red ONLY on "k-D,"/"k-D" (L1),
  "K=3" (L2), "K=9" (L3); the spec's "red 'should also be k-D' / 'use K-D filter' /
  'use 9-D filter'" is contradicted by the ink (those runs measure all-blue).
- DOUBLE SPACES reproduced from ink (L2 "use  K-D"; L3 "(Satellite  images)  use" —
  original gaps 13-14px vs 7-9px normal; closed-loop drift −6..−7px without them).
- Underlines: light-periwinkle 8888CC rects y164..165.8 under "images" (x205..265) and
  "parameters" (x351..453) — the original's underlines are periwinkle (1px core
  (103,99,180)), NOT the text color, so they are drawn as rects (pptxgenjs underline
  cannot differ from its run color).
- 'rd' superscript (L3): EXACT crop from the original (x481..493 y217..227). Native
  superscript runs measured broken in LO (auto-scaled to ~58% + under-raised, bottom
  229.4 vs 226) — the certified PNG mechanism is deterministic.
- Diagram panel: border center-line x87..859.5 y306.5..501.5, white fill, C00000 2pt
  (original left stroke 3px; 1.25pt measured too thin in closed loop).
- Imagery: 5 exact crops (plane_upper/lower, rgb_slab, mc_slab, line wedge x269..330
  y436..450) + 3 word crops + 'rd' crop — all at measured boxes. Inner labels
  ("RGB", "3 dims", "k dims" + arrows) are baked in the slab crops (PIL-verified inside).
- Red callout line stubs drawn only between crops: line A (213.5,419.5)→(231.5,440);
  long line C (494.5,428.5)→(569.5,421.5) — 1pt C00000.
- Black bar: x38..921, y519..537.5 (h 18.5) — chrome bottom stroke kept visible
  (documented sibling deviation, slides 002/005/031/032).

## Spec deviations (ink wins / chrome law)

1. No red top rule (spec's "y~6-8%" guess; PIL: no red rows y0..60) — same as 032.
2. Background = playlist chrome (white canvas + E9E9E7 panel), not spec's #DEDEDE.
3. Text-panel border 9999CC, body 000080 (spec guesses 0000CC for both).
4. Coloring runs per ink (see above).
5. Handwriting words + slabs + 'rd' = original-frame crops (dispatch-sanctioned).
6. The original's own lecture chrome (red left border x58, gray bg) is intentionally
   replaced by the playlist house chrome (founder directive 2026-10-11); stated in the
   judge ground rules.

## Self-check evidence (all banked in this dir)

- `house_chrome_check.py`: PASS on every render (1-6).
- `selfcheck_attempt_{1..6}.py` + `_out.txt`: closed-loop PIL checks (title geometry,
  panel borders, 4 body lines left/baseline/width, red-token positions, word-gap drift,
  'rd' box, underline bands, panel borders, crop ink presence, word extents, black bar) —
  attempt 3+ ALL PASS (~4px tolerance at 150dpi).
- `selfcheck_containment_3.txt`: frame containment PASS (the x<41 ink is the black
  bar's own legitimate pixels at x38..41).
- `crop_multichan_1.txt` + `crops/`: dense-region crop comparison (the diagnostic that
  found the stroke-weight root cause).

## Banking obligation

None (dispatch: "No banking obligation"; slide 33 is not a dependency parent in
001_introduction/slide_dependencies.json, and the playlist-scoped 002 references concern
001_transformers_part1's slides 15/19/33, not this lecture's).
