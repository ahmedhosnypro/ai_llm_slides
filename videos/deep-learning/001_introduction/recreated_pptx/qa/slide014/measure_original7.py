#!/usr/bin/env python3
"""Pass 7: exact fill-run extraction for box bboxes + border color sampling."""
import json
from collections import Counter
from PIL import Image

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_014.jpg").convert("RGB")
W, H = img.size
px = img.load()
out = {}

def cls(p):
    r, g, b = p
    if r > 235 and g > 235 and b > 235: return "."
    if r > 140 and g < 90 and b < 90: return "R"
    if 120 < r < 200 and g < 60 and b < 60: return "D"
    if g > 90 and g - r > 40 and g - b > 20 and r < 120: return "G"
    if b > 90 and b - r > 50 and b - g > 40: return "B"
    if r < 90 and g < 90 and b < 90: return "K"
    if 235 < r <= 255 and 200 < g < 240 and 165 < b < 215: return "T"
    if r > 235 and g > 235 and 195 < b < 240: return "Y"
    if 200 < r < 245 and g > 230 and b > 230: return "I"
    if 180 < r < 245 and 220 < g < 250 and 235 < b <= 256: return "i"
    return "?"

def runs(row_y, classes, min_len=8):
    res = []
    cur = None
    for x in range(50, 920):
        c = cls(px[x, row_y])
        if c in classes:
            if cur and cur[2] == c and x - cur[1] <= 2: cur[1] = x
            else:
                if cur and cur[1] - cur[0] >= min_len: res.append(tuple(cur))
                cur = [x, x, c]
        else:
            if cur and cur[1] - cur[0] >= min_len: res.append(tuple(cur))
            cur = None
    if cur and cur[1] - cur[0] >= min_len: res.append(tuple(cur))
    return res

# box fill vertical extents: use center columns of each box
def col_runs(col_x, classes, min_len=8):
    res = []
    cur = None
    for y in range(130, 380):
        c = cls(px[col_x, y])
        if c in classes:
            if cur and cur[2] == c and y - cur[1] <= 2: cur[1] = y
            else:
                if cur and cur[1] - cur[0] >= min_len: res.append(tuple(cur))
                cur = [y, y, c]
        else:
            if cur and cur[1] - cur[0] >= min_len: res.append(tuple(cur))
            cur = None
    if cur and cur[1] - cur[0] >= min_len: res.append(tuple(cur))
    return res

out["row200_runs"] = runs(200, "GDRTIYB")
out["row250_runs"] = runs(250, "GDRTIYB")
out["row275_runs"] = runs(275, "GDRTIYB")
out["col180_green_runs"] = col_runs(180, "G")
out["col400_darkred_runs"] = col_runs(400, "DR")
out["col600_ice_runs"] = col_runs(600, "I")
out["col710_tan_runs"] = col_runs(710, "T")
out["col810_yellow_runs"] = col_runs(810, "Y")

# ice box borders: sample rows/cols just outside the fill
# first get ice fill bbox precisely with row/col counts
def fill_bbox(ch, minrun=30):
    xs, ys = [], []
    for y in range(140, 370):
        for x in range(60, 900):
            if cls(px[x, y]) == ch:
                xs.append(x); ys.append(y)
    if not xs: return None
    return (min(xs), max(xs), min(ys), max(ys))

ib = fill_bbox("I")
out["ice_fill_bbox"] = ib
x0, x1, y0, y1 = ib
out["ice_border_samples"] = {
    "above_top": [px[x, y0 - 2] for x in range(560, 660, 25)],
    "top_row": [px[x, y0 - 1] for x in range(560, 660, 25)],
    "below_bottom": [px[x, y1 + 2] for x in range(560, 660, 25)],
    "bottom_row": [px[x, y1 + 1] for x in range(560, 660, 25)],
    "left_col": [px[x0 - 1, y] for y in range(230, 280, 12)],
    "right_col": [px[x1 + 1, y] for y in range(230, 280, 12)],
    "outside_left": [px[x0 - 3, y] for y in range(230, 280, 12)],
    "outside_right": [px[x1 + 3, y] for y in range(230, 280, 12)],
}
# scan ice box border rows: count navy/ice-border pixels per row near box
def rowclass_counts(y, x0_, x1_):
    return Counter(cls(px[x, y]) for x in range(x0_, x1_))
out["ice_rows_288_298"] = {y: dict(rowclass_counts(y, 540, 670)) for y in range(288, 299)}
out["ice_rows_190_200"] = {y: dict(rowclass_counts(y, 540, 670)) for y in range(190, 200)}

# darkred box: exact fill runs at several rows
out["dr_row210"] = runs(210, "D", 20)
out["dr_row300"] = runs(300, "D", 20)
out["dr_col350"] = col_runs(350, "DR", 20)

# green box
out["green_fill_bbox"] = fill_bbox("G")
# tan
out["tan_fill_bbox"] = fill_bbox("T")
# yellow
out["yellow_fill_bbox"] = fill_bbox("Y")
# navy panel strokes
out["navy_fill_bbox"] = fill_bbox("B")

# yellow box border? sample outside yellow fill
yb = fill_bbox("Y")
if yb:
    out["yellow_edges"] = {
        "top_above": [px[x, yb[2] - 1] for x in range(780, 850, 20)],
        "left_of": [px[yb[0] - 1, y] for y in range(240, 270, 10)],
        "right_of": [px[yb[1] + 1, y] for y in range(240, 270, 10)],
        "below": [px[x, yb[3] + 1] for x in range(780, 850, 20)],
    }

# cursor icon region below ice box (map showed c's around y301-313 x~640-660)
curs = []
for y in range(295, 330):
    for x in range(600, 700):
        r, g, b = px[x, y]
        if r < 200 and abs(r - g) < 30 and abs(g - b) < 30 and r > 60:
            curs.append((x, y, (r, g, b)))
xs = [c[0] for c in curs]; ys = [c[1] for c in curs]
out["cursor_gray_pts_bbox"] = (min(xs), max(xs), min(ys), max(ys)) if curs else None
out["cursor_n"] = len(curs)

print(json.dumps(out, indent=1, default=str))
