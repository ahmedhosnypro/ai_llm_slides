#!/usr/bin/env python3
"""Pass 6: map the bottom-right backprop panel precisely — block mode colors,
red border lines, white regions, pink chain, green boxes, nabla squares."""
from PIL import Image
import numpy as np
from scipy import ndimage

B = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_009.jpg"
bi = np.asarray(Image.open(B).convert("RGB"), dtype=np.int16)
R, G, Bl = bi[:,:,0], bi[:,:,1], bi[:,:,2]

# block-mode grid over x480..940 y275..520, 10px blocks
print("== BLOCK MODE GRID (x480..940 step10 / y275..520 step10) ==")
print("legend: W=white(>248) P=panelgray(229..236 all) g=warmgray(B<228,G>222) r=red k=dark .=other")
for y0 in range(275, 520, 10):
    row = []
    for x0 in range(480, 940, 10):
        reg = bi[y0:y0+10, x0:x0+10].reshape(-1, 3)
        vals, counts = np.unique(reg, axis=0, return_counts=True)
        c = tuple(int(v) for v in vals[np.argmax(counts)])
        r, g, b = c
        if r > 160 and g < 90 and b < 90: ch = "r"
        elif r < 100 and g < 100 and b < 100: ch = "k"
        elif r > 248 and g > 248 and b > 248: ch = "W"
        elif 229 <= r <= 238 and 229 <= g <= 238 and 229 <= b <= 238: ch = "P"
        elif r > 222 and g > 222 and b < 228: ch = "g"
        else: ch = "."
        row.append(ch)
    print(f"  y{y0:3d} {''.join(row)}")
print("          " + "".join(str((480 + i*10) // 100 % 10) for i in range(46)))

print("== RED INK components in bottom-right (x480..940 y275..520) ==")
red = (R > 140) & (G < 100) & (Bl < 100)
sub = np.zeros_like(red); sub[275:520, 480:940] = red[275:520, 480:940]
lab, n = ndimage.label(sub, structure=np.ones((3,3)))
objs = ndimage.find_objects(lab)
res = []
for i, sl in enumerate(objs):
    area = int((lab[sl] == i+1).sum())
    if area >= 25:
        ys, xs = sl
        res.append((area, xs.start, ys.start, xs.stop, ys.stop))
res.sort(reverse=True)
for area, x0, y0, x1, y1 in res[:25]:
    print(f"  area={area:5d} x{x0}..{x1} y{y0}..{y1} (w{x1-x0} h{y1-y0})")

print("== PINK chain (F8BBD0-ish) ==")
pink = (np.abs(R-248)<25) & (np.abs(G-187)<30) & (np.abs(Bl-208)<30)
sub = np.zeros_like(pink); sub[275:520, 480:940] = pink[275:520, 480:940]
lab, n = ndimage.label(sub, structure=np.ones((3,3)))
objs = ndimage.find_objects(lab)
res = []
for i, sl in enumerate(objs):
    area = int((lab[sl] == i+1).sum())
    if area >= 60:
        ys, xs = sl
        res.append((xs.start, ys.start, xs.stop, ys.stop, area))
res.sort()
for x0, y0, x1, y1, area in res[:20]:
    print(f"  x{x0}..{x1} y{y0}..{y1} (w{x1-x0} h{y1-y0}) area={area}")

print("== GREEN boxes (D5E8D5 fill, 7AA87A border) ==")
green = (np.abs(R-213)<18) & (np.abs(G-232)<15) & (np.abs(Bl-213)<18)
sub = np.zeros_like(green); sub[275:520, 480:940] = green[275:520, 480:940]
lab, n = ndimage.label(sub, structure=np.ones((3,3)))
objs = ndimage.find_objects(lab)
res = []
for i, sl in enumerate(objs):
    area = int((lab[sl] == i+1).sum())
    if area >= 60:
        ys, xs = sl
        res.append((xs.start, ys.start, xs.stop, ys.stop, area))
res.sort()
for x0, y0, x1, y1, area in res[:20]:
    print(f"  x{x0}..{x1} y{y0}..{y1} (w{x1-x0} h{y1-y0}) area={area}")

print("== NABLA squares (white fill + red border, black ∇) — row band y? ==")
# find red-bordered small squares: red mask density per row in x520..910
rows = red[300:480, 500:920].sum(axis=1)
s = None
print("  red row bands y300..480 (count>30):")
for i, v in enumerate(rows):
    if v >= 30 and s is None: s = i
    elif v < 30 and s is not None:
        print(f"    y{s+300}..{i+300} (peak {int(rows[s:i].max())})"); s = None
if s is not None: print(f"    y{s+300}..480")
