#!/usr/bin/env python3
"""probe9 — Net_i/Net_j ink metrics, j-arrow head, letter bboxes, mesh spot-checks."""
from PIL import Image
import numpy as np

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r_, g_, b_ = a[:,:,0], a[:,:,1], a[:,:,2]
redish = (r_>120) & (g_<90) & (b_<90)
dark = a.sum(axis=2) < 330

def bbox(m, x0, x1, y0, y1):
    sub = m[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs) == 0: return None
    return (x0+int(xs.min()), y0+int(ys.min()), x0+int(xs.max()), y0+int(ys.max()), int(len(xs)))

print("== Net_i ink rows (x204..248, red) ==")
for y in range(140, 170):
    n = redish[y, 204:249].sum()
    if n: print(f"  y{y}: {n}")
print("== Net_j ink rows (x370..413, red) ==")
for y in range(140, 170):
    n = redish[y, 370:414].sum()
    if n: print(f"  y{y}: {n}")
print("== Net_i cols (y142..167) ==", end=" ")
cols = [x for x in range(204, 249) if redish[142:167, x].sum()]
print(cols)
print("== Net_j cols ==", end=" ")
cols = [x for x in range(370, 414) if redish[142:167, x].sum()]
print(cols)

print("== j arrow head rows (x400..460 classified F/D) ==")
for y in range(364, 400):
    s = "".join(("F" if (abs(a[y,x,0]-215)<14 and a[y,x,1]>243 and abs(a[y,x,2]-180)<16)
                 else "D" if a[y,x].sum() < 400 else ".") for x in range(400, 461))
    if "F" in s or "D" in s: print(f"  y{y}: {s}")

print("== letter bboxes (dark on arrow shafts) ==")
print("  i letter:", bbox(dark, 259, 268, 370, 399))
print("  j letter:", bbox(dark, 423, 436, 370, 399))
print("== O_i r1/r2/r3 ink rows (x276..300 red, excluding port x>279&y>175) ==")
for (y0, y1, x0, x1) in [(158, 192, 276, 300), (228, 262, 274, 298), (310, 344, 272, 295)]:
    sub = redish[y0:y1, x0:x1]
    for yy in range(y1-y0):
        n = sub[yy].sum()
        if n: print(f"  band{y0}: y{y0+yy}: {n}")
    print("  ---")
print("== O_j r1 ink rows (x444..468) ==")
for yy in range(160, 192):
    n = redish[yy, 444:469].sum()
    if n: print(f"  y{yy}: {n}")

print("== mesh line spot checks (red px at midpoints of 9 lines) ==")
c1, c2 = 261.5, 427.0
r = 21
rows = [182.5, 254.5, 336.0]
for cy0 in rows:
    for cy1 in rows:
        x0, y0 = c1 + r, cy0
        x1, y1 = c2 - r - 1, cy1
        xm = (x0+x1)/2; ym = (y0+y1)/2
        cnt = redish[int(ym)-2:int(ym)+3, int(xm)-3:int(xm)+4].sum()
        print(f"  ({cy0}->{cy1}) mid({xm:.0f},{ym:.0f}): red={cnt}")
print("== arrowhead clusters at col2 left rim (red px x400..412 per row) ==")
for yy in range(160, 370, 4):
    n = redish[yy, 400:413].sum()
    if n > 3: print(f"  y{yy}: {n}")
