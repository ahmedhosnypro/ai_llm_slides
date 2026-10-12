#!/usr/bin/env bash
# probe_pair.sh <crop1> <view1> <crop2> <view2> — dispatch 2 analysis probes through the gate
set -u
cd /home/ahmed/Projects/ai_llm_slides
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide051/tmp
mkdir -p "$TMPDIR"
SK=.agents/skills/image-analysis/scripts/analyze_image.py
SCRATCH=videos/deep-learning/002_transformers_part2/scratch/slide051
CAP="2x-zoomed crop (LANCZOS) from a 960x540 lecture video frame of a 13.33x7.5in PowerPoint slide (video capture ~0.96 scale); slide body content"
P="This is a zoomed crop from a lecture slide (transformer architecture diagram redrawn by the instructor). Inventory EVERY visual element precisely: for each, give (1) kind: text label / filled rectangle / rounded rectangle / block arrow (state direction) / circle / checkmark glyph / dashed ellipse / connector line; (2) EXACT verbatim text if any (character-accurate; note subscript/superscript); (3) fill color and text color as approx hex; (4) rough bounds within the CROP as percentages (left,top,right,bottom). Note layering (what overlaps what). Be exhaustive - include small glyphs, thin lines, partial shapes at crop edges. Do not guess text: if text is illegible write ILLEGIBLE(<what you see>)."
c1="$1"; v1="$2"; c2="$3"; v2="$4"
scripts/16_vision_gate.sh timeout 300 python3 "$SK" analysis "$SCRATCH/crops/$c1.png" \
  --view "$v1" --capture "$CAP" --timeout 240 --rounds 1 --tries 1 \
  --transcript "$SCRATCH/probes/${c1%.png}.txt" -p "$P" > "$SCRATCH/probes/${c1%.png}.stdout" 2>&1 &
P1=$!
sleep 15
scripts/16_vision_gate.sh timeout 300 python3 "$SK" analysis "$SCRATCH/crops/$c2.png" \
  --view "$v2" --capture "$CAP" --timeout 240 --rounds 1 --tries 1 \
  --transcript "$SCRATCH/probes/${c2%.png}.txt" -p "$P" > "$SCRATCH/probes/${c2%.png}.stdout" 2>&1 &
P2=$!
wait $P1 $P2
echo "== $c1 =="; tail -c 400 "$SCRATCH/probes/${c1%.png}.stdout"
echo; echo "== $c2 =="; tail -c 400 "$SCRATCH/probes/${c2%.png}.stdout"
