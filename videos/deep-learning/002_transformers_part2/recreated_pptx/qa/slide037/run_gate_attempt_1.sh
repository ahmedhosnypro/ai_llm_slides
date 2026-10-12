#!/bin/bash
# Judge runner for slide 037 attempt 1 — implements the frozen procedure (probe ->
# W4 comparison), with the skill's patience rules. Self-execution fallback per
# scripts/17_worker_instructions.md §7 (no Agent/Task spawn tool in this environment).
set -u
cd /home/ahmed/Projects/ai_llm_slides
Q=videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide037
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide037
LOG=$Q/run_gate_attempt_1.log
echo "=== judge attempt 1 $(date -Is) ===" >> $LOG

probe () {
  scripts/16_vision_gate.sh timeout 150 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py analysis \
    $Q/render_1.png \
    --view "Slide 037 recreation attempt 1 — probe" \
    --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
    --timeout 120 --rounds 1 --tries 1 \
    --transcript $Q/probe_1.txt >> $LOG 2>&1
  [ -s $Q/probe_1.txt ]
}

# probe; on hang: sleep 300 and re-probe ONCE (frozen law)
if ! probe; then
  echo "probe try 1 failed/hung; sleeping 300 then re-probing once" >> $LOG
  sleep 300
  probe || { echo "PROBE_FAILED" >> $LOG; }
fi

# comparison at the W4 wall
cmp_once () {
  scripts/16_vision_gate.sh timeout 540 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $Q/render_1.png videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg \
    --view "Slide 037 recreation — fidelity check vs original lecture frame" \
    --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
    --thinking high --max-tokens 65536 \
    --timeout 420 --rounds 1 --tries 1 \
    --transcript $Q/judge_attempt_1.txt >> $LOG 2>&1
  [ -s $Q/judge_attempt_1.txt ]
}

for try in 1 2 3 4; do
  echo "=== comparison try $try $(date -Is) ===" >> $LOG
  if cmp_once; then
    echo "COMPARISON_LANDED try $try" >> $LOG
    exit 0
  fi
  echo "comparison try $try did not land; sleep 240 before next" >> $LOG
  sleep 240
done
echo "COMPARISON_FAILED_ALL_TRIES" >> $LOG
exit 1
