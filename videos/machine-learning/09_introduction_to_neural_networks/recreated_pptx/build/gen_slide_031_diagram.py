#!/usr/bin/env python3
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_W = 660 / 72
FIG_H = 192 / 72
DPI = 600

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.set_aspect("equal")
ax.axis("off")

RED = "#c00000"
GREEN = "#008000"
BLUE = "#0000ff"
BLACK = "#000000"
YELLOW = "#ffff66"
ORANGE = "#f4b183"

ax.add_patch(Rectangle((0, 0), FIG_W, FIG_H, facecolor="none", edgecolor=RED, linewidth=1.5, zorder=1))

input_x = (200 - 187) / 72
hidden_x = (423 - 187) / 72
output_x = (617 - 187) / 72
input_ys = [(249 - 134) / 72, (249 - 188) / 72]
hidden_ys = [(249 - 92) / 72, (249 - 161) / 72, (249 - 230) / 72]
output_ys = [(249 - 135) / 72, (249 - 189) / 72]

ax.text(input_x - 0.06, 2.208, "Input", ha="center", va="center", fontsize=10, color=BLUE, style="italic", fontweight="bold")
ax.text(hidden_x, 2.208, "Hidden", ha="center", va="center", fontsize=10, color=BLUE, style="italic", fontweight="bold")
ax.text(6.875, 2.208, "Output", ha="center", va="center", fontsize=10, color=BLUE, style="italic", fontweight="bold")
ax.text(8.194, 2.208, "Target", ha="center", va="center", fontsize=10, color=BLACK, fontweight="bold")

for y, label, value in zip(input_ys, ["x1", "x2"], ["7", "4"]):
    ax.text(input_x - 0.06, y, label, ha="right", va="center", fontsize=11, fontweight="bold", color=BLACK)
    ax.text(0.708, y, value, ha="center", va="center", fontsize=11, fontweight="bold", color=BLACK)

for x in [0.444, 0.875]:
    ax.plot([x, x], [0.639, 1.75], color=BLACK, linewidth=1.2, solid_capstyle="butt", zorder=4)

hidden_labels = ["O3=0.895", "O4=0.836", "O5=0.828"]
for y, label, out in zip(hidden_ys, ["3", "4", "5"], hidden_labels):
    ax.add_patch(Circle((hidden_x, y), 0.208, facecolor=YELLOW, edgecolor=BLACK, linewidth=1.2, zorder=5))
    ax.text(hidden_x, y, label, ha="center", va="center", fontsize=12, fontweight="bold", color=BLACK, zorder=6)
    ax.text(hidden_x + 0.125, y + 0.25, out, ha="left", va="bottom", fontsize=9, color=BLACK, zorder=6)

output_labels = ["O6=0.32", "O7=0.855"]
for y, label, out in zip(output_ys, ["6", "7"], output_labels):
    ax.add_patch(Circle((output_x, y), 0.208, facecolor=ORANGE, edgecolor=BLACK, linewidth=1.2, zorder=5))
    ax.text(output_x, y, label, ha="center", va="center", fontsize=12, fontweight="bold", color=BLACK, zorder=6)
    ax.text(output_x + 0.35, y + 0.12, out, ha="left", va="bottom", fontsize=9, color=BLACK, zorder=6)

w_ih = [[0.121, 0.405], [0.101, 0.305], [0.099, 0.295]]
for hi, hy in enumerate(hidden_ys):
    for ii, iy in enumerate(input_ys):
        ax.add_patch(FancyArrowPatch((0.95, iy), (hidden_x - 0.21, hy), arrowstyle="->", color=GREEN, linewidth=1.2, mutation_scale=9, zorder=3))
        ax.text((0.95 + hidden_x - 0.21) / 2, (iy + hy) / 2 + 0.04, f"{w_ih[hi][ii]:.3f}", ha="center", va="center", fontsize=8, fontweight="bold", color=GREEN, zorder=6)

w_ho = [[-0.399, 0.598], [-0.288, 0.696], [-0.187, 0.795]]
for hi, hy in enumerate(hidden_ys):
    for oi, oy in enumerate(output_ys):
        ax.add_patch(FancyArrowPatch((hidden_x + 0.21, hy), (output_x - 0.21, oy), arrowstyle="->", color=RED, linewidth=1.2, mutation_scale=9, zorder=3))
        ax.text((hidden_x + output_x) / 2, (hy + oy) / 2 + 0.04, f"{w_ho[hi][oi]:.3f}", ha="center", va="center", fontsize=8, fontweight="bold", color=RED, zorder=6)

for x in [7.819, 8.264]:
    ax.plot([x, x], [0.694, 1.875], color=BLACK, linewidth=1.2, solid_capstyle="butt", zorder=4)
ax.text(8.04, 1.597, "0", ha="center", va="center", fontsize=11, fontweight="bold", color=BLACK)
ax.text(8.04, 0.903, "1", ha="center", va="center", fontsize=11, fontweight="bold", color=BLACK)
ax.text(8.65, 1.556, "t6=0", ha="left", va="center", fontsize=9, fontweight="bold", color=BLACK)
ax.text(8.65, 0.903, "t7=1", ha="left", va="center", fontsize=9, fontweight="bold", color=BLACK)

out_png = os.path.join(OUT_DIR, "slide_031_nn_diagram.png")
fig.savefig(out_png, dpi=DPI, transparent=True)
plt.close(fig)

meta = {
    "image": "slide_031_nn_diagram.png",
    "width_in": FIG_W,
    "height_in": FIG_H,
    "dpi": DPI,
    "position": {"x": 187 / 72, "y": 58 / 72, "w": FIG_W, "h": FIG_H},
}
with open(os.path.join(OUT_DIR, "slide_031_nn_diagram.json"), "w") as f:
    json.dump(meta, f, indent=2)
print(out_png, FIG_W, FIG_H)
