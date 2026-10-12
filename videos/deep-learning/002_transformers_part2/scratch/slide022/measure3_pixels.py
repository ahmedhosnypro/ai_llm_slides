#!/usr/bin/env python3
"""measure3 — slide 022 raw pixel probes: rows 1/2/3 lane+box edges, colors,
arrow geometry, bottom panel, title/labels. Prints raw RGB samples."""
import json
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg"
img = Image.open(FR).convert("RGB")
A = np.asarray(img).astype(int)
out = {}

def px(x, y):
    return "%02X%02X%02X" % tuple(A[y, x])

def hscan(y, x0, x1, label):
    """print color transitions along a horizontal line"""
    out[label + f" y={y}"] = None
    prev = None
    trans = []
    for x in range(x0, x1):
        v = tuple((A[y, x] // 24) * 24)  # coarse quantize for transition detection
        if v != prev:
            trans.append((x, "%02X%02X%02X" % tuple(A[y, x])))
            prev = v
    out[label + f" y={y}"] = trans[:80]

def vscan(x, y0, y1, label):
    prev = None
    trans = []
    for y in range(y0, y1):
        v = tuple((A[y, x] // 24) * 24)
        if v != prev:
            trans.append((y, "%02X%02X%02X" % tuple(A[y, x])))
            prev = v
    out[label + f" x={x}"] = trans[:80]

# ROW1: horizontal scan through the middle of the boxes (y~135)
hscan(136, 160, 900, "row1_mid")
# vertical scan through box1 center (x~212) full row band
vscan(212, 105, 175, "row1_box1")
# vertical scan in the gap region (x~660, dots)
vscan(660, 105, 175, "row1_gap")
# horizontal scan through row1 lane top border zone
hscan(112, 160, 900, "row1_topborder")
hscan(158, 160, 900, "row1_botborder")

# ROW2: horizontal scan y~205
hscan(205, 160, 900, "row2_mid")
vscan(212, 178, 240, "row2_box1")
vscan(660, 178, 240, "row2_gap")

# ROW3: horizontal scan y~285 (box band)
hscan(285, 160, 900, "row3_mid")
vscan(212, 255, 330, "row3_box1")
vscan(660, 255, 330, "row3_gap")
# arrow band scan y~300
hscan(300, 200, 600, "row3_arrowband")
# delta band scan y~322
hscan(322, 200, 600, "row3_deltaband")

# BOTTOM panel: vertical scan x~450 (through text)
vscan(450, 340, 520, "panel_v")
hscan(360, 40, 930, "panel_line1")
# cyan fill + border colors
out["cyan_fill_px"] = [px(100, 400), px(500, 460), px(800, 400)]
out["cyan_border_px"] = [px(450, 348), px(450, 349), px(450, 350), px(450, 501), px(450, 502), px(450, 503)]
out["cyan_border_left_px"] = [px(66, 430), px(67, 430), px(68, 430), px(69, 430), px(70, 430)]
out["cyan_border_right_px"] = [px(890, 430), px(891, 430), px(892, 430), px(893, 430), px(894, 430)]

# DIAGRAM panel border colors
out["dbox_border_px"] = [px(64, 250), px(65, 250), px(66, 250), px(892, 250), px(893, 250), px(894, 250)]
out["dbox_top_px"] = [px(450, 110), px(450, 111), px(450, 112), px(450, 113)]
out["dbox_bot_px"] = [px(450, 340), px(450, 341), px(450, 342), px(450, 343), px(450, 344)]

# ROW1 lane border: the dashed dark border around the pale-yellow lane
# find lane extents: scan x for the fill edges at y=120 (above boxes)
hscan(120, 160, 900, "row1_y120")
hscan(150, 160, 900, "row1_y150")
# row1 lane border vertical dashes: probe columns near x=168-172 and 880-885
out["row1_lane_left_px"] = [px(164, 135), px(165, 135), px(166, 135), px(167, 135), px(168, 135), px(169, 135), px(170, 135)]
out["row1_lane_left2_px"] = [px(164, 125), px(165, 125), px(166, 125), px(167, 125), px(168, 125), px(169, 125), px(170, 125)]
out["row1_lane_right_px"] = [px(878, 135), px(879, 135), px(880, 135), px(881, 135), px(882, 135), px(883, 135), px(884, 135), px(885, 135)]
# row1 box borders red: probe around Word 0 box edges (x 185-190, 235-240?)
out["row1_box_border_px"] = [px(186, 135), px(187, 135), px(188, 135), px(189, 135), px(190, 135), px(191, 135)]

# ROW2 lane left/right border dashes
out["row2_lane_left_px"] = [px(164, 205), px(165, 205), px(166, 205), px(167, 205), px(168, 205), px(169, 205), px(170, 205)]
out["row2_lane_right_px"] = [px(878, 205), px(879, 205), px(880, 205), px(881, 205), px(882, 205), px(883, 205), px(884, 205), px(885, 205)]
# ROW2 box border colors
out["row2_box_border_px"] = [px(188, 205), px(189, 205), px(190, 205), px(191, 205), px(216, 205), px(217, 205), px(218, 205), px(219, 205)]

# ROW3 lane left/right border dashes
out["row3_lane_left_px"] = [px(163, 285), px(164, 285), px(165, 285), px(166, 285), px(167, 285), px(168, 285), px(169, 285), px(170, 285)]
out["row3_lane_left2_px"] = [px(163, 275), px(164, 275), px(165, 275), px(166, 275), px(167, 275), px(168, 275), px(169, 275), px(170, 275)]
out["row3_lane_right_px"] = [px(876, 285), px(877, 285), px(878, 285), px(879, 285), px(880, 285), px(881, 285), px(882, 285), px(883, 285), px(884, 285)]
# ROW3 box borders
out["row3_box_border_px"] = [px(185, 285), px(186, 285), px(187, 285), px(188, 285), px(189, 285), px(238, 285), px(239, 285), px(240, 285), px(241, 285)]

# arrows: fine probe around x 272-280 (arrow 1 head zone), y 294-303
out["arrow1_probe"] = {}
for y in range(293, 306):
    row = []
    for x in range(268, 285):
        c = A[y, x]
        row.append("%02X%02X%02X" % tuple(c) if (c[0] > 150 and c[0] - c[2] > 40) else "..")
    out["arrow1_probe"][y] = " ".join(row)

# delta labels: probe band y 315-330 for orange ink
orange = (A[..., 0] > 160) & (A[..., 0] - A[..., 2] > 60) & (A[..., 1] > 60) & (A[..., 1] < 200)
ys, xs = np.where(orange[310:335, 150:900])
out["delta_orange_bboxes"] = None
if len(xs):
    # cluster by x
    order = np.argsort(xs)
    xs_s = xs[order] + 150
    ys_s = ys[order] + 310
    clusters = []
    cur = [xs_s[0], xs_s[0], ys_s[0], ys_s[0]]
    for x, y in zip(xs_s[1:], ys_s[1:]):
        if x - cur[1] <= 12:
            cur[1] = max(cur[1], x); cur[2] = min(cur[2], y); cur[3] = max(cur[3], y)
        else:
            clusters.append(cur); cur = [x, x, y, y]
    clusters.append(cur)
    out["delta_orange_bboxes"] = [[int(v) for v in c] for c in clusters]

# orange arrows: cluster x 150-900, y 288-310
ys, xs = np.where(orange[286:312, 150:900])
clusters = []
if len(xs):
    xs_s = np.sort(np.unique(xs)) + 150
    cur = [xs_s[0], xs_s[0]]
    for x in xs_s[1:]:
        if x - cur[1] <= 12:
            cur[1] = max(cur[1], x)
        else:
            clusters.append(cur); cur = [x, x]
    clusters.append(cur)
out["arrow_orange_xclusters"] = [[int(v) for v in c] for c in clusters]

# dots row1: fine columns
grayish = (abs(A[..., 0] - A[..., 1]) < 20) & (abs(A[..., 1] - A[..., 2]) < 20) & (A[..., 0] < 190) & (A[..., 0] > 90)
sub = grayish[125:150, 615:725]
colc = sub.sum(axis=0)
out["dots1_cols"] = [[615 + i, int(colc[i])] for i in range(len(colc)) if colc[i] > 0]
out["dots1_px"] = [px(638, 139), px(640, 139), px(655, 139), px(657, 139), px(672, 139), px(690, 139), px(708, 139)]
# dots row2 (lavender/blue)
sub2 = (A[195:225, 615:725, 2] - A[195:225, 615:725, 0] > 25)
colc2 = sub2.sum(axis=0)
out["dots2_cols"] = [[615 + i, int(colc2[i])] for i in range(len(colc2)) if colc2[i] > 1]
out["dots2_px"] = [px(640, 207), px(642, 207), px(658, 207), px(676, 207), px(694, 207), px(708, 207)]

# title em check: cap height of 'S' (col of S start)
sub = A[52:85, 340:360]
redm = (sub[..., 0] > 110) & (sub[..., 0] - sub[..., 1] > 40)
rows = np.where(redm.any(axis=1))[0]
out["title_S_rows"] = [52 + int(rows.min()), 52 + int(rows.max())] if len(rows) else None
# subtitle cap rows
sub = A[80:110, 322:340]
blum = (sub[..., 2] - sub[..., 0] > 40)
rows = np.where(blum.any(axis=1))[0]
out["subtitle_paren_rows"] = [80 + int(rows.min()), 80 + int(rows.max())] if len(rows) else None

print(json.dumps(out, indent=1))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide022/measure3_output.txt", "w") as f:
    f.write(json.dumps(out, indent=1))
