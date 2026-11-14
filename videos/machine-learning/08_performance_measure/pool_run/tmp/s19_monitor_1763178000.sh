#!/usr/bin/env bash
# Read-only monitor for the live slide-019 judge loop (PID 246461).
# Exits 0 when judge_attempt_6.txt contains FINAL VERDICT or LOOP DONE, or the loop PID is gone.
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
OUT=$NS/recreated_pptx/qa/slide019/judge_attempt_6.txt
LOG=$NS/pool_run/tmp/s19_monitor_1763178000.out
echo "monitor start $(date -u +%FT%TZ) loop_pid=246461" >> "$LOG"
while true; do
  if grep -q 'FINAL VERDICT' "$OUT" 2>/dev/null; then
    echo "VERDICT $(grep -o 'FINAL VERDICT: [A-Z]*' "$OUT" | tail -1) at $(date -u +%FT%TZ)" >> "$LOG"
    exit 0
  fi
  if grep -q 'LOOP DONE' "$OUT" 2>/dev/null; then
    echo "LOOP DONE no verdict at $(date -u +%FT%TZ)" >> "$LOG"
    exit 2
  fi
  if ! kill -0 246461 2>/dev/null; then
    echo "loop pid 246461 gone at $(date -u +%FT%TZ); tail:" >> "$LOG"
    tail -5 "$OUT" >> "$LOG" 2>/dev/null
    exit 3
  fi
  echo "poll $(date -u +%FT%TZ) legs=$(grep -c '=== leg' "$OUT" 2>/dev/null) last=$(tail -1 "$OUT" 2>/dev/null | cut -c1-80)" >> "$LOG"
  sleep 60
done
