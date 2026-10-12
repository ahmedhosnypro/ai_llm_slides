#!/usr/bin/env python3
"""mkcrops_2.py — paired crops (render + original) for the 4 dense-region comparisons."""
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"
SCR = BASE + "scratch/slide039/"
ren = Image.open(BASE + "recreated_pptx/qa/slide039/render_2.png").convert("RGB")
org = Image.open(BASE + "unique_slides/slide_039.jpg").convert("RGB")
S = ren.width / 960.0

REGIONS = {
    "p_left":   (110, 225, 360, 500),
    "p_right":  (300, 225, 700, 500),
    "p_top":    (40, 40, 790, 230),
    "p_bottom": (250, 420, 940, 540),
}
for name, (x0, y0, x1, y1) in REGIONS.items():
    rc = ren.crop((int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S)))
    oc = org.crop((x0, y0, x1, y1))
    # bring the original crop to ~the render crop's resolution
    oc = oc.resize((rc.width, rc.height), Image.LANCZOS)
    rc.save(f"{SCR}rc_{name}.png")
    oc.save(f"{SCR}oc_{name}.png")
    print(name, rc.size)
