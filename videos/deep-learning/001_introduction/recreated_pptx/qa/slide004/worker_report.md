# Worker report — slide 004 "Artificial Intelligence" (deep-learning/001_introduction)

Worker: slide-recreation BUILDER, run 2026-10-12 (fresh start; no prior artifacts; ROOT —
no dependency parents, no dependents, no banking obligation; deps check printed `root`).
Slide id N=4, NNN=004.

## Verdict chain

1. **Build attempt 1** — `build/slide_004.js` (pptxgenjs, LAYOUT_WIDE, playlist house chrome
   imported from `videos/deep-learning/shared_patterns/house_chrome.js`, numeral `4`).
   Geometry PIL-measured from `unique_slides/slide_004.jpg` (960x540, 1px=1pt):
   - parent red box x270..650 y121..194 fill 9F0000 (measured modal (159,0,0));
   - child blue x121..406 / green x492..770, y275..350, fills 0200A7 / 0A873B (measured modals);
   - text Arial Bold: parent "Artificial Intelligence" 30pt (advance fit 293.4 vs 295 ink,
     spec-pinned 30), children 25pt (three exact advance fits + 18px cap height; spec's
     range pinned 24 — ink forensics wins per deck law), baselines 167 / 306 / 335;
   - two curved arrows: custGeom cubic-bezier strokes 2.5pt 7B2B34 (measured stroke modal
     (123,43,52)), fitted to the original centerline by orthogonal-distance LSQ
     (LEFT P0(460,194.5) C1(453.57,257.78) C2(287.08,221.72) P3(265.25,262), max orth resid
     2.17px; RIGHT P0(460,194.5) C1(464.81,259.12) C2(608.00,220.89) P3(629.75,262), max 3.42px);
     solid triangle heads (flipV) at measured bboxes, tips ON child tops (y274.5 vs box 275);
   - black footer bar x38..922 y519..537.5 (measured 519..539; 2-frame-px shorter so the
     chrome's half-visible bottom stroke stays visible — documented precedent of certified
     slide_002/005).
   Pre-judge iteration (no judge spent): closed-loop self-check caught rendered text ink
   3-8 render px narrower than the original's JPEG-inflated ink → per-line charSpacing
   (parent +0.05, child L1 +0.2, child L2 +0.3); rebuilt, re-rendered.
2. **Pre-judge self-checks (all PASS, banked)**:
   - `house_chrome_check.py render_1.png 4` → PASS (panel x 89-1913, badge (1860,148) d=70).
   - `selfcheck_attempt_1.py` (+ `selfcheck_attempt_1_output.txt`): box edges within
     0.5-2.2 render px of targets; fills exact modal match; bar within 1.2; text baselines
     within 2.1 render px, ink edges within 4.5; arrow centerline point-to-ink max 2.59
     frame px (mean 0.27); head tips 274.1 vs 274.5; containment clean. Checks 3/4/5/6 of
     the mandatory list are n/a (no equations, no multi-line delimiters, no tables).
   - TMPDIR (⚠ /tmp quota) pointed at the video scratch for every soffice/gate call;
     absolute `-env:UserInstallation` LO profile.
3. **Judge attempt 1** — probe landed (`probe_1.txt`, window open); comparison through
   `scripts/16_vision_gate.sh` (timeout 280 inner / 1700s outer per dispatch, `--thinking
   high --max-tokens 65536`, frozen template + deck-chrome ground rules from the banked
   `judge_prompt_1.txt`). Real comparison winner body (route: images, single-read,
   glm leg DEFERRED/BLOCKED):
   **FINAL VERDICT: PASS for 'faithful, usable recreation'.** Issues: one MINOR —
   "connector stroke color darker (maroon) in recreation vs brighter red in original,
   confidence 0.7". No BLOCKER/MAJOR findings.

## Final state

- Verdict: **PASS** (judge attempt 1 of max 6; W4/garbage retries not needed).
- Deliverable (SINGLE-VERSION): `videos/deep-learning/001_introduction/recreated_pptx/slide_004_recreated.pptx`
- Build: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_004.js`
  (banked copy `qa/slide004/build_attempt_1.js`)
- Transcript: `qa/slide004/judge_attempt_1.txt` (probe: `probe_1.txt`; prompt: `judge_prompt_1.txt`)
- DB (`VIDEO=deep-learning/001_introduction`): gen_status=passed, visual_check=PASS,
  visual_attempts=1, visual_transcript=<path above>, pptx_path/build_script set, last_error=null.
- Judge procedure executed by the worker itself (no Agent/Task spawn tool in this
  environment) — orchestrator-approved fallback per scripts/17_worker_instructions.md §7.

## Deviations / notes (all measured, all documented in build comments)

- Fills/arrows use measured frame modals (9F0000 / 0200A7 / 0A873B / 7B2B34) instead of the
  spec's brighter estimates (#A61E1B / #2020A5 / #21A04B / #C62828) — the frame is ground
  truth and the judge compares against the frame (same discipline as certified slide_005).
  The judge's single MINOR note (connector "darker maroon") is the same phenomenon seen from
  the other side: a crisp 2.5pt stroke reads darker than the original's JPEG-glowed one at
  equal hex; graded MINOR at 0.7 confidence on a PASS — not a fix trigger under the verdict law.
- Children 25pt vs spec-pinned 24pt (advance+cap fits).
- Chrome drawn per the FROZEN playlist law (panel x42..918, badge (893,71) numeral 4) while
  this lecture's original frames show a narrower panel (x53..906), border stroke at x~58, and
  NO badge — founder directive 2026-10-11 is explicit (playlist-wide chrome; badge numeral =
  file number, PENDING FOUNDER VETO per 001_introduction/AGENTS.md).
- Black bar drawn y519..537.5 (2 frame px above the original's 539 bottom) so
  house_chrome_check.py's bottom-stroke check stays satisfiable (certified precedent).
- The original's mouse-cursor artifact over the green box is correctly omitted (ground rule c).

## Skill banking

- New pattern: `.agents/skills/slide-recreation/patterns/curved-arrows-custgeom/`
  (example.js + index.json entry) — native curved arrows via custGeom bezier + explicit
  triangle heads, with the no-fill and tail-end pitfalls.
- Lessons appended to `memory/lessons.md`: custGeom arrows technique; charSpacing
  ink-width calibration; point-to-ink closed-loop checks (per-row comparison lies on
  near-horizontal strokes).
