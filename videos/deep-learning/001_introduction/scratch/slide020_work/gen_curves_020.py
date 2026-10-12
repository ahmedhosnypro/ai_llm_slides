#!/usr/bin/env python3
"""Curved-stroke PNGs for slide 020 (600dpi transparent, exact-size embed).
Pattern copied from certified qa/slide009/gen_curves_009.py.
Measured in 960x540 frame px (1px=1pt=1/72in). Canvas = curve bbox; embed at w/72,h/72 in.
Traces are PIL-measured from unique_slides/slide_020.jpg (scratch/slide020_work/measure4.py).
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
DPI = 600
BLUE = "#0C05A8"   # PIL cores #0800CF/#0300A6/#0900A7/#1C1484 -> #0C05A8
GREEN = "#1E8244"  # PIL core #1E8244 (vscan x772 y302-303)

def spline(pts, n=400):
    """Catmull-Rom through measured trace points -> dense polyline."""
    pts = np.array(pts, dtype=float)
    if len(pts) < 3:
        return pts
    # parametrize by cumulative chord length
    d = np.sqrt(((pts[1:] - pts[:-1]) ** 2).sum(axis=1))
    u = np.concatenate([[0], np.cumsum(d)])
    ui = np.linspace(0, u[-1], n)
    out = np.stack([np.interp(ui, u, pts[:, i]) for i in range(2)], axis=1)
    return out

def render(name, x0, y0, x1, y1, strokes, fills=()):
    w, h = x1 - x0, y1 - y0
    fig = plt.figure(figsize=(w/72, h/72), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x1); ax.set_ylim(y1, y0)
    ax.axis("off")
    for pts, lw, c, ls in strokes:
        ax.plot(pts[:, 0], pts[:, 1], lw=lw, color=c, linestyle=ls,
                solid_capstyle="round", dash_capstyle="round")
    for poly, c in fills:
        ax.fill(poly[:, 0], poly[:, 1], color=c, lw=0)
    fig.savefig(f"{OUT}/{name}.png", transparent=True)
    plt.close(fig)
    side = {"name": name, "bbox": [x0, y0, x1, y1], "embed_w_in": w/72, "embed_h_in": h/72}
    with open(f"{OUT}/{name}.json", "w") as f:
        json.dump(side, f, indent=1)
    print(name, f"bbox=({x0},{y0})-({x1},{y1}) embedWH=({w/72:.4f},{h/72:.4f})in")

# ---- arc_left: solid blue, ellipse left dot (368,135) -> down into Input Samples top.
# PIL trace: (368,135)(292,136)(239,140)(209,145)(190,150)(174,155)(160,160)(151,165)
#   (143,170)(136,175)(131,180)(127,185)(124,190)(123,195); head ink x116..125 y200..209,
# apex (120,211) touching box top border y212.
arc_left = spline([(368,135),(292,136),(239,140),(209,145),(190,150),(174,155),(160,160),
                   (151,165),(143,170),(136,175),(131,180),(127,185),(124,190),(123,195),
                   (120,201)])
headL = np.array([(120,211),(113.5,200.5),(126.5,200.5)])
render("arc_left_020", 108, 128, 374, 216, [(arc_left, 2.6, BLUE, "solid")], [(headL, BLUE)])

# ---- arc_right: dotted blue, ellipse right dot (474,135) -> right, over the error box,
# down into Samples Labels top. PIL trace: (479,135)(536,135)(572,137)(620,140)(676,143)
#   (716,146)(723,149)(760,155)(801,167)(814,173)(825,180)(836,190)(841,194); head ink
# x839..849 y198..209, apex (844,210) touching box top y212.
arc_right = spline([(474,135),(500,135),(536,135),(572,137),(620,140),(676,143),(716,146),
                    (723,149),(760,155),(801,167),(814,173),(825,180),(836,190),(841,195),
                    (844,200)])
headR = np.array([(844,211),(837.5,200.5),(850.5,200.5)])
render("arc_right_020", 468, 128, 856, 216,
       [(arc_right, 2.6, BLUE, (0, (1.8, 4.6)))], [(headR, BLUE)])

# ---- green feedback fan: stem from Prediction Error box bottom (769,298), four dashed
# curves up into the box bottoms, arrowhead apexes at y262 (box borders y263..265).
# PIL traces (measure4.py green rows).
stem = spline([(769,297),(759,305),(750,311),(720,315),(690,318),(655,321),(620,323)])
c_pre   = spline([(243,275),(252,281),(264,290),(282,296),(300,302),(331,308),(372,314),
                  (430,320),(510,323)])
c_ext   = spline([(365,275),(380,290),(397,299),(416,305),(443,311),(483,317),(550,322),
                  (585,323)])
c_sel   = spline([(471,278),(488,293),(504,302),(525,311),(556,317),(600,322),(625,323)])
c_cls   = spline([(581,275),(597,299),(614,311),(632,317),(660,322),(680,323)])
def head(x):
    return np.array([(x,261.5),(x-4.5,274),(x+4.5,274)])
green_strokes = [(stem, 1.8, GREEN, (0, (5, 4)))]
for c in (c_pre, c_ext, c_sel, c_cls):
    green_strokes.append((c, 1.8, GREEN, (0, (5, 4))))
green_fills = [(head(243), GREEN), (head(365), GREEN), (head(471), GREEN), (head(581), GREEN)]
render("green_fan_020", 232, 256, 782, 330, green_strokes, green_fills)
