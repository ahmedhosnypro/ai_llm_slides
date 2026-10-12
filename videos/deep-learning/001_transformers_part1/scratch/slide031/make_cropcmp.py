#!/usr/bin/env python3
"""Build cropped comparison pairs: render_1.png vs slide_031.jpg, same regions."""
from PIL import Image
import os

FR = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
RN = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide031/render_4.png").convert("RGB")
S = RN.width / 960.0
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide031/cropcmp"
os.makedirs(OUT, exist_ok=True)

REGIONS = {
    "qpanel":   (50, 90, 475, 310),
    "vpanel":   (470, 90, 900, 310),
    "kpanel":   (50, 300, 475, 535),
    "callouts": (435, 255, 930, 535),
    "titleband": (40, 40, 920, 100),
}
for name, (x0, y0, x1, y1) in REGIONS.items():
    fr = FR.crop((x0, y0, x1, y1))
    rn = RN.crop((int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S)))
    # upscale frame crop x2; render crop resized to the same dims
    fr2 = fr.resize((fr.width * 2, fr.height * 2), Image.LANCZOS)
    rn2 = rn.resize(fr2.size, Image.LANCZOS)
    fr2.save(f"{OUT}/{name}_orig.png")
    rn2.save(f"{OUT}/{name}_render.png")
    print(name, fr2.size)
