#!/usr/bin/env python3
"""Generate slide 007's measured one-vs-all classification diagram."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Rectangle

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_007_decision_boundary.png"
X0, X1, Y0, Y1 = 166, 798, 119, 507
W_IN = (X1 - X0) / 960 * 13.33
H_IN = (Y1 - Y0) / 540 * 7.5

fig = plt.figure(figsize=(W_IN, H_IN), dpi=200, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(X0, X1)
ax.set_ylim(Y1, Y0)
ax.axis("off")

red = "#C00000"
green = "#008000"
blue = "#0000FF"

red_line = np.array([[266, 202], [670, 475]], dtype=float)
green_line = np.array([[250, 380], [747, 215]], dtype=float)
blue_line = np.array([[377, 477], [690, 133]], dtype=float)


def y_on(line, x):
    (x0, y0), (x1, y1) = line
    return y0 + (x - x0) * (y1 - y0) / (x1 - x0)


def x_on(line, y):
    (x0, y0), (x1, y1) = line
    return x0 + (y - y0) * (x1 - x0) / (y1 - y0)


def clip(poly, inside, intersect):
    result = []
    for a, b in zip(poly, poly[1:] + poly[:1]):
        a_in, b_in = inside(a), inside(b)
        if a_in:
            result.append(a)
        if a_in != b_in:
            result.append(intersect(a, b))
    return result


def clip_y(poly, line, above):
    def inside(p):
        return p[1] <= y_on(line, p[0]) if above else p[1] >= y_on(line, p[0])

    def intersect(a, b):
        lo, hi = 0.0, 1.0
        for _ in range(50):
            mid = (lo + hi) / 2
            p = a + mid * (b - a)
            if inside(p) == inside(a):
                lo = mid
            else:
                hi = mid
        return a + ((lo + hi) / 2) * (b - a)

    return clip(poly, inside, intersect)


def clip_x(poly, line, left):
    def inside(p):
        return p[0] <= x_on(line, p[1]) if left else p[0] >= x_on(line, p[1])

    def intersect(a, b):
        lo, hi = 0.0, 1.0
        for _ in range(50):
            mid = (lo + hi) / 2
            p = a + mid * (b - a)
            if inside(p) == inside(a):
                lo = mid
            else:
                hi = mid
        return a + ((lo + hi) / 2) * (b - a)

    return clip(poly, inside, intersect)


panel = [np.array(p, dtype=float) for p in [[X0, Y0], [X1, Y0], [X1, Y1], [X0, Y1]]]
c1 = clip_x(clip_y(panel, green_line, True), blue_line, True)
c2 = clip_y(clip_x(clip_y(panel, green_line, False), blue_line, False), red_line, True)
c3 = clip_x(clip_y(clip_y(panel, red_line, False), green_line, False), blue_line, True)

for poly, face, edge, hatch in [
    (c1, "#F0F8F0", "#A9E0A9", "---"),
    (c2, "#F0F0FF", "#9A9AF0", "|||"),
    (c3, "#FDF0F0", "#E5A9A9", "---"),
]:
    ax.add_patch(Polygon(poly, closed=True, facecolor=face, edgecolor=edge,
                         linewidth=0.25, hatch=hatch, zorder=0))

ax.annotate("", xy=(292, 130), xytext=(292, 415),
            arrowprops=dict(arrowstyle="-|>", mutation_scale=14, color=red, lw=1.5), zorder=2)
ax.annotate("", xy=(635, 415), xytext=(292, 415),
            arrowprops=dict(arrowstyle="-|>", mutation_scale=14, color=red, lw=1.5), zorder=2)

for line, color in [(red_line, "#FF0000"), (green_line, green), (blue_line, blue)]:
    ax.plot(line[:, 0], line[:, 1], color=color, lw=2.0, zorder=2)

for xy, xytext, color in [
    ((500, 428), (525, 405), "#FF0000"),
    ((296, 310), (280, 330), green),
    ((630, 140), (610, 120), blue),
]:
    ax.annotate("", xy=xy, xytext=xytext,
                arrowprops=dict(arrowstyle="-|>", mutation_scale=20, color=color, lw=2.8), zorder=3)

points = {
    green: [(375, 165), (438, 165), (438, 208), (387, 250), (437, 250), (500, 240), (388, 280)],
    "#FF0000": [(355, 345), (323, 372), (348, 372), (323, 398), (355, 398)],
    "#1E2FC0": [(643, 297), (533, 340), (588, 340), (637, 340), (533, 370), (637, 370), (585, 380), (602, 390)],
}
for color, coords in points.items():
    xs, ys = zip(*coords)
    ax.scatter(xs, ys, s=230, c=color, edgecolors="none", zorder=4)

for x, y, color, rotation, label in [
    (269, 190, "#FF0000", -30, "d$_1$(x)"),
    (687, 208, green, 18, "d$_2$(x)"),
    (588, 152, blue, 55, "d$_3$(x)"),
]:
    ax.text(x, y, label, color=color, fontsize=14, style="italic",
            ha="center", va="center", rotation=rotation, zorder=5)

for x, y, label in [(655, 133, "+ve"), (270, 316, "+ve"), (513, 456, "+ve")]:
    ax.text(x, y, label, color="black", fontsize=14, fontweight="bold",
            ha="center", va="center", zorder=5)

for x, y, color, digit in [(498, 146, green, "1"), (565, 283, blue, "2"), (244, 374, red, "3")]:
    ax.add_patch(Rectangle((x, y), 35, 28, facecolor="#FFFF00", edgecolor="none", zorder=5))
    ax.text(x + 14, y + 14, "C", color=color, fontsize=19, fontweight="bold",
            ha="center", va="center", zorder=6)
    ax.text(x + 27, y + 19, digit, color="black", fontsize=12, fontweight="bold",
            ha="center", va="center", zorder=6)

fig.savefig(OUT, dpi=200, facecolor="white")
print(OUT)
