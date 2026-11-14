#!/usr/bin/env python3
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from render_math import fit_row, DPI
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_011")


def mat(rows):
    return r"\left[\;\substack{" + r"\\".join(rows) + r"}\;\right]"


ASSETS = [
    ("eq_dual.png", 15, 12.3, 0.62, [
        r"\text{Maximize }\mathcal{L}_D(\alpha)=\sum_{i=1}^{N}\alpha_i-\frac{1}{2}\sum_{j=1}^{N}\sum_{i=1}^{N}\alpha_i\alpha_j y_i y_j X_i^T X_j\ \Rightarrow\ "
        r"\text{Minimize }\mathcal{L}_D(\alpha)=\frac{1}{2}\sum_{i=1}^{N}\sum_{j=1}^{N}\alpha_i\alpha_j y_i y_j X_i^T X_j-\sum_{i=1}^{N}\alpha_i",
    ]),
    ("eq_YG.png", 13, 3.2, 1.42, [
        r"\text{Y}=(y_i y_j)",
        mat([r"\quad y_1\quad y_2\quad y_3\quad y_4",
             r"y_1\quad 1\quad 1\quad -1\quad -1",
             r"y_2\quad 1\quad 1\quad -1\quad -1",
             r"y_3\quad -1\quad -1\quad 1\quad 1",
             r"y_4\quad -1\quad -1\quad 1\quad 1"]),
    ]),
    ("eq_bounds.png", 12, 3.4, 0.85, [
        r"\alpha_i \leq C:\quad \alpha_1 \leq 1,\ \alpha_2 \leq 1,\ \alpha_3 \leq 1,\ \alpha_4 \leq 1",
        r"\alpha_i \geq 0:\quad \alpha_1 \geq 0,\ \alpha_2 \geq 0,\ \alpha_3 \geq 0,\ \alpha_4 \geq 0",
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
