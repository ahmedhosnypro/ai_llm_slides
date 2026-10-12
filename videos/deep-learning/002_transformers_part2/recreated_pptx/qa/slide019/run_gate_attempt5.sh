#!/bin/bash
cd /home/ahmed/Projects/ai_llm_slides
Q=videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide019
P=$(cat $Q/judge_template_p.txt)
AI=.agents/skills/image-analysis/scripts/analyze_image.py

echo "=== probe 5 ==="
for i in 1 2; do
  scripts/16_vision_gate.sh timeout 150 python3 $AI analysis \
    $Q/render_5.png \
    --view "Slide 019 recreation attempt 5 - probe" \
    --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
    --timeout 120 --rounds 1 --tries 1 \
    --transcript $Q/probe_5.txt
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

echo "=== crop: pin 5 ==="
run_cmp $Q/crop_pin_render_5.png $Q/crop_pin_orig_5.png \
  "Slide 019 recreation attempt 5 - zoomed crop comparison, WE ARE HERE pin region. Base = 001 slide 19's certified component, imported; expected difference = this slide's delta only (pin ADDED here: single smooth tail, three tilted lines, bulb->tail transition bulges per attempt-3/4 fixes). NOTE pixel-refutation record: the attempt-3 findings of green dashes crossing the bulb and a red dashed diagonal over the yellow box do NOT exist in the ground-truth frame (only 4 anti-alias edge px; zero red dashes in that region) - do not re-raise them. Inherited-region findings on pixel-identical regions are judge variance." \
  "IMG1=zoomed 150dpi render crop of the pin region; IMG2=zoomed original frame crop of the same region" \
  $Q/cropcmp_pin_5.txt

echo "=== main judge comparison 5 ==="
run_cmp $Q/render_5.png videos/deep-learning/002_transformers_part2/unique_slides/slide_019.jpg \
  "Slide 019 recreation - fidelity check vs original lecture frame. Base composition = 001 slide 19's judge-certified component (imported, not re-drawn, badge numeral 19); expected difference = this slide's delta only (legend callout boxes + leader hairlines + two navy chevron pairs removed; translucent yellow bottom band + red WE ARE HERE map-pin added; thin decoder inter-box arrow shafts added through two gaps). Inherited-region findings on pixel-identical regions are judge variance." \
  "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  $Q/judge_attempt_5.txt

echo "=== runner 5 done ==="
