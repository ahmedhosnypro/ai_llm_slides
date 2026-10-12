# Worker report — slide 039, deep-learning/001_introduction ("How many filters we should apply")

**Final verdict: PASS (judge attempt 1).** Certified single-read, default route (`models:
images`, no `--models` flag), glm leg DEFERRED/BLOCKED per routing law.

## Dispatch deviation (important, for the orchestrator)

The dispatch text described this slide as *"Where to Get Filters for Recognition (k>1-D
case...)"*. That is **incorrect for slide_039.jpg** — it matches slides 31–33. The ground
truth frame `unique_slides/slide_039.jpg`, the DB row, `slides_index.json` (group 52,
frame_02894), `slide_039_source/SOURCES.md`, and a banked vision read of the frame
(`frame_read.txt`) all identify slide 39 as **"How many filters we should apply"** (the
parameter-sharing / stationarity argument with the two meme photos). The passed spec
`analysis/slide_039_final.json` matches the frame element for element (vision-verified
before building). Built to the frame + spec. Slide 40 (same title, next annotation state)
was already certified separately — 39 and 40 are distinct frames (different layouts,
verified).

## Attempts used: 1 of 6

| Attempt | Build | Render | Pre-judge checks | Judge | Result |
|---|---|---|---|---|---|
| 1 | `build/slide_039.js` (banked copy `build_attempt_1.js`) | `render_1.png` (2001x1125 @150dpi) | house_chrome_check PASS; selfcheck 19/19 PASS | `judge_attempt_1.txt` | **PASS** |

Two pre-judge iterations happened WITHIN attempt 1 before any judge dispatch (closed-loop
discipline, not judge retries): (i) two self-check bugs fixed (title scan window included
the chrome panel-top border; cursor-zone scan extended into the inherently bright panel
gray); (ii) title size bumped 38.5→38.7pt after the closed-loop measured the LO render
2.4 frame-px narrower than the original's 560px ink width.

## Judge findings (attempt 1, verbatim summary)

- 0 BLOCKER, 0 MAJOR. Ground rules settled: house chrome (a), cursor omitted (c), black
  video bar omitted (c) — all intentional.
- MINOR (~60% conf): title red marginally brighter in the render (video compression
  darkens the original) — within color tolerance.
- MINOR (~50% conf, NOT counted): note-box bottom border fully visible in the render but
  clipped in the original by the video bar — mandated rule-(c) treatment.
- Visual-quality defects: none (no overflow/clipping/wrap/collision; line spacing matches).

## Verification chain (evidence in this dir)

- `measure_original1.py/.json` — PIL forensics: chrome vline x58 (frame quirk, same as
  certified slide 040), title ink x203..763 baseline ~84.5, white box stroke-center
  x75.5..880.5 y100.5..295, photos cat(183,308,266x136)/dog(473,305,260x139), annot box
  x72..900.5 y452.5..514, highlight rect x240..719 y264..290, 3 annot lines at
  baselines 468/484/500 pitch 16, black bar rows 518..539 (artifact, omitted).
- `font_solve2.py/.json` — sizes solved by ink width + height check: title Times New
  Roman Bold 38.7 (slide-040 ascender precedent), box body Liberation Serif 23.5
  (headers bold; serif corr 0.31 vs sans −0.60 on 'Conclusion'), phrase Arial Bold 21.5,
  annot lines Arial Italic 14.5.
- `frame_read.txt` — full-frame vision read through the gate: content matches the spec
  verbatim (incl. double space "locations  in"); cursor located at ≈(447,358).
- `crop_assets.py/.json` — photos cropped incl. baked borders/overlays; **cursor patched
  out** (mean of rows y∓26): 0 residual bright px, border column continuous 36/36.
- `house_chrome_check.py` — PASS (panel x 89..1913, badge (1860,148) d70, tol 8).
- `selfcheck_attempt_1.py/.json` — 19/19 PASS (title core band, box edges, 6 white-box
  line bands, 6 left inks, highlight rect, photo pixel-identity 4.8/4.4 MAD, cursor
  absence, annot box edges, 3 annot line bands, Red/Green word x, yellow blank x,
  containment 0 stray px). No equations/delimiters/tables on this slide → crop-vision
  tier not applicable (documented).
- `judge_prompt_1.txt` + `judge_payload_1.txt` — frozen prompt (payload sourced
  byte-for-byte); `probe_1.txt` — window probe; `judge_attempt_1.txt` — comparison
  transcript, `[winner] images (round 1, attempt 1)`, degenerate events 0.

## Build facts

- Deliverable (SINGLE-VERSION, no suffix): `videos/deep-learning/001_introduction/recreated_pptx/slide_039_recreated.pptx`
- Build script: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_039.js`
  (imports `shared_patterns/house_chrome.js`, numeral 39; bare hex; fontFace everywhere;
  margin:0; explicit lineSpacing; writeFile({fileName})).
- Assets: `build/assets/slide039_cat_photo.png` (266x136), `slide039_dog_photo.png` (260x139).
- Intentional deviations (all documented in the build header + judge ground rules):
  chrome drawn at canonical x42..918 (frame's own panel border sits at x58 — same quirk as
  certified slide 040); box borders drawn in measured washed lavender `8C89AE`/`A6A3BB`
  (spec's #3333CC is JPEG-washed in the frame; slide-040 precedent); annotation box fill
  `FAFDEA` (measured modal; spec FFFFE1 washed); line-2 blank reproduced as the word
  'Yellow' colored FFFF00 over an FFFF00 under-rect (yellow-on-yellow = blank, exactly as
  the source shows; spec uncertain item honored — blank not filled with readable text).
- No equations (no OMML pass), no advanced graphs (no graphgen), no dependents
  (`deps` shows no children of 39) → **no component-banking obligation**.

## DB state (final)

`gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
`visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide039/judge_attempt_1.txt`,
`pptx_path`/`build_script` set, `last_error=None`.

## Process note

Judge procedure executed by the worker via Bash (no Agent/Task spawn tool in this
environment) — orchestrator-approved fallback per `scripts/17_worker_instructions.md`
step 7; the verdict was taken verbatim from the vision model's comparison winner body.
All work stayed inside `videos/deep-learning/001_introduction/`; `unique_slides/` and
`frames/` untouched; no banked evidence deleted.
