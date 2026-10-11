#!/usr/bin/env bash
# Attempt-2 crop comparisons (changed regions only: banner fix + mid-panel mva eqs),
# through the fleet vision gate. Attempt-1 crops for left panel / derivation rows /
# callout / ribbon remain valid (render diff vs render_1 = 0 changed px in those regions).
set -u
cd /home/ahmed/Projects/ai_llm_slides
export TMPDIR=$PWD/videos/deep-learning/002_transformers_part2/scratch/slide031
Q=videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide031
TPL=$PWD/$Q/judge_template.txt

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
    --transcript "$Q/cropcmp_${name}_2.txt" \
    -p "$(cat "$TPL")"
  echo "crop $name exit=$? $(date +%T)"
}

run_cmp banner $Q/crops/banner_render_a2.png $Q/crops/banner_orig_a2.png \
  "Dense-region zoom check ATTEMPT 2 (re-judge after fix): TITLE BANNER STRIP (x55..910 y215..255 of the 960x540 frame). PIL-measured facts to treat as ground truth: pale-green fill strip with dark-green border, ONE text line y229..246 reading 'Squared Distance Between Vector of Pos \u201ct+\u03b4\u201d and Vector of Pos \u201ct\u201d [ Two Consecutive Positions ]' where 'Squared Distance Between' + 'and' + '[ Two Consecutive Positions ]' are RED and the two 'Vector of Pos ...' phrases are BLUE. ATTEMPT-2 FIX APPLIED: the five phrases are separate left-aligned text boxes at the frame-measured ink anchors x72/287/438/475/631 (the 29px gap before '[ Two Consecutive Positions ]' and the ~9px gaps around 'and' are now reproduced; phrase font sizes were fitted per-phrase so each phrase's rendered ink width matches the original's measured width within ~1px: 209/146/28/127/225 px). Judge whether the gaps, phrase order, colors, and per-phrase sizes now match the original."
run_cmp topband $Q/crops/topband_render_a2.png $Q/crops/topband_orig_a2.png \
  "Dense-region zoom check ATTEMPT 2 (re-judge after equation re-render): TOP BAND (left mint 'Vector at Pos t' panel + middle cream 'Vector at Pos t+delta' panel, x55..690 y40..220 of the 960x540 frame). PIL-measured facts to treat as ground truth: both panels blue-bordered; left panel rows sin(omega t)/cos(omega t) red at x100..161 with thin red bracket stems x88 and x174; red block arrow x127..139 y127..153; lower vector rows sin(a)/cos(a) red on yellow highlight rects x99..163; middle panel header red x236..381; vector A rows BLACK text x226..325 brackets x213/x335; large '=' two bars x348..362 y110..118; vector B rows mixed red(omega t)/blue(omega delta) terms x371..653 brackets x364/x658; red arrow x506..517 y132..157; result vector rows red(a)/blue(b) x392..629 brackets x376/x640. ATTEMPT-2 CHANGE: the vector-A rows were re-rendered with tight '+' spacing, omega(t+delta), matching the original's printed 'Sin (\u03c9(t+\u03b4))' / 'cos (\u03c9(t+\u03b4))'. Judge the middle panel's equation spacing/sizes against the original."
echo "ALL ATTEMPT-2 CROPS DONE $(date +%T)"
