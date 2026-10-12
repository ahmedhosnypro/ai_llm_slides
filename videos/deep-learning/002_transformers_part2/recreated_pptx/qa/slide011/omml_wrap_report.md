# Slide 011 OMML v2 wrap record (002_transformers_part2)

**Status: WRAPPED OK — LO render of the wrapped file pixel-identical to the certified
render (0 of 2,251,125 px differ).** Applied 2026-10-12 (OMML wrap pass, resumed run).
DB certification fields untouched.

- Deliverable: `recreated_pptx/slide_011_recreated.pptx` — single-version law: this file
  IS the wrapped deck now (never LO-resave it).
- Manifest: `recreated_pptx/qa/slide011/eq_011_omml_manifest.json`
- Certified render (comparison base): `qa/slide011/render_2.png` (judge PASS attempt 3)
- Post-wrap render (0-diff): `qa/slide011/render_final_omml.png`

## What was wrapped

| rel_id | asset | mathtext | fs (pt) | color |
|---|---|---|---|---|
| rId1 | eq015_kq.png | `K\cdot q` | 7.0 | #8B1A10 |
| rId2 | eq015_sqrtd.png | `\sqrt{d}` | 8.0 | #8B1A10 |

These are the K·q/√d scaling pieces of the attention formula (numerator PNG + radical
PNG placed at measured ink positions; the fraction bar is drawn content, untouched).

## Skips (documented)

- rId3 `eq015_scaling_rot.png`, rId4 `eq015_softmax_rot.png` — ROTATED pill labels
  (matplotlib text rotated 270° at generation, gen_assets.py). The OMML Choice shape
  cannot carry the rotation; wrapping would show horizontal text in PowerPoint while
  the Fallback stays rotated. Left as PNG-only (not equation-body content).
- rId6 `swoosh015.png` — bezier swoosh art (gen_assets.py), not an equation.
- (rId5/image-1-5.png exists only as an orphan rel — no `<p:pic>` uses it.)

## Provenance proofs (byte-exact re-render vs banked build assets)

- `K\cdot q` #8B1A10: byte-exact at fs 7.0 (and 7.0002) via `scripts/render_eq.py`.
- `\sqrt{d}` #8B1A10: byte-exact at fs 8.0 (prior run's 8.0163 was a width-fit artifact;
  scan found the true 8.0).
- eq015_scaling_rot/softmax_rot: generated as rotated DejaVu labels (gen_assets.py),
  not render_eq mathtext — n/a (skipped).

## Verification gates (all PASS)

1. Baseline pre-flight: LO render of the UNWRAPPED certified pptx vs
   `qa/slide011/render_2.png` = **0 of 2,251,125 px differ**.
2. LO render of the WRAPPED pptx vs certified = **0 of 2,251,125 px differ**.
3. Idempotence: wrapper re-run → `wrapped=0 skipped=2`, exit 0.
4. Base-md5: only `ppt/slides/slide1.xml` differs; every other entry byte-identical.
5. Structure: 2 `mc:AlternateContent` (a14 Choice OMML + verbatim pic Fallback).

Working evidence: `scratch/slide011/omml/` + `scratch/omml_wrap/`. LO render route:
`scratch/omml_wrap/render_omml.sh`.
