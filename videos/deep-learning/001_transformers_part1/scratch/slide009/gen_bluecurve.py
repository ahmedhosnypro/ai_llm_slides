#!/usr/bin/env python3
"""Generate the thin blue leader-curve PNG for slide 009 (600dpi transparent).
Frame-verified path (measure12 loose-bluish trace): starts at the blue callout's
right edge (~391,150), drops just right of the border (x~400, y150..183), sweeps
down-right THROUGH the measured points (417,189) (427,193) (440,198) (471,213)
(482,218), runs BEHIND the decoder (hidden mid-section), re-emerges below it and
descends (656,295) (677,304) (695,312), meeting the backprop panel's top border
at (~703,314). Drawn BEFORE the decoder/panel so the middle stays hidden, exactly
as in the original frame's z-order.
Washed 1px line reads (187..216, 185..214, 206..236) over beige -> stroke #8088C0 @1.1px.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets"
DPI = 600
BLUE = "#8088C0"

def quad(p0, p1, p2, n=200):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * np.array(p0) + 2 * t * (1 - t) * np.array(p1) + t ** 2 * np.array(p2)

x0, y0, x1, y1 = 388, 146, 708, 320
w, h = x1 - x0, y1 - y0
fig = plt.figure(figsize=(w / 72, h / 72), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(x0, x1); ax.set_ylim(y1, y0)
ax.axis("off")
LW = 1.1
segs = [
    quad((391, 150), (401, 152), (401, 170)),   # leave callout edge, turn down
    np.array([[401, 170], [401, 182]]),          # near-vertical drop
    quad((401, 182), (410, 187), (424, 192)),   # bend into the diagonal
    quad((424, 192), (470, 209), (482, 218)),   # diagonal (measured points)
    quad((482, 218), (590, 262), (656, 295)),   # behind decoder (inferred, slope ~0.44)
    quad((656, 295), (676, 303), (695, 312)),   # re-emerge, flatten
    quad((695, 312), (700, 314.5), (704, 315)), # meet the panel top border
]
for pts in segs:
    ax.plot(pts[:, 0], pts[:, 1], lw=LW, color=BLUE, solid_capstyle="round")
fig.savefig(f"{OUT}/bluecurve009.png", transparent=True)
plt.close(fig)
print("bluecurve009", f"bbox=({x0},{y0})-({x1},{y1}) embedWH=({w/72:.4f},{h/72:.4f})in")
