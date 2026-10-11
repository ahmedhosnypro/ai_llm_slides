#!/usr/bin/env python3
import numpy as np
from PIL import Image

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
PEACH = np.array([247, 227, 206])

def cls(c):
    r, g, b = c
    if r < 165 and g < 165 and b < 200: return "k"
    if r - g > 45 and r > 150: return "R"
    if b - r > 25 and b > 200: return "L"
    if r > 240 and g > 240 and b < 228: return "Y"
    if g - r > 12 and g - b > 12 and g > 170 and r < 235: return "G"
    if abs(r-247)+abs(g-227)+abs(b-206) <= 40: return "."
    if abs(r-233)+abs(g-233)+abs(b-231) <= 22: return ","
    return "?"

print("== box-to-bar zone x336..468, y196..400 (every 4th row) ==")
for y in range(196, 401, 4):
    row = "".join(cls(A[y, x]) for x in range(336, 468))
    if row.count(".") < len(row) - 2:
        print(f"y{y:3d} {row}")

print("\n== pill tight mask (252,252,218) tol 22 ==")
t = np.array([252, 252, 218])
for nm, (x0, x1) in {"Sim": (240, 400), "Prob": (400, 540), "WSum": (560, 720)}.items():
    sub = A[148:196, x0:x1]
    m = (np.abs(sub - t).sum(axis=2) <= 22)
    ys, xs = np.where(m)
    if len(xs) > 30:
        print(f"  {nm}: x{x0+xs.min()}..{x0+xs.max()} y{148+ys.min()}..{148+ys.max()} n={len(xs)}")
    else:
        print(f"  {nm}: n={len(xs)}")

print("\n== feed curve connections ==")
print("left zone x95..185, y455..500:")
for y in range(455, 500, 2):
    row = "".join(cls(A[y, x]) for x in range(95, 185))
    if row.count(".") < 88:
        print(f"y{y:3d} {row}")
print("right zone x490..812, y405..500 (rows w/ ink):")
for y in range(405, 500, 2):
    row = "".join(cls(A[y, x]) for x in range(490, 812, 2))
    if row.count(".") < 158:
        print(f"y{y:3d} {row}")

print("\n== strip container edges ==")
for y in (470, 471, 472, 473, 516, 517, 518, 519):
    row = "".join(cls(A[y, x]) for x in range(170, 500, 4))
    print(f"y{y:3d} {row}")
