#!/usr/bin/env python3
# crops5.py — dense-region crops (orig + render_5) for the pre-judge gate comparisons.
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
orig = Image.open(f"{ROOT}/unique_slides/slide_051.jpg").convert("RGB")
r5 = Image.open(f"{ROOT}/recreated_pptx/qa/slide051/render_5.png").convert("RGB")
K = 150.0 / 72.0
RX, RY = lambda fx: (fx - 18.128) / 0.961235 * K, lambda fy: (fy + 0.045) / 0.956566 * K
OUT = f"{ROOT}/scratch/slide051/crops5"

def crop_pair(name, fx0, fy0, fx1, fy1, zoom):
    # orig: direct crop then upscale
    oc = orig.crop((fx0, fy0, fx1, fy1))
    oc = oc.resize((oc.width * zoom, oc.height * zoom), Image.LANCZOS)
    oc.save(f"{OUT}/{name}_orig.png")
    # render: crop at mapped render coords, upscale to the same frame-px scale
    x0, y0, x1, y1 = int(RX(fx0)), int(RY(fy0)), int(RX(fx1)), int(RY(fy1))
    rc = r5.crop((x0, y0, x1, y1))
    scale = zoom / K * (72.0 / 150.0) * K  # render px -> frame px is /K*0.961..; simpler: target size
    target_w = int((fx1 - fx0) * zoom)
    rc = rc.resize((target_w, int(rc.height * target_w / rc.width)), Image.LANCZOS)
    rc.save(f"{OUT}/{name}_render.png")
    print(name, "orig", oc.size, "render", rc.size)

import os
os.makedirs(OUT, exist_ok=True)
crop_pair("enc_norms", 198, 255, 290, 350, 3)
crop_pair("dec_right", 713, 272, 870, 470, 2)
