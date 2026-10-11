#!/usr/bin/env python3
"""m3_scan.py — ASCII color-class maps: callout boxes (fine), enc/dec stacks, green trace."""
from PIL import Image
import collections

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg").convert("RGB")
px = IM.load()

def cls(c):
    r, g, b = c
    if r > 232 and g > 232 and b > 228: return "."          # panel/bg
    if r + g + b < 210: return "D"                           # black ink
    # vivid yellow-green (residual arrows) (144-200, 200-240, 40-110)
    if 130 <= r <= 215 and 190 <= g <= 255 and b <= 130 and g > r + 30: return "V"
    # pale green fill (222,255,196)
    if r >= 200 and g >= 240 and 150 <= b <= 215 and g > r + 15: return "P"
    # steel blue A&N fill (72-110,130-170,150-190)
    if b > r + 40 and b > 140 and g > r + 20 and g < b + 10: return "B"
    # dark blue-violet (96,120,216)
    if b > 170 and b > g + 60 and r < g + 20: return "U"
    # dark blue circles (0,0,128)
    if b > 90 and r < 60 and g < 60: return "b"
    # red
    if r > 120 and r > g + 50 and r > b + 50: return "R"
    # tan/brown (192,168,120) / (120,96,72)
    if r > g + 15 and g > b + 15: return "t" if r > 160 else "T"
    # olive (168,168,120)
    if abs(r - g) < 20 and g > b + 25 and r > 140: return "o"
    # gray (150-180 flat)
    if abs(r - g) < 14 and abs(g - b) < 14 and 110 < r < 215: return "K"
    # yellow (240,240,48)
    if r > 200 and g > 200 and b < 120: return "Y"
    # green (74,146,74)/(27,113,63)
    if g > r + 25 and g > b + 25: return "g"
    # salmon (192,120,80)
    if r > 160 and g > 100 and b < 110 and r > g + 40: return "S"
    return "?"

def dump(x0, x1, y0, y1, step, label):
    print(f"\n== {label} x{x0}..{x1} y{y0}..{y1} step{step} (col header every 10 cols) ==")
    hdr = "    " + "".join(str((x0 + i * step) // 100 % 10) if (x0 + i * step) % (100) < step else ("|" if (x0 + i * step) % 50 < step else " ") for i in range((x1 - x0) // step + 1))
    print(hdr)
    for y in range(y0, y1, step):
        row = "".join(cls(px[x, y]) for x in range(x0, x1, step))
        print(f"{y:3d} {row}")

# callout boxes fine map
dump(130, 570, 100, 215, 3, "CALLOUTS fine")
# encoder stack
dump(600, 745, 250, 420, 3, "ENC STACK")
# decoder stack
dump(730, 870, 190, 420, 3, "DEC STACK")
