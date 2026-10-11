#!/usr/bin/env python3
"""Measure slide_039 frame: chrome landmarks -> frame->slide mapping, then every
content element's ink bbox in frame px and mapped slide pts (1px frame = 1pt/0.958)."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_039.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()
out = {"size": [W, H]}

def reddish(p, thr=50):
    r, g, b = p
    return r > 120 and (r - g) > thr and (r - b) > thr

def blueish(p):
    r, g, b = p
    return b > 110 and (b - r) > 60 and (b - g) > 40

def darkish(p):
    return sum(p) < 260

# ---- 1. chrome landmarks: red border columns/rows
# left border: scan columns 40..80 for tall reddish runs
def red_col_frac(x):
    return sum(1 for y in range(40, 520) if reddish(px[x, y])) / 480.0
def red_row_frac(y):
    return sum(1 for x in range(50, 910) if reddish(px[x, y])) / 860.0

cols = [x for x in range(40, 100) if red_col_frac(x) > 0.5]
rcols = [x for x in range(880, 920) if red_col_frac(x) > 0.5]
rows = [y for y in range(30, 60) if red_row_frac(y) > 0.5]
# bottom border: red row near 500..525
brows = [y for y in range(495, 525) if red_row_frac(y) > 0.5]
out["chrome_left_cols"] = cols
out["chrome_right_cols"] = rcols
out["chrome_top_rows"] = rows
out["chrome_bottom_rows"] = brows

# badge: yellow fill bbox (FDFD96-ish: high r,g, b ~150-230)
ypts = [(x, y) for y in range(40, 115) for x in range(835, 905)
        if px[x, y][0] > 235 and px[x, y][1] > 235 and 120 < px[x, y][2] < 215]
if ypts:
    bx0, by0 = min(p[0] for p in ypts), min(p[1] for p in ypts)
    bx1, by1 = max(p[0] for p in ypts), max(p[1] for p in ypts)
    out["badge_yellow_bbox"] = [bx0, by0, bx1, by1]
    out["badge_yellow_center"] = [(bx0 + bx1) / 2, (by0 + by1) / 2]

# black strip: bottom rows fully dark
strip_rows = [y for y in range(H - 40, H) if sum(1 for x in range(100, 860) if sum(px[x, y]) < 120) > 700]
out["black_strip_rows"] = (strip_rows[0], strip_rows[-1]) if strip_rows else None

print(json.dumps(out, indent=1))
