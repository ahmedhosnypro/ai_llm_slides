#!/usr/bin/env python3
# m16_resume.py — final targeted forensics before the fix pass.
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
orig = Image.open(f"{ROOT}/unique_slides/slide_051.jpg").convert("RGB")

print("=== 1) ORIG Nx cluster fine: x820..874 y272..316 step 2 (class + key raw)")
def q(r, g, b):
    if g > 100 and g < 180 and r < 90 and b < 90: return "d"   # dark green stroke
    if b > 100 and r < 90 and g < 90: return "N"
    if r < 90 and g < 90 and b < 90: return "k"
    if g > 150 and g > r + 40 and g > b + 40: return "G"
    if 150 < r < 215 and 140 < g < 215 and 90 < b < 170: return "o"  # olive/khaki
    if r > 225 and g > 245 and b > 205: return "."
    if r > 150 and 90 < g < 200 and b < 130 and r > b + 40: return "T"
    if b > 150 and r < 150 and g < 160: return "b"
    if r > 170 and g < 160 and b > 170: return "P"
    if r > 200 and g > 200 and b > 200: return "w"
    return "?"
xs = list(range(820, 875, 2))
print("      " + "".join(f"{x % 10}" for x in xs))
for y in range(272, 317, 2):
    row = f"y{y:<4d}"
    for x in xs:
        row += q(*orig.getpixel((x, y)))
    print(row)

print()
print("=== 2) ORIG encoder Nx region for family comparison: x152..192 y308..346 step 2")
xs = list(range(152, 193, 2))
print("      " + "".join(f"{x % 10}" for x in xs))
for y in range(308, 347, 2):
    row = f"y{y:<4d}"
    for x in xs:
        row += q(*orig.getpixel((x, y)))
    print(row)

print()
print("=== 3) ORIG decoder bottom raw split: maroon vs brown icon, x734..814 y396..466 step 3")
for y in range(396, 467, 3):
    row = f"y{y:<4d}"
    for x in range(734, 815, 3):
        r, g, b = orig.getpixel((x, y))
        row += f"({r:3},{g:3},{b:3})"
    print(row)

print()
print("=== 4) ORIG encoder residual stubs region: x193..250 y262..345 step 2 (class)")
xs = list(range(193, 251, 2))
print("      " + "".join(f"{x % 10}" for x in xs))
for y in range(262, 346, 2):
    row = f"y{y:<4d}"
    for x in xs:
        row += q(*orig.getpixel((x, y)))
    print(row)
