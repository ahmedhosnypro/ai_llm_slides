# Legs status — slide 015, attempt 4 (judge legs; live run)

Worker `w015-buildfirst-20261024`. This file is the LIVE congestion record for
the verdict legs. It is updated as the run proceeds; the final adjudication and
certification outcome is appended to `worker_report.md`.

## Observed gateway load (fleet-global, `pgrep -c -f analyze_image.py`)

All observations are from the same run; times are UTC.

| time | gate | note |
|---|---|---|
| 11:09 | 9 | first probe this session |
| 11:11 | 8 | |
| 11:13 | 12 | |
| 11:22 | 17 | |
| 11:28 | 25 | |
| 11:30 | 22 | legs run #1 start |
| 11:46 | 20 | |
| 11:50 | 17 | |
| 11:54 | 15 | |
| 11:58 | 13 | lowest observed; still > 8 |
| 12:02 | 14 | |
| 12:10 | 22 | |
| 12:18 | 22 | legs run #1 tool-wall killed (no vision call ever dispatched) |
| 12:25 | 51 | peak |
| 12:2x | 44-48 | legs run #2 start (4h patient wait) |

**No vision call has been dispatched from this worker at any point**: the gate
never read `< 8`. Per gate law no leg was forced through, so **no
`FINAL VERDICT:` line exists for slide 015** and the slide is NOT certified.

The 14-25 concurrent `analyze_image.py` are **sibling lanes of deck 03 itself**
(measured via `ps`), not load from other decks — i.e. the congestion is local
to this deck's remaining slides, and it is not caused by this worker.

## What was verified independently (non-vision, banked, this session)

Re-measured on `render_4.png` vs `unique_slides/slide_015.jpg` with a fresh
script (`scratch/tmp/adjud_015_generic.py`, frame-px boxes, render scaled by
2001/960, both images sampled at equal effective scale):

| region | width ratio r/orig | height ratio | verdict |
|---|---|---|---|
| eq1_l1 | 0.88 | ~1.16 | forced narrow — see below |
| eq1_l2 | 0.87 | ~1.21 | forced narrow — see below |
| eq1_l3 | 0.90 | ~1.14 | forced narrow — see below |
| redbox_eq | 0.98 | — | matches the banked ratio 1.00 |
| normal | 0.93 | 1.00 | |
| solution | 0.76 | ~0.9 | forced narrow — see below |
| redbox_sent | 0.99 | 0.70 | line height only |
| deriv_l1 | 0.99 | 0.91 | |
| deriv_l2 | 0.97 | 1.00 | |
| peach_eq | 0.97 | 0.82 | |
| Remember | 1.02 | 0.65 | |

These reproduce the banked numbers exactly (eq1 0.87-0.90, solution 0.76),
which is the pre-condition for refuting any repeat finding.

### Geometric forcing, re-proved

Matching the original's width at the render's own ink aspect ratio would
require more ink height than the enclosing band allows, so the narrow widths
are forced rather than fixable:

| region | render wxh | aspect | orig width | height needed | band available |
|---|---|---|---|---|---|
| eq1_l1 | 610x50 | 12.20 | 694 | 56.9 | 44 |
| eq1_l2 | 575x51 | 11.27 | 663 | 58.8 | 47 |
| eq1_l3 | 500x51 | 9.80 | 555 | 56.6 | 45 |
| solution | 248x36 | 6.89 | 325 | 47.2 | 40 (green box interior) |

Each needed height exceeds its band, so widening to the original's width makes
the stacked lines collide / overflows its box. Recorded, not "fixed".

### Arrow adjudication re-confirmed

`adjud_015_generic.py arrow_gap` on the *strictly interior* gap
`x511..546, y466..521` at `luma<200`: **0 ink px in the original** (and 0 in the
render). The claimed right-pointing arrow after the normal-equation line does
not exist. Never add it.

Note for future measurements: measuring a gap that *includes* the boundary
columns (x510 or x547) picks up the equation's closing paren and the green
box's left edge and yields a false ~45 px signal. Interior-only measurement is
the correct one, and the correct one says zero.

### Crop pairs (fairness precondition)

All five pairs are exactly co-dimensioned, so no drift can be fabricated by
scale mismatch: eq_stack 1481x358, pinkbox 1329x121, peachbox 242x140,
deriv_stack 933x277, solution 727x121 (render and orig identical in each).

## Resume commands (nothing to redo; the bank is intact)

```bash
cd <repo root>
pgrep -c -f analyze_image.py            # must read < 8 before ANY call

# whole leg sequence, gate-policed, 4h patience per leg:
bash scratch/tmp/lorch15_main.sh        # probe -> judgeA (this file's live run)
bash scratch/tmp/lorch15_crops.sh       # the five Procedure B crop legs

# or leg by leg, exactly as banked:
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_015/dispatch_driver_4.sh probe
bash .../dispatch_driver_4.sh judgeA
bash .../dispatch_driver_4.sh crop eq_stack   # then pinkbox peachbox deriv_stack solution
```

Legs land at `qa/slide_015/probe_4.txt`, `judge_attempt_4.txt` and
`crop_4_<slug>_judge.txt`. A leg counts only when its transcript carries a real
`FINAL VERDICT:` line.

## Certification sequence (unchanged, for whoever lands the verdicts)

`claim()` resets `gen_status` to `building` (`scripts/15_progress.py:337`), so
`set gen_status passed` must be the LAST content write before `release`, and
`get 15` must be re-read after it. Final row must read
`gen_status=passed`, `visual_check=PASS`, `worker_id=""`.
