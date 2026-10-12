#!/usr/bin/env python3
"""Pass 3: precise sub-measurements — arrows, light-blue box, panel border, fonts, frame lines."""
import json
from collections import Counter
from PIL import Image

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_014.jpg").convert("RGB")
W, H = img.size
px = img.load()
out = {}

def is_red(p): r,g,b=p; return r>140 and g<80 and b<80

def bbox(pred, x0, x1, y0, y1):
    pts = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if pred(px[x, y])]
    if not pts: return None
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return (min(xs), max(xs), min(ys), max(ys))

# ---- arrows: full 2D bboxes in the gap regions ----
gaps = {
    "gap1_green_to_darkred": (264, 304, 130, 380),
    "gap2_darkred_to_next": (522, 560, 130, 380),
    "gap3_next_to_tan": (661, 692, 130, 380),
    "gap4_tan_to_yellow": (727, 761, 130, 380),
}
for name, (x0, x1, y0, y1) in gaps.items():
    out[f"red_bbox_{name}"] = bbox(is_red, x0, x1, y0, y1)

# column profiles through each gap at its red center to find arrowhead width
for name, (x0, x1, y0, y1) in gaps.items():
    bb = out[f"red_bbox_{name}"]
    if bb:
        cx = (bb[0] + bb[1]) // 2
        prof = []
        for x in range(bb[0], bb[1] + 1):
            c = sum(1 for y in range(bb[2], bb[3] + 1) if is_red(px[x, y]))
            prof.append((x, c))
        out[f"col_profile_{name}"] = prof

# ---- light-blue "Predicted Class" box: find fill color around x560..660 y220..290 ----
region = Counter()
for y in range(215, 300):
    for x in range(540, 670):
        p = px[x, y]
        region[p] += 1
out["modal_colors_x540_670_y215_300"] = region.most_common(8)

def is_mint(p): r,g,b=p; return 180<r<235 and 200<g<245 and 200<b<245 and abs(g-b)<20 and r<g
out["mint_bbox"] = bbox(is_mint, 530, 690, 130, 380)

# ---- panel blue border precise ----
def is_blueish(p): r,g,b=p; return b>140 and b-r>60 and b-g>40
out["blue_left_stroke"] = bbox(is_blueish, 60, 90, 140, 370)
out["blue_right_stroke"] = bbox(is_blueish, 875, 900, 140, 370)
out["blue_top_stroke"] = bbox(is_blueish, 100, 800, 125, 145)
out["blue_bottom_stroke"] = bbox(is_blueish, 100, 800, 360, 385)

# ---- box fills modal colors ----
def modal(x0, x1, y0, y1, n=4):
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            c[px[x, y]] += 1
    return c.most_common(n)

out["fill_green"] = modal(110, 250, 235, 270)
out["fill_darkred"] = modal(480, 515, 200, 230)
out["fill_mintbox"] = modal(570, 650, 240, 270) if out["mint_bbox"] else None
out["fill_tan"] = modal(698, 722, 180, 210)
out["fill_yellow"] = modal(770, 850, 240, 270)
out["bg_corner"] = [px[5, 5], px[950, 5], px[5, 300], px[480, 30]]
out["panel_interior"] = modal(300, 303, 150, 190, 2)

# ---- title per-word caps: first word 'How' ----
out["title_H_bbox"] = bbox(is_red, 160, 180, 60, 110)
out["title_full_bbox"] = bbox(is_red, 100, 860, 55, 120)
# word extents in title band
def word_intervals(y0, y1, x0=100, x1=860, gap=8):
    cols = [x for x in range(x0, x1) if any(is_red(px[x, y]) for y in range(y0, y1))]
    if not cols: return []
    ivs = [[cols[0], cols[0]]]
    for v in cols[1:]:
        if v - ivs[-1][1] <= gap: ivs[-1][1] = v
        else: ivs.append([v, v])
    return ivs
out["title_words"] = word_intervals(70, 105)
# descender check: rows of red in full title band
def rows_of(pred, x0, x1, y0, y1):
    return [y for y in range(y0, y1) if any(pred(px[x, y]) for x in range(x0, x1))]
out["title_rows_all"] = (rows_of(is_red, 160, 790, 55, 115)[:3], rows_of(is_red, 160, 790, 55, 115)[-3:])

# ---- takeaway per-word ----
out["takeaway_full_bbox"] = bbox(is_red, 90, 840, 425, 465)
out["takeaway_rows"] = (rows_of(is_red, 100, 820, 420, 470)[:3], rows_of(is_red, 100, 820, 420, 470)[-3:])
out["takeaway_words"] = word_intervals(430, 460, 90, 840, gap=7)

# ---- frame lines: loose red scan top rows and left cols ----
def is_red_loose(p): r,g,b=p; return r>110 and r-g>40 and r-b>40
out["top_rows_red_loose_y0_70"] = [y for y in range(0, 70) if sum(1 for x in range(0, W, 3) if is_red_loose(px[x, y])) > 20]
out["left_cols_red_loose_x0_60"] = [x for x in range(0, 60) if sum(1 for y in range(0, H, 3) if is_red_loose(px[x, y])) > 15]
# dark red border of chrome: check the actual frame edges of THIS original
out["edge_samples"] = {
    "y22_row": [px[x, 22] for x in (100, 400, 700, 900)],
    "x19_col": [px[19, y] for y in (100, 250, 400)],
    "y5_5": px[5, 5], "y270_x30": px[30, 270], "y270_x35": px[35, 270],
    "y44_x480": px[480, 44], "y45_x480": px[480, 45],
}

# ---- black bar precise ----
def is_black(p): r,g,b=p; return r<70 and g<70 and b<70
out["black_bar_bbox"] = bbox(is_black, 0, W, 505, H)
out["black_bar_rows"] = [y for y in range(505, H) if sum(1 for x in range(0, W, 5) if is_black(px[x, y])) > 100]

# ---- white panel interior extent ----
def is_whiteish(p): r,g,b=p; return r>235 and g>235 and b>235
out["white_bbox_inside_blue"] = bbox(is_whiteish, 80, 880, 140, 368)

print(json.dumps(out, indent=1, default=str))
