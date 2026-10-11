#!/usr/bin/env bash
# Full-slide judge, attempt 2 (probe + W4 comparison), per judge_full_prompt_2.txt.
set -u
cd /home/ahmed/Projects/ai_llm_slides
export TMPDIR=$PWD/videos/deep-learning/002_transformers_part2/scratch/slide031
Q=videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide031

echo "=== PROBE 2 $(date +%T) ==="
scripts/16_vision_gate.sh timeout 150 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py analysis \
  $Q/render_2.png \
  --view "Slide 031 recreation attempt 2 — probe" \
  --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
  --timeout 120 --rounds 1 --tries 1 \
  --transcript $Q/probe_2.txt
echo "probe exit=$? $(date +%T)"

echo "=== JUDGE COMPARISON 2 $(date +%T) ==="
scripts/16_vision_gate.sh timeout 540 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $Q/render_2.png videos/deep-learning/002_transformers_part2/unique_slides/slide_031.jpg \
  --view "Slide 031 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 420 --rounds 1 --tries 1 \
  --transcript $Q/judge_attempt_2.txt \
  -p "$(cat $Q/judge_prompt_2.txt)"
echo "judge exit=$? $(date +%T)"
