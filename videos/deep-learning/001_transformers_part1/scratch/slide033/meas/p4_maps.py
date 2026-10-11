#!/usr/bin/env python3
"""Slide 033 pass 4: ASCII ink maps (4x4 downsample) + targeted bounds scans."""
from PIL import Image
import numpy as np
from collections import Counter

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
H, W = A.shape[:2]
R, G, B = A[:,:,0], A[:,:,1], A[:,:,2]

def amap(name, m, x0=0, x1=959, y0=0, y1=539, step=4):
    print(f"--- {name} ---")
    for yy in range(y0, y1+1, step):
        row = ""
        for xx in range(x0, x1+1, step):
            blk = m[yy:yy+step, xx:xx+step]
            f = blk.mean()
            row += "#" if f > 0.55 else ("+" if f > 0.25 else ("." if f > 0.06 else " "))
        print(f"{yy:3d} {row}")

# red arrows/emphasis: strong red, dark-ish
red = (R > 130) & (G < 95) & (B < 95)
# dark red text 8B0000-ish
dred = (R > 90) & (R < 190) & (G < 60) & (B < 60)
# green ink (dashed borders/arrows): green dominant
green = (G > 110) & (R < 110) & (B < 130) & (G - R > 40) & (G - B > 25)
# dark blue ink (dots, sigma, W labels?)
dblue = (B > 110) & (R < 90) & (G < 100) & (B - R > 60)
# yellow boxes
yellow = (R > 215) & (G > 215) & (B < 160) & (B > 60)
# white (boxes/circles)
white = (R > 240) & (G > 240) & (B > 240)
# magenta-ish (X2 highlight border / pink cells)
mag = (R > 150) & (B > 130) & (G < 120) & (R - G > 60) & (B - G > 30)
# any dark ink (text)
dark = (R < 130) & (G < 130) & (B < 130)

amap("RED (arrows/circle/blockarrow)", red, 40, 930, 100, 540)
amap("GREEN (dashed/labels)", green, 40, 930, 100, 540)
