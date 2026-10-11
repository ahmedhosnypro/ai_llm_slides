#!/usr/bin/env bash
# Attempt-2 dense-region crop comparisons (pattern: dense-region-crop-compare).
# Crops (frame px): A center zoom (270,195,540,540); B right panel (555,95,915,540);
# C left schematic (35,220,215,505). Render crops from render_2.png at the same
# effective region (render px = frame px * 2000/960), both upscaled x2.
set -uo pipefail
SCRATCH=/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide041
QA=/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide041
cd /home/ahmed/Projects/ai_llm_slides

python3 - <<'EOF'
from PIL import Image
SCRATCH = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide041/"
QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide041/"
ren = Image.open(QA + "render_2.png").convert("RGB")
org = Image.open(SCRATCH + "../../unique_slides/slide_041.jpg").convert("RGB")
k = ren.width / org.width
crops = {
    "A_center_zoom": (270, 195, 540, 540),
    "B_right_panel": (555, 95, 915, 540),
    "C_left_schematic": (35, 220, 215, 505),
}
for name, (x0, y0, x1, y1) in crops.items():
    r = ren.crop((round(x0 * k), round(y0 * k), round(x1 * k), round(y1 * k)))
    r = r.resize((r.width * 2, r.height * 2), Image.LANCZOS)
    r.save(SCRATCH + f"att2_crop{name}_render.png")
    o = org.crop((x0, y0, x1, y1))
    o = o.resize((o.width * 2, o.height * 2), Image.LANCZOS)
    o.save(SCRATCH + f"att2_crop{name}_orig.png")
    print(name, "render", r.size, "orig", o.size)
EOF

# numeric ink measurement of each crop pair (rebuttal evidence)
python3 - <<'EOF'
from PIL import Image
import numpy as np
SCRATCH = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide041/"
for name in ("A_center_zoom", "B_right_panel", "C_left_schematic"):
    for tag in ("render", "orig"):
        p = SCRATCH + f"att2_crop{name}_{tag}.png"
        a = np.asarray(Image.open(p).convert("L"))
        ink = a < 180
        ys, xs = np.where(ink)
        if len(xs):
            print(f"{name} {tag}: {a.shape[1]}x{a.shape[0]} ink={int(ink.sum())} span=({xs.min()},{ys.min()})-({xs.max()},{ys.max()})")
        else:
            print(f"{name} {tag}: NO INK")
EOF
