#!/usr/bin/env python3
"""Targeted scans: dots, x-nodes, mesh, pills, hatch boxes, legend, Z row, query path."""
from PIL import Image
import numpy as np

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg"
A = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
X0, SX, SY = 17.63, 0.96123, 0.95657
def sl(x, y):
    return (round((x - X0) / SX, 1), round(y / SY, 1))

# 1. navy dots inside Dot Product box [289..375, 188..386]
sub = A[188:386, 289:375]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
navy = (b - r >= 30) & (b >= 90) & (r < 120) & (g < 120)
from scipy import ndimage
lab, n = ndimage.label(navy)
print("== navy dots in DotProduct box ==")
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 12: continue
    cx, cy = 289 + xs.mean(), 188 + ys.mean()
    print(f"   dot n={len(ys)} center frame ({cx:.1f},{cy:.1f}) slide {sl(cx, cy)} bbox f=[{289+xs.min()},{188+ys.min()},{289+xs.max()},{188+ys.max()}]")

# 2. red x-nodes in x 500..720, y 200..400
sub = A[200:400, 500:720]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
red = (r - g >= 60) & (r - b >= 50) & (r >= 140)
lab, n = ndimage.label(red)
print("== red comps x-nodes zone ==")
nodes = []
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 15: continue
    bb = [500 + xs.min(), 200 + ys.min(), 500 + xs.max(), 200 + ys.max()]
    w, h = bb[2] - bb[0] + 1, bb[3] - bb[1] + 1
    if 8 <= w <= 30 and 8 <= h <= 30 and 0.6 <= w / h <= 1.7:
        nodes.append(((500 + xs.mean(), 200 + ys.mean()), bb, len(ys)))
nodes.sort(key=lambda t: t[0][1])
for (c, bb, npx) in nodes:
    print(f"   node center ({c[0]:.1f},{c[1]:.1f}) slide {sl(*c)} bbox {bb} n={npx}")

# 3. red mesh lines inside Dot Product box (red thin, excluding dots region)
sub = A[210:390, 289:378]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
redm = (r - g >= 40) & (r - b >= 30) & (r >= 150)
print("== red mesh pixel count rows in DotProduct (y, count) ==")
for yy in range(0, sub.shape[0], 6):
    cnt = int(redm[yy].sum())
    if cnt > 3:
        xs = np.where(redm[yy])[0]
        print(f"   y={210+yy}: n={cnt} x {289+xs.min()}..{289+xs.max()}")

# 4. pills: sample grid rows y=150..180 at several x to find pill fills
print("== pill region samples (y=152..178) ==")
for (x, y) in [(300, 160), (310, 170), (330, 155), (400, 160), (420, 170),
               (500, 160), (510, 170), (560, 160), (620, 160), (650, 170), (680, 160)]:
    r, g, b = A[y, x]
    print(f"   ({x},{y}): #{r:02X}{g:02X}{b:02X}")

# 5. hatch boxes: redness density in y 100..215, x 60..280 and 700..900
print("== left hatch zone: red pixel counts per row (x 60..280) ==")
sub = A[100:215, 60:280]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
redm = (r - g >= 50) & (r - b >= 40) & (r >= 140)
for yy in range(0, sub.shape[0], 5):
    cnt = int(redm[yy].sum())
    if cnt > 5: print(f"   y={100+yy}: n={cnt}")
print("== right hatch zone: red pixel counts per row (x 700..900) ==")
sub = A[100:215, 700:900]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
redm = (r - g >= 50) & (r - b >= 40) & (r >= 140)
for yy in range(0, sub.shape[0], 5):
    cnt = int(redm[yy].sum())
    if cnt > 5: print(f"   y={100+yy}: n={cnt}")

# 6. legend box: pale-green fill bbox around x 700..900, y 420..510
sub = A[420:512, 690:900]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
pg = (np.abs(r - 204) <= 30) & (g >= 225) & (np.abs(b - 204) <= 30) & (g - r >= 12) & (g - b >= 12)
ys, xs = np.where(pg)
if len(ys):
    print(f"== legend pale-green bbox f=[{690+xs.min()},{420+ys.min()},{690+xs.max()},{420+ys.max()}] slide={sl(690+xs.min(),420+ys.min())}..{sl(690+xs.max(),420+ys.max())} n={len(ys)}")

# 7. Z row cells: PINK/MAG cells in [220..516, 459..495]
sub = A[459:496, 218:520]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
mag = (r >= 200) & (b >= 150) & (r - g >= 40) & (b - g >= 25)
lab, n = ndimage.label(mag)
print("== Z-row magenta/pink comps ==")
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 40: continue
    bb = [218 + xs.min(), 459 + ys.min(), 218 + xs.max(), 459 + ys.max()]
    print(f"   f={bb} w={bb[2]-bb[0]+1} h={bb[3]-bb[1]+1} n={len(ys)} slide x {sl(bb[0], bb[1])[0]}..{sl(bb[2], bb[3])[0]}")

# 8. query path: W_q box + q2 label — sample colors x 260..360, y 395..450
print("== W_q / q2 region samples ==")
for (x, y) in [(285, 410), (300, 410), (320, 410), (295, 400), (310, 425), (330, 430), (300, 440)]:
    r, g, b = A[y, x]
    print(f"   ({x},{y}): #{r:02X}{g:02X}{b:02X}")
# red text in query zone
sub = A[390:460, 260:370]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
redm = (r - g >= 60) & (r - b >= 50) & (r >= 140)
ys, xs = np.where(redm)
if len(ys):
    print(f"   red ink bbox f=[{260+xs.min()},{390+ys.min()},{260+xs.max()},{390+ys.max()}] n={len(ys)}")

# 9. O box region: x 540..690, y 100..150 — green pixels
sub = A[100:150, 530:700]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
grn = (g - r >= 40) & (g - b >= 40) & (g >= 130)
ys, xs = np.where(grn)
if len(ys):
    print(f"== O-box green ink bbox f=[{530+xs.min()},{100+ys.min()},{530+xs.max()},{100+ys.max()}] n={len(ys)} slide={sl(530+xs.min(),100+ys.min())}..{sl(530+xs.max(),100+ys.max())}")

# 10. green arrow between sigma and O: x 560..660, y 140..190
sub = A[138:192, 550:680]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
grn = (g - r >= 40) & (g - b >= 40) & (g >= 120)
ys, xs = np.where(grn)
if len(ys):
    print(f"== green arrow ink bbox f=[{550+xs.min()},{138+ys.min()},{550+xs.max()},{138+ys.max()}] n={len(ys)}")
