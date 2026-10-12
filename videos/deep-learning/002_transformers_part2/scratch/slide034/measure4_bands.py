#!/usr/bin/env python3
"""measure4_bands.py — fine census of specific bands: color histogram per band."""
import numpy as np
from PIL import Image
from collections import Counter

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_034.jpg"
img = np.asarray(Image.open(FR).convert("RGB")).astype(int)

def census(y0, y1, x0, x1, name, topn=14):
    win = img[y0:y1, x0:x1].reshape(-1, 3)
    # quantize to 16-level bins to defeat JPEG noise
    q = (win // 24) * 24
    c = Counter(map(tuple, q))
    print(f"=== {name} y{y0}-{y1} x{x0}-{x1} ===")
    for (rr, gg, bb), n in c.most_common(topn):
        print(f"  ({rr:3d},{gg:3d},{bb:3d})  {n}")

census(290, 340, 60, 890, "VECTOR ROW band (incl container)")
census(128, 180, 170, 890, "TOKEN ROW container+boxes")
census(36, 130, 60, 890, "TITLE+SUBTITLE zone")
census(360, 510, 200, 830, "BRACE+SUMMARY zone")
census(150, 260, 60, 170, "LEFT LABELS zone")
