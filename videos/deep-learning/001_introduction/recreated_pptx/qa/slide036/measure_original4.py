#!/usr/bin/env python3
"""Measure pass 4: vertical/horizontal color profiles to nail face structure + fine scans."""
from PIL import Image
import numpy as np
from collections import Counter

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_036.jpg"
a = np.asarray(Image.open(IM).convert("RGB")).astype(int)
lum = a.sum(axis=2) / 3

def prof_v(x, y0, y1, step=1):
    print(f"-- vertical profile x={x} --")
    prev = None
    for y in range(y0, y1, step):
        c = tuple(a[y, x])
        if prev is None or sum(abs(c[i] - prev[i]) for i in range(3)) > 40:
            print(f"  y={y}: {c}")
            prev = c

def prof_h(y, x0, x1, step=1):
    print(f"-- horizontal profile y={y} --")
    prev = None
    for x in range(x0, x1, step):
        c = tuple(a[y, x])
        if prev is None or sum(abs(c[i] - prev[i]) for i in range(3)) > 40:
            print(f"  x={x}: {c}")
            prev = c

prof_v(320, 195, 330)   # through slab: top face + main face
prof_v(250, 255, 400)   # through slab left part + column
prof_v(235, 270, 350)   # through left face strip
prof_v(450, 240, 345)   # through filter: top face + main face
prof_v(420, 260, 345)   # through filter left face
prof_h(300, 215, 370)   # across slab: left face -> main face -> right edge
prof_h(210, 240, 365)   # across slab top area

print("\n== dash inventory x 358..386 (gap between slab and X) ==")
dm = np.abs(a - np.array([80, 185, 210])).sum(axis=2) < 190
sub = dm[240:345, 358:386]
rows = sub.sum(axis=1)
bands = []
inb = False
for i, v in enumerate(rows):
    if v > 1 and not inb: s = i; inb = True
    elif v <= 1 and inb: bands.append((240 + s, 240 + i - 1)); inb = False
if inb: bands.append((240 + s, 344))
print("bands:", bands)
for b in bands:
    yc = (b[0] + b[1]) // 2
    xs = np.where(dm[yc, 220:420])[0]
    print(f"  band {b}: full-x {220+xs.min()}..{220+xs.max()}" if len(xs) else f"  band {b}: -")

print("\n== dash core color (rows 282..285, x 362..414 darkest) ==")
sub = a[282:286, 362:414].reshape(-1, 3)
sub = sub[sub.sum(axis=1) < 620]
print(Counter(map(tuple, sub)).most_common(8))

print("\n== X core color (y 247..252 + y 259..263, x 388..412) ==")
sub = np.vstack([a[247:253, 388:412].reshape(-1, 3), a[258:264, 388:412].reshape(-1, 3)])
sub = sub[sub.sum(axis=1) < 640]
print(Counter(map(tuple, sub)).most_common(8))

print("\n== neuron: orange ring + cyan center clean samples ==")
sub = a[293:300, 574:581].reshape(-1, 3)  # ring left
print("ring-left:", Counter(map(tuple, sub)).most_common(4))
sub = a[293:300, 586:600].reshape(-1, 3)  # center
print("center:", Counter(map(tuple, sub)).most_common(4))
# outer ring bbox via any-strong-color
m = ((np.abs(a - np.array([230, 135, 35])).sum(axis=2) < 160) | (np.abs(a - np.array([20, 185, 235])).sum(axis=2) < 160))
sub = m[270:320, 565:625]
ys, xs = np.where(sub)
print("neuron overall bbox:", (565 + xs.min(), 270 + ys.min(), 565 + xs.max(), 270 + ys.max()))
for y in range(278, 316, 2):
    r = np.where(m[y, 565:625])[0]
    if len(r): print(f"  y={y}: x {565+r.min()}..{565+r.max()}")

print("\n== equation red core ==")
sub = a[450:480, 329:594].reshape(-1, 3)
red = sub[(sub[:, 0] > 140) & (sub[:, 1] < 110) & (sub[:, 2] < 110)]
print(Counter(map(tuple, red)).most_common(6))

print("\n== title red core (big strokes) ==")
sub = a[61:90, 156:800].reshape(-1, 3)
red = sub[(sub[:, 0] > 120) & (sub[:, 0] < 210) & (sub[:, 1] < 60) & (sub[:, 2] < 70)]
print(Counter(map(tuple, red)).most_common(6))

print("\n== 3dims arrow rows (y 262..278, x 188..285) ==")
for y in range(262, 279):
    r = np.where(lum[y, 188:285] < 120)[0]
    if len(r): print(f"  y={y}: x {188+r.min()}..{188+r.max()} n={len(r)}")

print("\n== 7left tiny arrow rows (y 298..324, x 220..248) ==")
for y in range(298, 325):
    r = np.where(lum[y, 220:248] < 150)[0]
    if len(r): print(f"  y={y}: x {220+r.min()}..{220+r.max()} n={len(r)}")

print("\n== 7bottom glyph+arrow rows (y 313..350, x 240..280) ==")
for y in range(313, 350):
    r = np.where(lum[y, 240:280] < 150)[0]
    if len(r): print(f"  y={y}: x {240+r.min()}..{240+r.max()} n={len(r)}")

print("\n== arrow-to-3 rows (y 343..412, x 420..485) ==")
for y in range(343, 412, 2):
    r = np.where(lum[y, 420:485] < 120)[0]
    if len(r): print(f"  y={y}: x {420+r.min()}..{420+r.max()} n={len(r)}")

print("\n== arrow-to-neuron rows (y 320..435, x 575..695) ==")
for y in range(320, 435, 3):
    r = np.where(lum[y, 575:695] < 120)[0]
    if len(r): print(f"  y={y}: x {575+r.min()}..{575+r.max()} n={len(r)}")

print("\n== question word profile (columns) for font size ==")
sub = lum[410:452, 156:796]
cols = (sub < 150).sum(axis=0)
gaps = []
ing = False
for i, v in enumerate(cols):
    if v == 0 and not ing: s = i; ing = True
    elif v > 0 and ing:
        if i - s >= 6: gaps.append((156 + s, 156 + i - 1))
        ing = False
print("word gaps (>=6px):", gaps[:20])
rows = (sub < 150).sum(axis=1)
print("question row profile:", [(410 + i, int(v)) for i, v in enumerate(rows) if v > 0])

print("\n== equation row profile ==")
sub = lum[448:484, 325:600]
rows = (sub < 200).sum(axis=1)
print("eq rows:", [(448 + i, int(v)) for i, v in enumerate(rows) if v > 0])
cols = (sub < 200).sum(axis=0)
xs = np.where(cols > 0)[0]
print("eq x extent:", 325 + xs.min(), 325 + xs.max())

print("\n== RGB label rows ==")
sub = lum[150:215, 262:402]
rows = (sub < 150).sum(axis=1)
print("RGB rows:", [(150 + i, int(v)) for i, v in enumerate(rows) if v > 0])
cols = (sub < 150).sum(axis=0)
xs = np.where(cols > 0)[0]
print("RGB x extent:", 262 + xs.min(), 262 + xs.max())

print("\n== 3dims text rows ==")
sub = lum[243:265, 158:242]
rows = (sub < 150).sum(axis=1)
print("3dims rows:", [(243 + i, int(v)) for i, v in enumerate(rows) if v > 0])
