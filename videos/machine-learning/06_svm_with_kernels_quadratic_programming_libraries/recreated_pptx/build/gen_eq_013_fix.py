#!/usr/bin/env python3
import json, sys
import numpy as np
from PIL import Image

BUILD = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"
sys.path.insert(0, BUILD)
from render_eq_multi import render_segment, DPI, PAD_PX

OUT = BUILD + "/eq_013"
RED, BLUE, BLACK = "#FF0000", "#0000A0", "#000000"
A = r"\alpha"

def save(name, c):
    p = f"{OUT}/{name}.png"
    Image.fromarray(c).save(p)
    m = {"path": p, "w_in": round(c.shape[1] / DPI, 5), "h_in": round(c.shape[0] / DPI, 5)}
    with open(p + ".json", "w") as f: json.dump(m, f)
    print(name, m["w_in"], m["h_in"])

def row(name, latex, color, fs):
    a, _ = render_segment(latex, color, fs)
    c = np.zeros((a.shape[0] + 2 * PAD_PX, a.shape[1] + 2 * PAD_PX, 4), np.uint8)
    c[PAD_PX:PAD_PX + a.shape[0], PAD_PX:PAD_PX + a.shape[1]] = a
    save(name, c)

def col(name, rows, color, fs, gap=5):
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

obj = (r"[ +1" + A + r"_{1}^{2}+2" + A + r"_{1}" + A + r"_{2}-5.5" + A + r"_{1}" + A + r"_{3}-6" + A + r"_{1}" + A + r"_{4}"
       r"+2" + A + r"_{2}" + A + r"_{1}+4" + A + r"_{2}^{2}-11" + A + r"_{2}" + A + r"_{3}-12" + A + r"_{2}" + A + r"_{4}")
con = (r"-5.5" + A + r"_{3}" + A + r"_{1}-11" + A + r"_{3}" + A + r"_{2}+32.5" + A + r"_{3}^{2}+36" + A + r"_{3}" + A + r"_{4}"
       r"-6" + A + r"_{4}" + A + r"_{1}-12" + A + r"_{4}" + A + r"_{2}+36" + A + r"_{4}" + A + r"_{3}+40" + A + r"_{4}^{2} ]"
       r"-[ " + A + r"_{1}+" + A + r"_{2}+" + A + r"_{3}+" + A + r"_{4}\ ]")
row("obj", "[" + obj[1:], RED, 15)
row("constr", con, BLUE, 14)
row("sumbox", r"\sum_{i}" + A + r"_{i}y_{i}=0", BLACK, 14)
row("exp1", A + r"_{1}+" + A + r"_{2}-" + A + r"_{3}-" + A + r"_{4}=0", RED, 14)
row("alphaleC", A + r"_{i}\leq C_{i}", RED, 14)
row("listle", A + r"_{1}\leq 1,\ " + A + r"_{2}\leq 1,\ " + A + r"_{3}\leq 1,\ " + A + r"_{4}\leq 1", RED, 14)
row("alphage0", A + r"_{i}\geq 0", RED, 14)
row("listge", A + r"_{1}\geq 0,\ " + A + r"_{2}\geq 0,\ " + A + r"_{3}\geq 0,\ " + A + r"_{4}\geq 0", RED, 14)
row("arrow", r"\Rightarrow", BLUE, 18)
row("negalpha", r"-" + A + r"_{1}\leq 0,\ -" + A + r"_{2}\leq 0,\ -" + A + r"_{3}\leq 0,\ -" + A + r"_{4}\leq 0", RED, 14)
row("gxleh", r"\mathbf{G}\ x\ \leq\ \mathbf{h}", RED, 15)
row("axeb", r"\mathbf{A}\ x\ =\ \mathbf{b}", RED, 15)
for i, vals in enumerate(["-1\ \ 0\ \ 0\ \ 0", "0\ \ -1\ \ 0\ \ 0", "0\ \ 0\ \ -1\ \ 0", "0\ \ 0\ \ 0\ \ -1", "1\ \ 0\ \ 0\ \ 0", "0\ \ 1\ \ 0\ \ 0", "0\ \ 0\ \ 1\ \ 0", "0\ \ 0\ \ 0\ \ 1"], 1):
    row(f"g_row{i}", vals, BLACK, 13)
col("alphavec", [A + f"_{{{i}}}" for i in range(1, 5)], RED, 14)
for i, v in enumerate(["0", "0", "0", "0", "1", "1", "1", "1"], 1):
    row(f"h_row{i}", v, BLACK, 13)
row("arow", r"A=\left[1\ 1\ -1\ -1\right]_{1\times 4}", RED, 15)
row("brow", r"b=\left[0\right]_{1\times 1}", RED, 15)
col("hvec", ["0", "0", "0", "0", "1", "1", "1", "1"], BLACK, 10, gap=3)
col("sol", [r"\alpha_{1}=0.0000002,", r"\alpha_{2}=0.06897,", r"\alpha_{3}=0.06897,", r"\alpha_{4}=0.0000008"], RED, 16, gap=5)
