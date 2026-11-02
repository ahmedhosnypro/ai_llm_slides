#!/usr/bin/env bash
# Judge runner for slide 21 finish pass. args: <out_suffix> <render_png> [max_tries]
# ORIGINAL FIRST, render SECOND. Retries up to 8x on 429/HangError/empty (sleep 300 between).
set -u
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
OUT="$NS/recreated_pptx/qa/slide021/judge_${1}.txt"
RENDER="$2"
MAXT=${3:-8}
LOG="$NS/recreated_pptx/qa/slide021/judge_${1}.log"
PROMPT=$(cat "$NS/pool_run/judge_prompt_template.txt")
: > "$OUT"; : > "$LOG"
for i in $(seq 1 "$MAXT"); do
  S=$((90 + RANDOM % 61))
  echo "=== try $i/$MAXT pre-sleep ${S}s $(date -u +%FT%TZ) render=$RENDER ===" >> "$LOG"
  sleep "$S"
  timeout 540 bash scripts/16_vision_gate.sh /home/codespace/.pyenv/versions/3.15.2/bin/python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$NS/unique_slides/slide_021.jpg" "$RENDER" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    -p "$PROMPT" >> "$OUT" 2>&1
  rc=$?
  echo "try $i rc=$rc bytes=$(wc -c < "$OUT") $(date -u +%FT%TZ)" >> "$LOG"
  if grep -q "FINAL VERDICT" "$OUT"; then
    echo "VERDICT OBTAINED try $i rc=$rc" >> "$LOG"
    grep "FINAL VERDICT" "$OUT" | tail -1
    exit 0
  fi
  sleep 300
done
echo "ALL TRIES FAILED" >> "$LOG"
exit 1
