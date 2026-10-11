#!/usr/bin/env python3
"""Prepare dense-region crops (render + original, same effective scale, upscaled)
and pixel-measure both before any vision call (dense-region-crop-compare pattern)."""
from PIL import Image
import numpy as np
import os

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
REN = f"{ROOT}/recreated_pptx/qa/slide007/render_1.png"
ORG = f"{ROOT}/unique_slides/slide_007.jpg"
OUT = f"{ROOT}/recreated_pptx/qa/slide007/crops"
os.makedirs(OUT, exist_ok=True)

r_img = Image.open(REN)
o_img = Image.open(ORG)
k = r_img.width / o_img.width  # 2.0844

REGIONS = {
    # name: (render-space box x0,y0,x1,y1, upscale)
    "callout":  (83, 344, 1084, 600, 2),   # box + 4 lines + underlines + connector + arc junction
    "titlesub": (521, 83, 1397, 250, 2),   # title line1 + '(Challenges)'
}
for name, (x0, y0, x1, y1, sc) in REGIONS.items():
    r = r_img.crop((x0, y0, x1, y1))
    r = r.resize((r.width * sc, r.height * sc), Image.LANCZOS)
    r.save(f"{OUT}/{name}_render.png")
    o = o_img.crop((int(x0 / k), int(y0 / k), int(x1 / k), int(y1 / k)))
    o = o.resize((o.width * sc, o.height * sc), Image.LANCZOS)
    o.save(f"{OUT}/{name}_original.png")
    for tag in ("render", "original"):
        a = np.asarray(Image.open(f"{OUT}/{name}_{tag}.png").convert("L"))
        ink = a < 180
        ys, xs = np.where(ink)
        if len(xs):
            print(f"{name}_{tag}: size={a.shape[1]}x{a.shape[0]} ink_px={int(ink.sum())} "
                  f"span=({xs.min()},{ys.min()})-({xs.max()},{ys.max()})")
        else:
            print(f"{name}_{tag}: size={a.shape[1]}x{a.shape[0]} NO INK")
