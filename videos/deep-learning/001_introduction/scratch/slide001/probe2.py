#!/usr/bin/env python3
"""Probe 2: strict-core metrics (title cap heights, rule vs border, logo lockup bbox)."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_001.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

# strict red core (avoid JPEG halo): near C00000
core_red = (r > 140) & (g < 60) & (b < 60)
core_blue = (b > 120) & (r < 80) & (g < 80)

def rowprof(mask, x0, x1, y0, y1, label):
    print(f"--- {label} (x {x0}-{x1}) ---")
    for y in range(y0, y1):
        n = mask[y, x0:x1].sum()
        if n:
            xs = np.where(mask[y, x0:x1])[0]
            print(f"  y{y}: n={n} x {x0+xs.min()}-{x0+xs.max()}")

# 1. title L1 rows (strict)
rowprof(core_red, 150, 800, 115, 195, "title L1 strict rows")
rowprof(core_red, 150, 800, 190, 250, "title L2 strict rows")

# 2. rule/border region: raw colors rows 38..52 at several x
print("--- raw rows 38..52 (x=300, x=700) ---")
for y in range(38, 53):
    print(f"  y{y}: @300 {IM[y,300]} @700 {IM[y,700]} @60 {IM[y,60]} @900 {IM[y,900]}")

# 3. panel borders: columns 38..48 at y=300; 912..924 at y=300
print("--- cols 38..48 @y300 ---")
for x in range(38, 49):
    print(f"  x{x}: {IM[300, x]}")
print("--- cols 910..924 @y300 ---")
for x in range(910, 925):
    print(f"  x{x}: {IM[300, x]}")

# 4. logo lockup: non-panel-bg pixels in region x 550..930, y 415..540
print("--- logo region: non-bg mask rows ---")
bgd = (abs(r - 232) < 10) & (abs(g - 232) < 10) & (abs(b - 231) < 12)
nonbg = ~bgd
sub = nonbg[415:540, 550:930]
ys, xs = np.where(sub)
print(f"lockup ink: x {550+xs.min()}-{550+xs.max()}, y {415+ys.min()}-{415+ys.max()} "
      f"(in x {(550+xs.min())/72:.3f}-{(550+xs.max()+1)/72:.3f}, y {(415+ys.min())/72:.3f}-{(415+ys.max()+1)/72:.3f})")
for y in range(415, 540):
    row = nonbg[y, 550:930]
    if row.sum() > 4:
        xs2 = np.where(row)[0]
        print(f"  y{y}: n={row.sum()} x {550+xs2.min()}-{550+xs2.max()}")

# 5. white box interior columns (find box left/right edges): white cols in y 470..500
white = (r > 240) & (g > 240) & (b > 240)
for label, (yy0, yy1) in {"white rows 465-475": (465, 475), "white rows 495-505": (495, 505)}.items():
    cols = np.where(white[yy0:yy1, 550:935].sum(axis=0) > (yy1 - yy0) * 0.6)[0]
    if len(cols):
        print(f"{label}: white cols x {550+cols.min()}-{550+cols.max()}")

# 6. maroon text lines in white box
maroon = (r > 80) & (r < 200) & (g < 90) & (b < 110)
rowprof(maroon, 660, 930, 440, 530, "maroon text rows (logo box)")

# 7. emblem teal extent strict
teal = (g > 120) & (b > 120) & (r < 130) & (g - r > 40)
ys, xs = np.where(teal[420:540, 550:700])
print(f"teal strict: x {550+xs.min()}-{550+xs.max()}, y {420+ys.min()}-{420+ys.max()}")
