#!/usr/bin/env python3
"""mkcrops_1.py — measurement crops (2x upscaled) for gate-based vision reads."""
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_039.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide039/"
im = Image.open(FR).convert("RGB")

CROPS = {
    "c_front_left":  (110, 225, 360, 500),   # left X box, K rows, dot box, W^q branch
    "c_front_right": (300, 225, 700, 500),   # scaling, softmax, otimes, V/W^V, right X box
    "c_top":         (380, 85, 790, 265),    # Y boxes, arrows, labels, pill rows
    "c_bottom":      (120, 400, 940, 540),   # bottom X row, arrows+labels, sticker, connectors
}
for name, (x0, y0, x1, y1) in CROPS.items():
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
    p = OUT + name + ".png"
    c.save(p)
    print(p, c.size)
