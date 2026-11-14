#!/usr/bin/env python3
"""Generate the ROC plot PNG for slide 36, matched to the measured original region.

Original frame (960x540, 1px=1pt). Measured from unique_slides/slide_036.jpg:
- canvas box x[636,901] y[43,407] (embed region)
- ROC panel: navy border x[642,900] y[81,407], near-white fill #EEFEFB,
  light gridlines #C7DCDF at 0.1 intervals
- axes: y-axis x=664 (FPR=0), x-axis y=369 (TPR=0), FPR=1 at x=877, TPR=1 at y=167,
  red arrow tips at (664,107) and (888,369)
- purple ROC polyline through the 7 threshold points:
  thr 1.0 -> (0,0); 0.7 -> (0,0.6); 0.6 -> (1/6,0.6); 0.4 -> (1/6,0.8);
  0.3 -> (1/3,1); 0.1 -> (2/3,1); 0.0 -> (1,1)
- annotations: green "The Best / (If Any)" two-line label + bright green dot at
  (0,0.96) below the plateau + short hollow green arrow from above-right;
  red two-line "Best / (TPR)" label with short hollow arrow beneath pointing down-left;
  red two-line "Best / (FPR)" label with compact horizontal hollow left-arrow at the
  0.4 point level
Output PNG at 600 dpi; place with w = px/600 in.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.path import Path
from matplotlib.patches import PathPatch

DPI = 600
X0, X1 = 636, 901
Y0, Y1 = 407, 43  # y flipped: bottom=407, top=43
W_IN = (X1 - X0) / 72.0
H_IN = (Y0 - Y1) / 72.0

# axes in px
AX_X0, AX_X1 = 664, 877   # FPR 0..1
AX_Y0, AX_Y1 = 369, 167   # TPR 0..1 (y flipped)
LX = (AX_X0 - X0) / (X1 - X0)
RX = (AX_X1 - X0) / (X1 - X0)
BY = 1 - (AX_Y0 - Y1) / (Y0 - Y1)
TY = 1 - (AX_Y1 - Y1) / (Y0 - Y1)

PURPLE = "#800080"
GREEN = "#83FF06"
RED = "#FF0000"
NAVY = "#0A0A80"
PANEL_BG = "#EEFEFB"
GRID = "#C7DCDF"
AXIS_X = "#7A242D"   # dark red x-axis
AXIS_Y = "#761380"   # purple-navy y-axis

fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)

ax = fig.add_axes([LX, BY, RX - LX, TY - BY])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_facecolor("none")

# panel: fill + navy border, px x[642,900] y[81,407]
fpr0 = (642 - AX_X0) / (AX_X1 - AX_X0)
fpr1 = (900 - AX_X0) / (AX_X1 - AX_X0)
tpr0 = (AX_Y0 - 407) / (AX_Y0 - AX_Y1)
tpr1 = (AX_Y0 - 81) / (AX_Y0 - AX_Y1)
ax.add_patch(Rectangle((fpr0, tpr0), fpr1 - fpr0, tpr1 - tpr0,
                       facecolor=PANEL_BG, edgecolor=NAVY, lw=0.8,
                       zorder=0, clip_on=False))

# gridlines
for i in range(1, 5):
    ax.axvline(i / 5, color=GRID, lw=0.5, zorder=2)
    ax.axhline(i / 5, color=GRID, lw=0.5, zorder=2)

# ROC points (fpr, tpr) with threshold labels, ordered by decreasing threshold.
# Label offsets measured from the original's cream badge centers (data coords).
pts = [
    (1.0, 1.0, "0.0", (-0.06, 0.10)),
    (2 / 3, 1.0, "0.1", (0.023, 0.10)),
    (1 / 3, 1.0, "0.3", (-0.053, 0.10)),
    (1 / 6, 0.8, "0.4", (0.10, -0.13)),
    (1 / 6, 0.6, "0.6", (0.096, -0.10)),
    (0.0, 0.6, "0.7", (0.013, -0.153)),
    (0.0, 0.0, None, (0.0, 0.0)),    # threshold 1.0 at origin; its '1.0' label sits BELOW the plot box and is drawn as a slide text element in slide_036.js
]
fpr = [p[0] for p in pts]
tpr = [p[1] for p in pts]
# the 0.3->0.4 segment is a rounded rise in the original: quadratic bezier via (1/6, 1.0)
seg = Path([(1 / 3, 1.0), (1 / 6, 1.0), (1 / 6, 0.8)],
           [Path.MOVETO, Path.CURVE3, Path.CURVE3])
ax.add_patch(PathPatch(seg, facecolor="none", edgecolor=PURPLE, lw=1.8, zorder=3))
ax.plot([1.0, 2 / 3, 1 / 3], [1.0, 1.0, 1.0], color=PURPLE, lw=1.8, zorder=3)
ax.plot([1 / 6, 1 / 6, 0.0, 0.0], [0.8, 0.6, 0.6, 0.0], color=PURPLE, lw=1.8, zorder=3)
ax.scatter(fpr, tpr, s=55, facecolors="none", edgecolors=RED,
           linewidths=1.4, zorder=4, clip_on=False)
for x, y, lab, (dx, dy) in pts:
    if lab:
        ax.annotate(lab, (x, y), xytext=(x + dx, y + dy), fontsize=12,
                    color="#000000", zorder=5, ha="center", va="center",
                    annotation_clip=False,
                    bbox=dict(boxstyle="square,pad=0.3", facecolor="#FFFFE0",
                              edgecolor="#C0A000", lw=0.8))

# axes spines left/bottom only, with hollow arrowheads into the margin band
ax.spines["left"].set_visible(True); ax.spines["left"].set_color(AXIS_Y)
ax.spines["bottom"].set_visible(True); ax.spines["bottom"].set_color(AXIS_X)
ax.spines["left"].set_linewidth(1.2)
ax.spines["bottom"].set_linewidth(1.2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)


def hollow_arrow(xy, xytext, color, ms=30):
    a = ax.annotate("", xy=xy, xytext=xytext,
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=3.0,
                                    mutation_scale=ms, fill=False),
                    annotation_clip=False, zorder=6)
    a.arrow_patch.set_fill(True)
    a.arrow_patch.set_facecolor("white")
    return a


hollow_arrow((1.07, 0), (1.0, 0), AXIS_X, ms=20)     # x-axis tip at px (892,369)
hollow_arrow((0, 1.32), (0, 1.0), AXIS_Y, ms=20)     # y-axis tip at px (664,102)

# original carries no numeric tick labels on either axis — only gridlines,
# the TPR/FPR axis titles, and the threshold callouts
ax.set_xticks([])
ax.set_yticks([])


def fx(px):
    return (px - X0) / (X1 - X0)


def fy(py):
    return 1 - (py - Y1) / (Y0 - Y1)


# axis titles (original px: TPR rotated at x=647 y[239,263], FPR at x[759,785] y=386)
fig.text(fx(653), fy(251), "TPR", fontsize=9, color="#8B0000", ha="center",
         va="center", rotation=90)
fig.text(fx(772), fy(386), "FPR", fontsize=9, color="#8B0000", ha="center", va="center")

# green "The Best / (If Any)" two-line label + bright dot below the plateau + short
# hollow arrow approaching from above-right, pointing down-left at the dot
fig.text(fx(694), fy(105), "The Best", fontsize=8, color="#3F8F3F", ha="center", va="center")
fig.text(fx(693), fy(117), "(If Any)", fontsize=8, color="#3F8F3F", ha="center", va="center")
ax.scatter([0.0], [0.96], s=150, color=GREEN, zorder=6, edgecolors=GREEN, clip_on=False)
hollow_arrow((0.02, 0.99), (0.14, 1.12), GREEN)

# red "Best / (TPR)" two-line label near the top, short hollow arrow beneath it
# pointing down-left toward the 0.3 knee
fig.text(fx(780), fy(89), "Best", fontsize=8, color=RED, ha="center", va="center")
fig.text(fx(780), fy(101), "(TPR)", fontsize=8, color=RED, ha="center", va="center")
hollow_arrow((0.36, 1.08), (0.44, 1.24), RED)

# red "Best / (FPR)" two-line label beside a compact horizontal hollow left-arrow
# at the 0.4 point level (px y~209)
fig.text(fx(768), fy(193), "Best", fontsize=8, color=RED, ha="center", va="center")
fig.text(fx(768), fy(205), "(FPR)", fontsize=8, color=RED, ha="center", va="center")
hollow_arrow((0.216, 0.777), (0.3708, 0.7723), RED)

fig.patch.set_alpha(0.0)
out = "assets/roc_036.png"
fig.savefig(out, dpi=DPI, transparent=True, facecolor=(0, 0, 0, 0))
print("saved", out)
from PIL import Image
im = Image.open(out)
print("px size:", im.size, "-> in:", im.size[0] / DPI, im.size[1] / DPI)
