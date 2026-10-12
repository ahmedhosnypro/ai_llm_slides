#!/usr/bin/env python3
# crops12.py — upscaled inspection crops for slide 012 build decisions
from PIL import Image
SRC = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_012.jpg'
OUT = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide012/'
im = Image.open(SRC).convert('RGB')

def crop(name, x0, y0, x1, y1, scale=4):
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * scale, c.height * scale), Image.LANCZOS)
    c.save(OUT + name)
    print(name, c.size)

crop('c_brace1.png',   385, 135, 425, 370, 4)
crop('c_brace2.png',   548, 135, 590, 370, 4)
crop('c_brace3.png',   700, 140, 745, 400, 4)
crop('c_magenta.png',  500, 235, 570, 300, 6)
crop('c_res1.png',     290, 415, 360, 450, 6)
crop('c_res2.png',     465, 415, 535, 450, 6)
crop('c_strips.png',   240, 350, 735, 395, 2)
crop('c_eq.png',       190, 350, 240, 395, 6)
crop('c_embed.png',     85, 115, 260, 210, 3)
crop('c_h1top.png',    240, 130, 400, 240, 3)
crop('c_h2grid.png',   405, 130, 570, 365, 2)
crop('c_subtitle.png',  85, 74, 880, 102, 1)
crop('c_title.png',    150, 48, 810, 82, 1)
