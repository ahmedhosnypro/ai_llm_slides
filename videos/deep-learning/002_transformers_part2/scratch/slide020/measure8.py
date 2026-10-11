#!/usr/bin/env python3
"""Phase 8: remaining structure — row box edges from strong border rows, banner
white text, arrow shafts, delta glyphs, title advance fit."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_020.jpg"
img = Image.open(SRC).convert("RGB")
px = img.load()
out = {}


def is_red(p):
    r, g, b = p
    return r > 130 and (r - g) > 45 and (r - b) > 45


def is_green(p):
    r, g, b = p
    return g > 100 and (g - r) > 40 and (g - b) > 20


def is_blue(p):
    r, g, b = p
    return b > 150 and (b - r) > 60 and (b - g) > 60   # strict blue (borders/labels, not lavender)


def is_darkred(p):
    r, g, b = p
    return 110 < r < 190 and g < 60 and b < 60


def runs_of(mask_cols, gap=3):
    sp = []
    cur = None
    for x in mask_cols:
        if cur and x <= cur[1] + gap:
            cur[1] = x
        else:
            if cur: sp.append(tuple(cur))
            cur = [x, x]
    if cur: sp.append(tuple(cur))
    return sp


def cols_with(pred, x0, x1, y0, y1, minn=1):
    return [x for x in range(x0, x1) if sum(1 for y in range(y0, y1) if pred(px[x, y])) >= minn]


# row1: strong red rows 110-120 are labels; box borders? scan rows 96..108 & 122..135 for red cols
out["row1_redcols_top"] = runs_of(cols_with(is_red, 150, 900, 96, 108, 2), 3)
out["row1_redcols_bot"] = runs_of(cols_with(is_red, 150, 900, 122, 136, 2), 3)
# row2 box edges: green rows 155-157 and 190-193
out["row2_greencols_top"] = runs_of(cols_with(is_green, 130, 910, 153, 158, 2), 3)
out["row2_greencols_bot"] = runs_of(cols_with(is_green, 130, 910, 189, 195, 2), 3)
# row2: green verticals mid rows 160..186
out["row2_greencols_mid"] = runs_of(cols_with(is_green, 130, 910, 160, 187, 3), 3)
# row3 box edges: strict blue rows 219..221 and 253..256
out["row3_bluecols_top"] = runs_of(cols_with(is_blue, 130, 910, 218, 222, 2), 3)
out["row3_bluecols_bot"] = runs_of(cols_with(is_blue, 130, 910, 252, 257, 2), 3)
# row4: red rows 331 (container top?) and 397-399, 411-413
out["row4_redcols_330_333"] = runs_of(cols_with(is_red, 100, 910, 330, 334, 2), 3)
out["row4_redcols_396_400"] = runs_of(cols_with(is_red, 100, 910, 396, 401, 2), 3)
out["row4_redcols_410_415"] = runs_of(cols_with(is_red, 100, 910, 410, 416, 2), 3)
out["row4_redcols_mid"] = runs_of(cols_with(is_red, 100, 910, 340, 372, 3), 3)
# brace arms: red rows 400..410 (above spine)
out["brace_rows_400_410_cols"] = runs_of(cols_with(is_red, 100, 910, 400, 411, 2), 6)

# banner white text: near-white INSIDE banner only (rows 300..325, x 170..880)
def is_white(p):
    r, g, b = p
    return r > 235 and g > 235 and b > 235

out["banner_white_rows"] = [(y, sum(1 for x in range(170, 880) if is_white(px[x, y])))
                            for y in range(296, 330) if sum(1 for x in range(170, 880) if is_white(px[x, y])) > 3]
out["banner_white_cols"] = runs_of([x for x in range(170, 880)
                                    if sum(1 for y in range(300, 326) if is_white(px[x, y])) >= 2], 8)[:6] + \
    runs_of([x for x in range(170, 880) if sum(1 for y in range(300, 326) if is_white(px[x, y])) >= 2], 8)[-4:]
out["banner_yellow_rows"] = [(y, sum(1 for x in range(170, 880) if px[x, y][0] > 200 and px[x, y][1] > 160 and px[x, y][2] < 120))
                             for y in range(296, 330) if sum(1 for x in range(170, 880) if px[x, y][0] > 200 and px[x, y][1] > 160 and px[x, y][2] < 120) > 3]

# arrow shafts: red columns rows 268..292 (between row3/delta and banner)
out["arrow_shafts_268_292"] = runs_of(cols_with(is_red, 100, 910, 268, 293, 3), 4)
# arrow1 upper part: rows 200..216 (between row2 and row3)
out["arrow_shafts_200_216"] = runs_of(cols_with(is_red, 100, 910, 200, 217, 3), 4)
# arrow3: rows 330..358 (between banner bottom and row4 boxes)
out["arrow3_shaft"] = runs_of(cols_with(is_red, 100, 910, 333, 357, 3), 4)
# arrow4: rows 424..444
out["arrow4_shaft"] = runs_of(cols_with(is_red, 100, 910, 424, 445, 3), 4)

# delta glyphs: red clusters rows 246..266 excluding arrow x ranges
dd = [x for x in range(90, 860) if not (560 <= x <= 750)
      and sum(1 for y in range(246, 267) if is_red(px[x, y])) >= 2]
out["delta_cols"] = runs_of(dd, 6)

# dots in row gaps: dark gray dots row1 (y 95..130), strict
def is_dotgray(p):
    r, g, b = p
    return abs(r - g) < 30 and abs(g - b) < 30 and 70 < r < 160

out["row1_dots"] = runs_of([x for x in range(600, 760)
                            if sum(1 for y in range(95, 135) if is_dotgray(px[x, y])) >= 2], 4)
out["row1_dots_rows"] = [y for y in range(90, 140)
                         if sum(1 for x in range(600, 760) if is_dotgray(px[x, y])) >= 2]

# title: per-column red presence rows 58..84 for word segmentation
out["title_cols"] = runs_of([x for x in range(150, 850)
                             if sum(1 for y in range(58, 85) if is_red(px[x, y])) >= 1], 14)

print(json.dumps(out, indent=1))
