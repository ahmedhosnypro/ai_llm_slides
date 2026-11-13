#!/usr/bin/env python3
import json
import os
import sys

import numpy as np
from PIL import Image

BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
from render_eq_multi import render_segment, DPI, PAD_PX

EQ = os.path.join(BUILD, "eq_035")
BLUE, RED, BLACK = "0000FF", "FF0000", "000000"


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


def lag():
    return [
        ["ld", BLUE, r"\mathcal{L}_D(\alpha)"], ["eq", BLACK, "="],
        ["suma", BLACK, r"{\sum}_{i=1}^{N}"], ["alpha", RED, r"\alpha_i"],
        ["minus", BLACK, "-"], ["half", BLACK, r"\frac{1}{2}"],
        ["sumj", BLACK, r"{\sum}_{j=1}^{N}"], ["sumi", BLACK, r"{\sum}_{i=1}^{N}"],
        ["factors", RED, r"\alpha_i\alpha_j y_i y_j"],
        ["tail", BLUE, r"X_i^T X_j"],
    ]


def w_form():
    return [["w", BLUE, "W"], ["eq", BLACK, "="],
            ["sum", BLACK, r"{\sum}_{i=1}^{N}"], ["alpha", RED, r"\alpha_i"],
            ["y", BLUE, "y_i"], ["x", BLUE, "X_i"]]


def b_form():
    return [
        ["b", BLUE, "b"], ["eq", BLACK, "="], ["minus", BLACK, "-"],
        ["half", BLACK, r"\frac{1}{2}"], ["lb", BLACK, "["],
        ["max", RED, r"\max_{i:y_i=-1}"], ["t1", BLUE, r"W^T X_i"],
        ["plus", BLACK, "+"], ["min", RED, r"\min_{i:y_i=+1}"],
        ["t2", BLUE, r"W^T X_i"], ["rb", BLACK, "]"],
    ]


JOBS = [
    ("fix_lag_upper", lag(), 4.9, 0.70),
    ("fix_lag_lower", lag(), 4.9, 0.70),
    ("fix_w", w_form(), 1.65, 0.70),
    ("fix_b_upper", b_form(), 5.75, 0.70),
    ("fix_b_lower", b_form(), 5.75, 0.70),
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
