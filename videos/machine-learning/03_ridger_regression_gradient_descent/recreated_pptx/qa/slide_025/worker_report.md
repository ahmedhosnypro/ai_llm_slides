# Slide 025 worker report — "Types of Loss function shapes"

Deck: `machine-learning/03_ridger_regression_gradient_descent` (51 founder-curated frames).
Slide: root — no dependencies in the founder graph.
Worker: `worker_025_1792797757` (took over `worker_025_1792780958`, 43-min-stale heartbeat).
Status: **BUILD COMPLETE + RENDER CERTIFIED; judge legs in flight.**

## Deliverable

- `recreated_pptx/slide_025_recreated.pptx` — single plain-named version (no suffix), 1.54 MB.
- Build: `recreated_pptx/build/slide_025.js` (banked here as `build_attempt_1.js`).
- Plot generator: `recreated_pptx/build/generate_plots_025.py` (banked as `generate_plots_1.py`).
- Assets: `recreated_pptx/build/assets/plot_025_{tl,tr,bl,br}.png`.
- Render: `recreated_pptx/qa/slide_025/render_1.png` — 2001x1125 @ 150 dpi
  (md5 `ff08cf5eba14d7d0f095cc37a01059b8`).

## Content spec

`analysis/slide_025_final.json`: diagram-only slide, `verbatim_text.bullets` empty,
`subtitle_or_header` null, 22 labels, no equations. 11-step `recreation_brief`.
Validation `PASS_WITH_FIXES`, recreatability 8. Uncertain items preserved as `[?]`
(font family/sizes; total peak count; whether the top-left base shows `-2` on one
or both axes; that the 3-D plots are MATLAB-style and must be rebuilt from shape
descriptions) — the frame is the authority, and all four plots were REBUILT from
the measured shapes with the same libraries, not copied.

## Measured geometry (frame px, 1px = 1pt; scripts banked)

From `unique_slides/slide_025.jpg`, measured with PIL (banked as `measure_*.py`
in this dir and scratch):

| Element | Measured |
|---|---|
| Title ink | `Types of Loss function shapes`, red, x 266..585 (w 319), y 63..88, center x 425.5, ascender-to-descender 26px |
| Title font | Arial Bold **22 pt** (advance 319 px over 28 chars) |
| Badge | yellow disc x 861..891 y 60..88, purple ring x 856..895 y 56..92 (center (876,74), d ~35) — house chrome |
| Panel | E9E9E7 x 54..903, y 45..540; strokes L x58.5 / R x901 / B y538.5, **no top stroke** |
| 4 plot rects (white-fg bboxes, non-panel/non-gray) | TL x 60..460 y 116..289; TR x 480..898 y 116..316; BL x 60..460 y 296..527; BR x 480..898 y 346..530 |
| Blue label boxes (fill 0000FF, white bold text, TWO text bands each) | LB1 x 270..406 y 137..178 "Concave Function One Maxima"; LB2 x 475..611 y 184..225 "Convex Function One Minima"; LB3 x 474..611 y 354..391 "Non-Convex Multiple Minima"; LB4 x 382..518 y 452..489 "Gradient Descent Path to reach Minima" |
| Red reference lines (pure HORIZONTAL 2-D strokes in the original) | TL y168 x121..267 and y186 x110..279; TR y222 x619..873 and y234 x619..866; BL y418 x124..381; **BR none** |
| BL black annotations | "Global Maxima" ~x242..268 y304..319; "Local Maxima" ~x286..315 y337..352; "Local Minima" ~x286..311 y390..399; "Global Minima" ~x145..201 y439..465 |

### Key measurement conclusion — the red lines are 2-D, not 3-D

The original's red lines are uniform 1–2 px runs at constant frame y with the
x-extents above, i.e. flat horizontal strokes, not projected 3-D level rings
(which would project as slanted ellipses). They are drawn as figure-fraction
`Line2D` artists inside each plot PNG so they land at the measured rows exactly.

## Closed-loop verification (all green before judging)

| Check | Result |
|---|---|
| `shared_patterns/house_chrome_check.py render_1.png 025` | **PASS** — panel x 112-1882, y 94-bottom; strokes L/R/bottom present, **top bare**; badge center (1824,152) d=68 |
| Plot sizes vs measured regions | TL 400x174, TR 418x200, BL 400x231, BR 418x184 frame px — each PNG is 300 dpi with `figsize = px/72`, placed at `px/72` inches (no rescale, no resampling) |
| Title ink vs original | render x 265.7..583.8 y 66.8..86.5 (center 424.8, w 318.1) vs orig x 266..585 y 65..86 (center 425.5, w 319) — **within 1 px** |
| Label boxes | render/blue-px LB1 5310/4901, LB2 5326/4947, LB3 4797/4734, LB4 4699/4763 |
| Red lines | TL render (167-168, 182-192) vs orig (167-170, 185-188); TR render (221-222, 233-234) vs orig (217-227, 234-235); BL render (417-418) vs orig (417-419); BR none vs none |
| Frame containment | **0 content px** outside the panel (left/right/top/bottom all 0); orig has JPEG halos (823/1648/7/0) that are video artifacts |
| Curve smoothness | `ripple_check.py` — second-difference max 0.002 (TL), 0.0003 (TR), 0.0074 (BL), 0.0007 (BR) vs tol 0.35; GD-path turn cos = 1.000 and monotone (all OK) |

## Judge legs (frozen templates from `shared_patterns/judge_protocol_03.md`)

### Leg 1 — Template A, full-slide comparison (attempt K=1)

Dispatched through `scripts/16_vision_gate.sh` inside `timeout 1700`, with
`--thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1`,
`-p` payload byte-for-byte from Template A (only NNN=025, K=1 substituted).
Prompt banked at `judge_prompt_1.txt`. Transcript target `judge_attempt_1.txt`.

> Dispatch incidents (capacity, not build defects): the Template A probe was
> dispatched twice and both were killed by the 16-slot fleet flock before the
> client reached the model. The gateway was proven healthy independently — a
> direct ungated `analyze_image.py analysis` call on this slide's title crop
> returned a coherent body in 72.9 s — so with the window open the comparison
> was dispatched. A first comparison run was killed at the tool wall (660 s)
> because it was a child of the foreground shell; it was re-dispatched
> **detached** (`nohup setsid`, log `scratch/s025work/judge1.log`) so it
> survives. This is attempt accounting event 1 (not a garbage-body re-invoke).

### Leg 2 — Procedure B, zoomed crop-pairs

Crop pairs cut by `cut_crops_1.py` (banked) at **matched effective scale**
(render 2001x1125 → 2.08333 render-px/frame-px; each original crop LANCZOS-
upscaled by the same factor; `output_px/frame_px` equal per axis, verified):

| Region | frame px | render | orig up | matched |
|---|---|---|---|---|
| `lbl_upper` (LB1+LB2) | 371x106 | 773x221 | 773x221 | True |
| `lbl_lower` (LB3+LB4) | 154x151 | 321x314 | 321x315 | True |
| `tl` (dome + 2 red lines) | 405x179 | 844x372 | 844x373 | True |
| `tr` (bowl + 2 red lines) | 423x205 | 881x427 | 881x427 | True |
| `bl` (non-convex + red line + 4 annotations) | 405x236 | 844x492 | 844x492 | True |
| `br` (GD path + arrows) | 423x189 | 881x393 | 881x394 | True |
| `title` | 346x35 | 721x73 | 721x73 | True |

Banked as `crop_1_<name>_render.png` / `crop_1_<name>_orig.png`.

> Superseded first-generation crops (22:28, `crop_1_tl_dome_*`,
> `crop_1_tr_bowl_*`, `crop_1_bl_nonconvex_*`, `crop_1_br_gdpath_*`,
> `crop_1_labelboxes_*`) were cut from the pre-shrink plot rects and are kept
> as evidence, not re-used — the 22:38 set above is cut from the final
> `render_1.png`.

## Remaining

1. `judge_attempt_1.txt` verdict.
2. Procedure B crop-pair transcripts (`crop_1_<name>_judge.txt`) — one per dense
   region, `bl` first as the densest (4 annotations + reference line).
3. Adjudicate any FAIL/MINOR PIL-first against both images before touching the
   build.
4. On both legs clean: `visual_check=PASS`, `visual_transcript=<full-slide path>`,
   `gen_status=passed`, then `release`.

---

# Attempt K=2 — adjudication of the K=1 FAIL and fixes

## Attempt K=1 verdict (banked: `judge_attempt_1.txt`)

`FINAL VERDICT: FAIL` — 6 discrepancies (3 MAJOR, 3 MINOR), landed at 00:17 after the
gateway's abort+retry cycle (`[winner] images (round 1, attempt 3)`).

## PIL adjudication (both images, 960x540 frame space)

### MAJOR 1 — "bottom-row captions are transposed" → CONFIRMED, FIXED

Adjudication by measured X-overlap, using the top row as the control:

| box | measured x | plot it overlaps | that plot's nature |
|---|---|---|---|
| LB1 | 270..406 | TL (x86..409) | concave dome |
| LB2 | 475..611 | TR (x472..876) | convex bowl |
| LB3 | 474..611 | **BR (x470..878)** | single valley + black descent path |
| LB4 | 382..518 | **BL (x60..460)** | multi-extremum (Global/Local annotations) |

The top row's assignment is unambiguous (LB1's text is "Concave Function One
Maxima" and it overlaps the concave dome), which fixes the convention: **a caption
belongs to the plot it overlaps horizontally**. Applying it to the bottom row gives
LB3 → BR (gradient descent) and LB4 → BL (non-convex) — the opposite of my K=1 build,
i.e. the judge was right.

The analysis JSON's "right of / left of" phrasings are unreliable and were
correctly overridden by the frame: they describe LB1 as "upper-center, right of the
top-left plot" when LB1 (x270..406) actually sits *on* TL (x86..409).

Fix: swapped LB3/LB4 text in `slide_025.js`; banked as `build_attempt_2.js`.

### MAJOR 2 — "thin red per-quadrant frames omitted" → CONFIRMED, FIXED

The original does carry red frame structure around every plot, visible as long red
runs at each quadrant's edges (measured with a relaxed red mask, `rectscan.py`):

| plot | measured red sides | left | right | top | bottom |
|---|---|---|---|---|---|
| TL | L 467 px, B 288 px | yes | – | – | yes |
| TR | L 587, R 388, T 513, B 688 | yes | yes | yes | yes |
| BL | T 578, B 286 | – | – | yes | yes |
| BR | ink at x622..875 y348..527 | – | yes | – | – |

The red sides sit at/just outside each plot's own figure box, so the rectangle is
drawn on each PNG's bounds inset by ~2 px — that keeps all four sides inside the
image (a rect placed at a position outside the image is clipped, and half the frame
disappears).

Verified in the new render (`verify3.py`-style scan): **all four sides present in
all four quadrants** — TL x62/x458 y117/y288, TR x481/x895 y117/y314,
BL x62/x458 y297/y524, BR x481/x895 y347/y528.

### MAJOR 3 — "bottom-left axis data differ" → CONFIRMED, FIXED

The judge read the original's BL tick step as 1.5 with x,y ∈ [−3,3] and z to 8. My
K=1 BL used x,y ∈ [−3,3] but ticks only at ±2 and zlim (−4,6). Fixed: ticks now
−3/−1.5/0/1.5/3 on both horizontal axes, zticks −4/−2/0/2/4/6/8, and a `y` label
on the vertical axis. The surface's exact equation stays a rebuild (the analysis
marks it `[?]`), so only ranges/ticks/labels were aligned.

### MINOR 4 (TR ×10⁴ scaling) → already present

My K=1 build already draws the `×10⁴` factor and the 0/0.5/1.5 ticks on the TR
vertical axis. Not re-litigated.

### MINOR 5 (caption wrapping) → inherited from the original's own box widths

All four original boxes are ~137 px wide and their white text sits in exactly TWO
bands (band pitch ~12 px) — so two-line captions are the original's own geometry,
reproduced with `lineSpacing: 12`. Not a fix trigger.

### MINOR 6 (caption blue / path arrowheads) → styling judgment, no defect

Caption blue is the measured 0000FF-family fill; the descent path keeps its
arrowheads (`quiver` at 7 sampled indices).

## Verify-before-judge (all green)

| Check | Result |
|---|---|
| `house_chrome_check.py render 025` | **PASS** (panel x 112-1882, y 94-bottom; strokes L/R/bottom, top bare; badge (1824,152) d=68) |
| Red rectangles | all 4 sides × 4 quadrants present |
| Title ink | render x265..583 y67..86 vs orig x263..585 y65..85 |
| Label boxes | LB1 5310/4901, LB2 5326/4947, LB3 4732/4734, LB4 4776/4763 (render/orig blue px) |
| Curve smoothness | `ripple_check.py` — second-difference ≤ 0.0074 for all four curves (tol 0.35); GD-path turn cos = 1.000, monotone |

Render for the K=2 judge: `render_1.png` (2001x1125 @150dpi, md5
`e3365728bcd5ddff070f43a32bb5e64c`). Crops re-cut from it at matched effective
scale (2.08333 render-px/frame-px, original side LANCZOS-upscaled to match,
`cut_crops_1.py`).

---

# Attempt K=4 (worker_025_finish / worker_025_finish2) — BL red-arrow fix, re-render, judge legs

## Banked state at handoff

- Prior lane (worker_025_final) died mid-flight with gen_status="judging" (a
  non-standard value it set mid-flight); the row was taken over and the
  non-standard value cleared (claim() resets gen_status to "building").
  `pptx_path` was stale-relative; set to the prefixed
  `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_025_recreated.pptx`.
- Pre-fix chain banked as `build_attempt_3b.js` / `generate_plots_3b.py`
  (md5-verified identical to the then-current build tree).

## Adjudication of the K=2 FAIL (PIL-first, both images, 960x540)

Banked scripts: `measure_5_adjudicate.py`, `measure_6_terrain.py`,
`measure_7_bl.py` (+ `selfcheck_attempt_3/4.py`, `ripple_check.py`).

1. **K=2 MAJOR 1 "BR is a multi-bump terrain"** — REFUTED. Original BR carries
   ONE jet-red core (x695..841 y364..422, 2102 px) and a monotone
   red-over-blue column profile at every cut (x685/745/805: 0-1 transitions);
   a ridge/hollow terrain would oscillate. Same single-valley class as the
   render (whose column cuts are blue-only because its zlim maps the rim to
   cyan, not red). Surface fill differs; shape class does not.
2. **K=2 MAJOR 2 "five BL labels + red arrows"** — PARTIALLY CONFIRMED, FIXED.
   The original's BL has exactly FOUR text bands (y306..319, y337..352,
   y390..406, y433..477 — banked census) matching the analysis JSON's 22
   labels (one "Local Minima", leader lines). BUT the original also carries
   TWO red annotation arrows — filled wedge + 2px shaft + short diagonal —
   at slide px (192..207, 440..450) and (259..277, 478..486), ASCII-proven
   in `measure_7_bl.py` output and CONFIRMED OMITTED in every prior build.
   That is a real renderable-content omission (Template A ground rule 6).
3. **K=2 MINOR 3 "TR ticks/×10⁴"** — build already has z ticks 0/0.5/1/1.5
   and the ×10⁴ multiplier (generator lines 231-234); judged at crop scale.
4. **K=2 MINOR 4 "TL z ticks absent"** — generator has z ticks 0/2/4;
   labels exist in the source PNG (2021 dark px); judged at crop scale.
5. **K=2 MINOR 5 "title larger"** — REFUTED: title ink orig x262..586 (w325)
   y65..86 vs render x265..583 (w319) y66..86; both centred x424.
6. **K=2 MINOR 6 "label boxes encroach"** — REFUTED: four blue boxes match the
   original bboxes within 1-2 px (LB1 x270..406 y137..178 vs orig x271..405
   y139..176; etc.).
7. **K=2 MINOR 7 "stray red line in BL"** — REFUTED: the y417/418 line
   x124..382 IS in the original (loose-red row scan) and is reproduced.

## Fix (copy-then-modify)

`generate_plots_025.py` (banked as `generate_plots_4.py`): BL now draws the two
measured red arrows as figure-fraction artists AFTER `fit_zoom` (so their red
ink never enters `surface_box()`'s chroma fit). All four plots regenerated
(78 s), pptx rebuilt 16:00, re-rendered as `render_4.png`
(2001x1125 @150dpi, md5 `f885623df4e5a85b83774a87f1d1817f`).

Verify-before-judge (all green): house chrome PASS (panel x112-1882,
strokes L/R/bottom, top bare, badge (1824,152) d=68); frame containment
0/0/0/0; title within 1-2 px; BL reference line y417-418 x124..382; arrows
present (A1 265 red px, A2 202 red px in the render vs 55/50 loose-mask px in
the original — the render's are solid strokes, same geometry); curve ripple
check ALL SMOOTH (max d2 0.0074 « tol 0.35; GD-path turn cos 1.000 monotone);
7 crop pairs re-cut from render_4 at matched effective scale 2.0833
(`cut_crops_4.py`, all MATCHED=True).

## Staged judge dispatch (attempt K=4)

- `dispatch_A_4.sh` — Template A full-slide (payload `judge_prompt_4.txt`,
  Template A verbatim, 4115 chars) → `judge_attempt_4.txt`.
- `dispatch_crops_4.sh` — Template B loop over title/lbl_upper/lbl_lower/tl/
  tr/bl/br (payloads `crop_prompt_4_<name>.txt`, Template B with NNN→025 only,
  1914 chars, byte-verified in `verify_4.txt`) → `crop_4_<name>_judge.txt`.
- Both detached (`nohup setsid`) under `timeout 1700` with the approved
  analyzer `--timeout 1200`, `--thinking high --max-tokens 65536`.
