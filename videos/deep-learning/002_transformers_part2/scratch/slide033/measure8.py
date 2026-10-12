#!/usr/bin/env python3
"""slide033 measure-8: general pair box map + dx1 + defs/example/omega text bands."""
import numpy as np
from PIL import Image
from scipy import ndimage

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(FR).convert("RGB")).astype(int)
H, W, _ = a.shape
MAPX = lambda fx: (fx - 18.63) / 0.96123
MAPY = lambda fy: fy / 0.95556
S = lambda x0, x1, y0, y1: (f"f[{x0},{y0}..{x1},{y1}] slide[{MAPX(x0):.1f}..{MAPX(x1):.1f} x {MAPY(y0):.1f}..{MAPY(y1):.1f}] in[{MAPX(x0)/72:.3f}..{MAPX(x1)/72:.3f}, {MAPY(y0)/72:.3f}..{MAPY(y1)/72:.3f}]")

def ch(px):
    r, g, b = px
    if r > 246 and g > 246 and b > 246: return "."
    if 222 < r <= 246 and 222 < g <= 246 and 222 < b <= 246: return " "
    if r > 228 and g > 200 and 130 < b < 225 and r - b > 20: return "c"  # cream/tan
    if r > 215 and 150 < g < 215 and 100 < b < 180 and r - b > 55: return "o"
    if 140 < r < 215 and g > 175 and 110 < b < 210 and g - b > 20 and g - r > 10: return "g"
    if r < 150 and g > 130 and g - r > 30 and g - b > 30: return "G"
    if r > 115 and g < 85 and b < 85: return "R"
    if 100 < r < 160 and 20 < g < 100 and 20 < b < 110 and r - g > 30: return "M"  # maroon/dk red
    if r < 115 and g < 115 and b < 115: return "k"
    if b > 190 and g > 190 and b - r > 8: return "b"
    if b > 110 and r < 110 and b - r > 40: return "B"
    if r > 150 and g > 150 and b < 160 and r - b > 40 and g - b > 30: return "y"
    return ":"

print("=== GENERAL PAIR BOX map (x 84..196, y 110..220, step 2) ===")
print("     " + "".join(str((x // 10) % 10) for x in range(84, 197, 2)))
for y in range(110, 221, 2):
    print(f"{y:3d} " + "".join(ch(a[y, x]) for x in range(84, 197, 2)))

print("=== dx1 region map (x 400..480, y 480..525, step 2) ===")
print("     " + "".join(str((x // 10) % 10) for x in range(400, 481, 2)))
for y in range(480, 526, 2):
    print(f"{y:3d} " + "".join(ch(a[y, x]) for x in range(400, 481, 2)))

def bands(x0, x1, y0, y1, kind, gap=4, min_area=4):
    sub = a[y0:y1 + 1, x0:x1 + 1]
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    if kind == "red": m = (r > 120) & (g < 85) & (b < 85)
    elif kind == "blue": m = (b > 100) & (r < 100) & (b - r > 50)
    elif kind == "black": m = (r < 110) & (g < 110) & (b < 110)
    elif kind == "green": m = (g > 100) & (g < 190) & (r < 110) & (b < 120) & (g - r > 40)
    elif kind == "purple": m = (r > 80) & (r < 170) & (b > 110) & (b < 200) & (g < 90)
    elif kind == "orange": m = (r > 180) & (g > 80) & (g < 170) & (b < 100)
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    boxes = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_area: continue
        boxes.append([int(xs.min()) + x0, int(ys.min()) + y0, int(xs.max()) + x0, int(ys.max()) + y0])
    boxes.sort(key=lambda t: (t[1], t[0]))
    out, cur = [], None
    for t in boxes:
        if cur is None or t[1] - cur[3] > gap:
            if cur: out.append(cur)
            cur = [t[0], t[1], t[2], t[3]]
        else:
            cur[0] = min(cur[0], t[0]); cur[1] = min(cur[1], t[1])
            cur[2] = max(cur[2], t[2]); cur[3] = max(cur[3], t[3])
    if cur: out.append(cur)
    print(f"--- {kind} bands in x{x0}..{x1} y{y0}..{y1} ---")
    for bd in out:
        print(f"  {S(bd[0], bd[2], bd[1], bd[3])}")
    return out

print("=== DEFS BOX text bands (frame x 429..760, y 101..288) ===")
for k in ["red", "blue", "black", "green", "purple"]:
    bands(432, 758, 104, 286, k)

print("=== EXAMPLE BOX text bands (frame x 777..887, y 101..287) ===")
for k in ["red", "blue", "black", "green"]:
    bands(780, 885, 104, 285, k)

print("=== OMEGA BOX text bands (frame x 475..880, y 300..512) ===")
for k in ["red", "blue", "black"]:
    bands(478, 878, 302, 510, k)

print("=== TITLE/SUBTITLE precise ===")
bands(320, 620, 44, 68, "red", gap=3)
bands(140, 810, 69, 95, "blue", gap=3)

print("=== Vector Pairs label (blue) + Index label (red) ===")
bands(200, 265, 92, 124, "blue", gap=3)
bands(265, 320, 92, 124, "red", gap=3)

print("=== info box text bands (x 66..212, y 226..320) ===")
for k in ["black", "red", "green"]:
    bands(70, 208, 228, 318, k)

print("=== general pair box red text (x 104..172, y 130..210) ===")
bands(106, 170, 132, 208, "red", gap=4)
