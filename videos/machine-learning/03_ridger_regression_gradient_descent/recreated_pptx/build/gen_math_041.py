#!/usr/bin/env python3
"""Slide 041 equation asset generator (root worker 2 attempt 1).

Renders the three bracketed math blocks of slide 041 as 600dpi transparent
PNGs with matplotlib mathtext, so the parentheses have the frame's tall, thin,
stretchable proportions (the frame's delimiters are math-engine parens: the
48px-tall Initial-W parens carry only a ~2px stroke — a font glyph at that
height would carry a ~3px stroke, so mathtext is the correct engine).

Blocks
  vec_041       Initial W = (4 / -2 / -2)          frame y58..105, parens x330.5 / x352.5
  m41_c1..c6    the six 2-row column vectors       frame y77..107, parens cx-6.5 / cx+6.5
  m41_z         Check-classes matrix (0 7 3 / 0 6 2) frame y83..108, parens x596 / x658

Sidecar contract (same as scripts/render_eq.py): w_px/h_px/w_in/h_in/dpi.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DPI = 600
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUTDIR, exist_ok=True)

matplotlib.rcParams["mathtext.fontset"] = "custom"
matplotlib.rcParams["mathtext.rm"] = "Liberation Sans"
matplotlib.rcParams["mathtext.it"] = "Liber Sans:italic"
matplotlib.rcParams["mathtext.bf"] = "Liberation Sans:bold"


def render(latex, fontsize, color, stem):
    fig = plt.figure(figsize=(6, 3), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.02, 0.5, "$" + latex + "$", fontsize=fontsize, color=color,
             ha="left", va="center")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    alpha = buf[:, :, 3]
    ink = alpha > 8
    cols = np.where(ink.any(axis=0))[0]
    rows = np.where(ink.any(axis=1))[0]
    if not len(cols):
        raise RuntimeError("no ink for " + latex)
    x0, x1 = cols.min(), cols.max()
    y0, y1 = rows.min(), rows.max()
    crop = buf[y0:y1 + 1, x0:x1 + 1]
    im = Image.fromarray(crop)
    png = os.path.join(OUTDIR, stem + ".png")
    im.save(png)
    w, h = im.size
    side = {
        "w_px": w, "h_px": h,
        "w_in": w / DPI, "h_in": h / DPI,
        "dpi": DPI, "fontsize_pt": fontsize, "color": color,
    }
    with open(os.path.join(OUTDIR, stem + ".json"), "w") as f:
        json.dump(side, f, indent=1)
    print("%-10s %5dx%-5d  (%.1f x %.1f pt)  fs=%s" % (stem, w, h, w / DPI * 72, h / DPI * 72, fontsize))
    return side


if __name__ == "__main__":
    # calibration: the frame's digit cap height is 10px for the Initial-W vector
    # and 10-11px for the small matrices -> probe mathtext sizes
    for fs in (12, 13, 14, 15, 16):
        render(r"\begin{pmatrix}4\\-2\\-2\end{pmatrix}", fs, "000000", "probe_v%d" % fs)
