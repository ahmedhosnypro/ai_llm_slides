#!/usr/bin/env python3
"""Generate the red over-brace PNG for slide 009's back-propagation panel (v2).
Frame-verified shape (measure12/ASCII): main line y332..334 runs x540..695 and
x723..882 with a GAP under the center; a steep ARCH springs over the gap
((695,332.5) -> apex (~711,320.5) -> (723,332.5)); ends curl down-out
(left: (540,334)->(520,338.5); right: (882,334)->(907,341)).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets"
DPI = 600
RED = "#CC0000"

def quad(p0, p1, p2, n=200):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * np.array(p0) + 2 * t * (1 - t) * np.array(p1) + t ** 2 * np.array(p2)

x0, y0, x1, y1 = 519, 318, 908, 343
w, h = x1 - x0, y1 - y0
fig = plt.figure(figsize=(w / 72, h / 72), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(x0, x1); ax.set_ylim(y1, y0)  # y down
ax.axis("off")
LW = 2.4
segs = [
    quad((540, 334), (521, 335), (520, 339)),          # left end curl
    np.array([[540, 333.5], [695, 333.5]]),            # left line (stops at arch foot)
    quad((695, 333.5), (703, 316.0), (711, 320.8)),    # arch left side -> peak
    quad((711, 320.8), (719, 316.0), (723, 333.5)),    # arch right side (pointed peak)
    np.array([[723, 333.5], [882, 333.5]]),            # right line
    quad((882, 334), (900, 335), (907, 341)),          # right end curl
]
for pts in segs:
    ax.plot(pts[:, 0], pts[:, 1], lw=LW, color=RED, solid_capstyle="round")
fig.savefig(f"{OUT}/brace009.png", transparent=True)
plt.close(fig)
print("brace009 v2", f"bbox=({x0},{y0})-({x1},{y1}) embedWH=({w/72:.4f},{h/72:.4f})in")
