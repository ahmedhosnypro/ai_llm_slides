#!/usr/bin/env bash
# cmp5.sh — dense-region crop comparisons through the vision gate (frozen judge -p).
set -u
cd /home/ahmed/Projects/ai_llm_slides
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide051/tmp
mkdir -p "$TMPDIR"
SK=.agents/skills/image-analysis/scripts/analyze_image.py
SCRATCH=videos/deep-learning/002_transformers_part2/scratch/slide051
QA=videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide051

P="GROUND RULES (founder-mandated, settle these FIRST and never raise them as discrepancies): (a) The recreation uses a house template - outer red frame, yellow slide-number badge, centered red title. These are INTENTIONAL house chrome and are NOT discrepancies. (b) If image 2 (the original) is a contentless placeholder/Processing slide, then matching contentlessness IS a match. (c) Any mouse cursor / video-capture artifact visible in image 2 is a video artifact and is CORRECTLY omitted from the recreation. (d) Typed-vs-handwritten ink is an inherent medium difference - at most MINOR. (e) Equations in the recreation are rendered in PROFESSIONAL 2D FORMAT per founder directive 2026-10-09 - if image 2 (the original) shows the same equation in LINEAR/typed notation, that difference is a mandated format upgrade and is NOT a discrepancy. (f) Your verdict is about fidelity of renderable content ONLY. Image 1 is a PowerPoint recreation; image 2 is the original lecture slide. Compare them element by element for fidelity: text (verbatim, line breaks), layout/regions, shapes/arrows, colors (approx hex). Be PRECISE about text metrics and geometry - measure with your eyes, not vibes: (1) line height / line separation inside multi-line text blocks; (2) vertical centering of enclosed content; (3) sizes, gaps and ordering of elements; (4) horizontal AND vertical alignment of every label against its enclosing marks; (5) FRAME CONTAINMENT - every content element must sit fully INSIDE its enclosing frame/panel; (6) MISSING ELEMENTS - a visual element present in the original and absent in the recreation is a BLOCKER defect; (7) text legibility at this zoom - if a string is legible in image 2 but not in image 1, that is a MAJOR defect. A visible deviation in size, gap, alignment, or containment vs the original is a defect even when all text is verbatim. List EVERY discrepancy with severity (BLOCKER/MAJOR/MINOR) and confidence. End with: FINAL VERDICT: PASS or FAIL for 'this region matches at crop zoom'."

run_cmp() {
  local name="$1"; local cap="$2"
  scripts/16_vision_gate.sh timeout 540 python3 "$SK" comparison \
    "$SCRATCH/crops5/${name}_render.png" "$SCRATCH/crops5/${name}_orig.png" \
    --view "Slide 051 attempt-5 pre-judge crop check: ${name}" \
    --capture "$cap" \
    --thinking high --max-tokens 65536 \
    --timeout 420 --rounds 1 --tries 1 \
    --transcript "$QA/crop_cmp_${name}.txt" \
    -p "$P" > "$QA/crop_cmp_${name}.stdout" 2>&1
  echo "== $name exit=$? =="
  tail -c 600 "$QA/crop_cmp_${name}.stdout"
  echo
}

case "${1:-all}" in
  enc_norms) run_cmp enc_norms "IMG1=3x LANCZOS crop of the 150dpi recreation render - encoder stack lower half (steel norm bars, gray Feed Forward box, check circles, green residual stubs), frame x198-290 y255-350; IMG2=3x LANCZOS crop of the original lecture frame, identical region" ;;
  dec_right) run_cmp dec_right "IMG1=2x LANCZOS crop of the 150dpi recreation render - decoder right column (navy disc, tan Nx circle, green check badge, maroon Output Embedding box, dark-brown check, Positional Encoding label), frame x713-870 y272-470; IMG2=2x LANCZOS crop of the original lecture frame, identical region" ;;
  all) run_cmp enc_norms "IMG1=3x LANCZOS crop of the 150dpi recreation render - encoder stack lower half (steel norm bars, gray Feed Forward box, check circles, green residual stubs), frame x198-290 y255-350; IMG2=3x LANCZOS crop of the original lecture frame, identical region"
       run_cmp dec_right "IMG1=2x LANCZOS crop of the 150dpi recreation render - decoder right column (navy disc, tan Nx circle, green check badge, maroon Output Embedding box, dark-brown check, Positional Encoding label), frame x713-870 y272-470; IMG2=2x LANCZOS crop of the original lecture frame, identical region" ;;
esac
