#!/usr/bin/env python3
"""Slide 046 plot: three single-arm dotted spirals on gray panel, red frame."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "045_055", "slide_046_plot.png")

fig = plt.figure(figsize=(0.540 * 13.33, 0.698 * 7.5), dpi=200)
ax = fig.add_axes([0.13, 0.11, 0.84, 0.84])
ax.set_xlim(0, 38); ax.set_ylim(-12, 44)
ax.set_xticks([0, 5, 10, 15, 20, 25, 30, 35])
ax.set_yticks([-10, 0, 10, 20, 30, 40])
ax.set_facecolor("#FAFAFA")
ax.grid(True, color="#DCDCDC", linewidth=0.6)
ax.axhline(0, color="#7F7F7F", lw=1.0)
fig.patch.set_edgecolor("#C02020"); fig.patch.set_linewidth(2.0)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
for s in ax.spines.values():
    s.set_color("#404040"); s.set_linewidth(1.0)
ax.tick_params(colors="#404040", labelsize=9)

def spiral(cx, cy, r0, r1, turns, phase, color):
    t = np.linspace(0, turns * 2 * np.pi, 500)
    r = r0 + (r1 - r0) * t / (turns * 2 * np.pi)
    ax.plot(cx + r * np.cos(t + phase), cy + r * np.sin(t + phase) * 0.82,
            ":", color=color, lw=2.2, marker="o", markevery=6, markersize=2.5)

spiral(15, 18, 2.0, 13.5, 1.9, 0.9, "#0000FF")   # blue outer
spiral(22, 12, 1.5, 12.0, 2.1, 2.2, "#000000")   # black middle
spiral(19, 18, 2.0, 14.0, 2.0, 4.9, "#FF0000")    # red inner

fig.savefig(OUT, dpi=200, facecolor="#FAFAFA")
print("wrote", OUT)
