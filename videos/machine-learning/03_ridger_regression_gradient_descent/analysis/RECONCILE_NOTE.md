# Analysis reconciliation note (2026-10-19)

- `slide_50_raw.json` (unpadded, written when the image was still named slide_50.jpg)
  renamed to `slide_050_raw.json` (mv, bytes unchanged) after the founder's
  dense renumbering. `_meta.frame` inside still reads "slide_50.jpg" — historical
  name, same bytes as unique_slides/slide_050.jpg (OCR-attribution guard PASS:
  title "Iteration 2" + bullets match tesseract output of slide_050.jpg).
- All 48 pre-existing raws OCR-attribution-verified against their current
  unique_slides images (title-word match ≥50%: 47/48; slide_042 verified by
  layout-content match — handwritten badge not OCR-extractable).
- frames/ and review_packet/ were removed by the founder post-analysis;
  `_meta.source_timestamps` (kept_frame, start/end sec, precuration_slide)
  embedded in each raw is the surviving reconciliation record. slides_index.json
  and new2old_mapping.json are REBUILT from these metas (slides 33/43/44 have no
  raw yet at rebuild time -> provenance from the pre-curation draft is not
  available for them; marked "provenance: unrecoverable (frames removed)".)
