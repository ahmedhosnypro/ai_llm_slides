#!/usr/bin/env python3
"""MASTER measurement slide_039 -> slide pts JSON (frame->slide: x=(fx-18.63)/0.96123, y=fy/0.95556)."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_039.jpg"
img = Image.open(SRC).convert("RGB")
px = img.load()
SH, DH, SV = 0.96123, 18.63, 0.95556
def S(fx, fy): return (round((fx - DH) / SH, 1), round(fy / SV, 1))
def ink(p): return sum(p) < 640
def reddish(p):
    r, g, b = p
    return r > 120 and r - g > 50 and r - b > 50
def blueish(p):
    r, g, b = p
    return b > 110 and b - r > 60 and b - g > 40

out = {}

def bbox(x0, x1, y0, y1, pred):
    pts = [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1) if pred(px[x, y])]
    if not pts: return None
    a = S(min(p[0] for p in pts), min(p[1] for p in pts))
    b = S(max(p[0] for p in pts), max(p[1] for p in pts))
    return [a[0], a[1], b[0], b[1], round(b[0] - a[0], 1), round(b[1] - a[1], 1)]

def corecolor(x0, x1, y0, y1, pred=None):
    pts = [px[x, y] for y in range(y0, y1 + 1) for x in range(x0, x1 + 1) if ink(px[x, y]) and (pred is None or pred(px[x, y]))]
    pts.sort(key=sum)
    n = min(30, len(pts))
    return tuple(round(sum(p[i] for p in pts[:n]) / n) for i in range(3))

# ---- boxes (border bboxes via red/blue long runs already known) ----
out["quote_box_frame"] = [74, 96, 880, 153]
out["quote_box_slide"] = S(74, 96) + S(880, 153)
out["container_frame"] = [72, 162, 878, 397]
out["container_slide"] = S(72, 162) + S(878, 397)
out["summary_box_frame"] = [72, 410, 878, 503]
out["summary_box_slide"] = S(72, 410) + S(878, 503)

# ---- title ----
out["title_ink_slide"] = bbox(62, 849, 50, 94, ink)
out["title_core_rgb"] = corecolor(344, 565, 58, 84, reddish)

# ---- quote text ----
out["quote_line_ink_slide"] = bbox(78, 876, 98, 132, ink)
out["quote_blue_rgb"] = corecolor(81, 863, 110, 129, blueish)
out["covshift_ink_slide"] = bbox(600, 876, 133, 151, reddish)
out["covshift_red_rgb"] = corecolor(688, 844, 134, 151, reddish)

# ---- container: white fill check between quote box and container, container and summary
out["gap_fill_1"] = px[500, 158]
out["gap_fill_2"] = px[500, 403]
out["container_fill"] = px[300, 300]

# ---- flowchart boxes: yellow fills
ypts = [(x, y) for y in range(165, 260) for x in range(76, 875)
        if px[x, y][0] > 235 and px[x, y][1] > 235 and 190 < px[x, y][2] < 225]
cols = sorted(set(p[0] for p in ypts))
runs = []
x0 = cols[0]; prev = cols[0]
for x in cols[1:]:
    if x - prev > 3: runs.append((x0, prev)); x0 = x
    prev = x
runs.append((x0, prev))
rows_y = sorted(set(p[1] for p in ypts))
out["flow_yellow_col_runs_frame"] = runs
out["flow_yellow_rows_frame"] = [rows_y[0], rows_y[-1]]
out["flow_fill_rgb"] = px[200, 200]
# per-box border bbox: reddish bbox within each yellow column run +- few px
boxes = []
for (cx0, cx1) in runs:
    b = bbox(cx0 - 4, cx1 + 4, 165, 250, reddish)
    boxes.append(b)
out["flow_box_borders_slide"] = boxes

# flow text lines per box (inside border, excluding border rows)
def lines_in(x0, x1, y0, y1, gap=2):
    rows = {}
    for y in range(y0, y1 + 1):
        xs = [x for x in range(x0, x1 + 1) if ink(px[x, y])]
        if len(xs) >= 2: rows[y] = (min(xs), max(xs))
    segs = []
    cur = None
    for y in sorted(rows):
        if cur and y <= cur[1] + gap: cur[1] = y; cur[2].append(rows[y])
        else:
            if cur: segs.append(cur)
            cur = [y, y, [rows[y]]]
    if cur: segs.append(cur)
    res = []
    for y0s, y1s, sl in segs:
        fx0 = min(s[0] for s in sl); fx1 = max(s[1] for s in sl)
        res.append({"frame": [fx0, y0s, fx1, y1s], "slide": S(fx0, y0s) + S(fx1, y1s)})
    return res

out["flow1_text_lines"] = lines_in(120, 288, 176, 240)
out["flow2_text_lines"] = lines_in(346, 566, 176, 240)
out["flow3_text_lines"] = lines_in(622, 836, 176, 240)

# flow text colors (cores)
out["flow1_l1_rgb"] = corecolor(120, 288, 180, 198, reddish)
out["flow1_l2_rgb"] = corecolor(120, 288, 212, 230)
out["flow3_l1_rgb"] = corecolor(622, 836, 180, 198)
out["flow3_l2_rgb"] = corecolor(622, 836, 212, 230, reddish)

# ---- arrows: red ink between boxes
out["arrow1_slide"] = bbox(293, 340, 190, 235, reddish)
out["arrow2_slide"] = bbox(571, 616, 190, 235, reddish)

# ---- text block lines (inside container below flowchart) ----
out["conclusion_ink_slide"] = bbox(80, 300, 248, 270, reddish)
out["stmt1_ink_slide"] = bbox(160, 700, 272, 296, ink)
out["stmt1_blue_rgb"] = corecolor(165, 637, 275, 292, blueish)
out["idea_ink_slide"] = bbox(80, 500, 308, 330, reddish)
out["stmt2_ink_slide"] = bbox(160, 750, 332, 357, ink)
# underline: blue horizontal run in bottom rows of stmt2
urow = None
for y in range(344, 358):
    n = sum(1 for x in range(210, 340) if blueish(px[x, y]))
    if n > 100: urow = (y, n)
out["stmt2_underline_row_frame"] = urow
if urow:
    xs = [x for x in range(160, 750) if blueish(px[x, urow[0]])]
    # contiguous run containing 213..335
    runs_u = []
    x0 = None; prev = None
    for x in xs:
        if x0 is None: x0 = x
        elif x - prev > 2: runs_u.append((x0, prev)); x0 = x
        prev = x
    if x0: runs_u.append((x0, prev))
    out["underline_runs_frame"] = runs_u
out["norm_ink_slide"] = bbox(80, 300, 371, 396, reddish)   # 'Normalization:'
out["transform_ink_slide"] = bbox(218, 463, 371, 396, ink)  # 'Transforming the inputs to be'
out["zero_ink_slide"] = bbox(465, 760, 371, 396, blueish)   # 'Zero mean and unit variance.'
out["transform_rgb"] = corecolor(224, 461, 375, 392)
out["zero_blue_rgb"] = corecolor(467, 714, 375, 392, blueish)

# ---- summary box ----
out["sumhead_ink_slide"] = bbox(76, 500, 414, 440, reddish)
out["sumhead_rgb"] = corecolor(82, 379, 420, 437, reddish)
# bullet lines: split y 441..500
out["sum_lines"] = lines_in(76, 875, 441, 499, gap=1)
out["summary_fill_rgb"] = px[400, 430]
out["summary_fill_rgb2"] = px[600, 490]
out["summary_blue_rgb"] = corecolor(81, 698, 444, 481, blueish)

# stem-width check: 'T' of Transforming (x224.., y375..392) vs 'I'/'Z' bold blue
def stemw(x0, x1, y0, y1):
    # max horizontal ink run in middle rows
    best = 0
    for y in range(y0, y1 + 1):
        run = 0; mx = 0
        for x in range(x0, x1 + 1):
            if ink(px[x, y]): run += 1; mx = max(mx, run)
            else: run = 0
        best = max(best, mx)
    return best
out["stem_T_transforming"] = stemw(224, 240, 375, 392)   # T vertical stem
out["stem_Z_zeromean"] = stemw(467, 483, 375, 392)        # Z stroke bold
out["stem_I_input_stmt1"] = stemw(165, 180, 275, 292)    # I of Input (blue bold)

print(json.dumps(out, indent=1))
