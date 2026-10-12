#!/usr/bin/env python3
"""m0_scan.py — structured geometry scan of 002:37 frame (960x540, 1px=1pt).
Finds the three green-bordered regions, their inner content rows, and key fills."""
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg"
img = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
H, W, _ = img.shape

def near(rgb, tol):
    return (np.abs(img - np.array(rgb)).sum(axis=2) <= tol)

def runs(mask_1d, min_len=2):
    out = []
    start = None
    for i, v in enumerate(mask_1d):
        if v and start is None:
            start = i
        elif not v and start is not None:
            if i - start >= min_len:
                out.append((start, i - 1))
            start = None
    if start is not None and len(mask_1d) - start >= min_len:
        out.append((start, len(mask_1d) - 1))
    return out

green = near((46, 125, 50), 110) | near((27, 114, 63), 110) | near((20, 130, 30), 110)

# --- vertical green strokes (frame borders): columns with many green px
colcnt = green.sum(axis=0)
rowcnt = green.sum(axis=1)
print("GREEN cols with >=40 px:", [(x, int(colcnt[x])) for x in np.where(colcnt >= 40)[0]])
print("GREEN rows with >=40 px:", [(y, int(rowcnt[y])) for y in np.where(rowcnt >= 40)[0]])

# --- panel fills: peach FBE5D6 and lt-green D5E8D4 mode per column band
peach = near((251, 229, 214), 24)
lgreen = near((213, 232, 212), 24)
print("PEACH col range:", runs(peach.sum(axis=0) > 30), " row range:", runs(peach.sum(axis=1) > 30))
print("LGREEN col range:", runs(lgreen.sum(axis=0) > 30), " row range:", runs(lgreen.sum(axis=1) > 30))

# --- title: red text pixels in top area (y<140, x<600)
red = near((204, 0, 0), 90) | near((192, 0, 0), 90)
topred = red[:150, :]
ys, xs = np.where(topred)
if len(xs):
    print(f"TITLE red ink: x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()} count {len(xs)}")
    # line bands
    rowc = topred.sum(axis=1)
    print("TITLE row bands:", runs(rowc > 2))

# --- orange boxes E8A33D
orange = near((232, 163, 61), 55)
print("ORANGE cols:", runs(orange.sum(axis=0) > 8))
print("ORANGE rows:", runs(orange.sum(axis=1) > 8))

# --- right panel: scan a horizontal line through the middle of the architecture (y=300)
for y in (120, 200, 300, 400, 480):
    row = img[y]
    segs = []
    prev = None
    start = 0
    def cls(p):
        r, g, b = p
        if abs(r-46)+abs(g-125)+abs(b-50) <= 110: return "GREEN"
        if abs(r-251)+abs(g-229)+abs(b-214) <= 30: return "peach"
        if abs(r-213)+abs(g-232)+abs(b-212) <= 30: return "lgreen"
        if abs(r-232)+abs(g-163)+abs(b-61) <= 60: return "orange"
        if abs(r-201)+abs(g-166)+abs(b-107) <= 60: return "tan"
        if r>235 and g>235 and b>235: return "white"
        if abs(r-216)+abs(g-160)+abs(b-184) <= 60: return "mauve"
        if abs(r-179)+abs(g-157)+abs(b-219) <= 60: return "lav"
        if r<60 and g<60 and b<60: return "dark"
        return f"({r},{g},{b})"
    cur = cls(row[0]); start = 0
    for x in range(1, W):
        c = cls(row[x])
        if c != cur:
            if x - start >= 3: segs.append((start, x-1, cur))
            cur = c; start = x
    if W - start >= 3: segs.append((start, W-1, cur))
    print(f"ROW y={y}:", segs)
