# Worker report — slide 043 "Problem: Image will vanish  if applying more filters in cascade" (001_introduction, Deep Learning DSAI 308)

Date: 2026-10-12. **RE-RESUME worker**: the previous builder died on an API connection
timeout after ~143 min, banked 34 qa files (full build + calibration + measurement
forensics + selfcheck chain), and died before/around judging (no judge transcript
banked). This worker resumed from that banked state and took the slide to certification.
Judge attempts used: **1 of 6** (0 banked before this run).

## Verdict chain (per attempt)

0. **Banked intake (predecessor, ~06:00–07:18):** measurement forensics
   `measure_original{,2,3,4,4b,4c,5}_out.txt` + crops; LO baseline calibration
   (`calib{,2,3}.pptx` + `_measure_out.txt`); build `build/slide_043.js` (07:05) →
   `slide_043_recreated.pptx` (07:07) → `render_1.png` (07:07); selfcheck chain
   `selfcheck_attempt_1(.py|_out)` (29 fails), `1b_out` (10 fails), `1c_out` (1 fail:
   conv2 ctr x +6.64); banked render crops `crop_render_title/conv2.png` (07:18) —
   predecessor died here, before any judge call. **No banked judge attempt existed.**
1. **Banked-state verification (this worker):** re-rendered the CURRENT pptx (soffice,
   private profile, TMPDIR scratch inside the namespace) → **md5 identical to
   `render_1.png`** (`541d8a61…`) — the banked state is real; continued into pre-judge
   checks without a rebuild.
2. **Selfcheck FAIL resolution (all PIL-verified as checker artifacts or stale targets,
   no build changes needed):**
   - `conv2 ctr x +6.64` (1c's only FAIL): scan region x670..870 included the red panel
     border at x845 — border ink (lum 192 < 460) inflated the bbox. Clean region
     (x<840): render label ctr 753.22 vs original 755.00 → **delta −1.78, in tolerance**.
   - `_1_out` 29 fails: grid5/grid3 col+row −3.00s = fill-band pollution (green fill
     lum 293 / sage 450 inside the checker band); title left/right/top = chrome panel
     border + badge caught by the scan region; `num(0,0)` +5.9/+2.8 = red annotation
     ink inside the digit scan box; `content left 41.3 < 43` = chrome border itself.
   - `1b` residual fails: bullet3 band bottom −5.3 = descender assumed on a
     no-descender line ("Details are lost", measured 199.6 ≈ baseline 199.9); annot
     blob count 16 vs 9 = glyph pairs (18 connected components pair into 9
     annotations, verified by component analysis).
   - Label centers (clean bands, render vs original): Image (−0.40,+1.48), conv1
     (−1.11,+0.35), conv2 (−1.78,−0.60) frame px — all inside the ~4px/150dpi
     tolerance; widths within 4px.
3. **Pre-judge closed-loop (this worker, all banked):**
   - `house_chrome_check.py` on `render_1.png`: **PASS** (panel x 89–1913, y 95→bottom;
     badge center (1860,148) d=70; tol 8).
   - Mandatory dense-region crop comparisons (check 6; the slide has table grids):
     - `cropcmp_grid5.txt` (Image 5x5 + x0/x1 annotations, 2x): **PASS** — all 25
       values exact, 9 red annotations exact incl. checkerboard pattern and
       bottom-right placement, colors match; MINOR: "Image" label weight/size
       (ground rule (d)).
     - `cropcmp_conv.txt`: body truncated mid-list with NO verdict line (default
       8192-token budget) — no evidentiary value; its mid-body MAJOR claim (arrows
       ~50% taller/longer, gap 20 vs 45 crop px) was **PIL-refuted** (original arrows
       49.0×19.0 px vs render 50.9×20.6 — outline-stroke delta; gap to the 18 cell
       13.0 vs 12.1 frame px) and did NOT reproduce.
     - `cropcmp_conv2.txt` (re-run, --max-tokens 32768): **PASS** — values, geometry,
       arrows, centering all match; MINORs compression-class only.
4. **Judge attempt 1** (the only judge attempt; visual_attempts=1):
   - Banked `judge_prompt_1.txt` (deck-chrome GROUND RULES prelude: white FFFFFF
     canvas, gray E9E9E7 panel x42..918 y45→bottom, red C00000 border, badge
     FDFD96/6A5ACD at (893,71) d≈36 numeral 43, badge-absent-in-original note,
     black-bar/top-strip/cursor artifact omission) + the FROZEN template from
     `scripts/17_worker_instructions.md` verbatim; `-p` payload banked byte-for-byte
     as `judge_payload_1.txt` (chrome paragraph + generic GROUND RULES string).
   - Gateway probes: 2 short-wall probe hangs (150s outer, per template) during a
     deep fleet-queue period; window-open proven by the crop comparisons landing;
     proceeded per dispatch walls.
   - Comparison: `--thinking high --max-tokens 65536 --timeout 280 --rounds 1 --tries 1`
     inside `timeout 1700` outer, through `scripts/16_vision_gate.sh`. Landed first
     try: **validated winner** (`[winner] images (round 1, attempt 1)`, degenerate
     events 0, rc=0). Winner body ends **"FINAL VERDICT: PASS for 'faithful, usable
     recreation.'"** No BLOCKER/MAJOR; judge explicitly confirmed verbatim text incl.
     the double-space quirks ("vanish  if", "filter  of", "be3x3"), all grid values,
     the x1/x0/x1 checkerboard, arrows, box text, and containment. Two MINOR notes
     (yellow-column width ~0.5 conf; conv2 label few-px-left ~0.4 conf) — both
     sub-perceptual and PIL-contradicted (cells uniform 39.0px; label delta −1.78px);
     not fix triggers.
   - Judge procedure executed by the worker (no Agent/Task spawn tool in this
     environment; orchestrator-approved fallback per `scripts/17_worker_instructions.md`
     §Judge step 7). Certificate: single-read, default route (images), glm leg
     DEFERRED/BLOCKED.

## Build facts (inherited from the banked build — unchanged, all PIL-measured)

- Geometry/baseline constants per the banked `build/slide_043.js` header comment:
  title TimesB 29pt C00000 baseline 83.7; panel x81..845 y111..380; bullets URW Gothic
  20.7pt (Century Gothic metrics; original face not installed — ground rule (d));
  grid5 x244..438.5 y228..375, cells 39×29.6, fills FDFF0B/0DC94F (measured), Verdana
  Bold 16 numbers; 9 red FF0000 x1/x0 Comic-10pt annotations in the checkerboard that
  matches the slide-041 filter [[1,0,1],[0,1,0],[1,0,1]] (frame is ground truth; the
  spec's "3+3 under cols 1/3" was a spec-side guess — deviation documented by the
  predecessor, and the judge + crop comparison confirmed the frame match); grid3 sage
  95A38A cells 48×37 at 510/562/614 × 248/287/326 with 887240 borders; cell18 49×36;
  arrows rightArrow 50×20 at (451,296)/(676,296.5) white/black, adj2 zip-patched;
  explanation box x77..859 y393..509.5 white + navy 000080 border, 4 Times navy lines
  21/21.2pt, verbatim quirks preserved.
- Chrome: `shared_patterns/house_chrome.js` imported (numeral 43) — never re-drawn.
- No equations (mathtext/OMML laws n/a — the matrices are value grids); no advanced
  graphs (graphgen n/a).
- Artifacts omitted per spec brief step 17 + ground rule (c): bottom black bar
  (y518..539), top gray strip, mouse cursor (~790,90).
- Web-source evidence: `slide_043_source/SOURCES.md` (Goodfellow ch.9 Fig 9.13, d2l
  7.3, CS231n) — cascade arithmetic 5x5→3x3→1x1 and values verified; no corrections.

## Deliverables & DB

- PPTX (single version, unchanged since 07:07): `videos/deep-learning/001_introduction/recreated_pptx/slide_043_recreated.pptx`
- Build script: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_043.js`
  (per-attempt copy banked: `qa/slide043/build_attempt_1.js`)
- DB: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
  `visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide043/judge_attempt_1.txt`,
  `pptx_path`/`build_script` set, `last_error=null`.

## Deviations / notes

- No build changes were made by this worker — the banked build was verified sound
  (md5-identical render) and certified as-is.
- Documented (predecessor) deviations, judge-accepted: substituted fonts (URW Gothic
  for the bullet face, Comic Sans MS for the handwriting labels, Times for the title)
  — original faces not installed; ground rule (d) class.
- The 2 short-wall probe hangs + the truncated first conv-crop body are banked as
  evidence (`cropcmp_conv.txt` + log); the re-run (`cropcmp_conv2.txt`) carries the
  verdict.
- No banked evidence deleted; nothing written outside the video namespace (scratch
  under `qa/slide043/_scratch_resume/`); `unique_slides/` and `frames/` untouched.
- Slide 43 has no dependents in `slide_dependencies.json` (not a dependency-graph
  parent; row `depends_on`/`pattern_group` null) → no component-banking obligation.
