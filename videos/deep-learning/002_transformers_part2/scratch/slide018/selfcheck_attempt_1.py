#!/usr/bin/env python3
"""Closed-loop verification: 150dpi render vs original-frame mapped targets.

Targets are the ORIGINAL frame's strict-mask ink bboxes mapped to true slide
coords (measure_original.json), converted to 150dpi render px (x2.08333).
The render is measured with the SAME strict masks so mask bias cancels.
Tolerance: ~4px @150dpi (= 1.92 slide pt).
Run: python3 selfcheck_attempt_1.py <render.png>
"""
import json
import sys
import numpy as np
from PIL import Image

render = sys.argv[1] if len(sys.argv) > 1 else "slide-1.png"
im = np.asarray(Image.open(render).convert("RGB")).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
S = 150 / 72.0  # slide pt -> render px

red = (R > 140) & (G < 90) & (B < 90) & ((R - G) > 80) & ((R - B) > 80)
blue = (B > 110) & (R < 110) & (G < 110) & ((B - R) > 60) & ((B - G) > 60)
mag = (R > 130) & (B > 130) & (G < 110) & ((R - G) > 60) & ((B - G) > 60)

def bbox(m):
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]

out = {"render_size": [W, H]}

# chrome sanity: panel border present, letterbox ABSENT (no full-width black rows)
blackrow = ((R < 60) & (G < 60) & (B < 60)).mean(axis=1)
out["max_black_row_fraction_bottom_third"] = round(float(blackrow[int(H * 0.93):].max()), 4)

# title
tm = red.copy(); tm[:300, :] = False; tm[620:, :] = False; tm[:, 300:] = False
tb = bbox(tm)
out["title_render_bbox"] = tb
TGT_TITLE = [211.55 * S, 211.24 * S, 740.10 * S, 248.88 * S]  # x0,y0,x1,y1

# box (white fill extent probed through its center, same probe as the original)
inpanel = np.zeros_like(red, dtype=bool)
inpanel[int(0.9 * H):, :] = False
wm = (R > 240) & (G > 240) & (B > 240)
wm[: int(0.20 * H), :] = False  # exclude top canvas margin area
# restrict to panel interior region to avoid outer white canvas
cx_box = int((234.44 + 419.31 / 2) * S)
col = im[:, cx_box, :]
wr = [i for i in range(500, 1050) if col[i].min() > 240]
row_y = (294.87 + 149.55 / 2) * S
row = im[int(row_y), :, :]
wc = [j for j in range(200, 1800) if row[j].min() > 240]
out["box_render"] = {"rows": [wr[0], wr[-1]], "cols": [wc[0], wc[-1]]}
TGT_BOX = {"rows": [294.87 * S, 444.42 * S - 1], "cols": [234.44 * S, 653.74 * S - 1]}

# lines: strict masks inside the box
ymask = np.zeros_like(red); ymask[int(1.38 * 300):, :] = False
l1 = np.zeros_like(red); l1[600:740, 400:1700] = True
l2 = np.zeros_like(red); l2[740:940, 400:1700] = True
ink = (blue | red | mag)
b1 = bbox(ink & l1); b2 = bbox(ink & l2)
bl1 = bbox(blue & l1); bl2 = bbox(blue & l2)
r1 = bbox(red & l1); m2 = bbox(mag & l2)
out["line1_render"] = {"ink": b1, "blue": bl1, "red": r1}
out["line2_render"] = {"ink": b2, "blue": bl2, "mag": m2}
TGT_L1 = {"ink": [265.65 * S, 318.94 * S, 579.87 * S, 347.17 * S],
          "blue": [265.65 * S, 318.94 * S, (431 + 1) * 1.04026, 347.17 * S],
          "red": [(446) * 1.04026, 318.94 * S, 579.87 * S, 347.17 * S]}
TGT_L2 = {"ink": [265.65 * S, 387.96 * S, 607.96 * S, 417.23 * S],
          "blue": [265.65 * S, 387.96 * S, (431 + 1) * 1.04026, 417.23 * S],
          "mag": [(445) * 1.04026, 387.96 * S, 607.96 * S, 417.23 * S]}
# note: frame x -> slide via /0.96113 => frame*1.04026

def d(a, t):
    return [round(a[i] - t[i], 1) for i in range(4)]

res = {
    "title": {"measured": tb, "target_px": [round(v, 1) for v in TGT_TITLE], "delta_px": d(tb, TGT_TITLE)},
    "box": {"measured": out["box_render"], "target_px": {k: [round(v, 1) for v in vv] for k, vv in TGT_BOX.items()}},
    "line1": {"measured": out["line1_render"],
              "target_px": {k: [round(v, 1) for v in TGT_L1[k]] for k in TGT_L1},
              "delta_ink_px": d(b1, TGT_L1["ink"])},
    "line2": {"measured": out["line2_render"],
              "target_px": {k: [round(v, 1) for v in TGT_L2[k]] for k in TGT_L2},
              "delta_ink_px": d(b2, TGT_L2["ink"])},
}
print(json.dumps(res, indent=1))

# correction suggestions
tw = (tb[2] - tb[0] + 1) / S
corr = {"title_measured_w_pt": round(tw, 2), "title_target_w_pt": round((740.10 - 211.55), 2),
        "title_size_suggestion": round(40 * (740.10 - 211.55) / tw, 2)}
if b1:
    w1 = (b1[2] - b1[0] + 1) / S
    corr["line1_measured_w_pt"] = round(w1, 2)
    corr["line1_target_w_pt"] = round(579.87 - 265.65, 2)
    corr["line1_size_suggestion"] = round(30 * (579.87 - 265.65) / w1, 2)
if b2:
    w2 = (b2[2] - b2[0] + 1) / S
    corr["line2_measured_w_pt"] = round(w2, 2)
    corr["line2_target_w_pt"] = round(607.96 - 265.65, 2)
    corr["line2_size_suggestion"] = round(30 * (607.96 - 265.65) / w2, 2)
print(json.dumps(corr, indent=1))
