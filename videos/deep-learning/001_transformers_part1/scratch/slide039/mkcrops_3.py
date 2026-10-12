#!/usr/bin/env python3
"""mkcrops_3.py — verification crops from the ORIGINAL frame for targeted gate calls."""
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"
SCR = BASE + "scratch/slide039/"
org = Image.open(BASE + "unique_slides/slide_039.jpg").convert("RGB")

def crop(name, box, scale):
    c = org.crop(box)
    c = c.resize((c.width * scale, c.height * scale), Image.LANCZOS)
    c.save(SCR + name)
    print(name, c.size)

crop("v1_fraction.png", (312, 250, 412, 300), 6)
crop("v2_leftbox.png", (126, 280, 194, 406), 5)
crop("v3_bottomrow.png", (258, 448, 482, 492), 5)
crop("v7_vlabels.png", (604, 286, 678, 416), 5)

# sticker: unrotate around measured center, then crop the band
cy, cx = 477, 790
patch = org.crop((660, 420, 925, 535))
u = patch.rotate(-18.43, resample=Image.BICUBIC, center=(cx - 660, cy - 420), fillcolor=(255, 255, 255))
u = u.crop((692 - 660 - 8, 455 - 420 - 6, 892 - 660 + 8, 495 - 420 + 6))
u = u.resize((u.width * 4, u.height * 4), Image.LANCZOS)
u.save(SCR + "v4_sticker.png")
print("v4_sticker.png", u.size)
