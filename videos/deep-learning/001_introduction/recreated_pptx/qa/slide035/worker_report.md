# Worker report — slide 035 (001_introduction, Deep Learning DSAI 308)

**Status: CERTIFIED — PASS.** DB row: `gen_status=passed`, `visual_check=PASS`,
`visual_attempts=1`, `visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide035/judge_attempt_1.txt`.

- Deliverable (single-version law): `videos/deep-learning/001_introduction/recreated_pptx/slide_035_recreated.pptx`
- Build script: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_035.js`
  (thin wrapper) around the certified component
  `videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_035.js`
- BANKING (mandatory — slide 41 depends on 35): component banked at certification with a
  0-PIXEL-DIFF PROOF: a scratch build requiring ONLY the component renders
  **md5-identical** (`7026327cb716e60234031d935e36c6bb`) to the certified render
  (`qa/slide035/render_2.png`, the judged artifact) — see `out_component_proof.txt`.
  The component exports `renderBase(pptx, slide, opts)` at BLOCK granularity
  (panelRect/leftGrid/filterTable/panelContent/labels/title/captionBox/captionL1/captionL2,
  with `opts.skip`/`opts.only` and `opts.numeral`), chrome via the shared
  `shared_patterns/house_chrome.js` primitive.

## Resume note

This run RE-RESUMED after an API-connection timeout killed the previous builder (~94 min
in, no dispatcher-visible outputs). The predecessor left ONLY `qa/slide035/crops/`
(8 upscaled dense-region analysis crops). They were verified as genuine frame crops
(e.g. `title.png` matches the frame at (254,60) at /2 scale, MAD 11.4 — banked in
`out_prep_assets.txt`) and PRESERVED UNMODIFIED, superseded for the build by fresh 1:1
measured crops. No measurement outputs / build script / pptx existed; attempt numbering
starts at 1 with this worker. Judge procedure executed BY THE WORKER via Bash (no
Agent/Task spawn tool in this environment — orchestrator-approved fallback).

## What the slide is

Title "How to Apply Filter on image" (red bold); left 5x5 binary Image grid (green digits
over a faint green-tinted photo, thick red border); middle 3x3 yellow Filter grid; right
white computation panel containing the 5x5 grid with its top-left 3x3 highlighted yellow
with tiny red x1/x0 multipliers, a 3x3 output grid with sage-filled '4' first cell, and a
black curved arrow; light-yellow caption box with soft blue border, two lines
(dot-product / PERCEPTRON sentence). Playlist house chrome (white canvas, gray panel + red
border, badge numeral 35) via `shared_patterns/house_chrome.js`. This frame is one of the
founder's SWAPPED frames (new 35 <- old 43) — `unique_slides/slide_035.jpg` is ground
truth, no second-guessing.

## Build decisions (measured, spec-loses-to-ink where noted)

- All geometry PIL-measured (6 passes banked: `out_measure_original{,2,3,4,5,6}.txt`):
  title ink x266..713 (center 489.5, cap 70, baseline 93); labels Image x105..183 cap
  181..199 / Filter x275..340 cap 182..201; left-grid border x78..241 y208..336; filter
  grid x270..364 y219..291; panel x379.5..885.5 y168.5..431.5; panel content x398..875
  y185..420; caption box x67..891 y445..508; caption L1 ink x78..881 (caps 454, baseline
  471); L2 ink x84..492 (caps 481, baseline 498, underline y499..501).
- LEFT GRID CROPPED WHOLE (x77..243 y207..337): the faint green-tinted photo cannot be
  drawn by pptxgenjs; digits + internal grid lines + red border ride along (slide_030
  photo+matrix / 034 meme precedent). Per-cell digit forensics confirm the spec rows —
  notably r1c2 is a '1' with a base serif (`out_measure_original5.txt` P7 ASCII), so the
  spec's "1 1 1 0 0" row stands.
- PANEL CONTENT CROPPED WHOLE (x398..875 y185..420): the black curved arrow is INTERTWINED
  line-art — it arcs from (497,210) over apex (~670,193) to its head at (732,213) INSIDE
  the sage '4' cell, crossing the yellow block's top row and the inter-grid gap
  (slide_029 cube+arrow / 034 intertwined-line-art precedent; pptxgenjs has no
  custom-geometry arc). Baked content includes the 5x5 grid with yellow 3x3 + multipliers,
  the 3x3 output grid (per-cell tan borders rendering the measured double-line interior
  boundaries), and the '4' cell.
- CURSOR INPAINT (spec exclusion + ground rule (c)): the screen-recording cursor
  (x727..743 y369..385, over plain white) inpainted out of the panel-content crop via the
  banked cursor-inpaint-restore pattern (plain-white variant). Integrity
  (`out_prep_assets.txt`): zone dark-px 95 -> 0, changed-px confined to the zone, 6
  sentinels identical.
- BLACK SCRUB BAR (y519..539) deliberately NOT recreated: spec marks it "not slide
  content" (capture artifact), certified convention slide_034/040; covered by judge ground
  rule (c).
- Fonts (PIL ink fits, `out_measure_original6.txt`): title Arial Bold 33pt C00000 (word
  inks spot-on); labels Arial Bold 27.5; filter digits Verdana Bold 15 ('0' 9x11 / '1'
  7x11 vs measured 10/7 x 11 — Arial's narrow '0' rejected); caption L1 Arial Italic 23.5
  (ink 804; word starts within ~2px); L2 Arial Bold Italic 23.5.
- COLORS: measured hues win over the spec's vision estimates per the deck's
  pixel-column-profile law — filter border #8BD33F (spec #C8A000), caption box fill
  #FCFEE9 (spec #FFFFE1), caption border #9797B2 (spec #0000FF), '4'-cell fill #95A38A
  (spec #6B6B47), title red C00000 (modal #A81828 = JPEG-darkened, deck precedent).
- CAPTION LINE 2 COLOR LAYOUT (documented deviation from the spec's estimate): pixels show
  '(' NAVY, "can be modeled  by " RED (core #920716 = JPEG-faded C00000), "PERCEPTRON" RED
  BOLD UNDERLINED (underline y499..501, 163 px = PERCEPTRON only), ' )' NAVY. The crop-C
  comparison independently confirmed this layout matches the original. Double space before
  "by" verbatim (measured 14 px gap).
- This original frame's panel border sits at x57..902 (faint red top edge y43-44) vs the
  canonical chrome x42..918 — playlist law fixes the chrome to canonical values
  (documented; judge ground rule (a); slide_029/034 certified precedent).

## Closed-loop checks (all banked)

- Renders: `render_1.png` -> closed-loop fixes (title y-1, L1 +2.5/-2.5, L2 +1.5/-4 +
  size 23.5) -> `render_2.png` (judged artifact).
- `house_chrome_check.py`: PASS on both renders (`house_chrome_check_attempt{1,2}_out.txt`).
- Self-checks: `selfcheck_attempt_1.py` (v1; its baked-feature FAILs diagnosed as
  crisp-vs-JPEG mask artifacts) and `selfcheck_attempt_2.py` + clean-zone verifications
  (`out_selfcheck_2.txt` tail) — ALL PASS: title, labels, filter table (separator #8BD33F
  exact), left-grid border, panel border, caption box/fill/border, L1 (caps 454.6 vs 454,
  desc 476.2 vs 476, right 882.2 vs 881), L2 (red span width 386.9 vs 387 frame px),
  navy parens present at target, containment (caption text in box, panel content in
  crop), cursor zone clean (0 nonwhite), badge numeral centered (892.6, 71.0 vs 893,71).
- Baked-placement proof: 1:1 downscale diff MAD 7.20 / 7.29 (sub-pixel best offset)
  (`out_verify_placement_1.txt`) — the two crops land at exact frame positions.
- Dense-region crop comparisons through the gate (full judge params):
  `cropcheck_A_filter_grid.txt` PASS, `cropcheck_B_panel_yellow3x3.txt` PASS,
  `cropcheck_C_caption_l2.txt` PASS. Their MINOR findings touching baked pixels are
  REBUTTED with numbers in `rebuttal_cropchecks.md` (crop-density resampling artifacts;
  bottom-border claim contradicted by `out_filter_border_check.txt`: 442 green px in the
  bottom band, 0 below — no clipping).

## Judge (attempt 1 — PASS)

- Procedure executed BY THE WORKER via Bash (no Agent/Task spawn tool — orchestrator-
  approved fallback, noted per the worker instructions). Probe (`probe_1.txt`) opened the
  window after two short-wall attempts (the first two were killed unlogged by an inner
  wrapper racing the script's own wall — wrapper widened, documented here); then ONE
  full comparison with `--thinking high --max-tokens 65536 --timeout 240`, inner
  `timeout 280`, outer `timeout 1700`, gate-mediated (`scripts/16_vision_gate.sh`),
  payload sourced byte-for-byte from the banked `judge_p_payload_1.txt`.
- Transcript: `judge_attempt_1.txt` — coherent winner body, `[winner] images (round 1,
  attempt 1)`, degenerate events 0, **FINAL VERDICT: PASS** for "faithful, usable
  recreation".
- Findings: 3x MINOR only — (1) Image-to-Filter gap proportionally wider (~2.7% vs ~1%;
  the gap is measured-identical 29 frame px by construction — judge variance on
  eyeballed proportions), (2) arrowhead grazes the '4' slightly more (baked pixels,
  rebutted by the placement proof), (3) image-grid numerals marginally bolder (baked
  pixels, same rebuttal). No BLOCKER/MAJOR, no fix triggers.
- Certificate label: single-read, default route (images), glm leg DEFERRED/BLOCKED.
- Attempts used: 1 of 6 (renders iterated 1->2 inside attempt 1 via the closed loop; no
  judge retries needed).

## Banking

- `recreated_pptx/build/components/slide_035.js` — certified component, block-granular
  `renderBase(pptx, slide, opts)`, chrome via shared primitive. 0-pixel-diff proof:
  scratch build requiring ONLY the component renders md5-identical
  (`7026327cb716e60234031d935e36c6bb`) to the certified render
  (`out_component_proof.txt`). Child slide 41 requires it by absolute path and draws
  only its delta.
- Provenance: `build_attempt_1.js` (judged wrapper) + `build_attempt_1_component.js`
  (component snapshot at certification) + `build_attempt_1_closedloop_r1.js`
  (pre-fix intermediate, preserved).
- No files outside the 001_introduction namespace were written; soffice/gate calls used
  TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/slide035 with an absolute
  -env:UserInstallation (root-fs quota pressure documented: first script write hit a
  transient ENOSPC, retried clean).

## Attempt ledger

| Attempt | Render | Verdict | Evidence |
|---|---|---|---|
| 1 | render_2.png (in-loop from render_1) | **PASS** | judge_attempt_1.txt |
