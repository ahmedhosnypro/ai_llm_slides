import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets"

# ROC plot panel, PIL-measured from unique_slides/slide_030.jpg (local px, y down;
# panel origin abs (641,81); mpl y = PH - local_y):
#   panel 254x306; bg #EEFEFA; blue border #7E7EC8 ~2px at local (0,0)-(254,306)
#   grid vlines local x 18,60,103,146,189,231 ; hlines local y 68,110,149,188,228,268
#   red y-axis x=21, local y 4..273, arrowhead top ; red x-axis local y=270, x 21..249, arrowhead right
#   open red circles r~5 at local (169,67) [label 0.1] and (233,67) [label 0.0]
#   black labels '0.1' centered local (166,46), '0.0' centered local (218,46)
#   red rotated 'TPR' at local (10,168); red 'FPR' at local (129,282)
# No connecting line between the points (reanalysis: none drawn).
PW, PH = 254, 306
DPI = 300
PT = 72.0 / DPI  # points per image px; image placed at 1px=1pt so 1 img px = 1 slide pt

BG = "#EEFEFA"
BORDER = "#6A6CB7"
GRID = "#CFE4E8"
RED = "#FF0000"

fig = plt.figure(figsize=(PW / DPI, PH / DPI), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, PW); ax.set_ylim(0, PH)
ax.axis("off")
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
for sp in ax.spines.values():
    sp.set_visible(True); sp.set_color(BORDER); sp.set_linewidth(2 * PT)
for gx in [18, 60, 103, 146, 189, 231]:
    ax.plot([gx, gx], [0, PH], color=GRID, lw=1.0 * PT, zorder=1)
for gy in [68, 110, 149, 188, 228, 268]:
    ax.plot([0, PW], [PH - gy, PH - gy], color=GRID, lw=1.0 * PT, zorder=1)
# red arrow axes (local y down -> mpl y up)
ax.annotate("", xy=(249, PH - 270), xytext=(21, PH - 270),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.5 * PT,
                            mutation_scale=5), zorder=3)
ax.annotate("", xy=(21, PH - 4), xytext=(21, PH - 273),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.5 * PT,
                            mutation_scale=5), zorder=3)
# two open red circles at measured positions
for cx in [169, 233]:
    ax.add_patch(Circle((cx, PH - 67), 5, fill=True, facecolor=BG,
                        edgecolor=RED, lw=1.4 * PT, zorder=4))
# black threshold labels above the circles
LBLBOX = dict(boxstyle="square,pad=0.3", fc="white", ec="#777777")
ax.text(166, PH - 46, "0.1", color="#000000", fontsize=9 * PT, ha="center",
        va="center", zorder=5, bbox=LBLBOX)
ax.text(219, PH - 46, "0.0", color="#000000", fontsize=9 * PT, ha="center",
        va="center", zorder=5, bbox=LBLBOX)
ax.text(10, PH - 168, "TPR", color=RED, fontsize=11 * PT, rotation=90,
        ha="center", va="center", zorder=5)
ax.text(129, PH - 282, "FPR", color=RED, fontsize=11 * PT,
        ha="center", va="center", zorder=5)
fig.savefig(f"{OUT}/roc_030_v4.png", dpi=DPI, facecolor=fig.get_facecolor())
plt.close(fig)

from PIL import Image
im = Image.open(f"{OUT}/roc_030_v4.png")
print("roc_030_v4.png", im.size, "w_in=%.5f h_in=%.5f" % (im.size[0] / DPI, im.size[1] / DPI))
