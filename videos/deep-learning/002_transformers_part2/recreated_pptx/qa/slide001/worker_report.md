# Worker report — slide 001 PLACEHOLDER COVER (Deep Learning DSAI 308, Transformers — Part II)

Video: `deep-learning/002_transformers_part2` · Worker: per-slide build worker · Date: 2026-10-11
Deliverable: `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_001_recreated.pptx` (SINGLE-VERSION law — no suffix)
Build script: `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_001.js`
DB final state: `gen_status=passed`, `pptx_path` + `build_script` set. **`visual_check` deliberately
NOT set and `visual_attempts` NOT incremented** — per the placeholder-cover law this slide's
certification field is the founder's sign-off (no visual-judge comparison is possible; there is
no ground-truth frame).

## What this slide is

The cover frame is MISSING from lecture 002's video (DB `analysis_status='n/a-placeholder'`,
`validation_status='ready'`). Per the placeholder-cover law (playlist AGENTS.md + this video's
AGENTS.md "Special slides" + `scripts/17_worker_instructions.md` rule 7) it is rebuilt as a
placeholder **mirroring lecture 001's certified cover**:

- Visual reference: `videos/deep-learning/001_transformers_part1/unique_slides/slide_001.jpg`
  (read-only; nothing under 001 was modified).
- Structural reference: 001's certified build
  `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_001.js` — every
  element's geometry, font, size, color, and text is copied VERBATIM from it. No invented
  text or art.

## Build summary

- pptxgenjs, LAYOUT_WIDE 13.33×7.5, Arial everywhere, `margin:0`, no `#` hex.
- Chrome: **shared playlist module** `videos/deep-learning/shared_patterns/house_chrome.js`
  imported by absolute path, `drawHouseChrome(pres, s, { numeral: 1 })` — never re-drawn by
  hand. Badge numeral **1** per the placeholder spec (same as 001's cover).
- Title "Deep  Learning" (double space VERBATIM) / "DSAI 308" — 001's exact measured block:
  one centered box x 0.41 y 1.734 w 12.13, 60 pt bold `C00000`, explicit `lineSpacing: 67`.
- Credit block ("Prepared By" 20 pt bold italic red; name 24 pt bold `000090`; email 16 pt)
  at 001's measured positions, centered at ink-center 7.158 in.
- Instructors block (heading 20 pt bold italic red at ink-left 0.778 in; names 20 pt bold;
  emails 15 pt, second email italic) at 001's measured positions.
- Logo: **re-cropped from 001's source frame** at 001's measured rectangle (ink x 594-905,
  y 468-526 → PIL box (594, 468, 906, 527) = 312×59 px) into THIS build's assets dir
  (`build/assets/zewail_logo_slide001.png`). Verified **byte-identical to 001's certified
  asset: 0 / 18,408 px differ**. Embedded at exact size `w = px/72` in (4.3333×0.8194 in)
  at 001's measured position (x 8.25, y 6.5).
- Stray gray `+` crosshair artifact: **inherited** from 001's certified cover build at its
  measured position (the directive is "mirror 001's certified cover", and 001's certified
  build carries it). Flagged below for founder veto at sign-off — judge ground rule (c)
  classifies such artifacts as omittable, so removing it is a one-line change if desired.
- No equations, no tables, no delimiters, no charts (nothing from the math/dual-representation
  rules applies).

## Dependency status

`15_progress.py deps` → slide 1 is a **root** (no parent, no pattern group, and no child edge
in ANY video's graph points at `deep-learning/002_transformers_part2:1` — checked
`slide_dependencies.json` v2 edges), so the build was never dep-gated and **no component export
is required** under the playlist-scoped banking obligation.

## QA evidence (this directory)

| Check | Result | Evidence |
|---|---|---|
| 150 dpi render | `render_1.png` (2001×1125), rendered via private LO profile + `TMPDIR` override to `videos/deep-learning/002_transformers_part2/scratch/slide001/` (/tmp is quota-blocked) | `render_1.png` |
| `house_chrome_check.py` (shared playlist checker) | **PASS, exit 0** — panel x 89-1913, y 95-bottom; badge center (1860,148) d=70 @150 dpi; all within tol 8 | `house_chrome_check_1.txt` |
| PIL geometry comparison vs 001's certified render (`001_transformers_part1/recreated_pptx/qa/slide001/render_1.png`) | **ALL 17 elements within tolerance — every measured delta is 0 px** (title L1/L2, badge, panel, logo, credit block ×3, instructors block ×5, crosshair). **Full-image diff: 0 / 2,251,225 px differ — the placeholder render is PIXEL-IDENTICAL to 001's certified cover render.** Tolerance was ~4 px; measured deltas: all 0. | `selfcheck_attempt_1.py` + `selfcheck_attempt_1_output.txt` |
| Build provenance | build script verbatim at build time | `build_attempt_1.js` |

No judge was dispatched — CORRECT for this slide (rule 7: nothing to compare against; a judge
comparison is impossible without a ground-truth frame). No `visual_check`/`visual_attempts`
writes. No vision-gate calls were needed or made.

## Items explicitly flagged for founder sign-off

1. **Stray `+` crosshair artifact** — inherited from 001's certified cover to achieve the
   pixel-exact mirror; say the word and it is removed (one line) if the placeholder should
   show only the ideal cover.
2. Everything else is a verbatim mirror of 001's certified cover (same title, credit block,
   instructors, logo) — if the founder wants a DIFFERENT layout for 002's placeholder cover
   (e.g. title only), that is a content change to record in the spec.

## Certification state

**This slide's certification = FOUNDER SIGN-OFF — PENDING.** The machine-side gates that were
run (chrome check PASS, pixel-identical mirror of the certified cover) are complete; the
founder's approval of this placeholder is the remaining and deciding certification step.

AWAITING FOUNDER SIGN-OFF — view the render:
`videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide001/render_1.png`
(pixel-identical to 001's certified cover render; the deliverable pptx is
`videos/deep-learning/002_transformers_part2/recreated_pptx/slide_001_recreated.pptx`).
