#!/bin/bash
# judge_run_024.sh <K> <outfile> — one original-first comparison judge call for slide 024,
# retrying up to 8x on 429/HangError/empty with 300s sleeps. Run from repo root.
cd /home/codespace/ai_llm_slides || exit 1
NS=videos/machine-learning/08_performance_measure
K=$1
OUT="$NS/recreated_pptx/qa/slide024/$2"
TMP="$NS/pool_run/.judge24_${K}_$(basename "$OUT").tmp"
PROMPT=$(cat "$NS/pool_run/judge_prompt_template.txt")
mkdir -p "$NS/recreated_pptx/qa/slide024"
for i in $(seq 1 8); do
  echo "=== judge attempt K=$K leg $i/8 $(date -u +%FT%TZ) ===" >> "$OUT"
  timeout 540 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$NS/unique_slides/slide_024.jpg" \
    "$NS/recreated_pptx/qa/slide024/render_${K}.png" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    -p "$PROMPT" > "$TMP" 2>&1
  rc=$?
  cat "$TMP" >> "$OUT"
  echo "=== leg $i rc=$rc bytes=$(wc -c < "$TMP") $(date -u +%FT%TZ) ===" >> "$OUT"
  if grep -q 'FINAL VERDICT:' "$TMP" && ! grep -qiE '429|HangError|RateLimit' "$TMP"; then
    echo "verdict obtained on leg $i" >> "$OUT"
    break
  fi
  if [ "$i" -lt 8 ]; then
    echo "leg $i unusable; sleeping 300s" >> "$OUT"
    sleep 300
  fi
done
rm -f "$TMP"
echo "judge_run_024 K=$K done $(date -u +%FT%TZ)" >> "$OUT"
