#!/usr/bin/env python3
import json
import os
import sys

import numpy as np
from PIL import Image

BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
import render_math as rm

OUT = os.path.join(BUILD, "eq_038")
MAN_PATH = os.path.join(OUT, "rb3_manifest.json")
MAN = json.load(open(MAN_PATH))


def emit(name, rows, size, maxw, maxh, left=False, rowgap=8):
    segs = [rm.parse_row(r) for r in rows]
    meas = []
    for sg in segs:
        w = sum(rm.measure_segment(lt, c, size)[0] for c, lt in sg)
        h = max(rm.measure_segment(lt, c, size)[1] for c, lt in sg)
        meas.append((w, h))
    scale = min(maxw / max(w for w, _ in meas),
                maxh / (sum(h for _, h in meas) + rowgap * (len(rows)-1) / rm.DPI))
    pt = max(7.0, size * scale * 0.995)
    canvases = [rm.render_row(r, pt) for r in rows]
    w = max(c.shape[1] for c in canvases)
    h = sum(c.shape[0] for c in canvases) + rowgap * (len(rows)-1)
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    y = 0
    for c in canvases:
        x = 0 if left else (w-c.shape[1])//2
        canvas[y:y+c.shape[0], x:x+c.shape[1]] = c
        y += c.shape[0] + rowgap
    Image.fromarray(canvas).save(os.path.join(OUT, name+".png"))
    MAN[name] = {"file": "eq_038/"+name+".png", "w_in": round(w/rm.DPI,5),
                 "h_in": round(h/rm.DPI,5), "pt": round(pt,2)}
    print(name, MAN[name])


def vec(name, a, b):
    emit(name, [f"CC0000:\\left(\\overset{{{a}}}{{{b}}}\\right)^T"], 24, .8, .65)


for name, a, b in [("x1",1,1),("x2",2,2),("x3",7,4),("x4",8,4),
                   ("T1",2,3),("T2",4,5),("T3",6,2)]:
    vec("fix3_vec_"+name, a, b)

emit("fix3_dual", [
    "0000CC:\\mathrm{Minimize}\\ \\mathcal{L}_D(\\alpha)=\\frac{1}{2}"
    "{\\sum}_{j=1}^{N}{\\sum}_{i=1}^{N}\\alpha_i\\alpha_j y_i y_j"
    "[X_i^T X_j+1]^2-{\\sum}_{i=1}^{N}\\alpha_i"
], 22, 10.6, .55)

emit("fix3_qp", [
    "CC0000:\\mathrm{Minimize:}\\ [+4.5\\alpha_1^2+12.5\\alpha_1\\alpha_2"
    "-72\\alpha_1\\alpha_3-84.5\\alpha_1\\alpha_4",
    "000000:+12.5\\alpha_2\\alpha_1+40.5\\alpha_2^2-264.5\\alpha_2\\alpha_3"
    "-312.5\\alpha_2\\alpha_4",
    "000000:-72\\alpha_3\\alpha_1-264.5\\alpha_3\\alpha_2+2178\\alpha_3^2"
    "+2664.5\\alpha_3\\alpha_4",
    "000000:-84.5\\alpha_4\\alpha_1-312.5\\alpha_4\\alpha_2+2664.5\\alpha_4\\alpha_3"
    "+3280.5\\alpha_4^2]",
    "0000CC:-[\\alpha_1+\\alpha_2+\\alpha_3+\\alpha_4]"
], 18, 10.4, 1.25, left=True, rowgap=2)

emit("fix3_cons_l", [
    "000000:\\sum\\alpha_i y_i=0\\ \\Rightarrow\\ \\alpha_1+\\alpha_2-\\alpha_3-\\alpha_4=0",
    "000000:\\alpha_i\\leq C\\ \\Rightarrow\\ \\alpha_1\\leq1,\\alpha_2\\leq1,"
    "\\alpha_3\\leq1,\\alpha_4\\leq1",
    "000000:\\alpha_i\\geq0\\ \\Rightarrow\\ \\alpha_1\\geq0,\\alpha_2\\geq0,"
    "\\alpha_3\\geq0,\\alpha_4\\geq0"
], 15, 7.0, .85, left=True, rowgap=3)

json.dump(MAN, open(MAN_PATH,"w"), indent=1)
