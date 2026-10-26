#!/usr/bin/env bash
# Wave-5 crop judges for slide_059 (worker-slide_059_cascade).
# Sequential — ONE judge in flight at a time. Probe ONCE first; on timeout
# wait 60 s and re-probe once. Every judge banks: judge.md (stdout),
# judge_stderr.log, judge_call.log (COMMAND/PROMPT/STARTED/FINISHED/EXIT).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
J="$HERE/judges"
PROG="$J/judges_progress.log"
AI=/home/ahmed/Projects/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
mkdir -p "$J/probe"
: > "$PROG"

log() { echo "[$(date '+%F %T')] $*" | tee -a "$PROG" >&2; }

# ---------------- probe ----------------
probe_cmd() {
  echo "COMMAND: python3 $AI analysis $HERE/crops/crop06_labels_row_l2/crop.png -p \"Reply with exactly: PROBE-OK\""
}
if [ ! -s "$J/probe/probe.md" ]; then
  log "PROBE attempt 1"
  {
    probe_cmd
    echo "STARTED: $(date '+%F %T')"
  } > "$J/probe/probe_call.log"
  echo "PROMPT: Reply with exactly: PROBE-OK" >> "$J/probe/probe_call.log"
  timeout 240 python3 "$AI" analysis "$HERE/crops/crop06_labels_row_l2/crop.png" \
    -p "Reply with exactly: PROBE-OK" \
    > "$J/probe/probe.md" 2> "$J/probe/probe_stderr.log"
  rc=$?
  echo "FINISHED: $(date '+%F %T')" >> "$J/probe/probe_call.log"
  echo "EXIT: $rc" >> "$J/probe/probe_call.log"
  if [ $rc -ne 0 ] || ! grep -q "PROBE-OK" "$J/probe/probe.md" 2>/dev/null; then
    log "PROBE rc=$rc — waiting 60 s, re-probing once"
    sleep 60
    {
      probe_cmd
      echo "RETRY after 60 s wait; attempt 1 exit=$rc"
      echo "STARTED: $(date '+%F %T')"
    } > "$J/probe/probe_call.log"
    echo "PROMPT: Reply with exactly: PROBE-OK" >> "$J/probe/probe_call.log"
    timeout 360 python3 "$AI" analysis "$HERE/crops/crop06_labels_row_l2/crop.png" \
      -p "Reply with exactly: PROBE-OK" \
      > "$J/probe/probe.md" 2> "$J/probe/probe_stderr.log"
    rc=$?
    echo "FINISHED: $(date '+%F %T')" >> "$J/probe/probe_call.log"
    echo "EXIT: $rc" >> "$J/probe/probe_call.log"
  fi
  log "PROBE final rc=$rc"
fi

# ---------------- judges ----------------
# id | png | spec | transcript strings
judge_one() {
  local id="$1" png="$2" spec="$3" strings="$4"
  local out="$J/${id}_judge.md" err="$J/${id}_judge_stderr.log" logf="$J/${id}_judge_call.log"
  if [ -s "$out" ]; then log "SKIP $id (already banked)"; return 0; fi
  local prompt="This is a ${spec} upscale of crop ${id} from slide 059. The doc-parse transcript read the following strings for this crop: ${strings}. For each string: (1) is that text visible in the image? (2) if the visible text differs, what does it actually say? (3) give crop-pixel positions. Also list any clearly visible text the transcript missed. End with FINAL VERDICT: <one line>."
  local attempt rc
  for attempt in 1 2; do
    log "JUDGE $id attempt $attempt"
    {
      echo "COMMAND: python3 $AI analysis $png -p \"<see PROMPT line>\""
      echo "PROMPT: $prompt"
      echo "ATTEMPT: $attempt"
      echo "STARTED: $(date '+%F %T')"
    } > "$logf"
    timeout 900 python3 "$AI" analysis "$png" -p "$prompt" > "$out" 2> "$err"
    rc=$?
    echo "FINISHED: $(date '+%F %T')" >> "$logf"
    echo "EXIT: $rc" >> "$logf"
    if [ $rc -eq 0 ] && [ -s "$out" ]; then
      log "JUDGE $id attempt $attempt OK (exit 0, $(wc -c < "$out") bytes)"
      return 0
    fi
    log "JUDGE $id attempt $attempt FAILED rc=$rc"
    [ $attempt -eq 1 ] && sleep 20
  done
  log "JUDGE $id FINAL FAILURE rc=$rc"
  return 1
}

FAILED=""

# strings lists verbatim from parses/callNN_*/crop.parse.md
judge_one crop01 "$HERE/crops/crop01_softmax_cluster/crop.png" \
  "3x (softmax-circle-cluster, frame box 390,36,655,139 in 960x540)" \
  "ses, IC1, IC2, IC3, Softmax, Σ, Softmax, Σ" || FAILED="$FAILED crop01"

judge_one crop02 "$HERE/crops/crop02_xrow_labels/crop.png" \
  "2x (x-row-token-labels, frame box 168,400,897,452 in 960x540)" \
  "Xl, Xj, X3, X4, Xx, O, XNz, XNd" || FAILED="$FAILED crop02"

judge_one crop03 "$HERE/crops/crop03_yrow_labels/crop.png" \
  "2x (y-row-token-labels, frame box 168,206,897,264 in 960x540)" \
  "Yd, Y2, Y3, Y4, Y5, YNz, YNI" || FAILED="$FAILED crop03"

judge_one crop06 "$HERE/crops/crop06_labels_row_l2/crop.png" \
  "3x (labels-row-l2 of the softmax cluster, frame box 407,47,623,81 in 960x540)" \
  "s, C1, C2, C3" || FAILED="$FAILED crop06"

judge_one crop07 "$HERE/crops/crop07_circles_l2/crop.png" \
  "3x (circles-l2 of the softmax cluster, frame box 401,83,634,142 in 960x540)" \
  "Softmax, Z, Softmax, Z" || FAILED="$FAILED crop07"

judge_one crop08 "$HERE/crops/crop08_xrow_left_l2/crop.png" \
  "3x (x-row-left-l2, frame box 184,400,481,452 in 960x540)" \
  "X0, X3, X2, X3" || FAILED="$FAILED crop08"

judge_one crop09 "$HERE/crops/crop09_xrow_tail_l2/crop.png" \
  "3x (x-row-tail-l2, frame box 548,400,882,452 in 960x540)" \
  "X, XN, XNd" || FAILED="$FAILED crop09"

judge_one crop10 "$HERE/crops/crop10_yrow_left_l2/crop.png" \
  "3x (y-row-left-l2, frame box 184,206,481,264 in 960x540)" \
  "Y_d, 1, Y_i, 1, Y2, 1, Y_i" || FAILED="$FAILED crop10"

judge_one crop11 "$HERE/crops/crop11_yrow_tail_l2/crop.png" \
  "3x (y-row-tail-l2, frame box 548,206,882,264 in 960x540)" \
  "Y, Y N-2, YN-1" || FAILED="$FAILED crop11"

judge_one crop12 "$HERE/crops/crop12_annot_lower_l2/crop.png" \
  "2x (annot-lower-l2 of the left annotation column, frame box 41,312,309,533 in 960x540)" \
  "a ranked_table chart block titled 'Input Sequence' with rows 'Word Embedding Vectors | X0 | X' and 'Position Information Vectors | Vector_PO | Vector_PI'" \
  || FAILED="$FAILED crop12"

judge_one crop13 "$HERE/crops/crop13_xtail_l3/crop.png" \
  "3x (x-tail-l3, frame box 709,400,876,452 in 960x540)" \
  "XN2, XN4" || FAILED="$FAILED crop13"

judge_one crop14 "$HERE/crops/crop14_yleft_tight_l3/crop.png" \
  "3x (y-left-tight-l3, frame box 189,206,351,264 in 960x540)" \
  "Y_d, ☐, Y_d, ☐ (Y_d followed by an empty-box glyph, twice)" || FAILED="$FAILED crop14"

judge_one crop15 "$HERE/crops/crop15_x12_zone_l3/crop.png" \
  "3x (x12-zone-l3, frame box 494,400,656,452 in 960x540)" \
  "X2, X3" || FAILED="$FAILED crop15"

judge_one crop16 "$HERE/crops/crop16_annot_table_l3/crop.png" \
  "2x (annot-table-l3 of the left annotation column, frame box 41,369,309,526 in 960x540)" \
  "Input Sequence, Word Embedding Vectors, X0, X1, Position Information Vectors, Vector PO, Vector PI" \
  || FAILED="$FAILED crop16"

log "ALL JUDGES DONE. failed:${FAILED:- none}"
