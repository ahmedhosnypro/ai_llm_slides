#!/usr/bin/env bash
# Crop-pair comparisons for slide 031 pre-judge self-check (dense regions).
# Uses the FROZEN judge template from scripts/17_worker_instructions.md, byte-verbatim.
set -u
cd /home/ahmed/Projects/ai_llm_slides
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide031
QA=videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide031
CC=videos/deep-learning/001_transformers_part1/scratch/slide031/cropcmp

TEMPLATE='GROUND RULES (founder-mandated, settle these FIRST and never raise them as discrepancies): (a) The recreation uses a house template — outer red frame x:0.15 y:0.15 w:13.03 h:7.2 line #C00000 1.5pt over #E8E8E8 bg, yellow slide-number badge oval x:12.48 y:0.30 w:0.5 h:0.5 fill #FFF9C4, title box y:0.28 x:0.6 w:12.13 centered. These are INTENTIONAL house chrome and are NOT discrepancies. (b) If image 2 (the original) is a contentless placeholder/Processing slide, then matching contentlessness IS a match — do not demand content the original does not have. (c) Any mouse cursor / video-capture artifact visible in image 2 is a video artifact and is CORRECTLY omitted from the recreation. (d) Typed-vs-handwritten ink is an inherent medium difference — at most MINOR. (e) Equations in the recreation are rendered in PROFESSIONAL 2D FORMAT (stacked fractions with a horizontal bar, large ∑ with limits above/below, spatially aligned sub/superscripts) per founder directive 2026-10-09 — if image 2 (the original) shows the same equation in LINEAR/typed notation, that difference is a mandated format upgrade and is NOT a discrepancy. (f) Your verdict is about fidelity of renderable content ONLY. Image 1 is a PowerPoint recreation; image 2 is the original lecture slide. Compare them element by element for fidelity: title and all text (verbatim, line breaks), layout/regions, table contents and structure, chart types and data values, diagram shapes/arrows, colors (approx hex), imagery. Be PRECISE about text metrics and geometry — measure with your eyes, not vibes: (1) line height / line separation inside multi-line text blocks (e.g. a two-line value listed under a '"'"'(weight (kg), length (cm))'"'"' header must have the same inter-line spacing as the original); (2) vertical centering of enclosed content — text inside brackets, parentheses, or cells must sit vertically CENTERED within the delimiters, not hugging the top while the delimiter'"'"'s lower section wraps empty space; (3) sizes, gaps and ordering of legend items (e.g. '"'"'red class / blue class / green class'"'"') must match the original'"'"'s sizes and gaps; (4) horizontal AND vertical alignment of every label against its value, every value against its enclosing marks, and every region against the original. (5) FRAME CONTAINMENT — every content element (text, box, table, graph, image) must sit fully INSIDE its enclosing frame/panel: any ink that crosses or touches the boundary of the inner frame it belongs to (top/bottom/left/right), or of the house frame, is an overflow and a MAJOR defect; scrutinize the items closest to every frame edge. (6) MISSING ELEMENTS — if the original shows an equation, graph, image, table row, or any visual element that the recreation omits ENTIRELY (absent, not just styled differently), that is a BLOCKER defect; an equation region that renders empty is a BLOCKER even if everything else matches. (7) DELIMITER GEOMETRY — parentheses/brackets/braces that span multiple lines in the original must (i) span ALL the lines they enclose (topmost to bottommost), (ii) be wide enough that their strokes do not sit ON or overlap the enclosed text, (iii) match the original'"'"'s curvature/shape style; a delimiter covering only some of its lines, drawn over the text between it, clipped, or invisible is a MAJOR defect. (8) TABLE DATA — every table cell value must match the original exactly (or the real dataset the original displays, when it is a known dataset such as IRIS); missing rows, truncated tables, or wrong values are MAJOR-to-BLOCKER. A visible deviation in line spacing, vertical centering, gap, size, alignment, frame containment, delimiter geometry, or table data vs the original is a MAJOR defect even when all text is verbatim (founder directives 2026-10-10). List EVERY discrepancy with severity (BLOCKER/MAJOR/MINOR) and confidence, then any visual-quality defects in the recreation (text overflow/clipping, wrong wrapping, misalignment, collisions, illegibility). End with: FINAL VERDICT: PASS or FAIL for '"'"'faithful, usable recreation'"'"'.'

run_cmp() {
  local region="$1" view="$2"
  echo "=== crop comparison: $region ==="
  timeout 1700 scripts/16_vision_gate.sh timeout 540 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$CC/${region}_render.png" "$CC/${region}_orig.png" \
    --view "$view" \
    --capture "IMG1=2x-upscaled crop of the 150dpi PNG render of a 13.33x7.5in PPTX (recreation); IMG2=2x-upscaled crop of the original lecture video frame (960x540); same region of the slide" \
    --thinking high --max-tokens 65536 \
    --timeout 420 --rounds 1 --tries 1 \
    --transcript "$QA/cropcmp_${region}.txt" \
    -p "$TEMPLATE" 2>&1 | tail -2
  echo
}

case "${1:-all}" in
  qpanel)    run_cmp qpanel   "Slide 031 crop (Q panel: input capsule, W_Q 4x4 matrix, =, output capsule) — fidelity check vs original" ;;
  vpanel)    run_cmp vpanel   "Slide 031 crop (V panel: input capsule, W_V 4x4 matrix, =, output capsule) — fidelity check vs original" ;;
  kpanel)    run_cmp kpanel   "Slide 031 crop (K panel: input capsule, W_K 4x4 matrix, =, output capsule) — fidelity check vs original" ;;
  callouts)  run_cmp callouts "Slide 031 crop (dashed callouts, yellow emphasis box, white note box) — fidelity check vs original" ;;
  titleband) run_cmp titleband "Slide 031 crop (title with yellow highlight, subtitle with red keywords, slide-number badge) — fidelity check vs original" ;;
  all)       run_cmp qpanel   "Slide 031 crop (Q panel: input capsule, W_Q 4x4 matrix, =, output capsule) — fidelity check vs original" ;
             run_cmp vpanel   "Slide 031 crop (V panel: input capsule, W_V 4x4 matrix, =, output capsule) — fidelity check vs original" ;
             run_cmp kpanel   "Slide 031 crop (K panel: input capsule, W_K 4x4 matrix, =, output capsule) — fidelity check vs original" ;
             run_cmp callouts "Slide 031 crop (dashed callouts, yellow emphasis box, white note box) — fidelity check vs original" ;
             run_cmp titleband "Slide 031 crop (title with yellow highlight, subtitle with red keywords, slide-number badge) — fidelity check vs original" ;;
esac
