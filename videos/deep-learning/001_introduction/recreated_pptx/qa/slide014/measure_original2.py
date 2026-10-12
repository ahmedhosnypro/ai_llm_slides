#!/usr/bin/env python3
"""Precise measurement pass 2: interval-based structure extraction for slide_014.jpg."""
import json
from PIL import Image

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_014.jpg").convert("RGB")
W, H = img.size
px = img.load()

def intervals(mask_list, gap=2):
    """merge sorted x values into intervals allowing gap"""
    if not mask_list:
        return []
    s = sorted(mask_list)
    out = [[s[0], s[0]]]
    for v in s[1:]:
        if v - out[-1][1] <= gap:
            out[-1][1] = v
        else:
            out.append([v, v])
    return out

def is_red(p): r,g,b=p; return r>150 and g<80 and b<80
def is_blue(p): r,g,b=p; return b>150 and b-r>70 and b-g>50
def is_black(p): r,g,b=p; return r<70 and g<70 and b<70

out = {}

# ---- blue border rect: precise strokes ----
# top stroke: rows with many blue pixels
blue_rows = []
for y in range(100, 420):
    c = sum(1 for x in range(40, 920) if is_blue(px[x, y]))
    if c > 300: blue_rows.append((y, c))
out["blue_full_rows"] = blue_rows[:6] + blue_rows[-6:] if len(blue_rows) > 12 else blue_rows
blue_cols = []
for x in range(40, 920):
    c = sum(1 for y in range(100, 420) if is_blue(px[x, y]))
    if c > 100: blue_cols.append((x, c))
out["blue_full_cols"] = blue_cols[:4] + blue_cols[-4:] if len(blue_cols) > 8 else blue_cols

# ---- red interval rows: y78..96 (title), 197..306 (arrows), 438..449 (takeaway) ----
def red_x_intervals(y0, y1, min_run=3):
    """columns containing red within the row band"""
    cols = [x for x in range(W) if any(is_red(px[x, y]) for y in range(y0, y1 + 1))]
    return intervals(cols, gap=6)

out["title_red_cols_y78_96"] = red_x_intervals(78, 96)
out["takeaway_red_cols_y438_449"] = red_x_intervals(438, 449)

# arrows band: get red intervals at specific rows
for y in (200, 215, 230, 250, 270, 290, 300):
    cols = [x for x in range(W) if is_red(px[x, y])]
    iv = intervals(cols, gap=4)
    out[f"red_row_{y}"] = [[i[0], i[1]] for i in iv if i[1] - i[0] > 1]

# ---- node boxes: column profile of fill colors inside panel y140..370 ----
def runs_of(pred, xs_range, ys_range):
    """for each x in range, count pixels in y range matching pred; return intervals with count>min"""
    prof = {}
    for x in xs_range:
        c = sum(1 for y in ys_range if pred(px[x, y]))
        if c > 5: prof[x] = c
    return intervals(list(prof.keys()), gap=3)

def is_green(p): r,g,b=p; return g>90 and g-r>40 and g-b>20 and r<120
def is_darkred(p): r,g,b=p; return 120<r<200 and g<60 and b<70
def is_lightblue(p): r,g,b=p; return r>170 and 200<g<245 and b>235 and b-r>25
def is_tan(p): r,g,b=p; return r>220 and 200<g<240 and 150<b<205 and r-b>40
def is_lightyellow(p): r,g,b=p; return r>235 and g>235 and 150<b<225 and r-b>30

YB = range(150, 360)  # panel interior
out["green_cols"] = runs_of(is_green, range(60, 900), YB)
out["darkred_cols"] = runs_of(is_darkred, range(60, 900), YB)
out["lightblue_cols"] = runs_of(is_lightblue, range(60, 900), YB)
out["tan_cols"] = runs_of(is_tan, range(60, 900), YB)
out["lightyellow_cols"] = runs_of(is_lightyellow, range(60, 900), YB)

def rows_of(pred, x0, x1, y0=100, y1=430):
    prof = {}
    for y in range(y0, y1):
        c = sum(1 for x in range(x0, x1 + 1) if pred(px[x, y]))
        if c > 5: prof[y] = c
    return intervals(list(prof.keys()), gap=3)

if out["green_cols"]:
    g0, g1 = out["green_cols"][0]
    out["green_rows"] = rows_of(is_green, g0, g1)
if out["darkred_cols"]:
    d0, d1 = out["darkred_cols"][0]
    out["darkred_rows"] = rows_of(is_darkred, d0, d1)
if out["lightblue_cols"]:
    l0, l1 = out["lightblue_cols"][0]
    out["lightblue_rows"] = rows_of(is_lightblue, l0, l1, 100, 430)
if out["tan_cols"]:
    t0, t1 = out["tan_cols"][0]
    out["tan_rows"] = rows_of(is_tan, t0, t1)
if out["lightyellow_cols"]:
    y0_, y1_ = out["lightyellow_cols"][0]
    out["lightyellow_rows"] = rows_of(is_lightyellow, y0_, y1_)

# ---- red frame lines (top + left per slide-007 pattern?) ----
# scan rows 30..80 for red intervals
for y in (40, 42, 43, 44, 46, 50):
    cols = [x for x in range(W) if is_red(px[x, y])]
    out[f"red_row_{y}"] = intervals(cols, gap=6)
# scan cols 50..75 for red rows
for x in (56, 58, 60):
    rows = [y for y in range(H) if is_red(px[x, y])]
    out[f"red_col_{x}"] = intervals(rows, gap=6)

print(json.dumps(out, indent=1))
