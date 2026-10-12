#!/usr/bin/env python3
"""Fit frame->slide mapping for slide_037.jpg from the four chrome landmarks.
Chrome landmarks (slide space, from the playlist chrome law): panel left border x=42,
right border x=918(919), top border y=45, bottom red stroke y=538-539 (half-visible).
Method: find the red vertical border strokes and the black bottom strip in the frame,
plus the badge bbox cross-check."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()

def is_red(p):    r,g,b = p; return r > 130 and g < 80 and b < 80
def is_black(p):  r,g,b = p; return r < 60 and g < 60 and b < 60
def is_yellowish(p): r,g,b = p; return r > 200 and g > 200 and b < 180
def is_purple(p): r,g,b = p; return 90 <= r <= 160 and 60 <= g <= 120 and b > 160

out = {"size": [W, H]}

# 1. bottom black strip (video letterbox below the slide)
black_rows = []
for y in range(H-1, -1, -1):
    cnt = sum(1 for x in range(0, W, 4) if is_black(px[x, y]))
    if cnt > (W/4) * 0.9:
        black_rows.append(y)
    else:
        break
out["bottom_black_rows"] = black_rows[:6] + (["..."] if len(black_rows) > 6 else [])
out["bottom_black_count"] = len(black_rows)
ybot_black = (min(black_rows) - 1) if black_rows else H-1

# 2. vertical red border strokes: columns with long red runs
red_cols = [x for x in range(W) if sum(1 for y in range(0, ybot_black, 2) if is_red(px[x, y])) > 100]
out["red_border_cols_full"] = red_cols
# horizontal red border rows
red_rows = [y for y in range(H) if sum(1 for x in range(0, W, 2) if is_red(px[x, y])) > 200]
out["red_border_rows_full"] = red_rows

# 3. badge bbox in top-right
ys = [y for y in range(0, 200) for x in range(750, 960) if is_yellowish(px[x, y]) or is_purple(px[x, y])]
xs = [x for y in range(0, 200) for x in range(750, 960) if is_yellowish(px[x, y]) or is_purple(px[x, y])]
if ys:
    out["badge_bbox"] = (min(xs), min(ys), max(xs), max(ys))
    out["badge_center"] = ((min(xs)+max(xs))/2, (min(ys)+max(ys))/2)

# 4. panel gray fill sample (E9E9E7 = 233,233,231)
out["panel_fill_samples"] = {"x100_y110": px[100,110], "x500_y100": px[500,100], "x850_y450": px[850,450], "x60_y500": px[60,500]}

print(json.dumps(out, indent=1, default=str))
