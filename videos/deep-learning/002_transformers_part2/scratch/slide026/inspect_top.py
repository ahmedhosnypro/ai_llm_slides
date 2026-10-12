#!/usr/bin/env python3
"""Inspect rows 25..75: find any red line; also rows 505..525 for bottom border."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg"
img = Image.open(F).convert("RGB")
a = np.asarray(img).astype(int)

# print per-row: count of reddish px (broad), and mean color at x=400..500
for y in range(25, 75):
    row = a[y, 100:900]
    reddish = ((row[:, 0] - np.maximum(row[:, 1], row[:, 2])) > 30) & (row[:, 0] > 90)
    print(y, int(reddish.sum()), row[300], row[500])
