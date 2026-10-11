# Worker report — slide 037 "Self Attention Mechanism (Adding Scaling)"

Deep Learning DSAI 308, lecture `001_transformers_part1`. Built 2026-10-11 by the
per-slide build worker. **Final verdict: PASS (attempt 1)** — real comparison winner
body, no blockers.

## Deliverables

- PPTX (single-version law): `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_037_recreated.pptx`
- Build script: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_037.js`
- **Shared component (for child 38):**
  `videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_037.js`
  — exports `renderBase(pptx, slide, opts)` at BLOCK granularity:
  `canvas, title, pills, leftGroup, rightGroup, dotProduct, scaling, softmax, rowLines,
  sigma, multiply, output, strip, legend` with `opts.skip` / `opts.only` selectors.
  House chrome is NOT drawn inside the component; children call
  `components/house_chrome.js` (`drawHouseChrome`, numeral 38) themselves and compose
  their delta (green-bordered MatMul→SoftMax→Mask(opt.)→Scale→MatMul inset) on top.
- Equation assets (mathtext → 600 dpi transparent PNG, exact-size addImage):
  `build/assets/eq_Kq_037.png` (K.q label), `eq_Kq_num_037.png` + `eq_Sqrtd_037.png`
  (composed stacked fraction + drawn bar — chosen over the single-PNG `\dfrac` after
  closed-loop iteration), `eq_1xd_037.png` ×2, `eq_dxd_037.png`; superseded single-PNG
  fraction banked as `eq_KqoverSqrtd_037.png`.

## Process

1. Dependency gate: `15_progress.py deps` → slide 37 `root` (child 38 waits on it).
   Build allowed. After PASS, 38 shows `unblocked`.
2. Spec: `analysis/slide_037_final.json` (PASS_WITH_FIXES, score 9) + `slide_037_source/SOURCES.md`
   (eq. (1) order confirmed; course notation kept verbatim; K.q with period kept per raw).
3. Geometry: PIL color-region/ink-cluster forensics on `unique_slides/slide_037.jpg`
   (960×540) + 9 vision crop reads through the gate (banked `scratch/slide037/v_*.txt`).
   Key frame facts locked: 4 pipeline rows y=246/287/328/371; row 1 = X₄→W_k→K₄
   (resolves the spec's [?] row ordering); W_k boxes green-bordered, W_v boxes NAVY-bordered
   (measured — differs from the spec's "medium-green" for W_v); K/V vector stacks + labels
   float above the row lines; fraction bar at y206; legend overhangs the canvas bottom-right
   exactly as the original; the original's legend reads [1×d]·W(d×d)=[1×d] (three labels:
   1×d below block 1, d×d below-right of W, 1×d below-right of block 2 — vision-read at 4×).
4. Pre-judge self-checks (banked `qa/slide037/selfcheck_attempt_1.txt`, all PASS):
   - `house_chrome_check.py`: PASS (playlist chrome, NOT the ml-intro values).
   - Containment: 0 ink px outside the chrome panel.
   - Equation closed loop vs original ink bands (tol 4 px frame): fraction numerator
     dx 1.8, bar+denominator dx 1.1 / dy 2.9, K.q label dx 1.3, legend labels ≤3.3.
   - 18 structure regions compared (pills, boxes, stacks, strip, legend, containers):
     all ≤4 px except three documented row-line mask artifacts (≤6 px, ink-threshold
     sensitivity of the washed JPEG, geometry verified at 1–2 px).
   - Dense-region crop comparisons through the gate (4 pairs, banked `cropcmp_*.txt`):
     legend PASS; frac/row1/q2path FAILs drove real fixes (inner rect lighter fill
     FFF069, arrows 1.25→1.1pt, K-stack cells yellow/yellow/lavender/lavender, legend
     2nd label moved to its true position (877,501)) — all applied and re-verified.
5. Judge (attempt 1): probe (`probe_1.txt`, healthy full-slide read) + comparison with the
   frozen `-p` template, `--thinking high --max-tokens 65536`, W4 wall
   (`judge_attempt_1.txt`). **FINAL VERDICT: PASS**, no blockers. Banked evidence:
   `judge_prompt_1.txt`, `build_attempt_1.js`, `component_attempt_1.js`, `render_1.png`.

## Judge MINORs (accepted, none are fix triggers)

1. ⊗ rendered circle-X vs the original's circle-asterisk/star glyph (same role/placement;
   the spec itself says ⊗ circled-X; the two vision reads of the original disagree).
2. The original's extremely faint green dashed curves from the strip to the groups are
   attenuated to short dashed stubs at the measured positions (the curves are sub-visible
   in the frame; terminals represented).
3. Σ glyph slightly heavier than the original's.
4. Y₂ box slightly larger than the original's.

## Superscript "(1)" vs "(r)" — resolved, kept "(1)"

The 3× crop comparisons read the original's W-superscript as "(r)"; the raw
transcription of record and `SOURCES.md` (double-confirmed 2026-10-11) say "(1)"; an
8× tiebreaker crop (`zoom_wk_sup.txt`) reads it as illegible ("(r) or (n)"). Per the
fidelity law the spec of record stands: the build renders "W_k^(1)" / "W_v^(1)" /
"W_q^(1)" (true sub/superscript runs). The full-slide judge did NOT flag it (probe read
"the '(1)' … legible"). Documented here as the resolution of record.

## Notes

- No OMML wrap: this deck's certified slides (002/003/024 …) carry no
  `mc:AlternateContent` (PNG-only equation mechanism per the dispatch contract).
- The original's mouse-cursor artifact (subtitle area) and the unbalanced-parentheses
  subtitle typo are handled per ground rules (cursor omitted; typo kept verbatim).
- Judge procedure executed by the worker (no subagent spawn tool in this environment;
  orchestrator-approved fallback per 17 §7). One transient gate-wrapper anomaly was
  worked around by direct `analyze_image.py` invocation (probe); the judged comparison
  itself ran through the gate wrapper.
