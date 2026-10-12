#!/usr/bin/env python3
"""Save 2x-3x zoomed crops of key regions for visual inspection."""
from PIL import Image

SRC = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_009.jpg'
OUT = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide009'
im = Image.open(SRC).convert('RGB')

crops = {
    'crop_title':      (100, 55, 810, 100, 2),
    'crop_leftpanel':  (75, 100, 290, 510, 2),
    'crop_yrow':       (280, 100, 540, 300, 3),
    'crop_matrix':     (520, 100, 900, 300, 2),
    'crop_bcol':       (825, 100, 900, 300, 4),
    'crop_xboxes':     (520, 100, 670, 190, 4),
}
for name, (x0, y0, x1, y1, z) in crops.items():
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * z, c.height * z), Image.LANCZOS)
    c.save(f'{OUT}/{name}.png')
    print(name, c.size)
