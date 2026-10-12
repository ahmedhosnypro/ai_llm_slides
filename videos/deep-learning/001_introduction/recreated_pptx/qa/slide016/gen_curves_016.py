#!/usr/bin/env python3
"""Curved-stroke PNG for slide 016 (600dpi transparent, exact-size embed).
Same certified mechanism as qa/slide009/gen_curves_009.py (matplotlib cubic bezier
+ filled wedge head, 600dpi, transparent; embed at w/72,h/72 in).

Measured in unique_slides/slide_016.jpg (960x540, 1px=1pt=1/72in), qa/slide016/
measure_curve2.py + measure_head.py trace:
  - vertical stem at x96.5 from the ellipse boundary (~y178) down to ~y199,
  - bend right through (~98,205),(~100,212),(~102,219),(~104,224),(~107,228),
  - arrowhead wedge: tip at the SHIFTED Pre-processing left border (x129.5, y236),
    barbs back at (~119,230) / (~119,241)  (parent 009 head: tip (143,236.5),
    barbs (133,231.5)/(133,241.5) — the child box sits 15px further left).
Cubic fit checked at t=0.5 (101.6,218.1) vs measured (102,218) and t=0.75
(109,228) vs measured (107..108,228).
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
DPI = 600
RED = "#C00000"

def cubic(p0, p1, p2, p3, n=240):
    t = np.linspace(0, 1, n)[:, None]
    return ((1-t)**3 * np.array(p0) + 3*t*(1-t)**2 * np.array(p1)
            + 3*t**2*(1-t) * np.array(p2) + t**3 * np.array(p3))

def render(name, x0, y0, x1, y1, strokes, fills=()):
    w, h = x1 - x0, y1 - y0
    fig = plt.figure(figsize=(w/72, h/72), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x1); ax.set_ylim(y1, y0)
    ax.axis("off")
    for pts, lw, c in strokes:
        ax.plot(pts[:, 0], pts[:, 1], lw=lw, color=c, solid_capstyle="round")
    for poly, c in fills:
        ax.fill(poly[:, 0], poly[:, 1], color=c, lw=0)
    fig.savefig(f"{OUT}/{name}.png", transparent=True)
    plt.close(fig)
    side = {"name": name, "bbox": [x0, y0, x1, y1], "embed_w_in": w/72, "embed_h_in": h/72}
    with open(f"{OUT}/{name}.json", "w") as f:
        json.dump(side, f, indent=1)
    print(name, f"bbox=({x0},{y0})-({x1},{y1}) embedWH=({w/72:.4f},{h/72:.4f})in")

# curve 1 (slide 016): Training Data ellipse bottom -> left edge of the SHIFTED
# Pre processing box (outer border x129..236). trace: vertical drop (96.5,179)->
# (96.5,~200), bend right, into head back (119,235.5); wedge tip (129.5,236).
c1 = cubic((96.5, 179), (96.5, 213), (104, 227.5), (119, 235.5))
head1 = np.array([(129.5, 236), (119, 230), (119, 241)])
render("curve1_016", 91, 175, 133, 245, [(c1, 1.5, RED)], [(head1, RED)])
