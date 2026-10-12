#!/usr/bin/env python3
"""Refined chrome landmarks for slide_037.jpg: thin red border strokes, badge, gray panel extents."""
from PIL import Image
import json
from collections import Counter

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()

def reddish(p):   r,g,b = p; return r > 120 and g < 110 and b < 110 and (r-g) > 50 and (r-b) > 50
def is_yellowish(p): r,g,b = p; return r > 200 and g > 200 and b < 180
def is_purple(p): r,g,b = p; return 80 <= r <= 170 and 60 <= g <= 130 and b > 150
def is_black(p):  r,g,b = p; return r < 60 and g < 60 and b < 60

out = {}
ybot_black = 519  # from m0: rows 519..539 black

# vertical red strokes: count reddish px per column (search whole height above strip)
col_counts = []
for x in range(W):
    c = sum(1 for y in range(0, ybot_black, 1) if reddish(px[x, y]))
    col_counts.append((x, c))
# the panel borders are long continuous strokes; look for local maxima with c > 200
long_cols = [x for x, c in col_counts if c > 200]
out["long_red_cols"] = long_cols

# horizontal red strokes
row_counts = [(y, sum(1 for x in range(0, W, 1) if reddish(px[x, y]))) for y in range(0, ybot_black)]
long_rows = [y for y, c in row_counts if c > 300]
out["long_red_rows"] = long_rows

# badge: search only top-right corner strip x 830..960, y 30..120
ys = [y for y in range(20, 130) for x in range(820, 960) if is_yellowish(px[x, y]) or is_purple(px[x, y])]
xs = [x for y in range(20, 130) for x in range(820, 960) if is_yellowish(px[x, y]) or is_purple(px[x, y])]
if ys:
    out["badge_bbox"] = (min(xs), min(ys), max(xs), max(ys))
    out["badge_center"] = ((min(xs)+max(xs))/2.0, (min(ys)+max(ys))/2.0)
    # ring/fill colors
    fills = Counter(); rings = Counter()
    for y in range(min(ys), max(ys)+1):
        for x in range(min(xs), max(xs)+1):
            p = px[x, y]
            if is_yellowish(p): fills[p] += 1
            if is_purple(p): rings[p] += 1
    out["badge_fill_top"] = fills.most_common(2)
    out["badge_ring_top"] = rings.most_common(2)

# where does the gray panel E9E9E7 start/end horizontally? scan a clean row (y=110 — below title? title there.. pick y=220 near left edge)
def near_panel(p, tol=12):
    r,g,b = p
    return abs(r-233)<tol and abs(g-233)<tol and abs(b-231)<tol
for probe_y in [300, 460, 100]:
    xs2 = [x for x in range(0, 120) if near_panel(px[x, probe_y])]
    xs3 = [x for x in range(W-120, W) if near_panel(px[x, probe_y])]
    out[f"panel_gray_left_y{probe_y}"] = (min(xs2) if xs2 else None, max(xs2) if xs2 else None)
    out[f"panel_gray_right_y{probe_y}"] = (min(xs3) if xs3 else None, max(xs3) if xs3 else None)
# panel top: scan column x=100 downward for first gray
ys2 = [y for y in range(0, 200) if near_panel(px[100, y])]
out["panel_gray_top_x100"] = min(ys2) if ys2 else None

print(json.dumps(out, indent=1, default=str))
