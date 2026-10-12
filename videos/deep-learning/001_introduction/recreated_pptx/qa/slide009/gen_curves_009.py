#!/usr/bin/env python3
"""Curved-stroke PNGs for slide 009 (600dpi transparent, exact-size embed).
Measured in 960x540 frame px (1px=1pt=1/72in). Canvas = curve bbox; embed at w/72,h/72 in."""
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

# curve 1: Training Data ellipse bottom -> left edge of Pre processing.
# trace: vertical drop (96.5,188)->(96.5,208), bend right, flat into head at y236.5
c1 = cubic((96.5, 188), (96.5, 220), (110, 236.5), (132, 236.5))
head1 = np.array([(143, 236.5), (133, 231.5), (133, 241.5)])
render("curve1_009", 90, 183, 148, 247, [(c1, 1.5, RED)], [(head1, RED)])

# curve 2: right edge of Post processing -> top of Final Result ellipse.
# trace: (866,236)->(880,250)->(880,262)->(872,272)->(852,284)->(840,293); head tip (831,306)
c2 = cubic((867, 237), (895, 260), (880, 283), (842, 293))
head2 = np.array([(829.5, 307), (843, 297), (839.5, 290)])
render("curve2_009", 824, 230, 890, 312, [(c2, 1.5, RED)], [(head2, RED)])
