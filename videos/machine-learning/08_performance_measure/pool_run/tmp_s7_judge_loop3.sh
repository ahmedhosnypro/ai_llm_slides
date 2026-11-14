#!/bin/bash
# Slide 7 judge loop v3 — GATE-AWARE: ONE call in flight, outer 1700s / inner 1650s,
# original FIRST, render SECOND, frozen judge prompt, up to 8 legs, 300s sleeps.
# Appends to qa/slide007/judge_attempt_K.txt (K from argv[1], default 1).
cd /home/codespace/ai_llm_slides || exit 1
NS=videos/machine-learning/08_performance_measure
K=${1:-1}
RENDER=${2:-render_4.png}
OUT="$NS/recreated_pptx/qa/slide007/judge_attempt_${K}.txt"
TMP="$NS/recreated_pptx/qa/slide007/.attempt${K}.tmp"
PROMPT=$(cat "$NS/pool_run/judge_prompt_template.txt")
{
for i in $(seq 1 8); do
  echo "=== attempt_${K} leg $i/8 start $(date -u +%FT%TZ) ==="
  timeout 1700 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$NS/unique_slides/slide_007.jpg" "$NS/recreated_pptx/qa/slide007/${RENDER}" \
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
echo "=== slide7 judge_attempt_${K} loop done $(date -u +%FT%TZ) ===" >> "$OUT"
}
echo "loop v3 finished for attempt ${K}"
