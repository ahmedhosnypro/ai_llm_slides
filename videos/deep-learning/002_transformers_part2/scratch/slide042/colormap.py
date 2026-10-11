#!/usr/bin/env python3
"""Coarse ASCII color map of slide_042.jpg content + targeted pixel samples."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)

def code(px):
    r, g, b = px
    if r > 245 and g > 245 and b > 243: return "."   # white
    if abs(r - 233) < 12 and abs(g - 233) < 12 and abs(b - 231) < 12: return "g"  # gray panel
    if r < 60 and g < 60 and b < 60: return "K"       # black
    if r > 120 and g < 110 and b < 110 and r - g > 50: return "R"  # red
    if b > 120 and b - r > 40 and b - g > 40: return "B"  # blue
    if g > 110 and g - r > 30 and g - b > 50: return "G"  # green
    if r > 150 and b > 150 and g < 120: return "M"    # magenta
    if r > 200 and g > 160 and b < 120: return "Y"    # yellow
    if r > 200 and 60 < g < 180 and b < 90: return "O"  # orange
    if r < 150 and g < 150 and b > 140: return "b"    # dark blue / blue-gray
    if r < 150 and g > 130 and b < 130: return "d"    # dark green
    return "?"

# RIGHT BLOCK region: x 640..900, y 240..500, step 6
print("RIGHT BLOCK (x 640..900, y 240..500, step 6):")
print("    " + "".join(str((640 + i * 6) // 100 % 10) for i in range(44)))
for y in range(240, 500, 6):
    row = "".join(code(a[y, x]) for x in range(640, 900, 6))
    print(f"{y:4d} {row}")

print()
print("LEFT+MIDDLE (x 60..560, y 180..500, step 6):")
for y in range(180, 500, 6):
    row = "".join(code(a[y, x]) for x in range(60, 560, 6))
    print(f"{y:4d} {row}")

# targeted samples
def sample(name, x, y):
    print(f"{name} ({x},{y}) = {tuple(a[y, x])}")

print()
print("TARGETED SAMPLES:")
for pt in [(700, 400), (700, 450), (680, 420), (760, 420), (830, 270), (830, 340), (830, 400),
           (700, 300), (740, 300), (660, 280), (700, 260), (760, 260), (800, 300), (800, 260),
           (190, 300), (190, 380), (175, 270), (203, 300),
           (420, 300), (420, 400), (400, 268), (460, 268), (505, 300), (505, 410)]:
    sample("", *pt)
