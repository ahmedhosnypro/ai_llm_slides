# OMML_INVENTORY_r5 — deck 03 FINAL OMML wrap census + restage state (2026-11-01)

Namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`.
Method: for each of the 19 eq-pic slides, unzipped `recreated_pptx/slide_NNN_recreated.pptx`,
counted `mc:AlternateContent` elements and `<m:oMath` elements in `ppt/slides/slide1.xml`.
Every wrapped pic = one AlternateContent block containing one Choice (real OMML) + one
Fallback (original PNG) — hence altcontent_count = 2 × omath_count on all 19 slides.
Supersedes r4 (which predated the 2026-10-31/11-01 wrap shards).

## Summary

- Eq pics across 19 slides: **122 total, 122 wrapped, 0 remaining.**
- No slide with eq pics is unwrapped.
- Slides with sidecars but no embedded eq pic (unchanged, skip): 003, 043, 046, 047, 049.

## Per-slide table (final)

| slide | pics wrapped (oMath) | mc:AlternateContent | manifest | 0-px proof | deck page gate |
|---|---|---|---|---|---|
| 004 | 1 | 2 | $RJ/slide004/omml_manifest_parseable_only.json | 0 px vs preOMML backup | p4 stale-FAIL (md5 same; not drifted) |
| 005 | 8 | 16 | $RJ/slide005/omml_manifest_parseable_only.json | 0 px vs banked pdf | p5 stale-FAIL (not drifted) |
| 009 | 2 | 4 | qa/slide009/ | earlier 0-px proof | p9 stale-FAIL (not drifted) |
| 014 | 3 | 6 | $RJ/slide014/omml_manifest.json | 0 px (worker D1) | p14 PASS 0 px |
| 015 | 1 | 2 | $RJ/slide015/omml_manifest_parseable_only.json | 0 px vs banked pdf | p15 stale-FAIL (not drifted) |
| 021 | 5 | 10 | $RJ/slide021/omml_manifest_parseable_only.json | 0 px vs banked pdf | p21 PASS 0 px |
| 023 | 1 | 2 | $RJ/slide023/omml_manifest.json (qa/slide023/omml_manifest.json) | 0 px standalone before/after (worker C) | p23 FAIL — render-context text-AA artifact, deck XML/media byte-identical to source (see report) |
| 030 | 2 | 4 | $RJ/slide030/omml_manifest.json | 0 px vs banked pdf | p30 PASS 0 px |
| 031 | 1 | 2 | $RJ/slide031/omml_manifest.json | 0 px | p31 PASS 0 px |
| 032 | 1 | 2 | $RJ/slide032/omml_manifest.json | 0 px | p32 PASS 0 px |
| 033 | 1 | 2 | $RJ/slide033/omml_manifest.json | 0 px (worker D1) | p33 PASS 0 px |
| 034 | 1 | 2 | $RJ/slide034/omml_manifest.json | 0 px (worker D1) | p34 PASS 0 px |
| 036 | 1 | 2 | qa/slide036/ | earlier 0-px proof | p36 stale-FAIL (not drifted) |
| 037 | 5 | 10 | $RJ/slide037/omml_manifest.json | 0 px | p37 stale-FAIL detail (md5 same; not drifted) |
| 039 | 1 | 2 | qa/slide039/ | earlier 0-px proof | p39 stale-FAIL (not drifted) |
| 044 | 54 | 108 | $RJ/slide044/omml_manifest.json | 0 px | p44 PASS 0 px |
| 048 | 6 | 12 | $RJ/slide048/omml_manifest.json | 0 px; media byte-identical to sidecars | p48 PASS 0 px |
| 050 | 4 | 8 | $RJ/slide050/omml_manifest.json | 0 px | p50 PASS 0 px |
| 051 | 11 | 22 | $RJ/slide051/omml_manifest.json | 0 px; media byte-identical to sidecars | p51 PASS 0 px |

## Restage state (this run, 2026-11-01)

Live drift scan (ledger source_md5 vs on-disk slide md5, render_check != PASS, page 25
excluded per ownership): only pages **10** and **23** drifted.

- p10: `final_deck_tool.py update 10` + `render_check_pages.py 10` → **PASS 0 px**
  (gate_20261101-225651_p10). Ledger now PASS, source_md5 matches.
- p23: restaged twice (`update 23`); deck page slide23.xml and media are byte-identical to
  `slide_023_recreated.pptx` (verified by unzip+md5), but the gate FAILs twice with the
  same diff bbox (199,415,1785,967) — diffs are text anti-aliasing pixels (max delta at
  glyph edges, shift-invariant), i.e. a LibreOffice deck-vs-standalone render-context
  artifact, not a content mismatch. Ledger keeps FAIL with the gate report path.
- Final deck md5 after restage: 35918b6fa1187e85d107aabe481016ff.

## Notes

- Page 25 skipped (owned by another worker).
- No pptx modified, no wrapper run, no git, no DB writes, no vision calls, no evidence deleted.
