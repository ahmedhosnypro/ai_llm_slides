#!/usr/bin/env bash
# Crop comparisons (4 dense regions) + probe, through the fleet vision gate.
set -u
cd /home/ahmed/Projects/ai_llm_slides
export TMPDIR=$PWD/videos/deep-learning/002_transformers_part2/scratch/slide031
Q=videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide031
TPL=$PWD/$Q/judge_template.txt

echo "=== PROBE $(date +%T) ==="
scripts/16_vision_gate.sh timeout 150 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py analysis \
  $Q/render_1.png \
  --view "Slide 031 recreation attempt 1 — probe" \
  --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
  --timeout 120 --rounds 1 --tries 1 \
  --transcript $Q/probe_1.txt
echo "probe exit=$? $(date +%T)"

run_cmp () {
  local name=$1 render=$2 orig=$3 view=$4
  echo "=== CROP $name $(date +%T) ==="
  scripts/16_vision_gate.sh timeout 1650 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$render" "$orig" \
    --view "$view" \
    --capture "IMG1=150dpi-render crop (same region, same scale as IMG2); IMG2=original lecture frame crop resampled to the same scale" \
    --thinking high --max-tokens 65536 \
    --timeout 600 --rounds 1 --tries 1 \
    --transcript "$Q/cropcmp_${name}.txt" \
    -p "$(cat "$TPL")"
  echo "crop $name exit=$? $(date +%T)"
}

run_cmp topband $Q/crops/topband_render.png $Q/crops/topband_orig.png \
  "Dense-region zoom check: TOP BAND (left mint 'Vector at Pos t' panel + middle cream 'Vector at Pos t+delta' panel, x55..690 y40..220 of the 960x540 frame). PIL-measured facts to treat as ground truth: both panels blue-bordered; left panel rows sin(omega t)/cos(omega t) red at x100..161 with thin red bracket stems x88 and x174; red block arrow x127..139 y127..153; lower vector rows sin(a)/cos(a) red on yellow highlight rects x99..163; middle panel header red x236..381; vector A rows BLACK text x226..325 brackets x213/x335; large '=' two bars x348..362 y110..118; vector B rows mixed red(omega t)/blue(omega delta) terms x371..653 brackets x364/x658; red arrow x506..517 y132..157; result vector rows red(a)/blue(b) x392..629 brackets x376/x640."
run_cmp banner $Q/crops/banner_render.png $Q/crops/banner_orig.png \
  "Dense-region zoom check: TITLE BANNER STRIP (x55..910 y215..255 of the 960x540 frame). PIL-measured facts: pale-green fill strip with dark-green border, ONE text line y229..246 reading 'Squared Distance Between Vector of Pos \u201ct+\u03b4\u201d and Vector of Pos \u201ct\u201d [ Two Consecutive Positions ]' where 'Squared Distance Between' + 'and' + '[ Two Consecutive Positions ]' are RED and the two 'Vector of Pos ...' phrases are BLUE."
run_cmp deriv_a $Q/crops/deriv_a_render.png $Q/crops/deriv_a_orig.png \
  "Dense-region zoom check: DERIVATION ROWS 1-3 (x60..800 y258..362 of the 960x540 frame). PIL-measured facts: row1 (y265..288) is color-coded - BLUE brackets/operators/cos(b)/sin(b) terms, RED sin(a)/cos(a) terms, YELLOW highlight rects behind the 3rd 'sin(a)' (x325..369) and the trailing 'cos(a)' (x674..721), trailing blue '=' detached at x767..777; row2 (y299..318) ALL BLACK text ending ']' then detached '=' at x768..777; row3 (y338..356) ALL BLACK ending '... ] +' with the plus ATTACHED at x687..696."
run_cmp deriv_b $Q/crops/deriv_b_render.png $Q/crops/deriv_b_orig.png \
  "Dense-region zoom check: DERIVATION ROWS 4-7 + RESULT CALLOUT + ROTATED RIBBON (x60..870 y355..516 of the 960x540 frame). PIL-measured facts: row4 (y360..381) black ends ']' with detached '=' x772..781; row5 (y394..419) black with detached '=' x774..783; row6 (y428..452) black '[ sin(a)^2+cos^2(a) ] (cos(b)-1)^2 + [ ... ] (sin^2(b) ) = (cos(b)-1)^2 + sin^2(b)' with detached '=' x775..783; row7 (y470..496) black 'cos^2(b) -2 cos(b) +1 + sin^2(b) = 2 -2 cos(b) = 2(1-cos(b) )' with CYAN highlight rects x77..131 and x250..301; result callout box x574..735 y469..502 pale-green fill, GREEN border, NAVY text '=2 (1-cos(omega delta))'; rotated pale-yellow ribbon with red bold text lower-right, axis ~48deg, bbox ~x737..851 y400..511."
echo "ALL CROPS DONE $(date +%T)"
