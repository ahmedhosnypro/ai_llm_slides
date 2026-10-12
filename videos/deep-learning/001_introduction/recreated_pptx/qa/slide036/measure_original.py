#!/usr/bin/env python3
"""Measure slide_036.jpg ground truth (960x540, 1px = 1pt). Pass 1: coarse element bboxes."""
from PIL import Image
import numpy as np
from collections import Counter

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_036.jpg"
im = Image.open(IM).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"size {W}x{H}")

def modal(x0, y0, x1, y1, min_sat=0):
    r = a[y0:y1, x0:x1].reshape(-1, 3)
    c = Counter(map(tuple, r))
    return c.most_common(6)

def bbox_dark(x0, y0, x1, y1, thresh=140, name=""):
    """ink bbox of dark pixels in region"""
    sub = a[y0:y1, x0:x1]
    lum = sub.sum(axis=2) / 3
    ys, xs = np.where(lum < thresh)
    if len(xs) == 0:
        print(f"{name}: EMPTY"); return None
    bb = (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())
    print(f"{name}: x {bb[0]}..{bb[2]}  y {bb[1]}..{bb[3]}  ({bb[2]-bb[0]+1}x{bb[3]-bb[1]+1})")
    return bb

def bbox_col(x0, y0, x1, y1, target, tol, name=""):
    """ink bbox of pixels within tol of target color"""
    sub = a[y0:y1, x0:x1]
    d = np.abs(sub - np.array(target)).sum(axis=2)
    ys, xs = np.where(d <= tol)
    if len(xs) == 0:
        print(f"{name}: EMPTY"); return None
    bb = (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())
    print(f"{name}: x {bb[0]}..{bb[2]}  y {bb[1]}..{bb[3]}  ({bb[2]-bb[0]+1}x{bb[3]-bb[1]+1}) n={len(xs)}")
    return bb

print("\n== background / panel ==")
print("corner 5,5:", a[5, 5], " 480,5:", a[5, 480])
print("panel sample 480,300:", a[300, 480], " inside-box 480,250:", a[250, 480])
print("panel modal (60..900, 50..150):", modal(60, 50, 900, 150)[:3])
print("above-panel rows 40..50 col 480:", [tuple(a[y, 480]) for y in range(38, 52)])
print("panel border col scan x 30..70 at y=300:", [tuple(a[300, x]) for x in range(30, 75, 2)])
print("panel border col scan x 900..930 at y=300:", [tuple(a[300, x]) for x in range(900, 931, 2)])
print("panel border row scan y 40..55 at x=480:", [tuple(a[y, 480]) for y in range(40, 56)])
print("bottom rows 520..540 at x=480:", [tuple(a[y, 480]) for y in range(520, 540, 2)])

print("\n== title ==")
bbox_dark(100, 50, 900, 145, 150, "title ink (dark<150)")
r = a[50:145, 100:900].reshape(-1, 3)
red_mask = (r[:, 0] > 100) & (r[:, 0] > r[:, 1] * 1.8) & (r[:, 0] > r[:, 2] * 1.8)
print("title red pixels:", red_mask.sum(), "modal of red:", Counter(map(tuple, r[red_mask])).most_common(4))
# line split: row profile of dark pixels
sub = a[45:150, 100:900]
lum = sub.sum(axis=2) / 3
rows = (lum < 150).sum(axis=1)
print("title row profile (y45..149):", [(45 + i, int(v)) for i, v in enumerate(rows) if v > 0])

print("\n== white box ==")
print("row y=200 x 100..140:", [tuple(a[200, x]) for x in range(105, 135, 2)])
print("row y=200 x 830..860:", [tuple(a[200, x]) for x in range(830, 856, 2)])
print("col x=480 y 145..175:", [tuple(a[y, 480]) for y in range(145, 176, 2)])
print("col x=480 y 490..520:", [tuple(a[y, 480]) for y in range(490, 521, 2)])
white = (np.abs(a - 255).sum(axis=2) < 30)
ys, xs = np.where(white)
print("pure-white bbox (whole slide):", xs.min(), ys.min(), xs.max(), ys.max())

print("\n== RGB label ==")
bbox_dark(250, 150, 450, 210, 120, "RGB label")
print("modal RGB label ink:", modal(280, 160, 400, 205)[:4])

print("\n== input slab (orange) ==")
orange = np.abs(a - np.array([192, 112, 40])).sum(axis=2) < 160
ys, xs = np.where(orange)
print("orange-ish bbox:", xs.min(), ys.min(), xs.max(), ys.max(), "n=", len(xs))
print("modal orange region:", modal(220, 240, 360, 360)[:5])
# top face darker
dark_or = np.abs(a - np.array([138, 77, 21])).sum(axis=2) < 160
ys, xs = np.where(dark_or)
print("dark-orange bbox:", xs.min(), ys.min(), xs.max(), ys.max(), "n=", len(xs))
# scan slab edges: orange presence per column at y=300
for x in range(205, 380, 5):
    col = a[200:400, x]
    om = (np.abs(col - np.array([192, 112, 40])).sum(axis=1) < 160)
    print(f"  col x={x}: orange rows {200+np.where(om)[0].min() if om.any() else '-'}..{200+np.where(om)[0].max() if om.any() else '-'}")

print("\n== cyan column on slab face ==")
cyan = np.abs(a - np.array([41, 171, 226])).sum(axis=2) < 200
ys, xs = np.where(cyan[200:400, 200:380])
print("cyan-in-slab bbox:", (200 + xs.min(), 200 + ys.min(), 200 + xs.max(), 200 + ys.max()) if len(xs) else "EMPTY", "n=", len(xs))
