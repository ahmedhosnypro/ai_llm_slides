#!/usr/bin/env python3
"""Forensics 7: resolve ambiguities — raw dumps, modal fills, loose masks for thin strokes."""
import numpy as np
from PIL import Image
from collections import Counter

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_005.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def modal(x0, x1, y0, y1, label):
    patch = im[y0:y1, x0:x1].reshape(-1, 3)
    cnt = Counter(tuple(int(v) // 8 * 8 for v in p) for p in patch)
    top = cnt.most_common(3)
    avg = tuple(round(v, 1) for v in patch.mean(axis=0))
    print(f"{label}: avg {avg} modal {top}")

print("=== modal fills ===")
modal(175, 235, 182, 193, "WV cell1 interior")
modal(320, 380, 212, 224, "1stFM cell3 interior")
modal(320, 380, 385, 397, "1stFM cell13/14 interior")
modal(470, 525, 182, 193, "2ndFM cell1 interior")
modal(480, 515, 312, 334, "2ndFM center y312-334 (cyan?)")
modal(488, 505, 316, 326, "2ndFM narrow x488-505 y316-326")
modal(610, 665, 212, 224, "3rdFM cell3 interior (pink?)")
modal(750, 805, 182, 193, "4thFM cell1 interior")
modal(750, 805, 322, 334, "4thFM cell y322-334")
modal(755, 800, 226, 240, "4thFM x755-800 y226-240 (green?)")

print("\n=== 2nd FM raw row y=320, x456..537 (every 2px) ===")
row = im[320, 456:538]
print([f"{x+456}:{tuple(int(v) for v in row[x])}" for x in range(0, 82, 2)])

print("\n=== 4th FM raw row y=330, x737..818 (every 2px) ===")
row = im[330, 737:819]
print([f"{x+737}:{tuple(int(v) for v in row[x])}" for x in range(0, 82, 2)])

print("\n=== loose-red triangles in gaps ===")
loose_red = (r - g > 35) & (r - b > 35) & (r > 140)
for label, (xa, xb, ya, yb) in {
    "gap1 upper (cells1-3)": (246, 306, 176, 230),
    "gap1 lower (cells10-16)": (246, 306, 330, 400),
    "gap2 (tri3)": (539, 596, 300, 380),
    "gap3 (tri4)": (681, 735, 190, 280),
    "gap1 full": (246, 306, 176, 465),
    "gap2 full": (539, 596, 176, 465),
    "gap3 full": (681, 735, 176, 465),
    "gap0 (seq-blockarrow zone x246-306)": (246, 306, 295, 335),
}.items():
    m = loose_red[ya:yb, xa:xb]
    ys, xs = np.where(m)
    if len(xs):
        print(f"{label}: n={len(xs)} x {xs.min()+xa}..{xs.max()+xa} y {ys.min()+ya}..{ys.max()+ya}")
        # per-column min/max y to trace the triangle edges
        for xx in range(0, xb - xa, 6):
            col = np.where(m[:, xx])[0]
            if len(col):
                print(f"    x={xx+xa}: y {col.min()+ya}..{col.max()+ya}")
    else:
        print(f"{label}: EMPTY")

print("\n=== banner: yellowish top/bottom edge per column ===")
yel = (r > 225) & (g > 215) & (b < 200) & (r - b > 40)
for xx in range(580, 921, 40):
    col = np.where(yel[330:510, xx])[0]
    if len(col):
        print(f"  x={xx}: y {col.min()+330}..{col.max()+330} (n={len(col)})")
ys, xs = np.where(yel[330:510, 560:930])
print(f"banner yellow full: x {xs.min()+560}..{xs.max()+560} y {ys.min()+330}..{ys.max()+330}")

print("\n=== title bbox (chrome excluded) ===")
red = (r > 140) & (g < 110) & (b < 110)
m = red[50:145, 150:830]
ys, xs = np.where(m)
print(f"title: x {xs.min()+150}..{xs.max()+150} y {ys.min()+50}..{ys.max()+50}")
# row profile for cap-height
rows = np.where(m.sum(axis=1) > 2)[0]
print(f"title ink rows: {rows.min()+50}..{rows.max()+50}")

print("\n=== headers per stack (narrow windows) ===")
for nm, xa, xb in [("Words Vectors", 160, 260), ("1st FM", 300, 400), ("2nd FM", 450, 545), ("3rd FM", 590, 690), ("4th FM", 730, 825)]:
    m = red[145:180, xa:xb]
    ys, xs = np.where(m)
    print(f"{nm} header: x {xs.min()+xa}..{xs.max()+xa} y {ys.min()+145}..{ys.max()+145}")
    rowsum = m.sum(axis=1)
    lines = [y + 145 for y in range(35) if rowsum[y] > 0]
    # find line breaks
    brk = []
    prev = None
    for y in lines:
        if prev is not None and y - prev > 2:
            brk.append(prev)
        prev = y
    print(f"   line rows {lines[0]}..{lines[-1]}, breaks after {brk}")

print("\n=== seq arrow shaft vs label (red col profile x110-165) ===")
m = red[170:465, 110:165]
colsum = m.sum(axis=0)
for i, v in enumerate(colsum):
    if v > 0:
        print(f"  x={110+i}: {v}", end=";")
print()

print("\n=== bars: row RLE y=250 x395..460 ===")
row = im[250, 395:461]
prev = None
start = 395
for i, px in enumerate(row):
    key = tuple(int(v) // 24 for v in px)
    if key != prev:
        if prev is not None:
            print(f"  x{start}..{395+i-1}: avg {tuple(round(v,1) for v in im[250, start:395+i].mean(axis=0))}")
        prev = key
        start = 395 + i
print(f"  x{start}..{460}: avg {tuple(round(v,1) for v in im[250, start:461].mean(axis=0))}")

print("\n=== green callout box border (loose green) ===")
lg = (g - r > 25) & (g - b > 25) & (g > 110)
m = lg[100:160, 430:700]
ys, xs = np.where(m)
if len(xs):
    print(f"callout loose-green: x {xs.min()+430}..{xs.max()+430} y {ys.min()+100}..{ys.max()+100} n={len(xs)}")
# column profile to find the box edges
colsum = m.sum(axis=0)
cols = [i + 430 for i, v in enumerate(colsum) if v > 0]
print(f"green cols: {cols[:5]}...{cols[-5:] if len(cols)>5 else ''}")
rowsum = m.sum(axis=1)
rows_ = [i + 100 for i, v in enumerate(rowsum) if v > 0]
print(f"green rows: {rows_}")
# leader line below y160?
m2 = lg[160:200, 380:520]
ys2, xs2 = np.where(m2)
print(f"leader zone y160-200: " + (f"x {xs2.min()+380}..{xs2.max()+380} y {ys2.min()+160}..{ys2.max()+160} n={len(xs2)}" if len(xs2) else "EMPTY"))

print("\n=== kernel pictogram rows (salmon row profile x55-150) ===")
sal = (r > 225) & (g > 110) & (g < 200) & (b > 110) & (b < 200) & (r - b > 50)
m = sal[85:185, 55:150]
rowsum = m.sum(axis=1)
runs = []
s = p = None
for i, v in enumerate(rowsum):
    if v > 8:
        if s is None: s = p = i
        elif i == p + 1: p = i
        else: runs.append((s + 85, p + 85)); s = p = i
if s is not None: runs.append((s + 85, p + 85))
print(f"salmon row runs: {runs}")
ys, xs = np.where(m)
print(f"salmon bbox: x {xs.min()+55}..{xs.max()+55} y {ys.min()+85}..{ys.max()+85}")

print("\n=== caption details (blue + underline check) ===")
blue = (b > 120) & (r < 110) & (g < 110)
m = blue[500:535, 150:860]
ys, xs = np.where(m)
print(f"caption: x {xs.min()+150}..{xs.max()+150} y {ys.min()+500}..{ys.max()+500}")
rowsum = m.sum(axis=1)
for i, v in enumerate(rowsum):
    if v > 0:
        print(f"  y={500+i}: {v}", end=";")
print()

print("\n=== badge zone (yellow disc) ===")
yel2 = (r > 220) & (g > 215) & (b < 210) & (b > 120)
m = yel2[40:110, 850:930]
ys, xs = np.where(m)
print(f"badge yellow: x {xs.min()+850}..{xs.max()+850} y {ys.min()+40}..{ys.max()+40}")
