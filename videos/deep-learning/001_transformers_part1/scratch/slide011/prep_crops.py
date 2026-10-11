#!/usr/bin/env python3
"""Prepare + measure dense-region crop pairs (render vs original) for slide011."""
import numpy as np
from PIL import Image
import os

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
OUT = VID + "/recreated_pptx/qa/slide011/crops"
os.makedirs(OUT, exist_ok=True)
r_img = Image.open(VID + "/recreated_pptx/qa/slide011/render_1.png")
o_img = Image.open(VID + "/unique_slides/slide_011.jpg").convert("RGB")
k = r_img.width / o_img.width

REGIONS = {  # frame px boxes
    "arrows_olabels": (528, 108, 856, 172, 4),
    "xlabels_inputs": (120, 440, 460, 500, 4),
    "arc_dashes": (318, 218, 662, 346, 3),
    "notebox": (450, 402, 898, 532, 3),
    "enc_attention": (100, 190, 492, 312, 3),
}
for name, (x0, y0, x1, y1, up) in REGIONS.items():
    rc = r_img.crop((int(x0*k), int(y0*k), int(x1*k), int(y1*k)))
    rc = rc.resize((rc.width*up, rc.height*up), Image.LANCZOS)
    rc.save(f"{OUT}/{name}_render.png")
    oc = o_img.crop((x0, y0, x1, y1))
    oc = oc.resize((oc.width*up, oc.height*up), Image.LANCZOS)
    oc.save(f"{OUT}/{name}_original.png")
    for tag, path in (("render", f"{OUT}/{name}_render.png"), ("original", f"{OUT}/{name}_original.png")):
        a = np.asarray(Image.open(path).convert("L"))
        ink = a < 180
        ys, xs = np.where(ink)
        span = f"({xs.min()},{ys.min()})-({xs.max()},{ys.max()})" if len(xs) else "NONE"
        print(f"{name} {tag}: size={a.shape[1]}x{a.shape[0]} ink_px={int(ink.sum())} span={span}")
