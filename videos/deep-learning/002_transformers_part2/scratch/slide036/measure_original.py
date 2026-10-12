#!/usr/bin/env python3
"""Measure slide_036.jpg original frame: chrome landmarks -> frame->slide mapping,
badge cross-check, and content ink bboxes (title, info panel, diagram: token rows,
banner, arrows, dots, caption). 002 frames are ~0.958 zoomed-out captures with a
black letterbox strip below (slide_002 header law)."""
from PIL import Image
import numpy as np

P = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_036.jpg"
im = Image.open(P).convert("RGB")
W, H = im.size
print(f"frame size: {W}x{H}")
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]

red    = (R > 130) & (G < 90) & (B < 90)
gray   = (abs(R - 233) < 12) & (abs(G - 233) < 12) & (abs(B - 231) < 14)
blue   = (B > 120) & (R < 110) & (G < 110)          # text/dot/arrow blue #0000CC/#0000FF
navy   = (R < 80) & (G < 80) & (B > 85) & (B < 170) # banner #000080
cream  = (R > 235) & (G > 235) & (B > 195) & (B < 245)  # info panel fill #FFFFE6
yellow = (R > 220) & (G > 215) & (B < 190)          # badge FDFD96 + caption FFFF00
brighty= (R > 225) & (G > 225) & (B < 90)           # caption highlight #FFFF00
pink   = (R > 215) & (G > 110) & (G < 200) & (B > 160)  # token lower cell #FF99CC
lyell  = (R > 225) & (G > 225) & (B > 110) & (B < 215)  # token upper cell #FFFF99
green  = (G > 120) & (R < 110) & (B < 130)          # green dots #00B050
maroon = (R > 90) & (R < 200) & (G < 70) & (B < 70) # caption text #990000?

# ---- letterbox rows
row_dark = ((R < 60) & (G < 60) & (B < 60)).sum(axis=1)
dark_rows = [y for y in range(H) if row_dark[y] > W * 0.8]
print("dark rows:", (dark_rows[:3], dark_rows[-3:]) if dark_rows else "none")

# ---- gray panel extents
gray_cols, gray_rows = gray.sum(axis=0), gray.sum(axis=1)
gcols = [x for x in range(W) if gray_cols[x] > 30]
grows = [y for y in range(H) if gray_rows[y] > 30]
print(f"gray panel cols {gcols[0]}..{gcols[-1]}  rows {grows[0]}..{grows[-1]}")

# ---- red border landmarks
red_cols, red_rows = red.sum(axis=0), red.sum(axis=1)
rcols = [x for x in range(W) if red_cols[x] > 50]
rrows = [y for y in range(H) if red_rows[y] > 50]
print(f"red long-run cols {rcols[:8]}...{rcols[-8:]}")
print(f"red long-run rows {rrows[:8]}...{rrows[-8:]}")

# ---- badge
ys, xs = np.where(yellow)
if len(xs):
    print(f"yellow(all) bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(xs)}")

def band_report(mask, name, minpx=30, gap=3):
    """row-band clusters of a mask with x-extent + column clusters per band"""
    mys, mxs = np.where(mask)
    if not len(mys):
        print(f"[{name}] EMPTY")
        return
    rows = sorted(set(mys))
    bands = []
    s0 = p = rows[0]
    for y in rows[1:]:
        if y - p > gap:
            bands.append((s0, p)); s0 = y
        p = y
    bands.append((s0, p))
    print(f"[{name}] bands:")
    for (y0, y1) in bands:
        m = (mys >= y0) & (mys <= y1)
        if m.sum() < minpx:
            continue
        xl = np.sort(mxs[m])
        cl = []
        cs = cp = xl[0]
        for x in xl[1:]:
            if x - cp > 10:
                cl.append((cs, cp)); cs = x
            cp = x
        cl.append((cs, cp))
        print(f"  y {y0}..{y1} h={y1-y0+1} n={m.sum()} x {xl.min()}..{xl.max()} ncols={len(cl)}")
        if len(cl) <= 26:
            print(f"    xclusters={cl}")
        else:
            print(f"    xclusters(first8)={cl[:8]} ... last4={cl[-4:]}")

band_report(red, "RED ink", 25)
band_report(blue, "BLUE ink", 25, gap=4)
band_report(navy, "NAVY banner", 200, gap=4)
band_report(pink, "PINK token cells", 15, gap=4)
band_report(lyell, "LIGHTYELLOW token cells", 15, gap=4)
band_report(green, "GREEN dots", 3, gap=3)
band_report(brighty, "BRIGHT-YELLOW caption hl", 40, gap=4)
band_report(cream, "CREAM panel fill", 200, gap=4)
band_report(maroon, "MAROON-ish ink", 5, gap=3)
