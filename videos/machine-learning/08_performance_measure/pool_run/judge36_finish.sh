#!/usr/bin/env bash
# judge36_finish.sh <attempt|verify> <K> <render_png_name> — original-first comparison
# judge for slide 36, ONE call in flight, wide walls (outer 1700s / inner 1650s),
# up to 8 tries with 300s backoff until a FINAL VERDICT exists.
# Banks recreated_pptx/qa/slide036/judge_attempt_K.txt / judge_verify_K.txt.
set -u
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
Q=$NS/recreated_pptx/qa/slide036
KIND=$1
K=$2
RENDER=$Q/$3
OUT=$Q/judge_${KIND}_${K}.txt
PROMPT="$(cat $NS/pool_run/judge_prompt_template.txt)"
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
LOG=$Q/finish36_${KIND}_${K}.log

echo "start $(date -u +%FT%TZ) kind=$KIND K=$K render=$3" >> "$LOG"
for i in $(seq 1 8); do
  TRY=$Q/judge_${KIND}_${K}_try$i.txt
  timeout 1700 bash scripts/16_vision_gate.sh $PY \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $NS/unique_slides/slide_036.jpg "$RENDER" \
    --thinking high --max-tokens 65536 --timeout 1650 --rounds 1 --tries 1 \
    -p "$PROMPT" > "$TRY" 2>&1
  rc=$?
  echo "--- try $i rc=$rc bytes=$(wc -c < "$TRY") $(date -u +%FT%TZ)" >> "$LOG"
  if grep -q "FINAL VERDICT" "$TRY"; then
    cp "$TRY" "$OUT"
    echo "VERDICT $(grep -o 'FINAL VERDICT: [A-Z]*' "$TRY" | tail -1) -> $OUT $(date -u +%FT%TZ)" >> "$LOG"
    exit 0
  fi
  if [ $i -lt 8 ]; then sleep 300; fi
done
echo "NO VERDICT after 8 tries $(date -u +%FT%TZ)" >> "$LOG"
exit 1
