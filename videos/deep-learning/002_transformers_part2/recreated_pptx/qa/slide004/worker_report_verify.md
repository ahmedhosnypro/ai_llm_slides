# Worker report — 002_transformers_part2 slide 004 (SECOND dispatch: measurement + independent verification)

Slide 004 was certified by a CONCURRENT worker while this dispatch was mid-measurement
(the orchestrator double-dispatched; each of us found a `gen_status=building` DB row and
scratch evidence and concluded "resumed from a crashed prior attempt" about the other).
This report is THIS worker's record; the certified build's own report is
`worker_report.md` (untouched). Nothing in the certified deliverable was modified.

## Final verdict

**PASS (accepted)** — real visual-judge comparison PASS at attempt 1 by the concurrent
worker, independently re-verified by this worker. DB row already complete:
`gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
`visual_transcript=qa/slide004/judge_attempt_1.txt`. No DB writes needed.

## What this dispatch contributed

1. **Independent delta measurement** (`scratch/slide004/m1b..m15`, this worker's files:
   m1b_fit, m2_diff, m3_census, m4_structure, m5_fine, m6_highlights, m7_refgeom,
   m8_scans, m9_runs, m10_final/m10b_final, m11_delta, m12_iso, m13_segfit, m14_asset,
   m15_edges + fit*.npy/amap.npy/rects_*.npy):
   - Import verification: re-rendering 001:15's certified component with numeral 4
     reproduces `001_transformers_part1/qa/slide015/render_1.png` with **max diff 0
     outside the badge numeral** — pixel-exact inheritance (m2_diff.py).
   - Frame→render mapping from this frame's four chrome landmarks (59.0/901.0/43.0/516.0)
     + badge centroid, refined by content-masked SSD (SSD 249.6→169.6, m5):
     `render_x = -43.507 + 2.173933*fx ; render_y = -3.486 + 2.174227*fy`.
   - Delta census: composition matches the frame everywhere (title ink bbox, block
     arrow, both panels at JPEG-noise level, m4/m11); the ONLY real deltas are the two
     semi-transparent orange highlight rectangles. No removals.
   - Blend solve on clean flat fields (peach FDEDDD, mint CEFFE1, m10b): **alpha 0.50,
     color (240,122,2) = F07A00**, predicted cores match the frame within ≤1.5/255;
     blend-segment t-median across all highlight components 0.494..0.526 (m13).
   - Rect edges (blend-segment 50%-coverage crossings, m13/m15, build pt):
     H1 x 583.5..735.8, y ~356.3..401.7 (right edge = the Encoder/Decoder zone boundary
     line baked in the certified asset at pt 735.9..737.2, m14); H2 x 736.8..887.6,
     y ~275.5..323.9. The two rects ABUT on the zone boundary line and leave the dark
     line itself uncovered (frame probes t≈0.82 on the line column).
2. **Independent verification of the certified deliverable**
   (`qa/slide004/selfcheck_worker2.py` + `selfcheck_worker2_output.txt`):
   - Fresh soffice re-render of `slide_004_recreated.pptx` is **pixel-identical**
     (max diff 0) to the banked `qa/slide004/render_1.png`.
   - `house_chrome_check.py` → PASS.
   - Inheritance confinement: render-vs-base hot pixels (63,245) have **0 outside** the
     two highlight zones + badge numeral region.
   - Judge-evidence audit: `judge_prompt_1.txt` carries the frozen `-p` template
     byte-identical (spot-checked against `scripts/17_worker_instructions.md`) with the
     required shared-base `--view`; `judge_attempt_1.txt` is a coherent comparison body
     ending "FINAL VERDICT: PASS for 'faithful, usable recreation'." — not degenerate.

## Recorded precision notes (no action — below the acceptance gate)

The certified build used its own (valid) measurement chain; against this worker's
independent crossings the certified deliverable measures:

- Fill `E76B00`@50 vs this worker's clean-field fit `F07A00`@50: blended-over-peach
  error vs frame core (4,7,0.5)/255 for E76B00 vs (0.5,0.5,0.5) for F07A00; over mint
  (4.5,8,2.5) vs (0,0.5,1.5). The E76B00 fit's rms (5.3 over 7 mixed patches) is
  consistent with text-adjacent patch contamination; F07A00 fits the two large clean
  fields near-exactly. The difference is below the visual judge's discrepancy threshold
  (the judge passed the highlights explicitly: "Positions, extents, and overlap behavior
  match the original").
- Three rect edges sit 2.2–3.7pt from this worker's crossings (H1 bottom +3.7pt into the
  fade tail; H2 top −2.2pt; H2 right −2.2pt); the other five edges are ≤1.6pt. Both
  chains carry ±1–1.5pt mapping/crossing uncertainty, so the chains agree within their
  combined uncertainty on 5 of 8 edges and differ sub-judge-visibly on 3.

Under the verdict law (real comparison PASS = done; PIL evidence can never override the
visual gate) and the single-version law (one certified deliverable, already banked),
these notes are recorded for the record only. If the founder ever re-opens this slide,
the F07A00/edge numbers above are the measured targets.

## Judge findings disposition (inheritance law)

All four judge findings are MINOR and land on INHERITED certified pixels (0-diff proven
against 001:15's certified render): palette drift (#1, #4) and the up-arrow rendering
notes (#2, #3 — up1/up2 are the parent component's banked 600-dpi PNGs). Judge variance,
documented and overridden per `scripts/17_worker_instructions.md` dependency rule 5.
The crop-check's "(shifted right) missing" / "arrow clipped" findings were shown by the
concurrent worker's PIL check to be crop-window artifacts, not build defects.

## Evidence index (this dispatch)

- `qa/slide004/selfcheck_worker2.py`, `selfcheck_worker2_output.txt`
- `scratch/slide004/`: m1b–m15 scripts + fit.npy/fit2.npy/fit_content.npy/amap.npy/
  rects_segfit.npy/rects_iso.npy + base_num4.pptx/base-1.png (import check) +
  deliverable-1.png (fresh re-render) + frame_warped*_contentfit.png
- Certified evidence (concurrent worker, untouched): see `worker_report.md`
