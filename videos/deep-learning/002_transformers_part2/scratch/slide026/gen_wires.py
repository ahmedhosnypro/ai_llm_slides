#!/usr/bin/env python3
"""Wire-fan PNG for slide 026: 6 curved encoder wires from the Encoder connector bar
(frame 666, y=288..375) fanning to the Differential box bottom (y=281) and Sin/Cos
Encoder box top (y=398). Rendered 8x, transparent, exact-size embed later.
Rect covered: frame (664..860) x (246..430) -> 196x184 px @8x = 1568x1472.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as mpatches
import numpy as np

X0, X1, Y0, Y1 = 664, 860, 246, 430
S = 8
W, H = (X1 - X0) * S, (Y1 - Y0) * S

fig = plt.figure(figsize=(W / 300, H / 300), dpi=300)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, X1 - X0)
ax.set_ylim(Y1 - Y0, 0)  # frame y grows downward
ax.axis("off")

def f(x, y):
    return (x - X0, y - Y0)

starts = [(666, y) for y in (289, 306, 323, 341, 358, 373)]
ends = [(706, 281), (726, 281), (746, 281), (754, 398), (770, 398), (786, 398)]
lw = 1.5 * S / 1.4  # ~1.5 frame px wide

for i, ((sx, sy), (ex, ey)) in enumerate(zip(starts, ends)):
    x0, y0 = f(sx, sy)
    x1, y1 = f(ex, ey)
    if i < 3:
        # curve up-right: control near (sx+18, sy-10), (ex-14, ey+22)
        c1 = f(sx + 16, sy - 14)
        c2 = f(ex - 12, ey + 30)
    else:
        # curve down-right
        c1 = f(sx + 16, sy + 16)
        c2 = f(ex - 12, ey - 26)
    path = Path([(x0, y0), c1, c2, (x1, y1)], [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4])
    ax.add_patch(mpatches.PathPatch(path, fill=False, edgecolor="#1A1A1A", lw=lw,
                                    capstyle="round"))

fig.savefig("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/slide026_wires.png",
            transparent=True)
print("saved wires png", W, H)
