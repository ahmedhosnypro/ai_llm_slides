#!/bin/bash
# Judge runner for slide 008 (08_performance_measure). Original FIRST, render SECOND.
# Usage: judge_s08.sh <attemptK> <outfile> [render_png]
cd /home/codespace/ai_llm_slides || exit 1
NS=videos/machine-learning/08_performance_measure
K=$1
OUT="$NS/recreated_pptx/qa/slide008/$2"
RENDER="${3:-$NS/recreated_pptx/qa/slide008/render_${K}.png}"
PROMPT=$(cat "$NS/pool_run/judge_prompt_template.txt")
TMP="$NS/pool_run/tmp/.judge_s08_${K}.tmp"
mkdir -p "$NS/pool_run/tmp"
for i in $(seq 1 8); do
  echo "=== attempt $K retry $i/8 $(date -u +%FT%TZ) render=$RENDER ===" >> "$OUT"
  timeout 900 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$NS/unique_slides/slide_008.jpg" "$RENDER" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    -p "$PROMPT" > "$TMP" 2>&1
  rc=$?
  cat "$TMP" >> "$OUT"
  echo "=== attempt $K retry $i rc=$rc bytes=$(wc -c < "$TMP") $(date -u +%FT%TZ) ===" >> "$OUT"
  if grep -q 'FINAL VERDICT:' "$TMP" && ! grep -qiE '429|HangError|RateLimit' "$TMP"; then
    echo "verdict obtained: attempt $K retry $i" >> "$OUT"
    break
  fi
  [ "$i" -lt 8 ] && sleep 300
done
rm -f "$TMP"
echo "=== judge_s08 $K done $(date -u +%FT%TZ) ===" >> "$OUT"
