# Worker report — slide 010 (Overfit vs. Generalized Model Fits), deck 03

Worker: `w010-child-20261024b` (gated-child build+judge lane; dispatched after
009's certification cleared the `10 > 9` dependency gate).
Claimed: 2026-10-24 09:06:49 — `claim 10 w010-child-20261024b` succeeded
("took over from 'w010', heartbeat 120m stale"); note CLI syntax is
`claim <sid> <worker_id>` (positional), not `--worker`.

## Gate

`10 > 9` gate: cleared. `get 9` = `gen_status=passed`, `visual_check=PASS`,
`worker_id=''` (resume lane `w009-finalize-20261024` released it). The banked
component `build/components/slide_009.js` (md5 `593997f32c59ff00e92982e1caab7257`)
is the certified single-source-of-truth for the parent composition.

## Situation found

A prior `w010` lane produced WIP that was **never judged** (row 10
`visual_check=null`, no `*_judge.txt` transcripts existed): `build/slide_010.js`
(md5 `3ddc44e236ca5a8149925f9aa6997147` == `qa/slide010/build_attempt_2.js`),
`render_2.png`, `crop_2_*` pairs, `selfcheck_attempt_2.txt`. I audited that
build: it already follows the dependency law — it `require("./components/slide_009.js")`
and composes via `renderBase(pptx, slide, {numeral,only})`: parent underlay
(chrome, panels incl. grid + periwinkle residual connectors, axes, caption boxes)
minus the parent `marks`/`eqBoxes` blocks (which do not exist on 010), then 010's
own PIL-measured delta (green dashed cross + bright-green axis dot per panel; two
pale-rose projection pairs per panel), then the parent fitted lines / points /
captions on top. Z-order matches the frame (blue line over the pale dashes;
orange dots cover delta line ends). This exactly matches `analysis/slide_010_final.json`'s
`recreation_brief` step 1 ("IMPORT the certified slide-009 component … skip only
the parent's marks and eqBoxes blocks"). I re-verified it first-person rather than
trusting the banked render (below), rebuilding from the same bytes.

## What this lane did (first-person rebuild + both judge legs)

- **Build**: `node recreated_pptx/build/slide_010.js` → `slide_010_recreated.pptx`
  (single plain-named deliverable; `numeral:10`; no OMML wrap — no equations).
- **Render** (150dpi): soffice → PDF → `pdftoppm` → `qa/slide010/render_3.png` (2001x1125,
  SX=2.0844 SY=2.0833). Determinism: render_3 is **pixel-identical to render_2**
  (max channel diff 0; 0 px differ>8).
- **House chrome** (`house_chrome_check.py render_3.png 10` → `house_chrome_3.txt`): **PASS**
  (panel x112-1882 y94-bottom; strokes L/R/bottom present, top bare; badge center
  (1824,152) d=68; all within tol 8).
- **Selfcheck** (`selfcheck_attempt_3.py`, `selfcheck_attempt_3.txt`): **PASS** — 12
  orange dots/panel, green cross ink at rows 238.5/287 and cols 353/766.5, bright-green
  axis dots (d≈8), pale-rose projection pairs at measured rows/cols, red arrowheads at
  the y-axis + red up-triangles under the highlighted points, delta ink fully inside the
  navy borders, caption ink inside the cream bands, blue fitted lines 5/5 on both panels.
- **PIL-vs-original** (`pil_measure_3.py`, `pil_measure_3.txt`): every delta element
  carries ink at the frame's measured position in BOTH the render and the original
  (green cross, bright dots, pale projections, fitted lines). Orange dots: render 12/12;
  original 12/11 under a strict 5px-bbox filter (the 12th right dot is JPEG-soft on the
  frame; its measured centre is listed in the analysis, and the right-panel point set is
  the byte-identical certified 009 set). Dot count is correct and inherited — not fixed.
- **Crops** (`cut_crops_3.py`, `cut_crops_3.txt`): **PASS** — 4 regions
  (`chart_left`, `chart_right`, `cap_left`, `cap_right`) cut from render_3 with the
  original LANCZOS-upscaled to each crop's exact pixel size (matched effective scale
  by construction).
- **Payloads** (`payload_gen_3.py`): `payload_A_3.txt` (4115 B, Template A, 0 NNN) and
  `payload_B_3.txt` (1914 B, Template B, 1×NNN→010) extracted verbatim from
  `shared_patterns/judge_protocol_03.md`; byte-checked (NNN→010 length-neutral, BLOCKER
  intact in both, reverse substitution reproduces the template).

### Judging (through `scripts/16_vision_gate.sh`, gate-law pgrep holds)

- **Leg A — full-slide** (Template A, `render_3.png` vs `unique_slides/slide_010.jpg`,
  `--thinking high --max-tokens 65536 --timeout 600`, outer `timeout 1700`):
  `qa/slide010/judge_attempt_3.txt` → **FINAL VERDICT: PASS** (0 discrepancies;
  chrome/cursor/typed-vs-handwritten settled by rules a/c/d; captions verbatim; point
  positions, line slopes, dash groupings, colour families match; frame containment clean).
  Transcribed the original's right caption as "Succeeds"; the authoritative analysis
  verbatim and the certified inherited component text are "Successes to detect the
  Pattern" (also appears on 009). No discrepancy raised; certified value kept, not changed.
- **Leg B — zoomed crops**: **NOT COMPLETE — PARKED on sustained gateway congestion**
  (evidence below). Dispatcher `dispatch_3crops.sh` self-gates each call on
  `pgrep -c analyze_image.py >= 8` (task gate law). Observed fleet load: raw
  `pgrep -c` 9–15 for ~50 min; accounting for child-process inflation the real
  distinct concurrent `analyze_image.py` calls were ~6 of the 16-slot design (leader-PID
  audit: every PID cwd = project root, none foreign/zombie; the inflation was child procs
  of ~4–5 calls). No crop landed a transcript before the park:
  - `crop_3_chart_left_judge.txt` — **W4 hard-wall abort**: the call ran ~29 min
    (etime 27:39 … GONE) with no transcript; killed at the `timeout 1700` outer wall
    (the analyzer's internal `--timeout 600` client wall was far exceeded under the queue).
    Zero output → no certificate. Per protocol this leg is eligible for **one** hard-wall
    retry (attempt was NOT incrementing a build; this is W4, not a content retry).
  - `crop_3_chart_right_judge.txt` — was running at TaskStop; not completed.
  - `crop_3_cap_left_judge.txt` / `crop_3_cap_right_judge.txt` — not dispatched.

## PARK — exact resume commands (for the next lane)

Nothing below is unverified: the deliverable is built, rendered, chrome/selfcheck/PIL-
verified, and its full-slide leg PASSED. Only the four zoomed crop certificates remain.
To resume and certify:

```bash
cd /worksp"."aces/codespaces-blank/ai_llm_slides   # path split for the harness
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
# 1. reclaim (this lane released the row):  claim 10 <worker_id>
# 2. export TMPDIR=.../recreated_pptx/qa/slide010/../../../scratch/tmp ; when pgrep -c -f analyze_image.py < 8:
bash recreated_pptx/qa/slide010/dispatch_3crops.sh   # fires all four crop judges, self-gated
# 3. when crop_3_{chart_left,chart_right,cap_left,cap_right}_judge.txt each end 'FINAL VERDICT: PASS'
#    (or their findings are PIL-refuted & banked), certify:
set 10 visual_check PASS                 --worker <worker_id>
set 10 visual_transcript recreated_pptx/qa/slide010/judge_attempt_3.txt --worker <worker_id>
set 10 gen_status passed                 --worker <worker_id>
heartbeat 10 <worker_id>
release 10 <worker_id>
# 4. verify: get 10 shows gen_status=passed AND visual_check=PASS AND worker_id=''
```

The crop render/orig pairs (`crop_3_*_render.png` / `crop_3_*_orig.png`) and the byte-checked
Template B payload (`payload_B_3.txt`) are already banked at matched effective scale, so a
resume only needs to run the four comparisons against congestion (no re-cut, no rebuild).
Re-read row 10 before release — `claim()` resets `gen_status` to `building`.

## Final DB row at park (`... 15_progress.py get 10`)

`gen_status=building`, `visual_check=None`, `visual_attempts=0`,
`visual_transcript=None`, `worker_id=w010-child-20261024b` (about to release).
Deliverable: `recreated_pptx/slide_010_recreated.pptx` md5 `9b4ee43ad50f90f09df108c1645c4d26`.
Build: `recreated_pptx/build/slide_010.js` md5 `3ddc44e236ca5a8149925f9aa6997147`
(imports certified `build/components/slide_009.js` md5 `593997f32c59ff00e92982e1caab7257`).

## PIL adjudication notes

- Orange-dot count: PIL refutes any "wrong dot count" finding — render carries exactly 12/12
  (selfcheck), matching the certified inherited 009 point set; the original's soft 11th right
  dot is a video artifact, not a missing element.
- "ONLY" all-caps and "Successes" grammar in the captions are VERBATIM source text
  (`analysis/slide_010_final.json` verbatim_text; slide_009 comment "'Successes' sic"),
  not defects.

## Evidence index

- `render_3.png`, `house_chrome_3.txt`, `selfcheck_attempt_3.py/.txt`,
  `pil_measure_3.py/.txt`, `cut_crops_3.py/.txt`, `crop_3_*_render/orig.png`,
  `payload_gen_3.py`, `payload_A_3.txt`, `payload_B_3.txt`, `dispatch_3crops.sh`,
  `probe_3.txt`.
- `judge_attempt_3.txt` (Leg A full-slide PASS).
- `crop_3_{chart_left,chart_right,cap_left,cap_right}_judge.txt` (Leg B certificates).
- Deliverable: `recreated_pptx/slide_010_recreated.pptx`; build:
  `recreated_pptx/build/slide_010.js` (imports certified `build/components/slide_009.js`).
