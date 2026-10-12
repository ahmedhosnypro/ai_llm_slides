# Slide 037 worker report — "How many filter can we apply on the image"

**VERDICT: PASS (judge attempt 2, on render_2).** Certified 2026-10-12.
Child of certified slide 36 (dependency edge 37←36).

## Deliverable

- **PPTX (single version, no suffix):** `videos/deep-learning/001_introduction/recreated_pptx/slide_037_recreated.pptx`
- **Build:** `recreated_pptx/build/slide_037.js` — thin runner that `require()`s the
  CERTIFIED parent component by absolute path
  (`build/components/slide_036.js`) and calls
  `renderBase(pres, slide, { numeral: "37", skip: [...], geom: { content_box: {...} } })`
  for the shared playlist chrome + the white-panel construct, then draws this slide's
  measured delta. The parent module was NOT edited (cascade law).
- **Assets:** `build/assets/diagram037.png` (crop (68,266)-(894,451) from THIS frame,
  826x185, edge-safety verified: top row clean, crop bottom on clean row 451, cube
  bottom stroke 448-450 fully captured), `build/assets/eq_735_037.png` + `.json`
  (mathtext `5 \; \cdot \; 7 \; \cdot \; 7 \; \cdot \; 3 \; = \; 735`, 22.5pt #D42A2A,
  600dpi, ink 220.6x17.2 frame-px vs original 222x16).

## Why the parent's slab tiles were NOT reused

The parent's component note said slide 37 "reuses the LEFT slab unit" — but template-
matching the parent's `slabtop036`/`slabbody036` tiles against frame 037 FAILED
(mean abs diff 62-95 at the best offsets across a ±200px search; the parent's slab is
~223px wide at (158,160)/(158,219), this frame's slab is a redrawn ~93px-wide unit at
(177,294)). Per the dependency law the child's frame is ground truth for every element,
inherited included → the whole hand-drawn diagram is cropped from frame 037 (imagery
law, certified 034/036 precedent). What IS imported from the parent: the playlist chrome
(via `drawHouseChrome` through `renderBase`) and the white-panel-with-red-border
construct (parent block `content_box` at overridden geometry x65 y262 w832 h250 — the
same construct, this frame's measured geometry; frame 036 has no x65/x896 border lines,
so these are real borders of THIS frame, and the x58 dark line present in BOTH frames
36+37 is a video-capture artifact, not recreated — certified-036 precedent).

## FOUNDER CROWDING RESOLUTION (directive 2026-10-12)

The original slide 37 crams 36's diagram under an added 3-line explanation box (diagram
band 249px tall vs 36's 345px). PIL forensics (scratch/slide037/measure1-5.py, banked)
found exactly ONE overlap-class defect, which the delta fixes deliberately:

1. **FIXED — equation shifted down 8 frame-px (ink top 479 → 487).** The original's
   equation band (y479..494) interleaves the question's descender band (to y483); the
   recreation gives the caption pair a clean 4.8 frame-px band gap and 7.0 frame-px
   clearance to the panel border (original had 16px). The pair's "directly below" intent
   is preserved. Carried into judge ground rule (e2) + the --view field (frozen -p
   otherwise verbatim).
2. **REPRODUCED at measured geometry** (tight but non-overlapping in the original):
   question ascenders 4px under the cube's bottom stroke; yellow-box text pads
   (13 top / 5 bottom, 9 left); 'RGB' label 7px under the panel border.
3. **INSEPARABLE — reproduced faithfully via frame crops, documented:** the
   filter-cluster overlap density (5 bright + 3 muted slabs heavily overlapped), the two
   tiny '7' labels sitting on the dashed lines, the dashed-line clutter, and
   'Depth=5 dims' flush against the cube's top edge — all baked original ink in
   `diagram037.png`.

## Verdict chain (evidence)

| Step | Result | Evidence |
|---|---|---|
| PIL forensics (5 passes) + vision reads (title / yellow box / panel / q+eq strip) | layout, text, colors measured; 3 visual lines in the box (wrap after "filters on"), '3 dims' area, '=' cyan bars x484..505 y358..365, cube x521..784 y285..448 | `scratch/slide037/measure1-5_out.txt`, `v_title.txt`, `v_yellowbox.txt`, `v_panel.txt`, `v_qeq.txt` |
| Font fits | title Arial Bold 35pt (adv 714 vs 709, deck precedent 036=35), yellow box Times New Roman 26pt mixed runs (L1 812/803, L2 344/336, L3 727/718 — consistent +1%), question Comic Sans MS 27.5pt (adv ≈510.5 vs 510), pitch 33 pinned | `scratch/slide037/fit_fonts_037_out.txt` |
| Attempt 1: house_chrome_check | PASS | `house_chrome_check_attempt1_out.txt` |
| Attempt 1: full PIL self-check | 6 fails — all placement rides-low (title +3, ybox text +2.6, question +4.4; checker cross-contamination of eq/question scans) | `selfcheck_attempt_1_out.txt` |
| Attempt 2 (centerShift fixes −3/−1/−4): house_chrome_check | PASS | `house_chrome_check_attempt2_out.txt` |
| Attempt 2: full PIL self-check | **0 FAILS** — title Δ≤0.8, ybox tops 149.8/182.9/216.0 (targets 150/183/216), pitch 33.1/33.1, L1 left 74.4, panel borders ≤1.2 off, question Δ≤2.7, equation EXACT (196.3,487.2 vs placed 196,487), band gap 4.8, eq→border 7.0, diagram tile meandiff 15 (JPEG noise), containment clean | `selfcheck_attempt_2.py` + `_out.txt` |
| Crop check 1 — question+equation strip (2x, thinking high) | **PASS** — verbatim text; equation offset + mathtext format explicitly recognized as sanctioned | `crop_qeq_check_1.txt` |
| Crop check 2 — yellow box (2x, thinking high) | **PASS** — identical text/wrap/bold runs/red 'same location'; MINOR: border tint/weight | `crop_ybox_check_1.txt` |
| **Judge attempt 2** | **PASS** — FINAL VERDICT: PASS; findings: 2 MINOR (box outline weight; baked-pixel contrast impression), equation offset acknowledged per (e2), no BLOCKER/MAJOR | `judge_attempt_2.txt` (transcript), prompt per `judge_prompt_2.txt`, `-p` per `judge_p_payload_2.txt` |

Judge MINOR findings and dispositions:
1. "Yellow box faint gray/olive outline vs original's softer edge" — measured: the frame
   HAS 2px muted strokes on top/bottom/left (modal (185,186,170)), NO right stroke;
   recreated exactly as 3 filled 2px rects #B7BAAB. MINOR, documented, no fix trigger.
2. "Diagram renders slightly larger/contrastier" — the tile is BAKED ORIGINAL PIXELS at
   the measured box (tile meandiff 15/765 per sampled pixel); pixel identity overrides
   the impression. Judge variance, no fix trigger.

## Deviations from the spec JSON (frame is truth)

1. **Explanation box = 3 visual lines** (spec said "two-line paragraph"): the first
   bullet WRAPS after "filters on" — L2 "the same location.  For Example:" (measured
   bands 150-173/184-200/216-238 + vision read). Reproduced with identical wrap points.
2. **Yellow box border:** spec/validation said "no outline" — the frame shows thin muted
   strokes on top/bottom/left (no right). Drawn as measured (#B7BAAB 2px, 3-sided).
3. **'same location' segment color:** spec #990000 (kept; deck's C00000 precedent applies
   to titles; measured core on yellow is JPEG-muddied (160,101,97), spec value kept).
4. **Equation:** spec "handwritten style red" — rendered per the professional-format law
   (mathtext PNG 22.5pt #D42A2A, the certified 036 equation red; spec's #E02020 is
   within JPEG noise of it), ground rule (e).
5. **Equation position:** +8 frame-px — the founder crowding fix (see above).
6. **Badge numeral "37"** (file number; 001_introduction originals carry no printed
   numbers — assumption PENDING FOUNDER VETO per video AGENTS.md).
7. **Player bar rows 519..539 excluded** (video artifact; ground rule (c)).
8. **x58 vertical artifact line excluded** (present in frames 36 AND 37 → capture
   artifact; certified-036 precedent).
9. Sources honored: `slide_037_source/SOURCES.md` (CS231n depth column; 5·7·7·3=735
   confirmed; downloaded `depthcol.jpeg`). No [?] items in the spec JSON.

## Concurrent-evidence note

This qa dir also holds forensics files this worker did NOT create (timestamps
09:46-10:12 interleaved with this run): `measure6.py/_out.txt`, `cmp_slab.png`,
`crop_full_panel.png`, `crop_midzone_x3.png`, `crop_panel_left/right.png`,
`crop_slabunit_x2.png`, `crop_title.png`, `crop_yellowbox.png`, `glyphA/B/C_x8.png`,
`grid_panel_x2.png`, `leftborder_x4.png` — apparently a concurrent investigation of the
same frame. They are preserved untouched (never delete banked evidence). Its banked
numbers INDEPENDENTLY CORROBORATE this worker's measurements: question x73..583
y453..478, equation x196..417 (modal red (172,14,37) — same), cube x521..784, Depth
label inside the crop box. No contradictions.

## Component banking

No component banked for slide 37: NOTHING depends on it — same-video dep graph has no
37→child edge, and `002_transformers_part2/slide_dependencies.json` contains no
`001_introduction` reference. The playlist-scoped banking obligation does not trigger.

## Judge procedure note

No agent-spawn tool was available in this environment → the judge procedure was
executed by the worker via Bash, byte-for-byte per the banked prompt (probe +
comparison through `scripts/16_vision_gate.sh`, transcripts banked), per 17 §7
fallback (orchestrator-approved). Verdict taken verbatim from the comparison winner
body. Single-read, default route (images), glm leg DEFERRED/BLOCKED.

## DB state (final)

`gen_status=passed`, `visual_check=PASS`, `visual_attempts=2`,
`visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide037/judge_attempt_2.txt`,
`build_script` + `pptx_path` set. Slide 37 CERTIFIED.
