# Slide 030 — worker report (IN PROGRESS)

Worker: `w030-finish-20261024` (resumed lane; prior worker `w030-buildfirst-20261024`
was a stale zombie — heartbeat 88m at claim time).

Slide: **030 "Convex Function, Learning Rate =0.2, Start at X=3"** — deck
`machine-learning/03_ridger_regression_gradient_descent`.
Deliverable: `recreated_pptx/slide_030_recreated.pptx`
Build script: `recreated_pptx/build/slide_030.js`

## 1. Triage of the inherited state

- Prior row read `gen_status=building`, stale claim, no qa bank for renders,
  crops, scripts, or transcripts (the only prior qa content was a partial set of
  attempt 1-5 artifacts left in `qa/slide030/`, which I preserved and continued
  from — see "Resume" below).
- I re-ran the banked build script and re-rendered: the fresh render is
  **byte-identical** (md5 `ac17141f492f2b61291e4912007c0b78`) to the prior lane's
  `render_5.png`, so the 07:55 pptx and the build script were already in sync —
  no rebuild needed. The unpacked pptx carries the full inventory (240 shapes,
  2 equation PNGs, 6 tables, 207 line shapes = the dense parabola + grid).

## 2. Verification done before judging

- **House chrome**: `house_chrome_check.py` → **PASS** on `render_6.png`
  (panel x112..1882, strokes L/R/bottom present, top bare, badge (1824,152) d68).
  Banked: `house_chrome_check_6.txt`.
- **PIL measurement** (`measure_w030.py`, banked):
  - content ink fully inside the house panel (left/right/above = 0 px)
  - parabola: LSQ quadratic fit residual **max 6.4 px / mean 0.67 px** over 175
    sampled columns → ONE smooth arc (ripple check clean); fitted vertex
    x=687.1 y=253.9 vs build-model x=687.8 y=254.5 (≤1 px); ink 0 px outside the
    plot frame on all four sides; arms match the analytic f(x)=(x-5)^2+1 to ≤7 px
  - iteration table (8 rows x 12 cols, 96 cells, all cells carry ink) and param
    table (6/6 cells) verified; 5 colour bands' median fills match the original
    to within ~2-5 RGB
  - geometry deltas vs the original: title ink, red eq box, green box, dashed
    x=5 line, secant, tick labels all within ~1 px (sub-pixel agreement)
  - deviation found: **red arrow** is ~6 px shorter than the original
    (render y304..347 vs orig y304..340; the extra 7 px is the pink table fill
    bleeding into the mask). Same shape and tilt. Not yet adjudicated — the
    `arrow` crop leg will rule on it; if it flags, fix is a one-line geometry
    change in the build script.

## 3. Judge dispatch state (as of 12:40 UTC)

- Crops cut at matched effective scale (7 Procedure B pairs, LANCZOS
  H_render/540 ≈ 2.0833): param, formula, plot, iter_left, iter_right, callout,
  arrow. Scale audit `crop_6_scale_audit.json`: per-axis mismatch ≤ 0.47%
  (rounding only, well under the 8% drift threshold).
- Payloads regenerated from `shared_patterns/judge_protocol_03.md` with ONLY the
  protocol substitutions (`slide_NNN`→`slide030`, `K`→6) and **byte-verified by
  `make_payloads_6.py` → ALL BYTE CHECKS PASS**. (The verifier caught a real bug
  on first run: Template B payloads still contained `slide NNN` unsubstituted.)
- Wall evidence (all banked in `legA_full_dispatch.log`):
  - **Attempt at `--timeout 600`** (v1, 11:37): client aborted twice on its internal
    630 s HangError, then upstream returned HTTP 504 (`upstream_timeout`,
    Nvidia candidate) → no verdict.
  - **Attempt at `--timeout 1200`** (v3, 12:12: the ratified provisional W4 wall,
    payload byte-for-byte unchanged): aborted once on the internal 1230 s
    HangError, then the same upstream HTTP 504 → no verdict. The analyzer itself
    warns that `--timeout > 600` saturates the shared gateway.
  - Conclusion so far: the full-slide leg is failing on the **upstream provider**
    (NVIDIA NIM via IronRouter), not on slide content. Per the law this is **one
    hard-wall retry already consumed** for leg A; do not retry-loop it.
- Probe (Template A probe, `--timeout 120`) returned rc=124 (no body inside
  150 s) — the gateway window was congested at the time.
- Dispatcher v3 (`dispatch_legs_6_v3.sh`, detached via setsid+nohup) is running:
  after leg A failed it moved on to the 7 crop legs at tmo=1200, in the order
  param, formula, plot, iter_left, iter_right, callout, arrow.
  Note: the v1 background run hit the harness 600 s ceiling and was orphaned
  (its python client survived reparented to init and later died with no verdict),
  and a v2 attempt's orphan-detection was polluted by my own polling shells;
  v3 was started clean with no live client referencing slide030 confirmed first.
- Note the 1200 s wall was chosen because 600 s could not complete ANY leg —
  the upstream needs >1230 s of thinking under the current congestion, or it
  504s. Both are outside my control.

### Next commands when v3 finishes

```bash
QA=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide030
grep -o 'FINAL VERDICT: [A-Z]*' $QA/judge_attempt_6.txt | tail -1
for f in $QA/crop_6_*_judge.txt; do printf '%-40s %s\n' "$(basename $f)" "$(grep -o 'FINAL VERDICT: [A-Z]*' $f | tail -1 || echo NONE)"; done
```

Then: PIL-adjudicate every finding, fix real defects (copy-then-modify), re-render,
re-judge, and certify with the runbook sequence (pptx_path, build_script,
visual_check, visual_transcript, visual_attempts, gen_status, heartbeat, release)
— re-reading `get 30` before release to restore gen_status if set() reset it.

## 4. Banked evidence (this worker)

| file | what |
|---|---|
| `render_6.png` | fresh 150dpi render (md5-identical to prior render_5) |
| `house_chrome_check_6.txt` | chrome PASS |
| `measure_w030.py` | PIL measurement vs original |
| `parabola_check_w030.py` | curve ripple/containment check |
| `cut_crops_6.py` + `crop_6_scale_audit.json` + 14 crop PNGs | Procedure B pairs |
| `judge_prompt_6.txt`, `crop_prompt_6_*.txt` | byte-verified payloads |
| `make_payloads_6.py` | payload regenerator + byte-checker |
| `dispatch_legs_6.sh`, `dispatch_legs_6_v3.sh` | dispatchers |
| `worker_report_progress.log` | live dispatch log |
| `scratch/render_w030_finish.sh` (deck scratch) | rebuild + render script |

---

## 5. 2026-10-24 ~15:20 — resume by w030-finish-20261024b (timeout-resume)

### Resume state
- Re-claimed (prior heartbeat stale, 68 m) and confirmed the deliverable is still
  current: rebuild from `build/slide_030.js` re-renders to the SAME md5
  (`ac17141f…`) as the banked `render_5/render_6.png` → the 07:55 pptx is not stale.
- Banked crop verdict found: **`crop_6_formula_judge.txt` → FINAL VERDICT: PASS**
  (landed 13:41 during v3). 5 MINOR findings, zero MAJOR/BLOCKER.
- Verdict coverage before this resume: 1/8 legs. Missing: Leg A (full-slide) and
  crops plot, iter_left, iter_right, param, callout, arrow.
- Wall cause of the misses (banked dispatch logs): image leg dying with HTTP 504
  Nvidia `upstream_timeout` and/or internal 1230 s HangError — the same failure
  channel the fleet saw on 043. Text (vision) leg healthy. Gateway now light
  (real clients 3-4, pgrep 12).

### Adjudication of crop_6_formula PASS (all PIL, frame px, 960x540)
See the table in the transcript above this section; summary: operator spacing
(render eq bbox 405.4..522.9 vs orig 404.0..524.0 = 2.5 px narrower overall),
minus-glyph width (mandated professional mathtext), italic math-serif voice
(mandated 2D format), gap after `f(x)` (render line2 363.2..539.7 vs orig
353.0..547.0 → render is 17 px TIGHTER overall, so the "wider gap" reading is the
italic run, not a defect), and colour deltas (orig RGB is the JPEG wash of the
same house red/green). → **No build change; region certified clean.**

### Dispatched
`dispatch_legs_6_v4.sh` (detached, started 15:28:40): re-fires Leg A then the 6
missing crop legs sequentially at `--timeout 1200` (approved wall) inside
`timeout 1700`, payload bytes unchanged, `--thinking high --max-tokens 65536`,
gate law probing real clients < 8 (max 2 probes/hour, then wait).

## 6. 2026-10-24 ~17:50 — resume by w030-finish-20261024c (claim renewed)

### Claim / DB state
`get 30` (17:28): `gen_status=building`, `visual_check=null`,
`visual_attempts=1` (**must become 6** — fleet convention is the judge attempt
index: slide 13→`judge_attempt_6.txt`/attempts 6, slide 21→attempt 10,
slide 27→attempt 10), `visual_transcript=null`,
`worker_id=w030-finish-20261024c` (claimed `--force`; earlier ids ...b went
stale), `last_error=null`. Heartbeat sent this cycle.

### Deliverable currency re-verified
`scratch/render_w030_finish.sh` rebuilds `build/slide_030.js` and re-renders to
`render_6.png` md5 `ac17141f492f2b61291e4912007c0b78` = banked `render_5.png`
= `render_attempt_1.png`. House chrome check on render_6: PASS (panel
x112..1882, L/R/bottom red strokes, no top stroke, badge d68 at (1824,152)).
Payloads re-derived + byte-verified (idempotent regen, md5s unchanged,
`ALL BYTE CHECKS PASS`) and confirmed verbatim against
`shared_patterns/judge_protocol_03.md` sources.

### Judge-leg status at this cycle
Verdict coverage: **1/8** (formula PASS, adjudicated in section 5, no build
change). Still missing: Leg A full-slide + crops plot, iter_left, iter_right,
param, callout, arrow — all lost to the shared image upstream, not to the slide.

Failure channel (banked in `*_dispatch.log` / `probe_health_dispatch.log`):
every leg attempt ends either `HTTP 504 upstream_timeout` (Nvidia candidate
`nva…hWGS`) or an internal `HangError: hard wall-clock 1230s exceeded` (which
then retries and hits the 504). Observed 2026-10-24 16:18–17:55:
- legA_full (16:59 fire) → 504 in 60 s
- legB_plot (17:00 fire) → 504 in 62 s
- legB_iter_left round 1 (17:01) → 1230 s HangError + 504 pair, outer
  `timeout 1700` killed during retry 2 → rc=124 17:29
- legB_iter_left round 2 (17:33) → 1230 s HangError + 504 pair → rc=1 17:55
- legB_iter_right firing 17:55 (in flight)
So ~22 min per attempt and the healthy shape is "survive past 1230 s": the one
verdict that ever landed (formula, 13:14→13:41) took 27 min to complete. Fast
504 passes are the outage shape, so v5's `fire_leg` (which returns immediately
on a 504) exhausts legs quickly; v6 (added this cycle) therefore re-checks
EVERY leg each outer round and fires only the ones with no verdict yet,
including Leg A, which v5 already burned through and never revisits.

### Dispatch state
`dispatch_legs_6_v5.sh` (PID 706312, detached) — probes the lane with a light
`analysis` probe every 300 s, then fires missing legs back-to-back at
`--timeout 1200` inside `timeout 1700`, `--thinking high --max-tokens 65536`,
payload bytes unchanged, gate law real clients < 8.
`dispatch_legs_6_v6.sh` (new, this cycle) — 10 outer rounds, missing-leg-first
(Leg A first), fast-504 legs skipped rather than blocking, verdict-present legs
skipped. To be launched only when v5 exits and no duplicate leg is in flight.

### Adjudication posture (banked, pending verdicts)
- formula PASS → all 5 MINORs PIL-adjudicated, no build change (section 5).
- Two further MINOR candidates found PIL-first, awaiting a verdict:
  red arrow ~3 px narrower / ~2.2 px shorter than orig's arrow ink
  (render x170.8..190.9 / y304.2..333.0 vs orig x171..194 / y304..335 — same
  shape and tilt, so MINOR at most); plot point labels ~3 px smaller
  (orig (5,1) bbox 698..223 vs render 696.1..715.3). Both PIL-surfaced and
  neither is a content defect.
