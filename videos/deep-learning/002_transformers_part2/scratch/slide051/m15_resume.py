#!/usr/bin/env python3
# m15_resume.py — corrected render comparison + raw RGB for the mystery cluster.
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
orig = Image.open(f"{ROOT}/unique_slides/slide_051.jpg").convert("RGB")
r4 = Image.open(f"{ROOT}/recreated_pptx/qa/slide051/render_4.png").convert("RGB")
SX = lambda fx: (fx - 18.128) / 0.961235
SY = lambda fy: (fy + 0.045) / 0.956566
K = 150.0 / 72.0
# render px for a frame coord:
RX = lambda fx: SX(fx) * K
RY = lambda fy: SY(fy) * K

print("=== 1) RAW RGB, ORIG mystery cluster x828..878 y278..314 step 3")
for y in range(278, 315, 3):
    row = f"y{y}: "
    for x in range(828, 879, 3):
        r, g, b = orig.getpixel((x, y))
        row += f"({r:3},{g:3},{b:3})"
    print(row)

print()
print("=== 2) ORIG decoder PE region x780..880 y394..436 step 2 (class)")
def q(r, g, b):
    if b > 100 and r < 90 and g < 90: return "N"
    if r < 90 and g < 90 and b < 90: return "k"
    if g > 150 and g > r + 40 and g > b + 40: return "G"
    if r > 225 and g > 245 and b > 205: return "."   # mint
    if r > 225 and g > 130 and b < 135 and g < 215: return "O"  # orange
    if r > 150 and 90 < g < 200 and b < 130 and r > b + 40: return "T"  # tan/brown/maroon
    if b > 150 and r < 150 and g < 160: return "b"
    if r > 170 and g < 160 and b > 170: return "P"
    if r > 200 and g > 200 and b > 200: return "w"
    if r > 140 and g > 140 and b < 110: return "y"
    return "?"
xs = list(range(780, 881, 2))
print("      " + "".join(f"{x % 10}" for x in xs))
for y in range(394, 437, 2):
    row = f"y{y:<4d}"
    for x in xs:
        row += q(*orig.getpixel((x, y)))
    print(row)

print()
print("=== 3) RENDER_4 (sampled at RENDER px), norm box1 + decoder right + dec PE")
def dump_r(x0f, y0f, x1f, y1f, step, label):
    x0, y0 = int(RX(x0f)), int(RY(y0f))
    x1, y1 = int(RX(x1f)), int(RY(y1f))
    print(f"--- {label}: frame ({x0f},{y0f})-({x1f},{y1f}) = render ({x0},{y0})-({x1},{y1}) step {step}")
    xs = list(range(x0, x1 + 1, step))
    print("      " + "".join(f"{x % 10}" for x in xs))
    for y in range(y0, y1 + 1, step):
        row = f"r{y:<5d}"
        for x in xs:
            row += q(*r4.getpixel((x, y)))
        print(row)
dump_r(205, 260, 285, 284, 4, "RENDER4 enc norm box1")
dump_r(790, 285, 875, 335, 4, "RENDER4 dec right edge (Nx spot)")
dump_r(780, 396, 875, 432, 4, "RENDER4 dec PE region")
