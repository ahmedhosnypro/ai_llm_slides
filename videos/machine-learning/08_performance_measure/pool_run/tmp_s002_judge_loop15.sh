#!/usr/bin/env bash
# slide-002 recovery worker: judge attempt 15 vs render_15.png, original-first,
# frozen judge_prompt_template.txt, one call in flight, 1700s wall / --timeout 1650,
# up to 8 tries with 300s sleeps until a FINAL VERDICT line exists.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/08_performance_measure
QA=$NS/recreated_pptx/qa/slide002
LOG=$QA/judge_attempt_15.loop.log
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
cd "$ROOT"
for try in 1 2 3 4 5 6 7 8; do
  echo "try $try start $(date -u +%FT%TZ)" >> "$LOG"
  timeout 1700 bash scripts/16_vision_gate.sh "$PY" .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    videos/machine-learning/08_performance_measure/unique_slides/slide_002.jpg \
    videos/machine-learning/08_performance_measure/recreated_pptx/qa/slide002/render_15.png \
    --thinking high --max-tokens 65536 --timeout 1650 --rounds 1 --tries 1 \
    -p "$(cat videos/machine-learning/08_performance_measure/pool_run/judge_prompt_template.txt)" \
    > "$QA/judge_attempt_15.try$try.txt" 2>&1
  rc=$?
  echo "try $try rc=$rc end $(date -u +%FT%TZ)" >> "$LOG"
  if grep -q "FINAL VERDICT" "$QA/judge_attempt_15.try$try.txt"; then
    cp "$QA/judge_attempt_15.try$try.txt" "$QA/judge_attempt_15.txt"
    echo "VERDICT LANDED try $try rc=$rc $(date -u +%FT%TZ)" >> "$LOG"
    exit 0
  fi
  if [ "$try" -lt 8 ]; then sleep 300; fi
done
echo "EXHAUSTED 8 tries $(date -u +%FT%TZ)" >> "$LOG"
exit 1
