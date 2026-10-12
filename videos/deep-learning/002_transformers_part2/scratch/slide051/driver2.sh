#!/usr/bin/env bash
# driver2.sh — storm driver v2: 2 lanes, tighter walls, priority order, 4 rounds.
set -u
cd /home/ahmed/Projects/ai_llm_slides
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide051/tmp
mkdir -p "$TMPDIR"
SK=.agents/skills/image-analysis/scripts/analyze_image.py
SCRATCH=videos/deep-learning/002_transformers_part2/scratch/slide051
CAP="2x-zoomed crop (LANCZOS) from a 960x540 lecture video frame of a 13.33x7.5in PowerPoint slide (video capture ~0.96 scale); slide body content"
P="This is a zoomed crop from a lecture slide (transformer architecture diagram redrawn by the instructor). Inventory EVERY visual element precisely: for each, give (1) kind: text label / filled rectangle / rounded rectangle / block arrow (state direction) / circle / checkmark glyph / dashed ellipse / connector line; (2) EXACT verbatim text if any (character-accurate; note subscript/superscript); (3) fill color and text color as approx hex; (4) rough bounds within the CROP as percentages (left,top,right,bottom). Note layering (what overlaps what). Be exhaustive - include small glyphs, thin lines, partial shapes at crop edges. Do not guess text: if text is illegible write ILLEGIBLE(<what you see>)."

declare -A VIEWS
VIEWS[title]="slide 051 title band: red title text verbatim"
VIEWS[dec_top]="slide 051 decoder top: yellow Output box, red arrow, labels, teal Softmax/Linear boxes + dashed ellipses"
VIEWS[dec_bottom]="slide 051 decoder bottom: brown Output Embedding, texts, yellow box"
VIEWS[callout34]="slide 051 decoder callouts 3+4: white boxes, red text, block arrows"
VIEWS[enc_bottom]="slide 051 encoder bottom: Output Embedding box + side text lines + red arrow + labels"
VIEWS[dec_stacktop]="slide 051 decoder stack container top: dark block, gray box, yellow bar, blue boxes"
VIEWS[dec_stackbot]="slide 051 decoder stack container bottom: blue box, purple box, circles"
VIEWS[enc_stack]="slide 051 encoder stack zone: yellow box + stack container + boxes + red shapes + QKV circles"
VIEWS[enc_lower]="slide 051 encoder lower: positional encoding icon + label + red and green marks"
ORDER=(title dec_top dec_bottom callout34 enc_bottom dec_stacktop dec_stackbot enc_stack enc_lower)

run_one() {
  local c="$1"
  scripts/16_vision_gate.sh timeout 280 python3 "$SK" analysis "$SCRATCH/crops/$c.png" \
    --view "${VIEWS[$c]}" --capture "$CAP" --timeout 200 --rounds 1 --tries 1 \
    --transcript "$SCRATCH/probes/$c.txt" -p "$P" > "$SCRATCH/probes/$c.stdout" 2>&1
}

lane() { # $1 = lane offset (0/1): take every 2nd pending crop
  local off=$1
  for round in 1 2 3 4 5; do
    for ((i = off; i < ${#ORDER[@]}; i += 2)); do
      c=${ORDER[$i]}
      [ -s "$SCRATCH/probes/$c.txt" ] && continue
      echo "[lane$off] r$round $c $(date +%H:%M:%S)"
      run_one "$c" &
      local wp=$!; wait $wp
      if [ -s "$SCRATCH/probes/$c.txt" ]; then
        echo "[lane$off] OK $c ($(wc -c < "$SCRATCH/probes/$c.txt")B)"
      else
        echo "[lane$off] MISS $c — backoff 120s"; sleep 120
      fi
      sleep 15
    done
    local left=0
    for c in "${ORDER[@]}"; do [ -s "$SCRATCH/probes/$c.txt" ] || left=1; done
    [ $left -eq 0 ] && break
  done
}

lane 0 &
L1=$!
sleep 8
lane 1 &
L2=$!
wait $L1 $L2
echo "[driver2] done: $(ls "$SCRATCH/probes"/*.txt 2>/dev/null | wc -l) transcripts banked"
