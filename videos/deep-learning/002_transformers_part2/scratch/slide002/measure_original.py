#!/usr/bin/env python3
"""PIL-measure slide_002.jpg (960x540, 1px = 1pt) — chrome, title lines, bottom strip, cursor."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_002.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()
print(f"size: {W}x{H}")

def is_red(p):    r,g,b = p; return r > 140 and g < 70 and b < 70
def is_black(p):  r,g,b = p; return r < 60 and g < 60 and b < 60
def is_yellowish(p): r,g,b = p; return r > 200 and g > 200 and b < 180
def is_purple(p): r,g,b = p; return 90 <= r <= 160 and 60 <= g <= 120 and b > 160
def is_grayish(p): r,g,b = p; return abs(r-g) < 25 and abs(g-b) < 25 and 60 < r < 200

out = {}

# 1. bottom rows: black strip?
black_rows = []
for y in range(H-1, -1, -1):
    cnt = sum(1 for x in range(0, W, 4) if is_black(px[x, y]))
    if cnt > (W/4) * 0.9:
        black_rows.append(y)
    else:
        break
out["bottom_black_rows_desc"] = black_rows[:5] + (["..."] if len(black_rows) > 5 else [])
out["bottom_black_row_count"] = len(black_rows)
# also check rows just above the black strip for what's there
for y in [H-1, H-20, H-25, H-27, H-28, H-29, H-30, H-31, H-32, H-40]:
    if 0 <= y < H:
        row = [px[x, y] for x in range(0, W, 96)]
        out[f"row_y{y}_sample"] = row[:10]

# 2. red border: scan for vertical red strokes (columns with many red px)
red_cols = [x for x in range(W) if sum(1 for y in range(0, H, 3) if is_red(px[x, y])) > 30]
red_rows = [y for y in range(H) if sum(1 for x in range(0, W, 3) if is_red(px[x, y])) > 30]
out["red_border_cols"] = (min(red_cols), max(red_cols)) if red_cols else None
out["red_border_rows"] = (min(red_rows), max(red_rows)) if red_rows else None

# 3. panel fill: sample interior away from text
out["panel_fill_samples"] = [px[100, 400], px[480, 470], px[850, 300], px[60, 60]]

# 4. badge: yellow pixels in top-right quadrant
ys = [y for y in range(0, 200) for x in range(750, 960) if is_yellowish(px[x, y]) or is_purple(px[x, y])]
xs = [x for y in range(0, 200) for x in range(750, 960) if is_yellowish(px[x, y]) or is_purple(px[x, y])]
if ys:
    out["badge_bbox"] = (min(xs), min(ys), max(xs), max(ys))
    # sample fill + ring core colors
    from collections import Counter
    fills = Counter()
    for y in range(min(ys), max(ys)+1):
        for x in range(min(xs), max(xs)+1):
            p = px[x, y]
            if is_yellowish(p): fills[p] += 1
    out["badge_fill_top"] = fills.most_common(3)
    rings = Counter()
    for y in range(min(ys), max(ys)+1):
        for x in range(min(xs), max(xs)+1):
            p = px[x, y]
            if is_purple(p): rings[p] += 1
    out["badge_ring_top"] = rings.most_common(3)
    # numeral: dark pixels inside badge
    darks = [(x, y) for y in range(min(ys), max(ys)+1) for x in range(min(xs), max(xs)+1)
             if is_black(px[x, y])]
    if darks:
        out["badge_numeral_bbox"] = (min(d[0] for d in darks), min(d[1] for d in darks),
                                     max(d[0] for d in darks), max(d[1] for d in darks))

# 5. title ink: red pixels in central region (exclude border cols/rows and badge area)
border_l = min(red_cols) if red_cols else 42
border_r = max(red_cols) if red_cols else 918
ytop_border = min(red_rows) if red_rows else 45
ybot_black = (min(black_rows) - 1) if black_rows else H-1
region_rows = {}
for y in range(ytop_border + 10, ybot_black - 1):
    xs_red = [x for x in range(border_l + 12, border_r - 12) if is_red(px[x, y])]
    if xs_red:
        region_rows[y] = (min(xs_red), max(xs_red), len(xs_red))
# group contiguous rows into lines
lines = []
cur = None
for y in sorted(region_rows):
    if cur and y == cur[1] + 1:
        cur[1] = y
        cur[2].append(region_rows[y])
    else:
        if cur: lines.append(cur)
        cur = [y, y, [region_rows[y]]]
if cur: lines.append(cur)
out["red_ink_lines"] = []
for (y0, y1, segs) in lines:
    x0 = min(s[0] for s in segs); x1 = max(s[1] for s in segs)
    out["red_ink_lines"].append({
        "y0": y0, "y1": y1, "h_px": y1 - y0 + 1,
        "x0": x0, "x1": x1, "w_px": x1 - x0 + 1,
        "cx_px": (x0 + x1) / 2, "max_row_redcount": max(s[2] for s in segs),
    })

# 6. non-red ink below the title block (pen cursor candidate): dark/gray ink rows
#    in central band between last title line and black strip
last_title_y = lines[-1][1] if lines else 0
cursor_px = []
for y in range(last_title_y + 4, ybot_black):
    for x in range(border_l + 12, border_r - 12):
        p = px[x, y]
        if is_black(p) or is_grayish(p):
            cursor_px.append((x, y))
if cursor_px:
    out["cursor_candidate_bbox"] = (min(c[0] for c in cursor_px), min(c[1] for c in cursor_px),
                                    max(c[0] for c in cursor_px), max(c[1] for c in cursor_px))
    out["cursor_candidate_count"] = len(cursor_px)
else:
    out["cursor_candidate_bbox"] = None

print(json.dumps(out, indent=1, default=str))
