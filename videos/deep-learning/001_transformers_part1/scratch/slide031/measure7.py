#!/usr/bin/env python3
"""1px-resolution zoom maps with fine color classes."""
from PIL import Image
import sys

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()

def cls(c):
    r, g, b = c
    if r > 238 and g > 238 and b > 238: return "."
    if r < 90 and g < 90 and b < 90: return "#"
    if r < 160 and b > 120 and b - r > 50 and g < 120: return "N"   # dark navy
    if r < 160 and r - g > 45 and r - b > 45 and g < 110: return "r"  # dark red
    if r < 160 and g - r > 20 and g - b > 20 and g > 70: return "v"   # dark green
    if r > 130 and r-g > 55 and r-b > 55: return "R"
    if b > 120 and b-r > 55 and b-g > 35: return "B"
    if g > 105 and g-r > 30 and g-b > 30: return "G"
    if r > 225 and 150 < g < 218 and 160 < b < 235 and r-g > 18: return "k"
    if r > 233 and 210 < g < 245 and 180 < b < 230: return "P"
    if 130 < r < 215 and 130 < g < 218 and b > 195 and b-r > 20: return "w"
    if r < 220 and g > 200 and g-r > 12 and g-b > 8: return "g"
    if r > 225 and g > 210 and b < 165: return "Y"
    return "-"

def zoom(x0, x1, y0, y1, label):
    print(f"=== {label} x{x0}..{x1} y{y0}..{y1} ===")
    hdr = "     " + "".join(str((x//10) % 10) if x % 10 == 0 else " " for x in range(x0, x1))
    print(hdr)
    for y in range(y0, y1):
        print(f"{y:4d} " + "".join(cls(px[x, y]) for x in range(x0, x1)))

which = sys.argv[1] if len(sys.argv) > 1 else "all"
if which in ("all", "A"): zoom(58, 222, 128, 225, "A: Q capsule + 1xd + X2")
if which in ("all", "C"): zoom(370, 470, 95, 300, "C: Q = + output capsule + role letter")
