#!/usr/bin/env python3
"""Regenerate fix_mapping / fix_kernel with full text (M / Kern restored).

Root cause of the clipped labels: render_eq_multi.render_segment masks ink left
of a probe glyph, which chops wide centered text. This script renders without
that probe mask and tight-crops the whole canvas ink bbox instead.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

matplotlib.rcParams["mathtext.fontset"] = "cm"
matplotlib.rcParams["mathtext.default"] = "it"

DPI = 600
PAD_PX = 8
FIG_W, FIG_H = 16, 6

BUILD = os.path.dirname(os.path.abspath(__file__))
EQ = os.path.join(BUILD, "eq_035")
BLUE, RED, BLACK = "0000FF", "FF0000", "000000"


def render_segment(latex, color, fontsize):
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, color=color,
             ha="center", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    baseline_row = int(0.5 * FIG_H * DPI)
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    plt.close(fig)
    if len(rows) == 0:
        raise SystemExit(f"no ink for {latex!r}")
    y0, y1 = max(rows[0] - PAD_PX, 0), min(rows[-1] + PAD_PX, buf.shape[0])
    x0, x1 = max(cols[0] - PAD_PX, 0), min(cols[-1] + PAD_PX, buf.shape[1])
    return buf[y0:y1, x0:x1], baseline_row - y0


def compose(segs, fontsize):
    rendered = [render_segment(latex, "#" + color, fontsize) for _, color, latex in segs]
    max_b = max(b for _, b in rendered)
    heights = [a.shape[0] for a, _ in rendered]
    h = max_b + max(hh - b for (_, b), hh in zip(rendered, heights)) + PAD_PX
    w = sum(a.shape[1] for a, _ in rendered) + 2 * PAD_PX
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    boxes = {}
    x = PAD_PX
    for (arr, b), (label, _, _) in zip(rendered, segs):
        y = max_b - b
        canvas[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
        boxes[label] = [int(x), int(x + arr.shape[1]), int(y), int(y + arr.shape[0])]
        x += arr.shape[1]
    return canvas, boxes


def fit(segs, target_w_in, max_h_in):
    ref, _ = compose(segs, 20.0)
    rw, rh = ref.shape[1] / DPI, ref.shape[0] / DPI
    pt = 20.0 * min(target_w_in / rw, max_h_in / rh, 30.0 / 20.0)
    canvas, boxes = compose(segs, pt)
    return canvas, boxes, pt


JOBS = [
    ("fix_mapping", [
        ["label", RED, r"\mathrm{Mapping}"],
        ["rest", BLACK, r"\ \mathrm{Instead\ of\ using}\ X_i\ \mathrm{(of\ dimension}\ d\mathrm{)\ use}\ \phi(X_i)\ \mathrm{(with\ higher\ dimension)}"],
    ], 9.6, 0.30),
    ("fix_kernel", [
        ["label", RED, r"\mathrm{Kernelization}"],
        ["rest", BLACK, r"\ \mathrm{Instead\ of\ using}\ \phi(X_i)^T\phi(X_j)\ \mathrm{use}\ K(X_i^T,X_j)\ \mathrm{(Where}\ K\ \mathrm{is\ one\ of\ kernel\ functions)}"],
    ], 11.0, 0.30),
]


def main():
    for name, segs, tw, mh in JOBS:
        canvas, boxes, pt = fit(segs, tw, mh)
        out = os.path.join(EQ, name + ".png")
        Image.fromarray(canvas).save(out)
        info = {"w_px": canvas.shape[1], "h_px": canvas.shape[0],
                "fontsize_pt": [pt], "segments": boxes}
        with open(os.path.join(EQ, name + ".json"), "w") as fh:
            json.dump(info, fh, indent=1)
        print(name, canvas.shape[1] / DPI, canvas.shape[0] / DPI, pt)


if __name__ == "__main__":
    main()
