#!/usr/bin/env python3
"""measure6 — raw pixel samples + final color/geometry pins for slide 021."""
import json
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_021.jpg"
img = Image.open(FR).convert("RGB")
A = np.asarray(img).astype(int)
out = {}

def px(x, y):
    return "%02X%02X%02X" % tuple(A[y, x])

def strip_v(x, y0, y1, step=1):
    return {y: px(x, y) for y in range(y0, y1, step)}

def strip_h(y, x0, x1, step=1):
    return {x: px(x, y) for x in range(x0, x1, step)}

# 1. chrome right stroke raw (rows 400-410, x 895-910) + rows 460-470
out["right_stroke_400"] = strip_h(400, 895, 910)
out["right_stroke_465"] = strip_h(465, 895, 910)
out["right_stroke_200"] = strip_h(200, 895, 910)
# subpixel centroid on redness over clean bands
def red_centroid(x0, x1, y0, y1):
    sub = A[y0:y1, x0:x1]
    w = np.clip(sub[..., 0] - (sub[..., 1] + sub[..., 2]) / 2, 0, None).astype(float)
    if w.sum() == 0:
        return None
    cols = np.arange(x0, x1)
    return float((cols * w.sum(axis=0)).sum() / w.sum())
out["right_cx"] = red_centroid(893, 912, 380, 500)
out["left_cx"] = red_centroid(50, 70, 380, 500)
out["top_cy"] = None
sub = A[36:52, 200:700]
w = np.clip(sub[..., 0] - (sub[..., 1] + sub[..., 2]) / 2, 0, None).astype(float)
rows = np.arange(36, 52)
out["top_cy"] = float((rows * w.sum(axis=1)).sum() / w.sum())

# 2. row1 raw: box1 fill vs lane gap fill vs lane above/below boxes
out["r1_v_x195"] = strip_v(195, 130, 182)      # through box1 fill (left of digit)
out["r1_v_x660"] = strip_v(660, 130, 182)      # through gap (lane fill + dots zone)
out["r1_h_y155"] = strip_h(155, 160, 250)      # across box1 left border + fill
# 3. row3 raw: box1 interior/edges vs gap
out["r3_v_x200"] = strip_v(200, 283, 336)      # through box1
out["r3_v_x660"] = strip_v(660, 283, 336)      # through gap
out["r3_h_y310"] = strip_h(310, 168, 250)      # across box1 left edge
out["r3_h_y310b"] = strip_h(310, 228, 260)     # across box1 right edge
# 4. tan upper segment: rows 253-291 x 300-340 — any non-white pixel?
seg = []
for y in range(253, 292):
    row = A[y, 300:340]
    for i in range(row.shape[0]):
        r, g, b = row[i]
        if not (r > 235 and g > 235 and b > 235) and not (b - r > 40):
            seg.append((y, 300 + i, "%02X%02X%02X" % (r, g, b)))
out["tan_upper_hits"] = seg[:60]
out["tan_upper_n"] = len(seg)
# 5. dots color census (strictly darker than lane fill)
sub = A[150:162, 630:712].reshape(-1, 3)
m = (sub[..., 2] - sub[..., 0] > 30) & (sub[..., 0] < 190)
sel = sub[m]
if len(sel):
    q = sel // 4 * 4
    vals, counts = np.unique(q, axis=0, return_counts=True)
    o = counts.argsort()[::-1][:3]
    out["dot_core2"] = {"n": int(m.sum()), "modes": [["%02X%02X%02X" % tuple(v), int(c)] for v, c in zip(vals[o], counts[o])]}
# per-dot runs at row 156
row = A[156, 620:720]
dark = [620 + i for i in range(100) if row[i][2] - row[i][0] > 40 and row[i][0] < 190]
out["dot_row156_dark"] = dark
# 6. arrow + brace + subscript color census
def cen(x0, x1, y0, y1, fn, q=4, n=3):
    sub = A[y0:y1, x0:x1].reshape(-1, 3)
    m = fn(sub)
    sel = sub[m]
    if not len(sel):
        return None
    qq = sel // q * q
    vals, counts = np.unique(qq, axis=0, return_counts=True)
    o = counts.argsort()[::-1][:n]
    return {"n": int(m.sum()), "modes": [["%02X%02X%02X" % tuple(v), int(c)] for v, c in zip(vals[o], counts[o])]}
out["arrow1_core"] = cen(515, 530, 178, 206, lambda p: (p[..., 0] > 120) & (p[..., 0] - p[..., 1] > 60))
out["r1_digit_census2"] = cen(200, 220, 148, 162, lambda p: (p[..., 2] - p[..., 0] > 50) & (p[..., 2] > 120) & (p[..., 0] < 150))
out["brace_dark"] = cen(200, 850, 342, 345, lambda p: (p[..., 0] > 100) & (p[..., 0] - p[..., 1] > 40))
# 7. title em check: '[' bracket bbox + E cap
out["bracket_v"] = strip_v(276, 58, 100)
# 8. navy bar edges precise: cols at y 230
out["navy_h_y230"] = {x: px(x, 230) for x in list(range(160, 172)) + list(range(886, 898))}
# 9. dbox border rows precise at x 400
out["dbox_v_x400_top"] = strip_v(400, 108, 116)
out["dbox_v_x400_bot"] = strip_v(400, 353, 361)
# 10. ybox L1/L3 rows (red '[' + blue) for line tops
out["ybox_v_x86"] = strip_v(86, 393, 482, 1)  # through the '[' glyphs
# 11. green box border thickness at x 500
out["gbox_v_x500_top"] = strip_v(500, 368, 378)
out["gbox_v_x500_bot"] = strip_v(500, 484, 494)
# 12. gbox text: G1 'R' stem rows + full ink cols to size em
out["gbox_R_v"] = strip_v(342, 378, 398)
# 13. row1 lane left edge: cols at y 155
out["r1_h_y155_left"] = strip_h(155, 158, 182)
# 14. row3 lane left edge
out["r3_h_y310_left"] = strip_h(310, 158, 178)

with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide021/measure6_output.txt", "w") as f:
    f.write(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
