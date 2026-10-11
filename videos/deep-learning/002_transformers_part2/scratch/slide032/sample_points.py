#!/usr/bin/env python3
"""Sample raw pixel colors at key structural points."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_032.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def avg(x, y, r=3):
    patch = a[y - r:y + r + 1, x - r:x + r + 1]
    m = patch.reshape(-1, 3).mean(axis=0)
    return tuple(int(v) for v in m)

pts = {
    'top-left inside gray panel (70,60)': (70, 60),
    'top-center gray (300,52)': (300, 52),
    'right of badge (930,70)': (930, 70),
    'left margin (65,300)': (65, 300),
    'right margin (912,300)': (912, 300),
    'between subtitle and panel (500,105)': (500, 105),
    'left of vector box (75,150)': (75, 150),
    'vector box interior (140,150)': (140, 150),
    'callout interior (400,140)': (400, 140),
    'main panel (300,230)': (300, 230),
    'main panel (700,420)': (700, 420),
    'main panel left edge (85,350)': (85, 350),
    'main panel right edge (870,350)': (870, 350),
    'below main panel? (500,490)': (500, 490),
    'bottom margin (500,525)': (500, 525),
    'letterbox (500,535)': (500, 535),
}
for label, (x, y) in pts.items():
    print(f"{label:42s} {avg(x, y)}")
