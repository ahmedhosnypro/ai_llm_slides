# Slide 040 OMML v2 wrap record (002_transformers_part2)

**Status: WRAPPED OK — LO render of the wrapped file pixel-identical to the certified
render (0 of 2,251,125 px differ).** Applied 2026-10-12 (OMML wrap pass, resumed run).
DB certification fields untouched.

- Deliverable: `recreated_pptx/slide_040_recreated.pptx` — single-version law: this file
  IS the wrapped deck now (never LO-resave it).
- Manifest: `recreated_pptx/qa/slide040/eq_040_omml_manifest.json`
- Certified render (comparison base): `qa/slide040/render_7.png` (judge PASS attempt 5)
- Post-wrap render (0-diff): `qa/slide040/render_final_omml.png`

## What was wrapped (all 7 mathtext PNGs)

| rel_id | asset | OMML mathtext | fs (pt) | color |
|---|---|---|---|---|
| rId1 | slide040_h1.png | `\mathbf{Input:}\ \ \mathrm{Values\ of}\ x\ \mathrm{over\ a\ mini-batch:}\ \mathbb{B}=\{x_{1\ldots m}\};` | 15.75 | #000000 |
| rId2 | slide040_h2.png | `\mathrm{Parameters\ to\ be\ learned:}\ \gamma,\ \beta` | 15.5 | #008000 |
| rId3 | slide040_h3.png | `\mathbf{Output:}\ \ \{y_i=\mathrm{BN}_{\gamma,\beta}(x_i)\}` | 16.95 | #000000 |
| rId4 | slide040_eq1.png | `\mu_{\mathbb{B}} ⟵ \frac{1}{m} \sum_{i=1}^{m} x_i` | 19.5 | #000000 |
| rId5 | slide040_eq2.png | `\sigma_{\mathbb{B}}^{2} ⟵ \frac{1}{m} \sum_{i=1}^{m} (x_i - \mu_{\mathbb{B}})^2` | 19.5 | #000000 |
| rId6 | slide040_eq3.png | `\hat{x}_i \leftarrow \frac{x_i - \mu_{\mathbb{B}}}{\sqrt{\sigma_{\mathbb{B}}^2 + \epsilon}}` | 23.0 | #000000 |
| rId7 | slide040_eq4.png | `y_i \leftarrow \gamma\, \hat{x}_i + \beta \equiv \mathrm{BN}_{\gamma,\beta}(x_i)` | 18.6 | #000000 |

fs/color values from the build-side sidecars (`build/assets/slide040_*_eq.json`).

## Representation-level substitutions (documented; PNG fallbacks untouched)

The wrapper's certified converter lacks `\mathcal`, `\longleftarrow`, `\widehat`. The
OMML Choice carries glyph-identical equivalents; the PNG pixels (LibreOffice Fallback)
are untouched:

1. `\mathcal{B}` → `\mathbb{B}` — both produce the script-B glyph U+212C (the wrapper's
   DOUBLE_STRUCK map emits U+212C for B; matplotlib cm-fontset \mathcal{B} renders the
   same script B in the PNG).
2. `\longleftarrow` → literal `⟵` (U+27F5) — verified via matplotlib's mathtext table
   (`tex2uni['longleftarrow'] = U+27F5`): the OMML run glyph equals the PNG glyph.
3. `\widehat{x}` → `\hat{x}` — identical accent placement for a single-char base.

Same-document substitution precedent: slide 030's `\mathit{sin}`→`sin` (030 wrap report).

## Provenance proofs (byte-exact re-render vs banked build assets)

All 7 re-rendered with the certified renderer + this slide's generator matplotlibrc
(cm fontset, `scratch/slide040/matplotlibrc`) at the sidecar fs — **byte-exact (PIL
0-diff) vs `build/assets/slide040_*.png`** for h1, h2, h3, eq1, eq2, eq3, eq4.

## Verification gates (all PASS)

1. Baseline pre-flight: LO render of the UNWRAPPED certified pptx vs
   `qa/slide040/render_7.png` = **0 of 2,251,125 px differ**.
2. LO render of the WRAPPED pptx vs certified = **0 of 2,251,125 px differ**.
3. Idempotence: wrapper re-run → `wrapped=0 skipped=7`, exit 0.
4. Base-md5: only `ppt/slides/slide1.xml` differs; every other entry byte-identical.
5. Structure: 7 `mc:AlternateContent` (a14 Choice OMML + verbatim pic Fallback).

Working evidence: `scratch/slide040/omml/` + `scratch/omml_wrap/`. LO render route:
`scratch/omml_wrap/render_omml.sh`.
