#!/usr/bin/env python3
"""Probe vert1 columns; verify pitch; compare inherited regions vs parent certified render."""
from PIL import Image, ImageChops
import math

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"
im = Image.open(BASE + "recreated_pptx/qa/slide008/render_1.png").convert("RGB")
ld = im.load()

def anybluish(p):
    r, g, b = p
    return b - r > 18 and b > 150 and g < 225

# vert1 column profile at rows 615..625 (between wait1 bottom 607 and container top 636)
for y in (612, 620, 628):
    cols = [x for x in range(420, 470) if anybluish(ld[x, y])]
    print(f"render y={y}: bluish cols {cols}")
# what colors are at 432-436 vs 440-449?
for x in (433, 436, 441, 446, 450):
    print(f"  ({x},620) = {ld[x, 620]}")

# wait1 text pitch: per-row ink counts in the box
def blueink(p):
    r, g, b = p
    return b > 110 and b - r > 40 and g < 140
rows = [(y, sum(1 for x in range(109, 383) if blueink(ld[x, y]))) for y in range(536, 608)]
ink = [r for r in rows if r[1]]
print("wait1 ink rows:", ink[0], "...", ink[-1], "| gaps:", [(ink[i+1][0]-ink[i][0]) for i in range(len(ink)-1) if ink[i+1][0]-ink[i][0] > 1])

# inherited-region diff vs parent certified render
p6 = Image.open(BASE + "recreated_pptx/qa/slide006/render_1.png").convert("RGB")
print("parent render size:", p6.size)
if p6.size == im.size:
    # non-delta regions: everything except (title band x 250..660) and the delta boxes/leaders zone
    diff_total = 0
    regions = {
        "decoder half (x>980)": (980, 200, 1990, 620),
        "encoder (x<930, y>640)": (100, 640, 930, 1040),
        "ctx box+arc (x>930, y 500..860)": (930, 500, 1990, 860),
    }
    for tag, box in regions.items():
        d = ImageChops.difference(im.crop(box), p6.crop(box))
        bbox = d.getbbox()
        px_diff = sum(1 for p in d.getdata() if sum(p) > 30)
        print(f"  {tag}: diff>30 px = {px_diff} bbox={bbox}")
