#!/usr/bin/env python3
"""Slide 030: per-box ink lines, segments, colors, highlights."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def classify(r, g, b):
    mx, mn = max(r, g, b), min(r, g, b)
    if mx - mn < 45 and mx > 190: return "bg"          # white/gray
    if r > 200 and g > 180 and b < 130: return "YELLOW"
    if g > 140 and g - r > 25 and g - b > 30: return "GREEN"
    if r > 120 and r - g > 55 and r - b > 45: return "red"
    if b > 100 and b - r > 40 and b - g > 30: return "blue"
    if mx < 110: return "black"
    if mx - mn < 60: return "bg"
    return "other"

C = np.zeros((H, W), dtype=object)
cmap = np.zeros((H, W, 3), dtype=np.int8)
pal = {"bg": 0, "black": 1, "red": 2, "blue": 3, "YELLOW": 4, "GREEN": 5, "other": 6}
names = {v: k for k, v in pal.items()}
flat = im.reshape(-1, 3)
cls = np.zeros(len(flat), dtype=np.int8)
for i, (r, g, b) in enumerate(flat):
    pass
# vectorized classify
r, g, b = R, G, B
mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b)
cls = np.zeros((H, W), dtype=np.int8)
cls[(mx - mn < 45) & (mx > 190)] = 0
cls[(r > 200) & (g > 180) & (b < 130)] = 4
cls[(g > 140) & (g - r > 25) & (g - b > 30)] = 5
cls[(r > 120) & (r - g > 55) & (r - b > 45)] = 2
cls[(b > 100) & (b - r > 40) & (b - g > 30)] = 3
cls[(mx < 110)] = 1
cls[(mx - mn < 60)] = np.where(cls[(mx - mn < 60)] == 0, 0, cls[(mx - mn < 60)])

def region_lines(name, x0, y0, x1, y1, ink_ids=(1, 2, 3), gap=4, min_gap_rows=1):
    sub = cls[y0:y1, x0:x1]
    ink = np.isin(sub, ink_ids)
    rows = ink.any(axis=1)
    print(f"== {name} (x{x0}..{x1} y{y0}..{y1})")
    lines = []
    y = 0
    while y < len(rows):
        if rows[y]:
            y2 = y
            blank = 0
            while y2 < len(rows) - 1:
                if rows[y2 + 1]: y2 += 1; blank = 0
                else:
                    blank += 1
                    if blank >= min_gap_rows and (y2 + 2 >= len(rows) or not rows[y2 + 2] or blank >= gap): break
                    y2 += 1
            band = ink[y:y2 + 1]
            cols = band.any(axis=0)
            xs = np.where(cols)[0]
            if len(xs):
                lb = (x0 + int(xs[0]), y0 + y, x0 + int(xs[-1]), y0 + y2)
                # color census in band
                kinds = {}
                for yy in range(y, y2 + 1):
                    for xx in range(lb[0] - x0, lb[2] - x0 + 1):
                        k = names[sub[yy, xx]]
                        if k not in ("bg",): kinds[k] = kinds.get(k, 0) + 1
                print(f"  line y{lb[1]}..{lb[3]} x{lb[0]}..{lb[2]}  colors {kinds}")
                lines.append(lb)
            y = y2 + 1
        else:
            y += 1
    return lines

def segments(name, band, x0, ink_ids=(1, 2, 3), minw=2):
    yy0, yy1 = band[1], band[3]
    sub = cls[yy0:yy1 + 1, :]
    ink = np.isin(sub, ink_ids)
    colproj = ink.sum(axis=0)
    segs = []
    x = x0
    while x < W:
        if colproj[x] > 0:
            x2 = x; blank = 0
            while x2 < W - 1:
                if colproj[x2 + 1] > 0: x2 += 1; blank = 0
                else:
                    blank += 1
                    if blank >= 4: break
                    x2 += 1
            if x2 - x >= minw - 1:
                bandink = ink[:, x:x2 + 1]
                ys = np.where(bandink.any(axis=1))[0]
                kinds = {}
                for yy in range(ys[0], ys[-1] + 1):
                    for xx in range(x, x2 + 1):
                        k = names[sub[yy, xx]]
                        if k != "bg": kinds[k] = kinds.get(k, 0) + 1
                segs.append((x, x2, yy0 + int(ys[0]), yy0 + int(ys[-1]), kinds))
            x = x2 + 1
        else:
            x += 1
    print(f"  segments of {name}:")
    for s in segs:
        print(f"    x{s[0]}..{s[1]} y{s[2]}..{s[3]} {s[4]}")
    return segs

# ---- vector box
vl = region_lines("VECTOR BOX", 92, 57, 372, 231)
# ---- remember box
rl = region_lines("REMEMBER BOX", 504, 106, 845, 183)
# ---- derivation box
dl = region_lines("DERIVATION BOX", 91, 246, 659, 322)
# ---- matrix box
ml = region_lines("MATRIX BOX", 90, 338, 614, 495)
# ---- green note box
gl = region_lines("GREEN NOTE BOX", 620, 336, 868, 478)
