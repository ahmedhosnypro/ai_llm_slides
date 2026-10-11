#!/usr/bin/env python3
"""Generate matching render crops (same pipeline as the orig crops: 960-space, 2x upscale)."""
from PIL import Image
import os

REN = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide017/render_1.png'
OUT = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide017'
im = Image.open(REN).convert('RGB').resize((960, 540), Image.LANCZOS)

crops = {
    'r_crop_enc_bot.png': (560, 320, 745, 535),
    'r_crop_dec_top.png': (735, 95, 920, 340),
    'r_crop_dec_bot.png': (735, 330, 920, 535),
    'r_crop_gap.png': (600, 230, 800, 340),
}
for name, (x0, y0, x1, y1) in crops.items():
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
    c.save(os.path.join(OUT, name))
    print(name, c.size)
