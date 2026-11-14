#!/usr/bin/env python3
"""Slide 045 plot fix3: lattice dot grids, true hollow green annulus with small cyan core, single peanut blue blob."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "045_055", "slide_045_plot_fix3.png")
rng = np.random.default_rng(11)

CX0, CY0, CX1, CY1 = 0.234, 0.148, 0.764, 0.841
XLIM, YLIM = (0, 50), (0, 30)

def to_data(b):
    x0, y0, x1, y1 = b
    dx0 = (x0 - CX0) / (CX1 - CX0) * XLIM[1]
    dx1 = (x1 - CX0) / (CX1 - CX0) * XLIM[1]
    dy0 = YLIM[1] - (y1 - CY0) / (CY1 - CY0) * YLIM[1]
    dy1 = YLIM[1] - (y0 - CY0) / (CY1 - CY0) * YLIM[1]
    return dx0, dy0, dx1, dy1

fig = plt.figure(figsize=(0.530 * 13.33, 0.693 * 7.5), dpi=200)
ax = fig.add_axes([0.13, 0.11, 0.84, 0.84])
ax.set_xlim(*XLIM); ax.set_ylim(*YLIM)
ax.set_xticks([0, 10, 20, 30, 40, 50])
ax.set_yticks([0, 5, 10, 15, 20, 25, 30])
ax.set_facecolor("white")
ax.grid(True, color="#808080", linewidth=0.6, linestyle=":")
for s in ax.spines.values():
    s.set_color("#000000"); s.set_linewidth(1.2)
ax.tick_params(colors="#000000", labelsize=9)

def dot_grid(b, color, nx=25, ny=24, s=7):
    x0, y0, x1, y1 = to_data(b)
    xs = np.linspace(x0, x1, nx)
    ys = np.linspace(y0, y1, ny)
    gx, gy = np.meshgrid(xs, ys)
    ax.scatter(gx.ravel(), gy.ravel(), s=s, c=color)

def ring_path(cx, cy, w, h, hole_w, hole_h, wobble, seed):
    r = np.random.default_rng(seed)
    t = np.linspace(0, 2 * np.pi, 96, endpoint=False)
    a1, a2 = r.uniform(0, 2 * np.pi, 2)
    rad = 1 + wobble * (0.6 * np.sin(t + a1) + 0.4 * np.sin(2 * t + a2))
    xo = cx + (w / 2) * rad * np.cos(t)
    yo = cy + (h / 2) * rad * np.sin(t)
    xi = cx + (hole_w / 2) * np.cos(t)
    yi = cy + (hole_h / 2) * np.sin(t)
    verts = np.concatenate([np.column_stack([np.append(xo, xo[0]), np.append(yo, yo[0])]),
                            np.column_stack([np.append(xi[::-1], xi[-1]), np.append(yi[::-1], yi[-1])])])
    codes = np.concatenate([np.full(97, Path.LINETO), np.full(97, Path.LINETO)])
    codes[0] = Path.MOVETO; codes[96] = Path.CLOSEPOLY
    codes[97] = Path.MOVETO; codes[193] = Path.CLOSEPOLY
    return Path(verts, codes)

def blob_path(cx, cy, w, h, wobble, seed, h2=0.0, a2=0.0):
    t = np.linspace(0, 2 * np.pi, 96, endpoint=False)
    r = np.random.default_rng(seed)
    a1 = r.uniform(0, 2 * np.pi)
    rad = 1 + wobble * np.sin(t + a1) + h2 * np.sin(2 * t + a2)
    x = cx + (w / 2) * rad * np.cos(t)
    y = cy + (h / 2) * rad * np.sin(t)
    verts = np.column_stack([np.append(x, x[0]), np.append(y, y[0])])
    codes = np.full(97, Path.LINETO)
    codes[0] = Path.MOVETO; codes[-1] = Path.CLOSEPOLY
    return Path(verts, codes)

def blob(cx, cy, w, h, color, wobble=0.10, seed=1, h2=0.0, a2=0.0, alpha=0.9):
    ax.add_patch(PathPatch(blob_path(cx, cy, w, h, wobble, seed, h2, a2),
                           facecolor=color, edgecolor="none", alpha=alpha))

# four small-dot lattice clusters
dot_grid([0.281, 0.250, 0.424, 0.528], "#000000", nx=25, ny=24)
dot_grid([0.409, 0.250, 0.515, 0.537], "#FF00FF", nx=11, ny=24)
dot_grid([0.513, 0.250, 0.719, 0.756], "#FF0000", nx=21, ny=44)
dot_grid([0.281, 0.528, 0.535, 0.756], "#90EE90", nx=25, ny=24)

# region blobs — measured from original frame (data coords)
gx0, gy0, gx1, gy1 = to_data([0.344, 0.546, 0.482, 0.731])
cx0, cy0, cx1, cy1 = to_data([0.396, 0.611, 0.445, 0.685])
gcx, gcy = (gx0 + gx1) / 2, (gy0 + gy1) / 2
# hollow green annulus: outer w13.0 h8.0, hole w4.6 h3.4 (pale-green lattice shows through)
ax.add_patch(PathPatch(ring_path(gcx, gcy, gx1 - gx0, gy1 - gy0, 4.6, 3.4, 0.08, 5),
                       facecolor="#00FF00", edgecolor="none", alpha=0.9))
# small cyan core inside the hole
blob((cx0 + cx1) / 2, (cy0 + cy1) / 2, 3.3, 2.3, "#00FFFF", wobble=0.06, seed=6)
# blue: single connected peanut (nonconvex) blob
bx0, by0, bx1, by1 = to_data([0.559, 0.380, 0.658, 0.537])
blob((bx0 + bx1) / 2, (by0 + by1) / 2, bx1 - bx0, by1 - by0, "#0000FF",
     wobble=0.10, seed=7, h2=0.22, a2=0.9)

# large overlay dots on lattices
dot_grid([0.323, 0.315, 0.401, 0.491], "#000000", nx=6, ny=5, s=34)
dot_grid([0.422, 0.306, 0.490, 0.491], "#FF00FF", nx=6, ny=5, s=34)
dot_grid([0.513, 0.250, 0.719, 0.756], "#FF0000", nx=10, ny=8, s=34)

# tiny arrow toward blue blob
ax.annotate("", xy=(33.5, 18.5), xytext=(31.5, 20.5),
            arrowprops=dict(arrowstyle="->", color="#000000", lw=1.2))

fig.savefig(OUT, dpi=200, facecolor="white")
print("wrote", OUT)
