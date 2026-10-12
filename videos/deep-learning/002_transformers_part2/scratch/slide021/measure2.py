#!/usr/bin/env python3
"""measure2 — slide_021.jpg deep per-region measurement.
Refines measure1: chrome subpixel fit + badge cross-check; title split/cap;
diagram box; row1 lane/boxes/dots/labels; arrows per-row width; navy bar;
row3 lane/boxes; brace profile; tan line; yellow/green note boxes; censuses.
"""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_021.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()
out = {}


def is_redish(p):
    r, g, b = p
    return r > 130 and (r - g) > 35 and (r - b) > 35


def is_red(p):
    r, g, b = p
    return r > 120 and (r - g) > 50 and (r - b) > 50


def is_blue(p):
    r, g, b = p
    return b > 110 and (b - r) > 60 and (b - g) > 40


def is_navy(p):
    r, g, b = p
    return b > 90 and b < 190 and r < 70 and g < 70


def is_green(p):
    r, g, b = p
    return g > 100 and (g - r) > 40 and (g - b) > 30


def is_tan(p):
    r, g, b = p
    return 190 < r < 248 and 160 < g < 218 and 110 < b < 180 and (r - b) > 40


# ---------- 1. chrome subpixel ----------
def col_centroid(x0, x1, y0, y1, det):
    cols = [(x, sum(1 for y in range(y0, y1) if det(px[x, y]))) for x in range(x0, x1)]
    tot = sum(n for _, n in cols)
    return (sum(x * n for x, n in cols) / tot, tot) if tot >= 20 else (None, tot)


lc, ltn = col_centroid(45, 75, 150, 450, is_redish)
rc, rtn = col_centroid(885, 915, 150, 450, is_redish)
tp = [(y, sum(1 for x in range(100, 860) if is_redish(px[x, y]))) for y in range(38, 50)]
tc = sum(y * n for y, n in tp) / sum(n for _, n in tp)
bp = [(y, sum(1 for x in range(100, 860) if is_redish(px[x, y]))) for y in range(510, 522)]
bc = sum(y * n for y, n in bp) / sum(n for _, n in bp)
out["chrome"] = {"left": round(lc, 2), "right": round(rc, 2), "top": round(tc, 2), "bottom": round(bc, 2)}
# fit vs slide landmarks 42 / 919 / 45 / 540
sx = (rc - lc) / (919 - 42)
ax = lc - sx * 42
sy = (bc - tc) / (540 - 45)
ay = tc - sy * 45
out["fit"] = {"sx": round(sx, 6), "ax": round(ax, 3), "sy": round(sy, 6), "ay": round(ay, 3)}

# badge: yellow circle bbox in top-right region
def is_badyel(p):
    r, g, b = p
    return r > 220 and g > 210 and b < 190
bpts = [(x, y) for y in range(45, 100) for x in range(840, 920) if is_badyel(px[x, y])]
if bpts:
    bb = [min(p[0] for p in bpts), min(p[1] for p in bpts), max(p[0] for p in bpts), max(p[1] for p in bpts)]
    out["badge_bbox_frame"] = bb
    out["badge_center_frame"] = [(bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2]
    out["badge_center_slide"] = [round(((bb[0] + bb[2]) / 2 - ax) / sx, 1), round(((bb[1] + bb[3]) / 2 - ay) / sy, 1)]

# ---------- helpers ----------
def bbox(det, x0, x1, y0, y1):
    pts = [(x, y) for y in range(y0, min(y1, H)) for x in range(x0, min(x1, W)) if det(px[x, y])]
    if not pts:
        return None
    return [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts), len(pts)]


def col_profile(det, x0, x1, y0, y1, minc=1):
    return [(x, sum(1 for y in range(y0, y1) if det(px[x, y]))) for x in range(x0, x1)]


def row_profile(det, x0, x1, y0, y1, minc=1):
    return [(y, sum(1 for x in range(x0, x1) if det(px[x, y]))) for y in range(y0, y1)]


def runs(profile, minc):
    """contiguous runs where count >= minc"""
    rs, cur = [], None
    for v, n in profile:
        if n >= minc:
            if cur is None:
                cur = [v, v]
            else:
                cur[1] = v
        else:
            if cur:
                rs.append(tuple(cur))
                cur = None
    if cur:
        rs.append(tuple(cur))
    return rs


# ---------- 2. title ----------
out["title_red"] = bbox(is_red, 200, 490, 50, 105)
out["title_blue"] = bbox(is_blue, 480, 720, 50, 105)
# cap-height rows of the blue word (E cap): row profile of blue in x 493..662
out["title_blue_rows"] = runs(row_profile(is_blue, 493, 663, 50, 105), 3)
# the 'P' of Position (red) rows within x 380..430
out["title_P_rows"] = runs(row_profile(is_red, 380, 435, 50, 105), 3)

# ---------- 3. diagram box ----------
brow = row_profile(is_blue, 90, 880, 100, 380, 1)
out["box_border_rows"] = [(y, n) for y, n in brow if n > 500]
bcol = col_profile(is_blue, 60, 920, 115, 360, 1)
out["box_border_cols"] = [(x, n) for x, n in bcol if n > 180]

# ---------- 4. row1 ----------
# lane border (dashed blue) rows in x 175..895
out["row1_lane_rows"] = [(y, n) for y, n in row_profile(is_blue, 175, 895, 120, 200) if n > 100]
out["row1_lane_cols"] = [(x, n) for x, n in col_profile(is_blue, 160, 910, 125, 190) if n >= 12]
# box fill (light periwinkle) column runs at mid-row band
def is_lblue(p):
    r, g, b = p
    return 175 < r < 228 and 190 < g < 238 and b > 228 and (b - g) > 8 and (b - r) > 25
out["row1_fill_cols"] = runs(col_profile(is_lblue, 160, 910, 145, 170), 8)
out["row1_fill_rows"] = runs(row_profile(is_lblue, 190, 220, 125, 195), 8)
# dots: gray-steel colored pixels between x 615..745
def is_dot(p):
    r, g, b = p
    return 90 < r < 200 and 100 < g < 210 and 130 < b < 230 and abs(r - g) < 45 and (b - r) > 15
out["row1_dot_cols"] = runs(col_profile(is_dot, 610, 760, 148, 168), 3)
out["row1_dot_rows"] = runs(row_profile(is_dot, 610, 760, 135, 180), 3)
# sample dot core color
if out["row1_dot_cols"]:
    xs = out["row1_dot_cols"]
    cxm = (xs[0][0] + xs[-1][1]) // 2
out["dot_color_samples"] = [px[x, y] for x, y in [(638, 158), (656, 158), (672, 158), (690, 158), (704, 158)]]

# left labels rows (blue text x 74..168)
out["lab_blue_rows"] = runs(row_profile(is_blue, 74, 168, 120, 195), 2)
out["lab_red_rows"] = runs(row_profile(is_red, 70, 168, 200, 265), 2)
out["lab_blue_cols"] = bbox(is_blue, 70, 170, 125, 195)
out["lab_red_cols"] = bbox(is_red, 70, 170, 200, 265)

# ---------- 5. arrows: per-row red width ----------
def arrow_profile(x0, x1, y0, y1):
    prof = {}
    for y in range(y0, y1):
        xs = [x for x in range(x0, x1) if is_red(px[x, y])]
        if xs:
            prof[y] = [min(xs), max(xs), len(xs)]
    return prof
out["arrow1_profile"] = arrow_profile(490, 560, 172, 220)
out["arrow2_profile"] = arrow_profile(490, 560, 255, 300)

# ---------- 6. navy bar ----------
out["navy_rows"] = [(y, n) for y, n in row_profile(is_navy, 100, 900, 195, 270) if n > 300]
out["navy_cols"] = runs(col_profile(is_navy, 100, 910, 220, 245), 100)
# yellow text inside bar
def is_yel(p):
    r, g, b = p
    return r > 200 and g > 170 and b < 120
out["navy_yel"] = bbox(is_yel, 170, 880, 215, 252)
out["navy_yel_rows"] = runs(row_profile(is_yel, 280, 380, 210, 255), 2)
# white text inside bar
def is_white(p):
    r, g, b = p
    return r > 235 and g > 235 and b > 235
out["navy_white"] = bbox(is_white, 385, 880, 218, 248)
out["navy_white_rows"] = runs(row_profile(is_white, 385, 880, 210, 255), 2)

# ---------- 7. row3 ----------
out["row3_lane_rows"] = [(y, n) for y, n in row_profile(is_green, 175, 895, 270, 345) if n > 60]
out["row3_lane_cols"] = [(x, n) for x, n in col_profile(is_green, 160, 910, 280, 335) if n >= 8]
def is_lgreen(p):
    r, g, b = p
    return 190 < r < 240 and 215 < g < 252 and 190 < b < 242 and (g - r) > 8 and (g - b) > 6
out["row3_fill_cols"] = runs(col_profile(is_lgreen, 160, 910, 295, 320), 8)
out["row3_fill_rows"] = runs(row_profile(is_lgreen, 180, 215, 275, 345), 8)

# ---------- 8. brace ----------
out["brace_rows"] = [(y, n) for y, n in row_profile(is_red, 150, 900, 330, 370) if n > 5]
out["brace_cols"] = runs(col_profile(is_red, 150, 900, 333, 358), 2)
apex = None
for y in range(330, 370):
    xs = [x for x in range(150, 900) if is_red(px[x, y])]
    if xs:
        apex = (y, min(xs), max(xs), len(xs))
out["brace_apex_last"] = apex

# ---------- 9. tan line ----------
out["tan_all"] = bbox(is_tan, 240, 470, 240, 410)
out["tan_rows"] = [(y, n) for y, n in row_profile(is_tan, 240, 470, 240, 410) if n > 0]
out["tan_cols"] = [(x, n) for x, n in col_profile(is_tan, 240, 470, 240, 410) if n > 0]

# ---------- 10. yellow note box ----------
def is_yfill(p):
    r, g, b = p
    return r > 245 and g > 240 and 200 < b < 240
out["ybox_fill"] = bbox(is_yfill, 40, 300, 360, 510)
out["ybox_border_rows"] = [(y, n) for y, n in row_profile(is_tan, 60, 290, 370, 505) if n > 100]
out["ybox_border_cols"] = [(x, n) for x, n in col_profile(is_tan, 60, 290, 380, 500) if n > 40]
# text lines inside yellow box: blue + red census
out["ybox_blue_rows"] = runs(row_profile(is_blue, 80, 265, 385, 500), 2)
out["ybox_red_rows"] = runs(row_profile(is_red, 80, 265, 385, 500), 1)
out["ybox_red_cols"] = bbox(is_red, 78, 265, 390, 500)
out["ybox_blue_cols"] = bbox(is_blue, 78, 265, 390, 500)

# ---------- 11. green note box ----------
out["gbox_border_rows"] = [(y, n) for y, n in row_profile(is_green, 300, 780, 360, 505) if n > 150]
out["gbox_border_cols"] = [(x, n) for x, n in col_profile(is_green, 300, 790, 370, 495) if n > 40]
def is_black(p):
    r, g, b = p
    return sum(p) < 220
out["gbox_black_rows"] = runs(row_profile(is_black, 320, 760, 370, 500), 2)
out["gbox_black_cols"] = bbox(is_black, 320, 760, 370, 500)

# ---------- 12. color censuses ----------
def census(det, x0, x1, y0, y1, label):
    pts = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if det(px[x, y])]
    if not pts:
        out[label] = None
        return
    n = len(pts)
    rm = sum(px[x, y][0] for x, y in pts) / n
    gm = sum(px[x, y][1] for x, y in pts) / n
    bm = sum(px[x, y][2] for x, y in pts) / n
    out[label] = {"n": n, "avg": [round(rm), round(gm), round(bm)],
                  "hex": "%02X%02X%02X" % (round(rm), round(gm), round(bm))}

census(is_red, 273, 478, 60, 96, "c_title_red")
census(is_blue, 493, 663, 60, 96, "c_title_blue")
census(is_blue, 175, 890, 133, 137, "c_row1_lane_dash")
census(is_lblue, 200, 260, 145, 170, "c_row1_box_fill")
census(is_blue, 200, 240, 148, 165, "c_row1_digit")
census(is_navy, 200, 800, 222, 245, "c_navy")
census(is_yel, 286, 374, 224, 243, "c_navy_yellow")
census(is_white, 400, 860, 224, 243, "c_navy_white")
census(is_green, 175, 890, 283, 287, "c_row3_lane_dash")
census(is_lgreen, 180, 240, 295, 320, "c_row3_box_fill")
census(is_red, 300, 340, 295, 320, "c_row3_subscript")
census(lambda p: is_blue(p) and p[2] > 120, 180, 240, 295, 320, "c_row3_vector_blue")
census(is_red, 176, 866, 333, 358, "c_brace")
census(is_tan, 250, 340, 300, 390, "c_tan_line")
census(is_yfill, 100, 250, 390, 490, "c_ybox_fill")
census(is_tan, 70, 270, 384, 388, "c_ybox_border")
census(is_blue, 84, 242, 395, 480, "c_ybox_blue")
census(is_green, 314, 760, 372, 376, "c_gbox_border")
census(is_black, 340, 733, 378, 465, "c_gbox_black")

print(json.dumps(out, indent=1, default=str))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide021/measure2_output.txt", "w") as f:
    f.write(json.dumps(out, indent=1, default=str))
