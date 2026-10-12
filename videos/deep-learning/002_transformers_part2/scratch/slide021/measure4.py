#!/usr/bin/env python3
"""measure4 — slide 021 comprehensive re-measurement (independent pass).
Resolves the ambiguities left by the dead builder: row1 lane/box/digit structure,
row3 box geometry, title/label/navy text ems, tan-line path, right-edge marks.
Frame: unique_slides/slide_021.jpg (960x540, 1 frame px ~ 0.958 slide pt).
"""
import json
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_021.jpg"
img = Image.open(FR).convert("RGB")
A = np.asarray(img).astype(int)
H, W = A.shape[:2]
out = {"size": [W, H]}

def centroid_dark(x0, x1, y0, y1, axis, thr=140):
    """centroid of dark (low-luminance) pixels along axis within window"""
    sub = A[y0:y1, x0:x1]
    lum = sub.sum(axis=2) / 3.0
    mask = lum < thr
    if not mask.any():
        return None
    if axis == "x":
        cols = np.where(mask.any(axis=0))[0]
        wsum = mask.sum(axis=0)[cols]
        return x0 + float((cols * wsum).sum()) / wsum.sum()
    rows = np.where(mask.any(axis=1))[0]
    wsum = mask.sum(axis=1)[rows]
    return y0 + float((rows * wsum).sum()) / wsum.sum()

# 1. chrome landmarks ------------------------------------------------------
out["left"] = centroid_dark(50, 70, 100, 400, "x")
out["right"] = centroid_dark(890, 912, 100, 400, "x")
out["top"] = centroid_dark(100, 800, 36, 52, "y")
out["bottom"] = centroid_dark(100, 800, 505, 525, "y")

# 2. title ----------------------------------------------------------------
sub = A[52:104, 255:680]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
red_m = (r > 110) & (g < 90) & (b < 110)
blue_m = (b > 110) & (r < 100) & (g < 100)
def bbox(mask, x0, y0):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return [x0 + int(xs.min()), y0 + int(ys.min()), x0 + int(xs.max()), y0 + int(ys.max()), int(mask.sum())]
out["title_red"] = bbox(red_m, 255, 52)
out["title_blue"] = bbox(blue_m, 255, 52)
# bracket: leftmost 25 cols of red
out["title_bracket_rows"] = bbox(red_m[:, 0:26], 255, 52)
# "P" of Position: find it — red ink col profile after bracket
colprof = red_m.sum(axis=0)
runs = []
inrun = False
for i, c in enumerate(colprof):
    if c > 0 and not inrun:
        s = i; inrun = True
    elif c == 0 and inrun:
        runs.append([255 + s, 255 + i - 1]); inrun = False
if inrun:
    runs.append([255 + s, 255 + len(colprof) - 1])
out["title_red_colruns"] = runs
# P glyph rows (first run after the bracket+1 gap wider than 8)
pruns = [rr for rr in runs if rr[1] - rr[0] >= 12]
if pruns:
    px0, px1 = pruns[0][0], pruns[0][1]
    out["title_P_bbox"] = bbox(red_m[:, px0 - 255:px1 - 255 + 1], px0, 52)

# 3. blue diagram box ------------------------------------------------------
sub = A[100:370, 60:910]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
bb = (b - r > 60) & (b - g > 40) & (b > 90)
rows = np.where(bb.sum(axis=1) > 400)[0]
cols = np.where(bb.sum(axis=0) > 150)[0]
out["dbox_rows"] = [[100 + int(x), int(bb[x].sum())] for x in rows]
out["dbox_cols"] = [[60 + int(x), int(bb[:, x].sum())] for x in cols]

# 4. ROW1 structure (y 120..195) -------------------------------------------
sub = A[120:196, 140:910]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
# light fill (C9D7F0..CDCBFA): blue-tinted light
fill_m = (b > 225) & (b - r > 20) & (b - g > 15) & (r > 170)
# strong blue (dash/border/digit)
sblue_m = (b - r > 55) & (b > 110) & (r < 160)
out["r1_fill_rows"] = [[120 + int(y), int(fill_m[y].sum())] for y in range(sub.shape[0]) if fill_m[y].sum() > 30]
out["r1_sblue_rows"] = [[120 + int(y), int(sblue_m[y].sum())] for y in range(sub.shape[0]) if sblue_m[y].sum() > 30]
# fill column runs in the box band (rows where fill dense)
band = fill_m
colc = band.sum(axis=0)
runs = []
inrun = False
for i, c in enumerate(colc):
    if c >= 4 and not inrun:
        s = i; inrun = True
    elif c < 4 and inrun:
        runs.append([140 + s, 140 + i - 1, int(colc[s:i].max())]); inrun = False
if inrun:
    runs.append([140 + s, 140 + len(colc) - 1, int(colc[s:].max())])
out["r1_fill_colruns"] = runs
# per-box fill row extent: for the widest run
if runs:
    best = max(runs, key=lambda t: t[1] - t[0])
    rr = fill_m[:, best[0] - 140:best[1] - 140 + 1]
    ys = np.where(rr.sum(axis=1) > 10)[0]
    out["r1_box_rows"] = [120 + int(ys.min()), 120 + int(ys.max())]

# 5. ROW3 structure (y 278..340) -------------------------------------------
sub = A[278:342, 140:910]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
fill_m = (b - r > 8) & (g - r > 5) & (g > 200) & (b > 160) & (r < 245)  # E0F0D0-ish
sgreen_m = (g - r > 45) & (g - b > 25) & (g > 90)  # border/dash/text green
out["r3_fill_rows"] = [[278 + int(y), int(fill_m[y].sum())] for y in range(sub.shape[0]) if fill_m[y].sum() > 30]
out["r3_sgreen_rows"] = [[278 + int(y), int(sgreen_m[y].sum())] for y in range(sub.shape[0]) if sgreen_m[y].sum() > 20]
colc = fill_m.sum(axis=0)
runs = []
inrun = False
for i, c in enumerate(colc):
    if c >= 5 and not inrun:
        s = i; inrun = True
    elif c < 5 and inrun:
        runs.append([140 + s, 140 + i - 1]); inrun = False
if inrun:
    runs.append([140 + s, 140 + len(colc) - 1])
out["r3_fill_colruns"] = runs
if runs:
    best = max(runs, key=lambda t: t[1] - t[0])
    rr = fill_m[:, best[0] - 140:best[1] - 140 + 1]
    ys = np.where(rr.sum(axis=1) > 8)[0]
    out["r3_box_rows"] = [278 + int(ys.min()), 278 + int(ys.max())]
# lane background sample: rows between boxes' outside and lane borders
def mode_hex(x0, x1, y0, y1):
    sub = A[y0:y1, x0:x1].reshape(-1, 3)
    q = (sub // 8 * 8)
    vals, counts = np.unique(q, axis=0, return_counts=True)
    o = counts.argsort()[::-1][:4]
    return [[ "%02X%02X%02X" % tuple(vals[i]), int(counts[i])] for i in o]
out["r3_band_mode"] = mode_hex(620, 720, 292, 326)   # gap region between P5 and PN-2
out["r1_gap_mode"] = mode_hex(620, 720, 138, 173)    # row1 gap region
out["r1_outside_mode"] = mode_hex(155, 165, 168, 178)  # left of first box below dash
out["r3_outside_mode"] = mode_hex(155, 165, 330, 336)
out["panel_mode"] = mode_hex(30, 40, 300, 400)

# 6. navy bar + text --------------------------------------------------------
sub = A[210:258, 160:900]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
navy_m = (b > 120) & (r < 60) & (g < 60)
ys = np.where(navy_m.sum(axis=1) > 400)[0]
out["navy_rows_dense"] = [210 + int(ys.min()), 210 + int(ys.max())]
cols = np.where(navy_m.sum(axis=0) > 20)[0]
out["navy_cols"] = [160 + int(cols.min()), 160 + int(cols.max())]
yel_m = (r > 190) & (g > 190) & (b < 140)
out["navy_yellow_ink"] = bbox(yel_m, 160, 210)
wh_m = (r > 190) & (g > 190) & (b > 190)
out["navy_white_ink"] = bbox(wh_m, 160, 210)
out["navy_yellow_rows"] = bbox(yel_m[:, 286 - 160:373 - 160], 286, 210)
out["navy_white_rows"] = bbox(wh_m[:, 385 - 160:769 - 160], 385, 210)

# 7. brace fine profile -----------------------------------------------------
sub = A[330:358, 160:880]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
red_m = (r > 120) & (r - g > 50) & (r - b > 40)
prof = {}
for y in range(sub.shape[0]):
    xs = np.where(red_m[y])[0]
    if len(xs) > 0:
        prof[330 + y] = [160 + int(xs.min()), 160 + int(xs.max()), int(len(xs))]
out["brace_profile"] = prof

# 8. tan line ---------------------------------------------------------------
# tan D6B9A3-ish: r>170, g 150..210, b 120..190, r>g>b
sub = A[250:420, 230:470]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
tan_m = (r > 165) & (r - b > 20) & (g - b > 8) & (b > 100) & (b < 200) & (g < 225)
ys, xs = np.where(tan_m)
if len(xs):
    # per-row centroid to trace the line path
    trace = {}
    for yy in np.unique(ys):
        sel = xs[ys == yy]
        if len(sel) >= 2:
            trace[250 + int(yy)] = [230 + int(sel.min()), 230 + int(sel.max()), len(sel)]
    out["tan_trace"] = trace

# 9. yellow box -------------------------------------------------------------
sub = A[370:505, 60:280]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
yf_m = (r > 235) & (g > 235) & (b > 190) & (b < 245) & (r - b > 15)
ys = np.where(yf_m.sum(axis=1) > 60)[0]
cols = np.where(yf_m.sum(axis=0) > 25)[0]
out["ybox_fill"] = [60 + int(cols.min()), 370 + int(ys.min()), 60 + int(cols.max()), 370 + int(ys.max())]
# border (tan) rows/cols
tb_m = (r > 150) & (r - b > 25) & (g - b > 5) & (b < 190) & (g < 215)
rows = np.where(tb_m.sum(axis=1) > 60)[0]
out["ybox_border_rows"] = [370 + int(x) for x in rows]
cols2 = np.where(tb_m.sum(axis=0) > 40)[0]
out["ybox_border_cols"] = [60 + int(x) for x in cols2]
# text: blue + red inks
blue_m = (b - r > 40) & (b > 100) & (r < 150)
out["ybox_blue_rows_prof"] = [[370 + int(y), int(blue_m[y].sum())] for y in range(sub.shape[0]) if blue_m[y].sum() > 3]
red_m2 = (r > 130) & (r - g > 60) & (r - b > 60)
out["ybox_red_ink"] = bbox(red_m2, 60, 370)

# 10. green box -------------------------------------------------------------
sub = A[360:500, 300:780]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
gb = (g - r > 30) & (g - b > 30) & (g > 100)
rows = np.where(gb.sum(axis=1) > 200)[0]
out["gbox_border_rows"] = [360 + int(x) for x in rows]
cols = np.where(gb.sum(axis=0) > 40)[0]
out["gbox_border_cols"] = [300 + int(x) for x in cols]
blk_m = (r < 90) & (g < 90) & (b < 90)
prof = [[360 + int(y), int(blk_m[y].sum())] for y in range(sub.shape[0]) if blk_m[y].sum() > 3]
out["gbox_black_rows_prof"] = prof
out["gbox_black_cols"] = bbox(blk_m, 300, 360)

# 11. left labels -----------------------------------------------------------
sub = A[125:265, 60:180]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
blue_m = (b - r > 40) & (b > 100) & (r < 160)
red_m3 = (r > 120) & (r - g > 55) & (r - b > 45)
out["lab_blue_rows"] = [[125 + int(y), int(blue_m[y].sum())] for y in range(sub.shape[0]) if blue_m[y].sum() > 2]
out["lab_red_rows"] = [[125 + int(y), int(red_m3[y].sum())] for y in range(sub.shape[0]) if red_m3[y].sum() > 2]
out["lab_blue_ink"] = bbox(blue_m, 60, 125)
out["lab_red_ink"] = bbox(red_m3, 60, 125)

# 12. right-edge red verticals? (020 had them at x 887-890) -----------------
sub = A[125:340, 880:915]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
red_m4 = (r > 110) & (r - g > 45) & (r - b > 35)
prof = {}
for y in range(sub.shape[0]):
    xs = np.where(red_m4[y])[0]
    if len(xs) > 0:
        prof[125 + y] = [880 + int(xs.min()), 880 + int(xs.max()), len(xs)]
out["right_red_profile"] = prof

# 13. row1 dots -------------------------------------------------------------
sub = A[140:180, 620:720]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
dot_m = (b - r > 25) & (b > 130) & (r < 200)
cols = np.where(dot_m.sum(axis=0) > 2)[0]
runs = []
inrun = False
for i in range(len(cols) + 1):
    if i < len(cols) and (i == 0 or cols[i] == cols[i - 1] + 1):
        if not inrun:
            s = cols[i]; inrun = True
    else:
        if inrun:
            runs.append([620 + int(s), 620 + int(cols[i - 1])]); inrun = False
out["r1_dot_colruns"] = runs
ys = np.where(dot_m.sum(axis=1) > 2)[0]
out["r1_dot_rows"] = [140 + int(ys.min()), 140 + int(ys.max())] if len(ys) else None

with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide021/measure4_output.txt", "w") as f:
    f.write(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
