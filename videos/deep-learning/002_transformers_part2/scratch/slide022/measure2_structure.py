#!/usr/bin/env python3
"""measure2 — slide 022 structure: diagram panel, 3 rows (lanes/boxes/dots/arrows),
bottom cyan panel, title/subtitle, left labels. Frame: slide_022.jpg (960x540)."""
import json
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg"
img = Image.open(FR).convert("RGB")
A = np.asarray(img).astype(int)
H, W = A.shape[:2]
out = {"size": [W, H]}

def bbox(mask, x0, y0):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return [x0 + int(xs.min()), y0 + int(ys.min()), x0 + int(xs.max()), y0 + int(ys.max()), int(mask.sum())]

def colruns(mask, x0, minpix, minw=1):
    colc = mask.sum(axis=0)
    runs = []
    inrun = False
    for i in range(len(colc) + 1):
        on = i < len(colc) and colc[i] >= minpix
        if on and not inrun:
            s = i; inrun = True
        elif not on and inrun:
            if i - s >= minw:
                runs.append([x0 + s, x0 + i - 1])
            inrun = False
    return runs

def rowruns(mask, y0, minpix, minw=1):
    rc = mask.sum(axis=1)
    runs = []
    inrun = False
    for i in range(len(rc) + 1):
        on = i < len(rc) and rc[i] >= minpix
        if on and not inrun:
            s = i; inrun = True
        elif not on and inrun:
            if i - s >= minw:
                runs.append([y0 + s, y0 + i - 1])
            inrun = False
    return runs

def mode_hex(x0, x1, y0, y1):
    sub = A[y0:y1, x0:x1].reshape(-1, 3)
    q = (sub // 8 * 8)
    vals, counts = np.unique(q, axis=0, return_counts=True)
    o = counts.argsort()[::-1][:5]
    return [["%02X%02X%02X" % tuple(vals[i]), int(counts[i])] for i in o]

r, g, b = A[..., 0], A[..., 1], A[..., 2]
red_m = (r > 120) & (r - g > 55) & (r - b > 45)
blue_m = (b - r > 50) & (b - g > 35) & (b > 100)
gray_m = (abs(r - g) < 18) & (abs(g - b) < 18) & (r > 90) & (r < 180)

# 1. title / subtitle ------------------------------------------------------
out["title_red_ink"] = bbox(red_m[45:80, 200:760], 200, 45)
out["subtitle_blue_ink"] = bbox(blue_m[78:105, 200:760], 200, 78)
# underline row under "Word Index"
out["subtitle_rowprof"] = [[78 + y, int(blue_m[78 + y, 200:760].sum())] for y in range(27)]

# 2. diagram panel (thin blue border, white fill) ---------------------------
# search y 100..360
sub_blue = blue_m[100:360, 40:930]
out["dbox_border_rows"] = rowruns(sub_blue, 100, 300, 1)
out["dbox_border_cols"] = colruns(sub_blue, 40, 120, 1)

# 3. ROW bands: find lane containers. Row1 y~110-165, row2 y~180-235, row3 y~255-315
# lane1: dashed dark border + pale-yellow fill; boxes cream with red borders
fill1_m = (r > 235) & (g > 235) & (b > 190) & (b < 235) & (r - b > 12)
out["row1_fill_rows"] = rowruns(fill1_m[100:175, 150:900], 100, 100, 2)
out["row1_fill_colruns"] = colruns(fill1_m[100:175, 150:900], 150, 10, 3)
out["row1_gap_mode"] = mode_hex(620, 720, 115, 160)
out["row1_box_sample"] = mode_hex(190, 230, 120, 150)
# row1 box borders (red): vertical red strokes in band
sub = red_m[105:170, 160:900]
out["row1_red_colruns"] = colruns(sub, 160, 12, 1)
out["row1_red_rowruns"] = rowruns(sub, 105, 30, 1)

# 4. ROW2 --------------------------------------------------------------------
# light-blue fill lane + blue boxes
fill2_m = (b - r > 25) & (b > 200) & (r > 170) & (r < 235)
out["row2_fill_rows"] = rowruns(fill2_m[175:245, 150:900], 175, 100, 2)
out["row2_fill_colruns"] = colruns(fill2_m[175:245, 150:900], 150, 10, 3)
out["row2_gap_mode"] = mode_hex(620, 720, 185, 235)
out["row2_box_sample"] = mode_hex(190, 230, 190, 220)
sub = blue_m[175:245, 160:900]
out["row2_blue_colruns"] = colruns(sub, 160, 12, 1)
out["row2_blue_rowruns"] = rowruns(sub, 175, 30, 1)

# 5. ROW3 --------------------------------------------------------------------
# pink lane fill + cream boxes with red borders
fill3_m = (r > 230) & (r - g > 12) & (r - b > 20) & (g > 150)
out["row3_fill_rows"] = rowruns(fill3_m[250:320, 150:900], 250, 100, 2)
out["row3_fill_colruns"] = colruns(fill3_m[250:320, 150:900], 150, 10, 3)
out["row3_gap_mode"] = mode_hex(620, 720, 260, 310)
out["row3_box_sample"] = mode_hex(190, 230, 265, 295)
sub = red_m[250:320, 160:900]
out["row3_red_colruns"] = colruns(sub, 160, 12, 1)
out["row3_red_rowruns"] = rowruns(sub, 250, 30, 1)

# 6. arrows + +δ (orange) ----------------------------------------------------
orange_m = (r > 180) & (r - b > 80) & (g > 80) & (g < 190) & (b < 120)
out["orange_rows"] = rowruns(orange_m[255:345, 150:900], 255, 4, 1)
out["orange_colruns_band_arrows"] = colruns(orange_m[290:318, 150:900], 150, 3, 1)
out["orange_colruns_band_delta"] = colruns(orange_m[315:340, 150:900], 150, 3, 1)
out["orange_trace"] = {}
for y in range(280, 345):
    xs = np.where(orange_m[y, 150:900])[0]
    if len(xs):
        out["orange_trace"][y] = [150 + int(xs.min()), 150 + int(xs.max()), len(xs)]

# 7. dots (rows 1 and 2) ------------------------------------------------------
# gray dots row1
sub = gray_m[110:170, 615:725]
out["dots1_colruns"] = colruns(sub, 615, 2, 1)
out["dots1_rowruns"] = rowruns(sub, 110, 2, 1)
# blue dots row2
sub = blue_m[180:240, 615:725]
out["dots2_colruns"] = colruns(sub, 615, 2, 1)
out["dots2_rowruns"] = rowruns(sub, 180, 2, 1)

# 8. bottom cyan panel --------------------------------------------------------
cyan_m = (b > 200) & (b - r > 15) & (g > 200) & (abs(g - b) < 40) & (r < 235)
out["cyan_fill_rows"] = rowruns(cyan_m[340:540, 40:930], 340, 200, 2)
out["cyan_fill_cols"] = colruns(cyan_m[340:540, 40:930], 40, 100, 2)
out["cyan_sample"] = mode_hex(100, 300, 400, 420)
# panel border (blue) rows
sub = blue_m[340:540, 40:930]
out["cyan_border_rows"] = rowruns(sub, 340, 300, 1)
out["cyan_border_cols"] = colruns(sub, 40, 200, 1)

# 9. bottom panel text rows (dark inks) ---------------------------------------
dark_m = (r < 130) & (g < 130) & (b < 200)
sub = dark_m[350:520, 60:930]
out["panel_text_rowruns"] = rowruns(sub, 350, 6, 1)
red2_m = (r > 120) & (r - g > 60) & (r - b > 60)
out["panel_red_ink"] = bbox(red2_m[350:520, 60:930], 60, 350)
out["panel_blue_ink"] = bbox(blue_m[350:520, 60:930], 60, 350)
out["panel_black_ink"] = bbox((r < 90) & (g < 90) & (b < 90)[350:520, 60:930] if False else (A[350:520, 60:930].sum(axis=2) < 270), 60, 350)

# 10. left labels --------------------------------------------------------------
out["lab1_gray_ink"] = bbox(gray_m[105:170, 60:170], 60, 105)
out["lab2_blue_ink"] = bbox(blue_m[175:245, 60:170], 60, 175)
out["lab3_red_ink"] = bbox(red_m[250:320, 60:170], 60, 250)
out["lab1_gray_rows"] = rowruns(gray_m[105:170, 60:170], 105, 2, 1)
out["lab2_blue_rows"] = rowruns(blue_m[175:245, 60:170], 175, 2, 1)
out["lab3_red_rows"] = rowruns(red_m[250:320, 60:170], 250, 2, 1)

# 11. badge --------------------------------------------------------------------
yellow_m = (r > 200) & (g > 200) & (b < 140)
ys, xs = np.where(yellow_m)
m = (xs > 840) & (ys < 120)
out["badge_bbox"] = [int(xs[m].min()), int(ys[m].min()), int(xs[m].max()), int(ys[m].max())] if m.any() else None

# 12. mouse cursor zone (row3 right, ~x 830-870, y 285-310) — artifact check
out["cursor_sample"] = mode_hex(835, 875, 280, 315)

# 13. global color census samples ----------------------------------------------
out["mode_full"] = mode_hex(0, 960, 0, 540)
out["mode_row3_arrows_zone"] = mode_hex(240, 420, 295, 335)

print(json.dumps(out, indent=1))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide022/measure2_output.txt", "w") as f:
    f.write(json.dumps(out, indent=1))
