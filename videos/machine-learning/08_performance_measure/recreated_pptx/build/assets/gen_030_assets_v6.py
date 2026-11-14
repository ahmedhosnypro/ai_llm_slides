import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets"

# ROC plot panel, PIL-measured from unique_slides/slide_030.jpg (local px, y down;
# panel origin abs (641,81); mpl y = PH - local_y):
#   panel 254x306; bg #EEFEFA; blue border #1B1380 2px at local (0,0)-(254,306)
#   grid vlines local x 61,104,147,190,233 ; hlines local y 69,111,152,190,229
#   red axes #C00000 ~3px: y-axis x=20 local y 0..270 arrowhead top;
#     x-axis local y=270 x 20..260 arrowhead right; they MEET at local (20,270)
#   open red circles r5 at local (169,67) [label 0.1] and (232,67) [label 0.0]
#   labels '0.1'/'0.0' centered local (170,46)/(234,46), dark text, pale box, gray edge
#   red rotated 'TPR' centered local (10,168); red 'FPR' centered local (129,282)
# v6 fixes vs v5: house dark red #C00000 with 3px lw (v5's 1.2px anti-aliased to salmon);
# arrow tips extended to measured endpoints (x 260, y ~0); second point back to x232;
# label chips enlarged (12pt) with gray edge like the original.
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
for gx in [61, 104, 147, 190, 233]:
    ax.plot([gx, gx], [0, PH], color=GRID, lw=1.0 * PT, zorder=1)
for gy in [69, 111, 152, 190, 229]:
    ax.plot([0, PW], [PH - gy, PH - gy], color=GRID, lw=1.0 * PT, zorder=1)
# red arrow axes (local y down -> mpl y up); shrink 0 so they meet at local (20,270)
ax.annotate("", xy=(253, PH - 270), xytext=(20, PH - 270), annotation_clip=False,
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=3 * PT,
                            mutation_scale=2, shrinkA=0, shrinkB=0), zorder=3)
ax.annotate("", xy=(20, PH - 0.5), xytext=(20, PH - 270), annotation_clip=False,
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=3 * PT,
                            mutation_scale=2, shrinkA=0, shrinkB=0), zorder=3)
# two open red circles at measured positions
for cx in [169, 232]:
    ax.add_patch(Circle((cx, PH - 67), 5, fill=True, facecolor=BG,
                        edgecolor=RED, lw=2 * PT, zorder=4))
# dark threshold labels above the circles, pale box + gray edge
LBLBOX = dict(boxstyle="square,pad=0.4", fc="#FBFFEB", ec="#888888", lw=0.8 * PT)
ax.text(170, PH - 46, "0.1", color="#000000", fontsize=12 * PT, ha="center",
        va="center", zorder=5, bbox=LBLBOX)
ax.text(234, PH - 46, "0.0", color="#000000", fontsize=12 * PT, ha="center",
        va="center", zorder=5, bbox=LBLBOX)
ax.text(10, PH - 168, "TPR", color=RED, fontsize=11 * PT, rotation=90,
        ha="center", va="center", zorder=5)
ax.text(129, PH - 282, "FPR", color=RED, fontsize=11 * PT,
        ha="center", va="center", zorder=5)
fig.savefig(f"{OUT}/roc_030_v6.png", dpi=DPI, facecolor=fig.get_facecolor())
plt.close(fig)

from PIL import Image
im = Image.open(f"{OUT}/roc_030_v6.png")
print("roc_030_v6.png", im.size, "w_in=%.5f h_in=%.5f" % (im.size[0] / DPI, im.size[1] / DPI))
