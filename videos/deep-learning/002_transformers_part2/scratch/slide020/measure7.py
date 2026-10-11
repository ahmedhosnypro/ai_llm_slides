#!/usr/bin/env python3
"""Phase 7: decisive column profiles + box-edge color samples."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_020.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()
out = {}


def is_red(p):
    r, g, b = p
    return r > 130 and (r - g) > 45 and (r - b) > 45


def is_darkred(p):
    r, g, b = p
    return 110 < r < 190 and g < 60 and b < 60


def is_green(p):
    r, g, b = p
    return g > 100 and (g - r) > 40 and (g - b) > 20


def is_blue(p):
    r, g, b = p
    return b > 120 and (b - r) > 40 and (b - g) > 40


def colprof(x0, x1, y0, y1, pred, minn=1):
    prof = []
    for x in range(x0, x1):
        n = sum(1 for y in range(y0, y1) if pred(px[x, y]))
        if n >= minn:
            prof.append([x, n])
    return prof


def spans_of(prof, gap=3):
    sp = []
    cur = None
    for x, n in prof:
        if cur and x <= cur[1] + gap:
            cur[1] = x; cur[2] = max(cur[2], n)
        else:
            if cur: sp.append(cur)
            cur = [x, x, n]
    if cur: sp.append(cur)
    return sp


# row1 band: red column profile rows 96..140 (boxes+labels), tall spans = edges
p = colprof(60, 910, 96, 140, is_red)
out["row1_red_cols_spans"] = spans_of(p, 4)
# row1: what vertical extent do red pixels have per column cluster? sample tall spans
# row4 band: red columns rows 335..415
p4 = colprof(60, 910, 335, 415, is_red)
out["row4_red_cols_spans"] = spans_of(p4, 4)
# row2: green columns rows 150..200
p2 = colprof(60, 910, 150, 200, is_green)
out["row2_green_cols_spans"] = spans_of(p2, 4)
# row2: yellow cell columns rows 158..190
def is_yel_cell(p):
    r, g, b = p
    return r > 225 and 200 < g < 245 and 120 < b < 190
out["row2_yellow_spans"] = spans_of(colprof(60, 910, 158, 190, is_yel_cell), 2)
# row2: pink cell columns
def is_pink_cell(p):
    r, g, b = p
    return r > 225 and 120 < g < 190 and 150 < b < 215
out["row2_pink_spans"] = spans_of(colprof(60, 910, 158, 190, is_pink_cell), 2)
# row3: blue columns rows 212..262
p3 = colprof(60, 910, 212, 262, is_blue)
out["row3_blue_cols_spans"] = spans_of(p3, 4)
# banner: darkred column profile rows 296..328
out["banner_darkred_col_spans"] = spans_of(colprof(40, 920, 296, 328, is_darkred), 4)[:6] + ["..."] + spans_of(colprof(40, 920, 296, 328, is_darkred), 4)[-4:]
# brace: red rows 400..425, columns
out["brace_red_col_spans"] = spans_of(colprof(60, 910, 400, 425, is_red), 6)[:10] + ["..."] + spans_of(colprof(60, 910, 400, 425, is_red), 6)[-6:]
# delta glyphs: red columns rows 246..266 excluding arrows
dd = colprof(90, 860, 246, 266, is_red)
out["delta_col_spans_raw"] = spans_of(dd, 5)
# bolts: orange columns rows 246..262
def is_orange(p):
    r, g, b = p
    return r > 200 and 120 < g < 200 and b < 110
out["bolt_col_spans"] = spans_of(colprof(60, 910, 244, 264, is_orange), 4)
# label texts: green/blue/gray in label col rows per line
def rowprof(x0, x1, y0, y1, pred):
    prof = []
    for y in range(y0, y1):
        n = sum(1 for x in range(x0, x1) if pred(px[x, y]))
        if n:
            prof.append([y, n])
    return prof

def is_graytxt(p):
    r, g, b = p
    return abs(r - g) < 25 and abs(g - b) < 25 and 60 < r < 170

out["lab1_gray_rows"] = rowprof(40, 170, 80, 150, is_graytxt)
out["lab2_green_rows"] = rowprof(40, 170, 145, 210, is_green)
out["lab3_blue_rows"] = rowprof(40, 170, 215, 275, is_blue)
out["lab4_red_rows_x30_95"] = rowprof(30, 95, 280, 430, is_red)   # left of banner?
out["lab4_red_cols_r301_329"] = spans_of(colprof(30, 175, 301, 330, is_red), 4)
# color samples: 3x3 mean at points of interest
def samp(x, y):
    rs = gs = bs = 0
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            r, g, b = px[x + dx, y + dy]
            rs += r; gs += g; bs += b
    return f"#{rs//9:02X}{gs//9:02X}{bs//9:02X}"

out["samples"] = {
    "row1_box1_center_230_100": samp(230, 100),
    "row1_box1_center_230_112": samp(230, 112),
    "row1_above_lab_230_103": samp(230, 103),
    "row1_gap_470_112": samp(470, 112),
    "row1_left_edge_190_112": samp(190, 112),
    "row1_edge_196_100": samp(196, 100),
    "row1_edge_197_112": samp(197, 112),
    "row2_box1_100_170": samp(100, 170),
    "row2_yellow_200_172": samp(200, 172),
    "row2_pink_212_172": samp(212, 172),
    "row3_box1_100_235": samp(100, 235),
    "row4_box1_230_380": samp(230, 380),
    "row4_fill_gap_470_380": samp(470, 380),
    "banner_400_310": samp(400, 310),
    "brace_480_412": samp(480, 412),
    "inset_130_460": samp(130, 460),
    "lab1_90_100": samp(90, 100),
    "lab4_60_315": samp(60, 315),
    "caption_500_462": samp(500, 462),
}
print(json.dumps(out, indent=1))
