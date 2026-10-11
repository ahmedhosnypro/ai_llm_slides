#!/usr/bin/env python3
from PIL import Image
im = Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")
def crop(name, x0, y0, x1, y1, s=5):
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * s, c.height * s), Image.LANCZOS)
    c.save(f"videos/deep-learning/002_transformers_part2/scratch/slide030/{name}.png")
crop("c_mtx_r1c2", 415, 345, 480, 385, 6)
crop("c_mtx_r2c2", 405, 390, 475, 428, 6)
crop("c_L1tail", 580, 242, 660, 272, 6)
crop("c_L2mid", 440, 288, 525, 318, 6)
