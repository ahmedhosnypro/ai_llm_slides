#!/usr/bin/env python3
"""m10: high-zoom crops (4x-6x) for micro-label verification."""
from PIL import Image
import os

SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide011"
f = Image.open(f"{SCR}/frame11_slide.png")
os.makedirs(f"{SCR}/zooms", exist_ok=True)
REG = {
    "z1_leftW":    (138, 232, 192, 348, 6),
    "z2_rightWv":  (524, 228, 574, 348, 6),
    "z3_kq_frac":  (283, 203, 378, 244, 5),
    "z4_arclabel": (690, 275, 838, 335, 4),
    "z5_dotprod":  (222, 205, 295, 245, 5),
    "z6_qWbox":    (236, 348, 292, 408, 5),
    "z7_row1":     (86, 232, 238, 264, 5),
    "z8_chip_h1":  (596, 366, 646, 434, 5),
    "z9_topzone":  (380, 52, 745, 212, 3),
    "z10_sigma":   (398, 203, 505, 245, 4),
    "z11_qrow":    (172, 396, 396, 434, 4),
    "z12_h1pipeline": (88, 232, 340, 360, 3),
}
for name, (x0, y0, x1, y1, k) in REG.items():
    c = f.crop((x0, y0, x1, y1))
    c = c.resize((c.width * k, c.height * k), Image.LANCZOS)
    c.save(f"{SCR}/zooms/{name}.png")
    print(name, c.size)
