#!/usr/bin/env python3
"""Generate beam011.png: the bright yellow-green translucent beam quad.
Canvas slide-pt (392..704, 58..183); quad (516,58),(704,58),(670,183),(392,183).
600 dpi, transparent bg; embedded at exact px/600 size (w=312/72, h=125/72).
Color hashed hex per COLOR LAW (matplotlib); measured core over white (249,248,103)
-> base ~ (250,249,95) at ~85% alpha over white."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets"
DPI = 600
W, H = 312, 125
fig = plt.figure(figsize=(W / 72, H / 72), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(392, 704); ax.set_ylim(183, 58)  # inverted y -> slide coords 1:1
ax.axis("off")
ax.add_patch(Polygon([(516, 58), (704, 58), (670, 183), (392, 183)], closed=True,
                     facecolor=(250 / 255, 249 / 255, 95 / 255, 0.85), edgecolor="none"))
fig.savefig(f"{OUT}/beam011.png", transparent=True)
plt.close(fig)
im = Image.open(f"{OUT}/beam011.png")
print("beam011:", im.size, "embed at", 392 / 72, 58 / 72, im.size[0] / DPI, im.size[1] / DPI)
