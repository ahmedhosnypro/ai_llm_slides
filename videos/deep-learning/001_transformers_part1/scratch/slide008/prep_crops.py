#!/usr/bin/env python3
"""Prep render/original crop pairs (same scale) for dense-region comparisons."""
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"
OUT = BASE + "recreated_pptx/qa/slide008/crops/"
import os
os.makedirs(OUT, exist_ok=True)

ren = Image.open(BASE + "recreated_pptx/qa/slide008/render_1.png").convert("RGB")
orig = Image.open(BASE + "unique_slides/slide_008.jpg").convert("RGB")
F = ren.width / 960.0

def pair(x0, y0, x1, y1, name):
    r = ren.crop((round(x0 * F), round(y0 * F), round(x1 * F), round(y1 * F)))
    o = orig.crop((x0, y0, x1, y1)).resize(r.size, Image.LANCZOS)
    r.save(OUT + name + "_render.png")
    o.save(OUT + name + "_original.png")
    print(name, r.size)

pair(40, 160, 335, 236, "callout")   # callout box: 2 lines + underline
pair(45, 248, 350, 300, "waits")     # wait boxes + subscript digits
