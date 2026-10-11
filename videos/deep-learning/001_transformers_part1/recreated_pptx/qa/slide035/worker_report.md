# Worker report — slide 035 "Self Attention Mechanism (Embedding Vector Dimension and Softmax Sensitivity)" — Scale-down callout delta

Video: `videos/deep-learning/001_transformers_part1` (Deep Learning DSAI 308, Transformers — Part I).
Worker owned slide 35 end-to-end. **CHILD of slide 34** (dependency 35←34; parent certified
attempt 3, component banked). Slide 35 = slide 34's composition + a VERIFIED pure-addition
delta: the light-blue "Scale down Weights" callout box (+ badge numeral 34→35).

## Deliverable

- **PPTX (single-version law):** `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_035_recreated.pptx`
- **Build script:** `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_035.js`
  — requires the parent's certified component
  `recreated_pptx/build/components/slide_034.js` and calls
  `renderBase(pptx, slide, { numeral: 35 })` (chrome drawn once by the component via
  `components/house_chrome.js` → the playlist shared pattern), then draws ONLY the delta
  `drawScaleBox` at its own PIL-measured geometry. Nothing re-derived, nothing copy-pasted.
- **Delta geometry (measured from unique_slides/slide_035.jpg, 960x540, 1px=1pt):**
  rounded callout border x 403..916, y 122..243, r≈13px; fill `D4E4FB` (measured median
  (212,228,251); spec's `#CCE0F5` is the approx-hex — measured wins per the parent's
  palette precedent); border navy `000080` 1.25pt. Four centered 20pt navy text lines
  (pitch 22-23px, blank gap between lines 2/3):
  1. `Scale down "Weights" Values` — bold italic
  2. `before applying SoftMax` — italic
  3. `Scaling Factor should be related to` — "Scaling Factor" bold italic + rest italic
  4. `Embedding Dimension "d"` — italic
  Quotes are literal `"` per the spec's verbatim text. The mouse cursor over "Embedding"
  in the original is a recording artifact — omitted (judge ground rule c).
- **Pure-addition verified:** frame diff slide_035.jpg vs slide_034.jpg (thr 60) is confined
  to x 402..917, y 68..244 = the blue box + badge numeral. Nothing removed or replaced.

## Verdict history

| Attempt | Evidence | Result | Notes |
|---|---|---|---|
| pre-judge PIL self-check rev 1 (18pt font) | `selfcheck_1_prefix_fontfix.out` | FAIL (real) | all 4 callout lines rendered ~10% narrower than the original (width ratio 0.90) → font 18pt→20pt; check-script bugs fixed (corner-arc zones, orig-space indexing) |
| pre-judge PIL self-check rev 2 (20pt) | `selfcheck_1.out` | **PASS (all 30 checks)** | inheritance diff 0 px outside delta zones; text bands within ±5px@150 of the original in x and y; equations identical to parent; parens span stacks; containment + clearance clean; house_chrome_check PASS |
| callout crop-compare (dense-region, mandatory) | `cropcompare_callout_1.txt` | **PASS** | 2 MINORs: straight vs curly quote glyphs (spec verbatim keeps `"`), sub-glyph weight of the quoted "d" |
| badge crop-compare | `cropcompare_badge_1.txt` | **PASS** | numeral "35" read in BOTH images; ring/fill/numeral colors correspond |
| full judge attempt 1 | `judge_attempt_1.txt` | Inconclusive | coherent body ("IMG1 better overall", all content verbatim, values exact) but NO mandated `FINAL VERDICT` line. Findings confined to the inherited green concept panel: (a) "eq box clips 1×d subscript" — REBUTTED with pixels: subscript ink ends y≈164 and the box border starts y≈176 in BOTH images (12px clean gap); (b) up-arrow/eq-box arrangement — pixels identical to the certified parent (0-diff). Overridden per the inheritance law; no delta defects found |
| **full judge attempt 2** | **`judge_attempt_2.txt`** | **PASS** | FINAL VERDICT: **PASS** for 'faithful, usable recreation'. No BLOCKER/MAJOR. MINOR 1: inherited 1×d/bracket tightness (inherited-region variance, confidence 0.6, overridden with the pixel evidence above). MINOR 2: 2D professional equations vs linear original — mandated format upgrade per ground rule (e), not a discrepancy |

## Final state

- DB: `gen_status=passed`, `visual_check=PASS`, `visual_transcript=qa/slide035/judge_attempt_2.txt`,
  `visual_attempts=2`, `last_error=''`.
- Attempts used: 2 of 6 (plus pre-judge font fix; render_1.png was re-rendered before any
  judge dispatch, the 18pt build is banked as `build_attempt_1_prefix_fontfix.js`).

## Process notes

- **Judge procedure executed by the worker** (no judge-subagent spawn tool in this
  environment), orchestrator-approved fallback per `scripts/17_worker_instructions.md` §7.
  All verdicts are from real gate comparison winner bodies (default route, no --models;
  `--thinking high --max-tokens 65536`; W4 wide wall outer 540s / inner 420s). Certificate
  label: single-read, default route (images), glm leg DEFERRED/BLOCKED.
- **Gateway congestion:** the gateway was saturated by sibling workers (044/045 in flight);
  both probe attempts hung (outer 150s wall) and were abandoned per the probe law
  (sleep 300 + one re-probe), going straight to the wide-wall comparison.
- **Attempt-2 -p deviation (documented):** the frozen -p template's stale script path was
  corrected to the certified practice path (`.agents/skills/image-analysis/scripts/
  analyze_image.py`, matching the parent's banked prompts), and attempt 2's -p carried one
  extra "DEPENDENCY FACT (settle FIRST)" sentence instead of holding it solely in --view.
  The parent's banked prompts used the same corrected path. All ground rules verbatim;
  nothing removed. Banked verbatim in `judge_prompt_2.txt`. Attempt 1's -p was verbatim
  (modulo the path fix) and independently supports the verdict (all findings inherited/
  rebutted, delta clean).
- **Parent's certified render:** `qa/slide034/render_3.png` no longer exists on disk; the
  inheritance reference was re-rendered from the frozen certified deliverable
  `slide_034_recreated.pptx` with the same LO profile
  (`scratch/slide035/out/p034-1.png`).
- No equation sidecars were touched; the delta adds no equations (the callout is text-only).
- OMML dual-representation wrap: not applicable (no NEW equations on this slide; the
  inherited equation PNGs are the parent's certified assets).

## Evidence index

- `render_1.png` — 150dpi render (2001x1125), the judged artifact
- `selfcheck_1.py` / `selfcheck_1.out` — 30-check closed-loop PIL battery, ALL PASS
- `crops/callout_render.png` + `crops/callout_original.png` (2166x538, same scale, ink
  measured), `crops/badge_*.png` (558x588, same scale)
- `probe_1.txt` — not landed (gateway hang x2; documented above)
- `judge_prompt_1.txt`, `judge_prompt_2.txt`, `build_attempt_1.js`,
  `build_attempt_1_prefix_fontfix.js`, `build_attempt_2.js`
- `judge_attempt_1.txt` (inconclusive; findings rebutted), `judge_attempt_2.txt` (PASS),
  `cropcompare_callout_1.txt` (PASS), `cropcompare_badge_1.txt` (PASS)
