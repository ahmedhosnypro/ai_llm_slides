#!/usr/bin/env python3
"""m3.py — color census: what are the REAL colors in key regions of slide_039.jpg."""
from PIL import Image
import numpy as np
from collections import Counter

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_039.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im)

def census(name, x0, y0, x1, y1, top=8):
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    # quantize to /8 to merge jpeg noise
    q = (sub // 8 * 8)
    c = Counter(map(tuple, q))
    print(f"{name} ({x0},{y0})-({x1},{y1}):", c.most_common(top))

# panel fill (front panel, empty area near its left edge below X box?)
census("panel1-fill", 160, 430, 200, 460)
# left X box interior
census("leftX-box", 135, 300, 160, 340)
# Dot Product box area
census("dot-box", 270, 300, 310, 380)
# pink scaling box area (from pink mask x329-349 y263-404)
census("pink-box", 330, 300, 348, 390)
# Sigma box (paleblue mask found y142-250 x403-701 — sample inside)
census("sigma-box", 560, 200, 600, 220)
# cream pill near y170 x430-510
census("pill", 432, 165, 455, 180)
# green: where? Y box border at y148-162 x560-640 (red mask hit there but green?)
census("ybox-area", 555, 120, 645, 165, 10)
# bottom X row (highlighted cell) around y 465-480 x 175-260?
census("bottom-row", 180, 458, 260, 482, 10)
# sticker
census("sticker", 700, 440, 880, 510, 6)
# rear panel sliver right side x 830-890 y 200-300
census("rear-sliver", 830, 210, 890, 300, 8)
# W^k boxes: white boxes with blue border, left-mid of panel1 around x 200-240 y 250-400?
census("wk-area", 196, 250, 260, 300, 10)
