#!/usr/bin/env python3
"""Create 2x upscaled crops of dense regions for vision gate reads."""
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")

crops = {
    "crop_qpanel":   (50, 95, 470, 305),
    "crop_vpanel":   (465, 95, 900, 305),
    "crop_callouts": (430, 258, 935, 385),
    "crop_boxes":    (475, 375, 930, 530),
    "crop_titlesub": (40, 36, 930, 100),
}
import os
os.makedirs("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide031/crops", exist_ok=True)
for name, (x0, y0, x1, y1) in crops.items():
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
    p = f"/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide031/crops/{name}.png"
    c.save(p)
    print(name, c.size)
