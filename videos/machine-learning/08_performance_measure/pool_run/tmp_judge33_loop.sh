#!/bin/bash
# Judge attempt loop for slide 033 — original-first comparison through the fleet gate.
# Writes the verdict-bearing transcript to recreated_pptx/qa/slide033/judge_attempt_1.txt
cd /home/codespace/ai_llm_slides || exit 1
NS=videos/machine-learning/08_performance_measure
OUT="$NS/recreated_pptx/qa/slide033/judge_attempt_1.txt"
TMP="$NS/pool_run/tmp/.judge33_attempt.tmp"
mkdir -p "$NS/pool_run/tmp"
PROMPT=$(cat "$NS/pool_run/judge_prompt_template.txt")
: > "$OUT"
for i in $(seq 1 8); do
  echo "=== attempt $i/8 $(date -u +%FT%TZ) ===" >> "$OUT"
  timeout 540 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$NS/unique_slides/slide_033.jpg" \
    "$NS/recreated_pptx/qa/slide033/render_1.png" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    -p "$PROMPT" > "$TMP" 2>&1
  rc=$?
  cat "$TMP" >> "$OUT"
  echo "=== attempt $i rc=$rc bytes=$(wc -c < "$TMP") $(date -u +%FT%TZ) ===" >> "$OUT"
  if grep -aq 'FINAL VERDICT:' "$TMP" && ! grep -aqiE '429|HangError|RateLimit' "$TMP"; then
    echo "VERDICT OBTAINED on attempt $i" >> "$OUT"
    break
  fi
  [ "$i" -lt 8 ] && { echo "attempt $i unusable; sleeping 300s" >> "$OUT"; sleep 300; }
done
rm -f "$TMP"
echo "LOOP DONE $(date -u +%FT%TZ)" >> "$OUT"
