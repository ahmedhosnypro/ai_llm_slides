#!/usr/bin/env python3
"""Slide 038 — high-mag single-column crops + container edges + block arrow."""
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide038/"
img = Image.open(F).convert("RGB")

crops = {
    "hh_col2_full":  (240, 310, 320, 400, 8),   # column 2: bar->plus->Y'->block arrows
    "hh_col7_full":  (725, 310, 800, 400, 8),   # column 7 tail
    "hh_col2_bar":   (240, 255, 320, 300, 8),   # column 2: top bar + red arrow + label
    "hh_arrow_blk":  (260, 375, 300, 410, 10),  # block arrow zoom col2
    "hh_container":  (55, 275, 905, 375, 2),    # whole green container region
    "hh_col2_x":     (240, 440, 320, 500, 8),   # column 2 X row: block arrow + bar + orange
    "hh_orange_l":   (160, 330, 260, 470, 5),   # orange arrow path col1-2
    "hh_bar_left":   (70, 290, 300, 325, 5),    # gray bar left end + text start
    "hh_bar_right":  (700, 290, 890, 325, 5),   # gray bar right end + text end
}
for name, (x0, y0, x1, y1, k) in crops.items():
    c = img.crop((x0, y0, x1, y1))
    c = c.resize((c.width * k, c.height * k), Image.LANCZOS)
    c.save(OUT + name + ".png")
    print(name, c.size)
