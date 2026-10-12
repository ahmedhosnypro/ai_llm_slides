#!/usr/bin/env python3
"""Crop divergent regions from frame11 in slide coords, 2x upscale, for close reading."""
from PIL import Image

SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide011"
f = Image.open(f"{SCR}/frame11_slide.png")
import os
os.makedirs(f"{SCR}/crops", exist_ok=True)
REG = {
    "A_leftinput":  (60, 180, 250, 390),
    "B_pipeline":   (220, 175, 570, 385),
    "C_beamtop":    (380, 40, 720, 215),
    "D_right":      (560, 180, 870, 460),
    "E_queryrow":   (150, 340, 430, 465),
    "F_title":      (270, 460, 710, 525),
    "G_tagrow":     (280, 90, 860, 220),
}
for name, (x0, y0, x1, y1) in REG.items():
    c = f.crop((x0, y0, x1, y1))
    c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
    c.save(f"{SCR}/crops/{name}.png")
    print(name, c.size)
