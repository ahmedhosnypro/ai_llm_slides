#!/usr/bin/env bash
# Slide-008 recovery judge loop: original-first comparison, one call in flight,
# outer wall 1700s, inner --timeout 1650, up to 8 retries with 300s sleeps.
# Usage: s08_recovery_judge.sh <attempt|verify> <K> [renderK]
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
ROOT=/home/codespace/ai_llm_slides
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
MODE=${1:?attempt|verify}
K=${2:?transcript number}
R=${3:-$K}
QA="$NS/recreated_pptx/qa/slide008"
ORIG="videos/machine-learning/08_performance_measure/unique_slides/slide_008.jpg"
RENDER="videos/machine-learning/08_performance_measure/recreated_pptx/qa/slide008/render_${R}.png"
PROMPT="videos/machine-learning/08_performance_measure/pool_run/judge_prompt_template.txt"
cd "$ROOT"
if [ "$MODE" = attempt ]; then OUT="$QA/judge_attempt_${K}.txt"; else OUT="$QA/judge_verify_${K}.txt"; fi
: > "$OUT"
for i in $(seq 1 8); do
  echo "=== ${MODE} ${K} retry ${i}/8 $(date -u +%FT%TZ) render=videos/machine-learning/08_performance_measure/recreated_pptx/qa/slide008/render_${R}.png ===" >> "$OUT"
  timeout 1700 bash scripts/16_vision_gate.sh "$PY" .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$ORIG" "$RENDER" \
    --thinking high --max-tokens 65536 --timeout 1650 --rounds 1 --tries 1 \
    -p "$(cat "$PROMPT")" >> "$OUT" 2>&1
  rc=$?
  echo "=== ${MODE} ${K} retry ${i} rc=${rc} bytes=$(wc -c < "$OUT") $(date -u +%FT%TZ) ===" >> "$OUT"
  v=$("$PY" "$NS/pool_run/verdict.py" "$OUT")
  echo "verdict so far: $v" >> "$OUT"
  if [ "$v" = PASS ] || [ "$v" = FAIL ]; then
    echo "=== ${MODE} ${K} done verdict=$v after retry ${i} $(date -u +%FT%TZ) ===" >> "$OUT"
    echo "DONE verdict=$v retry=$i"
    exit 0
  fi
  if [ "$i" -lt 8 ]; then sleep 300; fi
done
echo "EXHAUSTED 8 retries, no verdict"
exit 1
