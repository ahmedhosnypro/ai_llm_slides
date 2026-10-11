#!/usr/bin/env python3
"""Slide 038 — save magnified inspection crops."""
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide038/"
img = Image.open(F).convert("RGB")

crops = {
    "z_toprow":      (60, 243, 900, 296, 2),   # top Y row: labels, bars, dots
    "z_layernorm":   (60, 288, 900, 335, 2),   # gray bar + text + red/green arrows
    "z_plusrow":     (60, 315, 900, 350, 2),   # plus row + green arrows
    "z_midrow":      (60, 344, 900, 400, 2),   # middle Y' row
    "z_navy_left":   (60, 375, 480, 470, 2),   # navy left + blue arrows + orange
    "z_navy_right":  (480, 375, 900, 470, 2),  # navy right
    "z_xrow":        (60, 455, 900, 512, 2),   # X row + caption
    "z_annotations": (60, 350, 175, 495, 4),   # left annotations
    "z_tail_top":    (720, 243, 900, 296, 4),  # top tail labels
    "z_tail_mid":    (720, 344, 900, 400, 4),  # mid tail labels
    "z_tail_x":      (720, 455, 900, 512, 4),  # x tail labels
    "z_caption":     (255, 485, 575, 515, 4),  # caption zoom
    "z_title":       (230, 60, 790, 100, 2),   # title zoom
    "z_defbox1":     (90, 105, 870, 175, 2),   # def lines 1-3
    "z_defbox2":     (90, 185, 870, 240, 2),   # def lines 4-5
    "z_badge":       (845, 45, 915, 100, 4),   # badge
}
for name, (x0, y0, x1, y1, k) in crops.items():
    c = img.crop((x0, y0, x1, y1))
    c = c.resize((c.width * k, c.height * k), Image.LANCZOS)
    c.save(OUT + name + ".png")
    print(name, c.size)
