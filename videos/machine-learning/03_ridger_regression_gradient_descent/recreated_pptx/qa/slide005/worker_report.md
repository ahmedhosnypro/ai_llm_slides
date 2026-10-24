# Worker report — slide 005 (deck 03_ridger_regression_gradient_descent)

Worker: `w005-buildfirst-20261024` (took over from the retired `slide005-worker-1792792740`,
whose claim was 186 min stale)
Slide: 005 "Minimization of Loss function to obtain BEST model parameters"
Date: 2026-10-24. Deliverable: `recreated_pptx/slide_005_recreated.pptx` (single plain-named pptx)

## Status at hand-off

- **Build: CURRENT and fully verified** — pptx md5 `58de0cb2c39c5ef004e60d9f000a48a9`
  matches a deterministic rebuild of `build/slide_005.js` in every zip entry
  (only `docProps/core.xml`'s `dcterms:created` timestamp differs).
- **Render: CURRENT** — `qa/slide005/render_9.png`, 2001x1125 @150dpi
  (md5 `01bcb967f29e502e99e80925aa320599`), reproduced by soffice→PDF→`pdftoppm -r 150`.
- **House chrome: PASS** on render_9 (`shared_patterns/house_chrome_check.py … 5`,
  panel x112-1882 y94-bottom, L/R/bottom strokes present, top bare, badge (1824,152) d=68).
- **PIL self-check: PASS** — `selfcheck_attempt_8.txt` (runbook checks 1/2/3/4/8).
- **Judging: NOT DONE — PARKED on gateway congestion.** No verdict exists; no transcript
  containing `FINAL VERDICT:` has been banked by any lane.
- **DB row: left untouched** (`gen_status=building`, `visual_check=null`,
  `visual_attempts=0`, `visual_transcript=null`) — nothing was written except heartbeats.

## Lane history (attempts 1→9)

| render | states | notes |
|---|---|---|
| render_1..6 (retired worker) | chrome PASS, ~1px bands | eqFit + DejaVu font calibration; see that worker's report, banked as `qa/slide005/worker_report.md` |
| render_6 | judge render, never judged | gateway wall: 20-22 queued calls, zero transcripts fleet-wide |
| render_7 | reproduction check | rebuilt attempt 6's pptx, byte-identical to `render_6.png` (md5 `6a2d79…`) — proved the banked render was still current |
| render_8 | BAD EQ5 BAND | eq5 band wrongly stretched to x683 from a noise-inflated window measurement |
| render_9 | **CURRENT** | eq5 band reverted to attempt 6's value; getbest containment fix applied |

## Attempt-9 audit (what I measured on BOTH images before touching the build)

Law honoured: "measure everything against BOTH images before any build change".

1. **Build currency** — rebuilt the pptx from the live script; 21/22 zip entries byte-identical,
   only the `core.xml` timestamp differs. So `render_6.png` was still the current render.
2. **Render reproducibility** — fresh soffice render == `render_6.png` pixel-for-pixel.
3. **Font identification (exhaustive)** — probed all 1935 installed faces against the
   original's (advance, ink-height) pair for the title and the body line. **No installed
   font reproduces the original's metrics.** The original's authoring font is absent from
   this machine, so DejaVu Sans 18 pt (which matches the original's horizontal advance to
   1 px) is the best available: its vertical ink extent is 3-5 px shorter than the
   original's for every text element. That gap is an unavoidable font-substitution
   artifact, not a build error, and it is identical at any size that preserves the advance.
4. **My own scale bug, caught and corrected** — first selfcheck used `2001/540 = 3.71`
   as the render scale (mixing axes). Correct scales are `sx = 2001/960 = 2.084375`,
   `sy = 1125/540 = 2.083333`. Every "BLOCKER" that first run reported was an artifact
   of the wrong scale.
5. **Window contamination, caught and corrected** — several measurement windows touched
   enclosing-box border strokes (the pink box's right border at x505-506, the blue box's
   top border at y134-135, the green box's border), inflating ink extents on BOTH images.
   Final windows are strictly interior.

### Real defect found and fixed — "Get Best W that minimizes the loss" overflowed its box

Measured on BOTH images (window clear of the pink box's right border, and the border
subtracted via a row-band baseline):

- ORIGINAL text ink: x196..500, y306..322 — it **ends 5 px inside** the pink box's right
  border (x505..506), confirmed column-by-column (ink rows 5 px at x500, then 0 from x501).
- Attempt-6 RENDER text ink: x196.7..510.5 — 18 pt DejaVu Sans advances 316.3 px / inks
  314.5 px (PIL-verified), carrying the ink **4 px past the border at x506**. Per runbook
  check (5) that is a frame-containment MAJOR.

Fix (`build/slide_005.js`): size 18 → 17.4 pt (ink 304.3 px, ending x501, 4 px inside the
border) and the box nudged y303 → y306 so the line's centre sits on the original's ink
centre (314.0 frame px). Verified after re-render: REND ink x196.7..499.9, dx1 = -0.09 px.

### Real defect caught and REFUTED — eq5's arrow chain

An attempt-8 change stretched eq5's band from x637 to x683 on the strength of a window
measurement. Noise-rejected segmentation (a column needs ≥3 ink rows) refuted it:

- ORIGINAL: 26 real glyph groups, x97..x637. Its columns x639..x646 hold **ZERO** ink,
  x647..x683 hold only 1 px/col of JPEG noise, and x689+ is the green box's border.
- Attempt-6 RENDER: 27 real groups, x95..x638 — **it already matched the original.**
- Stretching to x683 added 3 glyph groups / ~45 px of arrow the original does not have.

Band reverted, re-rendered, and the two renders diffed: **10,480 px differ and every one of
them sits in the getbest band (frame x196.7..510.5, y303.4..319.7), 0 px outside it** —
proving the revert restored attempt 6's geometry everywhere else and that getbest is the
single surgical change.

## Final measured state (render_9 vs slide_005.jpg, frame px)

Worst per-element ink-band deviation = **3.64 px** (fleet TOL 8). Equations eq1..eq5,
pinkfrac, rem1, rem2, green, title, rememberU/L and getbest all within TOL on all four edges.
House-frame overflow: **0 px** on all four sides. Per-box containment: every element's ink
inside its measured border, including the previously-overflowing pink box. Fraction bars
present in all six stacked fractions. Explicit `lineSpacing` on every textbox (17.4/18/14/12).

## Judge status — PARKED (gateway wedged)

- Gateway state at hand-off: **13 queued `analyze_image.py` processes**, IronRouter on
  :17844 at **0.7-0.8 % CPU over 3h45m** (pid 3035) — accepting but never completing.
  A slide019 judge call has been queued 11+ min with no output. Fleet-wide transcript
  writes are zero.
- Per the standing gate law (`pgrep -c -f analyze_image.py` ≥ 8 ⇒ do NOT dispatch) I did
  not dispatch a single vision call. Dispatching into this congestion would waste ~25 min
  and return no verdict.
- **5 legs are cut, payloaded and ready to fire the instant the gate opens** — see below.
- A background watcher (`scratch/tmp/gatewatch_005.sh`) polls every 240 s and logs to
  `scratch/tmp/gatewatch_005.log`; it exits 0 and writes `GATE OPEN …` when the queue
  drops below 8.

## Ready-to-fire legs (all self-block on congestion; syntax-checked, none executed)

Commands run from the project root. Each checks the queue first and exits 3 without
dispatching if ≥8 `analyze_image.py` are queued.

1. `qa/slide005/dispatch_attempt9/leg_A_full_slide.sh` — Template A full-slide judge
   (render_9 vs slide_005.jpg) → `qa/slide005/judge_attempt_9.txt`.
2. `qa/slide005/dispatch_attempt9/leg_B_eq_stack.sh` → `crop_9_eq_stack_judge.txt`
3. `qa/slide005/dispatch_attempt9/leg_B_blue_upper.sh` → `crop_9_blue_upper_judge.txt`
4. `qa/slide005/dispatch_attempt9/leg_B_pink_band.sh` → `crop_9_pink_band_judge.txt`
5. `qa/slide005/dispatch_attempt9/leg_B_lower_eqs.sh` → `crop_9_lower_eqs_judge.txt`

Fire Template A first, then the crop pairs, one at a time (dot 6 of Procedure B: map every
finding back to slide space — crop-relative coords × crop scale = frame px).

### Crop pairs (Procedure B, matched effective scale)

Region = slide-space frame px with ~8 px padding; the original crop is LANCZOS-upscaled so
`output_px/frame_px` is EQUAL per axis (render is 2001x1125 @150dpi).

| leg | region (frame px) | output px | files |
|---|---|---|---|
| eq_stack | x88..650 y100..285 | 1172x386 | `crop_9_eq_stack_{render,orig}.png` |
| blue_upper | x660..890 y128..245 | 479x243 | `crop_9_blue_upper_{render,orig}.png` |
| pink_band | x65..515 y280..350 | 938x146 | `crop_9_pink_band_{render,orig}.png` |
| lower_eqs | x64..900 y350..530 | 1743x375 | `crop_9_lower_eqs_{render,orig}.png` |

Note for the pink_band leg: it is the only crop whose region contains the attempt-9 fix,
so it MUST be judged against render_9 (it is).

### Payloads (byte-for-byte from `shared_patterns/judge_protocol_03.md`)

- `qa/slide005/judge_prompt_9.txt` — Template A, 4115 B, `slide NNN`→`slide 005`,
  `\bK\b`→9. Round-trip verified against the protocol text; `BLOCKER` ×4 intact; exactly
  one `FINAL VERDICT:` line.
- `qa/slide005/crop_prompt_9_{eq_stack,blue_upper,pink_band,lower_eqs}.txt` — Template B,
  1914 B each (identical bytes), `slide NNN`→`slide 005`. Round-trip verified.

## Banked evidence

- **Current deliverable**: `recreated_pptx/slide_005_recreated.pptx` (`58de0cb2…`) +
  `recreated_pptx/build/slide_005.js` (`6a65b1f6…`).
- **Current render**: `qa/slide005/render_9.png` (`01bcb967…`).
- **Pre-change snapshots (never deleted)**: `qa/slide005/build_attempt_6.js`,
  `slide_005_attempt6.pptx`, `render_6.png`, `render_7_attempt6b.png`, `render_8.png`
  (the bad-eq5-band render, kept as the refutation record).
- **Measurements**: `qa/slide005/measure_attempt9/` (17 scripts: selfcheck, render,
  pptx compare, font probe, segmentation, band/containment audits, diff, gatewatch).
  Text outputs: `selfcheck_attempt_8.txt`, `house_chrome_3.txt`.
- **Judge kit**: `qa/slide005/judge_prompt_9.txt`, `crop_prompt_9_*.txt`,
  `crop_9_*_desc.txt`, `dispatch_attempt9/*.sh`.

## Certification sequence (runbook-prescribed; NOT yet performed)

Per `scripts/17_worker_instructions.md:329` — only after Template A ends `FINAL VERDICT: PASS`
AND every crop leg is clean or PIL-adjudicated:

```
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 5 visual_check PASS --worker w005-buildfirst-20261024
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 5 visual_transcript <full-slide transcript path> --worker w005-buildfirst-20261024
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 5 gen_status passed --worker w005-buildfirst-20261024
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py heartbeat 5 w005-buildfirst-20261024
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py release 5 w005-buildfirst-20261024
```

Then verify `get 5` shows `gen_status=passed`, `visual_check=PASS`, `worker_id=""`.
(There is no `record-visual` subcommand.) Only transcripts with a real `FINAL VERDICT:`
line count as verdicts — template lines inside the banked `*_prompt.txt` files do not.

## Resume in one command block

```bash
C=<project-root>/ai_llm_slides     # this checkout lives under /workspaces/codespaces-blank/
Q="$C/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005"
cd "$C" && VIDEO=machine-learning/03_ridger_regression_gradient_descent \
  python3 scripts/15_progress.py claim 5 w005-resume-20261024 --force
tail -3 "$C/scratch/tmp/gatewatch_005.log"           # gate state
bash "$Q/dispatch_attempt9/leg_A_full_slide.sh"      # Template A
# then, one at a time:
for r in eq_stack blue_upper pink_band lower_eqs; do bash "$Q/dispatch_attempt9/leg_B_$r.sh"; done
```

## Query budget

No web searches were spent by this lane (the deck's web-source research leg for slide 005
is already `CONFIRMED` in `SOURCES_MAP.md`, so the economy law's "check sibling records
first" rule applied and no query was needed).
