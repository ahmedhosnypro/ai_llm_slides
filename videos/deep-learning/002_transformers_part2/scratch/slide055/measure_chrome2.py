#!/usr/bin/env python3
"""Slide 055: lower-threshold border landmark scan (thin 1-2px C00000 strokes diluted by JPEG)."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()

def redness(p):
    r, g, b = p
    return r - max(g, b)

out = {}
# per-column max vertical run of redness>40 in the border zones (avoid diagram area):
# left border expected near x 55..63, right near 898..906, top near y 40..46, bottom near 512..520
def col_red(x, y0, y1):
    return sum(1 for y in range(y0, y1) if redness(px[x, y]) > 40)
def row_red(y, x0, x1):
    return sum(1 for x in range(x0, x1) if redness(px[x, y]) > 40)

left = {x: col_red(x, 60, 500) for x in range(45, 75)}
right = {x: col_red(x, 60, 500) for x in range(890, 915)}
top = {y: row_red(y, 80, 850) for y in range(35, 55)}
bot = {y: row_red(y, 80, 850) for y in range(505, 525)}
out["left_profile"] = {k: v for k, v in left.items() if v > 20}
out["right_profile"] = {k: v for k, v in right.items() if v > 20}
out["top_profile"] = {k: v for k, v in top.items() if v > 100}
out["bottom_profile"] = {k: v for k, v in bot.items() if v > 100}

# sample colors on the found strokes
def show(d):
    ks = sorted(d)
    return ks
out["left_cols"] = show({k: v for k, v in left.items() if v > 20})
out["right_cols"] = show({k: v for k, v in right.items() if v > 20})
out["top_rows"] = show({k: v for k, v in top.items() if v > 100})
out["bottom_rows"] = show({k: v for k, v in bot.items() if v > 100})
print(json.dumps(out, indent=1))
