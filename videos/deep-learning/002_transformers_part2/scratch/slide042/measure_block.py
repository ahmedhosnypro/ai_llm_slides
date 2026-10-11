#!/usr/bin/env python3
"""Fine 2px ASCII map of right block + red-mask map + layer color samples."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)

def cls(px):
    R, G, B = int(px[0]), int(px[1]), int(px[2])
    if R > 240 and G > 240 and B > 235: return "."
    if R > 140 and G < 120 and B < 120 and R - G > 50 and R - B > 50: return "R"
    if B > 120 and B - R > 30 and B - G > 20: return "B"
    if G > 170 and G - R > 60 and G - B > 60: return "G"
    if G > 90 and G - R > 20 and G - B > 40: return "d"
    if R > 120 and B > 120 and G < 110: return "M"
    if R > 170 and G > 150 and B < 130: return "Y"
    if R > 170 and 80 < G < 170 and B < 100: return "O"
    if R < 100 and G < 100 and B < 100: return "K"
    return "?"

print("RIGHT BLOCK fine map x630..900 step2, y230..505 step2 (col header = x/10 %10):")
hdr = "     " + "".join(str((630 + i * 2) // 10 % 10) if (630 + i * 2) % 20 == 0 else " " for i in range(136))
print(hdr)
for y in range(230, 506, 2):
    row = "".join(cls(a[y, x]) for x in range(630, 902, 2))
    print(f"{y:4d} {row}")

print()
print("RED MASK map x580..900 step2, y270..515 step2:")
hdr = "     " + "".join(str((580 + i * 2) // 10 % 10) if (580 + i * 2) % 20 == 0 else " " for i in range(161))
print(hdr)
redm = (a[:, :, 0] > 130) & (a[:, :, 0] - a[:, :, 1] > 50) & (a[:, :, 0] - a[:, :, 2] > 50)
for y in range(270, 516, 2):
    row = "".join("R" if redm[y, x] else "." for x in range(580, 902, 2))
    print(f"{y:4d} {row}")

print()
print("LAYER COLOR CORE SAMPLES:")
for name, x, y in [("magenta face", 700, 400), ("magenta face2", 670, 430), ("green stripe", 795, 400),
                   ("orange stripe", 812, 400), ("yellow stripe", 828, 400), ("blue stripe", 845, 330),
                   ("green band top", 700, 300), ("dark band", 700, 310), ("K band above green", 700, 278),
                   ("yellow band", 730, 269), ("blue-gray band", 730, 245), ("blue-gray band2", 810, 242),
                   ("orange long region", 810, 350), ("orange 2", 810, 420), ("red line", 700, 285),
                   ("mid-grid front", 430, 310), ("mid-grid top", 430, 262), ("left stack front", 190, 290),
                   ("left stack top", 190, 270)]:
    print(f"  {name} ({x},{y}) = {tuple(int(v) for v in a[y, x])}")
