#!/usr/bin/env python3
"""Slide 045 plot rebuilt from final JSON: rectangular dot-grid clusters + blobs."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "045_055", "slide_045_plot.png")
rng = np.random.default_rng(11)

# chart bbox normalized, data ranges
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

# four small-dot grid clusters
dot_grid([0.281, 0.250, 0.424, 0.528], "#000000")
dot_grid([0.409, 0.250, 0.515, 0.537], "#FF00FF")
dot_grid([0.513, 0.250, 0.719, 0.756], "#FF0000")
dot_grid([0.281, 0.528, 0.535, 0.756], "#90EE90")

# region blobs
def blob(b, color):
    x0, y0, x1, y1 = to_data(b)
    ax.add_patch(Ellipse(((x0+x1)/2, (y0+y1)/2), x1-x0, y1-y0, facecolor=color, edgecolor="none", alpha=0.9))
blob([0.559, 0.380, 0.658, 0.537], "#0000FF")
blob([0.344, 0.546, 0.482, 0.731], "#00FF00")
blob([0.396, 0.611, 0.445, 0.685], "#00FFFF")

# large overlay dots
dot_grid([0.323, 0.315, 0.401, 0.491], "#000000", n=60, s=34)
dot_grid([0.422, 0.306, 0.490, 0.491], "#FF00FF", n=60, s=34)
dot_grid([0.513, 0.250, 0.719, 0.756], "#FF0000", n=120, s=34)

# tiny arrow toward blue blob
ax.annotate("", xy=(33.5, 18.5), xytext=(31.5, 20.5),
            arrowprops=dict(arrowstyle="->", color="#000000", lw=1.2))

fig.savefig(OUT, dpi=200, facecolor="white")
print("wrote", OUT)
