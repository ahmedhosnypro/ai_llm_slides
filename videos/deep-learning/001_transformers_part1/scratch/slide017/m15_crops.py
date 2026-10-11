#!/usr/bin/env python3
"""Prepare 2x upscaled crops of slide_017.jpg for gate analysis."""
from PIL import Image
import os

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
OUT = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide017'

crops = {
    'crop_enc.png': (560, 95, 745, 535),    # encoder panel + margin left
    'crop_dec.png': (735, 95, 920, 535),    # decoder panel + right margin
    'crop_gap.png': (600, 230, 800, 340),   # encoder top output -> decoder MHA crossing
    'crop_dec_top.png': (735, 95, 920, 340),
    'crop_dec_bot.png': (735, 330, 920, 535),
    'crop_enc_bot.png': (560, 320, 745, 535),
}
for name, (x0, y0, x1, y1) in crops.items():
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
    c.save(os.path.join(OUT, name))
    print(name, c.size)
