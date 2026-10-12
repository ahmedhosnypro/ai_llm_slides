"""Generate the two 3D-slab images for slide 038 at 600 dpi, transparent,
exact-size law (embed w = px/600). Geometry in frame pt (1px=1pt), PIL-measured."""
import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
DPI = 600
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets/"

TAN = "#AF6712"; DARK = "#8B4513"; BLACK = "#000000"

def render(name, x0, y0, x1, y1, draw):
    W, H = x1 - x0, y1 - y0
    fig = plt.figure(figsize=(W / 72, H / 72), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    def P(pts):  # frame px -> fig units (y flipped)
        return [((x - x0), (y1 - y)) for x, y in pts]
    draw(ax, P)
    fig.savefig(OUT + name, dpi=DPI, transparent=True)
    plt.close(fig)
    from PIL import Image
    im = Image.open(OUT + name)
    side = {"image": name, "bbox_frame_px": [x0, y0, x1, y1], "png_w": im.size[0], "png_h": im.size[1]}
    with open(OUT + name.replace(".png", ".json"), "w") as f: json.dump(side, f, indent=1)
    print(name, im.size, side)

# ---- 1) brown image-patch slab: tan parallelogram + dark right side band + black outline
def brown(ax, P):
    front = [(260, 348), (344, 296), (344, 385), (260, 437)]      # measured corners
    side  = [(344, 296), (353, 292), (353, 381), (344, 385)]      # dark right face (8px depth)
    topband = [(262, 350), (342, 298), (342, 306), (262, 358)]    # dark top-face band inside the top edge (judge attempt-1 + PIL ink band)
    ax.add_patch(Polygon(P(side), closed=True, facecolor=DARK, edgecolor=BLACK, lw=1.2))
    ax.add_patch(Polygon(P(front), closed=True, facecolor=TAN, edgecolor=BLACK, lw=1.2))
    ax.add_patch(Polygon(P(topband), closed=True, facecolor=DARK, edgecolor="none", lw=0))
render("slab038_brown.png", 256, 290, 356, 440, brown)

# ---- 2) five filter slabs: identical parallelograms, pitch 29, later drawn on top
SLAB_W = 42; RISE = 20; YL_TOP = 358; YL_BOT = 398
COLORS = ["#0BBFE9", "#0ABF50", "#E90000", "#FDFF0B", "#6A239D"]
def stack(ax, P):
    for k, col in enumerate(COLORS):
        xl = 393 + 28.75 * k
        pts = [(xl, YL_TOP), (xl + SLAB_W, YL_TOP - RISE), (xl + SLAB_W, YL_BOT - RISE), (xl, YL_BOT)]
        ax.add_patch(Polygon(P(pts), closed=True, facecolor=col, edgecolor=BLACK, lw=1.2))
render("slab038_stack.png", 390, 334, 556, 402, stack)
