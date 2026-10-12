# Worker report — slide 008, 001_introduction (Deep Learning DSAI 308)

Date: 2026-10-12. Worker: slide-recreation builder (fresh start; post-interruption survey
confirmed NO prior slide-008 artifacts — DB row `pending`, no build/, no qa/slide008/).

## Deliverable

- PPTX (SINGLE-VERSION, plain name): `videos/deep-learning/001_introduction/recreated_pptx/slide_008_recreated.pptx`
- Build script: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_008.js`
- DB (VIDEO=deep-learning/001_introduction, slide 8): `gen_status=passed`, `visual_check=PASS`,
  `visual_attempts=5`, `visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide008/judge_attempt_5.txt`,
  `pptx_path`/`build_script` set. Root slide, no dependents (slide_dependencies.json has no
  edges to 8) → no component-banking obligation.

## Verdict chain per attempt

- Attempt 1 — build v1 + render_1.png + house_chrome_check PASS + selfcheck_attempt_1: 9
  failures. Analysis: chrome elements (vertical rule, panel borders) polluted the check
  bands; bullets/headers had a real +3.0..3.9 frame-px vertical offset (LO line-layout
  model off). NOT judged (pre-judge fix). Banked: build_attempt_1.js, selfcheck output.
- Attempt 2 — build v2 (headers top = capTop − 12.5, bullets top = capTop − 13.3) +
  render_2.png + chrome check PASS + selfcheck_attempt_2: 2 failures — L1 title x-max
  −3.2 frame px (real, ~0.7% narrow advance) and rule-y-top (check band clipped at y50 —
  artifact). NOT judged. Banked: build_attempt_2.js, selfcheck output.
- Attempt 3 — build v3 (title charSpacing 0.1) + render_3.png + chrome check PASS +
  selfcheck_attempt_3 (fixed bands: rule band y35..530, title band x100..870):
  **ALL OK** — every position/advance/color/containment check green (max delta 1.7 frame px).
  Judge dispatch 1: probe OK (probe_3.txt), comparison ran but the worker OMITTED the
  `-p` payload in the shell command → model answered the script's default comparison
  prompt; coherent body, semantically pro-recreation, but NO literal FINAL VERDICT line →
  not certifiable evidence. Misfire banked as judge_attempt_3.txt.
- Attempt 4 — garbage-retry per worker-instructions §2b (same parameters, new transcript
  count): same worker error (payload still omitted) → same default-prompt shape, no FINAL
  VERDICT line. Misfire banked as judge_attempt_4.txt. Root cause diagnosed (payload
  extraction from judge_prompt_3.txt → judge_p_payload.txt, passed via `"$(cat …)"`).
- Attempt 5 — comparison re-run WITH the frozen GROUND RULES payload (byte-for-byte from
  the banked judge_prompt_3.txt): **FINAL VERDICT: PASS for 'faithful, usable recreation'**
  (judge_attempt_5.txt). Certificate: single-read, default route (images), glm leg
  DEFERRED/BLOCKED. Judge procedure executed by the worker itself via Bash — no
  Agent/Task spawn tool available in this environment (orchestrator-approved fallback,
  scripts/17_worker_instructions.md §7).

## Judge findings (attempt 5) and disposition

- All chrome differences (badge "8", red frame, gray panel) accepted per ground rule (a);
  original's black bottom bar + backdrop margins accepted as recording chrome.
- Content: title verbatim with identical two-line wrap; 3 headers verbatim (incl.
  "(for python)" lowercase); 11 bullets verbatim in order; box geometry within ~1%;
  frame containment satisfied; colors match; no missing elements; no visual-quality defects.
- 1 MINOR (medium conf.): "bullet line pitch ~8-10% looser (relative)". REFUTED by the
  closed-loop PIL measurement (selfcheck_attempt_3_output.txt): all 11 bullet cap tops
  within 0.4 frame px of the original (pitch mine 25.4-26.0 vs orig 25-26; paragraph gaps
  within 0.6 frame px). The model's original-side reads are rounded off JPEG-faded cap
  tops. Documented override per the ink law; not a fix trigger; does not block PASS.

## Forensics-driven deviations from the spec (ink wins — building.md)

- NO top red rule and NO top black letterbox drawn: the original frame has ZERO red ink
  above y43 and rows 0..41 are pure white (measure_original2/3.py). The spec's "Top rule
  at ~7%" + "Top letterbox strip" regions are video-frame artifacts/hallucinations.
- ADDED a full-height vertical red rule (1px, x58, y43..516) present in the original ink
  but absent from the spec.
- Black bottom player bar (y519..539) NOT drawn (spec step 13); mouse cursor NOT drawn
  (spec step 14, optional).
- Fonts metric-solved (Liberation/Arial TTFs): title Arial Bold 42pt (advance 735.2/263.8
  vs measured ink 733/262 at 42px; spec guessed ~40pt), headers Arial Bold 18.5pt (spec
  guessed ~18pt), bullets Arial Regular 18pt black 000000 (ink modal (0,1,0); spec guessed
  16-18pt / #1A1A1A).
- Content box border-centerline x71..460, y153..510 (spec estimated ~7-48% × 28-93% ≈
  x67..461, y151..502 — refined to ink).
- Chrome: playlist law (founder 2026-10-11) via shared_patterns/house_chrome.js import —
  white FFFFFF canvas, E9E9E7 panel x42..918 y45→bottom with C00000 border, badge
  FDFD96/6A5ACD at (893,71) d36, numeral "8" (file-number rule, PENDING FOUNDER VETO per
  001_introduction/AGENTS.md).

## Pre-judge mandatory self-checks (all on render_3.png)

1. Patterns index read — house-chrome pattern used via import; no other pattern applies
   (no equations/tables/delimiters/highlight-text-fit situations).
2. FRAME CONTAINMENT (PIL): 0 ink px between box borders and interior gap; 0 red px above
   the chrome top border; 0 dark px in the empty right region. PASS.
3. EQUATIONS EXIST: N/A (no equations on this slide).
4. DELIMITER GEOMETRY: N/A.
5. TABLE DATA: N/A.
6. ZOOMED CROP VISION: N/A (mandatory only for equations/multi-line delimiters/tables).
7. LINE/BOX WRAP: exact band counts (3 header bands, 11 bullet bands, 11 dot clusters);
   no ink outside intended bands. PASS.
8. EXPLICIT LINE SPACING: lineSpacing set on every text box (title 47, headers 24,
   bullets 24); all boxes single-line except the title (2 lines, pitch measured 47.4 vs
   original 47). PASS.
- house_chrome_check.py: PASS (panel x 89-1913, y 95-bottom; badge center (1860,148) d=70;
  tol 8).

## Evidence banked (qa/slide008/, never delete)

measure_original.py, measure_original2.py, measure_original3.py, measure_original4.py,
render_1.png, render_2.png, render_3.png, build_attempt_1.js, build_attempt_2.js,
build_attempt_3.js, selfcheck_attempt_1.py + output, selfcheck_attempt_2.py + output,
selfcheck_attempt_3.py + output, judge_prompt_3.txt, judge_prompt_4.txt, judge_p_payload.txt,
probe_3.txt, judge_attempt_3.txt (misfire), judge_attempt_4.txt (misfire),
judge_attempt_5.txt (CERTIFYING), this report.
