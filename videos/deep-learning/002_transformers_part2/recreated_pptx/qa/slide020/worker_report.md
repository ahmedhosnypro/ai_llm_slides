# worker_report.md — slide 020 (P2 pattern-group HEAD) — CERTIFIED

**Slide:** 20 (NNN 020) — "Pre-processing of Input Sequence" — video `002_transformers_part2`
**Verdict:** **PASS** (judge attempt 2; transcript `judge_attempt_2.txt`)
**Deliverable (single-version):** `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_020_recreated.pptx`
**Build script:** `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_020.js`
**DB row at close:** gen_status=passed · visual_check=PASS · visual_attempts=2 · visual_transcript=judge_attempt_2.txt

## Resume note

This run RESUMED a builder killed in a provider storm mid-work. Inherited state:
`qa/slide020/` was EMPTY (no banked renders/judges), but `scratch/slide020/` held three
measurement passes (measure1-3) with a partially-wrong y-mapping. All measurement was
redone from scratch (measure4-10) and no banked evidence was overwritten; attempt
numbering follows this run's renders (render_1..render_13) and judge attempts
(judge_attempt_1..2).

## Frame→slide mapping (re-derived from THIS frame's four chrome landmarks)

Stroke centers measured: left 59.0, right 902.0, top 43.0, bottom 516.0 (frame px) →

    slide_x = (frame_x − 18.628) / 0.961231 ;  slide_y = frame_y / 0.955556

Matches the certified slide_002/slide_003 fits. Badge cross-check: frame badge center
(875.5, 71.0) → slide (891.8, 74.3) vs house (893, 71) — the same 1-4px JPEG-bbox offset
class as the certified builds, confirming the shared playlist template.

## Build iterations (renders) — all chrome checks PASS from attempt 1 on

- render_1: first full build (chrome + self-check drove the loop).
- render_2..3: drawLane color bug fixed (`border.color` on a color string → undefined →
  LO default #333333); label sizes corrected to measured ems (lab1 14.5 it, lab2 16 bold,
  lab3 14 bold, lab4 14 bold-it); banner em 21→20.2 + capTop FY(305); row4 measured
  dashed lane [162,883]x[358,398] white fill added (pixel-mapped, was missing).
- render_4..7: dense-region crop checks (gate) drove: embedding strips re-modeled
  (pink X cell position: 2nd → 3rd of 6 — final per-cell fills MEASURED as a gradient:
  cream EFE9BE / pale-green EAF8D8 / pink F2A7C3 / lavender E9E7F4 / pinkish F2DEEC /
  gray-pink E6DDDB); underbrace switched from rotated leftBrace (LO mis-renders rot on
  the preset — XML had rot=16200000, LO rendered a fragment) to the certified raster
  mechanism (PIL 600dpi PNG → addImage at exact size, `assets/brace_020.png`); inset
  rebuilt from a full pixel map (PE text 2-line top-left, tilde + plus circles at rows
  427-439 right of the text with the vertical riser into the plus, pink box [131,449,
  202,475] centered under the cluster, up-arrow from Inputs at rows 480-497, bottom
  border 512-514).
- render_8..12: lab5 size/x fixed ("Input to Encoder" em 14, x at frame 204 — clears the
  green border); "Inputs" casing per crop-judge verbatim read (capital I, dark 404040);
  row2 groups bare (NO red outer rect — round-3 crop judge); orange pins → small
  downward triangles; subscripts 7pt; lanes sysDash + rounded corners.
- render_13: judge-attempt-1 fixes (below). **This render is the certified one.**

## Judge attempts (frozen `-p` template with ground rules; gate-routed; banked)

| # | Render | Verdict | Transcript | Key findings → action |
|---|--------|---------|-----------|------------------------|
| 1 | render_12 | FAIL | judge_attempt_1.txt | 2 BLOCKERs: (1) missing dashed container around the Word row; (2) missing right-edge grouping marks spanning the embedding+position rows; MAJOR: inset bottom vs house frame proximity; MINOR: I/P row tint. → Fixed 1/2 by adding the MEASURED row1 container (dark-gray 595959 dashed rounded rect [166,883]x[96,138] — pixel-proven: dash lines at rows 96-98 and 136-138, gray #5C5E5D cores; the judge's "red" was context bleed) and 2/2 by adding the two measured red dashed verticals at frame x 887-890 (segments rows [150,180] and [185,270] — pixel-proven #672833 cores); row4 boxes fill FAEEEE (measured #FAEEEE cores). The inset "containment" MAJOR was checked against the pixels: the original's inset bottom (513) sits the same 3px above the panel's bottom stroke — faithful as-is, no change (documented as judge variance). |
| 2 | render_13 | **PASS** | judge_attempt_2.txt | "All renderable content … matches the original." Residual (explicitly ruled usable by the judge): the right-edge grouping mark is drawn as a dashed vertical where the judge reads a curly brace — semantic function preserved by the arrows; embedding-strip cell count/pastel sequence "approximated" (MINOR); ellipsis dots slightly larger (MINOR); bottom brace curvature (MINOR). |

Probe calls: probe_1.txt timed out at the 150s wall (storm); the judge comparison itself
landed on the first try both attempts. Storm resilience: the earlier structure-inventory
call died twice (EmptyStreamError + wall) — the structure was instead established by
pixel measurement (measure4-10), which the later crop comparisons corroborated.

## Dense-region crop comparisons (mandatory self-check item 6) — ALL PASS

Banked under `qa/slide020/cropcheck*_*.txt` (render crop vs original crop, upscaled,
same ground rules). Rounds 1-4 drove the fixes; final states:
- `cropcheck5_row2_strips.txt` — PASS (pink cell 3rd of 6 ✓, gradient fills ✓, subscripts ✓)
- `cropcheck6_delta_bolt.txt` — PASS (pin triangles, +δ, dashed rule, red arrows ✓; the
  "yellow dashed arcs" a round-2 judge flagged were pixel-proven to be glyph fringes:
  41 px, all co-located with the 6 pins — JPEG artifact per ground rule (b), not drawn)
- `cropcheck8_inset.txt` — PASS (after the round-8 mirror fix: "~" LEFT, "+" RIGHT)

## Closed-loop self-checks

`selfcheck_attempt_*.py` + `_output.txt` banked (element-by-element render-ink vs
original-measured bbox, tol ~6 frame px) — attempt 13: **ALL OK** (14 element checks +
containment). `house_chrome_check.py`: **PASS** on every render.

## P2 pattern-group head — convention banked for members 21/22/34

- `qa/slide020/p2_row_lane_pattern.js` — the row-lane/banner/palette convention as a
  documented, commented pattern (chrome import, mapping fit, lane table, shared column
  grid, cell-strip gradient fills, thin-shaft+triangle arrows, raster-brace mechanism,
  marks chain, label typography, closed-loop discipline). **Members: re-measure YOUR
  frame, mirror the convention, do NOT clone this composition.**
- Group-shared measured constants (slide 020 frame): column centers 211.5+73.4k (gap
  after k=5; cols 7/8 at 769.5/843.5); ellipsis dots 5× at x 630-708; lane right edges
  ~883 (+ the red grouping verticals at 887-890); mapping ax 18.628 sx 0.961231.

## Artifacts

- Build: `build/slide_020.js` (+ `build/assets/brace_020.png`)
- Per-attempt provenance: `qa/slide020/build_attempt_1..13.js`, `render_1..13.png`
- Judge: `judge_prompt_1/2.txt`, `judge_attempt_1/2.txt`, `probe_1.txt`
- Crop checks: `cropcheck*_row2_strips/delta_bolt/inset.txt`
- Self-checks: `selfcheck_attempt_*.py` + `_output.txt`
- Measurements: `scratch/slide020/measure1..10_output.txt` (+ gen_brace_png.py)
- P2 pattern asset: `qa/slide020/p2_row_lane_pattern.js`

## Residual notes (all judged MINOR / ruled usable)

1. Right-edge grouping mark drawn as a red dashed vertical (measured) where the judge
   reads a curly brace — ruled usable ("semantic function … fully preserved").
2. Embedding-strip cell internals approximated (6 cells, measured gradient) vs the
   original's blurred ~7-cell look.
3. Ellipsis dots a touch larger; bottom-brace curvature approximated by the raster
   underbrace's straight-spine + V-cusp design.
4. The "yellow dashed arcs" and "extra orange marker" flags from early crop rounds were
   pixel-proven JPEG fringes / spec over-description and correctly NOT drawn.
