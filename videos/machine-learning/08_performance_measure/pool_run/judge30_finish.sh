#!/usr/bin/env bash
# judge30_finish.sh <attempt|verify> <K> <render_png_name> — original-first comparison judge
# for slide 30 through the fleet vision gate. Retries up to 8x on 429/HangError/empty
# (300s backoff), banks judge_attempt_K.txt / judge_verify_K.txt under qa/slide030/.
set -u
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
Q=$NS/recreated_pptx/qa/slide030
KIND=$1
K=$2
RENDER=$Q/$3
OUT=$Q/${KIND}_${K}.txt
PROMPT="$(cat $NS/pool_run/judge_prompt_template.txt)"
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
LOG=$Q/finish_${KIND}_${K}.log

echo "start $(date -u +%FT%TZ) kind=$KIND K=$K render=$3" >> "$LOG"
for i in $(seq 1 8); do
  TRY=$Q/${KIND}_${K}_try$i.txt
  timeout 3000 bash scripts/16_vision_gate.sh $PY \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $NS/unique_slides/slide_030.jpg "$RENDER" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    -p "$PROMPT" > "$TRY" 2>&1
  rc=$?
  echo "--- try $i rc=$rc bytes=$(wc -c < "$TRY") $(date -u +%T)" >> "$LOG"
  if grep -q "FINAL VERDICT" "$TRY"; then
    cp "$TRY" "$OUT"
    echo "VERDICT $(grep -o 'FINAL VERDICT: [A-Z]*' "$TRY" | tail -1) -> $OUT" >> "$LOG"
    exit 0
  fi
  if [ $i -lt 8 ]; then sleep 180; fi
done
echo "NO VERDICT after 8 tries" >> "$LOG"
exit 1
