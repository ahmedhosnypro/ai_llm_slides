#!/usr/bin/env python3
"""Slide 033 pass 7: 1px scanline strips + core-color sampling."""
from PIL import Image
import numpy as np
from collections import Counter

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg").convert("RGB")
A = np.asarray(IM).astype(int)

def strip(name, y, x0, x1, tol=26):
    """run-length colors along one scanline"""
    print(f"--- strip {name} y={y} x{x0}..{x1} ---")
    runs = []
    prev = None
    for x in range(x0, x1+1):
        c = tuple(A[y, x])
        if prev is None or max(abs(c[i]-prev[0][i]) for i in range(3)) > tol:
            runs.append([c, x, x])
            prev = runs[-1]
        else:
            runs[-1][2] = x
    out = []
    for c, a, b in runs:
        if b - a >= 1 or True:
            out.append(f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}[{a}{'..' + str(b) if b > a else ''}]")
    print("  " + " ".join(out))

def core(name, x0, y0, x1, y1, thr=140):
    sub = A[y0:y1+1, x0:x1+1].reshape(-1, 3)
    dk = sub[sub.max(axis=1) < thr]
    if len(dk) == 0:
        print(f"{name}: no core <{thr}"); return
    c = Counter(map(tuple, dk)).most_common(3)
    print(f"{name}: core {[(f'#{r:02X}{g:02X}{b:02X}', n) for (r, g, b), n in c]} (n_dark={len(dk)})")

# container row 1: cell structure
strip("L-container row1", 244, 59, 140)
strip("L-container row1 top", 238, 59, 140)
# W_k box + vector + K label row 1
strip("W_k row1", 246, 140, 260)
strip("Klabel row1", 234, 200, 260)
# V-side row 2: from circles to W_v boxes
strip("V row2", 288, 585, 760)
strip("V label row2", 283, 620, 700)
# sigma column row 2: circle/asterisk region
strip("circle row2", 288, 500, 590)
# Y2 box region: horizontal scan at label/border rows
strip("Y2 row130", 130, 520, 660)
strip("Y2 row113", 113, 520, 660)
strip("Y2 row148", 148, 520, 660)
# legend internals
strip("legend mid", 486, 730, 915)
strip("legend caption", 520, 730, 915)
# sentence row
strip("sentence row", 494, 175, 500)
strip("sentence X2", 490, 250, 330)
# query path
strip("q2 Wq", 452, 260, 330)
strip("q2 label", 415, 260, 330)
# title core colors
core("title L1 'S' (x221..244)", 221, 58, 244, 72, 120)
core("title L1 blue span? (x496..536)", 496, 62, 536, 72, 160)
core("title L1 (x597..614)", 597, 58, 614, 72, 160)
core("title L2 black (x205..214)", 205, 84, 214, 95, 120)
core("title L2 red X (x405..423)", 405, 84, 423, 95, 160)
core("title L2 red X2 (x701..718)", 701, 84, 718, 101, 160)
# K label color
core("K4 label", 236, 228, 252, 242, 150)
core("V2 label", 636, 310, 652, 324, 150)
core("DP 'Dot' label", 286, 198, 306, 212, 150)
core("DP 'K2q'", 346, 197, 370, 213, 150)
core("Soft max text", 467, 264, 480, 295, 150)
core("Sigma glyph", 578, 199, 588, 213, 150)
core("Y2 label green", 550, 149, 574, 167, 170)
core("pill text Similarity", 262, 168, 336, 182, 190)
core("W box label row1", 150, 233, 200, 259, 150)
# border colors
core("DP border top", 270, 192, 300, 197, 200)
core("W_k border", 148, 233, 200, 238, 200)
core("container L border top", 59, 225, 139, 231, 200)
core("softmax border", 456, 300, 460, 320, 200)
core("legend border", 735, 466, 905, 472, 200)
core("sentence border", 180, 473, 490, 479, 200)
core("X2 magenta border row", 261, 472, 336, 507, 220)
# dots color
core("dot1", 326, 242, 335, 251, 170)
# block arrow color
core("blockarrow", 266, 511, 287, 528, 190)
# emphasis circle: reddened-peach extent
sub = A[290:355, 185:275]
r, g, b = sub[:,:,0], sub[:,:,1], sub[:,:,2]
m = (r - g > 55) & (r - b > 40)
ys, xs = np.where(m)
if len(ys):
    print(f"emphasis circle reddened bbox: x {185+xs.min()}..{185+xs.max()} y {290+ys.min()}..{290+ys.max()} n={len(ys)}")
    cy, cx = 290+int(ys.mean()), 185+int(xs.mean())
    print(f"  centroid ({cx},{cy}); blend core color:", Counter(map(tuple, sub[m])).most_common(2))
