#!/usr/bin/env python3
"""Find the thin C00000 panel border + bottom letterbox + fit mapping."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_054.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()

def redness(p):
    r, g, b = p
    return r - max(g, b)

out = {}
# vertical border candidates: x in 50..80 and 885..915, count redness>40 pixels per column
cand = {}
for x0, x1 in [(50, 80), (885, 915)]:
    for x in range(x0, x1):
        c = sum(1 for y in range(50, 519) if redness(px[x, y]) > 40 and px[x, y][0] > 140)
        if c > 20:
            cand[x] = c
out["vborder_candidates"] = cand
# horizontal border: y in 35..50 and 505..519
cand_r = {}
for y0, y1 in [(35, 52), (505, 519)]:
    for y in range(y0, y1):
        c = sum(1 for x in range(60, 900) if redness(px[x, y]) > 40 and px[x, y][0] > 140)
        if c > 100:
            cand_r[y] = c
out["hborder_candidates"] = cand_r

# pixel grids around top-left corner (x 52..70, y 38..50) — print redness values
def grid(x0, x1, y0, y1):
    rows = []
    for y in range(y0, y1):
        rows.append("".join("R" if (redness(px[x,y])>40 and px[x,y][0]>140) else ("." if sum(px[x,y])>600 else "o") for x in range(x0, x1)))
    return rows
out["grid_topleft_x52_72_y38_50"] = grid(52, 72, 38, 50)
out["grid_topright_x895_915_y38_50"] = grid(895, 915, 38, 50)
out["grid_botleft_x52_72_y508_519"] = grid(52, 72, 508, 519)
out["grid_botright_x895_915_y508_519"] = grid(895, 915, 508, 519)
# left border color samples at found x
if cand:
    xl = min(cand)
    out["left_border_x_min"] = xl
    out["left_border_colors"] = [px[xl, y] for y in (100, 250, 400)]
    xr = max(cand)
    out["right_border_x_max"] = xr
    out["right_border_colors"] = [px[xr, y] for y in (100, 250, 400)]
print(json.dumps(out, indent=1, default=str))
