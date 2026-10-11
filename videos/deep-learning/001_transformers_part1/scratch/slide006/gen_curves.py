#!/usr/bin/env python3
"""Generate the curved-stroke PNGs for slide 006 (600 dpi transparent, exact-size embed).
Curves are measured in 960x540 frame px (1px = 1pt = 1/72in). Canvas = curve bbox (padded),
drawn in px units, saved at 600dpi -> device px = 72space_px * 600/72; embed at w/72 in.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets"
DPI = 600
DEC_INK = "#9EA828"
RED = "#A0000E"

def quad(p0, p1, p2, n=160):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * np.array(p0) + 2 * t * (1 - t) * np.array(p1) + t ** 2 * np.array(p2)

def render(name, x0, y0, x1, y1, strokes, fills=()):
    """strokes: list of (Nx2 px-array, lw_pt, color). fills: list of (Mx2 poly, color)."""
    w, h = x1 - x0, y1 - y0
    fig = plt.figure(figsize=(w / 72, h / 72), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x1); ax.set_ylim(y1, y0)  # y down
    ax.axis("off")
    for pts, lw, c in strokes:
        ax.plot(pts[:, 0], pts[:, 1], lw=lw, color=c, solid_capstyle="round")
    for poly, c in fills:
        ax.fill(poly[:, 0], poly[:, 1], color=c, lw=0)
    fig.savefig(f"{OUT}/{name}.png", transparent=True)
    plt.close(fig)
    print(name, f"bbox=({x0},{y0})-({x1},{y1}) embedWH=({w/72:.4f},{h/72:.4f})in")

# decoder recurrent curve A: quad (556,197) ctrl (564,160) end (645,255)
render("curve_a", 550, 183, 651, 259,
       [(quad((556, 197), (564, 160), (645, 255)), 2.0, DEC_INK)])
# curve B = A + 131px in x
render("curve_b", 681, 183, 782, 259,
       [(quad((687, 197), (695, 160), (776, 255)), 2.0, DEC_INK)])
# context arc: quad (469,326) ctrl (471,295) end (497,264) + right-pointing head wedge
arc = quad((469, 326), (471, 295), (497, 264))
head = np.array([(496, 260.5), (508.5, 263.5), (496, 266.5)])
render("ctx_arc", 464, 257, 512, 330,
       [(arc, 2.0, RED)], [(head, RED)])
