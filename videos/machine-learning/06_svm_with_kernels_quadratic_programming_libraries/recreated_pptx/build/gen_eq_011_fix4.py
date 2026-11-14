#!/usr/bin/env python3
"""fix4 for eq_011: numeric y-vector, larger red-labeled G/X matrices,
row-vector x matrix for YG, two-line objective (no third-line wrap)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from render_math import fit_row, DPI
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_011")
RED = "#C00000"
BLK = "#000000"


def mat(rows):
    return r"\left[\;\substack{" + r"\\".join(rows) + r"}\;\right]"


G_ROWS = [
    r"\quad x_1\quad x_2\quad x_3\quad x_4",
    r"x_1^T\quad 2\quad 4\quad 11\quad 12",
    r"x_2^T\quad 4\quad 8\quad 22\quad 24",
    r"x_3^T\quad 11\quad 22\quad 65\quad 72",
    r"x_4^T\quad 12\quad 24\quad 72\quad 80",
]
X_ROWS = [
    r"x_1\quad x_2\quad x_3\quad x_4",
    r"1\quad 2\quad 7\quad 8",
    r"1\quad 2\quad 4\quad 4",
]
YG_MAT = mat([
    r"\quad y_1\quad y_2\quad y_3\quad y_4",
    r"y_1\quad 1\quad 1\quad -1\quad -1",
    r"y_2\quad 1\quad 1\quad -1\quad -1",
    r"y_3\quad -1\quad -1\quad 1\quad 1",
    r"y_4\quad -1\quad -1\quad 1\quad 1",
])
ASSETS = [
    ("eq_obj.png", 13, 8.6, 1.05, [
        r"[ +1\alpha_1^2 +2\alpha_1\alpha_2 -5.5\alpha_1\alpha_3 -6\alpha_1\alpha_4 +2\alpha_2\alpha_1 +4\alpha_2^2 -11\alpha_2\alpha_3 -12\alpha_2\alpha_4 -5.5\alpha_3\alpha_1 -11\alpha_3\alpha_2 +32.5\alpha_3^2 +36\alpha_3\alpha_4",
        r"-6\alpha_4\alpha_1 -12\alpha_4\alpha_2 +36\alpha_4\alpha_3 +40\alpha_4^2 ] -[ \alpha_1+\alpha_2+\alpha_3+\alpha_4 ]",
    ]),
    ("eq_X.png", 14, 2.3, 1.45, [BLK + r":\text{X}=\ " + mat(X_ROWS)]),
    ("eq_G.png", 15, 3.3, 1.45, [BLK + r":\text{G}=X^T X\ " + mat(G_ROWS)]),
    ("eq_Y.png", 14, 1.7, 1.45, [
        BLK + r":\substack{y_1\\y_2\\y_3\\y_4}\ \left(\substack{1\\1\\-1\\-1}\right)",
    ]),
    ("eq_YG.png", 13, 4.85, 1.45, [
        BLK + r":\left|\ \overset{y_1\ \ y_2\ \ y_3\ \ y_4}{1\quad 1\quad -1\quad -1}\ \right|\ =\ " + YG_MAT,
    ]),
]
manifest = json.load(open(os.path.join(OUT, "manifest.json")))
for name, size, maxw, maxh, rows in ASSETS:
    canvases = []
    for r in rows:
        c, pt = fit_row(r, size, maxw, maxh / len(rows))
        canvases.append(c)
    w = max(c.shape[1] for c in canvases)
    gap = 8
    h = sum(c.shape[0] for c in canvases) + gap * (len(canvases) - 1)
    canvas = np.zeros((h, w, 4), dtype="uint8")
    y = 0
    for c in canvases:
        canvas[y:y + c.shape[0], 0:c.shape[1]] = c
        y += c.shape[0] + gap
    Image.fromarray(canvas).save(os.path.join(OUT, name))
    manifest[name] = {"w_px": int(w), "h_px": int(h), "w_in": round(w / DPI, 5), "h_in": round(h / DPI, 5)}
    print(name, manifest[name])
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=2)
