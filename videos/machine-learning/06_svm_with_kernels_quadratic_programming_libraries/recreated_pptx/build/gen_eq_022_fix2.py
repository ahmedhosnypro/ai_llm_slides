#!/usr/bin/env python3
import json, sys
import numpy as np
from PIL import Image

BUILD = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"
sys.path.insert(0, BUILD)
from render_eq_multi import render_segment, DPI, PAD_PX

OUT = BUILD + "/eq_022"
BLACK, RED, BLUE = "#000000", "#FF0000", "#0000FF"

def save(name, canvas):
    path = f"{OUT}/{name}.png"
    Image.fromarray(canvas).save(path)
    meta = {"path": path, "w_px": int(canvas.shape[1]), "h_px": int(canvas.shape[0]),
            "w_in": round(canvas.shape[1] / DPI, 5), "h_in": round(canvas.shape[0] / DPI, 5)}
    with open(path + ".json", "w") as fh:
        json.dump(meta, fh)
    print(name, meta["w_in"], meta["h_in"])

def row(name, segs, fs=14, gap=6):
    parts = [render_segment(latex, color, fs) for color, latex in segs]
    base = max(b for _, b in parts)
    h = max(base + (a.shape[0] - b) for a, b in parts) + 2 * PAD_PX
    w = sum(a.shape[1] for a, _ in parts) + gap * (len(parts) - 1) + 2 * PAD_PX
    c = np.zeros((h, w, 4), np.uint8)
    x = PAD_PX
    for (a, b), _ in zip(parts, segs):
        y = base - b
        c[y:y + a.shape[0], x:x + a.shape[1]] = a
        x += a.shape[1] + gap
    save(name, c)

def col(name, rows, fs=14, color=BLACK, gap=5):
    parts = [render_segment(r, color, fs) for r in rows]
    w = max(a.shape[1] for a, _ in parts) + 2 * PAD_PX + 8
    h = sum(a.shape[0] for a, _ in parts) + gap * (len(parts) - 1) + 2 * PAD_PX
    c = np.zeros((h, w, 4), np.uint8)
    y = PAD_PX
    for a, _ in parts:
        x = PAD_PX + 4 + (w - 2 * PAD_PX - 8 - a.shape[1]) // 2
        c[y:y + a.shape[0], x:x + a.shape[1]] = a
        y += a.shape[0] + gap
    for x in (PAD_PX, w - PAD_PX - 2):
        c[PAD_PX:h - PAD_PX, x:x + 2, 3] = 255
        c[PAD_PX:h - PAD_PX, x:x + 2, :3] = 0
    save(name, c)

def combine(name, canvases, gap=10):
    h = max(c.shape[0] for c in canvases)
    w = sum(c.shape[1] for c in canvases) + gap * (len(canvases) - 1) + 2 * PAD_PX
    out = np.zeros((h, w, 4), np.uint8)
    x = PAD_PX
    for c in canvases:
        y = (h - c.shape[0]) // 2
        out[y:y + c.shape[0], x:x + c.shape[1]] = c
        x += c.shape[1] + gap
    save(name, out)

def col_canvas(rows, fs, color, gap=5):
    parts = [render_segment(r, color, fs) for r in rows]
    w = max(a.shape[1] for a, _ in parts) + 2 * PAD_PX + 8
    h = sum(a.shape[0] for a, _ in parts) + gap * (len(parts) - 1) + 2 * PAD_PX
    c = np.zeros((h, w, 4), np.uint8)
    y = PAD_PX
    for a, _ in parts:
        x = PAD_PX + 4 + (w - 2 * PAD_PX - 8 - a.shape[1]) // 2
        c[y:y + a.shape[0], x:x + a.shape[1]] = a
        y += a.shape[0] + gap
    for x in (PAD_PX, w - PAD_PX - 2):
        c[PAD_PX:h - PAD_PX, x:x + 2, 3] = 255
        c[PAD_PX:h - PAD_PX, x:x + 2, :3] = 0
    return c

def row_canvas(segs, fs, gap=6):
    parts = [render_segment(latex, color, fs) for color, latex in segs]
    base = max(b for _, b in parts)
    h = max(base + (a.shape[0] - b) for a, b in parts) + 2 * PAD_PX
    w = sum(a.shape[1] for a, _ in parts) + gap * (len(parts) - 1) + 2 * PAD_PX
    c = np.zeros((h, w, 4), np.uint8)
    x = PAD_PX
    for (a, b), _ in zip(parts, segs):
        y = base - b
        c[y:y + a.shape[0], x:x + a.shape[1]] = a
        x += a.shape[1] + gap
    return c

A = ["a_{1}", "a_{2}"]
B = ["b_{1}", "b_{2}"]
UA = ["a_{1}^{2}", "a_{2}^{2}", r"\sqrt{2}a_{1}a_{2}", r"\sqrt{2}a_{1}", r"\sqrt{2}a_{2}", "1"]
UB = ["b_{1}^{2}", "b_{2}^{2}", r"\sqrt{2}b_{1}b_{2}", r"\sqrt{2}b_{1}", r"\sqrt{2}b_{2}", "1"]

row("eq_top", [(BLACK, r"\left[a^{T}b+1\right]^{2}")], 16)
combine("eq_vec", [col_canvas(A, 14, RED), row_canvas([(BLACK, ",")], 14), col_canvas(B, 14, BLUE)])
row("eq_calc_ab", [(BLACK, r"\mathrm{Calculate}\ "), (RED, r"a^{T}"), (BLUE, "b")], 13)
combine("eq_mat", [row_canvas([(RED, r"\left[a_{1}\ a_{2}\right]")], 12), col_canvas(B, 12, BLUE)])
row("eq_map", [(BLACK, r"a,\ b\ \Rightarrow\ u,\ v")], 13)
col("eq_colL", UA, 14, RED)
col("eq_colR", UB, 14, BLUE)
row("eq_calc_uv", [(BLACK, r"\mathrm{Calculate}\ "), (RED, r"u^{T}"), (BLUE, "v")], 13)
combine("eq_rowcol", [row_canvas([(RED, r"\left[a_{1}^{2}\ a_{2}^{2}\ \sqrt{2}a_{1}a_{2}\ \sqrt{2}a_{1}\ \sqrt{2}a_{2}\ 1\right]")], 18),
                      row_canvas([(BLACK, r",")], 18), col_canvas(UB, 14, BLUE)], 12)
