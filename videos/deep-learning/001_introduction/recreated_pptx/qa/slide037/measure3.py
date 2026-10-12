#!/usr/bin/env python3
"""Measure slide_037.jpg pass 3 — panel border with loose threshold; save crops."""
from PIL import Image
import numpy as np
from collections import Counter

SRC = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_037.jpg'
im = Image.open(SRC).convert('RGB')
a = np.asarray(im).astype(int)

# loose red: R dominates G and B by 50+
red = (a[:, :, 0] - a[:, :, 1] > 50) & (a[:, :, 0] - a[:, :, 2] > 50)
rr = red[:, 60:900].sum(axis=1)
print("loose-red long rows (>400):", [(y, int(c)) for y, c in enumerate(rr) if c > 400])
cc = red[265:510, :].sum(axis=0)
print("loose-red long cols (>120):", [(x, int(c)) for x, c in enumerate(cc) if c > 120])

# crops for visual inspection
for name, box in {
    'crop_title.png': (40, 40, 920, 130),
    'crop_yellowbox.png': (40, 130, 920, 250),
    'crop_panel_left.png': (40, 255, 520, 520),
    'crop_panel_right.png': (480, 255, 920, 520),
    'crop_full_panel.png': (40, 255, 920, 520),
}.items():
    im.crop(box).save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide037/' + name)
print("crops saved")
