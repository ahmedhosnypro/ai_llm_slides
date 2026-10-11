# Worker report — slide 007 "Traditional RNN  Seq2Seq model / (Challenges) — [1] Bottleneck"

Video: `videos/deep-learning/001_transformers_part1` · Worker: per-slide build worker (subagent)
Date: 2026-10-11 · FINAL VERDICT: **PASS** (judge attempt 1, real comparison transcript)

## Deliverable

- `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_007_recreated.pptx`
  (SINGLE-VERSION law — one plain-named pptx, no suffixes; no equations → no OMML pass;
  no advanced graphs → no graphgen pass)
- Build script: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_007.js`
- **DEPENDENCY-GATED CHILD BUILD (edge 7 ← 6):** the base (playlist chrome + all 27
  blocks) is drawn EXCLUSIVELY by the certified parent component
  `recreated_pptx/build/components/slide_006.js` via `renderBase(pres, slide, {numeral: 7})`
  — required, never re-derived or copy-pasted. The script draws ONLY slide 7's delta.
- **Component export:** slide 7 has NO dependents in `slide_dependencies.json`
  (nothing lists 7 as a parent), so per 17 §2 no `components/slide_007.js` is required.
  Children of 6 (slides 8, 9, 10) import slide_006.js directly, as this build did.

## Delta (all PIL-measured from `unique_slides/slide_007.jpg`, 960×540, 1px=1pt)

Measurers banked in `scratch/slide007/` (diff_006_007.py + measure_*.py, 5 passes).

1. **Pure-superset verification** (diff_006_007.py): pixel diff vs slide_006.jpg shows
   exactly two bands — the title/badge band and the callout band; no removals. The
   title-band diff is a ≤7px video-capture jitter of the IDENTICAL title string
   (best vertical shift dy=0, overlap 99%) + the badge numeral 6→7 (chrome). The
   inherited composition is therefore drawn by the certified component untouched.
2. **Title line 2 "(Challenges)"** — Arial bold 27pt `000066`, centered in the same
   title box (x252.5 w400), y81 h30 (ink y181..233 render vs frame 181..231 target;
   width 331 vs 329 target render px). Size calibrated against the LO render
   (20pt→245 px, linear → 27pt; matches ink width AND paren-span height).
3. **Bottleneck callout** — roundRect x44 y170 w412 h98 (px), rectRadius 0.03
   (corners measured ~1-2px), fill `DFFFFC` (mode 223,255,252), border `ABB8CB` 1pt
   (edge mean ~(171,184,203)). Four centered lines, Arial bold `000066`, explicit
   `lineSpacing: 18` (measured pitch 18px), per-line sizes calibrated on the LO render:
   L1 "[1] Bottleneck" 17.5pt (frame draws it ~13% larger than the body lines),
   L2–L4 15.5pt; render ink widths [240,679,785,391] vs frame targets
   [242,680,790,396] — all within 1.3%. Underlines (run-level, `u="sng"` verified in
   the XML and in the render): L1 full line, L2 none, L3 tail "by a single context
   vector", L4 tail "fixed  dimensionality". Verbatim double spaces kept
   ("sequence  is", "captured  by", "fixed  dimensionality").
   The white mouse cursor over the box right-center (measured x365..372 y243..248)
   is a video artifact — omitted.
4. **Leader connector** — 1pt line (463,188)→(477,279) px: traced on the frame; top
   end floats ~7px right of the box border (measured, reproduced), lower end meets
   the red ctx-arc ink. Color `A8AABC` (measured stroke samples
   ~(167..180,166..180,182..196), 1px AA-diluted gray-blue).

## Pre-judge self-checks (attempt 1 — ALL PASS, banked)

- `house_chrome_check.py` → PASS (panel x 89-1913, badge center (1860,148) d=70, tol 8)
  — `qa/slide007/house_chrome_check_1.txt`
- `qa/slide007/selfcheck_attempt_1.py` + `_out.txt` → ALL PASS:
  - **A1 inheritance**: render-vs-certified-parent-render diff bands confined to
    {badge numeral, subtitle, callout+connector} — every inherited pixel identical
    to the certified parent (the child law's closed-loop form).
  - **B subtitle**: present, w=331 (target 329), cx=942 (947), cy=207 (206).
  - **C box**: fill sample exactly (223,255,252); 4 border strokes on mid row/col.
  - **D lines**: 4 bands, centers 402/440/478/516 (targets 399/438/475/514), pitch
    38.2 (target 37.5), ink widths within 1.3%, underline rows at 415/491/528 with
    correct spans, L2 underline-free.
  - **E containment**: zero non-chrome ink beyond box borders; box inside house frame.
  - **F connector**: 12/12 ink samples along the traced path.
  - **G ink color**: median (0,0,102) = spec `000066`.
- **Dense-region crop comparisons** (pattern `dense-region-crop-compare`, full judge
  params, frozen template verbatim, both crops pixel-measured first):
  - `cropcmp_callout.txt` → **PASS**. Findings: MINOR "original looks bold-italic"
    (rebutted: validated spec typography_notes says bold sans-serif, no italic — same
    disposition as the parent's judge finding #3; spec stands) and MINOR "recreation
    text marginally wider" (rebutted with numbers: render ink widths are within 1.3%
    of frame targets, marginally NARROWER, not wider).
  - `cropcmp_titlesub.txt` → **PASS**, zero discrepancies; the judge confirmed the
    slight right-offset of "(Challenges)" exists in BOTH images (faithful).

## Judge (attempt 1)

- Banked prompt: `qa/slide007/judge_prompt_1.txt` (frozen -p template verbatim;
  shared-base fact + cursor-artifact note in the worker-editable --view).
- Probe: window open (crop comparisons had just used it; probe run RC=0, short-body
  warn only — not a hang).
- Comparison: `qa/slide007/judge_attempt_1.txt` → **FINAL VERDICT: PASS**.
  Findings (all MINOR) and dispositions:
  1. Decoder s₂/s₃ hooks: "curved in original, straight ticks in recreation" —
     INHERITED block (`dec_feedback`); identical pixels to the certified parent
     render (self-check A1); the parent's own judge dispositioned the same feature
     as variance (parent report finding #2/#6: both features present, 1px strokes).
     Override per dependency law — documented, not a fix trigger.
  2. Feedback arcs "slightly thicker/olive" — INHERITED (`dec_feedback` curve assets +
     `decInk`); certified parent pixels. Same override.
  3. Connector tint "slightly lighter/bluer" — MY DELTA; measured rebuttal: the
     frame's stroke samples are gray-blue (167..180, 166..180, 182..196); my
     `A8AABC` sits inside that range; 1px-stroke tint at judge zoom is unreliable.
     MINOR, low confidence — not a fix trigger.
  4. Decoder cell-group proportions "differ by a few pixels" — INHERITED
     (`DECBAR` geometry, certified; parent's judge finding #5 identical eyeball note).
     Override.
- No BLOCKER/MAJOR findings on the delta or the base. Verdict: PASS.

## DB state (final)

gen_status=passed · visual_check=PASS · visual_attempts=1 ·
visual_transcript=videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide007/judge_attempt_1.txt ·
pptx_path / build_script set · last_error=null

## Notes for the orchestrator

- First CHILD build of the dependency program: pattern = `require('./components/slide_NNN')`
  → `renderBase(pres, slide, {numeral: N})` → draw delta at own PIL-measured geometry →
  self-check inheritance diff vs the parent's certified render confined to delta zones.
- Judge procedure executed by the worker via Bash (no Agent/Task spawn tool in this
  environment) — orchestrator-approved fallback, noted per 17 §7.
- Slides 8, 9, 10 (also children of 6) remain unblocked and can reuse this exact pattern.
- /tmp quota workaround honored: all scratch (LO profile, renders, gate locks) under
  `videos/deep-learning/001_transformers_part1/scratch/slide007/` with TMPDIR override.

## Evidence files (qa/slide007/)

render_1.png · build_attempt_1.js · judge_prompt_1.txt · judge_template_clean.txt ·
selfcheck_attempt_1.py + _out.txt · house_chrome_check_1.txt · crops/ (4 PNGs + prep
measurements in prep_crops.py) · cropcmp_callout.txt · cropcmp_titlesub.txt ·
probe (RC=0; short-body, no transcript banked — window verified by the two crop
comparisons immediately prior) · judge_attempt_1.txt (certifying comparison).
