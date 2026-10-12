#!/usr/bin/env bash
# Crop-pair comparisons for slide 019 dense regions (pre-judge self-check #6).
set -u
cd /home/ahmed/Projects/ai_llm_slides
B=videos/deep-learning/001_introduction
Q=$B/recreated_pptx/qa/slide019/crops_attempt_5
TPL="GROUND RULES (founder-mandated, settle these FIRST and never raise them as discrepancies): (a) The recreation uses a house template — outer red frame x:0.15 y:0.15 w:13.03 h:7.2 line #C00000 1.5pt over #E8E8E8 bg, yellow slide-number badge oval x:12.48 y:0.30 w:0.5 h:0.5 fill #FFF9C4, title box y:0.28 x:0.6 w:12.13 centered. These are INTENTIONAL house chrome and are NOT discrepancies. (b) If image 2 (the original) is a contentless placeholder/Processing slide, then matching contentlessness IS a match — do not demand content the original does not have. (c) Any mouse cursor / video-capture artifact visible in image 2 is a video artifact and is CORRECTLY omitted from the recreation. (d) Typed-vs-handwritten ink is an inherent medium difference — at most MINOR. (e) Equations in the recreation are rendered in PROFESSIONAL 2D FORMAT (stacked fractions with a horizontal bar, large ∑ with limits above/below, spatially aligned sub/superscripts) per founder directive 2026-10-09 — if image 2 (the original) shows the same equation in LINEAR/typed notation, that difference is a mandated format upgrade and is NOT a discrepancy. (f) Your verdict is about fidelity of renderable content ONLY. Image 1 is a PowerPoint recreation crop; image 2 is the original lecture slide crop OF THE SAME REGION (resolutions differ). Compare them element by element for fidelity: text (verbatim, line breaks), shapes, colors, positions, stroke weights. Be PRECISE about text metrics and geometry — measure with your eyes, not vibes: line spacing, vertical centering, alignment, sizes, gaps. List EVERY discrepancy with severity (BLOCKER/MAJOR/MINOR) and confidence, then any visual-quality defects in the recreation crop (text overflow/clipping, wrong wrapping, misalignment, collisions, illegibility). End with: FINAL VERDICT: PASS or FAIL for 'faithful, usable recreation'."
run_one() {
  local name=$1; local view=$2
  for attempt in 1 2 3; do
    echo "=== $name comparison attempt $attempt $(date -Iseconds) ==="
    TMPDIR=/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide019 \
    scripts/16_vision_gate.sh timeout 540 python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
      $Q/${name}_render.png $Q/${name}_original.png \
      --view "$view" \
      --capture "IMG1=crop of the 150dpi PNG render (higher res); IMG2=crop of the original lecture frame — SAME region" \
      --thinking high --max-tokens 65536 \
      --timeout 420 --rounds 1 --tries 1 \
      --transcript $Q/cmp_${name}.txt \
      -p "$TPL"
    rc=$?
    echo "rc=$rc"
    if [ $rc -eq 0 ] && grep -q "FINAL VERDICT" $Q/cmp_${name}.txt 2>/dev/null; then
      echo "$name: verdict landed"; return 0
    fi
    [ $attempt -lt 3 ] && echo "retry after 120s storm backoff" && sleep 120
  done
  echo "$name: FAILED after retries"; return 1
}
run_one verr "Slide 019 crop — Prediction Error (Loss Function) vertical pink box with rotated bottom-to-top label (self-check crop comparison)"
run_one pencil "Slide 019 crop — pencil glyph in the Pre processing box top-right corner (self-check crop comparison)"
run_one chain_left "Slide 019 crop — Input Samples box, red arrow, dashed container left border, Pre processing box with two-line label (self-check crop comparison)"
