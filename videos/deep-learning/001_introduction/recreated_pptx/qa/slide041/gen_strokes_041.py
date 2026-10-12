#!/usr/bin/env python3
"""Hand-drawn stroke PNGs for slide 041 (600dpi transparent, exact-size embed).
Same certified mechanism as qa/slide009/gen_curves_009.py / qa/slide016/gen_curves_016.py
(matplotlib strokes, 600 dpi, transparent; embed at w/72 x h/72 in, never rescaled).

Traced from unique_slides/slide_041.jpg (960x540, 1px=1pt):

1. arrow_041.png — the big hand swoosh. ONE stroke: starts tapering at (463,169.5),
   rises right over the convolving grid's top row (apex ~(585,155.8), measured band
   y155-156 x554..620), then descends right-down (measured midline (625,158),
   (640,162), (656,166), (672,170)) and ends entering the Result '4' cell at
   ~(676,175). Arrowhead = filled wedge, tip (688,178) pointing down-right INTO the
   '4' cell, barbs (671,168.5)/(680,165.5) (measured widening y167..177 x664..687;
   the head's last px are entangled with the '4' digit — wedge models the on-white
   part, closed-loop F1 verifies).
   Stroke core (17,17,9) = black, band ~2.5-3px -> lw 2.6.
   Label 'g' descenders (y<=158, x495..575) are NOT part of the stroke (excluded).

2. brace_041.png — the wide shallow hand brace under "Inner product" (measured
   pale rose, darkest core (157,128,132) = #9D8084; NOT the spec's red estimate):
   spine x768..772 y355..364 (vertical, touches the label baseline), arms sweep
   down-outward: left (770,363)->(735,371.5)->(706,372.5)->tail (699.5,383.5);
   right (770,363)->(823,369.7)->(840,372)->tail (838,383.5). lw 1.6.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
DPI = 600
BLACK = "#111111"
ROSE = "#9D8084"

def cubic(p0, p1, p2, p3, n=240):
    t = np.linspace(0, 1, n)[:, None]
    return ((1-t)**3 * np.array(p0) + 3*t*(1-t)**2 * np.array(p1)
            + 3*t**2*(1-t) * np.array(p2) + t**3 * np.array(p3))

def render(name, x0, y0, x1, y1, strokes, fills=()):
    w, h = x1 - x0, y1 - y0
    fig = plt.figure(figsize=(w/72, h/72), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x1); ax.set_ylim(y1, y0)
    ax.axis("off")
    for pts, lw, c in strokes:
        ax.plot(pts[:, 0], pts[:, 1], lw=lw, color=c, solid_capstyle="round")
    for poly, c in fills:
        ax.fill(poly[:, 0], poly[:, 1], color=c, lw=0)
    fig.savefig(f"{OUT}/{name}.png", transparent=True)
    plt.close(fig)
    side = {"name": name, "bbox": [x0, y0, x1, y1], "embed_w_in": w/72, "embed_h_in": h/72}
    with open(f"{OUT}/{name}.json", "w") as f:
        json.dump(side, f, indent=1)
    print(name, f"bbox=({x0},{y0})-({x1},{y1}) embedWH=({w/72:.4f},{h/72:.4f})in")

# ---- arrow: two cubics + wedge head ----
a1 = cubic((463, 169.5), (500, 161), (540, 157.5), (585, 155.8))
a2 = cubic((585, 155.8), (615, 155.3), (648, 159), (674, 172.5))
head = np.array([(688, 178), (671, 168.5), (680, 165.5)])
render("arrow_041", 458, 149, 694, 183,
       [(a1, 2.6, BLACK), (a2, 2.6, BLACK)], [(head, BLACK)])

# ---- brace: spine + two arms ----
spine = np.array([[770.5, 354.5], [770.5, 363.5]])
bl = cubic((770, 363), (730, 371), (702, 371), (699.5, 383.5))
br = cubic((770, 363), (815, 368), (845, 369), (838, 383.5))
render("brace_041", 694, 351, 851, 387,
       [(spine, 2.0, ROSE), (bl, 1.6, ROSE), (br, 1.6, ROSE)])
