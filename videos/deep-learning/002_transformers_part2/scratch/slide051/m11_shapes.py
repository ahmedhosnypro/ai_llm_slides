#!/usr/bin/env python3
"""m11_shapes.py — comprehensive shape extraction with the decoded palette.
Connected components per color class, per panel zone. Reports frame-px bboxes.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_051.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)

CLASSES = {
    "navy":      ((0, 0, 155), 75),
    "steelblue": ((90, 145, 175), 42),
    "graybox":   ((127, 127, 127), 26),
    "lightgray": ((205, 205, 200), 18),
    "tan":       ((218, 197, 162), 26),
    "tanbrown":  ((170, 120, 75), 36),
    "salmon":    ((195, 125, 90), 38),
    "greenband": ((135, 205, 70), 50),
    "redstrip":  ((165, 25, 25), 65),
    "yellow":    ((250, 252, 60), 55),
    "magenta":   ((210, 130, 205), 45),
    "redbrown":  ((172, 101, 97), 32),
    "mintpale":  ((168, 226, 192), 38),
}
ZONES = {
    "ENC": (134, 460, 96, 505),
    "DEC": (566, 890, 96, 505),
}

def comps(mask, min_px=25):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(xs) < min_px:
            continue
        out.append((len(xs), int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())))
    out.sort(reverse=True)
    return out

for zone, (zx0, zx1, zy0, zy1) in ZONES.items():
    print(f"===== {zone} zone frame x {zx0}..{zx1} y {zy0}..{zy1} =====")
    for name, (rgb, tol) in CLASSES.items():
        m = np.abs(im - np.array(rgb)).max(axis=2) <= tol
        mm = np.zeros_like(m)
        mm[zy0:zy1, zx0:zx1] = m[zy0:zy1, zx0:zx1]
        cc = comps(mm)
        if not cc:
            continue
        line = []
        for npx, x0, x1, y0, y1 in cc[:8]:
            line.append(f"n{npx} x{x0}..{x1} y{y0}..{y1}")
        print(f"  {name:10s}: " + " | ".join(line))
