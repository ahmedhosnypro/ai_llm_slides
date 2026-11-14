#!/usr/bin/env bash
# Fresh slide-019 judge attempt 9 — original-first, frozen prompt, ONE call in
# flight, outer 1700s / inner 1650s walls, up to 8 legs, 300s backoff.
set -u
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
Q=$NS/recreated_pptx/qa/slide019
MODE=${1:-attempt}
K=${2:-9}
R=${3:-9}
if [ "$MODE" = attempt ]; then OUT="$Q/judge_attempt_${K}.txt"; else OUT="$Q/judge_verify_${K}.txt"; fi
LOG=$NS/pool_run/tmp/s19_${MODE}${K}_loop.out
: > "$OUT"
echo "${MODE}${K} start $(date -u +%FT%TZ) render=render_${R}.png prompt=judge_prompt_template.txt" >> "$LOG"
for leg in 1 2 3 4 5 6 7 8; do
  echo "=== leg $leg $(date -u +%FT%TZ) ===" >> "$OUT"
  timeout 1700 bash scripts/16_vision_gate.sh python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$NS/unique_slides/slide_019.jpg" \
    "$Q/render_${R}.png" \
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
