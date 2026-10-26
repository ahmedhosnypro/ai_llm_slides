#!/bin/bash
# Round-1 crop parses — slide_059_vj (wave-4). One call dir per parse; retries into fresh dirs.
set -u
RUN=/home/ahmed/Projects/ai_llm_slides/doc-parse-test/run_20261025-024314
VJ=$RUN/10_visual_judge/slide_059
LOG=$RUN/02_worker_logs/slide_059_commands.log
PARSER=$HOME/.agents/skills/doc-parse/scripts/parse_document.py

check_ok() {  # $1 = call dir -> prints OK if finish stop + non-empty content
  python3 - "$1" <<'PYEOF'
import json, sys, os
cd = sys.argv[1]
js = [f for f in os.listdir(cd) if f.endswith(".parse.json")]
if not js:
    print("FAIL"); raise SystemExit
j = json.load(open(os.path.join(cd, js[0])))
c = j.get("content") or ""
print("OK" if (j.get("finish_reason") == "stop" and isinstance(c, str) and c.strip()) else "FAIL")
PYEOF
}

run_parse() {  # $1 = call-dir path, $2 = crop png path
  local CD="$1" IMG="$2"
  local CMD="python3 $PARSER $IMG -o $CD --max-output-tokens 3000 --timeout 300"
  { echo "COMMAND: $CMD"; echo "STARTED: $(date '+%F %T')"; } > "$CD/call.log"
  eval "$CMD" > "$CD/stdout.log" 2> "$CD/stderr.log"
  local RC=$?
  { echo "FINISHED: $(date '+%F %T')"; echo "EXIT: $RC"; } >> "$CD/call.log"
  echo "$(date '+%F %T') | parse $(basename $CD) rc=$RC | exit=$?" >> "$LOG"
  echo $RC
}

for SPEC in "call01_round1:crop01_softmax_cluster" "call02_round1:crop02_xrow_labels" "call03_round1:crop03_yrow_labels" "call04_round1:crop04_pooled_row"; do
  CDNAME="${SPEC%%:*}"; STEM="${SPEC##*:}"
  IMG="$VJ/crops/round1/$STEM.png"
  BASE="$VJ/parses/$CDNAME"
  ATTEMPT=1
  while [ $ATTEMPT -le 3 ]; do
    if [ $ATTEMPT -eq 1 ]; then CD="$BASE"; else CD="${BASE}_retry$ATTEMPT"; fi
    mkdir -p "$CD"
    RC=$(run_parse "$CD" "$IMG")
    if [ "$RC" -eq 0 ] && [ "$(check_ok "$CD")" = "OK" ]; then
      echo "$(date '+%F %T') | $CDNAME attempt $ATTEMPT OK | exit=0" >> "$LOG"
      break
    fi
    if grep -qE '(429|500|502|503|504|Server Error|ServiceUnavailable|Too Many Requests)' "$CD/stdout.log" "$CD/stderr.log" 2>/dev/null; then
      echo "$(date '+%F %T') | $CDNAME attempt $ATTEMPT HTTP error -> sleep 60 | exit=0" >> "$LOG"
      sleep 60
    fi
    ATTEMPT=$((ATTEMPT+1))
  done
done
echo "ROUND1 PARSES DONE $(date '+%F %T')"
