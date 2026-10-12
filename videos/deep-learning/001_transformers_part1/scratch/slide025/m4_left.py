#!/usr/bin/env python3
"""Focused measurements: bracket greens, circle geometry+colors, title bands,
box edges — printed compactly."""
import sys
import numpy as np
from PIL import Image

im = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def hdr(s):
    print(f"\n===== {s} =====")

# --- LEFT PANEL: green bracket pixels ---
hdr("LEFT panel green pixels (G: g>r+40,g>b+25, g in 110..210)")
mask = (g > r + 40) & (g > b + 25) & (g > 110) & (g < 215) & (r < 140)
sub = mask[200:530, 40:215]
ys, xs = np.where(sub)
if len(ys):
    print(f"green bbox in region: x{xs.min()+40}-{xs.max()+40} y{ys.min()+200}-{ys.max()+200} n={len(ys)}")
    # cluster rows
    rows = sorted(set(ys + 200))
    print(f"rows with green: {rows[:6]}...{rows[-6:]}")
    cols = sorted(set(xs + 40))
    print(f"cols with green: {cols[:10]}...{cols[-10:]}")
    # print corner clusters
    for name, (ya, yb, xa, xb) in {
        "TL": (255, 290, 45, 80), "TR": (255, 290, 170, 205),
        "BL": (470, 505, 45, 80), "BR": (470, 505, 170, 205),
    }.items():
        m = mask[ya:yb, xa:xb]
        yy, xx = np.where(m)
        if len(yy):
            print(f"  {name}: x{xx.min()+xa}-{xx.max()+xa} y{yy.min()+ya}-{yy.max()+ya} n={len(yy)}")
        else:
            print(f"  {name}: none")
# sample green color
pts = [(y, x) for y, x in zip(ys, xs)][:5]
for y, x in pts[:3]:
    p = im[y + 200, x + 40]
    print(f"  green px ({x+40},{y+200}) = #{p[0]:02X}{p[1]:02X}{p[2]:02X}")

# --- LEFT circles: colored blobs y445-495 ---
hdr("LEFT circles y440-500")
for name, m in {
    "red": (r > 150) & (g < 110) & (b < 110),
    "blue": (b > r + 40) & (b > 100) & (r < 120),
    "purple": (r > 70) & (r < 170) & (b > g + 40) & (b > 110),
}.items():
    sub = m[440:500, 44:210]
    yy, xx = np.where(sub)
    if len(yy):
        print(f"  {name}: x{xx.min()+44}-{xx.max()+44} y{yy.min()+440}-{yy.max()+440} n={len(yy)}")

# circle center colors
hdr("LEFT circle interior samples")
for nm, cx, cy in [("Q", 90, 473), ("Q2", 88, 468), ("K", 128, 473), ("K2", 126, 466), ("V", 166, 473), ("V2", 164, 466), ("V3", 170, 480)]:
    p = im[cy, cx]
    print(f"  {nm} ({cx},{cy}) #{p[0]:02X}{p[1]:02X}{p[2]:02X}")

# --- LEFT title band: red text rows ---
hdr("LEFT title red rows (x46-206)")
mred = (r > 140) & (g < 90) & (b < 90)
for y in range(228, 275):
    n = mred[y, 46:207].sum()
    if n > 3:
        xs2 = np.where(mred[y, 46:207])[0]
        print(f"  y={y}: n={n} x{xs2.min()+46}-{xs2.max()+46}")

# --- LEFT boxes: beige mask bbox per box ---
hdr("LEFT beige boxes (E8D5B5-family)")
mbeige = (abs(r - 232) < 22) & (abs(g - 213) < 22) & (abs(b - 181) < 22) & (r > g) & (g > b)
from scipy import ndimage
lab, n = ndimage.label(mbeige[210:530, 44:210])
for i in range(1, n + 1):
    yy, xx = np.where(lab == i)
    if len(yy) < 150:
        continue
    # interior mode color
    y0b, y1b, x0b, x1b = yy.min() + 210, yy.max() + 210, xx.min() + 44, xx.max() + 44
    inner = im[y0b + 2:y1b - 2, x0b + 2:x1b - 2].reshape(-1, 3)
    med = np.median(inner, axis=0).astype(int)
    print(f"  box x{x0b}-{x1b} y{y0b}-{y1b} (w{x1b-x0b+1} h{y1b-y0b+1}) n={len(yy)} fill #{med[0]:02X}{med[1]:02X}{med[2]:02X}")

# --- LEFT panel bounds (T fill) ---
hdr("LEFT panel T-fill bounds")
mT = (abs(r - 224) < 16) & (abs(g - 170) < 16) & (abs(b - 117) < 18)
sub = mT[200:535, 40:215]
yy, xx = np.where(sub)
print(f"  T bbox x{xx.min()+40}-{xx.max()+40} y{yy.min()+200}-{yy.max()+200}")
# left/right edge columns at y=350
row = mT[350, 40:215]
xs3 = np.where(row)[0]
print(f"  y=350 T run x{xs3.min()+40}-{xs3.max()+40}")
col = mT[200:535, 120]
ys3 = np.where(col)[0]
print(f"  x=120 T run y{ys3.min()+200}-{ys3.max()+200}")

# --- LEFT panel border color ---
hdr("LEFT panel border sample (edges)")
for x in [43, 44, 45, 46, 47]:
    p = im[350, x]
    print(f"  ({x},350) #{p[0]:02X}{p[1]:02X}{p[2]:02X}")
for y in [208, 209, 210, 211, 212, 521, 522, 523, 524]:
    p = im[y, 120]
    print(f"  (120,{y}) #{p[0]:02X}{p[1]:02X}{p[2]:02X}")
