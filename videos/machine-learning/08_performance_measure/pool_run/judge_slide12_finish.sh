#!/bin/bash
# FINISH_BRIEF judge loop for slide 012 (08_performance_measure).
# Usage: judge_slide12_finish.sh <attempt_K> <transcript_name>   (original-first comparison)
# Runs from repo root; all writes stay inside the namespace.
cd /home/codespace/ai_llm_slides || exit 1
NS=videos/machine-learning/08_performance_measure
K=$1
OUTNAME=$2
OUT="$NS/recreated_pptx/qa/slide012/${OUTNAME}"
TMP="$NS/pool_run/.judge_s12_${OUTNAME}.tmp"
PROMPT=$(cat "$NS/pool_run/judge_prompt_template.txt")
RENDER="$NS/recreated_pptx/qa/slide012/render_${K}.png"
mkdir -p "$NS/recreated_pptx/qa/slide012"

echo "=== slide12 ${OUTNAME} start $(date -u +%FT%TZ) render=${RENDER} ===" | tee -a "$OUT"
for i in $(seq 1 8); do
  echo "=== ${OUTNAME} try $i/8 $(date -u +%FT%TZ) ===" | tee -a "$OUT"
  timeout 540 bash scripts/16_vision_gate.sh \
    python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$NS/unique_slides/slide_012.jpg" \
    "$RENDER" \
    --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 \
    -p "$PROMPT" > "$TMP" 2>&1
  rc=$?
  cat "$TMP" >> "$OUT"
  echo "=== ${OUTNAME} try $i rc=$rc bytes=$(wc -c < "$TMP") $(date -u +%FT%TZ) ===" | tee -a "$OUT"
  if grep -q 'FINAL VERDICT:' "$TMP" && ! grep -qiE '429|HangError|RateLimit' "$TMP"; then
    echo "[judge_s12 ${OUTNAME}] FINAL VERDICT obtained on try $i" | tee -a "$OUT"
    break
  fi
  if [ "$i" -lt 8 ]; then
    echo "[judge_s12 ${OUTNAME}] try $i unusable; sleeping 300s" | tee -a "$OUT"
    sleep 300
  fi
done
rm -f "$TMP"
echo "=== slide12 ${OUTNAME} done $(date -u +%FT%TZ) verdict: $(grep -a 'FINAL VERDICT' "$OUT" | tail -1) ===" | tee -a "$OUT"
