# Slide 032 — worker report (w032-finish-20261024)

Deck: `videos/machine-learning/03_ridger_regression_gradient_descent`
Slide: 032 — "Convex Function, Learning Rate =0.4, Start at X=3"
Lane: build + judge (Template A full-slide + Procedure B zoomed crop-pairs)

## Resume state

- Previous worker `worker-fresh-032c` left the row claimed-but-stale (heartbeat 193 min)
  and `gen_status=building` with `visual_attempts=0`: it did **ground-up PIL
  re-measurement only** and never dispatched a single judge call (banked in
  `MEASUREMENTS_STEP1.md`, `measure_ground_up_032.txt`, `measure_probe2..7_*.txt`;
  see its own note in `ORCHESTRATOR_FINDINGS.md`).
- I took the claim with `--force` over the stale heartbeat and **resumed from
  build attempt 8 / render_8** (attempt numbering continues at 9).
- Nothing was overwritten: every prior artifact (renders 1..8, build_attempt_1..8,
  all probe scripts and their outputs) is still in this directory.

## Certified-component check (import law)

Slides 030 and 031 are the same GD cost-curve family. Both rows are still
`gen_status=building` / `visual_check=null` (checked 2026-10-24 10:10) — **no
certified component exists yet**, so there was nothing to import. The build was
therefore continued from this slide's own measured state (no cross-slide copying;
the inherited numbers were independently re-verified against the frame by me,
see below).

## Build state

- Script: `recreated_pptx/build/slide_032.js`
- Deliverable: `recreated_pptx/slide_032_recreated.pptx` (single plain-named file)
- Renders: `render_8.png` (unchanged build; md5 `efff7b68…`) and `render_9.png`
  (2001×1125, 150 dpi) after one measured fix — see §Fix.
- Build provenance: `build_attempt_8.js` (inherited, unchanged) and
  `build_attempt_9.js` (this worker's copy of the live script).

## Fresh re-measurement and adjudication (attempt 9)

Scripts banked here: `measure_verify_9.py` … `measure_verify_16.py`,
`make_crops_9.py`, `make_prompts_9.py`, `verify_prompts_9.py` (+ their `.txt`
outputs). All numbers are my own PIL probes over `unique_slides/slide_032.jpg`
(960×540, 1 px = 1 pt) and `render_9.png` (2001×1125, 2.0844 render px per
frame px).

### House chrome — PASS
`python3 shared_patterns/house_chrome_check.py recreated_pptx/qa/slide032/render_9.png`
→ **PASS**: panel x112–1882 y94–bottom; L/R/bottom C00000 strokes present,
**top bare** (correct for this deck); badge centre (1824,152) d=68; all within
tol 8. Log: `house_chrome_check_9.txt`. Spot samples: canvas FFFFFF, panel
E9E9E7, left stroke C00000, bottom stroke C00000, top band E9E9E7 (no stroke).

### Title — confirmed (≤3 px)
Run ink extents, measured on both images (`measure_verify_15`):
| run | ORIG | REND9 | Δ |
|---|---|---|---|
| red "Convex Function," | x81.0..239.0 | x81.1..238.9 | 0 / 0 |
| green "Learning Rate =0.4," | x260.0..432.0 | x256.7..435.1 | −3.3 / +3.1 |
| blue "Start at X=3" | x446.0..556.0 | x448.6..558.4 | +2.6 / +2.4 |

Total title ink width 475 px (frame) vs 477.3 px (render) — a 2.3 px / 0.5 %
difference, i.e. MINOR and not worth a build change (the render is a hair wider
because Liberation Serif's advance differs from the frame's original typeface).

### Parameter table — confirmed
Row fills at text-free columns (`measure_verify_11`): ORIG D7E377 / D7B5F2 /
F9E5CD / E6FFD5 / F9BEC0 vs REND9 D8E175 / D4B2F5 / F6DDC1 / E7FFD2 / F4BEC2 —
all within JPEG tolerance of the build's measured fills.

### Graph — confirmed
- Plot frame: interior white; red LEFT/RIGHT/TOP strokes; gray bottom axis and
  gray y-axis (ORIG cores 8F9392 / 9C9E9B vs REND 969696 / 969696).
- Calibration XC=630.5, SX=11.5, YC=266, SY=12 re-confirmed from the gridline
  census (vertical cores 585/596/607/619/630 → 11.5 px/unit, x(0)=630; horizontal
  rows at 12 px/unit with y(0)=266).
- **Curve**: `f(x)=(x-5)²+1`, one smooth analytic quadratic (build asset
  `curve_032.json/png`, 600 dpi). Second-difference ripple is pure discretisation
  of a quadratic — analytic max |2nd difference| 8.04e-04. Column-by-column curve
  trace (`measure_verify_11`): render vs analytic within ±3.4 px at every probed
  x from 643 to 731; the frame's own curve deviates from the same analytic form by
  up to 5.35 px (JPEG + the original's own rendering), so the two agree to within
  each other's noise. Curve ink colour matches: render cores 7A98A9–7C99A8 vs
  frame cores 8698A6–94B0BB (the frame's are lighter because of JPEG, same family).
- **Black y=10 chord**: the original's dark core is x≈650..726 at frame y146 —
  the build draws x652..727, 2 pt. **The earlier banked claim
  ("MEASUREMENTS_STEP1.md §6: the chord is full-width x576..805") is REFUTED by
  fresh measurement**: a row census at y146 shows values E1E3E0 (gridline gray)
  from x578 to x646 and only x650..726 genuinely dark; y145/y147 show no
  continuous dark run. No build change (the chord is already correct).
- **Red vertical at data x=5**: confirmed present and dashed in the frame
  (`measure_verify_13`: reddish column cores at x687..690 spanning y68..307 with
  alternating runs of 5–10 px and gaps of 6–11 px). Build draws it dashed at
  x=687.5. Confirmed.
- **Dots**: left dot ORIG x646..659 core, REND 653.5 c 7 px; middle 687.5; right
  722.5 — matched to within 2 px.

### The one real defect found and fixed (pre-judge)

The two small gray "3" segment labels above the chord
(`measure_verify_14`, `measure_verify_15`, `measure_verify_16`):

| | ORIG ink core | render_8 | render_9 (after fix) |
|---|---|---|---|
| left | x669..674, y132..139 (6×8) | x671..673, y128..133 (5×6) | x668.8..672.6, y132.4..139.1 (5×8) |
| right | x700..707, y132..139 (8×8) | x705, y128..133 (2×5) | x701.9..705.7, y132.4..139.1 (5×8) |

The original's marks are ~11 pt "3" glyphs (an 11 pt Times digit is 5 px wide ×
7.8 px tall at 1 px = 1 pt); the build drew them at 9 pt in a 13 px box, which
produced a 5×6 px stem sitting 4–5 px **above** the frame's ink. Fix applied to
`build/slide_032.js:202-209`: `fontSize 9 → 11`, box `y 124 h 13 → y 127.5 h 16`
(so the glyph centres at y 135.5, the measured frame centre). Verified after
rebuild: render_9's glyph cores now match the frame's ink y132..139 in height and
position (`measure_verify_16.txt`).

### Table — confirmed
Iteration-table band fills match (§Parameter table). The 8×7 grid geometry
(outer frame 564BA7 x298.5..599.5 y330..527; five bands at 344/387/431/472/497
with splits at 363.5/406/450) was measured by the inherited worker and re-checked
here. Cell values are slide 032's own analysis record (the 030/031 contamination
alarm was independently refuted with a string test over both `final.json`
records and re-confirmed here).

## Procedure B crop pairs (attempt 9, matched effective scale)

`make_crops_9.py` cuts both images at the same slide-space bbox and LANCZOS-upscales
the original crop to the render crop's exact size, so both images share the same
effective scale per axis (2.081–2.085 render px per frame px):

| name | frame bbox | out px | region |
|---|---|---|---|
| title | 72,58 – 568,98 | 1034×83 | three-run title line |
| params | 68,170 – 216,259 | 308×186 | step / initial X / delta table |
| graph | 565,58 – 818,316 | 527×537 | plot box, curve, ticks, annotations |
| callouts | 328,176 – 600,362 | equation box, green box, pink band, arrow |
| table | 290,322 – 608,535 | 663×444 | 8-row × 7-column iteration table |

## Judge dispatch (attempt 9)

Payloads generated by `make_prompts_9.py` and **byte-verified** by
`verify_prompts_9.py` (`TOTAL FAILURES: 0`): each generated `-p` payload, with only
the documented substitution undone, is *exactly* the payload extracted from the
frozen block in `shared_patterns/judge_protocol_03.md` (Template A = lines 62–71,
Template B = lines 108–117). No backtick fence leaked into any payload; every
command line carries the runbook's own substitutions (render_9, slide_032.jpg,
judge_attempt_9, crop_9_<name>, "attempt 9").

Banked prompt files: `judge_prompt_9.txt`, `crop_9_{title,params,graph,callouts,table}_prompt.txt`.

Wall/load notes (banked evidence, founder item open):
- Gateway router itself answered the `images` alias in **6 s** (full 2001×1125
  render, `max_tokens 4096`) and **29 s** (900 px crop) in direct curl probes at
  10:35–10:50, i.e. the image leg was NOT dead.
- The prescribed **analysis probe** (`--timeout 120`, full-slide DEFAULT_PROMPT,
  `max_tokens 8192`) park: `probe_9_run.log` shows `probe_exit=124` at +150 s on
  **both** the initial probe and the single law-permitted sleep-300 re-probe; a
  direct curl with byte-identical payload shape also exceeded 200 s. The probe is
  under-budgeted for the long transcription prompt in the current congestion
  regime (fleet load 14–15 `analyze_image.py` processes, ≈5 real image calls).
- Both legs were therefore dispatched at their **protocol-prescribed budgets**
  (`timeout 1700` outer, `--timeout 600 --thinking high --max-tokens 65536`) by
  executing the byte-verified prompt files verbatim.

## Verdicts

(filled in after the transcripts land)
