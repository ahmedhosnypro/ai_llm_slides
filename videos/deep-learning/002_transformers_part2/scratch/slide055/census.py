#!/usr/bin/env python3
"""Slide 055 component census: color-region detection for all diagram elements.
Frame 960x540, 1px = 1pt. Mapping (identical to certified 054 fit): X0=18.63 SX=0.96123 SY=0.95556.
"""
from PIL import Image
import json
from collections import Counter

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()

def near(p, c, tol=28):
    return all(abs(p[i] - c[i]) <= tol for i in range(3))

def bbox_of(pred, x0, y0, x1, y1, step=1):
    xs, ys = [], []
    for y in range(y0, y1, step):
        for x in range(x0, x1, step):
            if pred(px[x, y]):
                xs.append(x); ys.append(y)
    if not xs:
        return None
    return [min(xs), min(ys), max(xs), max(ys), len(xs)]

out = {}

# ---- main peach panel (FCE5C6-ish) ----
out["peach_panel"] = bbox_of(lambda p: near(p, (252, 229, 198), 22), 20, 60, 940, 530, 2)

# ---- title ink (dark pixels y 50..95, x 60..850) ----
def dark(p):
    return sum(p) < 250
out["title_L1"] = bbox_of(dark, 60, 48, 850, 72)
out["title_L2"] = bbox_of(dark, 60, 72, 850, 96)

# ---- red ink census across the slide (for labels/arrows) ----
def redish(p):
    r, g, b = p
    return r > 150 and g < 90 and b < 90 and (r - max(g, b)) > 80
# red ink rows histogram (coarse)
red_rows = {}
for y in range(40, 540, 4):
    cnt = sum(1 for x in range(0, W, 2) if redish(px[x, y]))
    if cnt > 3:
        red_rows[y] = cnt
out["red_row_profile"] = red_rows

# ---- yellow regions (containers/pills/badge) ----
def yellowish(p):
    r, g, b = p
    return r > 210 and g > 200 and b < 170
yellow_boxes = []
# scan for yellow clusters in the body (y>100), crude connected columns
ys_hits = {}
for y in range(100, 540, 2):
    row = [x for x in range(20, 940, 2) if yellowish(px[x, y])]
    if row:
        ys_hits[y] = (min(row), max(row), len(row))
out["yellow_rows"] = {str(k): v for k, v in list(ys_hits.items())[::3]}

# ---- blue dots in dot-product box (navy 1B1F95-ish) ----
def navyish(p):
    r, g, b = p
    return b > 100 and r < 90 and g < 90 and (b - r) > 60
out["navy_dots_zone"] = bbox_of(navyish, 260, 180, 360, 400)
# dot cluster detection: rows of navy in x 270..350
dot_rows = {}
for y in range(180, 400):
    xs = [x for x in range(270, 360) if navyish(px[x, y])]
    if len(xs) >= 2:
        dot_rows[y] = (min(xs), max(xs), len(xs))
out["navy_dot_rows"] = dot_rows

# ---- left yellow container region ----
out["left_yellow_container"] = bbox_of(yellowish, 60, 200, 200, 420, 1)
out["right_yellow_container"] = bbox_of(yellowish, 740, 200, 900, 420, 1)

# ---- green boxes W_k (00CC00-ish bright green) ----
def bright_green(p):
    r, g, b = p
    return g > 150 and r < 140 and b < 140 and (g - r) > 40 and (g - b) > 40
out["left_Wk_boxes"] = bbox_of(bright_green, 150, 200, 260, 420)
out["right_Wk_boxes"] = bbox_of(bright_green, 690, 200, 780, 420)
out["O_box"] = bbox_of(bright_green, 520, 100, 680, 160)

# ---- blue W_v boxes (0033CC-ish / light blue fill w/ blue border) ----
def blueish(p):
    r, g, b = p
    return b > 150 and b - r > 60 and b - g > 40
out["Wv_blue_boxes"] = bbox_of(blueish, 690, 200, 780, 420)

# ---- pink scaling column (FF9C9C-ish) ----
def pinkish(p):
    r, g, b = p
    return r > 230 and 130 < g < 190 and 130 < b < 190
out["scaling_col"] = bbox_of(pinkish, 380, 180, 460, 420)
# ---- violet softmax column (CC99FF-ish) ----
def violetish(p):
    r, g, b = p
    return 180 < r < 230 and 130 < g < 180 and b > 220
out["softmax_col"] = bbox_of(violetish, 470, 180, 545, 420)

# ---- tan dot-product box (A99E8C-ish) ----
def tanish(p):
    r, g, b = p
    return 150 < r < 190 and 140 < g < 175 and 120 < b < 155 and r > g > b
out["dotprod_box"] = bbox_of(tanish, 280, 170, 380, 420)

# ---- sigma box (BFDCEF light blue) ----
def sigmablue(p):
    r, g, b = p
    return 180 < r < 210 and 215 < g < 235 and b > 235
out["sigma_box"] = bbox_of(sigmablue, 500, 170, 700, 230)

# ---- Z-row pink container (FF99CC-ish deeper pink) ----
def zpink(p):
    r, g, b = p
    return r > 240 and 120 < g < 180 and 170 < b < 215
out["zrow_container"] = bbox_of(zpink, 180, 440, 540, 520)
# ---- decoder caption magenta text ----
def magentaish(p):
    r, g, b = p
    return r > 170 and b > 170 and g < 120
out["decoder_caption"] = bbox_of(magentaish, 500, 440, 730, 510)

# ---- legend pale-green box (CCFFCC-ish) ----
def palegreen(p):
    r, g, b = p
    return 180 < r < 230 and g > 230 and 180 < b < 230
out["legend_box"] = bbox_of(palegreen, 700, 410, 920, 510)

# ---- bottom letterbox (omit as artifact): dark rows near bottom ----
out["letterbox_rows"] = [y for y in range(515, 540) if sum(1 for x in range(0, W, 4) if sum(px[x, y]) < 150) > 100]

print(json.dumps(out, indent=1))
