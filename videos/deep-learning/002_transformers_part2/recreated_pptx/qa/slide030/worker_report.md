# Slide 030 worker report — rotation-matrix derivation slide (RESUMED run)

## Outcome

**PASS** on judge attempt 1 (single-read, default route `images`, glm leg
DEFERRED/BLOCKED). DB: `gen_status=passed`, `visual_check=PASS`,
`visual_attempts=1`, `visual_transcript=judge_attempt_1.txt`.

- Deliverable: `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_030_recreated.pptx`
- Build: `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_030.js`
- Certified render: `qa/slide030/render_4.png` (150 dpi, 2001x1125)
- Judge transcript: `qa/slide030/judge_attempt_1.txt` (real comparison winner body)
- Judge prompt banked: `qa/slide030/judge_prompt_1.txt` (+ frozen `-p` template in
  `judge_template.txt`); per-attempt build snapshot `build_attempt_1.js`.

## Resume provenance

Resumed after the previous builder died in a provider storm post-build, after 6
pre-judge self-check iterations (`selfcheck_attempt_1..6`), 0 judge attempts.
Attempt 6 had exactly one closed-loop FAIL: `independ` dR=-4.6 (tol 3.0) — the
"Independent of Position t" label rendered ~1.15% narrower than the original.

## Fixes applied this run (pre-judge render iterations; judge attempts unaffected)

1. `independ` font size 20.1 -> 20.3 pt (em 19.23 -> 19.40): closes dR to +1.4
   (`selfcheck_attempt_7`, TOTAL FAILS 0, render_2).
2. **Crop-comparison BLOCKER (mid region, attempt c1):** the derivation-line-2
   minus (and matrix r2c1 minus), drawn as 4x3 frame-px rects, rendered as
   10x9 px blocks — the judge read them as solid squares (`▪`) corrupting
   `cos(ωt) − sin(ωt)`. Original ink is a 4x2 frame-px soft bar. Fix: rect
   height pinned to the inked rows, then to 1 frame px (`hl(...,303,303)` /
   `hl(...,411,411)`) because LibreOffice snaps shape rects UP ~2 px —
   luminance-profile verified: 3-row dark core + AA skirts, matching the
   original's rescaled profile (`render_4`, selfcheck_attempt_9 TOTAL FAILS 0).

## Pre-judge gates (all fresh, final = render_4)

- `house_chrome_check.py`: PASS (panel x 89-1913, badge (1860,148) d=70).
- Closed-loop PIL self-check `selfcheck_attempt_9.py`: TOTAL FAILS 0
  (44 equation segments, brace, 10 text elements, underline, 2 minus rects,
  5 bracket stems, frame containment, 6 fill/color samples).
- Mandatory zoomed crop vision analysis (item 6), through the vision gate with
  the frozen judge template, matched-scale crop pairs (`crops/`):
  - `cropcmp_top_c1.txt` — top region (vecbox + Remember): **PASS** (2 MINOR;
    region pixel-unchanged render_2 -> render_4, verdict stands).
  - `cropcmp_mid_c1.txt` — derivation region, render_2: **FAIL** (minus glyph
    BLOCKER) -> fixed -> `cropcmp_mid_c2.txt` (render_4): **PASS** (3 MINOR).
  - `cropcmp_bottom_c1.txt` — matrix + note + captions + brace: **PASS**
    (2 MINOR, both rule-(d) medium differences).
- Highlight-color claims cross-checked by PIL census of the ORIGINAL's
  marker-only pixels (G>140 median): L1 cos(ωδ)=(129,197,137) GREEN, L1 final
  sin=(235,255,135) YELLOW, L2 cos(ωδ)=(232,253,135) YELLOW, L2 final
  sin=(128,196,139) GREEN — the build's assignments are correct; the crop
  judges' "khaki/pale green" impressions are JPEG marker-softness artifacts.

## Judge attempt 1 (render_4)

Verdict body: element-by-element fidelity confirmed (all text verbatim,
highlight assignments "match exactly", delimiters span content, containment
satisfied, cursor artifact correctly omitted, no missing elements).
Findings — all MINOR, none fix triggers:
- D1/D2: tight left-bracket-to-"Sin" clearance in v2 vector and matrix left
  vector — judge notes the original is comparably tight (reproduces source).
- D3: Remember-box `=`/`+` spacing slightly looser than original (text verbatim;
  mathtext spacing vs typed spacing, rule-(d) family).
- D4: brace curvature simpler than the original's hand-drawn curly brace
  (same position/extent/label; certified slide-020 raster-brace mechanism).

## Probe/storm notes

- Probe on render_2 landed a valid body (window open); probes on render_4 hung
  twice (150 s wrapper, exit 124) with the fleet landing comparisons — per the
  dispatch law the judge comparison was dispatched directly at the W4 wall
  (timeout 540 / --timeout 420 / --thinking high / --max-tokens 65536) and
  landed first try.

## Component banking

Slide 30 is a ROOT slide with no dependents in `slide_dependencies.json` (no
in-video children, no cross-video refs, not in any pattern group) — no
component-banking obligation.

## Post-certification

**OMML v2 dual-representation wrap: APPLIED (this run).**

- Manifest: `qa/slide030/eq_030_omml_manifest.json` — 38 placed mathtext
  equations (all eq() images except `brace` = PIL-drawn raster under the
  certified slide-020 mechanism, and `m_minus`/`d2_s8` whose PNGs are
  unplaced — those minuses are the rect-drawn bars). Values (`mathtext`,
  `font_size_pt`, `color`) from the build-side `eq_030_manifest.json`
  (gen_eqs.py sidecar data); rel ids re-derived by the wrapper from the
  CURRENT pptx (rId1..rId38).
- One representation-level substitution, documented: `\mathit{sin}`/`\mathit{cos}`
  -> bare `sin`/`cos` in the two Remember identities (rm_id1/rm_id2) — the
  wrapper's converter does not support `\mathit`, and in mathtext a bare
  multi-letter run renders as the same italic letters the PNG shows. The PNGs
  (the certified pixels) are untouched.
- Wrapper run: `python3 scripts/18_omml_wrapper.py <pptx> <manifest> -o
  scratch/slide030/omml/...pptx` -> wrapped=38 skipped=0, exit 0; result moved
  over `recreated_pptx/slide_030_recreated.pptx` (single-version law: the
  deliverable IS the wrapped file; no `_omml` parallel version).
- Pixel-identity gate (mandatory): LibreOffice render of the wrapped pptx vs
  the certified render_4 = **0 of 2,251,225 pixels differ**. Banked as
  `qa/slide030/render_final_omml.png`. No re-judge (contract: the pass does
  not change pixels).
- Structure check: 38 mc:AlternateContent blocks (76 tag hits), 38 mc:Fallback
  pics, zip integrity OK. Never LO-resave this file from here on.
