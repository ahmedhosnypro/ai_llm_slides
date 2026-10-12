#!/usr/bin/env python3
"""measure3_colorrows.py — per-row color census for the main structures:
purple bar, red arrows/brace, blue dashes, green dashes, yellow highlight."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_034.jpg"
img = np.asarray(Image.open(FR).convert("RGB")).astype(int)
H, W, _ = img.shape
r, g, b = img[..., 0], img[..., 1], img[..., 2]

purple = (r > 100) & (r < 190) & (g < 60) & (b > 100) & (b < 190)
red = (r > 150) & (g < 90) & (b < 90)
blue = (b > 120) & (b - r > 60) & (b - g > 40) & (r < 120)
green = (g > 110) & (g - r > 50) & (g - b > 30)
yellow = (r > 200) & (g > 200) & (b < 140)

def span(mask, name, ymin=45, ymax=514, xmin=45, xmax=930, thr=3):
    print(f"--- {name} ---")
    rows = mask[:, xmin:xmax].sum(axis=1)
    inb = False
    for y in range(ymin, ymax):
        if rows[y] > thr and not inb:
            start = y; inb = True
        elif rows[y] <= thr and inb:
            if y - 1 - start >= 0:
                band = mask[start:y, :]
                xs = np.where(band.any(axis=0))[0]
                xs = xs[(xs >= xmin) & (xs < xmax)]
                if len(xs):
                    print(f"  y {start}..{y-1} (h={y-start})  x {xs.min()}..{xs.max()}  max={rows[start:y].max()}")
            inb = False

span(purple, "PURPLE bar")
span(red, "RED (arrows/brace/title/labels)", 45, 514)
span(blue, "BLUE dashes/labels")
span(green, "GREEN dashes/border")
span(yellow, "YELLOW (badge/highlight)", 45, 514)
