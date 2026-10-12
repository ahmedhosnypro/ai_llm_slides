#!/bin/bash
set -u
cd /home/ahmed/Projects/ai_llm_slides
V=videos/deep-learning/001_introduction
Q=$V/recreated_pptx/qa/slide022
G="TMPDIR=$V/scratch_022 scripts/16_vision_gate.sh"
PRELUDE="GROUND RULES (founder-mandated, settle these FIRST and never raise them as discrepancies): (a) The recreation uses a house template - the outer chrome is INTENTIONAL and NOT part of this comparison; judge ONLY the cropped content region. (b) IMG1 is a 150dpi LibreOffice render of a PowerPoint recreation; IMG2 is the original lecture video frame upscaled to the same size - JPEG softness in IMG2 is inherent. (c) Video artifacts (mouse cursor, black player bar) are correctly omitted. (d) Equations are rendered in PROFESSIONAL 2D FORMAT per founder directive - stacked vectors with tall thin parens; if IMG2 shows the same content slightly differently weighted, weigh CONTENT fidelity highest. (e) Small deviations of 1-3 frame-px in stroke weight/antialiasing are MINOR. Compare the two crops element by element (text verbatim, positions, colors, shapes, line geometry); list every discrepancy with severity (BLOCKER/MAJOR/MINOR) and confidence; end with 'CROP VERDICT: MATCH' or 'CROP VERDICT: MISMATCH'."
for C in eq1 eq2 dec diag; do  # round 2 on render_3
  TMPDIR=$V/scratch_022 scripts/16_vision_gate.sh timeout 280 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $Q/crops/${C}_render.png $Q/crops/${C}_orig.png \
    --view "Slide 022 crop check: $C region - recreation vs original (same scale)" \
    --capture "IMG1=150dpi LO render crop of the recreated PPTX; IMG2=original 960x540 frame crop upscaled to identical size" \
    --timeout 240 --rounds 1 --tries 1 \
    -p "$PRELUDE" \
    --transcript $Q/crop_${C}.txt 2>&1 | tail -4
  echo "--- done $C ---"
done
