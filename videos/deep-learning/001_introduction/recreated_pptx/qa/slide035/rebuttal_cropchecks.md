# Rebuttals to crop-comparison findings — slide 035 (2026-10-12)

The three dense-region crop comparisons (A filter grid, B panel yellow 3x3,
C caption line 2) all returned FINAL VERDICT: PASS. Their MINOR findings were
individually assessed; the ones touching BAKED content are resampling artifacts
of comparing crops at different pixel densities and are REBUTTED with numbers
(dense-region-crop-compare law: "a coherent body can still mis-state sizes at
zoom — a claim contradicted by measurement is a rebuttal, not a fix trigger").

## Crop B (panel yellow 3x3) — items 1, 2, 4: REBUTTED (resampling artifact)

The whole region B is a verbatim frame crop (panelcontent035.png placed at
(398,185) at exact 478/72 x 236/72 in). Placement proof:
`out_verify_placement_1.txt` + `out_selfcheck_2.txt` "baked placement" —
1:1 downscale diff MAD=7.29 (best offset dx=-1 dy=0, sub-pixel); changed-px
confined to the cursor zone (`out_prep_assets.txt`, 6 sentinels identical).
The baked arrow/greens are the ORIGINAL's own pixels:

1. "annotation line ~2x thicker in IMG1" — the two crops carry the same region
   at different pixel densities (render crop 1560x1184 vs original crop
   748x568 for the same frame box; the render is 150/72 = 2.083x denser). A
   same-physical stroke occupies 2.08x more pixels in IMG1's crop; apparent
   stroke weight scales with crop density. The pixels are identical by the
   placement proof — no weight difference exists in the slide.
2. "line dips and grazes the green cell in IMG1" — same artifact: the blurrier
   resampled copy is read as a lower path. Identical pixels by the proof.
3. "third-row right green cell darker in IMG2" — the model's own "could be
   JPEG chroma fade" applies: IMG1 IS those exact pixels resampled.
4. "row proportions 0.22 vs 0.24" — same density artifact (aspect is preserved
   by exact-size placement; measured cell grid x404..691/y200..416 lands
   within 1 px, `out_verify_placement_1.txt`).

## Crop A (filter grid) — D2, D3: REBUTTED / verified non-defects

- D2 "digits ~50% vs 40-43% of cell height": measured per-cell digit ink
  (out_measure_original5.txt P8): original digits 11 px cap in 23 px cells
  (48%); render digits Verdana Bold 15 cap 11 px in 24 px cells (46%). The
  claim's numbers are contradicted by ~2 px centers — rebuttal.
- D3 "bottom border thinner/partially cut": PIL green-border pixel counts
  (out_filter_border_check.txt): render bottom border band y289..294 x268..366
  = 442 green px (present, full span), below-bottom zone y292..296 = 0 px (no
  overflow/stubs beyond the border), matching the original's structure
  (bottom band 281 px, below-bottom 0). The "thin green stubs" the judge saw
  are the border's own AA at 4x zoom. No clipping exists.
- D1 (digit typeface read as serif-ish) — accepted as MINOR per ground rule
  (d); Verdana Bold's slab-like '1' base is the closest installed match
  (Arial's '0' 7px vs measured 10px was the rejected alternative;
  out_measure_original6.txt Q5).

## Crop C (caption line 2) — no rebuttals needed

Both MINORs are self-identified zoom/JPEG artifacts (paren weight at 2x zoom;
border hue chroma fade). The load-bearing verdict — the color layout (navy
parens, red span, red bold underlined PERCEPTRON) matches image 2 — confirms
the measured-layout build decision.
