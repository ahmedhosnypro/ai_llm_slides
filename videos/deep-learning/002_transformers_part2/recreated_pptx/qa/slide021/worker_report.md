# worker_report.md — slide 021 ("[1] Position Encoding", P2#2) — CERTIFIED

**Slide:** 21 (NNN 021) — video `002_transformers_part2`, pattern group P2 member #2 of [20, 21, 22, 34]
**Verdict:** **PASS** (judge attempt 1; transcript `judge_attempt_1.txt`)
**Deliverable (single-version):** `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_021_recreated.pptx`
**Build script:** `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_021.js`
**DB row at close:** gen_status=passed · visual_check=PASS · visual_attempts=1 · visual_transcript=judge_attempt_1.txt

## Resume note

This run RESUMED a builder killed in the fleet-wide provider interruption. Inherited
state: `qa/slide021/` was EMPTY (no banked renders/judges — no build script existed);
`scratch/slide021/` held measure1-3 + 2x crops from the dead builder. All measurement
was re-done independently (measure4-8, this run) with the dead builder's numbers used
as cross-checks — several of its readings were corrected (its red-filter missed the
L1/L3/L4 right edges; its "row3 boxes y[289,330]" conflated lane fill with box ink;
its chrome right/bottom centroids were contaminated by the blue box border and
letterbox). No banked evidence was overwritten. Judge attempt numbering: 1.

## Frame→slide mapping (re-derived from THIS frame's four chrome landmarks)

Red-weighted subpixel centroids: left 58.60, right 901.38, top 43.14, bottom 516
(letterbox edge) →

    slide_x = (frame_x − 18.13) / 0.961231 ;  slide_y = frame_y / 0.955556

Same fit class as certified 002/003/020 (020's ax 18.628 — its left stroke sits
1 frame px right of 021's). Badge cross-check: frame badge center (875.5, 71.0) →
slide (892.7, 74.3) vs house (893, 71) — the usual 1-4px JPEG-bbox offset class.

## Key structural findings (all pixel-verified, several overriding the spec)

1. **Row1 lane is a FILLED lavender lane** (C8C5F6, dashed dark-violet 2E2A62
   border — vertical dash cores 2A275C + JPEG blend math) with 8 boxes
   (CFCEF8 fill) y[144,165]; digits sit +3.5 frame px right of box centers
   (systematic across all 8 — reproduced with a label dx).
2. **Row3 vector boxes are KHAKI-bordered** (D1CBAA) rects y[300,321.5] with no
   distinct fill inside the green lane (EBFFD8, dashed 5A8568) — NOT the spec's
   "green outlines"; the spec's D5EED5 fill/green outline is a vision misread.
   Empty gap between Vector_P5 and Vector_PN-2 (no dots) ✓ spec.
3. **"Vector" labels are serif bold-italic** (Times-class, crop-judge-verified
   round 2; consistent with 020's certified diagram-label convention), not the
   spec's sans. Subscripts red italic, smaller, baseline-aligned.
4. **ybox typography solved by metric fit:** the ink-width ratio triple
   (L2/L1 1.087, L4/L2 1.384, L4/L1 1.504) matches Arial mixed-weight
   (bold "[1]"/"[2]" prefixes + word-only bold "Fixed"/"TRAINABLE" + regular
   "Function with"/"Parameters") at a single em 16.1 (±0.4%); every installed
   serif breaks a ratio by 5-9% and LiberationSerif would overflow the box.
   The "[1]"/"[2]" prefixes are DARK BLUE, not red (pixel census: 0 red px,
   ~100 blue px per prefix) — spec's red claim is a vision misread.
5. **Navy bar** 0000A6 (census) with tracked text: yellow "function" em 20.5
   cs 1.7 + white em 18.5 cs 0.67 (ink widths matched to ≤1px).
6. **NO right-edge red verticals** on 021 (020 had them at x 887-890) — checked
   (red census over x 884-899 = 0), correctly not drawn. Letterbox + mouse
   cursor omitted per ground rules (b)/(c).
7. **Title** em 40 (width-fitted; cap-height class agrees), two-color runs
   AE1120 / 00009C (census of the large glyphs).

## Build iterations (renders 1-17, all pre-judge; house chrome PASS on every render)

- render_1: first full build; selfcheck_attempt_1 drove em/position fixes
  (several selfcheck "fails" were window/filter artifacts — documented in
  selfcheck_attempt_2/3).
- render_2-4: text ems + tracking (navy), title em 40, digit dx +3.5,
  ybox em; selfcheck windows corrected (mixed-units bug, stale dead-builder
  expected bboxes replaced with this run's direct measurements).
- render_5: crop-judge round 1 (row3) caught a BLOCKER — the khaki box rects
  had been dropped when the Vector labels were re-pinned; restored.
- render_6-7: Vector labels → Times bold-italic em 15.6 with −3px dx
  (width-matched: ink 78px = target).
- render_8-10: ybox selective bolding (crop-judge round 1) → regular
  L1/L3 + bold L2/L4; then word-only bold spans + prefix bold (round 2).
- render_11-13: ybox font investigations — Times (ratio ✗), DejaVu Serif
  (bold-pair ratio ✓ but mixed-model ✗), settled Arial mixed-weight em 16.1
  (all three original ratios matched; cropcheck3_ybox PASS with zero
  discrepancies).
- render_14-17: brace — synthetic cusp failed 3 crop rounds (sharp V / blunt
  apex / shallow-lifted apex — round 4 exposed a 1-row trace-crop
  misalignment). Final: **alpha traced from the original's redness field**
  (crop y 336..352 exact, LANCZOS to the 600dpi box, census core 882830);
  apex lands at orig-y 351.34 vs target 351.5; cropcheck5_brace PASS.
- render_17 is the certified render.

## Dense-region crop comparisons (mandatory self-check item 6) — ALL PASS

Banked under `qa/slide021/` (render crop vs original crop, ground rules +
P2 family context, `--thinking high --max-tokens 65536`, gate-routed):
cropcheck_row1.txt (PASS, 5 MINOR), cropcheck2_row3.txt (FAIL → rects),
cropcheck3_row3.txt (PASS, 4 MINOR), cropcheck_navy.txt (PASS),
cropcheck_ybox.txt (FAIL → bolding), cropcheck2_ybox.txt (FAIL → spans/font),
cropcheck3_ybox.txt (PASS, zero discrepancies), cropcheck_gbox.txt (PASS,
2 MINOR), cropcheck_brace/2/3/4.txt (FAIL ×4 → traced-alpha),
cropcheck5_brace.txt (PASS, residual MINORs), cropcheck_tanline.txt (PASS),
cropcheck_labels.txt (PASS). Also `judge_unttemplated_precheck.txt` — a
comparison run WITHOUT the frozen `-p` (worker error, immediately re-run
templated; banked for transparency, not counted as an attempt).

## Closed-loop self-checks

`selfcheck_attempt_1..4.py` + `_output.txt` banked: render-ink vs
original-measured bbox, tol ~4.5px @150dpi. Final state (attempt 4): all
elements within tolerance except documented ≤6.7px right-edge width deltas on
three 15pt ybox lines (2-3% em noise; the L1/L3-vs-L2/L4 width conflict is
resolved by the mixed-weight model — see above) and the title bracket-top
(Arial's bracket does not overshoot caps; original's does by ~2 frame px).
`house_chrome_check.py`: **PASS on every render**.

## Judge attempts (frozen `-p` template with ground rules; gate-routed; banked)

| # | Render | Verdict | Transcript | Key findings |
|---|--------|---------|-----------|--------------|
| 1 | render_17 | **PASS** | judge_attempt_1.txt | 3 MINORs, no BLOCKER/MAJOR: (1) tan-line terminus lands "just left of the green box corner" vs the original's corner-anchored end (medium conf); (2) ellipsis dot count "5 vs ~6" (low conf — the original has exactly 5, pixel-measured; the 5th partially fuses in JPEG); (3) the tan line crosses the brace "slightly more prominently" (the traced-alpha brace carries JPEG halo). All text verbatim, all regions present, containment respected, brace spans the full vector row. |

Storm resilience: the probe window hung silently twice (gateway congestion);
the judge comparison itself landed first try. Judge procedure executed by the
worker via Bash per the banked prompt (no Agent/Task spawn tool in this
environment — orchestrator-approved fallback).

## P2 pattern-group verification + banking

- Shared-block verification vs the certified P2 head (slide020/render_13):
  chrome-top zone mean|d| = 0.57 (0.41% px >30 = the by-design badge numeral
  20→21), left canvas strip mean|d| = 0.00 — the shared chrome and lane
  mechanics are pixel-consistent.
- Banked for members 22/34: `qa/slide021/p2_member_notes_021.js` (per-frame
  re-measure workflow, 021's lane/grid/typography facts, the traced-alpha
  brace mechanism, the no-right-verticals finding).

## Artifacts

- Build: `build/slide_021.js` (+ `build/assets/brace_021.png`)
- Per-attempt provenance: `qa/slide021/build_attempt_1.js`, `render_1..17.png`
- Judge: `judge_prompt_1.txt`, `judge_attempt_1.txt`, `probe_1.txt` (empty —
  gateway hang), `judge_unttemplated_precheck.txt`
- Crop checks: `cropcheck*_*.txt` (13 transcripts)
- Self-checks: `selfcheck_attempt_1..4.py` + `_output.txt`
- Measurements: `scratch/slide021/measure1..8*.py/_output.txt`,
  `gen_brace_png.py`, `render_crops/`
- P2 member notes: `p2_member_notes_021.js`

## Residual notes (all judged MINOR / ruled usable)

1. Tan-line terminus: mine stops ~4pt short of the green box's top-left
   corner (the original reads corner-anchored; the measured pixels end at
   (302, 380) with nothing detectable at rows 372-380 — the faint jog, if any,
   is below JPEG detectability). Drawn to the measured end.
2. Ellipsis dots: 5 (pixel-measured); slightly heavier than the original's.
3. The traced-alpha brace carries a faint JPEG halo from its source (the
   original's own softness); the full-slide judge ruled it a faithful
   reproduction of the original's hand-drawn ink.
