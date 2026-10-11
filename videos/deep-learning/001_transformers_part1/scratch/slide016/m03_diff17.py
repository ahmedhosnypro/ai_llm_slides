#!/usr/bin/env python3
"""Diff diagram regions of slide_016.jpg vs slide_017.jpg (960x540)."""
import numpy as np
from PIL import Image

A = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_016.jpg").convert("RGB")).astype(int)
B = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg").convert("RGB")).astype(int)
d = np.abs(A - B).max(axis=2)

def region_diff(name, x0, y0, x1, y1):
    r = d[y0:y1+1, x0:x1+1]
    n = r.size
    print(f"{name}: x{x0}-{x1} y{y0}-{y1}  diff>24: {(r>24).sum():7d}/{n} ({(r>24).mean()*100:5.2f}%)  diff>60: {(r>60).sum():7d}  maxdiff {r.max()}")

# diagram zone (right of callout column, incl. green frame margin)
region_diff("diagram zone", 560, 95, 920, 530)
# tighter: inside green frame
region_diff("inside frame", 576, 104, 895, 523)
# encoder panel only
region_diff("enc panel", 577, 108, 735, 520)
# decoder panel only
region_diff("dec panel", 737, 108, 890, 520)
# title zone
region_diff("title zone", 100, 45, 860, 95)
# left callout column
region_diff("callout column", 42, 95, 560, 530)
