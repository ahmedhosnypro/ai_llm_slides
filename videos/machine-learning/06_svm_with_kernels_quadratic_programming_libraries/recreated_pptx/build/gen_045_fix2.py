#!/usr/bin/env python3
"""Slide 045 plot fix2: green cluster as annulus around cyan core, blue as nonconvex two-lobe blob."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "045_055", "slide_045_plot_fix2.png")
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

def dot_grid(b, color, n=600, s=7):
    x0, y0, x1, y1 = to_data(b)
    ax.scatter(rng.uniform(x0, x1, n), rng.uniform(y0, y1, n), s=s, c=color)

def blob_path(cx, cy, w, h, wobble, seed):
    r = np.random.default_rng(seed)
    t = np.linspace(0, 2 * np.pi, 96, endpoint=False)
    a1, a2, a3 = r.uniform(0, 2 * np.pi, 3)
    f1, f2, f3 = r.uniform(0.5, 1.0, 3)
    rad = 1 + wobble * (f1 * np.sin(t + a1) + f2 * np.sin(2 * t + a2) + f3 * np.sin(3 * t + a3))
    x = cx + (w / 2) * rad * np.cos(t)
    y = cy + (h / 2) * rad * np.sin(t)
    verts = np.column_stack([np.append(x, x[0]), np.append(y, y[0])])
    codes = np.full(len(t) + 1, Path.LINETO)
    codes[0] = Path.MOVETO
    codes[-1] = Path.CLOSEPOLY
    return Path(verts, codes)

def blob(cx, cy, w, h, color, wobble=0.10, seed=1, alpha=0.9):
    ax.add_patch(PathPatch(blob_path(cx, cy, w, h, wobble, seed),
                           facecolor=color, edgecolor="none", alpha=alpha))

# four small-dot grid clusters
dot_grid([0.281, 0.250, 0.424, 0.528], "#000000")
dot_grid([0.409, 0.250, 0.515, 0.537], "#FF00FF")
dot_grid([0.513, 0.250, 0.719, 0.756], "#FF0000")
dot_grid([0.281, 0.528, 0.535, 0.756], "#90EE90")

# region blobs — measured from original frame (data coords):
# green outer bbox [0.344,0.546,0.482,0.731] -> center (16.9,8.8) w 13.0 h 8.0
# cyan core  bbox [0.396,0.611,0.445,0.685] -> center (17.6,8.4) w 4.6 h 3.2
# blue bbox    [0.559,0.380,0.658,0.537] -> center (35.3,16.6) w 9.3 h 6.8, two lobes
gx0, gy0, gx1, gy1 = to_data([0.344, 0.546, 0.482, 0.731])
cx0, cy0, cx1, cy1 = to_data([0.396, 0.611, 0.445, 0.685])
blob((gx0 + gx1) / 2, (gy0 + gy1) / 2, gx1 - gx0, gy1 - gy0, "#00FF00", wobble=0.10, seed=5)
blob((cx0 + cx1) / 2, (cy0 + cy1) / 2, cx1 - cx0, cy1 - cy0, "#00FFFF", wobble=0.08, seed=6)
bx0, by0, bx1, by1 = to_data([0.559, 0.380, 0.658, 0.537])
blob(bx0 + 0.30 * (bx1 - bx0), by0 + 0.42 * (by1 - by0), 0.62 * (bx1 - bx0), 0.95 * (by1 - by0), "#0000FF", wobble=0.12, seed=7)
blob(bx0 + 0.72 * (bx1 - bx0), by0 + 0.68 * (by1 - by0), 0.55 * (bx1 - bx0), 0.62 * (by1 - by0), "#0000FF", wobble=0.12, seed=8)

# large overlay dots
dot_grid([0.323, 0.315, 0.401, 0.491], "#000000", n=60, s=34)
dot_grid([0.422, 0.306, 0.490, 0.491], "#FF00FF", n=60, s=34)
dot_grid([0.513, 0.250, 0.719, 0.756], "#FF0000", n=120, s=34)

# tiny arrow toward blue blob
ax.annotate("", xy=(33.5, 18.5), xytext=(31.5, 20.5),
            arrowprops=dict(arrowstyle="->", color="#000000", lw=1.2))

fig.savefig(OUT, dpi=200, facecolor="white")
print("wrote", OUT)
