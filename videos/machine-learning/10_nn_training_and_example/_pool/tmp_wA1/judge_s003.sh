set -u
cd /home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
PROMPT="$(cat judge_template.txt)"
RENDER="recreated_pptx/qa/slide003/render-1.png"
OUT="recreated_pptx/qa/slide003/judge_attempt_1.txt"
LOG=_pool/tmp_wA1/judge_s003.log; : > "$LOG"
for k in 1 2 3; do
  echo "s003 attempt $k START $(date -u +%T)" >> "$LOG"
  env VISION_SLOTS=2 bash _pool/vision_gate.sh \
    python3 -u /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
    comparison "$RENDER" "unique_slides/slide_003.jpg" \
    --view "Slide 003: image 1 = recreation render, image 2 = original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs original frame" \
    -p "$PROMPT" --timeout 780 --rounds 1 --tries 1 --max-tokens 24000 \
    > "$OUT" 2>&1
  echo "s003 attempt $k rc=$? $(date -u +%T) bytes=$(wc -c < "$OUT")" >> "$LOG"
  grep -q 'FINAL VERDICT' "$OUT" && { echo "VERDICT: $(grep 'FINAL VERDICT' "$OUT" | tail -1)" >> "$LOG"; exit 0; }
  grep -qE 'HTTP 429|HTTP 5|HangError|Connection reset|every model failed|upstream' "$OUT" && { echo "storm-sleep180" >> "$LOG"; sleep 180; continue; }
  echo "no-verdict" >> "$LOG"; exit 1
done
exit 1
