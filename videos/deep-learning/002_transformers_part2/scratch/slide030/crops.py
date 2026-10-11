#!/usr/bin/env python3
from PIL import Image
im = Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")
def crop(name, x0, y0, x1, y1, s=3):
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * s, c.height * s), Image.LANCZOS)
    c.save(f"videos/deep-learning/002_transformers_part2/scratch/slide030/{name}.png")
crop("c_vecbox", 85, 50, 380, 240, 3)
crop("c_matrix", 110, 340, 500, 440, 3)
crop("c_deriv1", 95, 240, 665, 275, 2)
crop("c_deriv2", 95, 288, 665, 320, 2)
crop("c_remember", 495, 100, 855, 190, 3)
crop("c_captions", 90, 435, 615, 500, 3)
crop("c_note", 610, 340, 880, 485, 3)
