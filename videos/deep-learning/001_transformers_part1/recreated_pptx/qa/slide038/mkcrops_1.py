#!/usr/bin/env python3
"""Crop render + original for the dense-region vision comparisons (3x upscale)."""
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
S = 2000 / 960.0
rnd = Image.open(f"{V}/recreated_pptx/qa/slide038/render_1.png").convert("RGB")
org = Image.open(f"{V}/unique_slides/slide_038.jpg").convert("RGB")

def crop3(img, x0, y0, x1, y1, scale, out):
    c = img.crop((round(x0 * scale), round(y0 * scale), round(x1 * scale), round(y1 * scale)))
    c = c.resize((c.width * 3, c.height * 3), Image.LANCZOS)
    c.save(out)
    print(out, c.size)

# inset: frame x[780..930] y[100..325]
crop3(rnd, 780, 100, 930, 325, S, f"{V}/recreated_pptx/qa/slide038/cc_inset_mine.png")
crop3(org, 780, 100, 930, 325, 1.0, f"{V}/recreated_pptx/qa/slide038/cc_inset_orig.png")
# scaling box + fraction: frame x[350..470] y[160..430]
crop3(rnd, 350, 160, 470, 430, S, f"{V}/recreated_pptx/qa/slide038/cc_scaling_mine.png")
crop3(org, 350, 160, 470, 430, 1.0, f"{V}/recreated_pptx/qa/slide038/cc_scaling_orig.png")
