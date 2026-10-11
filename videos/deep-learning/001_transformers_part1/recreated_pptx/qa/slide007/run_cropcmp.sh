#!/usr/bin/env bash
# Crop comparisons for slide 007 dense regions (dense-region-crop-compare pattern).
# Full judge params; frozen template verbatim; region-scoped --view with measured facts.
set -u
ROOT=/home/ahmed/Projects/ai_llm_slides
Q=$ROOT/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide007
SCRATCH=$ROOT/videos/deep-learning/001_transformers_part1/scratch/slide007
TPL=$(cat "$Q/judge_template_clean.txt")

cd "$ROOT"
export TMPDIR=$SCRATCH

# --- crop 1: callout + connector ---
scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$Q/crops/callout_render.png" "$Q/crops/callout_original.png" \
  --view "Dense-region zoom check: the '[1] Bottleneck' callout box + connector of slide 007. MEASURED FACTS (PIL, before this call): render crop 2002x512 px, original crop 962x244 px (same slide fraction, render is 2.08x original scale, both upscaled x2). Ink spans nearly the full crop in both. Expected content: light-blue rounded box with thin blue-gray border, 4 centered bold blue lines; underline under line 1 ('[1] Bottleneck'), under the TAIL of line 3 ('by a single context vector'), and under the TAIL of line 4 ('fixed  dimensionality'); NO underline under line 2; a thin gray-blue connector leaves the box right edge and runs down-right into the red context-vector arc. The white mouse cursor visible over the box in the original is a video-capture artifact and is CORRECTLY omitted from the recreation." \
  --capture "IMG1=crop of the 150dpi PPTX render (2.08x original scale); IMG2=crop of the original lecture frame, both upscaled x2" \
  --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
  --transcript "$Q/cropcmp_callout.txt" \
  -p "$TPL"
echo "CROP1_RC=$?"

# --- crop 2: title + subtitle ---
scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$Q/crops/titlesub_render.png" "$Q/crops/titlesub_original.png" \
  --view "Dense-region zoom check: slide 007 title block. MEASURED FACTS (PIL, before this call): render crop 1752x334 px, original crop 842x160 px (same slide fraction, render is 2.08x original scale, both upscaled x2). Line 1 'Traditional RNN  Seq2Seq model' (bold red) is the INHERITED judge-certified slide-006 component — identical pixels to the certified parent render; per the dependency law a finding on it is judge variance unless this child's draw broke it. The expected DELTA is line 2 '(Challenges)' in bold blue, centered under line 1: original ink x376..533 of 960, y87..111; render ink x776..1107 of 2001, y189..241 (width ratio to original 331/329 render px)." \
  --capture "IMG1=crop of the 150dpi PPTX render (2.08x original scale); IMG2=crop of the original lecture frame, both upscaled x2" \
  --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
  --transcript "$Q/cropcmp_titlesub.txt" \
  -p "$TPL"
echo "CROP2_RC=$?"
