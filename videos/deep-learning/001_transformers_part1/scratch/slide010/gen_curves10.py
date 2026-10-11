#!/usr/bin/env python3
"""Generate the curved-stroke PNG assets for slide 010 (600 dpi transparent).

Same mechanism as the certified slide-006 generator (scratch/slide006/gen_curves.py):
curves measured in 960x540 frame px (1px = 1pt = 1/72in); canvas = curve bbox padded;
embedded at exact size (w/72 in) — never rescaled.

Slide-010 measured endpoints (scratch/slide010/measure*.py + vision transcripts):
  feedback A: col1 arrow base (557,194) -> col2 hidden-bar top-left (649.5,252)
  feedback B: col2 arrow base (691,194) -> col3 hidden-bar top-left (783.5,252)
  pink connector: quad (490,343) ctrl (490,388) end (557,388), dusty rose
  dashed attention fan: 1 in-box S-curve + 3 fanning dashed curves hooking up to
    olive arrowheads beneath the decoder hidden bars (heads drawn natively in JS).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets"
DPI = 600
DEC_INK = "#9EA828"   # decoder olive ink (certified parent value)
ROSE = "#C07085"      # dashed attention strokes / pink connector (JPEG-core reconciled)

def quad(p0, p1, p2, n=200):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * np.array(p0) + 2 * t * (1 - t) * np.array(p1) + t ** 2 * np.array(p2)

def render(name, x0, y0, x1, y1, strokes, fills=()):
    w, h = x1 - x0, y1 - y0
    fig = plt.figure(figsize=(w / 72, h / 72), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x1); ax.set_ylim(y1, y0)  # y down
    ax.axis("off")
    for pts, lw, c, dashed in strokes:
        ls = (0, (4, 3)) if dashed else "-"
        ax.plot(pts[:, 0], pts[:, 1], lw=lw, color=c, solid_capstyle="round", linestyle=ls)
    for poly, c in fills:
        ax.fill(poly[:, 0], poly[:, 1], color=c, lw=0)
    fig.savefig(f"{OUT}/{name}.png", transparent=True)
    plt.close(fig)
    print(name, f"bbox=({x0},{y0})-({x1},{y1}) embedWH=({w/72:.4f},{h/72:.4f})in")

# ---- decoder recurrent hooks (parent design, columns fanned +4.5/+8.5) --------
ca = quad((557, 194), (565, 157), (649.5, 252))
render("curve_a10", 551, 184, 655, 257, [(ca, 2.0, DEC_INK, False)])
cb = quad((691, 194), (699, 157), (783.5, 252))
render("curve_b10", 685, 184, 789, 257, [(cb, 2.0, DEC_INK, False)])

# ---- pink connector: pink callout -> context-arc lower end --------------------
pc = quad((490, 343), (490, 388), (557, 388))
render("pink_conn", 486, 339, 561, 392, [(pc, 1.5, ROSE, False)])

# ---- dashed attention fan ------------------------------------------------------
# in-box S-curve: from the node's upper-right, arcs up, descends into the tangle
s1 = quad((332, 254), (344, 235), (365, 240))
s2 = quad((365, 240), (392, 247), (410, 268))
s3 = quad((410, 268), (424, 283), (442, 287))
# three fans exiting the left box and hooking up under the decoder columns
f1a = quad((444, 284), (505, 304), (545, 306))
f1b = quad((545, 306), (554, 299), (558, 287))
f2a = quad((450, 288), (565, 321), (660, 326))
f2b = quad((660, 326), (677, 311), (684, 288))
f3a = quad((456, 292), (625, 336), (750, 330))
f3b = quad((750, 330), (795, 321), (820, 287))
paths = [s1, s2, s3, f1a, f1b, f2a, f2b, f3a, f3b]
xs = np.concatenate([p[:, 0] for p in paths]); ys = np.concatenate([p[:, 1] for p in paths])
render("dash_fan", int(xs.min()) - 4, int(ys.min()) - 4, int(xs.max()) + 4, int(ys.max()) + 4,
       [(p, 1.25, ROSE, True) for p in paths])
