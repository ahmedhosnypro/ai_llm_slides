#!/usr/bin/env python3
"""Slide 036 fix3: regenerate b_top / b_bot as segmented composes with
full-height brackets (left[ ... right] cluster extraction, same technique as
gen_eq_035_fix4) so the t1/t2 term segments exist again for the green
highlights (ovals on top, rects on bottom). Updates eq_s36rb5_manifest.json.
"""
import json
import os
import sys

import numpy as np
from PIL import Image

BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
from render_eq_multi import render_segment, DPI, PAD_PX

EQ36 = os.path.join(BUILD, "eq_036")
MANIFEST = os.path.join(EQ36, "eq_s36rb5_manifest.json")
BLUE, RED, BLACK = "0000CC", "FF0000", "000000"
GAP = 40

BODY_TOP = r"\max_{i:y_i=-1}W^T X_i+\min_{i:y_i=+1}W^T X_i"
BODY_BOT = r"\max_{i:y_i=-1}[W_i^T X_j]^2+\min_{i:y_i=+1}[W_i^T X_j]^2"


def keep_cluster(arr, left=True):
    ink = arr[:, :, 3] > 8
    f = 4
    small = ink[::f, ::f]
    h, w = small.shape
    parent = list(range(h * w))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for y in range(h):
        for x in range(w):
            if small[y, x]:
                if x + 1 < w and small[y, x + 1]:
                    union(y * w + x, y * w + x + 1)
                if y + 1 < h and small[y, x]:
                    union(y * w + x, (y + 1) * w + x)
    comps = {}
    for y in range(h):
        for x in range(w):
            if small[y, x]:
                comps.setdefault(find(y * w + x), []).append(x)
    xs = {r: (min(v), max(v)) for r, v in comps.items()}
    if left:
        x0, x1 = min(xs.values(), key=lambda t: t[0])
    else:
        x0, x1 = max(xs.values(), key=lambda t: t[1])
    cut0, cut1 = x0 * f, (x1 + 1) * f
    if left:
        arr[:, cut1:, 3] = 0
    else:
        arr[:, :cut0, 3] = 0
    return arr


def bracket(left, body, fontsize):
    latex = (r"\left[" + body + r"\right.") if left else (r"\left." + body + r"\right]")
    arr, b = render_segment(latex, "#" + BLACK, fontsize)
    arr = keep_cluster(arr, left)
    ink = arr[:, :, 3] > 8
    cols = np.where(ink.any(axis=0))[0]
    rows = np.where(ink.any(axis=1))[0]
    arr = arr[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
    return arr, b


def compose_rendered(rendered, segs):
    max_b = max(b for _, b in rendered)
    heights = [a.shape[0] for a, _ in rendered]
    h = max_b + max(hh - b for (_, b), hh in zip(rendered, heights)) + PAD_PX
    w = sum(a.shape[1] for a, _ in rendered) + 2 * PAD_PX + GAP * (len(rendered) - 1)
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    boxes = {}
    x = PAD_PX
    for (arr, b), (label, _, _) in zip(rendered, segs):
        y = max_b - b
        canvas[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
        boxes[label] = [int(x), int(x + arr.shape[1]), int(y), int(y + arr.shape[0])]
        x += arr.shape[1] + GAP
    return canvas, boxes


def build_b(body, t1, t2, target_w_in, max_h_in):
    segs = [
        ["head", BLUE, r"b=-\frac{1}{2}"],
        ["open", BLACK, None],
        ["max", BLACK, r"\max_{i:y_i=-1}"],
        ["t1", BLUE, t1],
        ["mid", BLACK, r"+\min_{i:y_i=+1}"],
        ["t2", BLUE, t2],
        ["close", BLACK, None],
    ]

    def render_all(pt):
        return [(render_segment(s[2], "#" + s[1], pt) if s[2] else bracket(s[0] == "open", body, pt))
                for s in segs]

    ref, _ = compose_rendered(render_all(20.0), segs)
    rw, rh = ref.shape[1] / DPI, ref.shape[0] / DPI
    pt = 20.0 * min(target_w_in / rw, max_h_in / rh)
    canvas, boxes = compose_rendered(render_all(pt), segs)
    return canvas, boxes, pt


def main():
    with open(MANIFEST) as fh:
        manifest = json.load(fh)
    jobs = [
        ("s36rb4_b_top", BODY_TOP, r"W^T X_i", r"W^T X_i", 7.1, 0.45, "oval"),
        ("s36rb4_b_bot", BODY_BOT, r"[W_i^T X_j]^2", r"[W_i^T X_j]^2", 7.1, 0.60, "rect"),
    ]
    for name, body, t1, t2, tw, mh, hl_shape in jobs:
        canvas, boxes, pt = build_b(body, t1, t2, tw, mh)
        Image.fromarray(canvas).save(os.path.join(EQ36, name + ".png"))
        m = manifest[name]
        m.update(image=name + ".png", w_in=round(canvas.shape[1] / DPI, 5),
                 h_in=round(canvas.shape[0] / DPI, 5), fontsize_pt=round(pt, 3),
                 segments=boxes, highlights=["t1", "t2"], hl_shape=hl_shape)
        print(name, round(canvas.shape[1] / DPI, 3), "x", round(canvas.shape[0] / DPI, 3),
              "in @", round(pt, 2), "pt", "t1", boxes["t1"], "t2", boxes["t2"])
    with open(MANIFEST, "w") as fh:
        json.dump(manifest, fh, indent=1)


if __name__ == "__main__":
    main()
