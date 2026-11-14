#!/usr/bin/env python3
"""Generate the slide 028 neural-network architecture diagram in slide coordinates."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch
import numpy as np

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_028_nn_model_v2.png"
fig = plt.figure(figsize=(13.333333, 7.5), dpi=300)
fig.patch.set_alpha(0)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 960)
ax.set_ylim(540, 0)
ax.axis("off")
ax.set_facecolor("none")

PURPLE = "#b060b0"
RED = "#c00000"
BLUE = "#0000c0"
GREEN = "#2e8b57"


def box(x, y, w, h, fill, edge, lw=0.8):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge, lw=lw))


def neuron(cx, cy, fill, edge):
    r = 17
    ax.add_patch(Circle((cx, cy), r, facecolor=fill, edgecolor=edge, lw=0.9))
    ax.plot([cx, cx], [cy - r, cy + r], color=edge, lw=0.6)
    ax.text(cx - 8, cy + 1, r"$\Sigma$", fontsize=15, ha="center", va="center", color="black")
    t = np.linspace(-2, 2, 60)
    xs = cx + 2 + 12 * (t + 2) / 4
    ys = cy - 8 * np.tanh(t)
    ax.plot(xs, ys, color="black", lw=0.9)


# Input/target labels and dashed sample/target line.
box(68, 126, 58, 27, "#e7a8e7", PURPLE)
ax.text(97, 139.5, "Input\nSample", fontsize=7.5, ha="center", va="center", color="black")
box(824, 126, 64, 27, "#e7a8e7", PURPLE)
ax.text(856, 139.5, "Target\nLabel", fontsize=7.5, ha="center", va="center", color="black")
ax.add_patch(FancyArrowPatch((126, 139), (824, 139), arrowstyle="<->",
                             mutation_scale=8, lw=0.8, linestyle="--", color=PURPLE))

# Main network panel.
box(66, 166, 721, 253, "#e7dfd4", "#999999", 0.8)
for x in (128, 646):
    ax.plot([x, x], [166, 419], color="#777777", lw=0.7, ls="--")

rows = [211, 285, 360]
for y in (255, 278, 301, 324):
    ax.add_patch(Circle((78, y), 4, facecolor=PURPLE, edgecolor=PURPLE))
    for ny in rows:
        ax.plot([82, 143], [y, ny], color="#b8b8b8", lw=0.35, alpha=0.55)

# Five visual columns: unlabeled first column, then Net_i, Net_j, Net_k, output.
for a in rows:
    for b in rows:
        ax.plot([177, 233], [a, b], color="#b8b8b8", lw=0.4, alpha=0.6)
        ax.plot([267, 403], [a, b], color=RED, lw=0.55, alpha=0.7)
        ax.plot([437, 563], [a, b], color=RED, lw=0.55, alpha=0.7)
        ax.plot([597, 653], [a, b], color="#b8b8b8", lw=0.4, alpha=0.6)

for y in rows:
    neuron(160, y, "#f4f4f4", "#777777")
    neuron(250, y, "#e8f0f8", "#7080a0")
    neuron(420, y, "#d8f8c8", "#70a070")
    neuron(580, y, "#ffe0b8", "#c09060")
    neuron(670, y, "#f4f4f4", "#777777")
    for x in (190, 205, 220, 615, 630, 645):
        ax.add_patch(Circle((x, y), 2, facecolor="#888888", edgecolor="#888888"))
    for x in (267, 437, 597):
        ax.add_patch(Circle((x, y), 3, facecolor=RED, edgecolor=RED))

for x, label in ((200, "i"), (380, "j"), (540, "k")):
    ax.text(x, 183, rf"$Net_{label}$", fontsize=15, color=RED, ha="center", va="center")
for x, label in ((275, "i"), (450, "j"), (610, "k")):
    for y in rows:
        ax.text(x, y - 4, rf"$O_{label}$", fontsize=15, color=RED, ha="center", va="center")
for x, label in ((330, "ji"), (490, "kj")):
    for y in (205, 250, 295):
        ax.text(x, y, rf"$w_{{{label}}}$", fontsize=14, color=BLUE, ha="center", va="center")

for y, label in zip(rows, ("Output 1", "Output 2", "Output m")):
    ax.add_patch(FancyArrowPatch((688, y), (712, y), arrowstyle="-|>",
                                 mutation_scale=7, lw=0.7, color=RED))
    ax.text(718, y + 1, label, fontsize=9, ha="left", va="center", color="black")

# Error column, class labels, and the green return arrow.
box(795, 185, 20, 200, "#a00000", "#800000")
ax.text(805, 285, "Error Error", fontsize=11, color="white", ha="center", va="center", rotation=90)
for y, label in zip(rows, ("Class 1", "Class 2", "Class m")):
    box(830, y - 10, 55, 20, "#d5f5e3", "#70a070")
    ax.text(857.5, y, label, fontsize=8.5, ha="center", va="center", color="black")
ax.add_patch(FancyArrowPatch((792, 323), (765, 323), arrowstyle="-|>",
                             mutation_scale=10, lw=1.2, color=GREEN))

# Layer annotations and arrows, with the original's i/j/k arrow letters.
for x, fill, edge, top, bottom, letter in (
    (220, "#d5e8f7", "#8090c0", "Previous Layer", "Layer (i)", "i"),
    (380, "#d5f5e3", "#70a070", "Current Layer", "(You are here)", "j"),
    (560, "#fdebd0", "#c09060", "Next Layer", "Layer (K)", "k"),
):
    box(x, 430, 85 if x != 380 else 90, 30, fill, edge)
    ax.text(x + (85 if x != 380 else 90) / 2, 445, f"{top}\n{bottom}",
            fontsize=7.5, ha="center", va="center", color="black")
    cx = x + (85 if x != 380 else 90) / 2
    ax.add_patch(FancyArrowPatch((cx, 429), (cx, 417), arrowstyle="-|>",
                                 mutation_scale=9, lw=0.8, color=edge))
    ax.text(cx, 423, letter, fontsize=8, ha="center", va="center", color=edge)

# Footer layer labels and hidden-layer extent.
box(68, 472, 55, 33, "black", "black")
ax.text(95.5, 488.5, "I/P\nLayer", fontsize=9, color="#e0e060", ha="center", va="center")
box(655, 472, 55, 33, "black", "black")
ax.text(682.5, 488.5, "O/P\nLayer", fontsize=9, color="#e0e060", ha="center", va="center")
ax.add_patch(FancyArrowPatch((160, 494), (600, 494), arrowstyle="<->",
                             mutation_scale=9, lw=0.9, color="black"))
box(260, 485, 240, 20, "black", "black")
ax.text(380, 495, "H i d d e n    L a y e r (s)", fontsize=9, color="#e0e060",
        ha="center", va="center")

fig.savefig(OUT, dpi=300, transparent=True)
plt.close(fig)
print(OUT)
