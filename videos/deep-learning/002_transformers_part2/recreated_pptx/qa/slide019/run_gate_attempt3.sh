#!/bin/bash
cd /home/ahmed/Projects/ai_llm_slides
Q=videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide019
P=$(cat $Q/judge_template_p.txt)
AI=.agents/skills/image-analysis/scripts/analyze_image.py

echo "=== probe 3 ==="
for i in 1 2; do
  scripts/16_vision_gate.sh timeout 150 python3 $AI analysis \
    $Q/render_3.png \
    --view "Slide 019 recreation attempt 3 - probe" \
    --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
    --timeout 120 --rounds 1 --tries 1 \
    --transcript $Q/probe_3.txt
  rc=$?; echo "probe rc=$rc"; [ $rc -eq 0 ] && break; [ $i -eq 1 ] && sleep 300
done

run_cmp() {
  local img1="$1" img2="$2" view="$3" cap="$4" tr="$5"
  for i in 1 2 3; do
    scripts/16_vision_gate.sh timeout 540 python3 $AI comparison "$img1" "$img2" \
      --view "$view" --capture "$cap" \
      --thinking high --max-tokens 65536 \
      --timeout 420 --rounds 1 --tries 1 \
      --transcript "$tr" -p "$P"
    rc=$?; echo "cmp($tr) try $i rc=$rc"; [ $rc -eq 0 ] && return 0; [ $i -lt 3 ] && sleep 120
  done
  return 1
}

echo "=== crop: pin 3 ==="
run_cmp $Q/crop_pin_render_3.png $Q/crop_pin_orig_3.png \
  "Slide 019 recreation attempt 3 - zoomed crop comparison, WE ARE HERE pin region. Base = 001 slide 19's certified component, imported; expected difference = this slide's delta only (pin ADDED here, now single smooth tail + three tilted text lines per attempt-2 fix). Inherited-region findings on pixel-identical regions are judge variance." \
  "IMG1=zoomed 150dpi render crop of the pin region; IMG2=zoomed original frame crop of the same region" \
  $Q/cropcmp_pin_3.txt

echo "=== crop: chevron zones 3 ==="
run_cmp $Q/crop_chev_render_3.png $Q/crop_chev_orig_3.png \
  "Slide 019 recreation attempt 3 - zoomed crop comparison, decoder stack zones. Base = 001 slide 19's certified component, imported; expected difference = this slide's delta only (two navy chevron pairs absent here; thin dark inter-box arrow shafts ADDED through both gaps per attempt-2 fix; lowest chevron pair present). Inherited-region findings on pixel-identical regions are judge variance." \
  "IMG1=zoomed 150dpi render crop of the decoder stack; IMG2=zoomed original frame crop of the same region" \
  $Q/cropcmp_chev_3.txt

echo "=== main judge comparison 3 ==="
run_cmp $Q/render_3.png videos/deep-learning/002_transformers_part2/unique_slides/slide_019.jpg \
  "Slide 019 recreation - fidelity check vs original lecture frame. Base composition = 001 slide 19's judge-certified component (imported, not re-drawn, badge numeral 19); expected difference = this slide's delta only (legend callout boxes + leader hairlines + two navy chevron pairs removed; translucent yellow bottom band + red WE ARE HERE map-pin added; thin decoder inter-box arrow shafts added through two gaps). Inherited-region findings on pixel-identical regions are judge variance." \
  "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  $Q/judge_attempt_3.txt

echo "=== runner 3 done ==="
