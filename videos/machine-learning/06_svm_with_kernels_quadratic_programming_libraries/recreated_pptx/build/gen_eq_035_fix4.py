#!/usr/bin/env python3
"""Slide 035 fix4.

fix_b_lower: compose the equation from segments [head, open-bracket, max, t1,
mid, t2, close-bracket]. The brackets are rendered as full-height glyphs by
rendering \\left[BODY\\right. / \\left.BODY\\right] and erasing all ink except
the bracket cluster, so they span the whole max/min body. t1/t2 get exact
segment boxes for the green ovals (they no longer cover the subscripts).

fix_ident: 3-segment compose with a red => arrow between blue sides.
"""
import json
import os

import numpy as np
from PIL import Image
import gen_eq_035_fix3 as base

EQ = base.EQ
BLUE, RED = base.BLUE, base.RED
DPI = base.DPI
PAD = base.PAD_PX
GAP = 40

BODY = r"\max_{i:y_i=-1}W^T X_i+\min_{i:y_i=+1}W^T X_i"


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
                if y + 1 < h and small[y + 1, x]:
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
    ink2 = arr[:, :, 3] > 8
    c2 = np.where(ink2.any(axis=0))[0]
    r2 = np.where(ink2.any(axis=1))[0]
    print("  bracket cols", c2[0], c2[-1], "width", c2[-1] - c2[0] + 1,
          "rows", r2[0], r2[-1])
    return arr


def bracket(left, fontsize):
    latex = (r"\left[" + BODY + r"\right.") if left else (r"\left." + BODY + r"\right]")
    arr, b = base.render_segment(latex, "#" + BLUE, fontsize)
    arr = keep_cluster(arr, left)
    ink = arr[:, :, 3] > 8
    cols = np.where(ink.any(axis=0))[0]
    rows = np.where(ink.any(axis=1))[0]
    arr = arr[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
    return arr, b


def compose_rendered(rendered, fontsize):
    max_b = max(b for _, b in rendered)
    heights = [a.shape[0] for a, _ in rendered]
    h = max_b + max(hh - b for (_, b), hh in zip(rendered, heights)) + PAD
    w = sum(a.shape[1] for a, _ in rendered) + 2 * PAD + GAP * (len(rendered) - 1)
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    boxes = {}
    x = PAD
    for (arr, b), (label, _, _) in zip(rendered, SEGS):
        y = max_b - b
        canvas[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
        boxes[label] = [int(x), int(x + arr.shape[1]), int(y), int(y + arr.shape[0])]
        x += arr.shape[1] + GAP
    return canvas, boxes


def fit_b_lower(target_w_in, max_h_in):
    global SEGS
    SEGS = [
        ["head", BLUE, r"b=-\frac{1}{2}"],
        ["open", BLUE, None],
        ["max", BLUE, r"\max_{i:y_i=-1}"],
        ["t1", BLUE, r"W^T X_i"],
        ["mid", BLUE, r"+\min_{i:y_i=+1}"],
        ["t2", BLUE, r"W^T X_i"],
        ["close", BLUE, None],
    ]
    ref = compose_rendered(
        [(base.render_segment(s[2], "#" + s[1], 20.0) if s[2] else bracket(s[0] == "open", 20.0))
         for s in SEGS], 20.0)
    rw, rh = ref[0].shape[1] / DPI, ref[0].shape[0] / DPI
    pt = 20.0 * min(target_w_in / rw, max_h_in / rh)
    rendered = [(base.render_segment(s[2], "#" + s[1], pt) if s[2] else bracket(s[0] == "open", pt))
                for s in SEGS]
    canvas, boxes = compose_rendered(rendered, pt)
    return canvas, boxes, pt


def main():
    canvas, boxes, pt = fit_b_lower(5.9, 0.75)
    Image.fromarray(canvas).save(os.path.join(EQ, "fix_b_lower.png"))
    info = {"w_px": canvas.shape[1], "h_px": canvas.shape[0],
            "fontsize_pt": [pt], "segments": boxes}
    with open(os.path.join(EQ, "fix_b_lower.json"), "w") as fh:
        json.dump(info, fh, indent=1)
    print("fix_b_lower", canvas.shape[1] / DPI, canvas.shape[0] / DPI, pt)
    print("  boxes", boxes)

    segs = [
        ["lhs", BLUE, r"X_i^T X_j"],
        ["arrow", RED, r"\Rightarrow"],
        ["rhs", BLUE, r"\phi(X_i)^T\phi(X_j)"],
    ]
    canvas, boxes, pt = base.fit(segs, 4.7, 0.40)
    Image.fromarray(canvas).save(os.path.join(EQ, "fix_ident.png"))
    info = {"w_px": canvas.shape[1], "h_px": canvas.shape[0],
            "fontsize_pt": [pt], "segments": boxes}
    with open(os.path.join(EQ, "fix_ident.json"), "w") as fh:
        json.dump(info, fh, indent=1)
    print("fix_ident", canvas.shape[1] / DPI, canvas.shape[0] / DPI, pt)


if __name__ == "__main__":
    main()
