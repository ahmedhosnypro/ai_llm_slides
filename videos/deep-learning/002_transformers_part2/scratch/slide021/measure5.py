#!/usr/bin/env python3
"""measure5 — slide 021 fine pass: clean windows, core-color census, exact boxes."""
import json
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_021.jpg"
img = Image.open(FR).convert("RGB")
A = np.asarray(img).astype(int)
out = {}

def census(x0, x1, y0, y1, mask_fn, q=4, topn=3):
    sub = A[y0:y1, x0:x1].reshape(-1, 3)
    m = mask_fn(sub)
    sel = sub[m]
    if len(sel) == 0:
        return None
    qq = sel // q * q
    vals, counts = np.unique(qq, axis=0, return_counts=True)
    o = counts.argsort()[::-1][:topn]
    return {"n": int(m.sum()), "modes": [["%02X%02X%02X" % tuple(v), int(c)] for v, c in zip(vals[o], counts[o])]}

def rowprof(x0, x1, y0, y1, mask_fn, minc=2):
    sub = A[y0:y1, x0:x1]
    m = mask_fn(sub)
    return [[y0 + int(y), int(m[y].sum())] for y in range(sub.shape[0]) if m[y].sum() >= minc]

def colruns(x0, x1, y0, y1, mask_fn, minc=3, mingap=2):
    sub = A[y0:y1, x0:x1]
    m = mask_fn(sub)
    cc = m.sum(axis=0)
    runs, inrun, s, gap = [], False, 0, 0
    for i in range(len(cc)):
        if cc[i] >= minc:
            if not inrun:
                s, inrun = i, True
            gap = 0
        elif inrun:
            gap += 1
            if gap > mingap:
                runs.append([x0 + s, x0 + i - gap]); inrun = False
    if inrun:
        runs.append([x0 + s, x0 + len(cc) - 1])
    return runs

# filters
f_red   = lambda p: (p[..., 0] > 120) & (p[..., 0] - p[..., 1] > 60) & (p[..., 0] - p[..., 2] > 50)
f_redloose = lambda p: (p[..., 0] > 110) & (p[..., 0] - p[..., 1] > 40) & (p[..., 0] - p[..., 2] > 30)
f_blue  = lambda p: (p[..., 2] - p[..., 0] > 50) & (p[..., 2] > 110) & (p[..., 0] < 160)
f_blueany = lambda p: (p[..., 2] - p[..., 0] > 25) & (p[..., 2] > 120)
f_green = lambda p: (p[..., 1] - p[..., 0] > 25) & (p[..., 1] - p[..., 2] > 15) & (p[..., 1] > 100) & (p[..., 1] < 215)
f_darkblue = lambda p: (p[..., 2] - p[..., 0] > 40) & (p[..., 2] > 90) & (p[..., 0] < 120)
f_tan   = lambda p: (p[..., 0] > 170) & (p[..., 0] - p[..., 2] > 25) & (p[..., 1] - p[..., 2] > 10) & (p[..., 2] > 110) & (p[..., 2] < 205)
f_yellow= lambda p: (p[..., 0] > 185) & (p[..., 1] > 185) & (p[..., 2] < 150)
f_white = lambda p: (p[..., 0] > 195) & (p[..., 1] > 195) & (p[..., 2] > 195)
f_black = lambda p: (p[..., 0] < 90) & (p[..., 1] < 90) & (p[..., 2] < 90)

# 1. chrome right stroke, clean band
sub = A[380:480, 885:915]
m = f_red(sub)
cols = np.where(m.sum(axis=0) > 10)[0]
out["chrome_right_cols"] = [[885 + int(c), int(m[:, c].sum())] for c in cols]
sub = A[380:480, 45:75]
m = f_red(sub)
cols = np.where(m.sum(axis=0) > 10)[0]
out["chrome_left_cols"] = [[45 + int(c), int(m[:, c].sum())] for c in cols]

# 2. title P cap rows (P run x 332-352)
out["title_P_rows"] = rowprof(332, 353, 55, 100, f_red, 2)
out["title_E_rows"] = rowprof(493, 515, 55, 100, f_blue, 2)  # E of Encoding
out["title_red_core"] = census(332, 477, 60, 90, f_red)
out["title_blue_core"] = census(493, 662, 60, 90, f_blue)

# 3. labels, clean window x 70..160
out["lab_blue_rows"] = rowprof(70, 160, 128, 185, f_blue, 2)
out["lab_blue_ink_cols"] = colruns(60, 163, 130, 180, f_blue, 2)
out["lab_red_rows"] = rowprof(70, 160, 210, 258, f_red, 2)
out["lab_red_ink_cols"] = colruns(60, 163, 212, 255, f_red, 2)
out["lab_blue_core"] = census(70, 160, 135, 172, f_blue)
out["lab_red_core"] = census(70, 160, 215, 250, f_red)

# 4. row1 fine ------------------------------------------------------------
# box border rows: strong blue over box1 x 180..234
out["r1_box1_border_rows"] = rowprof(180, 234, 130, 180, f_blue, 8)
# box border cols: strong blue over y 146..163
out["r1_border_cols"] = colruns(160, 890, 146, 163, f_blue, 6, 1)
# digit ink: dark blue in box1
out["r1_digit0"] = rowprof(185, 230, 146, 164, f_darkblue, 2)
out["r1_digit0_cols"] = colruns(180, 234, 148, 163, f_darkblue, 1, 1)
# dots: window
out["r1_dots_cols"] = colruns(622, 718, 149, 164, f_blueany, 2, 2)
out["r1_dots_rows"] = rowprof(630, 712, 146, 168, f_blueany, 2)
out["r1_dot_core"] = census(630, 712, 150, 162, f_blueany)
# colors
out["r1_lane_fill"] = census(620, 720, 138, 172, lambda p: (p[..., 2] - p[..., 0] > 10), q=4)
out["r1_box_fill"] = census(190, 225, 150, 160, lambda p: (p[..., 2] - p[..., 0] > 10) & (p[..., 1] - p[..., 0] > 5), q=4)
out["r1_dash_core"] = census(300, 800, 135, 139, f_blue, 4)
out["r1_border_core"] = census(160, 890, 143, 147, f_blue, 4)
out["r1_digit_core"] = census(185, 230, 148, 163, f_darkblue, 4)
# lane extents: dash rows full profile
out["r1_dash_top"] = colruns(150, 900, 135, 139, f_blue, 2, 12)
out["r1_dash_bot"] = colruns(150, 900, 172, 177, f_blue, 2, 12)
out["r1_fill_rowprof"] = rowprof(620, 720, 130, 182, lambda p: (p[..., 2] - p[..., 0] > 10) & (p[..., 2] > 200), 20)

# 5. row3 fine ------------------------------------------------------------
out["r3_border_cols"] = colruns(160, 900, 294, 323, f_green, 5, 1)
out["r3_border_rows_box1"] = rowprof(180, 230, 282, 336, f_green, 5)
out["r3_box1_fill_rows"] = rowprof(185, 225, 285, 334, lambda p: (p[..., 1] - p[..., 0] > 5) & (p[..., 1] > 215) & (p[..., 2] > 190) & (p[..., 0] < 240), 15)
out["r3_vector_ink_rows"] = rowprof(180, 235, 288, 330, f_darkblue, 2)
out["r3_vector_ink_cols"] = colruns(172, 240, 292, 326, f_darkblue, 1, 1)
out["r3_sub_rows"] = rowprof(180, 240, 288, 330, f_redloose, 2)
out["r3_lane_fill"] = census(612, 640, 296, 322, lambda p: (p[..., 1] - p[..., 0] > 3), q=4)
out["r3_box_fill"] = census(190, 220, 310, 318, lambda p: (p[..., 1] - p[..., 0] > 3), q=4)
out["r3_dash_core"] = census(300, 800, 289, 293, f_green, 4)
out["r3_border_core"] = census(160, 900, 294, 323, f_green, 4)
out["r3_vector_core"] = census(175, 700, 292, 326, f_darkblue, 4)
out["r3_sub_core"] = census(175, 700, 300, 324, f_redloose, 4)
out["r3_dash_top"] = colruns(150, 900, 289, 293, f_green, 2, 12)
out["r3_dash_bot"] = colruns(150, 900, 325, 330, f_green, 2, 12)

# 6. navy text re-census (restrict to bar interior y 217..250)
out["navy_yellow"] = census(280, 380, 217, 250, f_yellow, 4)
out["navy_yellow_ink2"] = rowprof(280, 380, 216, 251, f_yellow, 2)
out["navy_yellow_cols"] = colruns(275, 385, 224, 244, f_yellow, 1, 2)
out["navy_white_ink2"] = rowprof(380, 780, 216, 251, f_white, 2)
out["navy_white_cols"] = colruns(378, 790, 226, 246, f_white, 1, 2)
out["navy_core"] = census(200, 800, 220, 248, lambda p: (p[..., 2] > 100) & (p[..., 0] < 70), 4)
out["navy_white_core"] = census(380, 780, 226, 246, f_white, 4)
out["navy_bar_edge_rows"] = rowprof(400, 500, 208, 260, lambda p: (p[..., 2] > 100) & (p[..., 0] < 70), 60)
out["navy_bar_edge_cols"] = colruns(155, 900, 218, 248, lambda p: (p[..., 2] > 100) & (p[..., 0] < 70), 60, 4)

# 7. tan line focused trace (exclude ybox border y>=379 & x<=270)
out["tan_trace2"] = {}
sub = A[250:382, 240:345]
m = f_tan(sub)
for y in range(sub.shape[0]):
    xs = np.where(m[y])[0]
    if len(xs) >= 1:
        out["tan_trace2"][250 + y] = [240 + int(xs.min()), 240 + int(xs.max()), len(xs)]
out["tan_core"] = census(240, 345, 250, 382, f_tan, 4)

# 8. ybox / gbox text fine
out["ybox_L2_rows"] = rowprof(80, 215, 412, 430, f_blue, 2)
out["ybox_L4_rows"] = rowprof(80, 248, 464, 482, f_blue, 2)
out["ybox_blue_core"] = census(80, 250, 395, 480, f_blue, 4)
out["ybox_fill_core"] = census(100, 240, 430, 445, lambda p: (p[..., 0] > 230) & (p[..., 2] > 180) & (p[..., 0] - p[..., 2] > 10), 4)
out["ybox_border_core"] = census(74, 268, 379, 384, f_tan, 4)
out["gbox_R_rows"] = rowprof(340, 356, 378, 400, f_black, 1)
out["gbox_L1_cols"] = colruns(330, 740, 382, 396, f_black, 1, 3)
out["gbox_L2_cols"] = colruns(330, 740, 404, 418, f_black, 1, 3)
out["gbox_L3_cols"] = colruns(330, 740, 447, 461, f_black, 1, 3)
out["gbox_border_core"] = census(314, 762, 370, 374, f_green, 4)

# 9. dbox border color + fill
out["dbox_border_core"] = census(200, 800, 110, 113, f_blue, 4)
out["dbox_fill"] = census(100, 150, 268, 286, lambda p: (p[..., 0] > 200), 4)

# 10. arrows re-verify
out["arr1_prof"] = rowprof(512, 534, 170, 220, f_red, 2)
out["arr2_prof"] = rowprof(512, 534, 250, 296, f_red, 2)

# 11. brace core color
out["brace_core"] = census(180, 860, 338, 348, f_red, 4)

# 12. right-edge marks check x 884..899
sub = A[125:340, 884:900]
m = f_redloose(sub)
out["right_marks"] = int(m.sum())

with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide021/measure5_output.txt", "w") as f:
    f.write(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
