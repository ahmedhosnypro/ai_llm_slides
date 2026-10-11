#!/usr/bin/env python3
"""Phase 1: chrome landmarks + frame->slide mapping fit for slide_020.jpg (960x540)."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_020.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()
out = {"size": [W, H]}

def is_red(p):
    r, g, b = p
    return r > 120 and (r - g) > 50 and (r - b) > 50

# --- vertical red border columns: scan columns with many red px near left/right edges
col_red = []
for x in range(30, 110):
    n = sum(1 for y in range(60, 500) if is_red(px[x, y]))
    col_red.append((x, n))
left_border = max((x for x, n in col_red if x < 90), key=lambda x: col_red[[c for c, _ in col_red].index(x)][1])
col_red_r = [(x, sum(1 for y in range(60, 500) if is_red(px[x, y]))) for x in range(870, 940)]
right_border = max(col_red_r, key=lambda t: t[1])[0]
# horizontal red border rows near top
row_red = [(y, sum(1 for x in range(100, 860) if is_red(px[x, y]))) for y in range(25, 70)]
top_border = max(row_red, key=lambda t: t[1])[0]
out["borders_frame"] = {"left": left_border, "right": right_border, "top": top_border}

# --- black letterbox: rows at bottom that are almost black across
black_rows = [y for y in range(480, H) if sum(1 for x in range(200, 760) if sum(px[x, y]) < 120) > 500]
out["letterbox_rows"] = (min(black_rows), max(black_rows)) if black_rows else None
# red bottom stroke of panel (just above letterbox?)
bottom_red = [(y, sum(1 for x in range(200, 760) if is_red(px[x, y]))) for y in range(495, 530)]
out["bottom_red_profile"] = [(y, n) for y, n in bottom_red if n > 100]

# --- badge: yellow fill bbox in x 840..910, y 40..105
def is_yellowish(p):
    r, g, b = p
    return r > 225 and g > 225 and 120 < b < 215
ypts = [(x, y) for y in range(40, 110) for x in range(835, 915) if is_yellowish(px[x, y])]
if ypts:
    bx0, by0 = min(p[0] for p in ypts), min(p[1] for p in ypts)
    bx1, by1 = max(p[0] for p in ypts), max(p[1] for p in ypts)
    out["badge_yellow_bbox"] = [bx0, by0, bx1, by1]
    out["badge_center"] = [(bx0 + bx1) / 2, (by0 + by1) / 2]

# --- fit mapping from borders (panel left 42, right 919, top 45, bottom 540 in slide pts)
lm = out["borders_frame"]
candidates = []
SH1 = (lm["right"] - lm["left"]) / (919 - 42)
SV1 = ((min(black_rows) - 1) - top_border) / (540 - 45) if black_rows else None
out["fit_SH"], out["fit_SV"] = SH1, SV1
DH = lm["left"] - SH1 * 42
out["fit_DH"] = DH
def to_slide(fx, fy):
    return ((fx - DH) / SH1, fy / SV1)

# cross-check badge
if ypts:
    scx, scy = to_slide(out["badge_center"][0], out["badge_center"][1])
    out["badge_center_slide"] = [round(scx, 1), round(scy, 1)]
    out["badge_delta_vs_house"] = [round(scx - 893, 1), round(scy - 71, 1)]

# --- title ink: red bold text near top (y 10..80), x between borders
tpts = [(x, y) for y in range(5, 80) for x in range(200, 800) if is_red(px[x, y])]
if tpts:
    tx0, ty0 = min(p[0] for p in tpts), min(p[1] for p in tpts)
    tx1, ty1 = max(p[0] for p in tpts), max(p[1] for p in tpts)
    out["title_ink_frame"] = [tx0, ty0, tx1, ty1]
    sx0, sy0 = to_slide(tx0, ty0); sx1, sy1 = to_slide(tx1, ty1)
    out["title_ink_slide"] = [round(sx0, 1), round(sy0, 1), round(sx1, 1), round(sy1, 1)]
    out["title_ink_slide_w"] = round(sx1 - sx0, 1)

print(json.dumps(out, indent=1))
