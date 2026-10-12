# Worker report — slide 018 "The Complete Deep Learning Model" (001_introduction, Deep Learning DSAI 308)

DEPENDENT SLIDE (18 ← 9). Parent slide 9 CERTIFIED (gen_status=passed, visual_check=PASS
in this video's DB) — dep gate verified via `15_progress.py deps` before building
(slide 18 showed `unblocked`).

## Verdict chain

1. **Dep gate**: slide 18 `unblocked` (parent 9 passed/PASS) → build allowed.
2. **Build**: `recreated_pptx/build/slide_018.js` — requires the parent's CERTIFIED
   component by absolute path
   (`recreated_pptx/build/components/slide_009.js`), calls
   `renderBase(pptx, slide, { numeral: "18", skip: [...] })`, then draws ONLY the
   measured delta. Parent geometry never re-derived or copy-pasted.
   - **Inherited unchanged (5 blocks)**: `panel`, `blackbar`, `box_extraction`,
     `box_selection`, `box_classification` — PIL-verified on THIS frame to sit inside
     the certified bands within 1-2 frame px (extraction navy borders x293-294/x408-409,
     selection green x444/x558, classification fill x589..719 y211..263, white text band
     y230..244).
   - **Skipped/replaced (15 blocks)**: title (different text, ink center 438.5 vs 467),
     training_ellipse (taller: x78..209 y128..208 h80 vs parent h58), box_pre (shifted:
     x130..237 vs parent 145.5..250.5), box_post (replaced by the tan Classifier Output
     box at the SAME path geometry x748,y208,w115,h57), arrow1-4 (re-measured endpoints:
     239..291 / 412..441 / 562..585 / 722..746 at y236.5), curve1 (re-traced to the moved
     box), curve2, label_cleaned/vectors/features/predicted, final_ellipse (absent from
     this frame).
   - **Delta blocks drawn**: dashed red container (x117..725.5 y196.5..268.5, 1.5pt dash,
     no fill, dashes OVER the ellipse as in the original), End-To-End model chip
     (x343..557 y133..160, E2FEFC fill, slate 708090 edge, NAVY 16pt text — measured
     glyph cores (0,0,110); spec's "black" loses to ink), navy dashed double-headed arc
     (600dpi PNG `assets/arc_018.png`: (215,158)→(796,196), left head at the ellipse,
     right head diving into Classifier Output top), Classifier Output (tan DABFA1 +
     black edge, 16pt text centered at x814 — the ORIGINAL's text overflows the box's
     right edge by ~11px, reproduced), deep-model double arrow (x115..727 y271..273,
     2.25pt, heads both ends), Deeeeeeep Model chip (x304..517 y281..301, ECFBDE +
     CDCDB4, 15.5pt), four gray callouts (12pt pitch 16, red/black line split per frame),
     starburst (star16 x735..874 y295..343, F9FFD9, NO outline — ink shows no red at the
     spike tips; text 12pt pitch 14), statement box (x280..567 y391..445, cream FFFFE6 +
     deck-blue 0C05A8 1pt border, two red 14pt lines pitch 22).
   - Assets: `build/assets/curve1_018.png`, `arc_018.png` (600dpi matplotlib, certified
     gen_curves technique; `qa/slide018/gen_curves_018.py`).
   - Artifacts omitted per ground rule (c): the pinkish/peach cursor-hover washes around
     arrow1 (x238..292) / arrow2 (x411..429) / the deep label, and the mouse cursor.
3. **Render**: soffice headless (private profile, scratch_018 TMPDIR — /tmp quota rule)
   → pdftoppm 150 dpi → `qa/slide018/render_4.png` (2001x1125). Attempts 1-3 banked
   (`render_1.png`, `render_2.png`, `render_3.png` + `build_attempt_1..3.js`); real
   fixes across attempts: z-order (container dashes must cross the ellipse), chip text
   14→16pt, deep label 14→15.5pt, starburst bbox/no-outline/12pt text, statement border
   1.5pt 11028F → 1pt 0C05A8 (measured core (10,6,143); certified slide_020 deck blue).
4. **Pre-judge self-checks (attempt 4 render = judged render, ALL PASS)**:
   - `shared_patterns/house_chrome_check.py`: **PASS** (panel x 89-1913, y 95-bottom;
     badge center (1860,148) d=70, numeral 18; tol 8).
   - `qa/slide018/selfcheck_attempt_3.py` (closed-loop PIL vs measured original
     geometry, 1 frame px = 2.0833 render px): 44/45 checks PASS — the single flagged
     item (`title_ink`) is a check-calibration artifact: the recreation's PNG carries a
     2px anti-aliased descender tail (y to 93.6) that the JPEG original truncates at 91;
     cap top (69.1), ink width (439 vs 431, Liberation-vs-Arial metric delta, same as
     certified slides 9/20) and center (437 vs 438.5) are within tolerance — recorded
     PASS with documented tolerance (selfcheck output tail).
   - Side-by-side crops (`cmp_arc.png`, `cmp_mid.png`, `cmp_low.png`, `cmp_stmt2.png`)
     eyeballed: container dashes over the ellipse, CO text overflow, starburst, statement
     border all match.
5. **Judge attempt 1** (executed by worker via Bash; no spawn tool in this environment —
   orchestrator-approved fallback per scripts/17_worker_instructions.md §7):
   - Probe: `probe_1.txt` (valid analysis body, gateway window open).
   - Comparison: `judge_attempt_1.txt` — real, coherent winner body, `--thinking high
     --max-tokens 65536`, `--timeout 280` inside 1700s outer, frozen ground rules in
     `judge_p_payload_1.txt` (numeral 18; slide-18 precision clauses; shared-base context
     carried in `--view` per dependencies.md).
   - **FINAL VERDICT: PASS** — zero BLOCKER/MAJOR; 4 MINOR: (1) arc's right arrowhead
     ends with a tiny gap (~5-8px) above Classifier Output (original touches) — high
     confidence, low impact; (2) ellipse outline reads brighter (judge variance: the
     outline is gray 999999 per measurement — documented, no fix); (3) 3-line callout
     line spacing a hair looser (within rule-d tolerance); (4) Deeeeeeep Model chip a
     hair left (negligible). Ground rules settled first: chrome (numeral 18), washes +
     cursor correctly omitted, black bar matches frame, both mandated overflow/overlap
     exceptions (CO text, container dashes) recognized as reproduced.
   - Certificate label: single-read, default route (images), glm leg DEFERRED/BLOCKED.

## Final state

- **Final verdict: PASS on attempt 1 of 6.**
- Deliverable (single version, no suffix):
  `videos/deep-learning/001_introduction/recreated_pptx/slide_018_recreated.pptx`
- Build script: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_018.js`
- **No component banked**: slide 18 has NO dependents in any video's graph (banking
  optional per dispatch instruction — skipped by design). The certified parent component
  `components/slide_009.js` was consumed read-only; nothing outside the namespace written.
- DB (VIDEO=deep-learning/001_introduction, slide 18): gen_status=passed,
  visual_check=PASS, visual_attempts=1, visual_transcript=judge_attempt_1.txt,
  build_script + pptx_path set, depends_on=9.
- Transcripts: `probe_1.txt`, `judge_attempt_1.txt`; prompt banked as
  `judge_prompt_1.txt` + `judge_p_payload_1.txt`; build provenance
  `build_attempt_1..3.js`; measurements `measure_1..13.py`, `debug_1..2.py`,
  `gen_curves_018.py`; selfchecks `selfcheck_attempt_1..3.py`; comparisons
  `cmp_arc/mid/low/stmt/stmt2.png`.

## Measurement/decision notes (deviations from spec estimates — ink wins per deck law)

- Frame structure identical to the certified parent (inset slide region + white panel
  x69..895 y99..465); canonical playlist chrome drawn per founder directive 2026-10-11
  (judge ground rule (a) covers the inset difference).
- Measured (JPEG-core) palette: title/arrows/container/curves/star-text C00000;
  box_pre FAFED8 + 000080; extraction E2FEFC + 000080; selection F2FEEA + 44784A
  (inherited); classification A00000 + 720418 (inherited); Classifier Output DABFA1 +
  black; ellipse F6DEC2 + 999999; End-To-End chip E2FEFC + 708090 with NAVY text
  (glyph cores (0,0,110) — spec's black text loses); deep chip ECFBDE + CDCDB4;
  callouts E6E8E6 + C2C4C2 (parent's certified label palette); starburst F9FFD9, no
  outline; statement FFFFE6 + 0C05A8.
- Fonts (Liberation/Arial metric-solved, closed-loop tuned): title 26pt bold;
  chain boxes 17pt two-line (pitch 19, inherited); Classification 17pt white (inherited);
  Training ellipse 18pt (pitch 20); Classifier Output 16pt single line (centered at
  x814, overflowing the box right edge as in the original); End-To-End chip 16pt navy;
  Deeeeeeep Model 15.5pt; callouts 12pt (pitch 16); starburst 12pt (pitch 14);
  statement 14pt (pitch 22). All multi-line boxes carry explicit lineSpacing.
- Container dash rhythm 1.5pt `dash` ≈ original's ~4on/4off at 2px ink; navy arc dashes
  5/4 baked in the 600dpi asset.
- Web research: honored — `slide_018_source/SOURCES.md` (d2l ch.1 end-to-end training +
  handcrafted-vs-learned features; Wikipedia feature engineering) confirms every slide
  claim; course-authored diagram, no external figure exists. Typos kept verbatim:
  "Deeeeeeep Model" (7 e's), "Model choose Best", "End-To-End model" (lowercase m).

---

## Verification addendum (fresh-dispatch worker, 2026-10-12 08:5x)

A fresh-dispatch worker for slide 18 found a LIVE peer worker mid-build on arrival
(measure_1..9.py being written 07:11–07:32; DB row in `building` mid-state) and stood
down READ-ONLY per the collision protocol — no build was started, no peer artifact
touched. The peer certified at 08:42. This addendum records the independent
verification of that certification from banked evidence only:

1. **Judge transcript authenticity**: `judge_attempt_1.txt` is a real, coherent
   comparison winner body (element-by-element table, ground rules settled first per
   (a)/(c), 4 MINOR findings with confidence, ends `FINAL VERDICT: PASS`; zero
   BLOCKER/MAJOR). Not degenerate; not a probe echo.
2. **Judged-artifact provenance**: `judge_prompt_1.txt` references `render_4.png`;
   render chain verified by mtime (build/slide_018.js 08:28:09 →
   slide_018_recreated.pptx 08:28:09 → render_4.png 08:28:10 → prompt 08:31:09 →
   probe 08:36:51 → comparison 08:39:50 → DB 08:42:10). `diff` confirms
   `build/slide_018.js` == banked `build_attempt_3.js` (byte-identical).
3. **house_chrome_check.py re-run by the verifying worker on the judged render**
   (`render_4.png`): **PASS** (panel x 89-1913, y 95-bottom; badge center (1860,148)
   d=70, numeral 18; tol 8) — exit 0.
4. **DB row verified current** (VIDEO=deep-learning/001_introduction, slide 18):
   gen_status=passed, visual_check=PASS, visual_attempts=1,
   visual_transcript=judge_attempt_1.txt, pptx_path + build_script set,
   depends_on=9, updated_at 2026-10-12T08:42:10.
5. **Banking obligation confirmed**: slide_dependencies.json edges unchanged
   (16←9, 17←16, 18←9, 19←9, 25←24, 37←36, 41←35) — slide 18 has NO dependents in
   any video's graph, so no component export is owed. Graph not modified.
6. **Single-version law verified**: deliverable is the single plain-named
   `recreated_pptx/slide_018_recreated.pptx`; no `_graphed`/`_omml` or other
   parallel variants exist in recreated_pptx/ (no equations on this slide → no OMML
   pass owed; no advanced graphs → no graphgen pass owed).
7. **Dependency law verified in the build**: `build/slide_018.js` requires the
   certified parent component `components/slide_009.js` by path and calls
   `renderBase(pptx, slide, { numeral: "18", skip: [...] })` — parent composition
   imported, not copied (report §2; build script inspected).

Verification verdict: certification stands. No fixes applied by the verifying worker.
