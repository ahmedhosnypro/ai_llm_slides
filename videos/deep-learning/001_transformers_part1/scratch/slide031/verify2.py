#!/usr/bin/env python3
"""Clean density-based verify: identical scans on frame (960x540) and render (2001x1125).
Prints both, scaled to frame space (render / S)."""
from PIL import Image

FR = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
RN = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide031/render_1.png").convert("RGB")
S = RN.width / 960.0

def mk(im):
    p = im.load(); W, H = im.size
    return p, W, H
fp, fW, fH = mk(FR)
rp, rW, rH = mk(RN)
def fc(x, y): return fp[x, y]
def rc(x, y): return rp[min(int(x * S), rW - 1), min(int(y * S), rH - 1)]

pred_red = lambda cc: cc[0] > 120 and cc[0] - cc[1] > 45 and cc[0] - cc[2] > 45
pred_blue = lambda cc: cc[2] > 110 and cc[2] - cc[0] > 40 and cc[2] - cc[1] > 30
pred_grn = lambda cc: cc[1] > 80 and cc[1] - cc[0] > 18 and cc[1] - cc[2] > 18
pred_pinkpill = lambda cc: abs(cc[0] - 255) < 12 and abs(cc[1] - 208) < 25 and abs(cc[2] - 246) < 25
pred_peach = lambda cc: 235 <= cc[0] <= 258 and 205 <= cc[1] <= 240 and 185 <= cc[2] <= 225 and cc[0] - cc[2] > 22 and cc[0] - cc[1] > 10
pred_yel = lambda cc: cc[0] > 235 and cc[1] > 210 and cc[2] < 175
isw = lambda cc: cc[0] > 244 and cc[1] > 244 and cc[2] > 244
not_bg = lambda cc: not isw(cc) and not pred_peach(cc) and sum(cc) < 700

def col_edges(get, x0, x1, y0, y1, pred, minfrac=0.5, label=""):
    """columns where frac of ys matches -> first/last"""
    first = last = None
    for x in range(x0, x1):
        n = sum(1 for y in range(y0, y1) if pred(get(x, y)))
        if n >= (y1 - y0) * minfrac:
            if first is None: first = x
            last = x
    print(f"    {label}: cols {first}..{last}")
    return first, last

def row_edges(get, x0, x1, y0, y1, pred, minfrac=0.5, label=""):
    first = last = None
    for y in range(y0, y1):
        n = sum(1 for x in range(x0, x1) if pred(get(x, y)))
        if n >= (x1 - x0) * minfrac:
            if first is None: first = y
            last = y
    print(f"    {label}: rows {first}..{last}")
    return first, last

def bbox(get, x0, y0, x1, y1, pred, label):
    xs = []; ys = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(get(x, y)):
                xs.append(x); ys.append(y)
    if xs:
        print(f"    {label}: x {min(xs)}..{max(xs)} y {min(ys)}..{max(ys)} n={len(xs)}")
    else:
        print(f"    {label}: NONE")

def both(name, fn):
    print(f"== {name} ==")
    print("  FRAME:"); fn(fc)
    print("  RENDER (frame space):"); fn(rc)

# Q panel red border
both("Q panel border strokes", lambda g: (
    row_edges(g, 70, 450, 88, 112, pred_red, 0.5, "top"),
    row_edges(g, 70, 450, 288, 312, pred_red, 0.5, "bottom"),
    col_edges(g, 46, 70, 110, 290, pred_red, 0.5, "left"),
    col_edges(g, 452, 478, 110, 290, pred_red, 0.5, "right"),
))
# Q input pill (strict pink)
both("Q input pill", lambda g: bbox(g, 60, 125, 240, 185, pred_pinkpill, "pink pill"))
# Q matrix container: non-white density edges
both("Q matrix edges", lambda g: (
    col_edges(g, 195, 400, 130, 270, lambda cc: not isw(cc), 0.85, "cols(dense nonwhite)"),
    row_edges(g, 230, 360, 100, 300, lambda cc: not isw(cc), 0.85, "rows(dense nonwhite)"),
))
# Q outcap: red outline cols
both("Q outcap red cols", lambda g: col_edges(g, 398, 470, 130, 270, pred_red, 0.3, "outline cols"))
# Q outcap rows (red outline rows near top/bottom caps)
both("Q outcap rows", lambda g: row_edges(g, 414, 449, 105, 305, pred_red, 0.25, "outline rows"))
# Q W_Q label bbox (red, tight window left of matrix, above panel bottom)
both("Q W_Q", lambda g: bbox(g, 185, 235, 265, 296, pred_red, "red ink"))
# Q X2 label
both("Q X2", lambda g: bbox(g, 105, 168, 165, 225, pred_red, "red ink"))
# Q 1xd
both("Q 1xd", lambda g: bbox(g, 170, 165, 220, 195, lambda cc: sum(cc) < 430, "dark"))
# Q role letter (above outcap, below panel top border)
both("Q role Q", lambda g: bbox(g, 402, 101, 470, 117, pred_red, "red ink"))
# K role letter zone
both("K role K zone", lambda g: bbox(g, 402, 296, 470, 316, pred_grn, "green ink"))
# callouts: strict ink = not white, not peach, sum<640
pred_ci = lambda cc: not isw(cc) and not pred_peach(cc) and sum(cc) < 640
both("callout1", lambda g: bbox(g, 430, 262, 700, 322, pred_ci, "ink"))
both("callout2", lambda g: bbox(g, 688, 296, 928, 352, pred_ci, "ink"))
both("callout3", lambda g: bbox(g, 430, 324, 700, 382, pred_ci, "ink"))
# emphasis: yellow + white box
both("emphasis yellow", lambda g: bbox(g, 600, 372, 940, 448, pred_yel, "yellow"))
pred_white_box = lambda cc: isw(cc)
both("emphasis white box", lambda g: (
    col_edges(g, 630, 910, 395, 425, pred_white_box, 0.7, "white cols"),
    row_edges(g, 660, 870, 370, 450, pred_white_box, 0.7, "white rows"),
))
# note box border rows/cols (grayish line on peach)
pred_grayline = lambda cc: abs(cc[0] - cc[1]) < 30 and abs(cc[1] - cc[2]) < 30 and 120 < (cc[0] + cc[1] + cc[2]) / 3 < 225
both("note box border", lambda g: (
    row_edges(g, 520, 880, 438, 460, pred_grayline, 0.6, "top"),
    row_edges(g, 520, 880, 508, 528, pred_grayline, 0.6, "bottom"),
    col_edges(g, 480, 505, 455, 512, pred_grayline, 0.5, "left"),
    col_edges(g, 890, 915, 455, 512, pred_grayline, 0.5, "right"),
))
# note text ink rows (blue/red) inside box
pred_noteink = lambda cc: (cc[2] > 90 and cc[2] - cc[0] > 40) or (cc[0] > 110 and cc[0] - cc[1] > 45 and cc[0] - cc[2] > 45)
both("note text rows", lambda g: row_edges(g, 500, 890, 445, 522, pred_noteink, 0.06, "blue/red ink rows"))
# title/subtitle ink extent (dark, x-limits via col profile)
pred_darkish = lambda cc: sum(cc) < 230
both("title ink cols", lambda g: col_edges(g, 80, 870, 48, 68, pred_darkish, 0.02, "dark cols"))
both("subtitle ink cols", lambda g: col_edges(g, 80, 875, 72, 92, lambda cc: sum(cc) < 400 or pred_red(cc), 0.02, "ink cols"))
# V panel + V matrix + V outcap quick
both("V outcap red cols", lambda g: col_edges(g, 812, 884, 130, 270, pred_red, 0.3, "outline cols"))
both("K outcap red cols", lambda g: col_edges(g, 400, 472, 350, 490, pred_red, 0.3, "outline cols"))
