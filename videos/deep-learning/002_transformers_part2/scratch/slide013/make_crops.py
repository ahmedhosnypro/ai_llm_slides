#!/usr/bin/env python3
"""Create zoom crops from the original frame for vision analysis (x2 upscale)."""
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_013.jpg').convert('RGB')
OUT = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide013/crops'
import os
os.makedirs(OUT, exist_ok=True)

CROPS = {
    'zoom_left':    (55, 160, 290, 435),
    'zoom_circles': (440, 220, 650, 400),
    'zoom_top':     (480, 105, 700, 200),
    'zoom_right':   (600, 190, 900, 420),
    'zoom_bottom':  (60, 405, 900, 516),
    'zoom_title':   (180, 44, 830, 106),
    'zoom_dp':      (250, 140, 400, 500),
}
for name, (x0, y0, x1, y1) in CROPS.items():
    c = im.crop((x0, y0, x1, y1))
    w, h = c.size
    c = c.resize((w * 2, h * 2), Image.LANCZOS)
    p = '%s/%s.png' % (OUT, name)
    c.save(p)
    print(name, c.size, '->', p)
