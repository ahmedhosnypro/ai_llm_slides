# Slide 031 OMML v2 wrap record (002_transformers_part2)

**Status: WRAPPED OK — LO render of the wrapped file pixel-identical to the certified
render (0 of 2,251,125 px differ).** Applied 2026-10-12 (OMML wrap pass, resumed run).
DB certification fields untouched.

- Deliverable: `recreated_pptx/slide_031_recreated.pptx` — single-version law: this file
  IS the wrapped deck now (never LO-resave it).
- Manifest: `recreated_pptx/qa/slide031/eq_031_omml_manifest.json` (59 entries, one per
  embedded `<p:pic>`, explicit rel_ids — rId1..rId59 in the build's `eq()` call order;
  dEq.png is embedded 5x = rId54..rId58, one entry each)
- Certified render (comparison base): `qa/slide031/render_2.png` (judge PASS attempt 2)
- Post-wrap render (0-diff): `qa/slide031/render_final_omml.png`

## What was wrapped

ALL 59 equation-segment embeds (55 unique assets from `build/assets/eq_manifest.json`,
the gen_eqs.py sidecar): left-panel vectors lv1/lv2, mid vector A (mva), vector B rows
mvb1/mvb2, remember identities mvr1/mvr2, "Let" definitions db1/db2, derivation rows
dR2..dR6, remainder rewrite r1_s01..r1_s13, dR7 segments, dEq "=" x5, and the callout.
Values (mathtext, fontsize_pt, color) from the sidecar; rel_ids re-derived from the
CURRENT pptx.

## Provenance proofs (byte-exact re-render vs banked build assets)

All 55 unique assets re-rendered and PIL-compared 0-diff against `build/assets/*.png`:
- 49 verified by the first-pass worker (`scratch/omml_wrap/provenance_results.json`),
  independently spot-re-verified where cheap (eq015-equivalents n/a; callout/db group
  intact).
- The 6 first-pass "failures" were VERIFIER ARTIFACTS, re-proven byte-exact this run:
  - dR2..dR6: `scripts/render_eq.py`'s 10-inch canvas cuts the left edge of long
    equations during its probe-drop (probe at x=0.15 overlaps the centered equation);
    gen_eqs.py generated these on a 20-inch canvas. Re-render with the generator's
    20in-canvas code path: **dR2 @fs17.486, dR3 @16.3265, dR4 @15.7605, dR5 @16.0301,
    dR6 @15.3015 — all byte-exact** (sidecar fs values are the rounded 2dp of these;
    the saved PNGs were rendered pre-rounding by fit()).
  - r1_s10: fine scan @fs 14.563..14.578 — **byte-exact** (sidecar 14.56; same rounding).

## Verification gates (all PASS)

1. Baseline pre-flight: LO render of the UNWRAPPED certified pptx vs
   `qa/slide031/render_2.png` = **0 of 2,251,125 px differ**.
2. LO render of the WRAPPED pptx vs certified = **0 of 2,251,125 px differ**.
3. Idempotence: wrapper re-run → `wrapped=0 skipped=59`, exit 0.
4. Base-md5: only `ppt/slides/slide1.xml` differs; every other entry byte-identical
   (no rels/content-types/media touched; the Fallbacks reuse the existing rIds).
5. Structure: 59 `mc:AlternateContent` (a14 Choice OMML, `m:oMathPara(jc=centerGroup)`,
   Cambria-Math runs — PowerPoint's own display-math pattern) + verbatim `<p:pic>`
   Fallback each; slide XML well-formedness re-checked.

Working evidence: `scratch/slide031/omml/` + `scratch/omml_wrap/` (rerender2/ scan
PNGs, verify_provenance.py + provenance_results.json from the first pass). LO render
route: `scratch/omml_wrap/render_omml.sh`.
