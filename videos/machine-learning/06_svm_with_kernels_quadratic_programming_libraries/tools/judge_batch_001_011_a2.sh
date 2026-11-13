#!/usr/bin/env bash
# Attempt-2 judge re-run for slides with NO_VERDICT on attempt 1.
set -u
cd /home/codespace/ai_llm_slides
export IR_API_KEY="$(cat /home/codespace/nvidia/.keys/ironrouter.key)"
V=videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries
TEMPLATE="$V/judge_prompt_active.txt"
LEDGER="$V/qa/rejudge2/ledger.jsonl"
for n in 002 003 004 006 007 008 009 010 011; do
  N=$((10#$n))
  R="$V/recreated_pptx/qa/slide$n/render_1.png"
  O="$V/unique_slides/slide_$n.jpg"
  T="$V/recreated_pptx/qa/slide$n/judge_attempt_2.txt"
  P="$V/recreated_pptx/qa/slide$n/judge_prompt_2.txt"
  cp "$TEMPLATE" "$P"
  echo "=== judging $n attempt 2 ==="
  scripts/16_vision_gate.sh timeout 540 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$R" "$O" \
    --view "Slide $n recreation — fidelity check vs original lecture frame" \
    --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
    --thinking high --max-tokens 65536 \
    --timeout 420 --rounds 1 --tries 1 \
    --transcript "$T" \
    -p "$(cat "$P")" > "$V/recreated_pptx/qa/slide$n/judge_stdout_2.txt" 2>&1
  rc=$?
  verdict=$(grep -o 'FINAL VERDICT: [A-Z]*' "$T" 2>/dev/null | tail -1)
  [ -z "$verdict" ] && verdict="NO_VERDICT(rc=$rc)"
  md5=$(md5sum "$V/recreated_pptx/slide_${n}_recreated.pptx" | cut -d' ' -f1)
  printf '{"slide": %s, "attempt": 2, "verdict": "%s", "pptx_md5": "%s", "transcript": "%s"}\n' \
    "$N" "$verdict" "$md5" "$T" >> "$LEDGER"
  echo "$n -> $verdict"
done
echo "ALL DONE A2"
