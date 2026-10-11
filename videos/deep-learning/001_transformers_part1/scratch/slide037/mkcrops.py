#!/usr/bin/env python3
"""Crop + upscale regions of slide_037.jpg for vision analysis."""
from PIL import Image
import os

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_037.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide037"
im = Image.open(IMG).convert("RGB")

CROPS = {
    # name: (x0, y0, x1, y1, upscale)
    "leftrow":    (50, 222, 262, 270, 4),    # left group row 1: embedding + W_k + K + arrow
    "y2sigma":    (495, 100, 690, 350, 3),   # Y2 block, green arrow, pills?, sigma, mult nodes
    "legend":     (725, 450, 930, 540, 4),   # dimension annotation box
    "strip":      (155, 395, 495, 540, 3),   # sentence strip + W_q + q2 + block arrow
    "dotbox":     (245, 185, 355, 415, 4),   # Dot Product box interior
    "rightrow":   (660, 222, 880, 270, 4),   # right group row 1
    "title":      (40, 48, 730, 105, 2),     # title + subtitle
    "scaling":    (360, 185, 460, 415, 3),   # scaling box + fraction
}
for name, (x0, y0, x1, y1, up) in CROPS.items():
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * up, c.height * up), Image.LANCZOS)
    p = os.path.join(OUT, f"crop_{name}.png")
    c.save(p)
    print(p, c.size)
