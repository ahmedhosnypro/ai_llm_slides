# Slide 015 OMML v2 wrap record (002_transformers_part2)

**Status: WRAPPED OK — LO render of the wrapped file pixel-identical to the certified
render (0 of 2,251,125 px differ).** Applied 2026-10-12 (OMML wrap pass, resumed run).
DB certification fields untouched.

- Deliverable: `recreated_pptx/slide_015_recreated.pptx` — single-version law: this file
  IS the wrapped deck now (never LO-resave it).
- Manifest: `recreated_pptx/qa/slide015/eq_015_omml_manifest.json`
- Certified render (comparison base): `qa/slide015/render_1.png` (judge PASS attempt 1)
- Post-wrap render (0-diff): `qa/slide015/render_final_omml.png`

## What was wrapped

| rel_id | asset | mathtext | fs (pt) | color |
|---|---|---|---|---|
| rId1 | eq015_kq.png | `K\cdot q` | 7.0 | #8B1A10 |
| rId2 | eq015_sqrtd.png | `\sqrt{d}` | 8.0 | #8B1A10 |

(K·q/√d scaling pieces of the attention-score formula; same assets as slide 011.)

## Skips (documented)

- rId3 `eq015_scaling_rot.png`, rId4 `eq015_softmax_rot.png` — ROTATED pill labels
  ("Scaling by √d", "Soft max"; matplotlib text rotated 270° at generation,
  scratch/slide015/gen_assets.py). The OMML Choice shape cannot carry the rotation;
  wrapping would corrupt the PowerPoint view. Left as PNG-only.
- rId5 `plane015.png` (translucent gray plane) and rId6 `swoosh015.png` (bezier
  swoosh) — art, not equations.

## Provenance proofs (byte-exact re-render vs banked build assets)

- `K\cdot q` #8B1A10: byte-exact at fs 7.0 via `scripts/render_eq.py`.
- `\sqrt{d}` #8B1A10: byte-exact at fs 8.0.

## Verification gates (all PASS)

1. Baseline pre-flight: LO render of the UNWRAPPED certified pptx vs
   `qa/slide015/render_1.png` = **0 of 2,251,125 px differ**.
2. LO render of the WRAPPED pptx vs certified = **0 of 2,251,125 px differ**.
3. Idempotence: wrapper re-run → `wrapped=0 skipped=2`, exit 0.
4. Base-md5: only `ppt/slides/slide1.xml` differs; every other entry byte-identical.
5. Structure: 2 `mc:AlternateContent` (a14 Choice OMML + verbatim pic Fallback).

Working evidence: `scratch/slide015/omml/` + `scratch/omml_wrap/`. LO render route:
`scratch/omml_wrap/render_omml.sh`.
