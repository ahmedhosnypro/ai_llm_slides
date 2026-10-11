#!/usr/bin/env python3
from PIL import Image
IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg").convert("RGB")
D = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide019/"
def crop(name, box, scale):
    c = IM.crop(box)
    c = c.resize((c.width * scale, c.height * scale), Image.LANCZOS)
    c.save(D + name)
    print(name, c.size)
crop("c_callouts.png", (125, 95, 575, 220), 2)
crop("c_enc.png", (595, 250, 750, 425), 2)
crop("c_dec.png", (725, 185, 870, 425), 2)
crop("c_enccirc.png", (625, 375, 745, 415), 4)
crop("c_dectop.png", (735, 100, 880, 150), 3)
