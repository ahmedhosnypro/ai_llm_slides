#!/usr/bin/env python3
import json
import os
import sys

BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
from render_eq_multi import render_segment, DPI
import numpy as np
from PIL import Image

OUT = os.path.join(BUILD, "assets", "resume032")
os.makedirs(OUT, exist_ok=True)
EQS = {
    "r1": [("0000FF", r"K(a,b)"), ("000000", r" = "), ("FF0000", r"K_{1}(a,b)"), ("000000", r" + "), ("FF0000", r"K_{2}(a,b)")],
    "r2": [("0000FF", r"K(a,b)"), ("000000", r" = "), ("008000", r"\alpha\,"), ("FF0000", r"K_{1}(a,b)")],
    "r3": [("0000FF", r"K(a,b)"), ("000000", r" = "), ("FF0000", r"K_{1}(a,b)"), ("000000", r" \ast "), ("FF0000", r"K_{2}(a,b)")],
    "r4": [("0000FF", r"K(a,b)"), ("000000", r" = "), ("FF0000", r"K_{1}(a,b)"), ("000000", r" \ast "), ("FF0000", r"K_{2}(a,b)"), ("000000", r" + "), ("008000", r"\alpha\,"), ("FF0000", r"K_{3}(a,b)")],
}
man = {}
for name, parts in EQS.items():
    rendered = [render_segment(latex, "#" + color, 15) for color, latex in parts]
    base = max(b for _, b in rendered)
    h = base + max(a.shape[0] - b for a, b in rendered) + 16
    w = sum(a.shape[1] for a, _ in rendered) + 8 * (len(parts) - 1) + 16
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    x = 8
    for (arr, b), _ in zip(rendered, parts):
        y = base - b
        canvas[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
        x += arr.shape[1] + 8
    path = os.path.join(OUT, name + ".png")
    Image.fromarray(canvas).save(path)
    man[name] = {"path": path, "w_px": int(w), "h_px": int(h), "w_in": round(w / DPI, 5), "h_in": round(h / DPI, 5), "dpi": DPI, "fontsize_pt": 15}
    print(name, man[name]["w_in"], man[name]["h_in"])
with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump(man, fh, indent=2)
