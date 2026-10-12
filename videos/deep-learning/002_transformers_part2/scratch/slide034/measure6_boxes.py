#!/usr/bin/env python3
"""measure6_boxes.py — per-box edges via column profiles + direct RGB samples."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_034.jpg"
img = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r, g, b = img[..., 0], img[..., 1], img[..., 2]

def px(x, y):
    return f"({img[y, x, 0]},{img[y, x, 1]},{img[y, x, 2]})"

print("== TOKEN ROW: dark-border column profile y142..168 ==")
dark = (r + g + b < 480) | ((b - r > 40) & (b < 215))
prof = dark[142:168, 150:900].sum(axis=0)
cols = np.where(prof >= 8)[0] + 150
# group consecutive
groups = []
for c in cols:
    if groups and c - groups[-1][-1] <= 2: groups[-1].append(c)
    else: groups.append([c])
print("border cols:", [f"{gp[0]}-{gp[-1]}" for gp in groups])

print("\n== TOKEN ROW samples ==")
print("lane@ (215,170):", px(215, 170), " box1 center (210,150):", px(210, 150),
      " between 860? (172,150):", px(172, 150))
for x in [200, 300, 400, 500, 620, 700, 780, 840]:
    print(f"  token y150 x{x}: {px(x, 150)}")

print("\n== VECTOR ROW: dark-border column profile y300..338 ==")
darkv = (r + g + b < 500)
prof = darkv[300:338, 150:900].sum(axis=0)
cols = np.where(prof >= 8)[0] + 150
groups = []
for c in cols:
    if groups and c - groups[-1][-1] <= 2: groups[-1].append(c)
    else: groups.append([c])
print("border cols:", [f"{gp[0]}-{gp[-1]}" for gp in groups])

print("\n== VECTOR ROW samples ==")
for x in [200, 300, 400, 500, 620, 700, 780, 840]:
    print(f"  vec y310 x{x}: {px(x, 310)}")
print("  lane edges: y294 x185:", px(185, 294), " y325 x185:", px(185, 325),
      " inside-box (200,310):", px(200, 310), " gap (660,310):", px(660, 310))

print("\n== VECTOR box top/bottom borders: row profile x190..870 ==")
for y in range(292, 345):
    n = darkv[y, 190:870].sum()
    if n > 30: print(f"  y{y}: n={n}")

print("\n== TOKEN box top/bottom: row profile x190..870 (dark) ==")
for y in range(135, 180):
    n = dark[y, 190:870].sum()
    if n > 30: print(f"  y{y}: n={n}")

print("\n== PURPLE BAR text zone: yellow + white runs y214..252 ==")
yel = (r > 200) & (g > 190) & (b < 150)
ys, xs = np.where(yel[214:252, 170:890])
if len(xs): print(f"yellow text: x {xs.min()+170}..{xs.max()+170}  y {ys.min()+214}..{ys.max()+214}")
white = (r > 230) & (g > 230) & (b > 230)
ys, xs = np.where(white[214:252, 170:890])
if len(xs): print(f"white text: x {xs.min()+170}..{xs.max()+170}  y {ys.min()+214}..{ys.max()+214}")
