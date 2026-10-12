#!/usr/bin/env python3
"""Asset fixes for slide 019 (600dpi transparent, exact-size embed, 1 frame px = 1pt).

Verification of the predecessor's gen_assets_019.py against the frame found:
  - greenfan: head tips 5-6px too short (measured apexes y255-265, generated 261-265)
    and the leftmost head apex at x~221 (generated 228). Regenerated with measured tips.
  - pencil: generated pointing up-RIGHT (tip lower-left); the frame's pencil points
    UP-LEFT (tip ~(248,208), body down-right to ~(268,232)) — direction was reversed.
    Regenerated with the measured orientation (+ detached lead dot at (246.5,206.5)).
  - container_019.png: geometry wrong (x194..658 from an arrow-contaminated bbox; the
    measured container is x200..629) — REPLACED by a native pptxgenjs roundRect in the
    build (certified slide_018 technique). The original PNG stays banked, unused.
  - bluefan_019.png: geometry verified OK (kept); the two ellipse-attach dots are
    missing from it and are drawn as native ellipses in the build.
Outputs: greenfan_019b.png / pencil_019b.png (+ .json sidecars) in build/assets.
"""
import json

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
DPI = 600
GREEN = "#0B7C33"    # feedback green (JPEG core, unchanged from validated bluefan choice)
INK = "#190D63"      # pencil navy (measured core)


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


# ---- green fan: origin dot at verr bottom (770,303.5) + 4 dashed beziers + up heads
# Measured head apexes (y255-265) poke INTO the box bottoms (boxes end y265.5):
#   pre (222,255.5) extr (360,257) sel (470,257.5) classif (588,264.5)
GREEN_CURVES = [
    ((700, 335), (330, 330), (228, 272), (222, 255.5), 6, 266.5),
    ((690, 332), (450, 330), (360, 273), (360, 257), 6, 268),
    ((680, 330), (560, 328), (470, 274), (470, 257.5), 6, 268.5),
    ((720, 325), (640, 330), (588, 276), (588, 264.5), 6, 275.5),
]


def draw_greenfan(ax):
    ax.add_patch(plt.Circle((770, 303.5), 6.5, color=GREEN, lw=0))
    for p1, p2, p3, tip, hw, by in GREEN_CURVES:
        c = cubic((766, 300.5), p1, p2, p3)
        ax.plot(c[:, 0], c[:, 1], lw=1.8, color=GREEN, linestyle=(0, (4, 3.5)), solid_capstyle="round")
        ax.fill(np.array([tip, (tip[0] - hw, by), (tip[0] + hw, by)]), color=GREEN, lw=0)


render("greenfan_019b", 205, 253, 790, 330, draw_greenfan)


# ---- pencil in Pre processing: tip UP-LEFT (247.5,207.5), body down-right to (268,232)
def draw_pencil(ax):
    tip = np.array([247.5, 208.5])
    end = np.array([267.5, 231.5])
    d = end - tip
    L = np.linalg.norm(d)
    dirv = d / L
    nrm = np.array([-dirv[1], dirv[0]])
    W = 4.6

    def pt(s, off):
        return tip + dirv * s + nrm * off

    # detached lead dot just beyond the apex (measured (246.5,206.5) ~1.2px)
    ax.add_patch(plt.Circle(tuple(tip - dirv * 2.2), 1.1, color=INK, lw=0))
    # dark sharpened cone 0..9
    ax.fill(np.array([tip, pt(9, W / 2), pt(9, -W / 2)]), color=INK, lw=0)
    # dark ferrule band 9..13.5
    ax.fill(np.array([pt(9, W / 2), pt(13.5, W / 2), pt(13.5, -W / 2), pt(9, -W / 2)]), color=INK, lw=0)
    # light barrel 13.5..L with dark outline
    barrel = np.array([pt(13.5, W / 2), pt(L, W / 2), pt(L, -W / 2), pt(13.5, -W / 2)])
    ax.fill(barrel, facecolor="#DDDDDD", edgecolor=INK, linewidth=0.7)
    # flat end cap
    ax.fill(np.array([pt(L, W / 2), pt(L + 1.2, W / 2), pt(L + 1.2, -W / 2), pt(L, -W / 2)]), color=INK, lw=0)


render("pencil_019b", 243, 204, 271, 235, draw_pencil)
