# Worker report — slide 021 ("Inverse Problem of Singular Matrix") — BUILD-FIRST lane

Namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`
Worker lane: `w021-buildfirst-20261024` (claimed 08:49 UTC, `--force` over a 170-min-stale
`worker-kimi-021-r3` claim).
Scope: BUFFER-FIRST — get slide 021 fully build-verified without spending a vision window,
then judge only if a window genuinely opens.

## What this slide is

Title "Inverse Problem of Singular Matrix" (red bold serif, top center). Three stacked
blue-outlined white content blocks: top/middle carry math labels + a 3×3 matrix table and a
determinant→conclusion chain on the right; the bottom carries `(XᵀX + λI)⁻¹`, a long arrow,
and the resulting inverse matrix of decimals.

## Deliverable state (all verified this lane)

| item | path | md5 |
|---|---|---|
| build script | `recreated_pptx/build/slide_021.js` | `56e8f2db37e3500b32013f9446b47b47` |
| deliverable pptx | `recreated_pptx/slide_021_recreated.pptx` | `6ea9e28cce3f9c47e6cf6abd42365147` |

(Note: re-running the build regenerates the file with a fresh creation/modification
timestamp in `docProps/core.xml`, so the file's whole-archive md5 differs between runs
(`74364813557716b5a83e0fde790d510f` on the last rebuild). All content — the six
`ppt/media/image-*.png` and every non-core XML part — are byte-identical, verified with a
part-by-part `diff -rq`. The content md5s above are the authoritative ones.)
| render (judge input) | `recreated_pptx/qa/slide021/render_10.png` | `a17310a3cac93cf23e3c8daed2bd0cea` |

**Reproducibility proven**: rebuilding `slide_021.js` from scratch produces a pptx whose
parts are byte-identical to the banked one except `docProps/core.xml` (pptxgenjs writes
creation/modification timestamps there). All six `ppt/media/image-*.png` and all non-core
XML are identical. So the deliverable is deterministic, not an accident.

## Three REAL defects found and fixed this lane (all PIL-adjudicated against the original)

### Defect 1 — build referenced a stale equation asset (the `det5685` typo)

`slide_021.js` asked for `eq_021_det5685.png` (936×192, the attempt-3-era asset) but the
measured/calibrated asset is `eq_021_d5685.png` (1064×215). pptxgenjs happily stretched the
old asset into the new 1064×215 box, so the embedded bytes did not match the sidecar. The
build's own header comment already said `d5685`, and its `eq()` call passed `1064, 215` —
the filename was the only thing out of step. Confirmed by unpacking the pptx:
`ppt/media/image-1-5.png` was 936×192 (wrong); after the fix it is 1064×215, matching
`eq_021_d5685.json` (`"w_px": 1064, "h_px": 215`).

**Fix**: one-word filename correction in `build/slide_021.js:180`. Slide XML geometry is
byte-identical before/after (verified: only the `<p:cNvPr … descr="…">` path label changed).

### Defect 2 — table rows drifted ~12px downward (LibreOffice row-height law)

**This was the significant one.** pptxgenjs's `row: { h: … }` sets a table row's declared
height, but LibreOffice treats that as a MINIMUM and expands the row to fit the glyph
line-height PLUS the cell's default vertical insets. At fs14 the measured pitch was
**22.5px instead of the original's ~17.7px**:

| table | original gridlines (y) | render before fix (y) | row pitch orig → broken |
|---|---|---|---|
| P1 | 173, 190, 208, 226 | 172.7, 195.3, 217.8 (+~240) | 17/18/18 → 22.5 |
| P2 | 341, 359, 376, 395 | drifted under a saturated fill (unmeasurable) | 18/17/19 → ~22 |
| P3 | 458, 475, 492, 511 | 456.3, 477.8, 499.4 (+~521) | 17/17/19 → 21.6 |

Row-3 digits sat at frame y225..230 versus the original's y213..222, i.e. ~12px below and
pushing toward the block bottom.

**Fix**: `margin: 0` on each table (kills the default vertical insets) + an explicit
`rowH` array in the ORIGINAL's measured per-row heights:
P1 `[px(17), px(18), px(18)]` y173..226, P2 `[px(18), px(17), px(19)]` y341..395,
P3 `[px(17), px(17), px(19)]` y458..511. Also corrected the table y to the measured
original tops (P2 340→341, P3 457→458).

**Result** (render_10): gridlines now within **0.8px** of the original on all three tables
(P1 172.7/189.5/207.3 vs 173/190/208; P2 340.6/358.4/375.2 vs 341/359/376;
P3 457.2/474.5/491.3 vs 458/475/492), and all 27 digit rows within **1.4px** of the
original's digit-ink bands (was up to 12px).

### Defect 3 — highlight was saturated FFFF00 over the whole cell; original is FDFD96 on a tight band

The middle table's 17/43/95 diagonal highlight was drawn as a whole-cell saturated-yellow
fill. PIL says otherwise (`measure_yellow.py`, cross-confirmed by `measure_highlight_021.py`):
the original's highlight is an **opaque FDFD96 (253,253,150) band behind the digits only**, not
a cell fill:

| cell | original band | broken build | fixed build |
|---|---|---|---|
| r1c1 (17) | x107..143 y345..357 (37×13) | saturated FFFF00, x93..155 | FDFD96 x107.0..143.4 y344.9..356.5 |
| r2c2 (43) | x173..210 y363..374 (38×12) | saturated FFFF00, x161..224 | FDFD96 x172.7..210.6 y362.2..373.7 |
| r3c3 (95) | x243..279 y380..392 (37×13) | saturated FFFF00, x229..292 | FDFD96 x242.8..279.2 y380.0..392.4 |

Render dominant cell colour went from `(255,255,0)` to exactly `(253,253,150)`; saturated
`FFFF00` pixel count in each cell is now **0**; band deviations are ≤1.0px in x, ≤1.0px in y.

**Fix**: removed the per-cell `fill: { color: YELLOW }` and instead draw three `HILITE`
(`FDFD96`) rects at the measured bands *before* `addTable`; the table cells carry no fill, so
the digits show through on top. Verified in the pptx XML: every `<a:tcPr … marT="0" marB="0">`
has `noFill`, and `FDFD96` appears as a shape fill.

## Verification run on the deliverable (render_10.png, 2001×1125 @150dpi)

1. **House chrome check** — `shared_patterns/house_chrome_check.py render_10.png 021` →
   **PASS** (panel x112-1882 y94-bottom; strokes L/R/bottom present, top bare; badge center
   (1824,152) d=68; all within tol 8).
2. **Closed-loop element check** — `closedloop_10.py` (adapted from the banked
   `closedloop_5.py`) → **VERDICT: ALL MEASURED ELEMENTS MATCH**. Every equation ink box,
   per-colour band (red `X^T X`, blue `+ λI`), table, chain text and arrow lands inside the
   closed-loop standard (6px position, 10px width). Containment: 0 ink pixels outside any
   block's blue strokes on P1/P2/P3.
3. **Attempt-3 judge claims re-checked PIL-first** — claims 1, 2, 3, 4, 6 all re-measured
   FALSE (det0 present in P1 x341..435; no red ink in y46..76 outside the house strokes;
   λ=3 green ink at y304..321 inside P2; `⁻¹` red ink in P3; arrows blue). Claim 5 (blue
   instead of dark-red/maroon headers) stands as a medium-confidence styling approximation;
   claim 7 (a strike/slash marker on the "15" cell) was **refuted**: the original's P1 "15"
   cell is a plain digit (x263..275 y177..187, n=49) — no extra mark exists, so nothing to fix.
4. **Ink census** — full colour-class comparison vs the original: red, blue, green, highlight
   and dark classes all agree to ≤1.4px on box origin; saturated-yellow class is absent in
   BOTH images (correct).

## Judge state — LEG 1 DISPATCHED AND LOST AT THE CLIENT WALL; no verdict, park honestly

This is the honest gap, recorded for the founder's open decision about the frozen wall.

**What happened.** A window genuinely opened at 09:33 UTC (`pgrep -c -f analyze_image.py`
read **5**, below the `< 8` threshold), so per the gate law leg 1 was dispatched at
09:39 UTC through `dispatch_leg1_fullslide.sh` (protocol invocation verbatim, frozen
`--timeout 600`). The dispatch therefore had a genuinely open window and **still**
produced **no transcript**: the process ran ~28 minutes and was killed by the outer
`timeout 1700` wrapper. `judge_attempt_10.txt` was never written, so there is no
`FINAL VERDICT:` line and **no evidence** — this attempt does not count as a verdict.

**Why I did not retry.** My own dispatch order requires BOTH that a window be open
(`pgrep < 8`) **and** that legs stop aborting at the client wall. My first dispatch had
an open window and still aborted at the wall, so the second condition is unmet — and the
second is exactly the founder-decision item (a sibling lane, 049, is testing whether an
extended wall lands verdicts). Retrying here would spend another ~28 min to re-produce
the same failure, and I was directed not to change the wall myself. Protocol permits one
hard-wall retry per leg; I deliberately did not spend it, because the retry condition I
was given (window open AND legs no longer wall-aborting) is not satisfied — the wall, not
the window, is the blocker. This is evidence for that decision, not a verdict.

**Consequence: slide 021 is NOT certified.** `visual_check` is deliberately NOT written
(no judge ran). Everything needed to certify the moment the wall is settled is staged and
byte-checked:

- **Leg 1** (Template A full-slide): payload `judge_prompt_10.txt` (4140 chars, extracted
  programmatically byte-for-byte from `shared_patterns/judge_protocol_03.md` — not
  hand-typed; no `NNN`, no bare `K`, `BLOCKER` count 4, `FINAL VERDICT` line present).
  Dispatch script: `qa/slide021/dispatch_leg1_fullslide.sh` (syntax-checked, `ROOT`
  resolves, protocol invocation verbatim).
  Transcript (written by the gate on completion):
  `qa/slide021/judge_attempt_10.txt`.
- **Leg 2** (Procedure B crop pairs): payload `crop_prompt_template_10.txt` (1915 chars,
  same extraction, `NNN`→`021` applied; `BLOCKER` count 2). Five pairs cut from render_10 at
  **matched effective scale 2.0833**, with both crops proven to have identical pixel
  dimensions on both axes (per the protocol's no-mismatch law):

  | region slug | frame-px region | crop size | contains |
  |---|---|---|---|
  | `top_table_eq` | x88..322 y126..232 | 490×223 | `X^T X` label + singular 3×3 table |
  | `top_chain` | x332..802 y182..218 | 981×77 | the "|X^T X| = 0" chain: two blue arrows, Singular Matrix, red italic No Inverse |
  | `mid_table_eq` | x80..322 y290..402 | 506×236 | `(XᵀX+λI)`, `λ=3`, regularized 3×3, 3 highlight bands |
  | `mid_chain` | x332..892 y348..382 | 1168×73 | the "|X^T X| = 5685" chain: two blue arrows, Non-Singular Matrix, red italic Inverse Exists |
  | `bot_eq_table` | x148..642 y450..519 | 1032×145 | `(XᵀX+λI)⁻¹`, long arrow, inverse matrix |

  Dispatch script: `qa/slide021/dispatch_leg2_crops.sh` (per-crop gate check at `< 8`,
  transcripts `crop_10_<slug>_judge.txt`). Generator: `qa/slide021/cut_crops_021.py`.

  Note: these five supersede the older `crop_3_*` and `crop_7_*` pairs, which were cut from
  earlier renders carrying the row-height and highlight defects. Old pairs kept as evidence,
  never deleted.

## Exact resume commands

```bash
cd /workspaces/codespaces-blank/ai_llm_slides

# claim / heartbeat as needed:
VIDEO=machine-learning/03_ridger_regression_gradient_descent \
  python3 scripts/15_progress.py claim 21 <your-worker-id> --force
VIDEO=machine-learning/03_ridger_regression_gradient_descent \
  python3 scripts/15_progress.py heartbeat 21 <your-worker-id>

# 1. probe BOTH dispatch conditions (window open AND legs are landing):
pgrep -c -f analyze_image.py          # must be < 8
#    ... and the wall must be settled (see this report's judge section).
#    If either is false: park, do NOT dispatch.

# 2. LEG 1 — full-slide judge (consumed one attempt, lost at the wall 10:07 UTC)
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide021/dispatch_leg1_fullslide.sh
#    -> transcript: recreated_pptx/qa/slide021/judge_attempt_10.txt

# 3. LEG 2 — the five crop pairs
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide021/dispatch_leg2_crops.sh
#    -> transcripts: recreated_pptx/qa/slide021/crop_10_<slug>_judge.txt

# 4. adjudicate PIL-first (bank under qa/slide021/), fix only REAL defects (copy-then-modify),
#    re-render as render_11, re-run BOTH legs from the new render.
```

If a leg FAILs: adjudicate PIL-first against BOTH images, fix by copy-then-modify, re-render
as `render_11.png`, re-cut the crop pairs from the new render, re-run both legs.

## DB state at hand-off

`gen_status=building` (parked, not `judging` — nothing is in flight), `build_script` and
`pptx_path` set, `visual_check=NULL`, `visual_attempts=1` (one attempt consumed by the
wall-aborted leg 1; no verdict), `visual_transcript=NULL`, worker
`w021-buildfirst-20261024`, heartbeat refreshed at hand-off.

**NOT CERTIFIED.** `visual_check` is deliberately NOT written: no judge produced a
verdict. Do not read `gen_status=building` as "nothing done" — the build is fully verified
and reproducible; only the two vision legs are outstanding, and they are staged to run
the moment the client wall is settled.

## Banked artifacts this lane

`render_10.png`, `render_10_closedloop.txt`, `build_attempt_9_pre_fixes.js` (pre-table/highlight-fix build),
`build_attempt_8_pre_assetfix.js`, `wall_abort_evidence_10.txt` (leg-1 wall-abort record for the
founder's wall decision), `judge_prompt_10.txt`, `crop_prompt_template_10.txt`,
`dispatch_leg1_fullslide.sh`, `dispatch_leg2_crops.sh`, `cut_crops_021.py`,
`measure_highlight_021.py`, `measure_yellow_bf.py`, `render_8.png` / `render_9.png`, `adjudicate_leg1_10.py`
(intermediate evidence), the ten `crop_10_*` PNGs + five `crop_10_*_desc.txt`,
`worker_report.md` (this file).
