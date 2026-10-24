# Slide 043 "Perceptron Iteration 2" — worker report (attempt 3)

Worker: `w043-finish-20261024`
Deck: `videos/machine-learning/03_ridger_regression_gradient_descent`
Status: **BUILD CURRENT + 3 REAL DEFECTS FIXED (render_3), VISION LEGS NOT RUN — image-leg wedge**

## DB row at handoff

```
gen_status            building
pptx_path             videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_043_recreated.pptx
build_script          videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_043.js
visual_check          null
visual_attempts       3      (staged, not yet dispatched)
visual_transcript     null
worker_id             w043-finish-20261024
```

## Triage of the inherited bank (all md5/timestamp verified)

| artifact | state | verdict |
|---|---|---|
| `build/slide_043.js` | md5 `43d645a7…`, identical to banked `qa/slide043/build_attempt_2.js` | current, reused as the base |
| `recreated_pptx/slide_043_recreated.pptx` | md5 `69b0dfc7…` | was current w.r.t. that script |
| `qa/slide043/render_2.png` | md5 `9cf70ff9…` | **re-rendered from the pptx and md5-IDENTICAL** — the prior render was genuinely current, not stale |
| `shared_patterns/house_chrome_check.py` on render_2 | PASS (panel x112-1882, y94-bottom; L/R/bottom strokes, top bare; badge (1824,152) d68) | reused |
| `build/assets/eq043_dx*.png|json` (Oct 24 08:33) | **ABANDONED partial rebuild** — only 6 of 22 assets produced; the generator `gen_eq_043.py` carries content typos (`"-0"`, `"02"` in the w specs); neither series is wired into the build | NOT reused |
| `build/components/` | contains slide_009/012/013/017/020/022/027/035 — **no perceptron-family component** | nothing to IMPORT |
| `slide_dependencies.json` | edges only `10>9`, `13>12`, `17>13`, `18>17` | **slide 43 is NOT dependency-gated**; the family note in my task brief is not backed by the founder graph |

## The prior bank's selfcheck was wrong on 2 of 4 claims

`selfcheck_attempt_2.txt` claimed 4 unfixed defects. I re-measured every one against BOTH images
(PIL, frame px, 960×540 original vs 2001×1125 render):

| claim | adjudication | action |
|---|---|---|
| `4b class-row colour` "render is black" | **CONFIRMED REAL** — original has 77 red px at x1..x3 and 32 blue px at x4..x6 (77/3 and 0/32 per-column); render had 0 red, 0 blue | FIXED |
| `3b matrix delimiter` "separate one-line parens per entry" | **CONFIRMED REAL** — original col1 ink bbox x593..617 y83..112 with ONE paren pair spanning both stacked entries (`( 0 ; 0 )`); render drew two separate inline `(0)` `(0)` lines at y83..97 / y110..117 | FIXED |
| `5a aug heading overflow` ink to 247.8 vs box edge 246 | **CONFIRMED REAL but marginal** (1.8 px). Box outline verified identical in both images (ORIG x69..246, REND x69..246 via grayblue-C0C3CA scan) | FIXED |
| `3a initial-W delimiter` "Step text starts inside the bracket; vector has no enclosing delimiter" | **REFUTED** — the original has tall bracket strokes at x331 and x431 spanning y62..101, and `Step η = 2` sits INSIDE them exactly as the render does (verified by full-res ASCII of the original) | no action |

Note the failure mode in the inherited report: `probe_1.txt` (a probe of **render_1**, attempt 1)
described four defects that the report asserted were already fixed in render_2 — but the report
never re-ran the probe or the selfcheck on render_2. The 3 defects above survived into the
deliverable untouched.

## Fixes applied (copy-then-modify; `slide_043_pre_fix.js` backed up in `scratch/tmp/`)

`recreated_pptx/build/slide_043.js` only — three edits:

1. **Class-row colour** (`slide_043.js:97`): `C1`→`C00000`, `C2`→`0000FF`, replacing the
   measured-wrong all-black row.
2. **Class-check matrix** (`slide_043.js:109`): the two inline `(0)/(7)/(3)` and `(0)/(6)/(2)`
   text rows are replaced by three generated 600dpi images (`eq043_mx1/2/3.png`) drawn as ONE
   tall paren pair per Z1 column spanning both stacked entries, centred (605/628/651, 95).
   The images come from `gen_eq_043.py`'s already-correct matrix specs (verified against the
   original: the digits really are `(0;0) (7;6) (3;2)`), which the prior lane had generated
   nothing from.
3. **Aug heading** (`slide_043.js:125`): `x 88 → 79`, `w 170 → 160`, keeping 11pt.

New assets: `recreated_pptx/build/assets/eq043_mx1.png|json`, `eq043_mx2.png|json`,
`eq043_mx3.png|json` (125×222/221/225 px at 600dpi, transparent).

## Verification of the fixes (`selfcheck_attempt_3.py` — output banked)

Rendered `render_3.png` at 2001×1125@150dpi (md5 `a050348c…`), house chrome **PASS**.

- FIX 1: render C1 red = 414 px, C2 blue = 489 px (original 77/32 — same direction, typed ink heavier) → PASS
- FIX 2: matrix paren span 26.4/26.4/26.8 frame px vs original 27/25/27; column bboxes
  REND 597.2..620.7 / 612.0..643.7 / 635.0..658.0 vs ORIG 598..612 / 612..643 / 635..657 → PASS
- FIX 3: heading ink x79.3..212.7, inside the 246 box edge (was 247.8) → PASS
- No regressions: all 6 equation bands inked (4128–5319 px each), frame containment
  (67.7,53.7,893.8,519.3) PASS, 24/24 table cells inked.

## Crop pairs cut for attempt 3 (Procedure B, matched effective scale)

`cropcut_attempt_3.py`; regions re-cut from **render_3** per the re-cut-after-rebuild law:

| region | frame bbox | render crop | orig upscaled | eff px/frame x/y |
|---|---|---|---|---|
| `topband` | 70,50..675,132 | 1261×171 | 1261×171 | 2.0843 / 2.0854 |
| `eqstack` | 268,133..859,535 | 1231×838 | 1231×838 | 2.0829 / 2.0846 |
| `midleft` | 60,130..260,320 | 417×396 | 417×396 | 2.0850 / 2.0842 |

All MATCHED (|eff − render dpi| < 0.005). `render_2 → render_3` region diff proves the
**eqstack region is pixel-identical (0 px changed)** — my three fixes all landed in the top band
and middle-left, so the calc-row stack was untouched.

## BLOCKER — image vision leg wedged (evidence banked)

Both probe dispatches for attempt 3 (`scratch/tmp/043_probe3.sh`, `043_probe3b.sh`, each under
the protocol's `timeout 150`) returned **EXIT_PROBE=124 with zero output and no transcript**.

Banked in `qa/slide043/wedge_evidence_3.txt` (+ `wedge_probe_attempt_3.py`):

- Queue depth 9→12 `analyze_image.py` processes, **9/9 at <1% CPU** in `futex_wait_queue` /
  `do_wait`, cputime 00:00:00, elapsed 39–274s — blocked on network I/O, not computing.
- Direct router measurements in the same window: `images` route (the analyzer's only
  `DEFAULT_MODELS` entry, `analyze_image.py:30`) **32.9s** for a 30-token image request;
  `nemotron-3.5-super-vl-120b-a12b` **1.7s**; text leg 0.5s (also seen at 31.6s in an earlier
  window).
- So: router alive and serving, text leg swings between 0.5s and 31.6s, the `images` virtual
  route is ~19× the direct VL route. A full-frame (2001×1125) analysis cannot complete inside
  the probe's `timeout 150` wrapper on that route, and the real judge's `timeout 600` /
  `timeout 1700` walls are at high risk for the same reason.

**Nothing was recorded as PASS.** No `visual_check`, no `visual_transcript`, no
`gen_status=passed` was written, because no judge leg produced a banked verdict with a
`FINAL VERDICT:` line. `gen_status` stays `building`.

## Files touched

- `recreated_pptx/build/slide_043.js` — the three fixes above (+ stale header comments corrected).
- `recreated_pptx/build/assets/eq043_mx1.png|json`, `eq043_mx2.png|json`, `eq043_mx3.png|json` — new.
- `recreated_pptx/slide_043_recreated.pptx` — rebuilt, md5 now differs from the inherited one.
- `recreated_pptx/qa/slide043/` — `render_3.png`, `selfcheck_attempt_3.py`, `cropcut_attempt_3.py`,
  `crop_3_topband_{render,orig}.png`, `crop_3_eqstack_{render,orig}.png`,
  `crop_3_midleft_{render,orig}.png`, `judge_prompt_3.txt`, `crop_prompt_3_{topband,eqstack,midleft}.txt`,
  `crop_prompt_3_*_desc.txt`, `wedge_probe_attempt_3.py`, `wedge_evidence_3.txt`,
  `build_attempt_2.js.md5guard`, this report.
- `scratch/tmp/` — `043_adj.py`, `043_ascii.py`, `043_initw.py`, `043_wdef.py`,
  `043_verify_fixes.py`, `043_cut_crops.py`, `043_verify_cur.sh`, `043_render_att3.sh`,
  `043_leg_a.sh`, `043_leg_b.sh`, `043_probe3.sh`, `043_probe3{,.b}.log`,
  `043_wedge_probe.py`, `slide_043_pre_fix.js`.
- No banked evidence deleted. No slide outside 43 touched.

## To finish this slide (next worker, fully staged)

The build side is DONE. Only the two judge legs remain. Staged dispatch scripts are banked and
runnable verbatim:

```bash
cd /worksp""aces/codespaces-blank/ai_llm_slides
# option 1 — the staged wrapper (heartbeats the DB, then dispatches):
bash scratch/tmp/043_leg_a.sh                      # Leg A: full-slide Template A on render_3
bash scratch/tmp/043_leg_b.sh topband              # Leg B: 3 dense regions, one call each
bash scratch/tmp/043_leg_b.sh eqstack
bash scratch/tmp/043_leg_b.sh midleft

# option 2 — re-arm the probe first if the gateway looks wedged again:
bash scratch/tmp/043_probe3.sh
```

Payloads are already banked and byte-verified: `judge_prompt_3.txt` (4115 bytes, identical to the
Template A template with `NNN→043`; the template contains **zero** standalone `\bK\b` tokens so the
attempt number never alters it — `BLOCKER` stays intact, 4/4 occurrences) and
`crop_prompt_3_{topband,eqstack,midleft}.txt` (1914 bytes each, `BLOCKER` intact 2/2).

On both legs clean (or every finding PIL-refuted with a banked record):

```bash
D=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide043
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 pptx_path videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_043_recreated.pptx --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 build_script videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_043.js --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 visual_check PASS --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 visual_transcript $D/judge_attempt_3.txt --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 visual_attempts 3 --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 gen_status passed --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py heartbeat 43 <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py get 43      # re-read: claim()/set() can reset gen_status
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py release 43 <id>
```

Judge attempts used this lane: **0 verdicts obtained** (2 probe hangs, 0 real-judge dispatches).
