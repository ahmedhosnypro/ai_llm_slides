#!/usr/bin/env python3
# probe44_resume1.py — resume probe: settle open facts before fixing the build.
# (1) box fills (GROUP/INSTANCE/LAYER) + RT rect interior fill, (2) LEFT front extent,
# (3) GN salmon split, (4) badge cross-check, (5) title/header ink, (6) RT rect borders.
import numpy as np
from PIL import Image

F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_044.jpg").convert("RGB")
a = np.asarray(F).astype(int)
H, W = a.shape[:2]
print("frame", W, H)

def census(x0, x1, y0, y1, name):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    from collections import Counter
    q = Counter(map(tuple, reg))
    top = q.most_common(6)
    print(f"{name} ({x0},{y0})-({x1},{y1}):", " | ".join(f"{c}:{n}" for c, n in top))

# --- 1. box fills (interior, away from text/borders)
census(300, 440, 375, 385, "GROUP fill top strip")
census(300, 440, 430, 440, "GROUP fill bottom strip")
census(500, 850, 365, 372, "INSTANCE fill top strip")
census(500, 850, 435, 440, "INSTANCE fill bottom strip")
census(100, 600, 457, 465, "LAYER fill top strip")
census(100, 600, 490, 498, "LAYER fill bottom strip")
# RT rect interior: strips inside the rect away from the cube
census(663, 685, 100, 160, "RT rect interior left strip")
census(860, 893, 100, 160, "RT rect interior right strip")
census(700, 880, 335, 358, "RT rect interior bottom strip")
# panel reference
census(620, 640, 60, 80, "panel above cubes")

# --- 2. LEFT front face: salmon mask (r>190, 80<g<170, 60<b<160, r-g>60)
sal = (a[:,:,0] > 190) & (a[:,:,1] > 80) & (a[:,:,1] < 175) & (a[:,:,2] > 55) & (a[:,:,2] < 165) & ((a[:,:,0] - a[:,:,1]) > 60)
ys, xs = np.where(sal)
m = (xs > 30) & (xs < 280) & (ys > 150) & (ys < 460)
print("LEFT salmon bbox: x", xs[m].min(), xs[m].max(), " y", ys[m].min(), ys[m].max())
# column/row extent scans
for yy in (260, 300, 350, 400, 425):
    row = np.where(sal[yy, 30:280])[0] + 30
    print(f"  salmon row y{yy}: ", (row.min(), row.max(), len(row)) if len(row) else "none")
for xx in (80, 120, 160, 190, 200, 230, 250):
    col = np.where(sal[200:460, xx])[0] + 200
    print(f"  salmon col x{xx}: ", (col.min(), col.max(), len(col)) if len(col) else "none")

# --- 3. GN front split at y250 (magenta vs salmon boundary) + front extents
mag = (a[:,:,0] > 150) & (a[:,:,2] > 150) & (a[:,:,1] < 110)
ys2, xs2 = np.where(mag)
m2 = (xs2 > 260) & (xs2 < 430) & (ys2 > 170) & (ys2 < 345)
print("GN magenta bbox: x", xs2[m2].min(), xs2[m2].max(), " y", ys2[m2].min(), ys2[m2].max())
m3 = (xs2 > 440) & (xs2 < 580) & (ys2 > 190) & (ys2 < 360)
print("IN magenta bbox: x", xs2[m3].min(), xs2[m3].max(), " y", ys2[m3].min(), ys2[m3].max())
m4 = (xs2 > 670) & (xs2 < 830) & (ys2 > 150) & (ys2 < 340)
print("RT magenta bbox: x", xs2[m4].min(), xs2[m4].max(), " y", ys2[m4].min(), ys2[m4].max())
# GN salmon right part rows
for yy in (200, 250, 300, 330):
    row = np.where(sal[yy, 330:425])[0] + 330
    print(f"  GN salmon row y{yy}: ", (row.min(), row.max(), len(row)) if len(row) else "none")

# --- 4. badge cross-check
yel = (a[:,:,0] > 215) & (a[:,:,1] > 215) & (a[:,:,2] < 190)
ysb, xsb = np.where(yel)
mb = (xsb > 840) & (xsb < 910) & (ysb > 40) & (ysb < 110)
print("badge yellow bbox: x", xsb[mb].min(), xsb[mb].max(), " y", ysb[mb].min(), ysb[mb].max(),
      " center", (xsb[mb].min()+xsb[mb].max())/2, (ysb[mb].min()+ysb[mb].max())/2)

# --- 5. title ink (strict red, y40..85)
red = (a[:,:,0] > 140) & (a[:,:,1] < 110) & (a[:,:,2] < 110)
ysr, xsr = np.where(red)
mt = (xsr > 100) & (xsr < 900) & (ysr > 40) & (ysr < 86)
print("title red bbox: x", xsr[mt].min(), xsr[mt].max(), " y", ysr[mt].min(), ysr[mt].max())
# header blue ink (y85..170, x50..360)
blu = (a[:,:,2] > 120) & (a[:,:,2] - a[:,:,0] > 40) & (a[:,:,2] - a[:,:,1] > 30)
ysh, xsh = np.where(blu)
mh = (xsh > 50) & (xsh < 400) & (ysh > 85) & (ysh < 170)
print("header blue bbox: x", xsh[mh].min(), xsh[mh].max(), " y", ysh[mh].min(), ysh[mh].max())

# --- 6. RT rect borders: red-ish rows/cols in x640..910, y85..370
rish = (a[:,:,0] > 130) & ((a[:,:,0] - a[:,:,1]) > 40) & ((a[:,:,0] - a[:,:,2]) > 30)
ysr2, xsr2 = np.where(rish)
mr = (xsr2 > 640) & (xsr2 < 912) & (ysr2 > 85) & (ysr2 < 375)
print("RT red-ish bbox: x", xsr2[mr].min(), xsr2[mr].max(), " y", ysr2[mr].min(), ysr2[mr].max())
# top border row profile x700..800
for yy in range(90, 97):
    n = int(rish[yy, 700:800].sum())
    print(f"  red y{yy}: {n}", end="")
print()
for yy in range(360, 368):
    n = int(rish[yy, 700:800].sum())
    print(f"  red y{yy}: {n}", end="")
print()
for xx in range(655, 665):
    n = int(rish[150:300, xx].sum())
    print(f"  red x{xx}: {n}", end="")
print()
for xx in range(893, 903):
    n = int(rish[150:300, xx].sum())
    print(f"  red x{xx}: {n}", end="")
print()
