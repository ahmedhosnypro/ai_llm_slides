#!/usr/bin/env python3
import json
import os
import sys
import numpy as np
from PIL import Image

BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
from render_eq_multi import render_segment, DPI

OUT = os.path.join(BUILD, "assets", "resume028_029")
os.makedirs(OUT, exist_ok=True)
MANIFEST = {}


def rgb(color):
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def save(name, arr, mathtext, fontsize, color, baseline=None):
    path = os.path.join(OUT, name + ".png")
    Image.fromarray(arr).save(path)
    h, w = arr.shape[:2]
    MANIFEST[name] = {
        "path": path, "w_px": int(w), "h_px": int(h),
        "w_in": round(w / DPI, 5), "h_in": round(h / DPI, 5),
        "dpi": DPI, "fontsize_pt": fontsize, "color": color,
        "mathtext": mathtext,
    }
    if baseline is not None:
        MANIFEST[name]["baseline_px"] = int(baseline)
        MANIFEST[name]["baseline_frac"] = round(baseline / h, 5)
    print(name, MANIFEST[name]["w_in"], MANIFEST[name]["h_in"])


def row(name, latex, fontsize, color):
    arr, baseline = render_segment(latex, "#" + color, fontsize)
    save(name, arr, latex, fontsize, color, baseline)


def rows(name, parts, fontsize, gap=0):
    rendered = [render_segment(latex, "#" + color, fontsize) for color, latex in parts]
    base = max(b for _, b in rendered)
    height = base + max(a.shape[0] - b for a, b in rendered) + 8
    width = sum(a.shape[1] for a, _ in rendered) + gap * (len(parts) - 1) + 16
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    x = 8
    for (arr, baseline), (color, latex) in zip(rendered, parts):
        y = base - baseline
        canvas[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
        x += arr.shape[1] + gap
    save(name, canvas, [p[1] for p in parts], fontsize, "+".join(p[0] for p in parts), base)


def column(name, entries, fontsize, color, gap=20):
    rendered = [render_segment(entry, "#" + color, fontsize)[0] for entry in entries]
    pitch = max(a.shape[0] for a in rendered) + gap
    inner_w = max(a.shape[1] for a in rendered)
    bar_w = 6
    height = pitch * len(rendered) + 16
    width = inner_w + 2 * bar_w + 36
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    canvas[8:-8, 8:8 + bar_w] = (*rgb(color), 255)
    canvas[8:-8, -8 - bar_w:-8] = (*rgb(color), 255)
    for i, arr in enumerate(rendered):
        x = 8 + bar_w + 10 + (inner_w - arr.shape[1]) // 2
        y = 8 + i * pitch + (pitch - arr.shape[0]) // 2
        canvas[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
    save(name, canvas, entries, fontsize, color)

RED, BLUE, BLACK = "FF0033", "0000CD", "000000"
row("s028_urow", r"\left(a_1^{2}\;a_2^{2}\;\sqrt{2}a_1a_2\;\sqrt{2}a_1\;\sqrt{2}a_2\;1\right)", 12, RED)
column("s028_ucol", [r"b_1^{2}", r"b_2^{2}", r"\sqrt{2}b_1b_2", r"\sqrt{2}b_1", r"\sqrt{2}b_2", r"1"], 14, BLUE, 24)
row("s028_ueq", r"=\phi(a)^{T}\phi(b)", 14, BLACK)
row("s028_where", r"\phi(x)\equiv\left(\overset{x_1}{x_2}\right)^{T}", 14, BLACK)
column("s028_xcol", [r"x_1^{2}", r"x_2^{2}", r"\sqrt{2}x_1x_2", r"\sqrt{2}x_1", r"\sqrt{2}x_2", r"1"], 14, BLACK, 24)
row("s028_leq", r"\phi(a)^{T}\phi(b)=", 14, BLACK)
row("s028_lrow", r"\left(1^{2}\;2^{2}\;\sqrt{2}\,1{\cdot}2\;\sqrt{2}\;2\sqrt{2}\;1\right)", 13, RED)
column("s028_lcol", [r"3^{2}", r"4^{2}", r"\sqrt{2}\,3{\cdot}4", r"3\sqrt{2}", r"4\sqrt{2}", r"1"], 13, BLUE, 18)
row("s028_lprod", r"=\left(1\;4\;2\sqrt{2}\;\sqrt{2}\;2\sqrt{2}\;1\right)", 13, RED)
column("s028_lnum", [r"9", r"16", r"12\sqrt{2}", r"3\sqrt{2}", r"4\sqrt{2}", r"1"], 13, BLUE, 18)

row("s029_rowlabel", r"e^{ab}=", 14, RED)
row("s029_row", r"\left(1\;\dfrac{a}{\sqrt{1!}}\;\dfrac{a^{2}}{\sqrt{2!}}\;\dfrac{a^{3}}{\sqrt{3!}}\;\dfrac{a^{4}}{\sqrt{4!}}\;\ldots\;\ldots\;\infty\right)", 10, BLACK)
column("s029_col", [r"1", r"\dfrac{b}{\sqrt{1!}}", r"\dfrac{b^{2}}{\sqrt{2!}}", r"\dfrac{b^{3}}{\sqrt{3!}}", r"\dfrac{b^{4}}{\sqrt{4!}}", r"\ldots", r"\ldots\;\infty"], 10, BLACK, 12)
rows("s029_phia", [("0000CC", r"\phi(a)"), ("CC0000", r"^{T}")], 16)
row("s029_phib", r"\phi(b)", 16, "0000CC")

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump(MANIFEST, fh, indent=2)
print("wrote", os.path.join(OUT, "manifest.json"))
