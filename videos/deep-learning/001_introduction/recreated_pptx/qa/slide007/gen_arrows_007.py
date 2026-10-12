#!/usr/bin/env python3
"""Generate the slide-007 arrow fan as ONE 600dpi transparent PNG (certified
slide_011 mechanism: catmull-rom centerline through PIL-traced stroke centers +
solid triangle heads, exact-size embed via JSON sidecar).

Traces are from measure_original.py output (frame px, 1px = 1pt):
  shared origin (486.5, 251) at title-box bottom; heads tip down at y~327
  landing on the box-top centers (180 / 386.5 / 590 / 795).
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

DPI = 600
ASSET = ("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/"
         "recreated_pptx/build/assets/arrows007.png")
RED = "#C00000"
LW = 2.2  # stroke width in frame-px (= pt)

# canvas in frame px
X0, Y0, X1, Y1 = 175, 245, 800, 330

A1 = [(486.5, 251), (486.5, 256), (486.5, 260), (485, 264), (475, 268), (467.5, 272),
      (456, 276), (440, 280), (416, 284), (372.5, 288), (309, 292), (258.5, 296),
      (228.5, 300), (210.5, 304), (198.5, 308), (190.5, 312), (187, 315)]
A2 = [(486.5, 251), (485.5, 264), (483, 268), (480.5, 272), (477, 276), (472, 280),
      (464.5, 284), (451, 288), (429.5, 292), (412.5, 296), (402, 300), (396.5, 304),
      (392.5, 308), (390, 312), (388.5, 315.5)]
A3 = [(486.5, 251), (487.5, 264), (490.5, 268), (492, 272), (496.5, 276), (501.5, 280),
      (509.5, 284), (524, 288), (545.5, 292), (563, 296), (574, 300), (580.5, 304),
      (584, 308), (587, 312), (588.5, 315.5)]
A4 = [(486.5, 251), (487.5, 264), (498, 268), (505.5, 272), (517, 276), (533, 280),
      (557.5, 284), (601.5, 288), (665.5, 292), (715.5, 296), (746.5, 300), (764, 304),
      (775.5, 308), (784, 312), (787.5, 315.5)]

HEADS = {  # tip (x, y), base y, half width  (base y~316.5, tip y~327, ~11px wide)
    1: ((180.0, 327.0), 316.5, 5.5),
    2: ((386.5, 327.0), 316.5, 5.5),
    3: ((590.0, 327.0), 316.5, 5.5),
    4: ((795.0, 327.0), 316.5, 5.5),
}

def catmull_rom(pts, n=240):
    pts = np.asarray(pts, float)
    if len(pts) < 3:
        t = np.linspace(0, 1, n)
        return np.stack([np.interp(t, [0, 1], pts[:, 0]), np.interp(t, [0, 1], pts[:, 1])], axis=1)
    p = np.vstack([pts[0] + (pts[0] - pts[1]), pts, pts[-1] + (pts[-1] - pts[-2])])
    out = []
    segs = len(p) - 3
    for i in range(segs):
        p0, p1, p2, p3 = p[i], p[i+1], p[i+2], p[i+3]
        t = np.linspace(0, 1, max(2, n // segs), endpoint=False)
        out.append(0.5 * ((2*p1) + (-p0+p2)*t[:, None] + (2*p0-5*p1+4*p2-p3)*(t**2)[:, None]
                          + (-p0+3*p1-3*p2+p3)*(t**3)[:, None]))
    out.append(p[-2][None, :])
    return np.vstack(out)

w_pt, h_pt = X1 - X0, Y1 - Y0
fig = plt.figure(figsize=(w_pt/72, h_pt/72), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, w_pt); ax.set_ylim(h_pt, 0)
ax.axis("off")

for key, pts in {1: A1, 2: A2, 3: A3, 4: A4}.items():
    q = np.asarray(pts) - np.array([X0, Y0])
    curve = catmull_rom(q)
    ax.plot(curve[:, 0], curve[:, 1], color=RED, lw=LW, solid_capstyle="round", zorder=2)
    (tx, ty), by, hw = HEADS[key]
    ax.add_patch(Polygon([(tx - X0, ty - Y0), (tx - hw - X0, by - Y0), (tx + hw - X0, by - Y0)],
                         closed=True, color=RED, zorder=3))

fig.savefig(ASSET, dpi=DPI, transparent=True)
plt.close(fig)
info = {"asset": ASSET, "canvas_pt": [X0, Y0, X1, Y1],
        "w_in": round(w_pt/72, 5), "h_in": round(h_pt/72, 5)}
with open(ASSET.replace(".png", ".json"), "w") as f:
    json.dump(info, f, indent=1)
print(json.dumps(info))
