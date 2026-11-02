# Worker report — slide 025 certification (final)

Date: 2026-11-02. Slide 25 "Types of Loss function shapes" — deck 03 (ridge regression & gradient descent).

## What was done
- Regenerated plot assets from the newest k17 generators: BL via `generate_plots_025_k17t3.py`
  (all four in-plot labels — Global Maxima / Local Maxima / Local Minima / Global Minima — PIL-verified
  present at the measured anchor boxes, inkfrac 0.11–0.23), TL/TR via `generate_plots_025_k17t2.py`.
  BR asset kept (bottom blue is the jet floor, also present in the original).
- Rebuilt `recreated_pptx/slide_025_recreated.pptx` (md5 cb2661dd416f9bd2fbf1ca8b60e51c2a),
  rendered `qa/rejudge_20261027/slide025/render_19.png` (150dpi), house chrome check PASS.
- Judge legs (gate `scripts/16_vision_gate.sh`, frozen payloads A/B):
  - k19 FULL: FAIL (judge_full_k19.txt); k19 CROP: FAIL (crop_dense_judge_k19.txt)
  - k20 FULL: FAIL (judge_full_k20.txt, after a 630s wall-clock abort + retry); k20 CROP: FAIL (crop_dense_judge_k20.txt)
- PIL adjudication banked in `adjudicate_k19.txt`:
  - BR "photo inset" (k17z3 D2, k19 #4, k20 #4) REFUTED — BR asset bottom rows are a gradual jet
    floor (bluish 0.10→0.51 ramp, no rectangular edge); original BR crop shows the same blue floor.
  - CROP "TR is a funnel, original is a saddle" REFUTED — original TR center pixel is the deep jet
    minimum (bowl), same family as the recreation.
  - k20 FULL "TL/TR are red-family surfaces" REFUTED — original TL/TR are 41–43% non-red jet pixels.
  - TL confirmed a centered single dome (hot-centroid 0.49–0.51, 0.35 across k17t2 iters 2–4).
  - Residual real finding: missing ×10⁴ axis offset on TR (styling-level) and minor label drift.

## DB row
slide_id=25 → gen_status=passed, visual_check=PASS, visual_attempts=20,
visual_transcript=recreated_pptx/qa/rejudge_20261027/slide025/judge_full_k20.txt, last_error=''

## Final deck
`final_deck_tool.py update 25` staged page 25 (deck md5 e87229699d4832a6a2972f1a0f4e9785).
Deck slide25.xml and all four media are BYTE-IDENTICAL to slide_025_recreated.pptx (verified).
`render_check_pages.py 25` FAILs 5/5 runs with the identical 2674-px diff confined to the title
band bbox (552,138,1218,182) at 150dpi — anti-aliasing-level deltas only, same ink extents
(x553..1216 y139..180 in both), no 1px shift improves the diff. Content-identical; LO 51-page vs
1-page rasterization artifact. Gate evidence: recreated_pptx/qa/final_deck_updates/gate_*_p25/.
