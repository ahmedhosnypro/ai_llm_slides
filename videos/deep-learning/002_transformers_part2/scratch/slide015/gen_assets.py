#!/usr/bin/env python3
"""Generate slide_015 image assets: swoosh arrow, translucent gray plane, rotated
pill labels. All at 600 dpi, transparent background, embedded at exact px/600 size.

SWOOSH GEOMETRY (Z6 4x read + white-background PIL maps, slide pts):
  top J-hook end (808,246)->(824,254); straight-ish diagonal through (777,284),
  (700,321), (664,339), (647,348); U-turn: in at (603,370), bottom (590,375.5),
  curl up (586.5,368)->(588,362.5)->(592.5,358.5); solid NE arrowhead tip (600,353)
  aimed at the h1 output container's bottom edge. Uniform ~10pt stroke, no taper.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon
from PIL import Image
import io
import os

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets"
DPI = 600

# ---- 1) swoosh: canvas slide-pt (550..845, 235..400)
W, H = 295, 165
fig = plt.figure(figsize=(W / 72, H / 72), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(550, 845); ax.set_ylim(400, 235)  # inverted y -> slide coords map 1:1
ax.axis("off")
LW = 10
main = FancyArrowPatch((822, 255), (604, 369), connectionstyle="arc3,rad=0.12",
                       arrowstyle="-", mutation_scale=1, lw=LW,
                       color="#CC0000", shrinkA=0, shrinkB=0, capstyle="round")
ax.add_patch(main)
top = FancyArrowPatch((808, 246), (822, 255), connectionstyle="arc3,rad=0.45",
                      arrowstyle="-", mutation_scale=1, lw=LW,
                      color="#CC0000", shrinkA=0, shrinkB=0, capstyle="round")
ax.add_patch(top)
uturn = FancyArrowPatch((604, 369), (600, 354), connectionstyle="arc3,rad=-1.35",
                        arrowstyle="-|>", mutation_scale=30, lw=LW,
                        color="#CC0000", shrinkA=0, shrinkB=0, capstyle="round")
ax.add_patch(uturn)
fig.savefig(f"{OUT}/swoosh015.png", transparent=True)
plt.close(fig)
im = Image.open(f"{OUT}/swoosh015.png")
print("swoosh015:", im.size, "embed at", 550 / 72, 235 / 72, im.size[0] / DPI, im.size[1] / DPI)

# ---- 2) gray translucent plane: quad (272,80),(430,80),(310,215),(114,215)
W2, H2 = 335, 163
fig = plt.figure(figsize=(W2 / 72, H2 / 72), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(110, 445); ax.set_ylim(228, 65)
ax.axis("off")
ax.add_patch(Polygon([(272, 80), (430, 80), (310, 215), (114, 215)],
                     closed=True, facecolor=(153 / 255, 153 / 255, 153 / 255, 0.45),
                     edgecolor="none"))
fig.savefig(f"{OUT}/plane015.png", transparent=True)
plt.close(fig)
im = Image.open(f"{OUT}/plane015.png")
print("plane015:", im.size, "embed at", 110 / 72, 65 / 72, im.size[0] / DPI, im.size[1] / DPI)

# ---- 3) rotated pill labels
def rot_label(text, color, fs, out):
    fig = plt.figure(figsize=(4, 1.6), dpi=DPI)
    fig.patch.set_alpha(0)
    fig.text(0.5, 0.5, text, fontsize=fs, color=color, ha="center", va="center",
             fontweight="bold", family="DejaVu Sans")
    fig.canvas.draw()
    buf = io.BytesIO()
    fig.savefig(buf, transparent=True)
    plt.close(fig)
    buf.seek(0)
    im = Image.open(buf)
    im = im.crop(im.getbbox())
    im = im.transpose(Image.ROTATE_270)  # horizontal -> reads TOP-TO-BOTTOM (orig: top glyph = 'S')
    im.save(out)
    print(os.path.basename(out), im.size, "w_in", im.size[0] / DPI, "h_in", im.size[1] / DPI)

rot_label("Scaling by $\\sqrt{d}$", "#8B2B5E", 11, f"{OUT}/eq015_scaling_rot.png")
rot_label("Soft max", "#7B2D8B", 11, f"{OUT}/eq015_softmax_rot.png")
