#!/bin/bash
# Wave-5 cascade crop judges — content-anchored, ONE in flight, banked call logs.
set -u
S=/home/ahmed/Projects/ai_llm_slides/doc-parse-test/run_20261025-024314
B=$S/11_cascade/slide_057
AI=/home/ahmed/Projects/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
J=$B/judges
CMDS=$S/02_worker_logs/slide_057_cascade_v1_commands.log
mkdir -p "$J"

judge() { # judge <cropNN_dirname> <box> <class> <strings-list>
  local cid="$1" box="$2" cls="$3" strings="$4"
  local nn=${cid%%_*}; nn=${nn#crop}
  local out=$J/crop${nn}_judge.log err=$J/crop${nn}_judge_stderr.log call=$J/crop${nn}_judge_call.log
  if [ -s "$out" ] && grep -q "FINAL VERDICT" "$out"; then echo "$cid: already banked"; return 0; fi
  local prompt="This is a 3x upscale of crop ${cid} (${cls}, frame box ${box} in 960x540) from slide 057. The doc-parse transcript read the following strings for this crop: ${strings}. For each string: (1) is that text visible in the image? (2) if the visible text differs, what does it actually say? (3) give crop-pixel positions. Also list any clearly visible text the transcript missed. End with FINAL VERDICT: <one line>."
  {
    echo "COMMAND: python3 $AI analysis $B/crops/$cid/crop.png -p \"<prompt see PROMPT below>\" --timeout 300 --rounds 1 --tries 1 > judges/crop${nn}_judge.log 2> judges/crop${nn}_judge_stderr.log"
    echo "PROMPT: $prompt"
    echo "STARTED: $(date '+%F %T')"
  } > "$call"
  echo "$(date '+%F %T') | crop judge crop${nn} ($cid) launching, ONE in flight" >> "$CMDS"
  timeout 340 python3 "$AI" analysis "$B/crops/$cid/crop.png" -p "$prompt" --timeout 300 --rounds 1 --tries 1 > "$out" 2> "$err"
  local rc=$?
  echo "EXIT: $rc" >> "$call"
  echo "FINISHED: $(date '+%F %T') rc=$rc bytes=$(wc -c < "$out")" >> "$call"
  echo "$(date '+%F %T') | crop judge crop${nn} ($cid) rc=$rc bytes=$(wc -c < "$out")" >> "$CMDS"
  echo "$cid: rc=$rc bytes=$(wc -c < "$out")"
}

judge crop01_enc_top_ychips_bars "86,89,462,241" "class_Picture" "Encoder Block M"
judge crop02_enc_bottom_emb "86,406,462,522" "class_Chart" "Word Embedding; Positional Encoding / Embedding; Word 0; Word 1; Word 2; Word 3; Word 4; Word 5; Word N2"
judge crop05_dec_top_bars_attn "569,49,871,356" "class_Picture" "Encode Decoder Attention; Feed Forward Networks [ One Hidden with RELU Activation; Residual Connection and Layer Normalization"
judge crop06_dec_bottom_tokens "569,395,871,525" "class_Picture" "Multi-Head Self Attention; Word and Position Encoding; Residual Connection and Layer Normalization"
judge crop08_ychips_tight "86,97,459,136" "class_Picture" "Yo; Y1; Y2; Y3; Y5; Y6; Yx1; Yx1"
judge crop09_kv_column "443,87,622,433" "class_Picture" "K; Read Forw; Read Forward; Decoder Attention; Encode Decoder Attention"
echo "ALL-JUDGES-DONE"
