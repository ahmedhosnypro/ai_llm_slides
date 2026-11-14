import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets"

# ROC plot panel, PIL-measured from unique_slides/slide_030.jpg (local px, y down;
# panel origin abs (641,81); mpl y = PH - local_y):
#   panel 254x306; bg #EEFEFA; blue border #1B1380 ~2px at local (0,0)-(254,306)
#   grid vlines local x 18,60,103,146,189,231 ; hlines local y 69,111,152,190,229
#   red y-axis x=21, local y 3..269, arrowhead top ; red x-axis local y=269, x 21..249, arrowhead right
#   open red circles r~5 at local (169,67) [label 0.1] and (229,67) [label 0.0]
#   black labels '0.1' centered local (166,46), '0.0' centered local (219,46) in pale boxes, thin red outline
#   red rotated 'TPR' centered local (10,168); red 'FPR' centered local (129,282)
# v5 fixes vs v4: shrinkA/shrinkB=0 so the axes actually meet at the origin and reach
# the measured endpoints (default 2pt shrink left a ~7px gap at the corner);
# second marker x 233->229; label chips pale fill + thin red outline + smaller pad.
PW, PH = 254, 306
DPI = 300
PT = 72.0 / DPI  # points per image px; image placed at 1px=1pt so 1 img px = 1 slide pt

BG = "#EEFEFA"
BORDER = "#1B1380"
GRID = "#C2E0E6"
RED = "#C00000"

fig = plt.figure(figsize=(PW / DPI, PH / DPI), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, PW); ax.set_ylim(0, PH)
ax.set_xticks([]); ax.set_yticks([])
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.add_patch(Rectangle((0, 0), PW, PH, fill=False, edgecolor=BORDER,
                       lw=2 * PT, zorder=6))
for gx in [18, 60, 103, 146, 189, 231]:
    ax.plot([gx, gx], [0, PH], color=GRID, lw=1.0 * PT, zorder=1)
for gy in [69, 111, 152, 190, 229]:
    ax.plot([0, PW], [PH - gy, PH - gy], color=GRID, lw=1.0 * PT, zorder=1)
# red arrow axes (local y down -> mpl y up); shrink 0 so they meet at local (21,269)
ax.annotate("", xy=(249, PH - 269), xytext=(21, PH - 269),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2 * PT,
                            mutation_scale=4, shrinkA=0, shrinkB=0), zorder=3)
ax.annotate("", xy=(21, PH - 3), xytext=(21, PH - 269),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2 * PT,
                            mutation_scale=4, shrinkA=0, shrinkB=0), zorder=3)
# two open red circles at measured positions
for cx in [169, 229]:
    ax.add_patch(Circle((cx, PH - 67), 5, fill=True, facecolor=BG,
                        edgecolor=RED, lw=1.4 * PT, zorder=4))
# black threshold labels above the circles, pale box + thin red outline
LBLBOX = dict(boxstyle="square,pad=0.7", fc="#FBFFEB", ec="#C00000", lw=0.8 * PT)
ax.text(166, PH - 46, "0.1", color="#000000", fontsize=13 * PT, ha="center",
        va="center", zorder=5, bbox=LBLBOX)
ax.text(219, PH - 46, "0.0", color="#000000", fontsize=13 * PT, ha="center",
        va="center", zorder=5, bbox=LBLBOX)
ax.text(10, PH - 168, "TPR", color=RED, fontsize=11 * PT, rotation=90,
        ha="center", va="center", zorder=5)
ax.text(129, PH - 282, "FPR", color=RED, fontsize=11 * PT,
        ha="center", va="center", zorder=5)
fig.savefig(f"{OUT}/roc_030_v5.png", dpi=DPI, facecolor=fig.get_facecolor())
plt.close(fig)

from PIL import Image
im = Image.open(f"{OUT}/roc_030_v5.png")
print("roc_030_v5.png", im.size, "w_in=%.5f h_in=%.5f" % (im.size[0] / DPI, im.size[1] / DPI))
