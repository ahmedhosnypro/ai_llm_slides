#!/usr/bin/env python3
"""Build stacked comparison sheets: render crops vs original frame crops,
same regions, same scales, same order — for one gated vision comparison."""
import numpy as np
from PIL import Image, ImageDraw

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
REN = f"{BASE}/recreated_pptx/qa/slide036/render_2.png"
ORIG = f"{BASE}/unique_slides/slide_036.jpg"
OUT = f"{BASE}/scratch/slide036"

ren = Image.open(REN).convert("RGB")
orig = Image.open(ORIG).convert("RGB")
S = 150 / 72.0
FX = lambda fx: (fx - 18.628) / 0.961231
FY = lambda fy: fy / 0.955556

# (tag, fx0, fy0, fx1, fy1, scale)
REGIONS = [
    ("R1 Y-row right: tail units + dots", 530, 340, 850, 400, 3),
    ("R2 X-row right: tail units + dots", 530, 452, 850, 490, 3),
    ("R3 Y-row left + upper gutter", 60, 340, 430, 400, 2),
    ("R4 info panel", 93, 106, 867, 338, 1.4),
    ("R5 caption + lower gutter", 60, 440, 600, 510, 2),
]

def build_sheet(src, is_render):
    tiles = []
    for (tag, fx0, fy0, fx1, fy1, sc) in REGIONS:
        if is_render:
            x0, y0 = FX(fx0) * S, FY(fy0) * S
            x1, y1 = FX(fx1) * S, FY(fy1) * S
            c = src.crop((int(x0), int(y0), int(x1), int(y1)))
        else:
            c = src.crop((fx0, fy0, fx1, fy1))
        c = c.resize((int(c.width * sc), int(c.height * sc)), Image.LANCZOS)
        lab_h = 26
        tile = Image.new("RGB", (c.width, c.height + lab_h), (255, 255, 255))
        tile.paste(c, (0, lab_h))
        d = ImageDraw.Draw(tile)
        d.text((6, 5), tag, fill=(0, 0, 0))
        d.rectangle([0, 0, tile.width - 1, tile.height - 1], outline=(180, 180, 180))
        tiles.append(tile)
    wmax = max(t.width for t in tiles)
    htot = sum(t.height for t in tiles) + 10 * (len(tiles) - 1)
    sheet = Image.new("RGB", (wmax, htot), (255, 255, 255))
    y = 0
    for t in tiles:
        sheet.paste(t, (0, y))
        y += t.height + 10
    return sheet

a = build_sheet(ren, True)
b = build_sheet(orig, False)
a.save(f"{OUT}/sheet_render.png")
b.save(f"{OUT}/sheet_original.png")
print("sheets:", a.size, b.size)
