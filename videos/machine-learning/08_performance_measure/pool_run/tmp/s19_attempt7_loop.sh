#!/usr/bin/env bash
# Fresh slide-019 recovery judge attempt 7 — original-first, frozen prompt,
# ONE call in flight, outer 1700s / inner 1650s walls, up to 8 legs, 300s backoff.
set -u
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
Q=$NS/recreated_pptx/qa/slide019
OUT=$Q/judge_attempt_7.txt
LOG=$NS/pool_run/tmp/s19_attempt7_loop.out
: > "$OUT"
echo "attempt7 start $(date -u +%FT%TZ) render=render_5.png prompt=judge_prompt_template.txt" >> "$LOG"
for leg in 1 2 3 4 5 6 7 8; do
  echo "=== leg $leg $(date -u +%FT%TZ) ===" >> "$OUT"
  timeout 1700 bash scripts/16_vision_gate.sh python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$NS/unique_slides/slide_019.jpg" \
    "$Q/render_5.png" \
    --thinking high --max-tokens 65536 --timeout 1650 --rounds 1 --tries 1 \
    -p "$(cat "$NS/pool_run/judge_prompt_template.txt")" >> "$OUT" 2>&1
  rc=$?
  echo "=== leg $leg rc=$rc $(date -u +%FT%TZ) ===" >> "$OUT"
  echo "leg $leg rc=$rc $(date -u +%FT%TZ)" >> "$LOG"
  if grep -q 'FINAL VERDICT' "$OUT"; then
    echo "VERDICT $(grep -o 'FINAL VERDICT: [A-Z]*' "$OUT" | tail -1) after leg $leg" >> "$LOG"
    break
  fi
  if [ "$leg" -lt 8 ]; then sleep 300; fi
done
echo "LOOP DONE $(date -u +%FT%TZ)" >> "$OUT"
echo "LOOP DONE $(date -u +%FT%TZ)" >> "$LOG"
