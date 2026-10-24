# Worker report — slide 042 "Iteration 1"

Deck: `videos/machine-learning/03_ridger_regression_gradient_descent`
Lane: build + visual judge (both legs)
Worker: `worker-fresh-02`

## Deliverable

- **pptx**: `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_042_recreated.pptx`
  (single plain-named version, per founder single-version law)
- **build script**: `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_042.js`
- **final render**: `recreated_pptx/qa/slide042/render_10.png` (150 dpi)

## What the slide contains

Perceptron iteration-1 worked example: top-left x1..x6 vector table with C1/C2 class
row, top-centre `Initial W = (4;-2)` + red italic `Step η = 2`, top-right
check-classes matrix with the colour legend, left-middle "Upgraded Vectors (From Top)"
table, a red "Iteration 1" badge, and a five-box right computation stack for
`d(x1)..d(x5)` with update/keep actions and W matrices.

## Frame measurements (960×540, 1px = 1pt)

Measured from `unique_slides/slide_042.jpg` with PIL. Banked in
`qa/slide042/` (`calibrate_*.txt`, `final_verify.txt`, `selfcheck_*.txt`) and the
scratch scans under `scratch/tmp/eq042/`.

| region | measured geometry |
|---|---|
| blue-bordered box | x68..720, y54..130, border 0000FF 1pt, **white** interior |
| top-left table | caption y64..73 blue; digit band A y79..91; digit band B y94..105; class row y110..123 (C1 red x90..137, C2 blue x158..205); red ⇒ x239..253 |
| top-centre | `Initial W =` x266..323 y75..84; matrix parens x330..353 y63..102; `Step η = 2` red italic x365..435 y66..80 |
| top-right | `Check classes of` x499..582 y79..88; Z header y64..76 x601..655; Z digits y82..108; **legend x257..508 y110..123** |
| legend colours | black `C1 positive,` x257..302 — blue `C2` x310..326 — black ` negative,` x330..378 — green `Zero` x395..423 — black ` is unaccepted` x430..508 (**no red in the legend: the frame has zero red ink there**) |
| left-middle | caption x81..234 y148..159; **four** digit bands y166..175 / 183..191 / 195..211 / 214..222; class row y231..243 |
| LM parens | thin 1px strokes per column at (93,107), (115,128), (137,150), (173,182), (205,218), spanning the four bands |
| iteration badge | red rect **x84..214, y277..305** (not x54..200), white bold text x99..197 y284..298 |
| right stack | **five white boxes** x276..898 at y228..261 / 272..327 / 338..393 / 404..459 / 470..527, separated by **panel-gray gaps** (NOT black rules — the frame's gap rows carry zero dark ink) |
| green marks | present in every box at x~384..406; boxes 3–5 also at x~736..750 |

Table values (cross-checked against `analysis/slide_042_final.json`):

- top-left columns: x1=(1,1) x2=(2,1) x3=(1,2) x4=(5,4) x5=(6,5) x6=(6,6)
  (band A = 1,2,1,5,6,6; band B = 1,1,2,4,5,6)
- left-middle band1 = 1,1,1,2,1,1; band2 = all 1; band3 = all 1; band4 = 1,2,1,5,6,6
- check-classes: Z1=(0,0) Z2=(7,6) Z3=(3,2)
- stack: d(x1)=…=0 → Update Weight → W=(4;-2)+2·(1;1)=(6;0);
  d(x2)=…=6 → Keep same Weight → W=(6;0);
  d(x3)=…=6 → Keep same Weight → W=(6;0);
  d(x4)=…=6 → Update Weight → W=(6;0)-2·(1;5)=(4;-10);
  d(x5)=…=-96 → Keep same Weight → W=(4;-10)

## Build iterations (all banked in `qa/slide042/`)

| K | what changed |
|---|---|
| 1 | first run; structure roughly right, several metrics off |
| 2 | white content areas + white stack boxes replacing black rules; badge corrected to x84..214 y277..305; legend rebuilt |
| 3 | font-size calibration pass (from `calibrate.txt` render-vs-frame width ratios) |
| 4 | **legend fix**: pptxgenjs emits `<a:pPr>` between rich-text runs, which breaks the run sequence — replaced the single multi-run `addText` with five separate per-colour text boxes |
| 5 | `d(x_i) =` label: the Unicode subscript glyph renders far too wide; replaced with adjacent `d(x` + small digit + `) =` boxes |
| 6 | tightened label box widths |
| 7 | raised text boxes to stop descender spill into the gray gaps |
| 8 | compressed matrix row pitch 12px → 11px; tightened line-B box heights |
| 9 | raised line B per box → **all four gaps verified ink-free** |
| 10 | **LM parens**: 48pt glyph parens swallowed the digits (render y179..223 vs frame thin strokes) — replaced with thin 0.75pt line shapes + top/bottom hooks; 84/84 self-checks pass |

## Self-check

`qa/slide042/selfcheck_attempt_10.py` — 84/84 PASS on `render_10.png`, covering
the blue box and its four edges, both TL digit bands, TL class-row colours, the red
arrow, `Initial W =` + matrix parens + `Step η`, the check-classes caption/header/digits,
all five legend segments in order (and confirming **no red** in the legend, matching
the frame), the LM caption, all four LM digit bands, the LM paren span, the LM class row,
the badge rect edges and white text, five white boxes at their measured y-ranges with
the panel gaps ink-free (no black rules), the green marks, and the red `Update Weight`
occurrences.

`shared_patterns/house_chrome_check.py render_10.png 42` → **PASS**

## Visual judge legs

| leg | variant | transcript |
|---|---|---|
| A | full-slide comparison, `render_10.png` vs original | `qa/slide042/judge_attempt_10.txt` |
| B | zoomed crop-pairs (`stack`, `tl_table`, `lm_table`, `topright`, `legend`), matched effective scale LANCZOS ×2.0833 | `qa/slide042/crop_10_*_judge.txt` |

Crop pairs are cut from slide-space regions with 8px padding; the original crop is
LANCZOS-upscaled to the render's pixel dimensions so both sides have identical
effective scale (see the Procedure B law in `shared_patterns/judge_protocol_03.md`).
