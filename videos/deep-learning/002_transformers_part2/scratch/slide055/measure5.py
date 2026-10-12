#!/usr/bin/env python3
"""Final targeted scans for slide_055.jpg."""
from PIL import Image
import numpy as np
from scipy import ndimage

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg"
A = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
X0, SX, SY = 17.63, 0.96123, 0.95657
def sl(x, y): return (round((x - X0) / SX, 1), round(y / SY, 1))

# 1. x-nodes redo: red comps x 500..760, y 200..400, no aspect filter
sub = A[200:400, 500:760]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
red = (r - g >= 60) & (r - b >= 50) & (r >= 140)
lab, n = ndimage.label(red)
print("== red comps x 500..760 y 200..400 (n>=12) ==")
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 12: continue
    bb = [500 + int(xs.min()), 200 + int(ys.min()), 500 + int(xs.max()), 200 + int(ys.max())]
    print(f"   f={bb} {bb[2]-bb[0]+1}x{bb[3]-bb[1]+1} n={len(ys)} c=({500+xs.mean():.0f},{200+ys.mean():.0f})")

# 2. pills: pale yellow-green fill comps y 140..190
sub = A[140:190, 260:720]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
pill = (r >= 238) & (g >= 240) & (b >= 200) & (b <= 228) & (g - b >= 15)
lab, n = ndimage.label(pill)
print("== pale yellow-green pill comps y 140..190 x 260..720 ==")
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 60: continue
    bb = [260 + int(xs.min()), 140 + int(ys.min()), 260 + int(xs.max()), 140 + int(ys.max())]
    print(f"   f={bb} {bb[2]-bb[0]+1}x{bb[3]-bb[1]+1} n={len(ys)}")

# 3. K.q label bbox: red ink x 370..410, y 185..215
sub = A[183:218, 368:412]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
redm = (r - g >= 50) & (r - b >= 40) & (r >= 140)
ys, xs = np.where(redm)
if len(ys):
    print(f"== K.q label red bbox f=[{368+xs.min()},{183+ys.min()},{368+xs.max()},{183+ys.max()}] n={len(ys)}")

# 4. fraction bbox precise: red x 440..485, y 182..222
sub = A[180:224, 438:488]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
redm = (r - g >= 50) & (r - b >= 40) & (r >= 130)
ys, xs = np.where(redm)
print(f"== fraction red bbox f=[{438+xs.min()},{180+ys.min()},{438+xs.max()},{180+ys.max()}] n={len(ys)} slide {sl(438+xs.min(),180+ys.min())}..{sl(438+xs.max(),180+ys.max())}")

# 5. K strips + labels: what's between W_k (x 200..228) and DotProduct (x 289)?
print("== K strip zone samples (y=237 row) x 232..290 ==")
for x in range(232, 290, 3):
    rr, gg, bb2 = A[237, x]
    print(f"   ({x},237): #{rr:02X}{gg:02X}{bb2:02X}", end="")
print()
# red K labels: red ink x 232..290
sub = A[220:375, 230:292]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
redm = (r - g >= 50) & (r - b >= 40) & (r >= 140)
lab, n = ndimage.label(redm)
print("== red K-label comps in strip zone ==")
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 15: continue
    bb = [230 + int(xs.min()), 220 + int(ys.min()), 230 + int(xs.max()), 220 + int(ys.max())]
    print(f"   f={bb} n={len(ys)}")

# 6. Y container rows: dark/red cells inside yellow containers
sub = A[218:380, 101:181]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
dark = (r < 130) & (g < 130) & (b < 130)
lab, n = ndimage.label(dark)
print("== dark comps in left Y container ==")
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 10: continue
    bb = [101 + int(xs.min()), 218 + int(ys.min()), 101 + int(xs.max()), 218 + int(ys.max())]
    print(f"   f={bb} n={len(ys)}")

# 7. query zone detail: red ink comps x 260..370, y 385..460
sub = A[385:460, 260:370]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
redm = (r - g >= 50) & (r - b >= 40) & (r >= 140)
lab, n = ndimage.label(redm)
print("== red comps in query zone ==")
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 10: continue
    bb = [260 + int(xs.min()), 385 + int(ys.min()), 260 + int(xs.max()), 385 + int(ys.max())]
    print(f"   f={bb} n={len(ys)}")
# W_q box: dark text comps
dark = (r < 120) & (g < 120) & (b < 120)
lab, n = ndimage.label(dark)
print("== dark comps in query zone ==")
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 8: continue
    bb = [260 + int(xs.min()), 385 + int(ys.min()), 260 + int(xs.max()), 385 + int(ys.max())]
    print(f"   f={bb} n={len(ys)}")

# 8. caption zone: magenta text comps x 520..700, y 450..500
sub = A[450:500, 520:700]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
mag = (r >= 180) & (b >= 150) & (r - g >= 35) & (b - g >= 25)
lab, n = ndimage.label(mag)
print("== magenta comps in caption zone ==")
rows = []
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 6: continue
    rows.append((450 + int(ys.min()), 520 + int(xs.min()), 520 + int(xs.max()), 450 + int(ys.max()), len(ys)))
for rr in sorted(rows):
    print(f"   y={rr[0]}..{rr[3]} x {rr[1]}..{rr[2]} n={rr[4]}")

# 9. corridor scans for connectors (redness elevation vs panel baseline)
def corridor(name, x0, x1, y0, y1):
    sub = A[y0:y1, x0:x1]
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    redm = (r - g >= 40) & (r - b >= 30) & (r >= 150)
    print(f"== corridor {name} [{x0},{y0},{x1},{y1}] ==")
    for yy in range(0, sub.shape[0], 4):
        cnt = int(redm[yy].sum())
        if cnt > 2:
            xs = np.where(redm[yy])[0]
            print(f"   y={y0+yy}: n={cnt} x {x0+xs.min()}..{x0+xs.max()}")

corridor("K->dots", 266, 340, 220, 380)
corridor("softmax->nodes", 517, 560, 200, 380)
corridor("nodes->sigma", 540, 680, 205, 240)
corridor("V->nodes", 600, 680, 220, 380)
corridor("q2->dots", 290, 320, 340, 420)
corridor("Wv left-arrows", 690, 760, 220, 380)
