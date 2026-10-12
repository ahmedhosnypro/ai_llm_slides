#!/usr/bin/env python3
"""Curved-stroke PNGs for slide 018 (600dpi transparent, exact-size embed).
Certified slide_009/020 pattern (gen_curves_009.py). Measured in 960x540 frame px
(1px=1pt=1/72in). Canvas = stroke bbox; embed at w/72,h/72 in.

curve1_018: Training Data ellipse bottom-left -> left edge of Pre processing.
  trace: (96.5,188) vertical drop, bend right, flat into head tip (130,236.5)
  (slide 018's Pre processing box sits at x130..237 vs parent's 145.5..250.5).
arc_018: dashed navy double-headed arc Training Data -> Classifier Output top.
  trace: (215,158) flat to ~x500, sag to (789,192.5), head dives to (801,206).
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
DPI = 600
RED = "#C00000"
NAVY = "#000080"

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
    for pts, lw, c, ls in strokes:
        ax.plot(pts[:, 0], pts[:, 1], lw=lw, color=c, linestyle=ls, solid_capstyle="round")
    for poly, c in fills:
        ax.fill(poly[:, 0], poly[:, 1], color=c, lw=0)
    fig.savefig(f"{OUT}/{name}.png", transparent=True)
    plt.close(fig)
    side = {"name": name, "bbox": [x0, y0, x1, y1], "embed_w_in": w/72, "embed_h_in": h/72}
    with open(f"{OUT}/{name}.json", "w") as f:
        json.dump(side, f, indent=1)
    print(name, f"bbox=({x0},{y0})-({x1},{y1}) embedWH=({w/72:.4f},{h/72:.4f})in")

# curve 1 (solid red, matches parent curve1 style): ellipse bottom -> Pre processing left edge
c1 = cubic((96.5, 188), (96.5, 215), (103, 236.5), (118, 236.5))
head1 = np.array([(130, 236.5), (120, 231.5), (120, 241.5)])
render("curve1_018", 90, 183, 134, 247, [(c1, 1.5, RED, "-")], [(head1, RED)])

# navy dashed arc: Training Data right edge -> top of Classifier Output (double-headed)
arc = cubic((215, 158), (450, 157.5), (745, 174), (796, 196))
headL = np.array([(212, 158), (223, 152.5), (223, 163.5)])   # left head, points LEFT
headR = np.array([(801.5, 207), (791.5, 194.5), (803.5, 193.5)])  # right head, dives DOWN
render("arc_018", 208, 149, 807, 212, [(arc, 1.4, NAVY, (0, (5, 4)))],
       [(headL, NAVY), (headR, NAVY)])
