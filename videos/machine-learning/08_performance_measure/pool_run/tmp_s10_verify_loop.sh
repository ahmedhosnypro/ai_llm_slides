#!/bin/bash
# Slide 10 corroboration (verify) loop — same walls as the attempt loop, fresh call,
# transcript judge_verify_K.txt. K from argv[1], render from argv[2].
cd /home/codespace/ai_llm_slides || exit 1
NS=videos/machine-learning/08_performance_measure
K=${1:-1}
RENDER=${2:-render_1.png}
OUT="$NS/recreated_pptx/qa/slide010/judge_verify_${K}.txt"
TMP="$NS/recreated_pptx/qa/slide010/.verify${K}.tmp"
PROMPT=$(cat "$NS/pool_run/judge_prompt_template.txt")
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
mkdir -p "$NS/recreated_pptx/qa/slide010"
{
for i in $(seq 1 8); do
  echo "=== verify_${K} leg $i/8 start $(date -u +%FT%TZ) ==="
  timeout 1700 bash scripts/16_vision_gate.sh "$PY" .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$NS/unique_slides/slide_010.jpg" "$NS/recreated_pptx/qa/slide010/${RENDER}" \
    --thinking high --max-tokens 65536 --timeout 1650 --rounds 1 --tries 1 \
    -p "$PROMPT" > "$TMP" 2>&1
  rc=$?
  cat "$TMP" >> "$OUT"
  echo "=== leg $i rc=$rc $(date -u +%FT%TZ) ===" >> "$OUT"
  if grep -q 'FINAL VERDICT:' "$TMP" && ! grep -qiE '429|HangError|RateLimit' "$TMP"; then
    echo "verdict obtained on leg $i rc=$rc" >> "$OUT"
    break
  fi
  if [ "$i" -lt 8 ]; then
    echo "leg $i unusable (rc=$rc, no clean verdict); sleeping 300s" >> "$OUT"
    sleep 300
  fi
done
rm -f "$TMP"
echo "=== slide10 judge_verify_${K} loop done $(date -u +%FT%TZ) ===" >> "$OUT"
}
echo "verify loop finished for ${K}"
