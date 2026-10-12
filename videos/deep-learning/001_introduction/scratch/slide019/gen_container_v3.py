#!/usr/bin/env python3
"""Container asset v3 for slide 019: peach fill + EXPLICIT dash segments (matplotlib
ignored linestyle=(0,(3.5,3.5)) on FancyBboxPatch — v2/v1 rendered SOLID, duty=1.00
measured on the alpha channel). Geometry from the original frame:
  fill+outline zone x194..630 y196..273, corner r10; dash rows 196-198 (dashes 3.5on/3.5off
  along x211..620), bottom row ~273 (dashes x214..618), left border x194 (vertical dashes
  y206..263); right border hidden BEHIND the Classification box (x532..630) — not drawn.
600dpi transparent PNG, 1 frame px = 1pt (8.333 asset px per frame px)."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
DPI = 600
K = DPI / 72.0  # asset px per frame px
RED = "#A00000"
PEACH = "#F6DEC2"

x0, y0, x1, y1 = 191, 193, 633, 276
w, h = x1 - x0, y1 - y0
fig = plt.figure(figsize=(w / 72, h / 72), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(x0, x1); ax.set_ylim(y1, y0); ax.axis("off")
ax.add_patch(FancyBboxPatch((194, 196), 630 - 194, 273 - 196,
                            boxstyle="round,pad=0,rounding_size=10",
                            linewidth=2.0, edgecolor="none", facecolor=PEACH))

LW = 2.0  # pts == frame px here


def dash_line(p0, p1, on=3.5, off=3.5):
    p0 = np.array(p0, float); p1 = np.array(p1, float)
    d = p1 - p0
    L = np.hypot(*d)
    if L < 1e-6:
        return
    u = d / L
    t = 0.0
    while t < L:
        t2 = min(t + on, L)
        a = p0 + u * t
        bpt = p0 + u * t2
        ax.plot([a[0], bpt[0]], [a[1], bpt[1]], color=RED, lw=LW, solid_capstyle="butt")
        t += on + off


def dash_arc(cx, cy, r, a0, a1, on=3.5, off=3.5):
    # angles in degrees, arc drawn clockwise from a0 to a1 (screen coords, y down)
    total = abs(a1 - a0) * np.pi / 180 * r
    n = max(1, int(total / (on + off)))
    t = 0.0
    while t < total:
        t2 = min(t + on, total)
        ang0 = a0 + (t / total) * (a1 - a0)
        ang1 = a0 + (t2 / total) * (a1 - a0)
        p0 = (cx + r * np.cos(np.deg2rad(ang0)), cy + r * np.sin(np.deg2rad(ang0)))
        p1 = (cx + r * np.cos(np.deg2rad(ang1)), cy + r * np.sin(np.deg2rad(ang1)))
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=RED, lw=LW, solid_capstyle="butt")
        t += on + off


# straight dashed edges (corner arcs handled separately)
dash_line((205, 197), (620, 197))    # top (orig dash row 196-198, center ~197)
dash_line((205, 272.5), (620, 272.5))  # bottom (orig dash row ~273)
dash_line((194.5, 207), (194.5, 262))  # left (vertical dashes y206..263)
# right edge NOT drawn — hidden behind Classification in the original
# corner arcs r10 centered (204,206) (204,263) (620,206) (620,263)
dash_arc(204, 206, 10, 180, 270)     # top-left: from (194,206) to (204,196)
dash_arc(620, 206, 10, 270, 360)     # top-right: from (620,196) to (630,206)
dash_arc(204, 263, 10, 90, 180)      # bottom-left: from (204,273) to (194,263)
dash_arc(620, 263, 10, 0, 90)        # bottom-right: from (630,263) to (620,273)

fig.savefig(f"{OUT}/container_v3_019.png", transparent=True)
plt.close(fig)
side = {"name": "container_v3_019", "bbox": [x0, y0, x1, y1], "embed_w_in": w / 72, "embed_h_in": h / 72,
        "note": "explicit 3.5/3.5 dash segments; right border omitted (hidden behind classif)"}
with open(f"{OUT}/container_v3_019.json", "w") as f:
    json.dump(side, f, indent=1)
print("container_v3_019", f"bbox=({x0},{y0})-({x1},{y1}) embedWH=({w/72:.4f},{h/72:.4f})in")
