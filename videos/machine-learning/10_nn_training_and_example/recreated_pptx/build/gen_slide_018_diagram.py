#!/usr/bin/env python3
"""Slide 18 network diagram as one 600dpi transparent PNG.
Canvas == placed area: x 358..758 orig-px, y 55..208 orig-px (960x540 frame).
Placed in pptx at (X(358), Y(55)) with w=X(400), h=Y(153) -> no rescale.
Topology measured from unique_slides/slide_018.jpg: 4 columns x 3 rows of
(Sigma circle + f box) neuron pairs, fully-connected adjacent columns,
yellow Net circles above cols 3-4, purple bias-1 circles below, input dots.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch, Rectangle
import sys

# placed area in original-frame pixels
PX0, PY0, PX1, PY1 = 358, 55, 758, 208
W = PX1 - PX0
H = PY1 - PY0
fig = plt.figure(figsize=(W / 72.0, H / 72.0), dpi=600)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)  # y down? no: use y-up with local coords ly = H - (py - PY0)
ax.axis("off")
fig.patch.set_alpha(0.0)

def LX(px): return px - PX0
def LY(py): return H - (py - PY0)

# panel background
ax.add_patch(Rectangle((0, 0), W, H, facecolor="#D9CDC1", edgecolor="#D4A7AC", lw=1.2))

ROWS = [84, 126, 171]           # orig py
COLS = [409, 476, 563, 640]     # orig px of Sigma centers
FILLS = ["#F4F0E8", "#CFE0F0", "#B8E8A8", "#F8C8A8"]
SIGMA_C = "#C0392B"

# dense fully-connected lines between adjacent columns (all pairs)
for ci in range(3):
    for r1 in ROWS:
        for r2 in ROWS:
            ax.plot([LX(COLS[ci] + 12), LX(COLS[ci + 1] - 12)],
                    [LY(r1), LY(r2)], color="#D8A8B8", lw=0.6, alpha=0.85, zorder=1)
# input dots -> col1
for dy in [108, 122, 134, 147]:
    for r in ROWS:
        ax.plot([LX(376), LX(COLS[0] - 12)], [LY(dy), LY(r)], color="#C8B8C8", lw=0.5, alpha=0.7, zorder=1)
# col3 -> output arrows (straight, red-ish)
for r1 in ROWS:
    for r2 in ROWS:
        ax.plot([LX(652), LX(688)], [LY(r1), LY(r2)], color="#C05868", lw=0.6, alpha=0.9, zorder=1)

# neuron pairs: Sigma circle + f box
for ci, cx in enumerate(COLS):
    for r in ROWS:
        ax.add_patch(Circle((LX(cx), LY(r)), 11, facecolor=FILLS[ci],
                            edgecolor="#888888", lw=0.8, zorder=3))
        ax.text(LX(cx), LY(r), r"$\Sigma$", fontsize=11, fontweight="bold",
                color=SIGMA_C, ha="center", va="center", zorder=4)
        bx, by = LX(cx + 24), LY(r)
        ax.add_patch(FancyBboxPatch((bx - 8, by - 8), 16, 16,
                     boxstyle="round,pad=1", facecolor="#F8F4EC",
                     edgecolor="#888888", lw=0.7, zorder=3))
        ax.text(bx, by, "f", fontsize=9, style="italic", color="#333333",
                ha="center", va="center", zorder=4)

# Net_j / O_j labels between columns (red, small)
for ci in range(3):
    for r in ROWS:
        ax.text(LX(COLS[ci] + 38), LY(r) - 6, "Net", fontsize=5.5, color="#C00000",
                ha="center", va="center", zorder=4)
        ax.text(LX(COLS[ci] + 52), LY(r) + 7, "O", fontsize=6, color="#C00000",
                ha="center", va="center", zorder=4, fontweight="bold")

# yellow Net circles above cols 3-4 (k layer) and curved feedback dashed arrows
for ci in (2, 3):
    for r in ROWS:
        ax.add_patch(Circle((LX(COLS[ci] + 14), LY(r) - 22), 9,
                            facecolor="#FFE066", edgecolor="#C8A020", lw=0.7, zorder=3))
        ax.text(LX(COLS[ci] + 14), LY(r) - 22, "Net", fontsize=4.5, color="#7A6000",
                ha="center", va="center", zorder=4)
for r1 in ROWS:
    for r2 in ROWS:
        if r1 != r2:
            ax.add_patch(FancyArrowPatch((LX(COLS[3] + 14), LY(r1) - 30),
                                         (LX(COLS[2] + 14), LY(r2) - 30),
                                         connectionstyle="arc3,rad=-0.35",
                                         arrowstyle="-|>", mutation_scale=5,
                                         color="#404040", lw=0.6, ls=(0, (3, 2)), zorder=2))
# w_kj label near top feedback
ax.text(LX(600), LY(62), r"$w_{kj}$", fontsize=6, color="#3050C0", ha="center", zorder=4)

# bias-1 purple circles below cols 2 and 4
for cx in (COLS[1], COLS[3]):
    ax.add_patch(Circle((LX(cx), LY(196)), 8, facecolor="#800080",
                        edgecolor="#800080", zorder=3))
    ax.text(LX(cx), LY(196), "1", fontsize=7, color="#FFFFFF", fontweight="bold",
            ha="center", va="center", zorder=4)
    ax.annotate("", xy=(LX(cx), LY(184)), xytext=(LX(cx), LY(196)),
                arrowprops=dict(arrowstyle="-|>", color="#40A020", lw=1.2), zorder=2)

# input magenta dots
for dy in [108, 122, 134, 147]:
    ax.add_patch(Circle((LX(372), LY(dy)), 3, facecolor="#800080", edgecolor="#800080", zorder=3))
# input data label bottom-left
ax.add_patch(Circle((LX(373), LY(198)), 6, facecolor="#800080", edgecolor="#800080", zorder=3))
ax.text(LX(383), LY(198), "Input Data", fontsize=6.5, color="#8B007A",
        fontweight="bold", ha="left", va="center", zorder=4)

# output boxes (O_k label + Output n)
for i, r in enumerate(ROWS):
    ax.text(LX(694), LY(r) - 4, r"$O_k$", fontsize=6.5, color="#C00000",
            fontweight="bold", ha="left", va="center", zorder=4)
    ax.add_patch(Rectangle((LX(706), LY(r) - 7), 38, 14, facecolor="#FFFFFF",
                           edgecolor="#1A1080", lw=1.0, zorder=3))
    ax.text(LX(725), LY(r), f"Output {i+1 if i<2 else 'm'}", fontsize=5.5,
            color="#1A1080", fontweight="bold", ha="center", va="center", zorder=4)

out = sys.argv[1] if len(sys.argv) > 1 else "slide_018_diagram.png"
fig.savefig(out, dpi=600, transparent=True)
print("ok", out)
