#!/bin/bash
# Slide 7 corroboration loop — verify_15 on render_12.png (fresh call, same frozen prompt,
# original FIRST). ONE call in flight, outer 1700s / inner 1650s, up to 8 legs, 300s sleeps.
cd /home/codespace/ai_llm_slides || exit 1
NS=videos/machine-learning/08_performance_measure
K=15
RENDER=render_12.png
OUT="$NS/recreated_pptx/qa/slide007/judge_verify_${K}.txt"
TMP="$NS/recreated_pptx/qa/slide007/.verify${K}.tmp"
PROMPT=$(cat "$NS/pool_run/judge_prompt_template.txt")
{
for i in $(seq 1 8); do
  echo "=== verify_${K} leg $i/8 start $(date -u +%FT%TZ) ==="
  timeout 1700 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$NS/unique_slides/slide_007.jpg" "$NS/recreated_pptx/qa/slide007/${RENDER}" \
    --thinking high --max-tokens 65536 --timeout 1650 --rounds 1 --tries 1 \
    -p "$PROMPT" > "$TMP" 2>&1
  rc=$?
  cat "$TMP" >> "$OUT"
  echo "=== verify leg $i rc=$rc $(date -u +%FT%TZ) ===" >> "$OUT"
  if grep -q 'FINAL VERDICT:' "$TMP" && ! grep -qiE '429|HangError|RateLimit' "$TMP"; then
    echo "verify verdict obtained on leg $i rc=$rc" >> "$OUT"
    break
  fi
  if [ "$i" -lt 8 ]; then
    echo "verify leg $i unusable (rc=$rc); sleeping 300s" >> "$OUT"
    sleep 300
  fi
done
rm -f "$TMP"
echo "=== slide7 judge_verify_${K} loop done $(date -u +%FT%TZ) ===" >> "$OUT"
}
echo "verify loop finished for ${K}"
