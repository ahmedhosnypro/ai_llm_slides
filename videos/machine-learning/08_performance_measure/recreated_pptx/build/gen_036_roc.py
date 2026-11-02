#!/usr/bin/env python3
"""Generate the ROC plot PNG for slide 36, matched to the measured original region.

Original frame (960x540, 1px=1pt). Measured from unique_slides/slide_036.jpg:
- canvas box x[636,901] y[43,407] (embed region)
- ROC panel: navy border x[642,900] y[50,406], near-white fill #EEFEFB,
  light gridlines #C7DCDF at 0.1 intervals
- axes: y-axis x=664 (FPR=0, purple-navy #761380), x-axis y=369 (TPR=0, dark red
  #7A242D), FPR=1 at x=895, TPR=1 at y=167, arrowheads at both axis ends
- purple ROC polyline through the 7 threshold points:
  thr 1.0 -> (0,0); 0.7 -> (0,0.6); 0.6 -> (1/6,0.6); 0.4 -> (1/6,0.8);
  0.3 -> (1/3,1); 0.1 -> (2/3,1); 0.0 -> (1,1)
- annotations: green "The Best / (If Any)" + green dot at (0,1) corner; red
  "Best (TPR)" arrow to the top segment; red "Best (FPR)" arrow to the mid point
Output PNG at 600 dpi; place with w = px/600 in.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

DPI = 600
X0, X1 = 636, 901
Y0, Y1 = 407, 43  # y flipped: bottom=407, top=43
W_IN = (X1 - X0) / 72.0
H_IN = (Y0 - Y1) / 72.0

# axes in px
AX_X0, AX_X1 = 664, 895   # FPR 0..1
AX_Y0, AX_Y1 = 369, 167   # TPR 0..1 (y flipped)
LX = (AX_X0 - X0) / (X1 - X0)
RX = (AX_X1 - X0) / (X1 - X0)
BY = 1 - (AX_Y0 - Y1) / (Y0 - Y1)
TY = 1 - (AX_Y1 - Y1) / (Y0 - Y1)

PURPLE = "#800080"
GREEN = "#00A000"
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

# panel: fill + navy border, drawn inside the axes (figure-level patches cover axes)
# panel px x[642,900] y[50,406] -> data coords via axes calibration
fpr0 = (642 - AX_X0) / (AX_X1 - AX_X0)
fpr1 = (900 - AX_X0) / (AX_X1 - AX_X0)
tpr0 = (AX_Y0 - 406) / (AX_Y0 - AX_Y1)
tpr1 = (AX_Y0 - 50) / (AX_Y0 - AX_Y1)
ax.add_patch(Rectangle((fpr0, tpr0), fpr1 - fpr0, tpr1 - tpr0,
                       facecolor=PANEL_BG, edgecolor=NAVY, lw=0.3,
                       zorder=0, clip_on=False))

# gridlines
for i in range(1, 10):
    ax.axvline(i / 10, color=GRID, lw=0.15, zorder=2)
    ax.axhline(i / 10, color=GRID, lw=0.15, zorder=2)

# ROC points (fpr, tpr) with threshold labels, ordered by decreasing threshold
pts = [
    (1.0, 1.0, "0.0", (-0.045, 0.04)),
    (2 / 3, 1.0, "0.1", (-0.03, 0.04)),
    (1 / 3, 1.0, "0.3", (-0.03, 0.04)),
    (1 / 6, 0.8, "0.4", (-0.085, 0.0)),
    (1 / 6, 0.6, "0.6", (-0.02, -0.065)),
    (0.0, 0.6, "0.7", (-0.085, 0.0)),
    (0.0, 0.0, None, (0.0, 0.0)),    # threshold 1.0 at origin; its '1.0' label sits BELOW the plot box and is drawn as a slide text element in slide_036.js
]
fpr = [p[0] for p in pts]
tpr = [p[1] for p in pts]
ax.plot(fpr, tpr, color=PURPLE, lw=1.8, zorder=3)
ax.scatter(fpr, tpr, s=55, facecolors="none", edgecolors=RED,
           linewidths=1.4, zorder=4)
for x, y, lab, (dx, dy) in pts:
    if lab:
        ax.annotate(lab, (x, y), xytext=(x + dx, y + dy), fontsize=7.5,
                    color="#000000", zorder=5, ha="center", va="center",
                    annotation_clip=False)

# axes spines left/bottom only, with arrowheads into the margin band
ax.spines["left"].set_visible(True); ax.spines["left"].set_color(AXIS_Y)
ax.spines["bottom"].set_visible(True); ax.spines["bottom"].set_color(AXIS_X)
ax.spines["left"].set_linewidth(1.2)
ax.spines["bottom"].set_linewidth(1.2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.annotate("", xy=(1.03, 0), xytext=(1.0, 0),
            arrowprops=dict(arrowstyle="-|>", color=AXIS_X, lw=1.2),
            annotation_clip=False, zorder=6)
ax.annotate("", xy=(0, 1.10), xytext=(0, 1.0),
            arrowprops=dict(arrowstyle="-|>", color=AXIS_Y, lw=1.2),
            annotation_clip=False, zorder=6)

# original carries no numeric tick labels on either axis — only gridlines,
# the TPR/FPR axis titles, and the threshold callouts
ax.set_xticks([])
ax.set_yticks([])

def fx(px):
    return (px - X0) / (X1 - X0)

def fy(py):
    return 1 - (py - Y1) / (Y0 - Y1)

# axis labels (original px: TPR rotated x[647,664] y[200,262], FPR x[759,785] y[380,386])
fig.text(fx(655), fy(231), "TPR", fontsize=9, color="#8B0000", ha="center",
         va="center", rotation=90)
fig.text(fx(772), fy(383), "FPR", fontsize=9, color="#8B0000", ha="center", va="center")

# green "The Best (If Any)" + dot at the ideal corner (0,1) + arrow
fig.text(fx(690), fy(82), "The Best", fontsize=8, color=GREEN, ha="center", va="center")
fig.text(fx(690), fy(97), "(If Any)", fontsize=8, color=GREEN, ha="center", va="center")
ax.scatter([0.0], [1.0], s=55, color=GREEN, zorder=6, edgecolors=GREEN)
ax.annotate("", xy=(0.01, 0.985), xytext=(0.10, 0.90),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.2),
            annotation_clip=False, zorder=6)

# red "Best (TPR)" -> top segment; "Best (FPR)" -> mid point
fig.text(fx(800), fy(72), "Best (TPR)", fontsize=8, color=RED, ha="center", va="center")
ax.annotate("", xy=(0.55, 1.005), xytext=(fx(795), fy(80)),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2),
            annotation_clip=False, zorder=6)
fig.text(fx(800), fy(200), "Best (FPR)", fontsize=8, color=RED, ha="center", va="center")
ax.annotate("", xy=(1 / 6 + 0.02, 0.6), xytext=(fx(795), fy(192)),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2),
            annotation_clip=False, zorder=6)

fig.patch.set_alpha(0.0)
out = "assets/roc_036.png"
fig.savefig(out, dpi=DPI, transparent=True, facecolor=(0, 0, 0, 0))
print("saved", out)
from PIL import Image
im = Image.open(out)
print("px size:", im.size, "-> in:", im.size[0] / DPI, im.size[1] / DPI)
