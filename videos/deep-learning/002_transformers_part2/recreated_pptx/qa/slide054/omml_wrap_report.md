# Slide 054 OMML v2 wrap record (002_transformers_part2)

**Status: WRAPPED OK — LO render of the wrapped file pixel-identical to the certified
render (0 of 2,251,125 px differ).** Applied 2026-10-12 (OMML wrap pass, resumed run).
DB certification fields untouched.

- Deliverable: `recreated_pptx/slide_054_recreated.pptx` — single-version law: this file
  IS the wrapped deck now (no `_omml` suffix; never LO-resave it).
- Manifest: `recreated_pptx/qa/slide054/eq_054_omml_manifest.json`
- Certified render (comparison base): `qa/slide054/render_7.png` (judge PASS attempt 7)
- Post-wrap render (0-diff): `qa/slide054/render_final_omml.png`

## What was wrapped

| rel_id | asset | mathtext | fs (pt) | color |
|---|---|---|---|---|
| rId1 | eq_Kcdotq_over_sqrtd.png | `\dfrac{K\cdot q}{\sqrt{d}}` | 12.0 | #C00000 |

- Manifest values re-derived from the CURRENT pptx (rIds inventoried from
  `ppt/slides/slide1.xml` + rels; rId1 = the fraction pic; rId2/rId3 = bezier
  connector art `conn_left/conn_right.png` — not equations, left unwrapped).
- Provenance proof: re-rendered `\dfrac{K\cdot q}{\sqrt{d}}` @12.0pt #C00000 with the
  certified renderer (`scripts/render_eq.py`) — **byte-exact (PIL 0-diff)** vs the
  banked `build/assets/eq_Kcdotq_over_sqrtd.png`. (The earlier provenance attempt used
  `\frac` — display-style `\dfrac` is what generated the asset; hit found at fs 12.0.)
- Wrapper: `python3 scripts/18_omml_wrapper.py <pptx> <manifest> -o
  scratch/slide054/omml/slide_054_recreated_omml.pptx` → wrapped=1 skipped=0, exit 0.

## Verification gates (all PASS)

1. Baseline pre-flight: LO render of the UNWRAPPED certified pptx vs
   `qa/slide054/render_7.png` = **0 of 2,251,125 px differ** (pipeline faithful).
2. LO render of the WRAPPED pptx vs certified render = **0 of 2,251,125 px differ**
   (the mc:Fallback pic serves the identical pixels to LibreOffice).
3. Idempotence: wrapper re-run on the wrapped file → `wrapped=0 skipped=1`, exit 0.
4. Base-md5: every zip entry byte-identical between input and wrapped output except
   `ppt/slides/slide1.xml` (the only touched part; no rels/content-types/media).
5. Structure: 1 `mc:AlternateContent` (a14 Choice with `m:oMathPara(jc=centerGroup)`
   Cambria-Math pattern + verbatim `<p:pic>` Fallback).

Working evidence (rerender/scan/baseline PNGs): `scratch/slide054/omml/` +
`scratch/omml_wrap/`. LO render route: `scratch/omml_wrap/render_omml.sh`
(short-home-path PDF workaround; never LO-resave the wrapped deliverable).
