"""Scatter plot for slide 046 - Perceptron Iteration 4 (decision boundary + classified points).

Geometry measured from unique_slides/slide_046.jpg (960x540, 1px = 1pt) via PIL:
  plot frame (red border): interior x 315..822, y 176..478  -> 507 x 302 frame px
  x axis: tick n at frame x = 362.5 + 52.6875*n   (n = 0..8), tick bottom at y=447
  y axis: tick n at frame y = 428.5 - 30.5625*n   (n = 0..7), tick right at x=356
  tick marks: 11 px (measured ~10-11 px), 1.3 pt black
  tick number ink: cap-top y429.5 (bottom row) / y421 (upper row), right edge x356,
                   mid-digit centres on the tick axis; ~7.3 pt bold (measured cap 8 px)
  decision line: vertical red at data x = 3.5 (measured core x544-547 -> data 3.478; no
                 such line in the slide deck's other frames at 3.0), full interior height
  markers (measured centres -> data):
      blue squares   (1,2) (1,1) (2,1)      ~13x13 px -> 4.3 pt, marker edge on the point
      magenta diamonds (6,6) (6,5) (5,4)    ~9x9 px  -> 3.0 pt, point on the vertex
      red triangles  (7,6) (3,2) (0,0)      ~9x8 px   -> 3.0 pt, point on the centroid
  "+ve" annotation near the top of the decision line: black bold text + 21 px black
      left-pointing arrow whose rounded tip lands on the red line at frame (546, 219).
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

OUT = os.path.join(os.path.dirname(__file__), "assets", "plot_046_scatter.png")
DPI = 600
# interior rect in frame px (the red border box: x 312..824, y 173..481 incl. the
# tick marks + labels that sit just inside its right/bottom edges)
X0, X1 = 312, 825
Y0, Y1 = 173, 482
W = (X1 - X0 + 1) / 72.0
H = (Y1 - Y0 + 1) / 72.0

fig = plt.figure(figsize=(W, H), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(X0, X1 + 1)
ax.set_ylim(Y1 + 1, Y0)
ax.axis("off")
fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)


def dx(data_x):
    return 362.5 + 52.6875 * data_x


def dy(data_y):
    return 428.5 - 30.5625 * data_y


# ---- measured data points -------------------------------------------------
BLUE = (0.0, 0.0, 1.0)        # #0000FF
RED = (1.0, 0.0, 0.0)         # #FF0000
MAGENTA = (1.0, 0.0, 1.0)     # #FF00FF

ax.plot([dx(3.5), dx(3.5)], [Y0, Y1], color=RED, lw=1.3, solid_capstyle="butt", zorder=2)
ax.plot([X0, X1], [Y0, Y0], color=RED, lw=1.3, solid_capstyle="butt", zorder=3)
ax.plot([X0, X0], [Y0, Y1], color=RED, lw=1.3, solid_capstyle="butt", zorder=3)
ax.plot([X0, X1], [Y1, Y1], color=RED, lw=1.3, solid_capstyle="butt", zorder=3)
ax.plot([X1, X1], [Y0, Y1], color=RED, lw=1.3, solid_capstyle="butt", zorder=3)

# squares: pix (1,2)(1,1)(2,1)
for (px_, py_) in [(1, 2), (1, 1), (2, 1)]:
    ax.add_patch(plt.Rectangle((dx(px_) - 6.5, dy(py_) - 6.5), 13, 13,
                               facecolor=BLUE, edgecolor="none", zorder=5))
# diamonds: (6,6)(6,5)(5,4)
diam = plt.Polygon
for (px_, py_) in [(6, 6), (6, 5), (5, 4)]:
    ax.add_patch(plt.Polygon([(dx(px_), dy(py_) - 4.5), (dx(px_) + 4.5, dy(py_)),
                               (dx(px_), dy(py_) + 4.5), (dx(px_) - 4.5, dy(py_))],
                              closed=True, facecolor=MAGENTA, edgecolor="none", zorder=5))
# triangles: (7,6)(3,2)(0,0)
for (px_, py_) in [(7, 6), (3, 2), (0, 0)]:
    ax.add_patch(plt.Polygon([(dx(px_), dy(py_) - 3.5), (dx(px_) + 4.3, dy(py_) + 4.0),
                               (dx(px_) - 4.3, dy(py_) + 4.0)],
                              closed=True, facecolor=RED, edgecolor="none", zorder=5))

# ---- ticks (measured: inside the plot box's bottom/right edge) -------------
# x-axis: tick marks 2 px tall just above the bottom border row (frame y 444..445),
# digit caps 437..444 (baseline ~444). y-axis: marks left of the left border (frame
# x 340..341), digits x 350..354 centred on the tick row.
for n in range(9):
    ax.plot([dx(n), dx(n)], [Y1 - 6, Y1 - 1], color="black", lw=1.0, zorder=6)
for n in range(8):
    ax.plot([X0 + 1, X0 + 6], [dy(n), dy(n)], color="black", lw=1.0, zorder=6)

for n in range(9):
    ax.text(dx(n) + 0.6, Y1 - 4.0, str(n), ha="center", va="baseline",
            fontsize=7.3, fontweight="bold", color="black", zorder=6)
for n in range(8):
    ax.text(X0 + 15.0, dy(n) + 2.6, str(n), ha="center", va="baseline",
            fontsize=7.3, fontweight="bold", color="black", zorder=6)

# ---- "+ve" + arrow --------------------------------------------------------
ax.text(505, 202, "+ve", ha="right", va="baseline", fontsize=10,
        fontweight="bold", color="black", zorder=7)
ax.annotate("", xy=(546.5, 219), xytext=(526, 217.5),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.6,
                            shrinkA=0, shrinkB=0,
                            mutation_scale=13), zorder=7)

fig.savefig(OUT, dpi=DPI, transparent=True, pad_inches=0)
print("wrote", OUT)
