#!/usr/bin/env bash
# driver.sh — storm-resilient sequential probe dispatcher.
# For each crop: dispatch through the gate; if no transcript lands, sleep 120 and retry (max 4 dispatches).
set -u
cd /home/ahmed/Projects/ai_llm_slides
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide051/tmp
mkdir -p "$TMPDIR"
SK=.agents/skills/image-analysis/scripts/analyze_image.py
SCRATCH=videos/deep-learning/002_transformers_part2/scratch/slide051
CAP="2x-zoomed crop (LANCZOS) from a 960x540 lecture video frame of a 13.33x7.5in PowerPoint slide (video capture ~0.96 scale); slide body content"
P="This is a zoomed crop from a lecture slide (transformer architecture diagram redrawn by the instructor). Inventory EVERY visual element precisely: for each, give (1) kind: text label / filled rectangle / rounded rectangle / block arrow (state direction) / circle / checkmark glyph / dashed ellipse / connector line; (2) EXACT verbatim text if any (character-accurate; note subscript/superscript); (3) fill color and text color as approx hex; (4) rough bounds within the CROP as percentages (left,top,right,bottom). Note layering (what overlaps what). Be exhaustive - include small glyphs, thin lines, partial shapes at crop edges. Do not guess text: if text is illegible write ILLEGIBLE(<what you see>)."

run_one() { # $1 crop, $2 view
  local c="$1" v="$2"
  scripts/16_vision_gate.sh timeout 480 python3 "$SK" analysis "$SCRATCH/crops/$c.png" \
    --view "$v" --capture "$CAP" --timeout 380 --rounds 1 --tries 1 \
    --transcript "$SCRATCH/probes/$c.txt" -p "$P" > "$SCRATCH/probes/$c.stdout" 2>&1
}

declare -A VIEWS
VIEWS[enc_stack]="slide 051 encoder stack zone: yellow box + stack container + boxes + red shapes + QKV circles"
VIEWS[enc_lower]="slide 051 encoder lower: positional encoding icon + label + red and green marks"
VIEWS[enc_bottom]="slide 051 encoder bottom: Output Embedding box + side text lines + red arrow + labels"
VIEWS[dec_top]="slide 051 decoder top: yellow Output box, red arrow, labels, teal Softmax/Linear boxes + dashed ellipses"
VIEWS[dec_stacktop]="slide 051 decoder stack container top: dark block, gray box, yellow bar, blue boxes"
VIEWS[dec_stackbot]="slide 051 decoder stack container bottom: blue box, purple box, circles"
VIEWS[dec_bottom]="slide 051 decoder bottom: brown Output Embedding, texts, yellow box"
VIEWS[callout34]="slide 051 decoder callouts 3+4: white boxes, red text, block arrows"
VIEWS[title]="slide 051 title band: red title text"

ORDER=(enc_stack enc_lower enc_bottom dec_top dec_stacktop dec_stackbot dec_bottom callout34 title)

for round in 1 2 3 4; do
  pending=0
  for c in "${ORDER[@]}"; do
    [ -s "$SCRATCH/probes/$c.txt" ] && continue
    pending=1
    echo "[driver] round $round dispatch $c at $(date +%H:%M:%S)"
    run_one "$c" "${VIEWS[$c]}" &
    WP=$!
    wait $WP
    if [ -s "$SCRATCH/probes/$c.txt" ]; then
      echo "[driver] OK $c ($(wc -c < "$SCRATCH/probes/$c.txt") bytes)"
    else
      echo "[driver] MISS $c rc=$? — backoff 120s"
      sleep 120
    fi
    sleep 20
  done
  [ $pending -eq 0 ] && break
done
echo "[driver] done: $(ls "$SCRATCH/probes"/*.txt 2>/dev/null | wc -l) transcripts banked"
