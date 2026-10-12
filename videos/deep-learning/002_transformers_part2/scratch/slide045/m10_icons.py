#!/usr/bin/env python3
"""Slide 045 — FFN icon pixel census (m10): tile fill/border, dot rows, fan color, RELU."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]

def classify(px):
    r, g, b = px
    if r > 235 and g > 235 and b > 235: return "."      # white
    if r > 200 and g > 200 and b < 210 and b > 150: return "c"  # cream/yellow pale
    if r > 180 and g < 130 and b < 130: return "R"      # red/orange strong
    if r > 150 and 130 <= g < 200 and b < 150 and r - b > 60: return "o"  # orange/salmon
    if g > 130 and r < 130 and g - r > 40: return "G"   # green
    if r > 120 and b > 120 and g < r - 20 and g < b - 10: return "P"  # purple/magenta
    if b > 120 and b - r > 40 and b - g > 20: return "B"  # blue
    if r < 110 and g < 110 and b < 110: return "K"      # dark/black
    if abs(r - g) < 30 and abs(g - b) < 30 and r < 200: return "k"  # gray
    return "?"

print("== icon 1 tile map (frame x 176..236, y 212..258), 1px ==")
print("    " + "".join(str((176 + i) % 10) for i in range(0, 60)))
for y in range(212, 259):
    row = "".join(classify(img[y, x]) for x in range(176, 236))
    print(f"  {y}: {row}")

print("== icon 2 tile map (frame x 248..308, y 212..258) ==")
for y in range(212, 259):
    row = "".join(classify(img[y, x]) for x in range(248, 308))
    print(f"  {y}: {row}")

print("== FFN box background between tiles (x 238..246, y 220..250) ==")
print("  median:", np.median(img[220:250, 238:246].reshape(-1, 3), axis=0))
print("  between icons 2/3 (x 312..322):", np.median(img[220:250, 312:322].reshape(-1, 3), axis=0))
print("  box far left inside (x 168..178, y 220..250):", np.median(img[220:250, 168:178].reshape(-1, 3), axis=0))

print("== tile vertical extent at icon1 center x=206 ==")
for y in range(200, 262):
    px = img[y, 206]
    print(f"  y={y}: {tuple(px)}", "".join(classify(px)))
