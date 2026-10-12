#!/usr/bin/env python3
"""Corrected container asset for slide 019 (attempt 3): the peer's container_019.png used
bbox x191..661 (right border at ~658, contaminated by the classif->pred arrow in
measure_original2), but the original's dashes measure only to x~629 — the right border is
hidden BEHIND the Classification box (x532..630). LO's native dash preset also renders a
~24px dash period (selfcheck attempt 1/2) vs the original's (3.5,3.5). Regenerate with the
peer's matplotlib dash pattern at corrected geometry. 600dpi transparent, 1 frame px = 1pt."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
DPI = 600
RED = "#A00000"
PEACH = "#F6DEC2"

x0, y0, x1, y1 = 191, 193, 633, 276
w, h = x1 - x0, y1 - y0
fig = plt.figure(figsize=(w / 72, h / 72), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(x0, x1); ax.set_ylim(y1, y0); ax.axis("off")
p = FancyBboxPatch((194, 196), 630 - 194, 273 - 196,
                   boxstyle="round,pad=0,rounding_size=10",
                   linewidth=2.0, edgecolor=RED, facecolor=PEACH,
                   linestyle=(0, (3.5, 3.5)))
ax.add_patch(p)
fig.savefig(f"{OUT}/container_v2_019.png", transparent=True)
plt.close(fig)
side = {"name": "container_v2_019", "bbox": [x0, y0, x1, y1], "embed_w_in": w / 72, "embed_h_in": h / 72}
with open(f"{OUT}/container_v2_019.json", "w") as f:
    json.dump(side, f, indent=1)
print("container_v2_019", f"bbox=({x0},{y0})-({x1},{y1}) embedWH=({w/72:.4f},{h/72:.4f})in")
