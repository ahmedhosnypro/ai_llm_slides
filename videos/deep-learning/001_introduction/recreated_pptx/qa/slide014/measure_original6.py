#!/usr/bin/env python3
"""Pass 6: ASCII class map of the flowchart panel + loose rescans."""
import json
from PIL import Image

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_014.jpg").convert("RGB")
W, H = img.size
px = img.load()

def cls(p):
    r, g, b = p
    if r > 235 and g > 235 and b > 235: return "."          # white
    if r > 140 and g < 90 and b < 90: return "R"            # red (arrows/title)
    if 120 < r < 200 and g < 60 and b < 60: return "D"      # darkred box
    if g > 90 and g - r > 40 and g - b > 20 and r < 120: return "G"  # green
    if b > 90 and b - r > 50 and b - g > 40: return "B"     # navy border
    if r < 90 and g < 90 and b < 90: return "K"             # black
    if 235 < r <= 255 and 200 < g < 240 and 165 < b < 215: return "T"  # tan
    if r > 235 and g > 235 and 195 < b < 240: return "Y"    # yellow
    if 200 < r < 245 and g > 230 and b > 230: return "I"    # ice/mint fill
    if 180 < r < 245 and 220 < g < 250 and 235 < b <= 256: return "i"  # pale blue border
    if r > 120 and 60 < g < 200 and 60 < b < 200 and abs(g - b) < 40: return "c"  # gray cursor
    return " "

# map the whole panel: x 60..900 step 6, y 125..380 step 4  -> 140 cols x 64 rows
print("PANEL MAP (x60..900 step6, y125..380 step4):")
hdr = "     " + "".join(str((60 + i * 6) // 100 % 10) for i in range(141))
print(hdr)
for y in range(125, 381, 4):
    row = "".join(cls(px[x, y]) for x in range(60, 901, 6))
    print(f"{y:4d} {row}")

# title + takeaway map
print("\nTITLE (y70..108 step2, x150..800 step6):")
for y in range(70, 109, 2):
    print(f"{y:4d} " + "".join(cls(px[x, y]) for x in range(150, 801, 6)))
print("\nTAKEAWAY (y430..458 step2, x100..830 step6):")
for y in range(430, 459, 2):
    print(f"{y:4d} " + "".join(cls(px[x, y]) for x in range(100, 831, 6)))
