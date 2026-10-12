#!/usr/bin/env python3
"""Pass 4: text metrics, borders, box bboxes, arrow color."""
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

def modal(x0, x1, y0, y1, n=3):
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            c[px[x, y]] += 1
    return c.most_common(n)

def is_red(p): r,g,b=p; return r>140 and g<80 and b<80
def is_whiteish(p): r,g,b=p; return r>225 and g>225 and b>225
def is_black(p): r,g,b=p; return r<90 and g<90 and b<90

# 1. title/takeaway color + caps
out["title_color"] = modal(163, 500, 80, 94)
out["takeaway_color"] = modal(108, 800, 438, 450)
out["title_T_bbox"] = bbox(is_red, 162, 180, 60, 110)          # 'H' of How
out["takeaway_T_bbox"] = bbox(is_red, 108, 120, 425, 465)      # 'T' of Try
out["takeaway_g_desc"] = bbox(is_red, 233, 283, 425, 470)      # 'parameters' with p descender

# 2. red L extents
out["L_top_row42_x"] = [x for x in range(W) if is_red(px[x, 42]) or is_red(px[x, 43])]
out["L_top_row42_x"] = (min(out["L_top_row42_x"]), max(out["L_top_row42_x"])) if out["L_top_row42_x"] else None
ys = [y for y in range(H) if is_red(px[58, y]) or is_red(px[57, y])]
out["L_left_col57_58_y"] = (min(ys), max(ys)) if ys else None
out["L_stroke_color"] = modal(58, 59, 200, 260)

# 3. blue panel border colors
out["border_top"] = modal(300, 600, 134, 137)
out["border_bottom"] = modal(300, 600, 371, 374)
out["border_right"] = modal(885, 888, 200, 300)
out["border_left_samples"] = [px[x, 250] for x in range(68, 80)]

# 4. mint box (Predicted Class)
def is_ice(p): r,g,b=p; return 210<r<245 and g>242 and 235<b<255
out["ice_bbox"] = bbox(is_ice, 525, 700, 140, 375)
out["ice_fill"] = modal(560, 650, 235, 270, 4)
# border of ice box: sample ring around
bb = out["ice_bbox"]
if bb:
    x0, x1, y0, y1 = bb
    out["ice_border_top"] = [px[x, y0 - 1] for x in range(570, 620, 8)]
    out["ice_border_bottom"] = [px[x, y1 + 1] for x in range(570, 620, 8)]
# black text inside ice box
out["ice_text_bbox"] = bbox(is_black, bb[0] + 2, bb[1] - 2, bb[2] + 2, bb[3] - 2) if bb else None
if out["ice_text_bbox"]:
    t = out["ice_text_bbox"]
    rows = [y for y in range(t[2], t[3] + 1) if any(is_black(px[x, y]) for x in range(t[0], t[1] + 1))]
    # group rows into lines
    lines = []
    for y in rows:
        if lines and y - lines[-1][1] <= 2: lines[-1][1] = y
        else: lines.append([y, y])
    out["ice_text_lines"] = lines
out["ice_text_color"] = modal(t[0], t[1], lines[0][0], lines[0][1], 4) if out["ice_text_bbox"] else None

# 5. green box text rows
out["green_text_bbox"] = bbox(is_whiteish, 101, 262, 226, 280)
rows = [y for y in range(226, 281) if any(is_whiteish(px[x, y]) for x in range(101, 262))]
lines = []
for y in rows:
    if lines and y - lines[-1][1] <= 2: lines[-1][1] = y
    else: lines.append([y, y])
out["green_text_lines"] = lines
out["green_text_wordcols"] = None

# 6. dark red box text rows (white text)
rows = [y for y in range(199, 305) if any(is_whiteish(px[x, y]) for x in range(306, 520))]
lines = []
for y in rows:
    if lines and y - lines[-1][1] <= 2: lines[-1][1] = y
    else: lines.append([y, y])
out["darkred_text_lines"] = lines
if lines:
    l1 = lines[0]
    cols = [x for x in range(306, 520) if any(is_whiteish(px[x, y]) for y in range(l1[0], l1[1] + 1))]
    out["darkred_line1_x"] = (min(cols), max(cols))
    if len(lines) > 1:
        l2 = lines[1]
        cols2 = [x for x in range(306, 520) if any(is_whiteish(px[x, y]) for y in range(l2[0], l2[1] + 1))]
        out["darkred_line2_x"] = (min(cols2), max(cols2))
        out["darkred_line2_color"] = modal(min(cols2), max(cols2), l2[0], l2[1], 3)

# 7. tan box: black text (Error rotated)
out["tan_text_bbox"] = bbox(is_black, 695, 725, 162, 345)

# 8. yellow box: rescan bbox with loose fill + text rows
def is_yel(p): r,g,b=p; return r>240 and g>240 and 195<b<240
out["yellow_bbox_loose"] = bbox(is_yel, 740, 890, 150, 370)
bb2 = out["yellow_bbox_loose"]
if bb2:
    rows = [y for y in range(bb2[2], bb2[3] + 1) if any(is_black(px[x, y]) for x in range(bb2[0], bb2[1] + 1))]
    lines = []
    for y in rows:
        if lines and y - lines[-1][1] <= 2: lines[-1][1] = y
        else: lines.append([y, y])
    out["yellow_text_lines"] = lines
    if lines:
        l1 = lines[0]
        cols = [x for x in range(bb2[0], bb2[1] + 1) if any(is_black(px[x, y]) for y in range(l1[0], l1[1] + 1))]
        out["yellow_line1_bbox"] = (min(cols), max(cols), l1[0], l1[1])
    out["yellow_fill"] = modal(bb2[0] + 5, bb2[0] + 25, bb2[2] + 3, bb2[2] + 10, 3)

# 9. arrow color
out["arrow_color"] = modal(291, 300, 249, 255, 4)

# 10. green/darkred/tan/yellow exact box edges via fill predicates at strict thresholds
def is_green(p): r,g,b=p; return g>100 and g-r>60 and g-b>30
out["green_box"] = bbox(is_green, 90, 280, 210, 300)
def is_dr(p): r,g,b=p; return 130<r<185 and g<40 and b<40
out["darkred_box"] = bbox(is_dr, 295, 530, 180, 320)
def is_tan(p): r,g,b=p; return 235<r<255 and 205<g<235 and 180<b<210
out["tan_box"] = bbox(is_tan, 685, 735, 150, 360)

# 11. dark red box: does it have a border/darker outline? sample edges
out["darkred_edge_samples"] = {"left": [px[304, y] for y in (220, 250, 280)], "top": [px[x, 197] for x in (350, 420, 480)]}

print(json.dumps(out, indent=1, default=str))
