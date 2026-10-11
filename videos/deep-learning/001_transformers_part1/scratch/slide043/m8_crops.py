#!/usr/bin/env python3
"""Crops of slide_043.jpg for vision analysis, upscaled x2 (LANCZOS)."""
from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')
def crop(name, box, scale=2):
    c = im.crop(box)
    c = c.resize((c.width*scale, c.height*scale), Image.LANCZOS)
    c.save(f'/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide043/{name}.png')
    print(name, box, '->', c.size)
crop('crop_pipeline', (150, 40, 800, 160))
crop('crop_title',    (540, 40, 925, 125))
crop('crop_staircase',(40, 183, 960, 275))
crop('crop_frontleft',(40, 270, 350, 540))
crop('crop_frontmid', (350, 270, 630, 540))
crop('crop_right',    (620, 250, 960, 540))
crop('crop_legend',   (690, 415, 960, 540))
crop('crop_bottom',   (40, 470, 640, 540))
