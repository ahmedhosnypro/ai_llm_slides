# Worker report — slide 053 (002_transformers_part2), Deep Learning DSAI 308

**Slide:** "Self Attention Look Ahead Mask (Used in  Decoder first Block )" — root slide,
no dependencies, no pattern group. Built end-to-end 2026-10-12.

## Deliverables (single-version law)

- **PPTX:** `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_053_recreated.pptx`
  (build → judge PASS → OMML v2 wrap applied to this same file; LibreOffice render of the
  wrapped file is pixel-identical to the certified render, 0 of 2,251,125 px differ).
- **Build script:** `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_053.js`
  (pptxgenjs; imports `videos/deep-learning/shared_patterns/house_chrome.js`,
  numeral 53; embeds `build/assets/eq_053_softmax.png`).
- **Equation asset:** `recreated_pptx/build/assets/eq_053_softmax.png`
  (matplotlib mathtext `\sigma(x_j)=\frac{e^{x_j}}{\sum_i e^{x_i}}`, 600 dpi, 20.7 pt,
  black; sidecar values re-derived into the OMML manifest
  `qa/slide053/eq_053_manifest.json`; wrapper: rId1 wrapped v2).

## Geometry / method

- Frame→slide mapping fitted from THIS frame's four chrome landmarks (left 58.67,
  right 900.51, top 43.23, bottom 516.45): slide_x=(fx−18.45)/0.95991,
  slide_y=(fy+0.29)/0.95600. Badge cross-check (875,71)→(891.4,74.6) vs house (893,71),
  within ~3 px JPEG noise.
- All content placed from PIL ink measurements (scratch/slide053/measure_chrome.py …
  measure7.py); closed-loop ink check iterated over 4 renders to bring every element's
  ink edges within ~2 pt of the mapped targets (`selfcheck_attempt_1/1b/2.py`).
- House chrome check: PASS on every render (`shared_patterns/house_chrome_check.py`).

## Attempts (judge = frozen `-p` template with ground rules, `--thinking high --max-tokens 65536`)

Mandatory pre-judge zoomed crop comparisons (self-check 6) + full-slide judge:

| Attempt | Render | Check | Verdict | Notes |
|---|---|---|---|---|
| 1 | render_1.png | house chrome + closed-loop | — | zone-contaminated reads; title em 24→24.3, stmt lines 17→16.7/16.8→16.7, digits −1.9 pt, eq 20.2→20.7 pt |
| 4 (crops) | render_4.png | eq-box crop (cmp_eqbox.txt) | FAIL→ | judge misread the ORIGINAL as vertically centered; PIL shows the original's equation also sits high (10/19 pt gaps); retry with PIL facts in `--view`: **PASS** (cmp_eqbox_retry.txt) |
| 4 (crops) | render_4.png | matrix crop | PASS | cmp_matrix.txt |
| 4 (full) | render_4.png | full judge (judge_attempt_4.txt) | **FAIL** | BLOCKER: "−∞ values omitted from the 10 masked cells" (my build had solid red blocks) |
| — | — | pixel forensics | — | full RGB dump proved the original's masked cells are SALMON CHIPS (E3AA8A) with 7E4027 borders and a dark-red "−∞" value each — my red>55 mask had hidden this; build fixed |
| 5/6 (crops) | render_6.png | matrix crop retry | FAIL→PASS | first retry run hit my own crop-window bug (container top/bottom borders cropped out); regenerated crop including the full container: **PASS** (cmp_matrix_attempt6_retry.txt). The judge's "diagonal should be corner-to-corner" note is contradicted by PIL: the original's green/mauve boundary starts 27 pt right of the top-left corner; the render matches the measured boundary. |
| 5 (full) | render_6.png | full judge (judge_attempt_5.txt) | **PASS** | 3 MINOR cosmetic notes (panel proportion, diagonal end, malade tag height) — no BLOCKER/MAJOR |

**Final verdict: PASS** on judge attempt 5 (real comparison transcript:
`qa/slide053/judge_attempt_5.txt`).

## Frame-vs-spec deviations (frame ground truth wins; recorded in slide_053_source/SOURCES.md)

1. Subtitle split: RED "(Used in  Decoder " + BLUE "first Block " + RED ")" — the spec's
   "blue Decoder first Block" was a vision error (PIL advance fit).
2. Statement box: ONE blue box contains all three lines (spec drew box + separate lines).
3. Masked cells: salmon chips + dark-red "−∞" (spec said mauve field + red −∞; my first
   build said solid red blocks — both corrected by pixel forensics).
4. Upper-triangle field #C4ACA0 (spec #A87C7C); diagonal starts 27 pt right of the corner
   (spec said corner-to-corner); title 24.3 pt (spec ~28 pt).

## Evidence index (qa/slide053/)

- judge_prompt_1.txt (frozen substituted prompt), build_attempt_1.js / build_attempt_4.js /
  build_attempt_6.js (per-attempt provenance)
- render_1..6.png + render_final_omml.png (150 dpi renders; render_6 = certified pre-wrap,
  render_final_omml = post-wrap, pixel-identical)
- crops/: orig_eqbox/render_eqbox, orig_matrix/render_matrix, cmp_eqbox.txt (FAIL),
  cmp_eqbox_retry.txt (PASS), cmp_matrix.txt (PASS), cmp_matrix_attempt6.txt (FAIL, crop
  artifact), cmp_matrix_attempt6_retry.txt (PASS)
- judge_attempt_4.txt (FAIL), judge_attempt_5.txt (PASS — certification transcript)
- eq_053_manifest.json (OMML wrap manifest), selfcheck_attempt_1/1b/2.py

## Notes

- Judge procedure executed by the worker (no spawn/Agent tool available in this
  environment) — orchestrator-approved fallback, byte-for-byte per the banked prompt,
  vision through `scripts/16_vision_gate.sh` (default `images` route, one probe per
  dispatch, `--thinking high --max-tokens 65536`, W4 540 s wall, no gate hangs observed).
- OMML wrap: applied post-certification to the single plain-named deliverable;
  LO render verified pixel-identical (0/2,251,125 px); file never LO-resaved after wrap.
- Component banking obligation: slide 053 has no dependents in any video's dependency
  graph (root slide; not a cross-video parent), so no component export is required.
