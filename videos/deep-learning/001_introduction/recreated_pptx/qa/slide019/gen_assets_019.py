#!/usr/bin/env python3
"""Asset PNGs for slide 019 (600dpi transparent, exact-size embed, 1 frame px = 1pt).
Measured geometry: qa/slide019/measure_original{1..5}.py + *_out.txt.
Assets: dashed peach container, blue curve fan (solid + dashed + heads),
green feedback fan (4 dashed beziers + heads + origin dot), pencil glyph."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
DPI = 600
RED = "#A00000"      # frame-measured red (title/arrows/dashes family)
BLUE = "#1A1078"     # curve navy-blue (JPEG core)
GREEN = "#0B7C33"    # feedback green (JPEG core)
PEACH = "#F6DEC2"    # container fill
INK = "#1A1078"      # pencil outline


def cubic(p0, p1, p2, p3, n=400):
    t = np.linspace(0, 1, n)[:, None]
    return ((1 - t) ** 3 * np.array(p0) + 3 * t * (1 - t) ** 2 * np.array(p1)
            + 3 * t ** 2 * (1 - t) * np.array(p2) + t ** 3 * np.array(p3))


def render(name, x0, y0, x1, y1, draw):
    w, h = x1 - x0, y1 - y0
    fig = plt.figure(figsize=(w / 72, h / 72), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x1)
    ax.set_ylim(y1, y0)  # y down = frame coords
    ax.axis("off")
    draw(ax)
    fig.savefig(f"{OUT}/{name}.png", transparent=True)
    plt.close(fig)
    side = {"name": name, "bbox": [x0, y0, x1, y1], "embed_w_in": w / 72, "embed_h_in": h / 72}
    with open(f"{OUT}/{name}.json", "w") as f:
        json.dump(side, f, indent=1)
    print(name, f"bbox=({x0},{y0})-({x1},{y1}) embedWH=({w/72:.4f},{h/72:.4f})in")


# ---- 1. dashed container: roundRect x194..658 y196..273 r10, peach fill, red dash ----
def draw_container(ax):
    p = FancyBboxPatch((194, 196), 658 - 194, 273 - 196,
                       boxstyle="round,pad=0,rounding_size=10",
                       linewidth=2.0, edgecolor=RED, facecolor=PEACH,
                       linestyle=(0, (3.5, 3.5)))
    ax.add_patch(p)


render("container_019", 191, 193, 661, 276, draw_container)


# ---- 2. blue fan: solid curve ellipse->Input Samples + dashed curve ellipse->Samples Labels
def draw_bluefan(ax):
    # solid: ellipse left (370,134) -> (118,204); head tip (118,212) down into Input top (212)
    c = cubic((370, 134), (240, 132), (130, 158), (118, 204))
    ax.plot(c[:, 0], c[:, 1], lw=2.0, color=BLUE, solid_capstyle="round")
    ax.fill(np.array([(118, 212), (110, 199), (127, 199)]), color=BLUE, lw=0)
    # dashed: ellipse right (468,134) -> (843,201); head tip (846,212) down into Samples top (212)
    d = cubic((468, 134), (650, 130), (790, 155), (843, 201))
    ax.plot(d[:, 0], d[:, 1], lw=2.0, color=BLUE, linestyle=(0, (5, 4)), solid_capstyle="round")
    ax.fill(np.array([(846, 212), (837, 198), (855, 198)]), color=BLUE, lw=0)


render("bluefan_019", 103, 126, 858, 215, draw_bluefan)


# ---- 3. green fan: origin dot at verr bottom (770,303) + 4 dashed beziers + up heads ----
GREEN_CURVES = [
    # (P1, P2, P3-end, head tip, base half-width, base y)
    ((700, 335), (330, 330), (228, 272), (228, 261), 6, 272),
    ((690, 332), (450, 330), (360, 273), (360, 262), 6, 273),
    ((680, 330), (560, 328), (470, 274), (470, 262), 6, 273),
    ((720, 325), (640, 330), (588, 276), (588, 265), 6, 276),
]


def draw_greenfan(ax):
    ax.add_patch(plt.Circle((770, 303), 6.5, color=GREEN, lw=0))
    for p1, p2, p3, tip, hw, by in GREEN_CURVES:
        c = cubic((766, 300), p1, p2, p3)
        ax.plot(c[:, 0], c[:, 1], lw=1.8, color=GREEN, linestyle=(0, (4, 3.5)), solid_capstyle="round")
        ax.fill(np.array([tip, (tip[0] - hw, by), (tip[0] + hw, by)]), color=GREEN, lw=0)


render("greenfan_019", 205, 253, 790, 330, draw_greenfan)


# ---- 4. pencil glyph in Pre processing (tip lower-left ~(246,233), body up-right) ----
def draw_pencil(ax):
    ang = np.deg2rad(-42)
    L, W = 15.0, 4.2          # body length / width
    tippt = np.array([246.5, 233.0])
    dirv = np.array([np.cos(ang), np.sin(ang)])
    nrm = np.array([-dirv[1], dirv[0]])
    base = tippt + dirv * 4.5                       # tip base center
    b1, b2 = base + nrm * W / 2, base - nrm * W / 2
    end = tippt + dirv * L
    e1, e2 = end + nrm * W / 2, end - nrm * W / 2
    # tip (dark)
    ax.fill(np.array([tippt, b1, b2]), color=INK, lw=0)
    # body (white with dark outline)
    ax.fill(np.array([b1, e1, e2, b2]), facecolor="white", edgecolor=INK, linewidth=1.0)
    # eraser band
    m1 = e1 - dirv * 3.0
    m2 = e2 - dirv * 3.0
    ax.fill(np.array([m1, e1, e2, m2]), facecolor="#C9C9C9", edgecolor=INK, linewidth=0.6)


render("pencil_019", 243, 211, 266, 236, draw_pencil)
