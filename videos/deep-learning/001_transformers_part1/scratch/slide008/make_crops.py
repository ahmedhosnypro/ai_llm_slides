#!/usr/bin/env python3
"""Generate zoomed crops of the delta regions for vision verification."""
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"
im = Image.open(BASE + "unique_slides/slide_008.jpg").convert("RGB")
OUT = BASE + "scratch/slide008/"

def crop(x0, y0, x1, y1, scale, name):
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * scale, c.height * scale), Image.LANCZOS)
    c.save(OUT + name)
    print(name, c.size)

crop(40, 160, 335, 236, 4, "crop_callout.png")    # callout box: 2 lines + underline + border
crop(45, 248, 350, 300, 4, "crop_waits.png")      # wait boxes text
crop(175, 255, 480, 340, 3, "crop_leaders.png")   # leaders, endpoints, h-arrows, red dot
