#!/bin/bash
# f6_probes.sh — run the pending zone probes (p2, p3, p4) through the vision gate.
cd /home/ahmed/Projects/ai_llm_slides
S=videos/deep-learning/002_transformers_part2/scratch/slide037
AI=.agents/skills/image-analysis/scripts/analyze_image.py
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide037
mkdir -p "$TMPDIR"

probe() {
  local img="$1" view="$2" tr="$3"; shift 3
  for i in 1 2 3; do
    scripts/16_vision_gate.sh timeout 1660 python3 $AI analysis "$img" \
      --view "$view" --capture "Composite: TOP half = ORIGINAL lecture frame zone (slide-space, zoomed); BOTTOM half = certified parent composition render of the same zone. Crop scale noted in the image labels; slide_pt = crop_px/scale + origin." \
      --timeout 1560 --rounds 1 --tries 1 --transcript "$tr" -p "$1"
    rc=$?; echo "[$(date +%H:%M:%S)] $tr rc=$rc"
    [ $rc -eq 0 ] && return 0
    [ $i -lt 3 ] && sleep 90
  done
  return 1
}

P4="Two stacked panels of the SAME slide zone (slide coords x185-660 y225-465, zoom 1.5x: slide_pt = crop_px/1.5 + (185,225)). TOP (green label) = ORIGINAL lecture frame. BOTTOM (red label) = certified parent composition render. Answer about the TOP (original) only, terse and numeric: (1) The red DASHED lines between the two green inset boxes and the architecture panel: how many distinct dashed lines? For EACH line: start point, end point (slide coords), straight or curved. (2) Which element does each line start from (which inset edge/corner) and end at (which target)? (3) Is there a red dashed ROUNDED rectangle (selection-style box) in this zone? Give its bbox and whether corners are rounded. (4) The thin red rectangle around the mauve 'Scaled Dot-Product Attention' box inside the center inset: present? bbox? (5) List any OTHER red marks in TOP that BOTTOM does not have (one line each, bbox)."

P2="Two stacked panels of the SAME slide zone (slide coords x560-905 y95-300, zoom 2x: slide_pt = crop_px/2 + (560,95)). TOP (green label) = ORIGINAL lecture frame. BOTTOM (red label) = certified parent composition render. Answer about the TOP (original) only, terse and numeric: (1) 'Encoder' and 'Decoder' labels: verbatim text, color, italic?, position bbox. (2) The red balloon/map-pin: head circle bbox, tail tip point, the white text verbatim (how many lines, what rotation). (3) A red dashed rounded rectangle: bbox, rounded corners yes/no. (4) The yellow band: bbox. (5) The decoder stack boxes top-to-bottom: fill colors (steel-blue? tan? white?) of Add&Norm / Feed Forward / Add&Norm / Multi-Head Attention. (6) The Softmax and Linear boxes near the top: fill colors. (7) 'Output'/'Probabilities' texts: positions, any red arrow nearby. (8) List every element visible in TOP but ABSENT in BOTTOM (one line each with bbox)."

P3="Two stacked panels of the SAME slide zone (slide coords x560-905 y300-530, zoom 2x: slide_pt = crop_px/2 + (560,300)). TOP (green label) = ORIGINAL lecture frame. BOTTOM (red label) = certified parent composition render. Answer about the TOP (original) only, terse and numeric: (1) The red circle around the encoder Multi-Head Attention area: outer bbox, OUTLINE (ring) or SOLID fill, stroke width, and what is visible INSIDE it. (2) The steel-blue 'Add & Norm' box that BOTTOM shows just above the salmon Multi-Head Attention box: is it visible in TOP, or hidden/covered? (3) The red dashed rounded box: bottom edge y and right edge x (slide coords). (4) V/K/Q circles under the encoder stack: colors and center positions. (5) The 'Positional Encoding' element: box fill color, bbox, icon contents (analog clock? plus-in-circle? sine squiggle?). (6) 'Input Embedding' box and 'Inputs' red arrow: bboxes, colors. (7) The Nx circle left of the encoder stack: fill, text, bbox. (8) Decoder lower area: box fill colors and the purple container. (9) The dashed red curved arrow on the decoder's right side: start and end points. (10) Every element in TOP absent in BOTTOM (one line each, bbox)."

probe $S/probes/p4_funnel.png "slide 037 probe P4: funnel dashes + dashed box, original vs parent" $S/probes/p4_funnel.txt "$P4"
probe $S/probes/p2_arch_top.png "slide 037 probe P2: arch top (pin, labels, dec stack), original vs parent" $S/probes/p2_arch_top.txt "$P2"
probe $S/probes/p3_arch_bottom.png "slide 037 probe P3: arch bottom (ring, V/K/Q, PE, embeds), original vs parent" $S/probes/p3_arch_bottom.txt "$P3"
echo "ALL PROBES DONE"
