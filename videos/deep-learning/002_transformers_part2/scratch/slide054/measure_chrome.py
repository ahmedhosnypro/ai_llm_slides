#!/usr/bin/env python3
"""PIL-measure slide_054.jpg chrome landmarks -> fit frame->slide mapping."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_054.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()
print(f"size: {W}x{H}")

def is_red(p):    r,g,b = p; return r > 140 and g < 70 and b < 70
def is_yellowish(p): r,g,b = p; return r > 200 and g > 200 and b < 180
def is_purple(p): r,g,b = p; return 90 <= r <= 160 and 60 <= g <= 120 and b > 160
def is_black(p):  r,g,b = p; return r < 60 and g < 60 and b < 60

out = {}
# bottom rows: black letterbox?
black_rows = []
for y in range(H-1, -1, -1):
    cnt = sum(1 for x in range(0, W, 4) if is_black(px[x, y]))
    if cnt > (W/4) * 0.9:
        black_rows.append(y)
    else:
        break
out["bottom_black_row_count"] = len(black_rows)
out["bottom_black_first_row"] = min(black_rows) if black_rows else None

# red border: vertical/horizontal strokes
red_cols = [x for x in range(W) if sum(1 for y in range(0, H, 3) if is_red(px[x, y])) > 40]
red_rows = [y for y in range(H) if sum(1 for x in range(0, W, 3) if is_red(px[x, y])) > 40]
out["red_border_cols"] = (min(red_cols), max(red_cols)) if red_cols else None
out["red_border_rows"] = (min(red_rows), max(red_rows)) if red_rows else None
# top border row precise: for the leftmost/rightmost red cols, find contiguous red rows near top
out["red_col_profile"] = {x: sum(1 for y in range(0, H, 3) if is_red(px[x, y])) for x in red_cols}
out["red_row_profile"] = {y: sum(1 for x in range(0, W, 3) if is_red(px[x, y])) for y in red_rows[:12]}

# panel fill samples (gray) + canvas
out["canvas_sample_20_20"] = px[20, 20]
out["panel_sample_100_300"] = px[100, 300]

# badge: yellow/purple pixels in top-right quadrant (x>820, y<120)
ys = [y for y in range(0, 140) for x in range(820, 960) if is_yellowish(px[x, y]) or is_purple(px[x, y])]
xs = [x for y in range(0, 140) for x in range(820, 960) if is_yellowish(px[x, y]) or is_purple(px[x, y])]
if ys:
    bb = (min(xs), min(ys), max(xs), max(ys))
    out["badge_bbox"] = bb
    out["badge_center"] = ((bb[0]+bb[2])/2, (bb[1]+bb[3])/2)
    darks = [(x, y) for y in range(bb[1], bb[3]+1) for x in range(bb[0], bb[2]+1) if is_black(px[x, y])]
    if darks:
        out["badge_numeral_bbox"] = (min(d[0] for d in darks), min(d[1] for d in darks),
                                     max(d[0] for d in darks), max(d[1] for d in darks))

print(json.dumps(out, indent=1, default=str))
