#!/usr/bin/env python3
"""Measured panel images for slide 014 (960x540 frame, 1 px = 1 pt)."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, FancyArrowPatch

OUT = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build")
DPI = 300
RED = "#C00000"
BRIGHT_RED = "#E02020"
GREEN = "#008000"
BLUE = "#0000C0"
GRAY = "#D0D0D0"
MINT = "#E4FFFA"
MINT_EDGE = "#A0D8D0"
PINK = "#F5E1FA"
PINK_EDGE = "#D8B4E2"


def panel(w, h):
    fig = plt.figure(figsize=(w / 72, h / 72), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.axis("off")
    return fig, ax


def arrow(ax, p0, p1, color, lw=1.2, head=7):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=color, lw=lw,
            solid_capstyle="butt", zorder=2)
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    n = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / n, dy / n
    px, py = -uy, ux
    tip = p1
    base = (p1[0] - ux * head, p1[1] - uy * head)
    ax.add_patch(Polygon([tip, (base[0] + px * head * .42, base[1] + py * head * .42),
                          (base[0] - px * head * .42, base[1] - py * head * .42)],
                         closed=True, facecolor=color, edgecolor="none", zorder=3))


def neuron(ax, x, y, number=None, number_pos=None):
    ax.add_patch(Circle((x, y), 16, facecolor=MINT, edgecolor=MINT_EDGE, lw=1.2, zorder=4))
    ax.text(x, y, r"$\Sigma$", fontsize=17, color="black", ha="center", va="center", zorder=5)
    if number is not None:
        nx, ny = number_pos
        ax.add_patch(Circle((nx, ny), 10, facecolor=RED, edgecolor="none", zorder=6))
        ax.text(nx, ny, str(number), fontsize=10, color="white", fontweight="bold",
                ha="center", va="center", zorder=7)


def step_box(ax, x, y, w=40, h=30):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=PINK, edgecolor=PINK_EDGE, lw=1.2, zorder=4))
    cx = x + w * .48
    ax.plot([cx, cx], [y + 6, y + h - 6], color=BLUE, lw=1.8, zorder=5)
    ax.plot([cx, x + w - 7], [y + 6, y + 6], color=BLUE, lw=1.8, zorder=5)
    ax.plot([x + 7, cx], [y + h - 6, y + h - 6], color=BLUE, lw=1.8, zorder=5)


# Main panel: original frame x83..553, y100..305 (470x205).
fig, ax = panel(470, 205)
ax.text(29, 74, r"$x_1$", fontsize=10, color="black", ha="center", va="center")
ax.text(29, 154, r"$x_2$", fontsize=10, color="black", ha="center", va="center")
arrow(ax, (40, 72), (158, 45), GRAY, 1.0)
arrow(ax, (40, 152), (158, 50), GRAY, 1.0)
arrow(ax, (40, 78), (158, 165), GRAY, 1.0)
arrow(ax, (40, 156), (158, 170), GRAY, 1.0)
# Colored arrowheads at the neuron rims.
arrow(ax, (150, 47), (159, 45), BRIGHT_RED, 1.0, 6)
arrow(ax, (150, 52), (159, 49), BRIGHT_RED, 1.0, 6)
arrow(ax, (150, 162), (159, 165), BLUE, 1.0, 6)
arrow(ax, (150, 169), (159, 170), BLUE, 1.0, 6)
neuron(ax, 175, 45, 1, (202, 17))
neuron(ax, 175, 170, 2, (202, 185))
neuron(ax, 277, 110, 3, (277, 140))
arrow(ax, (191, 50), (261, 105), GREEN, 1.4)
arrow(ax, (191, 165), (261, 115), GREEN, 1.4)
ax.text(97, 35, r"$w_{11}$", fontsize=9, color=RED, style="italic", ha="center", va="center")
ax.text(97, 85, r"$w_{12}$", fontsize=9, color=RED, style="italic", ha="center", va="center")
ax.text(97, 135, r"$w_{21}$", fontsize=9, color=BLUE, style="italic", ha="center", va="center")
ax.text(97, 170, r"$w_{22}$", fontsize=9, color=BLUE, style="italic", ha="center", va="center")
ax.text(232, 70, r"$w_{31}$", fontsize=9, color=GREEN, style="italic", ha="center", va="center")
ax.text(232, 150, r"$w_{32}$", fontsize=9, color=GREEN, style="italic", ha="center", va="center")
arrow(ax, (293, 110), (342, 110), BRIGHT_RED, 1.4)
step_box(ax, 347, 95)
arrow(ax, (387, 110), (412, 110), BRIGHT_RED, 1.4)
ax.text(418, 110, "O/P", fontsize=10, color="black", fontweight="bold", ha="left", va="center")
ax.text(337, 48, r">0 $\Rightarrow$ 1", fontsize=7, color="#008000", ha="center", va="center")
ax.text(337, 62, r"$\leq$0 $\Rightarrow$ 0", fontsize=7, color="#808000", ha="center", va="center")
fig.savefig(OUT / "slide_014_main_diagram.png", dpi=DPI, transparent=True)
plt.close(fig)

# Small panel: original frame x607..891, y337..462 (284x125).
fig, ax = panel(284, 125)
ax.text(28, 38, r"$x_1$", fontsize=9, color="black", ha="center", va="center")
ax.text(28, 78, r"$x_2$", fontsize=9, color="black", ha="center", va="center")
arrow(ax, (38, 40), (99, 58), GREEN, 1.2)
arrow(ax, (38, 76), (99, 62), GREEN, 1.2)
ax.text(63, 28, r"$w'_1$", fontsize=9, color=GREEN, style="italic", ha="center", va="center")
ax.text(63, 82, r"$w'_2$", fontsize=9, color=GREEN, style="italic", ha="center", va="center")
neuron(ax, 113, 60)
arrow(ax, (129, 60), (163, 60), BRIGHT_RED, 1.3)
step_box(ax, 163, 45)
arrow(ax, (203, 60), (228, 60), BRIGHT_RED, 1.3)
ax.text(228, 60, "O/P", fontsize=9, color="black", fontweight="bold", ha="left", va="center")
fig.savefig(OUT / "slide_014_small_diagram.png", dpi=DPI, transparent=True)
plt.close(fig)
print("wrote measured slide 014 panel images")
