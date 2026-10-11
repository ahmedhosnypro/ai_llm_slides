#!/usr/bin/env python3
"""Fix-up measurements: colors (mode), underline, bullet split, boldness, arrows, box borders."""
from PIL import Image
from collections import Counter
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_039.jpg"
img = Image.open(SRC).convert("RGB")
px = img.load()
SH, DH, SV = 0.96123, 18.63, 0.95556
def S(fx, fy): return (round((fx - DH) / SH, 1), round(fy / SV, 1))
def ink(p): return sum(p) < 640

out = {}

def mode_color(x0, x1, y0, y1, q=24):
    c = Counter()
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            p = px[x, y]
            if ink(p):
                c[(p[0] // q * q, p[1] // q * q, p[2] // q * q)] += 1
    return c.most_common(6)

out["title_mode"] = mode_color(344, 565, 58, 84)
out["quote_mode"] = mode_color(81, 863, 108, 131)
out["covshift_mode"] = mode_color(688, 845, 133, 151)
out["conclusion_mode"] = mode_color(88, 184, 250, 267)
out["stmt1_mode"] = mode_color(165, 638, 273, 294)
out["transform_mode"] = mode_color(224, 462, 373, 394)
out["zero_mode"] = mode_color(466, 715, 373, 394)
out["sumhead_mode"] = mode_color(82, 380, 419, 439)
out["sumbody_mode"] = mode_color(81, 699, 442, 483)
out["flow_border_mode"] = mode_color(116, 292, 172, 244, q=16)
out["quote_border_mode"] = mode_color(74, 880, 96, 153, q=16)
out["summary_border_mode"] = mode_color(72, 878, 410, 503, q=16)

# underline scan rows 344..360 x205..345: any long horizontal dark run
prof = {}
for y in range(344, 362):
    n = sum(1 for x in range(205, 345) if ink(px[x, y]))
    prof[y] = n
out["stmt2_rowprof"] = prof
# full-width extent of underline row(s)
urows = [y for y, n in prof.items() if n > 60]
if urows:
    for y in urows:
        xs = [x for x in range(160, 760) if ink(px[x, y])]
        runs = []
        x0 = xs[0]; prev = xs[0]
        for x in xs[1:]:
            if x - prev > 3: runs.append((x0, prev)); x0 = x
            prev = x
        runs.append((x0, prev))
        out[f"underline_y{y}_runs_frame"] = runs

# summary rows profile to split bullet lines
prof2 = {}
for y in range(440, 500):
    n = sum(1 for x in range(76, 875) if ink(px[x, y]))
    if n: prof2[y] = n
out["summary_rowprof"] = prof2

# bold test: stem width of T in Transforming at mid-height rows (below top bar)
def hrun(y, x0, x1):
    best = 0; run = 0
    for x in range(x0, x1 + 1):
        if ink(px[x, y]): run += 1; best = max(best, run)
        else: run = 0
    return best
out["T_bar_row"] = [hrun(y, 222, 242) for y in range(375, 382)]
out["T_stem_rows"] = [hrun(y, 228, 238) for y in range(382, 392)]
# compare: Z of Zero (bold blue) vertical stroke, x467..483
out["Z_stem_rows"] = [hrun(y, 469, 481) for y in range(375, 392)]
# I of Input stmt1 (bold blue) x165..178
out["I_stem_rows"] = [hrun(y, 166, 176) for y in range(275, 292)]
# N of Normalization: (bold red) x89..110
out["N_stem_rows"] = [hrun(y, 90, 102) for y in range(375, 392)]
# t of 'the' in 'Transforming the' — regular black lowercase stem x330..340
out["t_stem_rows"] = [hrun(y, 330, 342) for y in range(378, 392)]

# arrows precise frame bbox (reddish incl. darker)
def bboxf(x0, x1, y0, y1):
    pts = [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)
           if (lambda p: p[0] > 110 and p[0] - p[1] > 35 and p[0] - p[2] > 35)(px[x, y])]
    if not pts: return None
    return [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)]
a1 = bboxf(292, 342, 190, 240)
a2 = bboxf(570, 619, 190, 240)
out["arrow1_frame"] = a1
out["arrow2_frame"] = a2
out["arrow1_slide"] = S(a1[0], a1[1]) + S(a1[2], a1[3]) if a1 else None
out["arrow2_slide"] = S(a2[0], a2[1]) + S(a2[2], a2[3]) if a2 else None
# arrow vertical profile (head rows taller)
if a1:
    out["arrow1_rowprof"] = {y: sum(1 for x in range(a1[0], a1[2] + 1)
                                    if (lambda p: p[0] > 110 and p[0] - p[1] > 35 and p[0] - p[2] > 35)(px[x, y]))
                             for y in range(a1[1], a1[3] + 1)}

# box border rects = yellow bbox (already have col runs); slide coords
runs = [(117, 291), (342, 569), (618, 839)]
out["flow_boxes_slide"] = [S(r[0] - 1, 171) + S(r[1] + 2, 245) for r in runs]

# line C re-measure excluding border rows (y<=394)
def bbox_ink(x0, x1, y0, y1):
    pts = [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1) if ink(px[x, y])]
    if not pts: return None
    a = S(min(p[0] for p in pts), min(p[1] for p in pts))
    b = S(max(p[0] for p in pts), max(p[1] for p in pts))
    return [a[0], a[1], b[0], b[1], round(b[0] - a[0], 1), round(b[1] - a[1], 1)]
def bbox_red(x0, x1, y0, y1):
    pts = [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)
           if (lambda p: p[0] > 110 and p[0] - p[1] > 35 and p[0] - p[2] > 35)(px[x, y])]
    if not pts: return None
    a = S(min(p[0] for p in pts), min(p[1] for p in pts))
    b = S(max(p[0] for p in pts), max(p[1] for p in pts))
    return [a[0], a[1], b[0], b[1], round(b[0] - a[0], 1), round(b[1] - a[1], 1)]
def bbox_blue(x0, x1, y0, y1):
    pts = [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)
           if (lambda p: p[2] > 100 and p[2] - p[0] > 45 and p[2] - p[1] > 30)(px[x, y])]
    if not pts: return None
    a = S(min(p[0] for p in pts), min(p[1] for p in pts))
    b = S(max(p[0] for p in pts), max(p[1] for p in pts))
    return [a[0], a[1], b[0], b[1], round(b[0] - a[0], 1), round(b[1] - a[1], 1)]

out["lineC_norm_red"] = bbox_red(80, 218, 371, 394)
out["lineC_transform_ink"] = bbox_ink(220, 464, 371, 394)
out["lineC_zero_blue"] = bbox_blue(464, 760, 371, 394)
# line A period color: last word run x597..637
out["lineA_period_mode"] = mode_color(620, 640, 275, 294)

# summary bullet dots: ink at x 78..96 rows 444..483
out["bulletdot_rows"] = {y: sum(1 for x in range(78, 98) if ink(px[x, y])) for y in range(442, 486)
                         if sum(1 for x in range(78, 98) if ink(px[x, y])) > 0}

# 'during training steps' bbox (frame) precise: box1 interior line2
out["flow1_l2"] = bbox_ink(118, 290, 208, 240)
out["flow2_l1"] = bbox_ink(344, 568, 176, 208)
out["flow2_l2"] = bbox_ink(344, 568, 208, 240)
out["flow3_l1"] = bbox_ink(620, 838, 176, 208)
out["flow3_l2"] = bbox_ink(620, 838, 208, 240)
out["flow1_l1"] = bbox_ink(118, 290, 176, 208)

# quote line exact left/right ink + cap height rows
prof3 = {}
for y in range(100, 134):
    n = sum(1 for x in range(78, 876) if ink(px[x, y]))
    if n: prof3[y] = n
out["quote_rowprof"] = prof3

# title rows profile (for cap height + baseline)
prof4 = {}
for y in range(48, 96):
    n = sum(1 for x in range(340, 570) if ink(px[x, y]))
    if n: prof4[y] = n
out["title_rowprof"] = prof4

print(json.dumps(out, indent=1))
