#!/usr/bin/env python3
"""Pass 5: strict box bboxes, per-line text x-ranges, cap heights, stroke colors, L extents."""
import json
from collections import Counter
from PIL import Image

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_014.jpg").convert("RGB")
W, H = img.size
px = img.load()
out = {}

def bbox(pred, x0, x1, y0, y1):
    pts = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if pred(px[x, y])]
    if not pts: return None
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return (min(xs), max(xs), min(ys), max(ys))

def modal_red(x0, x1, y0, y1):
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]
            if r > 120 and r - g > 60 and r - b > 60:
                c[(r, g, b)] += 1
    return c.most_common(4)

def lines_from(pred, x0, x1, y0, y1, gap=2):
    rows = [y for y in range(y0, y1) if any(pred(px[x, y]) for x in range(x0, x1))]
    ls = []
    for y in rows:
        if ls and y - ls[-1][1] <= gap: ls[-1][1] = y
        else: ls.append([y, y])
    res = []
    for l in ls:
        cols = [x for x in range(x0, x1) if any(pred(px[x, y]) for y in range(l[0], l[1] + 1))]
        res.append({"y": l, "x": (min(cols), max(cols))})
    return res

def is_red(p): r,g,b=p; return r>140 and g<80 and b<80
def is_whiteish(p): r,g,b=p; return r>225 and g>225 and b>225
def is_black(p): r,g,b=p; return r<90 and g<90 and b<90

# title/takeaway red-ink modal colors
out["title_red_modal"] = modal_red(162, 776, 78, 95)
out["takeaway_red_modal"] = modal_red(108, 815, 437, 449)

# strict node boxes by fill
def is_green(p): r,g,b=p; return 0<r<60 and 100<g<160 and 30<b<90
out["green_strict"] = bbox(is_green, 80, 290, 200, 310)
def is_dr(p): r,g,b=p; return 130<r<185 and g<35 and b<35
out["darkred_strict"] = bbox(is_dr, 280, 545, 170, 330)
def is_ice(p): r,g,b=p; return 215<r<240 and 246<g<256 and 240<b<256
out["ice_strict"] = bbox(is_ice, 520, 700, 145, 370)
def is_tan(p): r,g,b=p; return 235<r<255 and 205<g<235 and 180<b<210
out["tan_strict"] = bbox(is_tan, 680, 740, 145, 360)
def is_yel(p): r,g,b=p; return 240<r<256 and 244<g<256 and 200<b<232
out["yellow_strict"] = bbox(is_yel, 745, 885, 150, 350)

# per-line text
out["green_text"] = lines_from(is_whiteish, 102, 262, 226, 280)
out["darkred_text"] = lines_from(is_whiteish, 306, 520, 199, 305)
out["ice_text"] = lines_from(is_black, 530, 690, 160, 300)
yt = out["yellow_strict"]
out["yellow_text"] = lines_from(is_black, yt[0]+2, yt[1]-1, yt[2]+2, yt[3]-1) if yt else None
out["tan_text"] = lines_from(is_black, 693, 725, 162, 345)

# cap heights: first-letter bboxes
out["cap_green_T"] = bbox(is_whiteish, 114, 126, 240, 268)     # 'T' of Training
out["cap_dr_C"] = bbox(is_whiteish, 343, 358, 218, 242)        # 'C' of Classification
out["cap_ice_P"] = bbox(is_black, 572, 586, 222, 246)          # 'P' of Predicted
out["cap_yel_T"] = bbox(is_black, 770, 782, 224, 250)          # 'T' of True Label (approx)
out["cap_title_H"] = bbox(is_red, 162, 178, 60, 110)
out["cap_take_T"] = bbox(is_red, 108, 120, 425, 465)

# L-frame extents with loose predicate
def is_red_loose(p): r,g,b=p; return r>100 and r-g>35 and r-b>35
xs = [x for x in range(W) if is_red_loose(px[x, 43])]
out["L_top_x_extent"] = (min(xs), max(xs)) if xs else None
ys = [y for y in range(H) if is_red_loose(px[58, y])]
out["L_left_y_extent"] = (min(ys), max(ys)) if ys else None
# stroke darkness: darkest red pixel in the L
best = (255, None)
for y in range(40, 48):
    for x in range(100, 800):
        r, g, b = px[x, y]
        if r - g > 35 and r - b > 35 and r < best[0]:
            best = (r, (x, y, (r, g, b)))
out["L_top_darkest"] = best
best2 = (255, None)
for y in range(100, 500):
    for x in range(54, 62):
        r, g, b = px[x, y]
        if r - g > 35 and r - b > 35 and r < best2[0]:
            best2 = (r, (x, y, (r, g, b)))
out["L_left_darkest"] = best2

# slide 7 L stroke darkest for comparison
img7 = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_007.jpg").convert("RGB")
px7 = img7.load()
best7 = (255, None)
for y in range(40, 48):
    for x in range(100, 800):
        r, g, b = px7[x, y]
        if r - g > 35 and r - b > 35 and r < best7[0]:
            best7 = (r, (x, y, (r, g, b)))
out["slide7_L_top_darkest"] = best7

# panel border strokes: strict column/row profiles of dark blue
def is_navy(p): r,g,b=p; return b>90 and b-r>60 and b-g>60 and r<160
out["navy_left_cols"] = [x for x in range(60, 90) if sum(1 for y in range(140, 370) if is_navy(px[x, y])) > 150]
out["navy_right_cols"] = [x for x in range(875, 900) if sum(1 for y in range(140, 370) if is_navy(px[x, y])) > 150]
out["navy_top_rows"] = [y for y in range(125, 145) if sum(1 for x in range(90, 870) if is_navy(px[x, y])) > 500]
out["navy_bot_rows"] = [y for y in range(360, 385) if sum(1 for x in range(90, 870) if is_navy(px[x, y])) > 500]
out["navy_darkest"] = None
bl = min(Counter(px[x, y] for y in range(140, 370) for x in range(72, 78)).items(), key=lambda kv: sum(kv[0]))
out["navy_darkest_left"] = bl
br = min(Counter(px[x, y] for y in range(140, 370) for x in range(884, 890)).items(), key=lambda kv: sum(kv[0]))
out["navy_darkest_right"] = br

# ice box border: does the ice box have its own border? sample just outside strict fill
ib = out["ice_strict"]
if ib:
    out["ice_edge_samples"] = {
        "top_above": [px[x, ib[2]-1] for x in range(570, 650, 20)],
        "bottom_below": [px[x, ib[3]+1] for x in range(570, 650, 20)],
        "left_of": [px[ib[0]-1, y] for y in range(200, 280, 20)],
        "right_of": [px[ib[1]+1, y] for y in range(200, 280, 20)],
    }

# yellow box strict edges check: rows count profile
if yt:
    x0, x1, y0, y1 = yt
    rowc = {y: sum(1 for x in range(x0, x1+1) if is_yel(px[x, y])) for y in range(y0-6, y1+7)}
    out["yellow_row_counts"] = {y: c for y, c in rowc.items() if c > 10}

print(json.dumps(out, indent=1, default=str))
