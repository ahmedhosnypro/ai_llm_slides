#!/usr/bin/env bash
# run_cropchecks.sh — dense-region crop comparisons through the vision gate.
# Pattern: dense-region-crop-compare. Full judge params. Dispatch walls: <=2 concurrent
# per lane, ~15s spacing. Inner timeout 280 > script wall 270 (--timeout 240+30).
set -u
cd /home/ahmed/Projects/ai_llm_slides
QA=videos/deep-learning/001_introduction/recreated_pptx/qa/slide035
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/slide035
PAYLOAD="$QA/judge_p_payload_1.txt"

run_cmp () {
  local name="$1" rcrop="$2" ocrop="$3" view="$4"
  timeout 1700 scripts/16_vision_gate.sh timeout 280 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$rcrop" "$ocrop" \
    --view "$view" \
    --capture "IMG1=zoomed crop of the 150dpi render; IMG2=same region cropped from the original lecture frame (ground truth)" \
    --thinking high --max-tokens 65536 \
    --timeout 240 --rounds 1 --tries 1 \
    --transcript "$QA/cropcheck_${name}.txt" \
    -p "$(cat "$PAYLOAD")"
}

run_cmp A_filter_grid "$QA/crop_render_A_filter_grid.png" "$QA/crop_orig_A_filter_grid.png" \
  "Slide 035 dense region A — Filter 3x3 yellow grid: cell values, borders, digit rendering" &
P1=$!
sleep 15
run_cmp B_panel_yellow3x3 "$QA/crop_render_B_panel_yellow3x3.png" "$QA/crop_orig_B_panel_yellow3x3.png" \
  "Slide 035 dense region B — computation panel top: 5x5 grid's yellow 3x3 with tiny red x1/x0 multipliers and row-1 digits" &
P2=$!
wait $P1 $P2
sleep 15
run_cmp C_caption_l2 "$QA/crop_render_C_caption_l2.png" "$QA/crop_orig_C_caption_l2.png" \
  "Slide 035 dense region C — caption line 2: paren colors, red bold span, underlined PERCEPTRON" &
wait $!
echo "ALL_CROPCHECKS_DONE"
