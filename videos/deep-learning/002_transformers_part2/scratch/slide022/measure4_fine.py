#!/usr/bin/env python3
"""measure4 — slide 022 fine measurement: box edges per row, dots, arrows, +delta,
color census, bottom-panel text bands, labels, title, right-edge check."""
import json
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg"
img = Image.open(FR).convert("RGB")
A = np.asarray(img).astype(int)
out = {}

def census(x0, x1, y0, y1, maskfn, topn=6):
    sub = A[y0:y1, x0:x1].reshape(-1, 3)
    m = maskfn(sub)
    sel = sub[m]
    if len(sel) == 0:
        return None
    q = (sel // 4 * 4)
    vals, counts = np.unique(q, axis=0, return_counts=True)
    o = counts.argsort()[::-1][:topn]
    tot = int(m.sum())
    return {"n": tot, "modes": [["%02X%02X%02X" % tuple(vals[i]), int(counts[i])] for i in o]}

R, G, B = A[..., 0], A[..., 1], A[..., 2]

# ---------- 1. color census ----------
out["c_row1_lane_fill"] = census(600, 700, 121, 132, lambda s: (s.sum(axis=1) > 550) & (abs(s[:, 0] - s[:, 2]) < 30) & (s[:, 0] > 180))
out["c_row1_lane_fill2"] = census(700, 860, 150, 156, lambda s: (s.sum(axis=1) > 550) & (s[:, 0] > 180))
out["c_row1_box_fill"] = census(250, 320, 128, 134, lambda s: (s.sum(axis=1) > 560) & (s[:, 0] > 200))
out["c_row1_text"] = census(185, 900, 133, 142, lambda s: (s[:, 0] - s[:, 1] > 60) & (s[:, 0] - s[:, 2] > 55) & (s[:, 0] < 190))
out["c_row1_dash"] = census(160, 900, 117, 120, lambda s: (s.sum(axis=1) < 420) & (abs(s[:, 0] - s[:, 1]) < 25) & (abs(s[:, 1] - s[:, 2]) < 25))
out["c_row1_border"] = census(180, 890, 125, 129, lambda s: (s[:, 0] - s[:, 1] > 20) & (s[:, 0] > 150) & (s[:, 1] > 100))
out["c_row1_dots"] = census(630, 715, 133, 144, lambda s: (s.sum(axis=1) < 560) & (abs(s[:, 0] - s[:, 1]) < 22) & (abs(s[:, 1] - s[:, 2]) < 22))

out["c_row2_lane_fill"] = census(600, 700, 190, 200, lambda s: (s[:, 2] - s[:, 0] > 30) & (s[:, 0] > 150))
out["c_row2_dash"] = census(160, 900, 186, 189, lambda s: (s[:, 2] - s[:, 0] > 30) & (s.sum(axis=1) < 480))
out["c_row2_border"] = census(185, 890, 190, 222, lambda s: (s[:, 2] - s[:, 0] > 45) & (s[:, 2] > 120) & (s[:, 0] < 140))
out["c_row2_text"] = census(190, 880, 195, 213, lambda s: (s[:, 2] - s[:, 0] > 80) & (s[:, 2] > 90) & (s[:, 0] < 90))
out["c_row2_dots"] = census(630, 715, 200, 216, lambda s: (s[:, 2] - s[:, 0] > 25) & (s[:, 0] < 160) & (s[:, 2] < 230))

out["c_row3_lane_fill"] = census(600, 700, 266, 274, lambda s: (s[:, 0] - s[:, 2] > 5) & (s[:, 0] > 230) & (s[:, 1] > 200))
out["c_row3_dash"] = census(160, 900, 261, 264, lambda s: (s[:, 0] - s[:, 1] > 55) & (s[:, 0] < 200))
out["c_row3_border"] = census(180, 890, 276, 280, lambda s: (s[:, 0] - s[:, 1] > 55) & (s[:, 0] < 210))
out["c_row3_box_fill"] = census(250, 320, 283, 288, lambda s: (s[:, 0] > 230) & (s[:, 1] > 220))
out["c_row3_text"] = census(200, 870, 280, 298, lambda s: (s[:, 0] - s[:, 1] > 70) & (s[:, 0] - s[:, 2] > 60) & (s[:, 0] < 170))
out["c_arrows"] = census(265, 850, 293, 306, lambda s: (s[:, 0] - s[:, 2] > 70) & (s[:, 1] > 60) & (s[:, 1] < 190) & (s[:, 0] > 140))
out["c_delta"] = census(215, 810, 315, 329, lambda s: (s[:, 0] - s[:, 2] > 55) & (s[:, 0] > 110) & (s[:, 0] < 220))

out["c_title"] = census(340, 690, 58, 80, lambda s: (s[:, 0] - s[:, 1] > 45) & (s[:, 0] < 200))
out["c_subtitle"] = census(320, 720, 84, 106, lambda s: (s[:, 2] - s[:, 0] > 55) & (s[:, 2] > 90) & (s[:, 0] < 110))
out["c_lab1"] = census(76, 170, 113, 158, lambda s: (abs(s[:, 0] - s[:, 1]) < 20) & (abs(s[:, 1] - s[:, 2]) < 20) & (s.sum(axis=1) < 480))
out["c_lab2"] = census(70, 168, 178, 230, lambda s: (s[:, 2] - s[:, 0] > 55) & (s[:, 2] > 90) & (s[:, 0] < 120))
out["c_lab3"] = census(70, 168, 262, 295, lambda s: (s[:, 0] - s[:, 1] > 55) & (s[:, 0] < 190))
out["c_dbox_border"] = census(64, 894, 111, 113, lambda s: (s[:, 2] - s[:, 0] > 35) & (s.sum(axis=1) < 500))
out["c_cyan_fill"] = census(200, 800, 355, 365, lambda s: (s[:, 2] - s[:, 0] > 8) & (s[:, 1] > 225))
out["c_cyan_border"] = census(64, 894, 348, 351, lambda s: (s[:, 2] - s[:, 0] > 30) & (s.sum(axis=1) < 500))
out["c_panel_text_blue"] = census(70, 900, 365, 495, lambda s: (s[:, 2] - s[:, 0] > 70) & (s[:, 2] > 100) & (s[:, 0] < 100))
out["c_panel_red"] = census(70, 900, 385, 410, lambda s: (s[:, 0] - s[:, 1] > 60) & (s[:, 0] < 190))
out["c_badge_ring"] = census(855, 895, 50, 95, lambda s: (s[:, 2] - s[:, 1] > 30) & (s[:, 2] > 120) & (s[:, 0] < 160))
out["c_badge_fill"] = census(860, 890, 55, 90, lambda s: (s[:, 0] > 220) & (s[:, 1] > 220) & (s[:, 2] < 190))
out["c_dot2"] = census(634, 714, 202, 215, lambda s: (s[:, 2] - s[:, 0] > 20) & (s[:, 2] > 150) & (s[:, 0] < 150))

# ---------- 2. box edges per row ----------
def border_cols(y0, y1, x0, x1, maskfn, minc):
    sub = maskfn(A[y0:y1, x0:x1])
    colc = sub.sum(axis=0)
    cols = [x0 + i for i in range(len(colc)) if colc[i] >= minc]
    # cluster consecutive
    runs = []
    for c in cols:
        if runs and c - runs[-1][1] <= 2:
            runs[-1][1] = c
        else:
            runs.append([c, c])
    return runs

red_strong = lambda s: (s[..., 0] - s[..., 1] > 55) & (s[..., 0] - s[..., 2] > 45) & (s[..., 0] > 110)
blue_strong = lambda s: (s[..., 2] - s[..., 0] > 45) & (s[..., 2] > 110) & (s[..., 0] < 150)
red_soft = lambda s: (s[..., 0] - s[..., 1] > 22) & (s[..., 0] > 140) & (s[..., 1] > 90)

out["row3_vborder_cols"] = border_cols(277, 302, 170, 895, red_strong, 14)
out["row2_vborder_cols"] = border_cols(190, 223, 170, 895, blue_strong, 12)
out["row1_vborder_cols"] = border_cols(126, 148, 170, 895, red_soft, 10)
# box top/bottom border rows
def border_rows(y0, y1, x0, x1, maskfn, minc):
    sub = maskfn(A[y0:y1, x0:x1])
    rc = sub.sum(axis=1)
    return [[y0 + i, int(rc[i])] for i in range(len(rc)) if rc[i] >= minc]
out["row1_hborder_rows"] = border_rows(115, 165, 180, 890, red_soft, 40)
out["row2_hborder_rows"] = border_rows(180, 235, 180, 890, blue_strong, 40)
out["row3_hborder_rows"] = border_rows(255, 310, 180, 890, red_strong, 40)

# ---------- 3. dots fine ----------
def dot_cols(y0, y1, x0, x1, maskfn, minc=2):
    sub = maskfn(A[y0:y1, x0:x1])
    colc = sub.sum(axis=0)
    cols = [x0 + i for i in range(len(colc)) if colc[i] >= minc]
    runs = []
    for c in cols:
        if runs and c - runs[-1][1] <= 3:
            runs[-1][1] = c
        else:
            runs.append([c, c])
    return runs
grayish = lambda s: (abs(s[..., 0] - s[..., 1]) < 22) & (abs(s[..., 1] - s[..., 2]) < 22) & (s.sum(axis=2) < 560) & (s.sum(axis=2) > 150)
out["dots1_runs"] = dot_cols(133, 144, 620, 725, grayish)
# vertical extent of dot 1
sub = grayish(A[125:150, 633:643])
rows = np.where(sub.any(axis=1))[0]
out["dot1_rows"] = [125 + int(rows.min()), 125 + int(rows.max())] if len(rows) else None
bluedot = lambda s: (s[..., 2] - s[..., 0] > 22) & (s[..., 0] < 170) & (s[..., 2] > 140)
out["dots2_runs"] = dot_cols(200, 216, 620, 725, bluedot)
sub = bluedot(A[195:225, 634:644])
rows = np.where(sub.any(axis=1))[0]
out["dot2_rows"] = [195 + int(rows.min()), 195 + int(rows.max())] if len(rows) else None

# ---------- 4. arrows trace ----------
orange = (R > 140) & (R - B > 70) & (G > 55) & (G < 200) & (B < 140)
out["arrow_trace"] = {}
for y in range(288, 310):
    xs = np.where(orange[y, 170:890])[0]
    if len(xs):
        out["arrow_trace"][y] = [170 + int(xs.min()), 170 + int(xs.max()), len(xs)]
# per-arrow bbox: cluster x in band y 290..308
ys, xs = np.where(orange[290:308, 170:890])
clusters = []
if len(xs):
    pts = sorted(zip(xs + 170, ys + 290))
    cur = [pts[0][0], pts[0][0], pts[0][1], pts[0][1]]
    for x, y in pts[1:]:
        if x - cur[1] <= 14:
            cur[1] = max(cur[1], x); cur[2] = min(cur[2], y); cur[3] = max(cur[3], y)
        else:
            clusters.append(cur); cur = [x, x, y, y]
    clusters.append(cur)
out["arrow_bboxes"] = [[int(v) for v in c] for c in clusters]

# ---------- 5. delta ----------
ys, xs = np.where(orange[313:331, 170:890])
clusters = []
if len(xs):
    pts = sorted(zip(xs + 170, ys + 313))
    cur = [pts[0][0], pts[0][0], pts[0][1], pts[0][1]]
    for x, y in pts[1:]:
        if x - cur[1] <= 14:
            cur[1] = max(cur[1], x); cur[2] = min(cur[2], y); cur[3] = max(cur[3], y)
        else:
            clusters.append(cur); cur = [x, x, y, y]
    clusters.append(cur)
out["delta_bboxes"] = [[int(v) for v in c] for c in clusters]

# ---------- 6. bottom panel text bands with column profiles ----------
dark = (A.sum(axis=2) < 420)
for name, (y0, y1) in {"line1": (362, 386), "problems": (386, 405), "b1a": (408, 430), "b1b": (430, 452), "b2": (452, 472), "b3": (474, 494)}.items():
    sub = dark[y0:y1, 60:930]
    cols = np.where(sub.any(axis=0))[0]
    if len(cols):
        out[f"band_{name}"] = {"rows": [y0, y1], "x": [60 + int(cols.min()), 60 + int(cols.max())], "n": int(sub.sum())}
# underline rows in line1 (Depends on Seq. Length): solid-ish row
sub = dark[378:390, 60:930]
prof = sub.sum(axis=1)
out["line1_underline_rows"] = [[378 + i, int(prof[i])] for i in range(len(prof)) if prof[i] > 60]
# red Problems: bbox
redm = (R > 120) & (R - G > 60) & (R - B > 60)
sub = redm[386:406, 60:400]
ys2, xs2 = np.where(sub)
out["problems_bbox"] = [60 + int(xs2.min()), 386 + int(ys2.min()), 60 + int(xs2.max()), 386 + int(ys2.max())] if len(xs2) else None
# bullet dots x (dark round markers ~ x 84?)
sub = dark[408:495, 60:120]
colc = sub.sum(axis=0)
out["bulletdot_cols"] = [[60 + i, int(colc[i])] for i in range(len(colc)) if colc[i] >= 3]

# ---------- 7. labels fine ----------
out["lab1_lines"] = []
sub = (abs(R - G) < 22) & (abs(G - B) < 22) & (A.sum(axis=2) < 480)
for y0, y1 in [(112, 126), (127, 142), (143, 160)]:
    s2 = sub[y0:y1, 70:172]
    ys3, xs3 = np.where(s2)
    if len(xs3):
        out["lab1_lines"].append([70 + int(xs3.min()), y0 + int(ys3.min()), 70 + int(xs3.max()), y0 + int(ys3.max())])
out["lab2_lines"] = []
bluem = (B - R > 55) & (B > 90) & (R < 120)
for y0, y1 in [(175, 197), (197, 230)]:
    s2 = bluem[y0:y1, 70:172]
    ys3, xs3 = np.where(s2)
    if len(xs3):
        out["lab2_lines"].append([70 + int(xs3.min()), y0 + int(ys3.min()), 70 + int(xs3.max()), y0 + int(ys3.max())])
out["lab3_lines"] = []
for y0, y1 in [(260, 278), (278, 296)]:
    s2 = redm[y0:y1, 70:172]
    ys3, xs3 = np.where(s2)
    if len(xs3):
        out["lab3_lines"].append([70 + int(xs3.min()), y0 + int(ys3.min()), 70 + int(xs3.max()), y0 + int(ys3.max())])

# ---------- 8. title/subtitle fine ----------
out["title_ink_bbox"] = [340, 60, 688, 79]
# subtitle underline: solid row
sub = bluem[80:110, 300:760]
prof = sub.sum(axis=1)
out["subtitle_rows_prof"] = [[80 + i, int(prof[i])] for i in range(len(prof)) if prof[i] > 5]
# find underline run: a row where blue is contiguous over "Word Index" (~x 435-535)
for y in range(98, 108):
    xs4 = np.where(bluem[y, 300:760])[0]
    if len(xs4) > 60:
        runs = []
        s = xs4[0]; p = xs4[0]
        for x in xs4[1:]:
            if x - p > 4:
                runs.append([300 + int(s), 300 + int(p)]); s = x
            p = x
        runs.append([300 + int(s), 300 + int(p)])
        out.setdefault("subtitle_underline", {})[y] = runs

# ---------- 9. right-edge red verticals check (020 had them; 021 not) ----------
out["right_red"] = {}
for y0, y1, nm in [(115, 165, "r1"), (180, 235, "r2"), (255, 310, "r3")]:
    sub = redm[y0:y1, 884:900]
    ys5, xs5 = np.where(sub)
    out["right_red"][nm] = int(len(xs5))

# ---------- 10. badge ----------
yellowish = (R > 215) & (G > 215) & (B < 190)
ys6, xs6 = np.where(yellowish[40:110, 845:905])
out["badge_bbox2"] = [845 + int(xs6.min()), 40 + int(ys6.min()), 845 + int(xs6.max()), 40 + int(ys6.max())] if len(xs6) else None
# numeral 22 ink (dark) inside badge
darkm = (A.sum(axis=2) < 330)
sub = darkm[55:90, 860:892]
ys7, xs7 = np.where(sub)
out["badge_numeral_bbox"] = [860 + int(xs7.min()), 55 + int(ys7.min()), 860 + int(xs7.max()), 55 + int(ys7.max())] if len(xs7) else None

# ---------- 11. row1 lane right dash fine + lane top/bottom exact ----------
out["row1_lane_right_scan"] = {}
for y in [120, 130, 140, 150, 155]:
    seg = A[y, 875:895]
    out["row1_lane_right_scan"][y] = " ".join("%02X%02X%02X" % tuple(c) for c in seg)
out["row1_lane_left_scan"] = {}
for y in [120, 130, 140, 150, 155]:
    seg = A[y, 160:180]
    out["row1_lane_left_scan"][y] = " ".join("%02X%02X%02X" % tuple(c) for c in seg)
out["row1_lane_top_scan_x600"] = " ".join("%02X%02X%02X" % tuple(A[y, 600]) for y in range(114, 126))
out["row1_lane_bot_scan_x600"] = " ".join("%02X%02X%02X" % tuple(A[y, 600]) for y in range(152, 164))
out["row2_lane_top_scan_x600"] = " ".join("%02X%02X%02X" % tuple(A[y, 600]) for y in range(182, 194))
out["row2_lane_bot_scan_x600"] = " ".join("%02X%02X%02X" % tuple(A[y, 600]) for y in range(220, 232))
out["row3_lane_top_scan_x660"] = " ".join("%02X%02X%02X" % tuple(A[y, 660]) for y in range(257, 268))
out["row3_lane_bot_scan_x660"] = " ".join("%02X%02X%02X" % tuple(A[y, 660]) for y in range(298, 312))
out["row3_lane_left_scan"] = {}
for y in [268, 275, 285, 295, 302]:
    seg = A[y, 160:178]
    out["row3_lane_left_scan"][y] = " ".join("%02X%02X%02X" % tuple(c) for c in seg)
out["row3_lane_right_scan"] = {}
for y in [268, 275, 285, 295, 302]:
    seg = A[y, 875:895]
    out["row3_lane_right_scan"][y] = " ".join("%02X%02X%02X" % tuple(c) for c in seg)

# ---------- 12. summary line1 left/right ink ----------
sub = dark[362:386, 60:930]
ys8, xs8 = np.where(sub)
out["line1_bbox"] = [60 + int(xs8.min()), 362 + int(ys8.min()), 60 + int(xs8.max()), 362 + int(ys8.max())] if len(xs8) else None

print(json.dumps(out, indent=1))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide022/measure4_output.txt", "w") as f:
    f.write(json.dumps(out, indent=1))
