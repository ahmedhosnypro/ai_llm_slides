#!/usr/bin/env python3
"""Measured plot and perceptron panels for slide 011 (960x540 frame)."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, Polygon

OUT = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build")
DPI = 300
RED = "#990000"
NAVY = "#000080"
CYAN = "#00FFFF"
GREEN = "#93F63A"
BLUE = "#2A2AC8"


def panel(w, h, ox, oy):
    fig = plt.figure(figsize=(w / 72, h / 72), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.axis("off")
    return fig, ax, lambda x, y: (x - ox, y - oy)


def arrow(ax, p0, p1, color=RED, lw=1.8, head=8):
    ax.annotate("", xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=head), zorder=4)


# Decision plot: original panel x537..843, y109..370.
fig, ax, f = panel(307, 262, 537, 109)
ax.add_patch(Rectangle((0, 0), 307, 262, facecolor="white", edgecolor="none", zorder=0))
arrow(ax, f(618, 329), f(618, 125))
arrow(ax, f(618, 329), f(831, 329))
ax.plot(*zip(f(598, 171), f(731, 348)), color=NAVY, lw=3.2,
        solid_capstyle="butt", zorder=3)
for x, y, color in [(618, 328, CYAN), (618, 260, CYAN),
                    (699, 328, CYAN), (699, 260, GREEN)]:
    ax.add_patch(Circle(f(x, y), 9, facecolor=color, edgecolor="white", lw=.5, zorder=5))
ax.text(*f(600, 134), r"$x_2$", fontsize=10, color=RED, ha="center", va="center")
ax.text(*f(821, 339), r"$x_1$", fontsize=10, color=RED, ha="center", va="center")
ax.text(*f(600, 196), "2", fontsize=10, color=RED, ha="center", va="center")
ax.text(*f(710, 344), "1.2", fontsize=10, color=RED, ha="center", va="center")
fig.savefig(OUT / "plot_s011.png", dpi=DPI, facecolor="white")
plt.close(fig)

# Perceptron: original panel x142..513, y354..489.
fig, ax, p = panel(371, 135, 142, 354)
for y in (379, 418, 470):
    ax.plot(*zip(p(174, y), p(300, 420.5)), color="#C9C4C4", lw=.8, zorder=1)
ax.text(*p(166, 379), r"$x_1$", fontsize=9, color="black", ha="center", va="center")
ax.text(*p(166, 418), r"$x_2$", fontsize=9, color="black", ha="center", va="center")
ax.text(*p(166, 470), "1", fontsize=9, color="#E02B38", fontweight="bold", ha="center", va="center")
ax.text(*p(207, 372), "-5", fontsize=9, color=BLUE, ha="center", va="center")
ax.text(*p(207, 429), "-3", fontsize=9, color=BLUE, ha="center", va="center")
ax.text(*p(207, 472), "6", fontsize=9, color=BLUE, ha="center", va="center")
ax.add_patch(Polygon([p(292, 416), p(292, 426), p(299, 421)], closed=True,
                     facecolor=RED, edgecolor="none", zorder=5))
ax.add_patch(Circle(p(316, 420.5), 17, facecolor="#E4FFFA", edgecolor="#5FCFC0", lw=1.1, zorder=3))
ax.text(*p(316, 420.5), r"$\Sigma$", fontsize=16, color="black", ha="center", va="center", zorder=5)
arrow(ax, p(334, 420.5), p(360, 420.5), lw=1.4)
ax.add_patch(Rectangle(p(360, 405), 39, 31, facecolor="#FAE1FE", edgecolor="#E08FD8", lw=1.1, zorder=2))
ax.plot(*zip(p(380, 410), p(380, 430)), color=BLUE, lw=2.2, zorder=5)
ax.plot(*zip(p(380, 410), p(392, 410)), color=BLUE, lw=2.2, zorder=5)
ax.plot(*zip(p(368, 430), p(380, 430)), color=BLUE, lw=2.2, zorder=5)
sx, sy = p(344, 365)
ax.add_patch(FancyBboxPatch((sx, sy), 64, 31, boxstyle="round,pad=0,rounding_size=3",
                            facecolor="#FFFCE0", edgecolor="#E8E8B0", lw=.8, zorder=1))
ax.text(*p(376, 373), r">0 $\Rightarrow$ 1", fontsize=8, color="#808000", ha="center", va="center", zorder=5)
ax.text(*p(376, 386), r"$\leq$0 $\Rightarrow$ 0", fontsize=8, color="#808000", ha="center", va="center", zorder=5)
arrow(ax, p(402, 420.5), p(461, 420.5), lw=1.4)
ax.text(*p(473, 420.5), "O/P", fontsize=9, color="black", ha="left", va="center")
fig.savefig(OUT / "perceptron_s011.png", dpi=DPI, transparent=True)
plt.close(fig)
print("wrote plot_s011.png and perceptron_s011.png")
