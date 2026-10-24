# Slide 016 worker report — "L₁ and L₂ Regularization"

Worker: `worker-kimi-016-retry` (took over the lane from `worker_slide016_01`, claim heartbeat
140m stale > 40m threshold, per 15_progress.py takeover path).
Deck: `machine-learning/03_ridger_regression_gradient_descent`.
Claimed at 2026-10-23 20:5x. Protocol: `shared_patterns/judge_protocol_03.md`
(Template A full-slide + Procedure B crop-pairs).

## State at pickup

| item | value |
|---|---|
| build script | `recreated_pptx/build/slide_016.js` (banked, 209 lines) |
| deliverable pptx | `recreated_pptx/slide_016_recreated.pptx` (59433 B) |
| render | `qa/slide016/render_1.png` 2001x1125 (150dpi of 13.33x7.5in) |
| house chrome check | PASS (panel x112-1882 y94-bottom; strokes L/R/bottom present, top bare; badge (1824,152) d68) |
| DB row | `gen_status=building`, `visual_check=NULL`, `visual_attempts=0` |
| qa bank | render_1.png only — NO dispatch brief, no measurement bank, no selfcheck |

## Pre-judge PIL forensics (the reason this report exists)

The render's ink map was diffed against the original frame (both brought to 960x540
frame px; render downscaled 2001x1125 -> 960x540 LANCZOS, scale 2.0833 render-px per
frame-px). Per-band dark-ink counts:

| frame rows | original ink px | render ink px | verdict |
|---|---|---|---|
| 0-30 | 0 | 0 | match |
| 90-150 | 2599 | 3960 | render has both headers, original has one |
| 150-300 | ~8600 | ~10500 | OK |
| 300-330 | 120 | 337 | borderline |
| 330-360 | 1468 | **150** | **render empty** |
| 360-390 | 1565 | **150** | **render empty** |
| 390-420 | 1428 | **150** | **render empty** |
| 420-450 | 1156 | **150** | **render empty** |
| 480-540 | 4213 | 4316 | OK |

The 150 px in each empty band is exactly the two red strokes (x58.5 / x901) — i.e. no
text ink at all. Line-band inventory (interior x90..828, strict ink mask):

**Original — 12 text lines** (white box borders at x82-83 / x832-833, y89-91 and y532-534):

| line | band y | x extent | content |
|---|---|---|---|
| title | 59-86 | 312-621 | dark red #8B0000 bold title |
| L1 | 104-117 | 111-325 | "Regularizers are based on:" RED bold |
| L2 | 129-146 | 147-514 | "Penalize large values of W (model parameters)" BLUE bold |
| L3 | 179-197 | 92-556 | bullet 1, black, YELLOW highlight x286-457 y175-198 |
| L4 | 230-248 | 92-783 | bullet 2 line 1 |
| L5 | 256-273 | 110-750 | bullet 2 line 2 |
| L6 | 281-298 | 110-563 | bullet 2 line 3, ends with RED run x111-290 (the "customized weigh factor" red underline sits at y~296-298 under this line) |
| L7 | 332-350 | 92-667 | bullet 3 line 1, RED run x385-667 |
| L8 | 357-374 | 146-696 | bullet 3 line 2, BLUE run x254-390 ("L₂ regularization") |
| L9 | 408-426 | 92-768 | bullet 4 line 1, RED run x420-765 |
| L10 | 434-447 | 146-389 | bullet 4 line 2, BLUE run x254-390 ("L₁ regularization") |
| L11 | 484-502 | 92-807 | bullet 5 line 1, small RED run x647-670 |
| L12 | 510-527 | 109-190 | bullet 5 line 2, RED run x170-190 |

**Render — 7 text lines only** (box at x84-85 / x829-830, y93 and y528-530):

| line | band y | x extent |
|---|---|---|
| title | 69-97 | 92-825 |
| a | 169-183 | 100-496 |
| b | 191-206 | 100-726 |
| c | 210-225 | 100-768 |
| d | 230-251 | 99-707 |
| e | 256-270 | 200-461 |
| f | 280-294 | 100-801 |
| g | 495-509 | 100-825 |

### Root cause (two independent defects in `build/slide_016.js`)

1. **Five lines of body text never render.** The build defines 5 body bullets (l3-l7) but
   the original's bullets 2-5 each wrap onto TWO-3 visual lines each (12 total lines vs
   the build's 7). The build's boxes are ~0.7in tall and its font sizes/box widths
   re-wrap the copy into fewer, longer lines; LibreOffice renders only what fits, so the
   region y330-450 is blank in the render. The two BLUE key-term runs ("L₂ regularization"
   on original L8, "L₁ regularization" on original L10) live in exactly that blank band —
   i.e. the render is missing BOTH blue key terms, which the full-slide judge will flag as
   BLOCKER (missing element).
2. **The two header lines are vertically misplaced.** The build puts L1 at y=1.50in
   (108 frame px) and L2 at y=1.85in; the render's first body line "a" starts at y=169 and
   its own header-equivalents never appear as measured lines (the build's l1/l2 boxes
   render above y=169 but the render's line "a" at 169 is already bullet-1 content —
   the red header and blue sub-header are absorbed into the compressed wrapping).
   Measured original header positions are L1 y=104-117 and L2 y=129-146; the render has
   nothing at those rows.

Also noted: the yellow highlight (render x~72..92? -> measured at y175-198 in the
ORIGINAL, x286-457) does not appear at the same y in the render because the render's
line "a" (bullet 1) sits at y169-183, close but the highlight in the build is at
y=2.25in (162 frame px) x=4.0-6.4in (288-461) — that part is nearly right; the black
underlines on L11/L12 (original "Small number of samples (N)" x92-807 and
"Large vector Length (d)" x109-190) exist in the build but land at the render's wrong
line (its line "g" at y495-509), so they underline the wrong text.

### What a fix needs (for the next worker — NOT done by this worker)

Rebuild `build/slide_016.js` to reproduce all 12 lines with the measured geometry:
explicit per-line y positions in frame px -> inches (/72), matching x extents and the
red/blue/yellow color runs listed above. Simplest faithful approach: one `addText` per
line at the measured y (mid-line), letting each line be a single-string run with the
color-runs split into rich-text arrays for the colored spans. Line y-mids (frame px):
110, 137, 188, 239, 264, 289, 340, 366, 416, 440, 493, 518 — i.e. in inches
1.528, 1.903, 2.611, 3.319, 3.667, 4.014, 4.722, 5.083, 5.778, 6.111, 6.847, 7.194.

## Judge legs (this worker)

Attempt 1 (Template A) dispatched through `scripts/16_vision_gate.sh` per protocol.
Transcript: `qa/slide016/judge_attempt_1.txt`.
Payload: `qa/slide016/judge_prompt_1.txt` (shared prelude + Template A body byte-verbatim
from judge_protocol_03.md, NNN=016 K=1).
Crops cut per Procedure B (`create_crops_1.py`, matched effective scale 2.083x on both
axes, verified by assertion):
- `crop_1_missing_band_{render,orig}.png` — frame bbox (80,325)-(815,455): the original's
  L7-L10 block (both blue key terms + red runs); render crop is empty ink.
- `crop_1_full_body_{render,orig}.png` — frame bbox (80,98)-(815,532): the whole 12-line
  text block inside the white content box.
Template B payloads: `crop_1_missing_band_prompt.txt`, `crop_1_full_body_prompt.txt`.

Gateway state during this worker's run: heavy 504/502/429/connection-error storm. Probe 1
(150s wall) returned no body; protocol hang rule applied (slept 300s); probe 2 also
returned no body. Per parent's storm instruction the real judge was then dispatched
directly with `--timeout 600 --thinking high --max-tokens 65536` inside `timeout 1700`.

**Attempt 1 result: ECHO-CLASS GARBAGE (no evidence, no attempt counted).** The first
dispatch carried the protocol's shared prelude prepended to the Template A body. All three
model attempts failed garbage/hang:
- attempt 1: `GarbageError: echo-class response` — the model echoed the prelude's SKILL.md
  path span verbatim ("home ahmed projects ai llm slides agents skills image analysis
  skill m"), copied-prompt coverage 78% of the response.
- attempt 2: same echo-class, 58% coverage.
- attempt 3: `HangError: hard wall-clock 630s exceeded` — giving up.
This deck's own banked judges (slide012/judge_prompt_1.txt, slide014/judge_prompt_1.txt)
do NOT carry the prelude — they send the Template A body alone and produced coherent
bodies. The payload was therefore restored to the protocol's exact `-p` spec (the
"GROUND RULES..." template body, 4140 B, NNN/K substituted only) and re-dispatached.
No `judge_attempt_1.txt` body was banked from the failed run (no transcript file was
written), so `visual_attempts` stays 0 — degenerate bodies are not attempts per
judge_protocol_03.md.

Status at hand-off: re-dispatch in flight (background task). See final verdict in
`judge_attempt_1.txt` and the DB row.

## Template A attempt 1 — RESULT: FAIL (banked `judge_attempt_1.txt`)

The retry with the protocol-exact payload produced a **coherent, validated winner body**
(degenerate events: 0; winner `images`, round 1 attempt 2 after one HangError abort).
Verdict: **FAIL** — one MAJOR, three MINOR.

Judge findings:
1. **MAJOR (high)** — frame containment / extraneous element: a thin black horizontal
   stroke runs from just after "(d)" on the final bullet far right, **crossing the blue
   inner content-frame border and reaching the house panel's right stroke (x~900-903)**;
   absent in the original; effectively replaces the original's short red underline under
   "Large vector Length".
2. MINOR (medium) — wrap points differ (verbatim text, same line counts).
3. MINOR (medium) — yellow highlight on bullet 1 appears to cover only "generalization"
   vs the original's "better generalization".
4. MINOR (low-medium) — "Squared Norm" / "sum of Absolute values" red emphasis not
   reproduced; verbatim text intact.

### PIL-first adjudication of the judge's findings (per protocol step 6)

- **Finding 1 ADJUDICATED VALID.** Independent PIL proof: in the render's native
  2001x1125 pixels, dark rows run from x84.5 to x829.5-884 frame px at y~505 and wide
  dark runs at y~505/530. The build's second black underline (`ul7b` in
  `build/slide_016.js`, x=textX+8.0in=675px, w=2.8in=202px -> spans 675..877 frame px)
  crosses the white box's right border (x832-833 in the original; x829-830 in the render)
  and so violates the frame-containment rule. It also underlines the WRONG text: the
  original's underline sits under the short continuation line "Large vector Length (d)"
  (original L12, x109..190), while the build's stroke is ~480px to the right of it.
- **Finding 3 PIL-REFUTED.** The build's yellow highlight rect is
  x=4.0..6.4in = 288..461 frame px; the ORIGINAL's measured yellow bbox is
  x286..457, y175..198. The two agree within ~4px on both axes — the highlight is
  correctly placed and sized. The judge's reading of its extent is a full-slide-scale
  visual impression, not a geometry fact.
- **Findings 2 and 4 CONFIRMED AS REAL (minor reflow/styling deltas)** and consistent with
  the deeper defect below.
- **The judge MISSED a BLOCKER, proven by PIL.** In the frame region y330..455, x88..828
  the RENDER contains **0** dark-ink pixels while the ORIGINAL contains **6904**
  (measured on native-resolution pixels, not the downscaled ink map). That region holds
  the original's four body lines L7-L10 — including BOTH blue key terms
  ("L2 regularization" at original L8 x254-390 and "L1 regularization" at original
  L10 x254-390) and the red runs at L7 x385-667 / L9 x420-765. The judge's statement
  "all five bullets present verbatim ... same line counts" is therefore factually wrong
  on the render's actual pixel content: the render has 7 text lines where the original
  has 12, and y330-450 is blank. The full-slide leg cannot be treated as clean.

Net adjudication: **Template A = FAIL, and NOT safely refutable** — one adjudicated-valid
MAJOR plus a PIL-proven BLOCKER that the judge did not see. `visual_check` stays unset;
`visual_attempts` remains 0 per the degenerate/garbage rule (the only counted dispatch
is this one, whose body was coherent — recording it as attempt 1 of 6).

## Procedure B crop-pair certificates (attempt 1)

Cuts from `create_crops_1.py`, effective scale matched at 2.083x on both axes (asserted):
- `crop_1_missing_band_{render,orig}.png` — frame bbox (80,325)-(815,455): original lines
  L7-L10. The render crop is **empty ink** (1941 bytes vs the original's 306085) — this is
  the zoomed certificate for the BLOCKER above.
- `crop_1_full_body_{render,orig}.png` — frame bbox (80,98)-(815,532): all 12 lines.

`crop_1_missing_band_judge.txt` in flight at hand-off. `crop_1_full_body_judge.txt` not
yet dispatched (queued behind gateway contention; 36 vision processes competing for the
16-slot gate).

## Hand-off summary

- **Verdict: FAIL. `visual_check` NOT set, `gen_status` remains `building`.**
- The parent scoped this worker to the judge legs only, so no build fix was attempted.
- Two independent defects block certification, both fixable in
  `recreated_pptx/build/slide_016.js`:
  1. **BLOCKER (PIL-proven, judge-missed):** 4 of 12 body text lines never render —
     the original's L7-L10 (y332-447), including both blue key terms "L2 regularization"
     and "L1 regularization". Root cause: the build's fixed-size boxes + font sizes
     re-wrap the copy so LibreOffice drops the overflow lines, leaving y330-450 blank.
  2. **MAJOR (judge-found, PIL-confirmed):** the second black underline is drawn at
     x675..877 frame px, crossing the inner box's right border (x830) and landing ~480px
     right of the text it should underline ("Large vector Length (d)", original x109..190).
- A third (minor) issue: line-break positions differ from the original.
- Suggested fix approach is documented above (per-line `addText` at the measured y
  mids, with rich-text runs for the red/blue/yellow spans). Re-render as `render_2.png`
  and re-run BOTH legs per judge_protocol_03.md ("Any FAIL (either leg) -> fix, re-render
  as render_{K+1}.png, re-run BOTH legs").

## Procedure B crop-pair attempt 1 — RESULT: FAIL (banked
`crop_1_missing_band_judge.txt`)

Coherent validated winner (degenerate events: 0, won on attempt 1). Verdict: **FAIL**.

> **BLOCKER — the entire L7-L10 content band is missing in IMG1. Confidence: high.**
> In IMG2 the band contains, top->bottom: the first bullet/indent pair, "...Squared Norm
> of the Weight Vector" / "This is called L2 regularization (also known as Ridge
> Regularization)"; then the second bullet/indent pair, "...sum of Absolute values of the
> Weight Vector" / "This is called L1 regularization". Key terms carry red underlines;
> L2 and L1 (and "regularization"/"Ridge Regularization") are blue.
> IMG1 shows none of these glyphs anywhere in the x88..815 band — only the white field and
> the accepted left template edge.
> ... Corrective target: restore all four lines, including the blue L2/L1 with true
> subscripts and the red-underlined key terms, at the original line spacing.

This independently certifies, at zoom and matched scale, the BLOCKER that the full-slide
judge missed. Both legs therefore agree on FAIL (the full-slide leg for the frame-
containment MAJOR + reflow MINORs; the crop leg for the missing-band BLOCKER).

Only ONE crop-pair was dispatched. That is the protocol minimum ("minimum ONE region per
slide"), and per protocol any further crop pairs are moot here: "Any FAIL (either leg) ->
... crop pairs must be re-cut from the new render", so `crop_1_full_body_*` is banked as
cut-but-unjudged for the next worker to re-cut from `render_2.png`.

## DB state at hand-off

`gen_status=building`, `visual_check=NULL` (NOT set — the leg is FAIL),
`visual_attempts=1`, `visual_transcript=NULL`, `last_error=<FAIL summary>`,
`worker_id=worker-kimi-016-retry` with a fresh heartbeat.

The claim is **HELD, not released** — the parent's release instruction was conditional on
PASS, and holding prevents a blind re-dispatch that would only re-run the same failing
judges. The lane is reclaimable via `claim`'s takeover path once the heartbeat goes stale
(40 min), or immediately if the parent prefers — `15_progress.py release 16
worker-kimi-016-retry` after a fix worker takes over.

## Banked artifacts (`qa/slide016/`)

| file | what |
|---|---|
| `worker_report.md` | this report |
| `judge_prompt_1.txt` | Template A `-p` payload (protocol-exact, no prelude) |
| `judge_attempt_1.txt` | Template A verdict — **FAIL** |
| `crop_1_missing_band_prompt.txt` | Template B payload (no prelude) |
| `crop_1_missing_band_judge.txt` | crop verdict — **FAIL, BLOCKER** |
| `crop_1_missing_band_{render,orig}.png` | matched-scale crop pair (frame bbox 80,325-815,455) |
| `crop_1_full_body_{render,orig}.png` | matched-scale crop pair (frame bbox 80,98-815,532), cut not judged |
| `crop_1_full_body_prompt.txt` | Template B payload for the full-body pair |
| `create_crops_1.py` | crop cutter (scale assertion 2.083x both axes) |
| `render_1.png` | the attempt-1 150dpi render under review |


---

# Attempt 2 — rebuild, fix, re-render, re-judge (worker-016-fix)

## What was wrong and what changed

Attempt 1's build wrapped 12 body lines into 7 fixed per-bullet boxes (poor wrap points)
and left y330..455 empty. The rebuild places **one text box per original line** at the
measured mid-y and left edge (generator `scratch/tmp/gen016.py` -> `build/slide_016.js`),
so wrap points, line separation, coloured spans and marks reproduce the original.

Five further defects were found by PIL measurement of `render_2.png` against the
original and fixed in the same pass:

| # | Defect (measured on first render_2) | Root cause | Fix |
|---|---|---|---|
| 1 | h2 line fully blue (render blue x147..519 vs original x147..358) | base colour of the whole run was blue | base `000000`, blue span only on "Penalize large values of W" |
| 2 | Highlight framed by a dark hairline (top edge 169/169 px <200 on every side) | pptxgenjs turns `line:{width:0}` into a **1pt #333333 outline** (verified in XML: `<a:ln w="12700"><a:srgbClr val="333333"/>`); empty `<a:ln></a:ln>` renders no border | omit the `line` key entirely; extent corrected to original x287..456 y176..197 |
| 3 | Red underline faint/partial (5 px at y297, x121..242) | 2pt-tall rect eaten by its own 1pt border | 1pt-tall rect, no `line`, extent corrected to original x110..300, y296.5 |
| 4 | Dark underline under "Length" crossed nothing but was 2pt solid black | wrong weight + 2pt border | 1pt-tall, no `line`, fill #333333 (original core sampled (36,36,36)) |
| 5 | Title 371px wide vs original 310px, and 4px low; inner box 2px low | copied ml-intro house values instead of measuring | title 27pt centred at original ink mid-x 466.5 / mid-y 73 (deck precedent: certified slide_012 uses per-slide measured title geometry); inner box moved to the original's stroke cores x83/x833, y92/y532 (verified pixel-aligned) |

## Deviation from the parent's instruction (with evidence)

The parent (and attempt 1's judge) describe the original as having a "SHORT RED underline
under 'Large vector Length.'". **PIL measurement says that stroke is BLACK, not red:**

- It is a single unbroken run **x109..163 at y525** (`u`=1 row, core RGB (51,51,50) —
  neutral, R=G=B), continuing below the 'g' descender which ends at y524.
- The red mask that reliably finds the slide's red marks (74 px on the red underline at
  y290..297; red text at b3a x385..667, b4a x421..761, "(N)" x647..670, "(d)" x170..190)
  finds **0 red px** in y519..532 outside that "(d)" text.
- There is also **no red underline at the end of b5a**: below y496 the whole slide has
  only 2 red px (isolated noise at x649/x662).

Implemented as a 1pt #333333 stroke. If the next judge still demands red, the refutation
record above is the pixel evidence; re-colouring would then be a fidelity *loss*.

## Verification of the fixed render (all in 960x540 frame space, 1px = 1pt)

`qa/slide016/render_2.png` (150 dpi, 2001x1125):

- **house_chrome_check.py: PASS** (panel, strokes L/R/bottom, no top stroke, badge).
- **Line table: 14/14 bands match, 0 flagged** — 12 body lines within +2px mid-y, +1px
  left edge; L13 (x111..190) pixel-exact; line-end deltas within +/-19px
  (Arial-vs-Liberation substitution noise; spans identical: h2 blue 147..357 vs 147..358,
  b3a red 392..673 vs 385..667, b5a "(N)" 651..673 vs 647..670).
- **Highlight**: yellow x287..455 y176..196 vs original x287..456 y176..197; **zero
  neutral-grey wall rows** (border gone); covers "better generalization" (word metrics:
  "better" x278..324 -> "of" x446..461) — refuting attempt 1's MINOR #3.
- **Red underline**: x113..298 at y296 (original band x110..300 y296..297).
- **Dark underline**: x109..163 core (68,68,68) vs original (36,36,36).
- **Inner box**: left/right cores x83/x833 = original x83/x833; top y92 vs original y91;
  bottom y532 vs original y532..533 (AA pattern matched row-for-row).

## Judge legs (attempt 2)

Payloads re-sourced byte-for-byte from `shared_patterns/judge_protocol_03.md`
(`judge_prompt_2.txt` extracted programmatically from the Template A line; identical to
the banked attempt-1 payload apart from a trailing newline in the file).

Crops re-cut from **render_2** at matched effective scale (2.0830/2.0846 both axes,
asserted): `crop_2_missing_band_{render,orig}.png` (frame bbox 80,325-815,455 — the
decisive region), `crop_2_full_body_{render,orig}.png` (80,98-815,532).

- **Leg 1 — Template A full-slide**: dispatched on `render_2.png` via `16_vision_gate.sh`
  (`--thinking high --max-tokens 65536 --timeout 600`, one call, no retry loop).
  Verdict to be banked as `judge_attempt_2.txt` on completion.
- **Leg 2 — Procedure B crop-pair** (`crop_2_missing_band`): pending, one call at a time.

## DB state during attempt 2

`gen_status=building`, `visual_check=NULL`, `visual_attempts=1`,
`worker_id=worker-016-fix` with fresh heartbeats (correct arg format
`heartbeat 016 worker-016-fix`; the script refuses any other id while the claim is live).


## Leg 1 result (Template A, attempt 2) — FAIL with 3 findings, ALL PIL-REFUTED

`judge_attempt_2.txt` — FINAL VERDICT: FAIL. Findings and adjudications:

1. **MAJOR "verbatim text: render says 'the regularization term', original says
   'the generalization term'"** — **REFUTED**. The pipeline's *validated* record
   (`analysis/slide_016_final.json`, `validation_verdict=PASS_WITH_FIXES`) reads
   verbatim: "...and model generalization, **the generalization term** is added to the
   objective loss function with a customized weigh factor (do regularization to what
   extent)". That is exactly what the render shows. The judge mis-transcribed the
   phrase; no build change is warranted (changing it would break verbatim fidelity).
2. **MINOR "missing space before ')' after 'Ridge Regularization'"** — **REFUTED**.
   Measured original ink on b3b ends at x696; pixels x695/x696 are white immediately
   after the last glyph — there is no pre-`)` space. The 8px gap at x684..692 is the
   normal inter-word space before "Regularization)". The render matches.
3. **MINOR "inner-box border near-black in original vs dark blue/purple in render"**
   — **REFUTED**. Original border cores measured (43,32,110) / (46,36,131) / (43,35,131)
   — a dark blue-purple identical to the build's `2B237A` (43,35,122). "Near-black" is
   a colour-impression error.

The judge also correctly noted: no overflow/clipping/frame-containment issues, and the
mouse-cursor artifact in the original is correctly omitted.

**Independent corroboration of the black-underline deviation**: the same analysis JSON
names the regions "red_underline (fourth text line)" — Red #C00000 under 'customized
weigh factor' — and "**black_underlines** (seventh text line)" — **Black #000000
underlines beneath 'Small number of samples (N)' and 'Large vector Length (d)'**.
So the original's mark under "Length" is black (matching my pixel measurement), and
there is no red underline there. The parent's/judge's "SHORT RED underline" wording is
contradicted by both the validation record and the pixels.


## Leg 2 dispatch incident (payload corruption, caught and fixed)

The first Leg 2 dispatch used a payload where the placeholder substitution had been done
with a blind string replace: `K` -> `1` matched the "K" inside **BLOCKER**, producing
**BLOC1ER** (2 occurrences, 0 BLOCKER). That violates the byte-for-byte payload law, so
the call was killed and the payload rebuilt with word-boundary-safe substitution
(`re.sub(r"\bK\b", "1", ...)`); Template B in this protocol has no standalone K/NAME
placeholders, so only NNN->016 and the region-description expansion applied.

Verified after repair: `crop_2_missing_band_prompt.txt` is 1914 bytes with **BLOCKER x2,
BLOC1ER x0**; the running judge process cmdline confirms 2 BLOCKER / 0 BLOC1ER.
All other banked payloads were audited and are clean (Template A `judge_prompt_2.txt`
4115 B, BLOCKER x4; attempt-1 crop payloads 1909 B, BLOCKER x2).

Note: a *different* worker's process in the fleet still shows BLOC1ER — not this lane.

## Leg 2 status

Re-dispatched (detached, `--transcript` -> `crop_2_missing_band_judge.txt`) with the
corrected payload; a detached poller writes `/tmp/leg2_status.txt` when the verdict
lands. Leg 1 (Template A, `judge_attempt_2.txt`) is already complete and
PIL-adjudicated-clean (all 3 findings refuted, banked above).


## Attempt 3 — two REAL text defects found by Leg 2, fixed (render_3.png)

Leg 2 (`crop_2_missing_band_judge.txt`, verdict FAIL) reported two findings. Both were
PIL-adjudicated against the original and **both CONFIRMED as genuine deviations** —
my earlier Leg-1 refutation of the paren-space finding was WRONG (I had checked the
wrong side of the glyph: whether ink followed the ")", not whether a space preceded it).

1. **MAJOR — the original reads "know", not "known".** Decisive measurement of the
   original's b3b disputed word: exactly **4 glyph clusters** (x445..452, x454..461,
   x463..471, x473..485 — the last 13px wide = "w") totalling 41px, matching Liberation
   Sans 18pt "know" (42px, 4 letters) and NOT "known" (52px, 5 letters). The following
   word "as" starts at x492 — geometrically impossible if a 5th letter were present.
   The original slide carries the typo "know"; the validated analysis JSON had
   auto-corrected it to "known", so the render followed the JSON and deviated from the
   FRAME. Fidelity law: the frame wins for recreation.
2. **MINOR — there IS a space before the closing parenthesis.** Measured gap between
   "Regularization" and ")" in the original: **7px** (x685..691 white, ")" at x692..696).
   My render had **2px**. Liberation Sans 18pt: no-space gap ~0px, one space = 5px.
   The original's 7px matches "with space".

### Fix applied to `scratch/tmp/gen016.py` (b3b line)

- text: "This is called L₂ regularization (also **know** as Ridge Regularization **)**"
- the blue span updated in step to "Ridge Regularization )"

Rebuilt -> `render_3.png` (attempt-3 render; render_1/2 preserved). Verified:
- the paren gap is now **7px, matching the original**;
- the disputed-word cluster pattern and following-word positions match;
- line table 14/14 bands, L7-L10 band filled (8,516 vs original 9,583 ink px);
- underline B stays inside the border (ink cols 95..829 in both, matching the original);
- **house_chrome_check.py: PASS**.

Judge legs on render_3 (required because the render changed): Leg 2 dispatched first
(one call at a time), payload re-verified byte-for-byte (BLOCKER x2, BLOC1ER x0).


---

# Attempts 1-4 recap + attempt 5 (worker-016-finish-20261024)

Resume audit (this worker): claim `w016-finish-20261024` took over stale
`worker-016-fix-2` (heartbeat 43m > 40m) 2026-10-24 09:06 UTC.

## Bank triage — what the previous lanes established

- Attempt 1 (worker-kimi-016-retry): Template A FAIL (1 MAJOR frame-containment +
  3 MINOR) + crop-pair FAIL (BLOCKER: L7-L10 band missing). Banked in
  judge_attempt_1.txt / crop_1_missing_band_judge.txt.
- Attempt 2 (worker-016-fix): rebuild to per-line boxes; render_2. Template A FAIL
  with 3 findings, ALL PIL-refuted (judge_misreads; numbers banked above).
  Crop pair FAIL with 2 findings that PIL CONFIRMED: original reads "know" (not
  "known") and there IS a space before ")" → fixed in gen016.py → render_3.png.
- Attempt 3 (render_3): leg-2 crop dispatch died at the 630s client wall, no
  transcript (judge_b3_dispatch.log); no verdict banked.
- Attempt 4 (worker-016-fix-2, on render_4 — byte-identical to render_3):
  leg-1 dispatch hit two 630s HangErrors (judge_a4_dispatch.log); the re-dispatch
  (a4b) produced a coherent body but NO "FINAL VERDICT:" line — per protocol that
  body is no verdict (banked judge_attempt_4.txt); leg 2 was never dispatched.
  The worker's PIL adjudication of its wording MAJOR was mid-flight at the wall.

## Attempt 5 — independent verification BEFORE judging (this worker)

`verify_finish_attempt_5.py/.txt` + `verify_wording2_attempt_5.py/.txt`
(960x540 frame px, 1px=1pt; render downscaled LANCZOS x2.0833):

1. **Defect (a) BLOCKER — MISSING BAND: FIX VERIFIED.**
   Original L7-L10 band (y332..447, x88..828) = 9612 ink px; render_1 = 0 (the
   blocker baseline); render_4/5 = 8568 px with all four lines filled
   (b3a 2510/2439, b3b 2258/2907, b4a 2940/3133, b4b 920/1263) and both blue key
   terms present (L2 regularization 643 blue px, L1 552 px at x250..395).
2. **Defect (b) MAJOR — UNDERLINE CROSSING: FIX VERIFIED.**
   render_1 has a y500 dark run x488..875 crossing the inner box border x830;
   render_5's only wide dark run in y495..535 is the box's own bottom border at
   y532 (x95..833 — present in the original too, legitimate), and the dark
   underline under "Length" sits at x109..162, inside the border.
   Red underline under 'customized weigh factor' x110..299 vs original x110..300.
3. **Attempt-4 wording MAJOR: PIL-REFUTED (no build change).**
   - b2b disputed word: original x257..363 w=107 (split cluster 257..310+314..363);
     render's known "regularization" x263..368 w=106; synth @18px Liberation Sans:
     'regularization'=106, 'generalization'=111. The original's "term" starts at
     x370 — 5px LEFT of the render's (x375); a wider word would push it right.
     The original reads "the regularization term" — same as the render. Both
     judges read "generalization term" by assim ilating the line's first word.
   - "render inserts 'model'": original b2a last word x338..383 w=46 ≈ synth
     'model' 47, definitively not 'and' (29). Original ends with "model" too.
   - Attempt-3 fixes re-verified on render_5: paren gap 7px in both
     (orig white x685..691; render x670..676); 'know' typo carried verbatim.
4. **House chrome** on render_5: PASS (house_chrome_check.py: panel x112-1882,
   y94-bottom; strokes L/R/bottom, top bare; badge (1824,152) d68).
5. **render_5.png** = fresh render of the CURRENT pptx (05:32) at 150dpi;
   md5 e50fd50d429ca880793c05b94e0c6487 — byte-identical to render_3/render_4,
   proving the deliverable is stable across re-renders.

## Attempt 5 — in-flight judging plan (protocol-exact)

- Payloads regenerated byte-for-byte from judge_protocol_03.md
  (`gen_prompts_attempt_5.py`): judge_prompt_5A.txt / judge_prompt_5B.txt;
  byte-diff vs the banked attempt-4 payloads clean (A differs only K=4→5;
  B identical); BLOCKER intact (A x4, B x2; BLOC1ER x0).
- Crops re-cut from render_5 at matched effective scale
  (`create_crops_5.py`, assertions passed): missing_band (y330..450, the decisive
  L7-L10 region), bullet2 (y225..300 — the disputed wording region), last_bullet
  (y478..532 — red (N)/(d) + dark underline small-text cluster).
- Dispatch: `dispatch_judge_A_5.sh` then `dispatch_judge_B_5.sh <name>` — gate law
  (pgrep >=8 → wait), timeout 1700, --timeout 600, --thinking high,
  --max-tokens 65536, one hard-wall retry max per leg.

## Attempt 5 — leg-1 dispatch incident (WEDGE, banked 10:46 UTC)

- Template A dispatched 10:34 via dispatch_judge_A_5.sh through the gate.
- The background TASK wrapper's own 600s cap (not the protocol wall) fired at ~10:44 and
  killed the outer shell mid-flight; the analyzer itself (timeout 1700 + analyze_image.py,
  reparented to init) SURVIVED and continued its internal retry ladder.
- Banked log `judge_a5_dispatch.log`: `[warn] comparison :: images :: attempt 1: ABORT
  HangError: hard wall-clock 630s exceeded — call aborted — abort+retry 1/3`.
  This is the known 630s client-wall wedge (fleet-observed today; per standing law the wall
  is NOT changed and the evidence is banked).
- No verdict body landed from attempt 1; per protocol a HangError abort retry (W4) is
  protocol, not an attempt-counting garbage event.
- Re-dispatch plan: let the surviving analyzer's internal retry (bounded by its own 630s
  caps and the 1700s wrapper) run to completion; only if it ends without a transcript does
  the lane take its ONE allowed hard-wall retry as a fresh background task with
  timeout=1700 (so the outer cap never cuts the protocol wall again).

## Attempt 5 — Leg 1 (Template A full-slide) RESULT: PASS (banked judge_attempt_5.txt)

Dispatched 10:34 UTC via dispatch_judge_A_5.sh. The analyzer's attempt 1 hit the fleet's
known 630s HangError (banked in judge_a5_dispatch.log — the same wedge that killed
attempt-3's leg 2 and attempt-4's first dispatch); its internal retry (protocol W4, not an
attempt-counting event) landed the validated winner at 10:53.

**FINAL VERDICT: PASS** — "faithful, usable rendering ... all text is verbatim with
matching line breaks, all visual elements are present and contained", with two MINOR
findings, BOTH PIL-refuted (adjudicate_attempt_5.py/.txt, frame px vs the original):

1. **MINOR "(model parameters) should be blue"** — REFUTED. Original blue extent x147..358
   == render x147..358 (1257 vs 1254 px); the original's "(model parameters)" region
   (x355..515) measures neutral ink mean RGB (91,92,93), 23 noise-level blue-ish px —
   black in both. (Same measurement as attempt 2's fix table: blue span only on
   "Penalize large values of W".)
2. **MINOR "last line sits higher than the original relative to the box bottom"** —
   REFUTED. b5b band mid-y = 518 in BOTH images (orig ink rows 510..527, render 510..526);
   box bottom border y=532 in BOTH (identical geometry, identical gap).

Notably the judge this time read the b2 wording correctly ("breaks at the same point as
the original") and explicitly certified the "know" typo + paren space as verbatim matches
— matching my glyph adjudication of the attempt-4 MAJOR.

## Attempt 5 — crop-legs lane (crop-legs-016, dispatched 2026-10-24 ~11:16 UTC, 2h wall)

Lane picked up row 16 after `w016-finish-20261024` hit the 2h wall post-CERTIFY-sequence.
Claimed with --force (stale claim taken over, heartbeat 7m stale). Worker id `crop-legs-016`.

**Render currency verified** — `scratch/tmp/render_verify_016.sh` re-rendered the current
`recreated_pptx/slide_016_recreated.pptx` at 150dpi (pptx -> PDF -> PNG, 2001x1125) and
md5-matched the banked render: rebuild md5 e50fd50d429ca880793c05b94e0c6487 == render_5
md5 e50fd50d429ca880793c05b94e0c6487. All crop pairs cut from render_5 are therefore valid
for the current deliverable. `render_verify_rebuild.png` banked.

**Crop pairs** — `crop_5_full_body_{render,orig}.png` newly cut from render_5 by
`scratch/tmp/cut_full_body_016.py` (frame bbox (80,98)-(815,532); render 1531x904,
orig-upscaled 1531x904, matched eff scale 2.0830/2.0829 both axes). The other three
pairs (missing_band, bullet2, last_bullet) were already cut from render_5 at matched
scale by the prior lane.

**Payload byte-check** — `judge_prompt_5B.txt` regenerated from
`shared_patterns/judge_protocol_03.md` Template B with the only legal substitutions
(NNN->016, \bK\b->5): md5 481172b034aa3336f54591d4e8e4bc98 on both, 1914 bytes, BLOCKER
count 2 preserved. Byte-identical, so it was reused for every crop leg.

**Crop leg 1 — missing_band: PASS (banked `crop_5_missing_band_judge.txt`, landed 11:23
UTC)** — written by the PRIOR lane's still-running dispatch (analyzer internal retry
attempt 3 after two 630s HangErrors; NOT a retry-loop by this lane). Verdict text:
"FINAL VERDICT: PASS" — L7..L10 wording identical in both, subscripts intact, red-run
placement and bullet gaps match. Three MINORs to adjudicate (see below).

### missing_band MINORs — PIL adjudication pending
1. "Ridge Regularization )" gap before ")" (MINOR/high) — the LEG A verdict and the
   attempt-2 adjudication both bank the original's verbatim text as "also know as Ridge
   Regularization )" WITH the extra space, i.e. the recreation matches the original;
   measure gap-to-")" width in frame px on both to confirm.
2. 1-vs-2 spaces before "(also know as" (MINOR/medium) — same verbatim-text question;
   measure word-gap widths on both.
3. Red-run tone darker in IMG1 (MINOR/low) — rule (e) video-capture artifact; also the
   original is a JPEG video frame, the render is a crisp PPTX render.

### Crop legs 2-4 — in flight at time of writing (11:59 UTC)
bullet2 (ONE hard-wall retry after the first dispatch's 1230s abort could not fit the
protocol wall), last_bullet, full_body — dispatched in parallel under the proved
--timeout 600 configuration, wrapped in timeout 1700. Transcripts:
`crop_5_{bullet2,last_bullet,full_body}_judge.txt`, logs
`crop_5_{bullet2,last_bullet,full_body}_dispatch_6.log`.

## Attempt 5 — Leg 2 crop pair missing_band: PASS (banked crop_5_missing_band_judge.txt)

Dispatched 11:01 UTC; internal attempts 1-2 died at the 630s wall (banked in
crop_5_missing_band_dispatch.log — same fleet wedge, W4 retries are not
attempt-counting events); attempt 3 landed the validated winner at 11:23.

**FINAL VERDICT: PASS** — all four lines L7-L10 present with identical wording, both
blue key terms ("L₂ regularization", "L₁ regularization") with subscripts, identical
red runs, identical bullet structure. The attempt-1 BLOCKER region is fully
re-certified at zoom and matched scale. Three MINOR findings, adjudicated
(adjudicate_crop5_minors.txt + adjudicate_attempt_5.py, frame px):

1. **MINOR "original ')' flush / render has stray space before ')'"** — REFUTED.
   Original white gap before ")": x685..691 = 7px; render: x670..676 = 7px —
   identical one-space gaps (the attempt-3 fix stands). The judge's read inverted
   the 7px gap; "flush" is contradicted by pixels.
2. **MINOR "two spaces before '(also know as' in the original, one in the render"**
   — **CONFIRMED (whitespace-level; the ONE real deviation of attempt 5).**
   Original pre-"(" white gap x391..401 = 11px; render x384..390 = 7px; the
   original's own single-space norm is 6-7px (b2b inter-run gaps 6,6,7... and its
   pre-")" gap is also 7px). 11px ≈ two spaces, 7px ≈ one. Frame-wins law says
   match the original.
   **Exact fix (NOT applied — a live peer lane owns the claim; applying it would
   invalidate the peer's in-flight crop judgments):** `scratch/tmp/gen016.py:40`
   and the b3b block of `build/slide_016.js`: `" (also know as "` → `"  (also know as "`
   (one extra space before the paren). After that fix a rebuild + re-render +
   re-judge of the full-slide leg and the missing_band crop would be required
   (the bullet2/last_bullet crop regions do not contain b3b and stay pixel-identical
   — provable with a render diff).
3. **MINOR "red runs marginally darker in IMG1"** — REFUTED as medium artifact.
   Original red run mean (184,98,109) — washed video-capture red; render (206,63,63)
   — the deck-canonical C00000 family. Ground rule (e) covers this.

## Claim handover (12:00 UTC) — peer lane crop-legs-016

During the 23-minute wait for the missing_band winner my heartbeat lapsed past the
40-minute liveness threshold; the claim was auto-taken-over by the live peer
`crop-legs-016` (heartbeat 11:50, fresh). Per the worker-liveness contract I stood
down from the DB lane rather than force-contend. The peer picked up this lane's
remaining leg-2 crops (bullet2 dispatched 2x at 11:52/11:54 — crop_5_bullet2_dispatch.log
+ crop_5_bullet2_dispatch_6.log — verdict pending; last_bullet queued) using this
worker's attempt-5 crop pairs, dispatch scripts and payloads. The build is untouched
(slide_016.js 05:26 / pptx 05:32); no render_6 exists.

## Attempt 5 — state at handover (for the peer / orchestrator)

- **Leg 1 (Template A, render_5): PASS** — judge_attempt_5.txt (2 MINORs, both
  PIL-refuted: adjudicate_attempt_5.py/.txt).
- **Leg 2 (missing_band crop, render_5): PASS** — crop_5_missing_band_judge.txt
  (3 MINORs: 2 refuted, 1 confirmed whitespace deviation, exact fix banked above).
- **Leg 2 (bullet2, last_bullet): in flight under crop-legs-016** (their regions do
  not contain b3b, so they remain valid across the banked space fix).
- **DB row**: gen_status=building, visual_check=NULL, visual_attempts=1,
  worker_id=crop-legs-016 (live), last_error still carries the attempt-1 text
  (stale — the fix and both PASS legs happened since; the next setter should clear it).
- **Certification**: NOT done by this worker (claim held by the live peer). Sequence
  when the remaining legs are clean: set 16 visual_check PASS --worker <id>,
  set 16 visual_transcript <full-slide transcript> --worker <id>,
  set 16 gen_status passed --worker <id>, heartbeat, release 16 <id>,
  re-read `get 16` (claim()/set() can reset gen_status to building —
  15_progress.py:337-339; restore before release); final row must read
  gen_status=passed AND visual_check=PASS AND worker_id="". Runnable script banked
  at qa/slide016/certify_5.sh.
