#!/bin/bash
# Attempt-2 retry for crop08/crop09 judges (attempt 1 hit the 340s wall, rc=124).
set -u
S=/home/ahmed/Projects/ai_llm_slides/doc-parse-test/run_20261025-024314
B=$S/11_cascade/slide_057
AI=/home/ahmed/Projects/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
J=$B/judges
CMDS=$S/02_worker_logs/slide_057_cascade_v1_commands.log

retry() { # retry <cropNN_dirname> <box> <class> <strings-list>
  local cid="$1" box="$2" cls="$3" strings="$4"
  local nn=${cid%%_*}; nn=${nn#crop}
  local out=$J/crop${nn}_judge.log err=$J/crop${nn}_judge_stderr.log call=$J/crop${nn}_judge_call.log
  if [ -s "$out" ] && grep -q "FINAL VERDICT" "$out"; then echo "$cid: already banked"; return 0; fi
  local prompt="This is a 3x upscale of crop ${cid} (${cls}, frame box ${box} in 960x540) from slide 057. The doc-parse transcript read the following strings for this crop: ${strings}. For each string: (1) is that text visible in the image? (2) if the visible text differs, what does it actually say? (3) give crop-pixel positions. Also list any clearly visible text the transcript missed. End with FINAL VERDICT: <one line>."
  {
    echo "ATTEMPT: 2 (attempt 1 rc=124, 340s wall) — python3 $AI analysis $B/crops/$cid/crop.png -p \"<prompt below>\" --timeout 380 --rounds 1 --tries 1"
    echo "PROMPT: $prompt"
    echo "STARTED: $(date '+%F %T')"
  } >> "$call"
  echo "$(date '+%F %T') | crop judge crop${nn} ($cid) retry attempt-2 launching, ONE in flight" >> "$CMDS"
  timeout 420 python3 "$AI" analysis "$B/crops/$cid/crop.png" -p "$prompt" --timeout 380 --rounds 1 --tries 1 > "$out" 2> "$err"
  local rc=$?
  echo "EXIT: $rc (attempt 2)" >> "$call"
  echo "FINISHED: $(date '+%F %T') rc=$rc bytes=$(wc -c < "$out")" >> "$call"
  echo "$(date '+%F %T') | crop judge crop${nn} ($cid) retry rc=$rc bytes=$(wc -c < "$out")" >> "$CMDS"
  echo "$cid retry: rc=$rc bytes=$(wc -c < "$out")"
}

retry crop08_ychips_tight "86,97,459,136" "class_Picture" "Yo; Y1; Y2; Y3; Y5; Y6; Yx1; Yx1"
retry crop09_kv_column "443,87,622,433" "class_Picture" "K; Read Forw; Read Forward; Decoder Attention; Encode Decoder Attention"
echo "ALL-RETRIES-DONE"
