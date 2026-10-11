#!/usr/bin/env python3
"""PIL forensics on slide_005.jpg (960x540, 1px = 1pt) — column profiles."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_005.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]
print(f"size {W}x{H}")
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# color classes (JPEG-soft)
def cls(name, mask):
    ys, xs = np.where(mask)
    print(f"{name}: {len(xs)} px", end="")
    if len(xs):
        print(f"  x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}")
    else:
        print()

red    = (r > 140) & (g < 110) & (b < 110)                       # title/arrows/outline
yellow = (r > 200) & (g > 190) & (b < 200) & (abs(r-g) < 70)     # FFFFCC cells + banner
peach  = (r > 200) & (g > 150) & (g < 220) & (b > 110) & (b < 190)  # FFCC99
cyan   = (b > 200) & (g > 200) & (r < 200)                        # 99FFFF
pink   = (r > 220) & (g > 170) & (g < 230) & (b > 220)            # FFCCFF
pgreen = (g > 200) & (b > 180) & (b < 230) & (r > 170) & (r < 230)  # CCFFCC
graybar= (abs(r-191) < 25) & (abs(g-191) < 25) & (abs(b-191) < 25)  # BFBFBF
blue   = (b > 120) & (r < 100) & (g < 100)                        # 0000CC text
green  = (g > 120) & (r < 120) & (b < 120)                        # 00A000
salmon = (r > 220) & (g > 110) & (g < 180) & (b > 110) & (b < 180)  # FF9999 kernel

cls("red", red); cls("yellowFFFFCC/banner", yellow); cls("peach", peach)
cls("cyan", cyan); cls("pink", pink); cls("palegreen", pgreen)
cls("graybar", graybar); cls("blue", blue); cls("green", green); cls("salmon", salmon)

# column profile of the five cell-stack regions: scan y 170..470 (pipeline band)
band = np.s_[170:470]
print("\n--- column profile in band y170..470 ---")
for name, m in [("yellow", yellow), ("peach", peach), ("cyan", cyan), ("pink", pink), ("palegreen", pgreen), ("graybar", graybar)]:
    colsum = m[band].sum(axis=0)
    runs_, s, p = [], None, None
    for i, v in enumerate(colsum):
        if v > 3:
            if s is None: s = p = i
            elif i == p+1: p = i
            else: runs_.append((s,p)); s = p = i
    if s is not None: runs_.append((s,p))
    print(f"{name}: runs(x ranges with >3px in band) {runs_}")

# red column profile (cell outlines / arrows / title)
print("\n--- red column profile y170..470 (outlines etc.) ---")
colsum = red[band].sum(axis=0)
strong = np.where(colsum > 30)[0]
runs_, s, p = [], None, None
for i in strong:
    if s is None: s = p = i
    elif i == p+1: p = i
    else: runs_.append((s,p)); s = p = i
if s is not None: runs_.append((s,p))
print(f"red vertical-line columns (>30px tall in band): {runs_}")
