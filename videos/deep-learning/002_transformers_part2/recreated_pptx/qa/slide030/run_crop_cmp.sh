#!/bin/bash
# crop comparison runner: $1=crop name  $2=attempt tag
cd /home/ahmed/Projects/ai_llm_slides
V=videos/deep-learning/002_transformers_part2
Q=$V/recreated_pptx/qa/slide030
scripts/16_vision_gate.sh timeout 540 python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $Q/crops/c_$1_render.png $Q/crops/c_$1_orig.png \
  --view "Slide 030 self-check crop comparison ($1) — region zoom vs original lecture frame" \
  --capture "IMG1=crop of the 150dpi PNG render of the recreation; IMG2=the SAME region cropped from the original lecture video frame, rescaled to identical size" \
  --thinking high --max-tokens 65536 \
  --timeout 420 --rounds 1 --tries 1 \
  --transcript $Q/cropcmp_$1_$2.txt \
  -p "$(cat $Q/judge_template.txt)"
