# Worker report — slide 028 "Self Attention Mechanism (Not Sensitive to Words Order)"

VIDEO: deep-learning/001_transformers_part1 · N=28, NNN=028 · child of 26 (edge 28←26,
parent certified attempt 1). Worker: per-slide BUILD WORKER, 2026-10-11.
FINAL VERDICT: **PASS** (attempt 3, real comparison transcript).
Deliverable (SINGLE-VERSION law): `recreated_pptx/slide_028_recreated.pptx`
Build: `recreated_pptx/build/slide_028.js` (pptxgenjs, run from project root,
NODE_PATH=$(npm root -g)).

## Dependency-gate compliance

- `15_progress.py deps` at start: slide 28 **unblocked** (parent 26 = passed + PASS).
- Base imported from the CERTIFIED component `recreated_pptx/build/components/slide_026.js`
  via `renderBase()` — never re-derived. Two opts-gated passes preserve the certified
  z-order around the replaced strip block (`skip:["title","strip","queryArrows","feedCurves"]`
  → my strip → `only:["queryArrows","feedCurves"]`), then the new boxes, then my title.
- House chrome drawn ONCE via `components/house_chrome.js` (`drawHouseChrome`, numeral 28).
- Certified component NOT edited (cascade law) — all deltas live in the child build.
- Slide 28 has NO dependents in the graph → no component export required.

## Delta (PIL pixel forensics on unique_slides/slide_028.jpg; frame-diff vs slide_026.jpg)

1. Title L1: parenthetical → "(Not Sensitive to Words Order)" (yellow highlight x481..775,
   ink x233..772 — same certified box/size, ink center 502.5 identical to parent's).
2. Subtitle: word order shuffles to **X4, X2, X1, X3** (verbatim frame content, unbalanced
   parens kept; ink band pixel-identical to parent's — only digits swap).
3. Bottom token row labels shuffle to **X4, X2(highlighted), X1, X3** — strip block
   replaced with pixel-identical geometry (frame-diff: only the 3 digit glyphs + the old
   cursor spot differ). VISION-CONFIRMED by crop A: "Label order left→right is X4, X2, X1,
   X3 in both images — the shuffled order matches."
4. NEW box "Sequential nature of the input is IGNORED": roundRect x382..719 y426..460,
   WHITE fill, dashed green 3B7A40 border, green 2A842A **bold italic** 15.5pt.
5. NEW box "Mitigated Later with / Positional Encoder": roundRect x725..896 y459..523.5,
   **mint E6FCE7** fill, dashed green border; line 1 red 9E101E bold, line 2 blue 0033CC
   bold italic; lineSpacing 18 (measured pitch), 16.5pt (render-calibrated).
6. 8 red diamond marks in the Dot Product box (4 ON the flow lines left of the dots +
   4 below the dots — the visible ink of the spec's "thin red fan lines … reach each
   dot"; fine-scan measured centers/sizes in build/slide_028.js block 4b).

NOT part of the delta (pixel-identical to the parent, cross-correlation 0.94–1.0 diagonal):
the left/right stack labels read X1..X4 top-to-bottom in BOTH frames — the analysis JSON's
"X4..X1 top-to-bottom" stack claim contradicts the frame; **the frame is ground truth**
(inherited untouched). Mouse cursor (near W23 in this frame) = video artifact, omitted.

## Attempts

| K | Render | Result |
|---|--------|--------|
| 1 | render_1.png | chrome check PASS; selfcheck ALL PASS after fixing check bugs (green-mask caught box border; parent-reference baselines introduced). Probe ×2 hung (gateway saturated); crop A landed: label shuffle CONFIRMED; its X2-label finding shown pixel-identical to certified parent → variance. |
| 2 | render_2.png | Fixes: box1 italic + box2 mint fill (crop B findings; PIL corroboration: box2 lower-interior median (231,253,232) = container fill; box1 (252,255,252) = white). Crop B2: "IMG1 … better overall — Mint fix confirmed … Italic fix confirmed." **Judge: FAIL** — F1 missing fan-mark ink in Dot Product box [REAL: frame has 8 red diamond marks, both renders omit; P-vs-R diff 0 → adopted as child delta]; F2 box2 crosses panel edge [FALSE: original breaches identically — canvas edge x866, box2 to x896 in BOTH frame and render; the "peach" the judge saw was red-text anti-aliasing]; F3 ⊗/⊛ MINOR [inherited, frame-identical]. |
| 3 | render_3.png | Added delta (f) diamonds. chrome PASS; selfcheck ALL PASS (incl. 8/8 diamonds). **Judge: FINAL VERDICT: PASS.** |

## Attempt-3 judge dispositions (PASS + residual notes)

- Item 1 (MAJOR, ~60%): block arrow under X2 "crosses the bottom edge of the inner beige
  panel … unlike IMG2" — **FALSIFIED**: the arrow is the certified parent's measured
  geometry (266,526)→(284,512), ink below the canvas bottom (~523) IN THE ORIGINAL;
  frame-diff 026↔028 = 0 and P-vs-R diff = 0 there. Nudging would break fidelity. Overridden.
- Item 2 (MINOR): fan-line shafts vs diamonds — shafts are invisible in the frame pixels;
  the diamonds ARE the measured ink. Documented.
- Items 3–4 (MINOR): row-4 line stop (x688, measured) and arrow angle — inherited
  certified geometry, P-vs-R identical → variance. Documented.

## Mandatory pre-judge self-checks (banked)

- `shared_patterns/house_chrome_check.py`: PASS on every render (1–3).
- `selfcheck_attempt_3.py` (+ outputs for 1/2/3): house containment vs certified parent
  (x86..1915 y93..1124 — identical), title L1 ink/width (+0.1%), highlight, subtitle red
  band, box1 white fill + text cal (647 vs 652 = −0.8%), box2 L1/L2 cal (−1.2%/−0.6%),
  line pitch 37.6 vs 37.5, text containment, strip X2 cells (0.71 vs 0.67) + sysDot
  border, box2 occludes feed curve, **8/8 Dot-Product diamonds present**.
- Zoomed crop comparisons (gate, transcripts banked): crop A (strip labels), crop B
  (attempt 1 boxes), crop B2 (attempt 2 boxes).

## Evidence paths (qa/slide028/)

- Transcripts: judge_attempt_2.txt (FAIL), judge_attempt_3.txt (PASS),
  crop_compare_A.txt, crop_compare_B.txt, crop_compare_B2.txt
- Prompts: judge_prompt_1/2/3.txt (+ judge_p_template.txt = the frozen −p block)
- Builds: build_attempt_1/2/3.js; renders render_1/2/3.png
- Self-checks: selfcheck_attempt_1/2/3.py + _output.txt
- Note: judge procedure executed by the worker (no spawn tool in this environment) —
  documented fallback per 17 §7. Certificate label: single-read, default route (images),
  glm leg DEFERRED/BLOCKED. Two initial probes hung on a saturated gateway; crop A's
  success opened the window; comparisons ran under W4 wide walls.

## Slide-28-specific finding for the skill memory (inherited-gap class)

A certified parent's render can carry a fidelity gap its own judge missed (here: the 8
Dot-Product diamond marks). The child's frame is ground truth for EVERY element — when the
child's judge + spec + pixel forensics agree on inherited missing ink, fix it in the CHILD
delta (component stays frozen). Cross-check tooling that paid off: full-slide P-vs-R diff
(inherited regions must be pixel-identical), digit cross-correlation between frames
(stack labels), and color matching against on-frame certified references (green=2A842A,
blue=0033CC, red=9E101E).
